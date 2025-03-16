from time import sleep
menu = """

[1]Depositar
[2]Sacar
[3]Extrato
[4]Sair
        """

saldo = 0
limite = 500
extrato_temporario = list()
extrato = list()
extrato_saque = list()
numero_saques = numero_depositos = total_saque = total_deposito = 0
limite_saques = 3


while True:

    try:
        opcao = int(input(menu))
    except ValueError:
        print("Entrada inválida. Por favor digite apenas numeros.")
        continue
    print()
    if opcao == 1:
        try:
            deposito = float(input('Digite o valor que sera depositado: R$ '))   
            if deposito <= 0:
                print('Não é possivel depositar um valor igual ou menor que zero.')
            else:                
                extrato_temporario  = deposito
                saldo = saldo + deposito
                numero_depositos = numero_depositos + 1
                extrato.append(extrato_temporario)
                total_deposito = total_deposito + deposito
        except ValueError:
            print("Entrada inválida. Por favor digite apenas numeros.")

    elif opcao == 2:
        saques_restantes = limite_saques - numero_saques 
        if saldo == 0:
            print('Saldo insuficiente para tentativa de saque.')
        else:
            if numero_saques < limite_saques:
                print('Valor maximo de saque R$500,00. Com limite de 3 saques diários.')
                print(f'Restam {saques_restantes} saques diarios')
                try: 
                    saque = float(input('Digite o valor que deseja sacar:R$ '))               
                    if saque <= 500 and saque <= saldo and numero_saques < limite_saques:
                        print('Aguarde as notas sairem na boca do caixa.')
                        sleep(2)
                        print('Saque efetuado com sucesso!')
                        extrato_saque.append(saque)
                        saldo = saldo - saque
                        numero_saques = numero_saques + 1
                        total_saque = total_saque + saque
                    elif saque > 500:
                        print('Operação falhou. O valor digitado excede o limite permitido.')
                    elif saque <= 0:
                        print('Operação falhou. Não é possivel sacar um valor menor ou igual a R$00,00 ')
                    elif saque > saldo:
                        print('Operação falhou. Valor de saque maior que o saldo atual.')
                except ValueError:
                    print("Entrada inválida. Por favor digite apenas numeros.")
            else:
                print('A cota de saque diaria foi atingida.')
                
    elif opcao == 3:
        print(f'Depósitos efetuados:{numero_depositos} ')
        for i, v in enumerate(extrato):
            if i > 0:
                print(',',end=' ')
            print(f'R$ {v:.2f}',end=' ')           
        if numero_depositos > 0:    
            print() 
        print(f'Valor total dos depósitos R$ {total_deposito:.2f}\n')
        
        print('Saques efetuados: ',end='')
        if numero_saques == 0:
            print(numero_saques)
        else:
            print(f'{numero_saques}')
            for i,v in enumerate(extrato_saque):
                if i > 0:
                    print(',',end=' ')
                print(f'R${v:.2f}',end=' ')
        if numero_saques > 0:
            print()
        print(f'Valor total dos saques R${total_saque:.2f}')
        print(f'Saques diarios efetuados:{numero_saques}\n')             
        print(f'Saldo disponível: R${saldo:.2f}')      
              
    elif opcao == 4:
        print('Obrigado por utilizar nosso banco. Volte sempre!')
        break
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
