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
                print("Por favor, insira um CPF válido.")
            continue
        except ValueError:
            print("Entrada inválida.")

    cpf = str(cpf)
    usuario = verificar_cpf(usuarios, cpf=cpf)

    if usuario:
        print("!!! Já existe usuário cadastrado com este CPF!")
        return

    nome = input("Informe o nome do usuário: ")

    while True:
        try:
            data = int(input("Informe a data de nascimento (dd-mm-aaaa): "))
            if len(str(data)) == 8:
                data = str(data)
                break
            else:
                print("Por favor, insira uma data válida.")
                continue
        except ValueError:
            print("Entrada inválida.")
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
            print("Por favor, insira apenas as siglas do estado.")
            continue
    endereco = f'{logradouro}, {nro} - {bairro} - {cidade}/{estado}'

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print(cpf,nome,data_nascimento,endereco)

def verificar_cpf(usuarios,*,cpf):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def saque(*, valor, saldo, extrato, limite, saques_do_dia,limite_saque):
    if valor > saldo:
        print("!!! Operação falhou! Você não possui saldo sufuciente.")
    elif valor > limite:
        print("!!! Operação falhou! O valor do saque excedeu o limite.")
    elif saques_do_dia >= limite_saque:
        print("!!! Operação falhou! Número de saques foi excedido.")
    elif valor > 0:
        saldo -= valor
        when = datetime.now().strftime('%d/%m/%Y %H:%M')
        extrato += f'{when} Saque:\t\tR$ {valor: .2f}-\n\n'
        saques_do_dia += 1
        print("*** SAQUE REALIZADO COM SUCESSO ***")
    else:
        print("!!! Operação falhou! O valor informado é inválido.")

    return saldo, extrato, saques_do_dia

def deposito(valor, saldo, extrato, /):
    if valor > 0:
        saldo += valor
        when = datetime.now().strftime('%d/%m/%Y %H:%M')
        extrato += f'{when} Deposito:\tR$ {valor: .2f}+\n\n'
        print("*** DEPÓSITO REALIZADO COM SUCESSO ***")
    else:
        print("!!! Operação falhou! O valor informado é inválido. Tente novamente!")
    return saldo, extrato

def exibir_extrato(saldo,/,*,extrato):
    print("\n================== EXTRATO ==================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\n\tSaldo: R$ {saldo: .2f}")
    print("=============================================")

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
            case "u":
                criar_usuario(usuarios)
            case _:
                print("!!! Operação inválida, por favor selecione novamente a operação desejada.")

main()