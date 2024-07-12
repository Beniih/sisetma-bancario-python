import textwrap
from datetime import datetime

def menu():
    menu = """
    =================== MENU ====================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [n]\tNova Conta
    [u]\tNovo Usuário
    [l]\tListar Contas
    [q]\tSair

    => """
    return input(textwrap.dedent(menu))

def criar_usuario(usuarios):
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
    usuario = verificar_cpf(usuarios, cpf=cpf)

    if usuario:
        print("\n!!! Já existe usuário cadastrado com este CPF!\n")
        return

    nome = input("Informe o nome do usuário: ")

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

    print("\n*** Usuário cadastrado com sucesso! ***\n")
    return {"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco}

def verificar_cpf(usuarios,*,cpf):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, nr_conta, usuarios):
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
    usuario = verificar_cpf(usuarios, cpf=cpf)

    if usuario:
        print("\n*** Conta criada com sucesso! ***\n")
        return {"agencia": agencia, "numero_conta": nr_conta, "usuario": usuario}
    else:
        print("\n!!! Usuário não encontrado, processo de criação de conta encerrado!\n")

def saque(*, valor, saldo, extrato, limite, saques_do_dia,limite_saque):
    if valor > saldo:
        print("!!! Operação falhou! Você não possui saldo sufuciente.\n")
    elif valor > limite:
        print("!!! Operação falhou! O valor do saque excedeu o limite.\n")
    elif saques_do_dia >= limite_saque:
        print("!!! Operação falhou! Número de saques foi excedido.\n")
    elif valor > 0:
        saldo -= valor
        when = datetime.now().strftime('%d/%m/%Y %H:%M')
        extrato += f'{when} Saque:\t\tR$ {valor: .2f}-\n\n'
        saques_do_dia += 1
        print("*** SAQUE REALIZADO COM SUCESSO ***")
    else:
        print("\n!!! Operação falhou! O valor informado é inválido.\n")

    return saldo, extrato, saques_do_dia

def deposito(valor, saldo, extrato, /):
    if valor > 0:
        saldo += valor
        when = datetime.now().strftime('%d/%m/%Y %H:%M')
        extrato += f'{when} Deposito:\tR$ {valor: .2f}+\n\n'
        print("*** DEPÓSITO REALIZADO COM SUCESSO ***\n")
    else:
        print("!!! Operação falhou! O valor informado é inválido. Tente novamente!\n")
    return saldo, extrato

def exibir_extrato(saldo,/,*,extrato):
    print("\n================== EXTRATO ==================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\n\tSaldo: R$ {saldo: .2f}")
    print("=============================================")

def listar_contas(contas):
    for conta in contas:
        registro = f"""\
            Agencia:\t{conta['agencia']}
            C \ C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
            """
        print("=" * 100)
        print(textwrap.dedent(registro))

def main():
    AGENCIA = "0001"
    LIMITE_SAQUES = 3

    usuarios = []
    contas = []
    saldo = 0
    limite = 500
    extrato = ""
    saques_do_dia = 0
    

    while True:
        
        opcao = menu()

        match opcao:
            case "d":
                valor = float(input("Informe o valor do depósito: "))
                saldo, extrato = deposito(
                    valor,
                    saldo,
                    extrato
                    )
            case "s":
                valor = float(input("Informe o valor do saque: "))
                saldo, extrato, saques_do_dia = saque(
                    valor=valor,
                    saldo=saldo,
                    extrato=extrato,
                    limite=limite,
                    saques_do_dia=saques_do_dia,
                    limite_saque=LIMITE_SAQUES
                    )
            case "e":
                exibir_extrato(
                    saldo,
                    extrato=extrato
                    )
            case "q":
                break
            case "n":
                nr_conta = len(contas) + 1
                nova_conta = criar_conta(AGENCIA, nr_conta, usuarios)
                if nova_conta:
                    contas.append(nova_conta)
            case "u":
                novo_usuario = criar_usuario(usuarios)
                if novo_usuario:
                    usuarios.append(novo_usuario)
            case "l":
                listar_contas(contas)
            case _:
                print("\n!!! Operação inválida, por favor selecione novamente a operação desejada.\n")

main()