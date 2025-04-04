from time import sleep
import os
from datetime import datetime
import re

def limpar_terminal():
        os.system('cls' if os.name == 'nt' else 'clear')

def validar_cpf(cpf) -> bool:
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

def apenas_letras(texto):
    return bool(re.fullmatch(r'^[a-zA-ZáéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇàèìòùÀÈÌÒÙ\s]+$', texto))

class Banco:
    def __init__(self):
        self.usuarios = []  
        self.contas = []
        self.agencia = '0001'
        self.numero_conta = 0

    def Cadastrar_Usuario(self):
        limpar_terminal()
        cpf = str(input('CPF: ')).strip() # CPF como string para manter zeros à esquerda
        cpf = ''.join([c for c in cpf if c.isalnum()])
        
        if not validar_cpf(cpf):
            print('\nCPF inválido!')
            input('\nAperte qualquer tecla para voltar')
            return False
        
        if self.filtrar_usuario(cpf):
            print('Usuário já cadastrado.')
            input('\nAperte qualquer tecla para voltar')
            return False
            

        nome = input('Nome: ').title().strip()
        if apenas_letras(nome):
            pass
        else:
            print("Nome deve conter apenas letras")
            input('Aperte qualquer tecla para voltar.')
            return
        data = input('Data de nascimento (DD/MM/AAAA): ').strip() 
        data = f"{data[:2]}/{data[2:4]}/{data[4:]}"
        
        try:
            datetime.strptime(data, '%d/%m/%Y')

            novo_usuario = {
                "nome": nome,
                "data_nascimento": data,
                "cpf": cpf
            }
            
            self.usuarios.append(novo_usuario)
            print('\nUsuário cadastrado com sucesso!')
            self.criar_conta(cpf)

        except ValueError:
            print('Data inválida! Use o formato DD/MM/AAAA')
            input('Aperte qualquer tecla para voltar')
            return

        if input('\nAperte qualquer tecla para voltar'):
            return novo_usuario

    def filtrar_usuario(self,cpf):
        for usuario in self.usuarios:
            if usuario['cpf'] == cpf:
                return usuario
        return None
    
    def criar_conta(self,cpf):
        limpar_terminal()
        usuario = self.filtrar_usuario(cpf)
        contas_do_usuario = sum (1 for conta in self.contas if conta['usuario']['cpf']== cpf)
        
        
        if contas_do_usuario >= 1:
            print("""Criar uma nova conta
[1] Sim
[2] Não                
                  """)
            try:
                new_conta = int(input(''))
                if new_conta == 1:
                    self.numero_conta += 1
                    nova_conta = {
                        "agencia": self.agencia,
                        "numero": self.numero_conta,
                        "usuario": usuario,
                        "saldo": 0,
                        "extrato": [],
                        "saques_realizados": 0,
                        "limite_saques": 3,
                        "limite_por_saque": 500
                    }
                    self.contas.append(nova_conta)    
                    print('Conta criada com sucesso.')
                elif new_conta == 2:
                    return
                else:
                    print('Opção inválida')
                    input('Aperte qualquer tecla para voltar.')
                    return
            except ValueError:
                print('Digite apenas números.')
                input('Aperte qualquer tecla para voltar.')
                return
            
        else:
            self.numero_conta += 1
            nova_conta = {
                "agencia": self.agencia,
                "numero": self.numero_conta,
                "usuario": usuario,
                "saldo": 0,
                "extrato": [],
                "saques_realizados": 0,
                "limite_saques": 3,
                "limite_por_saque": 500
            }
            self.contas.append(nova_conta)    
            print('Conta criada com sucesso.')    
            input('Aperte qualquer tecla para voltar.')    
            return                  

    def selecionar_conta(self, cpf):
        contas_usuario = [c for c in self.contas if c["usuario"]["cpf"] == cpf]
        
        if not contas_usuario:
            print("\nNenhuma conta encontrada para este usuário.")
            input('Aperte qualquer tecla para voltar.')
            return None
            
        if len(contas_usuario) == 1:
            return contas_usuario[0]
            
        print("\nContas disponíveis:")
        for i, conta in enumerate(contas_usuario, 1):
            print(f"{i} - Ag: {conta['agencia']} C/C: {conta['numero']}")
        
        while True:
            try:
                opcao = int(input("Selecione a conta: ")) - 1
                if 0 <= opcao < len(contas_usuario):
                    return contas_usuario[opcao]
                print("Opção inválida.")
            except ValueError:
                print("Digite um número válido.")

    def depositar(self, conta):  
        limpar_terminal()
        print('======= DEPÓSITO =======')
        try:
            deposito = float(input('Digite o valor que sera depositado: R$ ')) 
            if deposito <= 0:
                print('\nNão é possivel depositar um valor igual ou menor que zero.')
                input('\nAperte qualquer tecla para voltar')
                return 

            conta['saldo'] += deposito
            conta[ 'extrato'].append(('depósito', deposito,datetime.now()))
            print('\nDepósito realizado com sucesso!')

        except ValueError:
                print("\nEntrada inválida. Por favor digite apenas numeros.")
        input('\nAperte qualquer tecla para voltar')
        return
    
    def sacar(self,conta): 
        limpar_terminal()
        print('======= SAQUE =======')
        print('Valor maximo de saque R$500,00. Com limite de 3 saques diários.')
        print(f'Saques diarios realizados {conta['saques_realizados']}/{conta['limite_saques']}')
        try:
            if conta['saldo'] <= 0:
                print('Saldo insuficiente para tentativa.')
                input('Aperte qualquer tecla para continuar.')
                return
            if conta["saques_realizados"] >= conta["limite_saques"]:
                print("\nLimite diário de saques atingido.")
            saque = float(input("Valor do saque: R$ "))
            if saque <= 0:
                print("\nValor deve ser positivo.")
            elif saque > conta["limite_por_saque"]:
                print(f"\nLimite por saque: R$ {conta['limite_por_saque']:.2f}")
            elif conta["saques_realizados"] >= conta["limite_saques"]:
                print("\nLimite diário de saques atingido.")
            elif saque > conta["saldo"]:
                print("\nSaldo insuficiente.")
            else:
                conta["saldo"] -= saque
                conta["saques_realizados"] += 1
                conta["extrato"].append(("Saque", -saque, datetime.now()))
                print('Retire as notas na boca do caixa.')
                sleep(2)
                print("\nSaque realizado com sucesso!")
                
        except ValueError:
            print("\nValor inválido. Use apenas números.")
   
        input('\nAperte qualquer tecla para voltar')
        return

    def visualizar_extrato(self,conta):
        limpar_terminal()
        limpar_terminal()
        print(f"\n=== EXTRATO BANCÁRIO ===")
        print(f"Agência: {conta['agencia']} Conta: {conta['numero']}")
        print(f"Cliente: {conta['usuario']['nome']}")
        print(f"CPF: {conta['usuario']['cpf']}")
        print("\nMovimentações:")
        
        if not conta["extrato"]:
            print("Nenhuma movimentação registrada.")
        else:
            for operacao in conta["extrato"]:
                tipo, valor, data = operacao
                print(f"{data.strftime('%d/%m/%Y %H:%M')} - {tipo}: R$ {valor:+.2f}")
        
        print(f"\nSaldo atual: R$ {conta['saldo']:.2f}")             
        input('\nAperte qualquer tecla para voltar')
        return  

    def mostrar_usuarios(self):
        limpar_terminal()
        print("\n--- USUÁRIOS CADASTRADOS ---")
        for usuario in self.usuarios:
            print(f"\nNome: {usuario['nome']}" )
            print(f'Data: {usuario['data_nascimento']}')
            print(f'CPF: {usuario['cpf']} ')
        
        input('\nAperte qualquer tecla para voltar')
        return  
    
    def listar_conta(self,cpf): 
        limpar_terminal()
        for conta in self.contas:
            if conta['usuario']['cpf'] == cpf:
                print(f"""
Agência: {conta['agencia']}
C/C:     {conta['numero']}
Titular: {conta['usuario']['nome']}
CPF:     {conta['usuario']['cpf']}

    """)
        input('\nAperte qualquer tecla para voltar')
        return 

    def main(self): 
        while True:
            limpar_terminal()
            print("""
[1] Login
[2] Cadastrar Usuário
            """)
            try:
                login = int(input('Escolha uma opção: '))               
                if login == 1:
                    limpar_terminal()
                    cpf = str(input('CPF: '))
                    if not validar_cpf(cpf):
                        print('\nCPF inválido!')
                        input('\nAperte qualquer tecla para voltar')
                        continue
                    
                    usuario = self.filtrar_usuario(cpf)
                    if not usuario:
                        print('\nUsuário não encontrado.')
                        input('\nAperte qualquer tecla para voltar')
                        continue
        
                    if usuario:
                        self.tela_principal(cpf)
                    else:
                        continue
                elif login == 2:
                    self.Cadastrar_Usuario()
                
                else:
                    print('Opção inválida.')
            except ValueError:
                print('Operação inválida. Tente novamente.')   
                input('\nAperte qualquer tecla para voltar')
                continue
                     
    def tela_principal(self,cpf):
        conta = self.selecionar_conta(cpf)
        while True: 
            limpar_terminal()
            self.menu()
            try:
                opcao = int(input('Escolha uma opção: '))

                if opcao == 1:
                    self.depositar(conta)
                    
                elif opcao == 2:
                    self.sacar(conta)

                elif opcao == 3:
                    self.visualizar_extrato(conta) 

                elif opcao == 4:
                    self.mostrar_usuarios()

                elif opcao == 5:
                    self.listar_conta(cpf)
                
                elif opcao == 6:
                    self.criar_conta(cpf)

                elif opcao == 7:
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

    def menu(self):
        print("""
[1] Depósito
[2] Saque
[3] Extrato
[4] Ver usuários cadastrados
[5] Mostrar contas
[6] Criar conta
[7] Sair
        """)

if __name__ == '__main__':
    banco = Banco()
    banco.main()
