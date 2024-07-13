import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
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


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

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
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n!!! Operação falhou! Você não tem saldo suficiente. !!!")

        elif valor > 0:
            self._saldo -= valor
            print("\n*** Saque realizado com sucesso! ***")
            return True

        else:
            print("\n!!! Operação falhou! O valor informado é inválido. !!!")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n*** Depósito realizado com sucesso! ***")
        else:
            print("\n!!! Operação falhou! O valor informado é inválido. !!!")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n!!! Operação falhou! O valor do saque excede o limite. !!!")

        elif excedeu_saques:
            print("\n!!! Operação falhou! Número máximo de saques excedido. !!!")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


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
                "data": datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
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
    menu = """\n
    =================== MENU ====================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [n]\tNova conta
    [l]\tListar contas
    [u]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n!!! Cliente não possui conta! !!!")
        return

    for conta in cliente.contas:
        print(f'Opção {cliente.contas.index(conta) + 1}\t-\tConta: {conta.numero}\n')
    
    while True:
        try:
            ref = int(input('Selecione uma das opções de contas: '))
            if ref > 0:
                ref -= 1
            else:
                print("\n!!! Entrada inválida.\n!!! Por favor, selecione uma conta válida.\n")
                continue

            if ref < len(cliente.contas):
                break
            else:
                print("\n!!! Entrada inválida.\n!!! Por favor, selecione uma conta válida.\n")
                continue


        except ValueError:
            print("\n!!! Entrada inválida.\n!!! Por favor, selecione uma conta válida.\n")

    return cliente.contas[ref]


def depositar(clientes):
    while True:
        try:
            cpf = int(input("Informe o CPF (apenas números): "))
            if len(str(cpf)) == 11:
                break
            else:
                print("\n!!! Por favor, insira um CPF válido.\n")
            continue
        except ValueError:
            print("\n!!! Entrada inválida.\n!!! Por favor, insira um CPF válido.\n")

    cpf = str(cpf)
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n!!! Cliente não encontrado! !!!")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    while True:
        try:
            cpf = int(input("Informe o CPF (apenas números): "))
            if len(str(cpf)) == 11:
                break
            else:
                print("\n!!! Por favor, insira um CPF válido.\n")
            continue
        except ValueError:
            print("\n!!! Entrada inválida.\n!!! Por favor, insira um CPF válido.\n")

    cpf = str(cpf)
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n!!! Cliente não encontrado! !!!")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    while True:
        try:
            cpf = int(input("Informe o CPF (apenas números): "))
            if len(str(cpf)) == 11:
                break
            else:
                print("\n!!! Por favor, insira um CPF válido.\n")
            continue
        except ValueError:
            print("\n!!! Entrada inválida.\n!!! Por favor, insira um CPF válido.\n")

    cpf = str(cpf)
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n!!! Cliente não encontrado! !!!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================== EXTRATO ==================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n{transacao['data']}\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("=============================================")


def criar_cliente(clientes):
    while True:
        try:
            cpf = int(input("Informe o CPF (apenas números): "))
            if len(str(cpf)) == 11:
                break
            else:
                print("\n!!! Por favor, insira um CPF válido.\n")
            continue
        except ValueError:
            print("\n!!! Entrada inválida.\n!!! Por favor, insira um CPF válido.\n")

    cpf = str(cpf)
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n!!! Já existe cliente com esse CPF! !!!")
        return

    nome = input("Informe o nome completo: ")
    while True:
        try:
            data = int(input("Informe a data de nascimento (dd-mm-aaaa): "))
            if len(str(data)) == 8:
                data = str(data)
                break
            else:
                print("\n!!! Por favor, insira uma data válida.\n")
                continue
        except ValueError:
            print("\n!!! Entrada inválida.\n!!! Por favor, insira uma data válida.\n")
    data_nascimento = f"{data[:2]}/{data[2:4]}/{data[4:]}"
    logradouro = input("Informe o logradouro (Rua, Av., etc): ")
    nro = input("Informe o número: ")
    bairro = input("Informe o bairro: ")
    cidade = input("Informe a cidade: ")
    while True:
        estado = input("Informe as siglas do estado (ex.: SP, RJ): ")
        if len(estado) == 2:
            break
        else:
            print("\n!!! Por favor, insira apenas as siglas do estado.\n")
            continue
    endereco = f'{logradouro}, {nro} - {bairro} - {cidade}/{estado}'

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n*** Cliente criado com sucesso! ***")


def criar_conta(numero_conta, clientes, contas):
    while True:
        try:
            cpf = int(input("Informe o CPF (apenas números): "))
            if len(str(cpf)) == 11:
                break
            else:
                print("\n!!! Por favor, insira um CPF válido.\n")
            continue
        except ValueError:
            print("\n!!! Entrada inválida.\n!!! Por favor, insira um CPF válido.\n")

    cpf = str(cpf)
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n!!! Cliente não encontrado, fluxo de criação de conta encerrado! !!!")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n*** Conta criada com sucesso! ***")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def main():
    
    clientes = []
    contas = []
    

    while True:
        
        opcao = menu()

        match opcao:
            case "d":
                depositar(clientes)
            case "s":
                sacar(clientes)
            case "e":
                exibir_extrato(clientes)
            case "q":
                break
            case "n":
                numero_conta = len(contas) + 1
                criar_conta(numero_conta, clientes, contas)
            case "u":
                criar_cliente(clientes)
            case "l":
                listar_contas(contas)
            case _:
                print("\n!!! Operação inválida, por favor selecione novamente a operação desejada.\n")

main()