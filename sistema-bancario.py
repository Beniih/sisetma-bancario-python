from datetime import datetime

menu = """
  [d] Depositar
  [s] Sacar
  [e] Extrato
  [q] Sair

  => """

saldo = 0
limite = 500
extrato = ""
saques_do_dia = 0
LIMITE_SAQUES = 3

while True:
    
    opcao = input(menu)

    match opcao:
        case "d":
            valor = float(input("Informe o valor do depósito: "))

            if valor > 0:
                saldo += valor
                extrato += f'Deposito: R$ {valor: .2f}  {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n'
            else:
                print("Operação falhou! O valor informado é inválido. Tente novamente!")
        case "s":
            valor = float(input("Informe o valor do saque: "))
            
            if valor > saldo:
                print("Operação falhou! Você não possui saldo sufuciente.")
            elif valor > limite:
                print("Operação falhou! O valor do saque excedeu o limite.")
            elif saques_do_dia >= LIMITE_SAQUES:
                print("Operação falhou! Número de saques foi excedido.")
            elif valor > 0:
                saldo -= valor
                extrato += f'Saque: R$ {valor: .2f}  {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n'
                saques_do_dia += 1
            else:
                print("Operação falhou! O valor informado é inválido.")
        case "e":
            print("\n================ EXTRATO ================")
            print("Não foram realizadas movimentações." if not extrato else extrato)
            print(f"\nSaldo: R$ {saldo: .2f}")
            print("=========================================")
        case "q":
            break
        case _:
            print("Operação inválida, por favor selecione novamente a operação desejada.")