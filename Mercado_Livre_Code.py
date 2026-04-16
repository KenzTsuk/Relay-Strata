import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

ARQUIVO_CUPONS = "cupons.json"

TABELA_PRECOS_FRETE = {
    (0, 0.3): 11.97,
    (0.3, 0.5): 12.87,
    (0.5, 1): 13.47,
    (1, 2): 14.07,
    (2, 3): 14.97,
    (3, 4): 16.17,
    (4, 5): 17.07,
    (5, 9): 44.45,
    (9, 13): 65.95,
    (13, 17): 73.45,
    (17, 23): 85.95,
    (23, 30): 98.95,
    (30, 40): 109.45,
    (40, 50): 116.95,
    (50, 60): 124.95,
    (60, 70): 187.43,
}

FATOR_DISTANCIA_ZONA = {
    1: 1.0,
    2: 1.2,
    3: 1.5,
}

class Produto:

    def __init__(self, nome: str, preco: float, peso_kg: float,
                 altura_cm: float = 0, largura_cm: float = 0,
                 comprimento_cm: float = 0, categoria: str = "outros"):
        self.nome = nome
        self.preco = preco
        self.peso_kg = peso_kg
        self.altura_cm = altura_cm
        self.largura_cm = largura_cm
        self.comprimento_cm = comprimento_cm
        self.categoria = categoria

    @property
    def volume_cm3(self) -> float:
        return self.altura_cm * self.largura_cm * self.comprimento_cm

    @property
    def peso_volumetrico(self) -> float:
        if self.volume_cm3 == 0:
            return 0
        return self.volume_cm3 / 6000

    @property
    def peso_cobrado(self) -> float:
        return max(self.peso_kg, self.peso_volumetrico)

    def __repr__(self):
        return (f"{self.nome} (R${self.preco:.2f}, {self.peso_kg}kg, "
                f"vol: {self.volume_cm3:.0f}cm³)")


class Pedido:
    def __init__(self, zona: int, reputacao_vendedor: str = "verde",
                 modalidade_frete: str = "normal"):
        self.zona = zona
        self.produtos: List[Produto] = []
        self.cupom: Optional['Cupom'] = None
        self.reputacao_vendedor = reputacao_vendedor
        self.modalidade_frete = modalidade_frete

    def adicionar_produto(self, produto: Produto):
        self.produtos.append(produto)

    @property
    def preco_total(self) -> float:
        return sum(p.preco for p in self.produtos)

    @property
    def peso_total_cobrado(self) -> float:
        return sum(p.peso_cobrado for p in self.produtos)

    @property
    def peso_total_fisico(self) -> float:
        return sum(p.peso_kg for p in self.produtos)

    def calcular_frete_base_por_peso(self, peso_cobrado: float) -> float:
        
        for (limite_inf, limite_sup), valor in TABELA_PRECOS_FRETE.items():
            if limite_inf <= peso_cobrado < limite_sup:
                return valor
        return 250.0

    def aplicar_desconto_reputacao(self, frete_base: float) -> float:

        descontos = {
            "verde": 0.20,
            "amarela": 0.10,
            "vermelha": 0.0,
        }
        desconto = descontos.get(self.reputacao_vendedor, 0)
        return frete_base * (1 - desconto)

    def aplicar_modalidade_frete(self, frete_com_desconto: float) -> float:
        
        if self.modalidade_frete == "expresso":
            return frete_com_desconto * 1.3
        return frete_com_desconto

    def calcular_frete(self) -> Optional[float]:

        if self.zona not in FATOR_DISTANCIA_ZONA:
            return None

        frete_base = self.calcular_frete_base_por_peso(self.peso_total_cobrado)

        frete_com_distancia = frete_base * FATOR_DISTANCIA_ZONA[self.zona]

        frete_com_reputacao = self.aplicar_desconto_reputacao(frete_com_distancia)

        frete_final = self.aplicar_modalidade_frete(frete_com_reputacao)

        return max(frete_final, 5.0)

    def aplicar_cupom(self, cupom: 'Cupom'):
        self.cupom = cupom

    def aplicar_politica_frete_gratis(self, frete_calculado: float) -> Tuple[float, bool]:

        if self.cupom and self.cupom.tipo == "frete_gratis":
            return 0.0, True

        if self.preco_total >= 79.0:
            return 0.0, True
        elif 19.0 <= self.preco_total < 79.0:

            return 0.0, True
        return frete_calculado, False

    def finalizar(self) -> Tuple[float, float, str]:

        frete = self.calcular_frete()
        if frete is None:
            raise ValueError("Zona inválida para cálculo de frete.")

        frete, is_frete_gratis = self.aplicar_politica_frete_gratis(frete)

        if self.cupom:
            preco_final, frete_final, msg_cupom = self.cupom.aplicar(self.preco_total, frete)
        else:
            preco_final, frete_final, msg_cupom = self.preco_total, frete, "Nenhum cupom aplicado."

        if is_frete_gratis and not (self.cupom and self.cupom.tipo == "frete_gratis"):
            msg_frete = "Frete Grátis aplicado por política do Mercado Livre!"
        elif is_frete_gratis and self.cupom and self.cupom.tipo == "frete_gratis":
            msg_frete = "Frete Grátis aplicado pelo cupom!"
        else:
            msg_frete = f"Frete calculado com base no peso e distância."

        # Combina as mensagens
        mensagem_final = f"{msg_cupom} {msg_frete}".strip()
        return preco_final, frete_final, mensagem_final

    def exibir_detalhes_frete(self):

        print("\n--- ANÁLISE DETALHADA DO FRETE ---")
        print(f"Peso físico total: {self.peso_total_fisico:.2f}kg")
        print(f"Peso cúbico (volumétrico) total: {self.peso_total_cobrado - self.peso_total_fisico:.2f}kg")
        print(f"Peso cobrado para o frete: {self.peso_total_cobrado:.2f}kg")
        print(f"Valor base por peso (tabela): R${self.calcular_frete_base_por_peso(self.peso_total_cobrado):.2f}")
        print(f"Fator de distância (zona {self.zona}): {FATOR_DISTANCIA_ZONA[self.zona]}x")
        print(f"Desconto por reputação ({self.reputacao_vendedor}): "
              f"{'Sim' if self.reputacao_vendedor != 'vermelha' else 'Não'}")
        print(f"Modalidade: {self.modalidade_frete}")
        print("-" * 40)

