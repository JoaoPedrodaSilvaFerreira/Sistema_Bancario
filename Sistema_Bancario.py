from time import sleep
import os
from datetime import datetime


usuarios = []  
contas = []
saldo = conta = numero_saques = numero_depositos = total_saque = total_deposito = 0
limite = 500
extrato = list()
extrato_saque = list()
limite_saques = 3
cpf = ''
Numero_conta = 1

def main():
    while True: 
        limpar_terminal()
        menu()
        try:
            opcao = int(input('Escolha uma opção: '))
            
            if opcao == 1:
                Cadastrar_Usuario()

            elif opcao == 2:
                criar_conta()

            elif opcao == 3:
                depositar()
                
            elif opcao == 4:
                sacar()

            elif opcao == 5:
                visualizar_extrato() 

            elif opcao == 6:
                mostrar_usuarios()

            elif opcao == 7:
                listar_conta()

            elif opcao == 8:
                print('\nObrigado por utilizar nosso banco. Volte sempre!')
                break
            else:
                print("\nOpção inválida!")
                if input('\nAperte qualquer tecla para voltar'):
                    return 
        except ValueError:
            print("\nEntrada inválida. Por favor digite apenas numeros.")           
            if input('\nAperte qualquer tecla para voltar'):
                return 

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    print("""
    [1] Cadastrar usuário
    [2] Criar conta
    [3] Depósito
    [4] Saque
    [5] Extrato
    [6] Ver usuários cadastrados
    [7] Mostrar contas
    [8] Sair
    """)

def Cadastrar_Usuario():
    limpar_terminal()
    cpf = str(input('CPF: ')).strip() # CPF como string para manter zeros à esquerda
    cpf = ''.join([c for c in cpf if c.isalnum()])
    if not validar_cpf(cpf):
        print('\nCPF inválido!')
        input('\nAperte qualquer tecla para voltar')
        return
    
    if filtrar_usuario(cpf):
        print('Este usuário já existe.')
        if input('\nAperte qualquer tecla para voltar'):
            return 
        return

    nome = input('Nome: ').title().strip()
    data = input('Data de nascimento (DD/MM/AAAA): ').strip() 
    data = f"{data[:2]}/{data[2:4]}/{data[4:]}"
    
    try:
        datetime.strptime(data, '%d/%m/%Y')
        Usuario = {"Nome": nome, "Data": data, "CPF": cpf }
        usuarios.append(Usuario)
        print("\nUsuário cadastrado com sucesso!")

    except ValueError:
        print('Data inválida! Use o formato DD/MM/AAAA')
        
    if input('\nAperte qualquer tecla para voltar'):
        return

def filtrar_usuario(cpf):
    for Usuario in usuarios:
        if Usuario['CPF'] == cpf:
            return Usuario
    return None

def mostrar_usuarios():
    limpar_terminal()
    print("\n--- USUÁRIOS CADASTRADOS ---")
    for Usuario in usuarios:
        print(f"Nome: {Usuario['Nome']} | Data: {Usuario['Data']}  | CPF: {Usuario['CPF']}  ")
    if input('\nAperte qualquer tecla para voltar'):
        return  

def listar_conta(): 
    limpar_terminal()
    for conta in contas:
        print(f"""
Agência: {conta['Agencia']}
C/C:     {conta['Numero_conta']}
Titular: {conta['Usuario']['Nome']}

""")
    if input('\nAperte qualquer tecla para voltar'):
        return 

def criar_conta():
    global Numero_conta
    limpar_terminal()
    cpf = input('Digite seu cpf:').strip()
    cpf = ''.join([c for c in cpf if c.isalnum()])
    if not validar_cpf(cpf):
        print('\nCPF inválido!')
        input('\nAperte qualquer tecla para voltar')
        return

    Usuario = filtrar_usuario(cpf)
    if Usuario:

        nova_conta =  {'Agencia': '0001', 'Numero_conta': Numero_conta, 'Usuario': Usuario}
        contas.append(nova_conta)
        Numero_conta = Numero_conta + 1
        print('\nConta criada com sucesso.')
    else:
        print('\nUsuario não encontrado. Por favor cadastre o usuario.')
    if input('\nAperte qualquer tecla para voltar'):
        return 

def validar_cpf(cpf: str) -> bool:
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))
    
    # Verifica se tem 11 dígitos ou se é uma sequência de dígitos repetidos
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    
    # Calcula o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    # Calcula o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    # Verifica se os dígitos calculados conferem com os informados
    return cpf[-2:] == f"{digito1}{digito2}"   

def depositar():  
    global saldo,extrato
    global numero_depositos
    global total_deposito
    limpar_terminal()
    try:
        deposito = float(input('Digite o valor que sera depositado: R$ ')) 
        if deposito <= 0:
                print('\nNão é possivel depositar um valor igual ou menor que zero.')
        else:                
            extrato_temporario  = deposito
            saldo = saldo + deposito
            numero_depositos = numero_depositos + 1
            extrato.append(extrato_temporario)
            total_deposito = total_deposito + deposito    
            print('\nDepósito efetuado com sucesso!')    
    except ValueError:
            print("\nEntrada inválida. Por favor digite apenas numeros.")
    if input('\nAperte qualquer tecla para voltar'):
        return
    
def sacar(): 
    global numero_saques
    global saldo,extrato
    global total_saque,extrato_saque
    limpar_terminal()
    saques_restantes = limite_saques - numero_saques 
    if saldo == 0:
        print('Saldo insuficiente para tentativa de saque.')
    else:
        if numero_saques < limite_saques:
            print('Valor maximo de saque R$500,00. Com limite de 3 saques diários.')
            print(f'Restam {saques_restantes} saques diarios')
            try: 
                saque = float(input('Digite o valor que deseja sacar:R$ '))               
                if saque <= 0:
                    print('\nOperação falhou. Não é possivel sacar um valor menor ou igual a R$ 0,00 ')
                elif saque <= 500 and saque <= saldo:
                    print('Aguarde as notas sairem na boca do caixa.')
                    sleep(2)
                    print('\nSaque efetuado com sucesso!')
                    extrato_saque.append(saque)
                    saldo = saldo - saque
                    numero_saques = numero_saques + 1
                    total_saque = total_saque + saque
                elif saque > 500:
                    print('\nOperação falhou. O valor digitado excede o limite permitido.')
                elif saque > saldo:
                    print('\nOperação falhou. Valor de saque maior que o saldo atual.')                       
            except ValueError:
                print("\nEntrada inválida. Por favor digite apenas numeros.")
                sacar()
        else:
            print('\nA cota de saque diaria foi atingida.')   
    if input('\nAperte qualquer tecla para voltar'):
        return

def visualizar_extrato():
    limpar_terminal()
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
    if input('\nAperte qualquer tecla para voltar'):
        return  
                   
if __name__ == '__main__':
    main()
