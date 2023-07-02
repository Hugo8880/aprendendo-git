from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def __str__(self):
        return f"Nome: {self.nome}\nCPF: {self.cpf}\nData de Nascimento: {self.data_nascimento}\nEndereço: {self.endereco}"


class Conta(ABC):
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        if valor > self._saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False

        self._saldo -= valor
        print("\n=== Saque realizado com sucesso! ===")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        self._saldo += valor
        print("\n=== Depósito realizado com sucesso! ===")
        return True

    @abstractmethod
    def __str__(self):
        pass


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        if valor > self._limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
            return False

        if self.historico.numero_saques >= self._limite_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
            return False

        return super().sacar(valor)

    def __str__(self):
        return f"Agência: {self.agencia}\nC/C: {self.numero}\nTitular: {self.cliente.nome}"


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

    @property
    def numero_saques(self):
        return len([transacao for transacao in self._transacoes if transacao["tipo"] == "Saque"])


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
    menu = """
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(menu).strip().lower()


def filtrar_cliente(cpf, clientes):
    return next((cliente for cliente in clientes if cliente.cpf == cpf), None)


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))

    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))

    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            print(f"Tipo: {transacao['tipo']}")
            print(f"Valor: {transacao['valor']}")
            print(f"Data: {transacao['data']}")
            print("---------------------------------------")

    print(f"Saldo: R${conta.saldo}")
    print("=========================================")


def criar_conta(clientes):
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    numero_conta = input("Informe o número da conta: ").strip()
    limite = float(input("Informe o limite da conta corrente (opcional): ") or "500")
    limite_saques = int(input("Informe o limite de saques da conta corrente (opcional): ") or "3")

    conta = ContaCorrente(numero_conta, cliente, limite, limite_saques)
    cliente.adicionar_conta(conta)
    print("\n=== Conta criada com sucesso! ===")


def listar_contas(clientes):
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    contas = cliente.contas

    if not contas:
        print("\n@@@ Cliente não possui contas! @@@")
    else:
        print("\n============== CONTAS ===============")

        for conta in contas:
            print(conta)

        print("=====================================")


def novo_usuario(clientes):
    nome = input("Informe o nome do novo cliente: ").strip()
    data_nascimento = input("Informe a data de nascimento do novo cliente (DD/MM/AAAA): ").strip()
    cpf = input("Informe o CPF do novo cliente: ").strip()
    endereco = input("Informe o endereço do novo cliente: ").strip()

    cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
    clientes.append(cliente)
    print("\n=== Novo cliente cadastrado com sucesso! ===")


def main():
    clientes = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)
        elif opcao == "s":
            sacar(clientes)
        elif opcao == "e":
            exibir_extrato(clientes)
        elif opcao == "nc":
            criar_conta(clientes)
        elif opcao == "lc":
            listar_contas(clientes)
        elif opcao == "nu":
            novo_usuario(clientes)
        elif opcao == "q":
            print("\n=== Obrigado por utilizar o banco! ===")
            break
        else:
            print("\n@@@ Opção inválida! Tente novamente. @@@\n")


if __name__ == "__main__":
    main()
