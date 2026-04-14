import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

ARQUIVO_CUPONS = "cupons.json"
TAXA_BASE_FRETE = 2.50
DISTANCIAS_ZONAS = {1: 10, 2: 25, 3: 50}


class Produto:

    def __init__(self, nome: str, preco: float, peso_kg: float):
        self.nome = nome
        self.preco = preco
        self.peso_kg = peso_kg

    def __repr__(self):
        return f"{self.nome} (R${self.preco:.2f}, {self.peso_kg}kg)"


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


class CalculadoraFrete:
    
    @staticmethod
    def calcular(zona: int, peso_total_kg: float) -> Optional[float]:
        if zona not in DISTANCIAS_ZONAS:
            return None
        distancia_km = DISTANCIAS_ZONAS[zona]
        frete = TAXA_BASE_FRETE * distancia_km * peso_total_kg
        return max(frete, 5.0)


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


class Pedido:

    def __init__(self, zona: int):
        self.zona = zona
        self.produtos: List[Produto] = []
        self.cupom: Optional[Cupom] = None

    def adicionar_produto(self, produto: Produto):
        self.produtos.append(produto)

    @property
    def preco_total(self) -> float:
        return sum(p.preco for p in self.produtos)

    @property
    def peso_total(self) -> float:
        return sum(p.peso_kg for p in self.produtos)

    def calcular_frete(self) -> Optional[float]:
        return CalculadoraFrete.calcular(self.zona, self.peso_total)

    def aplicar_cupom(self, cupom: Cupom):
        self.cupom = cupom

    def finalizar(self) -> Tuple[float, float, str]:
        """Retorna (preco_final, frete_final, mensagem_detalhada)."""
        frete = self.calcular_frete()
        if frete is None:
            raise ValueError("Zona inválida para cálculo de frete.")

        if self.cupom:
            preco_final, frete_final, msg = self.cupom.aplicar(self.preco_total, frete)
        else:
            preco_final, frete_final, msg = self.preco_total, frete, "Nenhum cupom aplicado."

        return preco_final, frete_final, msg


def exibir_menu():
    print("\n" + "=" * 50)
    print("      SIMULADOR AVANÇADO - MERCADO LIVRE")
    print("=" * 50)
    print("1. Nova simulação de pedido")
    print("2. Gerenciar cupons (listar/adicionar)")
    print("3. Sair")
    print("-" * 50)


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
    return Produto(nome, preco, peso)


def nova_simulacao(ger_cupons: GerenciadorCupons):
    print("\n--- INICIANDO NOVO PEDIDO ---")
    zona = obter_zona()
    if zona is None:
        return

    pedido = Pedido(zona)

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
        print(f"{i}. {p.nome} - R${p.preco:.2f} ({p.peso_kg}kg)")
    print(f"Subtotal: R${pedido.preco_total:.2f}")
    print(f"Peso total: {pedido.peso_total:.2f}kg")
    print(f"Zona: {zona} (distância {DISTANCIAS_ZONAS[zona]}km)")

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
        print(f"Frete original (zona {zona}, {pedido.peso_total:.2f}kg): R${pedido.calcular_frete():.2f}")
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
            else:  # frete_gratis
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