class Cupom:
    TIPOS = ["percentual", "fixo", "frete_gratis"]

    def __init__(self, codigo: str, tipo: str, valor: float, data_validade: datetime):
        if tipo not in self.TIPOS:
            raise ValueError(f"Tipo inválido. Use um de: {self.TIPOS}")
        self.codigo = codigo.upper()
        self.tipo = tipo
        self.valor = valor
        self.data_validade = data_validade

    @property
    def valido(self) -> bool:
        return datetime.now() <= self.data_validade

    def aplicar(self, preco_total: float, frete: float) -> Tuple[float, float, str]:
        if not self.valido:
            return preco_total, frete, f"Cupom {self.codigo} expirado!"

        if self.tipo == "percentual":
            desconto = preco_total * self.valor
            novo_preco = preco_total - desconto
            return novo_preco, frete, f"Cupom {self.codigo}: {self.valor*100:.0f}% de desconto (R${desconto:.2f})"
        elif self.tipo == "fixo":
            desconto = min(self.valor, preco_total)
            novo_preco = preco_total - desconto
            return novo_preco, frete, f"Cupom {self.codigo}: R${desconto:.2f} de desconto"
        elif self.tipo == "frete_gratis":
            return preco_total, 0.0, f"Cupom {self.codigo}: frete grátis!"
        else:
            return preco_total, frete, "Erro: tipo de cupom desconhecido"

    def to_dict(self) -> dict:
        return {
            "codigo": self.codigo,
            "tipo": self.tipo,
            "valor": self.valor,
            "data_validade": self.data_validade.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Cupom':
        return cls(
            codigo=data["codigo"],
            tipo=data["tipo"],
            valor=data["valor"],
            data_validade=datetime.fromisoformat(data["data_validade"])
        )


class GerenciadorCupons:
    def __init__(self, arquivo: str = ARQUIVO_CUPONS):
        self.arquivo = arquivo
        self.cupons: Dict[str, Cupom] = {}
        self._carregar()

    def _carregar(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
                for codigo, dados_cupom in dados.items():
                    self.cupons[codigo] = Cupom.from_dict(dados_cupom)
        else:
            self._adicionar_padroes()

    def _adicionar_padroes(self):
        hoje = datetime.now()
        self.cupons["DESC10"] = Cupom("DESC10", "percentual", 0.10, hoje + timedelta(days=30))
        self.cupons["DESC20"] = Cupom("DESC20", "percentual", 0.20, hoje + timedelta(days=15))
        self.cupons["FRETEGRATIS"] = Cupom("FRETEGRATIS", "frete_gratis", 0.0, hoje + timedelta(days=7))
        self.cupons["REAL5"] = Cupom("REAL5", "fixo", 5.0, hoje + timedelta(days=10))
        self._salvar()

    def _salvar(self):
        dados = {codigo: cupom.to_dict() for codigo, cupom in self.cupons.items()}
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)

    def obter_cupom(self, codigo: str) -> Optional[Cupom]:
        codigo = codigo.upper()
        cupom = self.cupons[codigo] if codigo in self.cupons else None
        if cupom and not cupom.valido:
            print(f"⚠️ Cupom {codigo} está expirado (válido até {cupom.data_validade.strftime('%d/%m/%Y')}).")
            return None
        return cupom

    def adicionar_cupom(self, cupom: Cupom):
        self.cupons[cupom.codigo] = cupom
        self._salvar()
        print(f"Cupom {cupom.codigo} adicionado com sucesso!")

    def listar_cupons(self):
        if not self.cupons:
            print("Nenhum cupom cadastrado.")
        else:
            print("\n--- CUPONS DISPONÍVEIS ---")
            for cupom in self.cupons.values():
                status = "Válido" if cupom.valido else "Expirado"
                print(f"{cupom.codigo} - {cupom.tipo} - {cupom.valor} - {status} até {cupom.data_validade.strftime('%d/%m/%Y')}")
            print("----------------------------\n")

def obter_numero(mensagem: str, tipo=float, min_val=None) -> Optional[float]:
    while True:
        try:
            valor = tipo(input(mensagem))
            if min_val is not None and valor < min_val:
                print(f"Valor deve ser >= {min_val}.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Digite um número.")

def obter_zona() -> Optional[int]:
    while True:
        zona = obter_numero("Zona de entrega (1, 2 ou 3): ", int)
        if zona in [1, 2, 3]:
            return zona
        print("Zona inválida. Use 1, 2 ou 3.")


def obter_reputacao() -> str:
    print("\nReputação do vendedor:")
    print("1. Verde (melhor desconto)")
    print("2. Amarela (desconto médio)")
    print("3. Vermelha (sem desconto)")
    opcao = input("Escolha: ")
    if opcao == "1":
        return "verde"
    elif opcao == "2":
        return "amarela"
    else:
        return "vermelha"

def obter_modalidade() -> str:
    print("\nModalidade de frete:")
    print("1. Normal")
    print("2. Expresso (+30% no custo)")
    opcao = input("Escolha: ")
    if opcao == "2":
        return "expresso"
    return "normal"

def criar_produto_interativo() -> Optional[Produto]:
    print("\n--- Novo produto ---")
    nome = input("Nome do produto: ").strip()
    if not nome:
        print("Produto ignorado (nome vazio).")
        return None
    preco = obter_numero("Preço (R$): ", float, 0)
    if preco is None:
        return None
    peso = obter_numero("Peso (kg): ", float, 0)
    if peso is None:
        return None

    incluir_dimensoes = input("Incluir dimensões para cálculo de peso cúbico? (s/n): ").lower() == 's'
    altura = largura = comprimento = 0.0
    if incluir_dimensoes:
        altura = obter_numero("Altura da embalagem (cm): ", float, 0) or 0.0
        largura = obter_numero("Largura da embalagem (cm): ", float, 0) or 0.0
        comprimento = obter_numero("Comprimento da embalagem (cm): ", float, 0) or 0.0

    print("Categorias disponíveis: eletronicos, livros, roupas, outros")
    categoria = input("Categoria do produto: ").strip().lower()
    if categoria not in ['eletronicos', 'livros', 'roupas', 'outros']:
        categoria = 'outros'

    return Produto(nome, preco, peso, altura, largura, comprimento, categoria)


def nova_simulacao(ger_cupons: GerenciadorCupons):
    print("\n--- INICIANDO NOVO PEDIDO ---")
    zona = obter_zona()
    if zona is None:
        return

    reputacao = obter_reputacao()
    modalidade = obter_modalidade()
    pedido = Pedido(zona, reputacao, modalidade)

    while True:
        prod = criar_produto_interativo()
        if prod:
            pedido.adicionar_produto(prod)
            print(f"Produto adicionado: {prod}")
        mais = input("Adicionar outro produto? (s/n): ").lower()
        if mais != 's':
            break

    if not pedido.produtos:
        print("Pedido vazio. Simulação cancelada.")
        return

    print("\n--- RESUMO DO PEDIDO ---")
    for i, p in enumerate(pedido.produtos, 1):
        print(f"{i}. {p.nome} - R${p.preco:.2f} ({p.peso_kg}kg, cubado: {p.peso_volumetrico:.2f}kg)")

    print(f"Subtotal: R${pedido.preco_total:.2f}")
    print(f"Peso total (físico): {pedido.peso_total_fisico:.2f}kg")
    print(f"Peso total (cobrado): {pedido.peso_total_cobrado:.2f}kg")
    print(f"Zona: {zona} (fator {FATOR_DISTANCIA_ZONA[zona]}x)")
    print(f"Reputação: {pedido.reputacao_vendedor}")
    print(f"Modalidade: {pedido.modalidade_frete}")
    pedido.exibir_detalhes_frete()

    cod_cupom = input("\nCódigo do cupom (ou Enter para nenhum): ").strip().upper()
    if cod_cupom:
        cupom = ger_cupons.obter_cupom(cod_cupom)
        if cupom:
            pedido.aplicar_cupom(cupom)
        else:
            print(f"Cupom '{cod_cupom}' não encontrado ou inválido.")

    try:
        preco_final, frete_final, msg = pedido.finalizar()
        print("\n" + "=" * 40)
        print("         CÁLCULO FINAL")
        print("=" * 40)
        print(f"Preço original dos produtos: R${pedido.preco_total:.2f}")
        print(f"Frete original calculado: R${pedido.calcular_frete():.2f}")
        print(f"Desconto aplicado: {msg}")
        print(f"Preço após descontos: R${preco_final:.2f}")
        print(f"Frete final: R${frete_final:.2f}")
        print(f"TOTAL A PAGAR: R${preco_final + frete_final:.2f}")
        print("=" * 40)
    except ValueError as e:
        print(f"Erro no cálculo: {e}")

def gerenciar_cupons(ger_cupons: GerenciadorCupons):
    while True:
        print("\n--- GERENCIAR CUPONS ---")
        print("1. Listar todos os cupons")
        print("2. Adicionar novo cupom")
        print("3. Voltar ao menu principal")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            ger_cupons.listar_cupons()
        elif opcao == "2":
            codigo = input("Código do cupom: ").strip().upper()
            if not codigo:
                print("Código inválido.")
                continue
            print("Tipos disponíveis: percentual, fixo, frete_gratis")
            tipo = input("Tipo: ").strip().lower()
            if tipo not in Cupom.TIPOS:
                print("Tipo inválido.")
                continue
            if tipo == "percentual":
                valor = obter_numero("Valor percentual (ex: 0.15 para 15%): ", float, 0)
                if valor is None or valor > 1:
                    print("Percentual deve estar entre 0 e 1.")
                    continue
            elif tipo == "fixo":
                valor = obter_numero("Valor fixo em R$: ", float, 0)
                if valor is None:
                    continue
            else:
                valor = 0.0

            dias_validade = obter_numero("Dias de validade (a partir de hoje): ", int, 1)
            if dias_validade is None:
                continue
            data_validade = datetime.now() + timedelta(days=dias_validade)

            novo_cupom = Cupom(codigo, tipo, valor, data_validade)
            ger_cupons.adicionar_cupom(novo_cupom)
        elif opcao == "3":
            break
        else:
            print("Opção inválida.")

def exibir_menu():
    print("\n" + "=" * 50)
    print("      SIMULADOR AVANÇADO - MERCADO LIVRE")
    print("=" * 50)
    print("1. Nova simulação de pedido")
    print("2. Gerenciar cupons (listar/adicionar)")
    print("3. Sair")
    print("-" * 50)

def main():
    gerenciador = GerenciadorCupons()
    while True:
        exibir_menu()
        opcao = input("Opção: ").strip()
        if opcao == "1":
            nova_simulacao(gerenciador)
        elif opcao == "2":
            gerenciar_cupons(gerenciador)
        elif opcao == "3":
            print("Encerrando simulador. Obrigado!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()