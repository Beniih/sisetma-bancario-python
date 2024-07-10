from datetime import datetime

def criar_usuario(usuarios):
    cpf = int(input("Informe o CPF (apenas números): "))
    nome = str(input("Informe o nome do usuário: "))
    data_nascimento = str(input("Informe a data de nascimento: "))
    logradouro = str(input("Informe o logradouro (Rua, Av., etc): "))
    nro = int(input("Informe o número (0 caso S/N): "))
    bairro = str(input("Informe o bairro: "))
    cidade = str(input("Informe a cidade: "))
    estado = str(input("Informe a sigla do estado (ex.: SP, RJ): "))
    endereco = f'{logradouro}, {nro} - {bairro} - {cidade}/{estado}'
    print(cpf,nome,data_nascimento,endereco)


def verificar_cpf(usuarios,*,cpf):
    pass

def saque(*, valor, saldo, extrato, limite, saques_do_dia,limite_saque):
    if valor > saldo:
        print("Operação falhou! Você não possui saldo sufuciente.")
    elif valor > limite:
        print("Operação falhou! O valor do saque excedeu o limite.")
    elif saques_do_dia >= limite_saque:
        print("Operação falhou! Número de saques foi excedido.")
    elif valor > 0:
        saldo -= valor
        when = datetime.now().strftime('%d/%m/%Y %H:%M')
        extrato += f'{when} Saque:\t\tR$ {valor: .2f}-\n\n'
        saques_do_dia += 1
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato, saques_do_dia

def deposito(valor, saldo, extrato, /):
    if valor > 0:
        saldo += valor
        when = datetime.now().strftime('%d/%m/%Y %H:%M')
        extrato += f'{when} Deposito:\tR$ {valor: .2f}+\n\n'
    else:
        print("Operação falhou! O valor informado é inválido. Tente novamente!")
    return saldo, extrato

def exibir_extrato(saldo,/,*,extrato):
    print("\n================== EXTRATO ==================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\n\tSaldo: R$ {saldo: .2f}")
    print("=============================================")

def main():

    menu = """
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

    => """

    AGENCIA = "0001"
    LIMITE_SAQUES = 3

    usuarios = []
    contas = []
    saldo = 0
    limite = 500
    extrato = ""
    saques_do_dia = 0
    

    while True:
        
        opcao = input(menu)

        match opcao:
            case "d":
                valor = float(input("Informe o valor do depósito: "))
                saldo, extrato = deposito(valor, saldo, extrato)
            case "s":
                valor = float(input("Informe o valor do saque: "))
                saldo, extrato, saques_do_dia = saque(valor=valor, saldo=saldo, extrato=extrato, limite=limite, saques_do_dia=saques_do_dia, limite_saque=LIMITE_SAQUES)
            case "e":
                exibir_extrato(saldo, extrato=extrato)
            case "q":
                break
            case _:
                print("Operação inválida, por favor selecione novamente a operação desejada.")

main()