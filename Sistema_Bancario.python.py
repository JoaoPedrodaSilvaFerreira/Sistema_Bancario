from time import sleep
import os
from datetime import datetime
import re
from bancodedados import session, Usuario, Contas,Extrato
import random 
from decimal import Decimal,InvalidOperation
#criar função de troca de conta 
#criar tabela de contas no banco de dado e vincular o valor e extrato
#e limpar o codigo eliminando as listas e dicionarios que nao sao mais necessarios
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
            data = datetime.strptime(data, '%d/%m/%Y').date()
        
            banco = Usuario(nome= nome, cpf= cpf, data_nascimento= data)
            session.add(banco)
            session.commit()

            print('\nUsuário cadastrado com sucesso!')
            self.criar_conta(cpf)
        

        except ValueError:
            print('Data inválida! Use o formato DD/MM/AAAA')
            input('Aperte qualquer tecla para voltar')
            return
            
        if input('\nAperte qualquer tecla para voltar'):
            return 

    def filtrar_usuario(self,cpf):

        usuario_existente = session.query(Usuario).filter_by(cpf= cpf).first() 
        if usuario_existente:
            return usuario_existente
        return None
   
    def gerar_numero_conta(self):
        # Gerar um número de conta aleatório de 6 dígitos
        numero_conta = str(random.randint(100000, 999999))
        while True:
            conta_existente = session.query(Contas).filter_by(numero_conta = numero_conta).first()
            if not conta_existente:   
                return numero_conta
    
    def criar_conta(self,cpf, tipo_conta='corrente'):
        limpar_terminal()
        conta_existente = session.query(Contas).filter_by(cpf= cpf).first()
        if conta_existente:
            resp = int(input('Criar nova conta?\n[1]Sim\n[2]Não\n'))
            if resp == 1:
                numero_conta = self.gerar_numero_conta()
                senha = ''
                senha2 = ''
                print(f'Crie uma senha para sua conta {tipo_conta}!\nÉ necessario ter quatro caracteres.')
                while True:
                    senha = (input('Senha: '))
                    senha = ''.join(filter(str.isdigit, senha))
                    while True:
                        if len(senha) != 4 or senha == senha[0] * 4:
                            print('Sua senha deve ter apenas 4 caracteres!')
                        else:
                            break
                    print('Por favor confirme sua senha!')
                    senha2 = (input('Senha: '))
                    if senha != senha2:
                        print('As senhas não estão iguais. Crie novamente')
                    else:
                        print('Senha cadastrada.')
                        sleep(2)
                        
                        nova_conta = Contas(
                            cpf=cpf ,
                            saldo=0,
                            numero_conta=numero_conta,
                            saques_diario_realizado= 0,
                            tipo_conta=tipo_conta,
                            agencia=self.agencia,
                            limite_transacao_diaria = 0, 
                            senha = senha
                        )
                        session.add(nova_conta)
                        session.commit()
                        print(f"Conta {tipo_conta} criada com sucesso! Número: {numero_conta}")
                        break
        else:
            numero_conta = self.gerar_numero_conta()
            senha = ''
            senha2 = ''
            print(f'Crie uma senha para sua conta {tipo_conta}!\nÉ necessario ter quatro caracteres.')
            while True:
                    while True:
                        senha = (input('Senha: '))
                        senha = ''.join(filter(str.isdigit, senha))               
                        if len(senha) != 4 or senha == senha[0] * 4:
                            print('Sua senha deve ter apenas 4 caracteres!')
                        else:
                            break
                    print('Por favor confirme sua senha!')
                    senha2 = (input('Senha: '))
                    if senha != senha2:
                        print('As senhas não estão iguais. Crie novamente')
                    else:
                        print('Senha cadastrada.')
                        sleep(2)
                        
                    nova_conta = Contas(
                            cpf=cpf ,
                            saldo=0,
                            numero_conta=numero_conta,
                            saques_diario_realizado= 0,
                            tipo_conta=tipo_conta,
                            agencia=self.agencia,
                            limite_transacao_diaria = 0,  
                            senha = senha
                        )
                    session.add(nova_conta)
                    session.commit()
                    print(f"Conta {tipo_conta} criada com sucesso! Número: {numero_conta}")
                    break

    def resete_limite_diario(self, conta_logada):
        # if not session.query(Extrato).filter_by(id=conta_logada.id).first():  # Verificar se a conta existe
        #     return
     
        # Busca o último extrato da conta específica
        ultimo_extrato = session.query(Extrato)\
            .filter_by(id_conta=conta_logada.id)\
            .order_by(Extrato.data.desc())\
            .first()
        # hoje  = datetime.now().date()
        # Se não há extratos ou o último é de outro dia, reseta os limites
        if not ultimo_extrato or ultimo_extrato.data < datetime.now().date():
            conta_logada.saques_diario_realizado = 0
            conta_logada.limite_transacao_diaria = 0
            session.commit()
        else:
            return
               
    def selecionar_conta(self, cpf):
    # Consultar no banco as contas do usuário
        contas_usuario = session.query(Contas).filter_by(cpf=cpf).all()
        
        if not contas_usuario:
            print("\nNenhuma conta encontrada para este usuário.")
            input('Aperte qualquer tecla para voltar.')
            return None
            
        if len(contas_usuario) == 1:
            return contas_usuario[0]
            
        print("\nContas disponíveis:")
        for i, conta in enumerate(contas_usuario, 1):
            print(f"{i} - Ag: {conta.agencia} C/C: {conta.numero_conta}")
        
        while True:
            try:
                opcao = int(input("Selecione a conta: ")) - 1
                if 0 <= opcao < len(contas_usuario):
                    return contas_usuario[opcao]
                print("Opção inválida.")
            except ValueError:
                print("Digite um número válido.")

    def inserir_extrato(self, cpf, numero_conta, tipo, valor, agencia):
        """
        Insere um registro no extrato bancário
        """
        try:
            conta = session.query(Contas).filter_by(
                cpf=cpf, 
                numero_conta=numero_conta, 
                agencia=agencia
            ).first()
            
            if conta:
                novo_extrato = Extrato(
                    tipo=tipo,
                    valor=float(valor),  # Converte Decimal para float se necessário
                    data=datetime.now(),
                    id_conta=conta.id
                )
                session.add(novo_extrato)
                session.commit()
                return True
            return False
            
        except Exception as e:
            session.rollback()
            print(f"Erro ao inserir extrato: {str(e)}")
            return False

    def depositar(self, conta_logada):
        """
        Realiza operação de depósito na conta
        """
        limpar_terminal()
        self.resete_limite_diario(conta_logada)
        print('======= DEPÓSITO =======')

        if conta_logada.limite_transacao_diaria >= 10:
            print('Você atingiu o limite máximo de transações diárias.')
            input('Aperte qualquer tecla para continuar.')
            return

        try:
            # Obter e validar o valor do depósito
            valor_input = input('Digite o valor que será depositado: R$ ').strip()
            
            # Tratamento da entrada monetária
            valor_str = valor_input.replace('R$', '').replace(' ', '').replace(',', '.')
            deposito = Decimal(valor_str)
            
            if deposito <= 0:
                print('\nNão é possível depositar um valor igual ou menor que zero.')
                return

            # Verificar casas decimais
            if deposito.as_tuple().exponent < -2:  # Mais de 2 casas decimais
                print('\nUse no máximo 2 casas decimais.')
                return

            # Realizar o depósito
            conta_logada.saldo += deposito
            conta_logada.limite_transacao_diaria += 1
            
            # Registrar no extrato
            extrato_sucesso = self.inserir_extrato(
                cpf=conta_logada.cpf,
                numero_conta=conta_logada.numero_conta,
                tipo='Depósito',
                valor=deposito,
                agencia=conta_logada.agencia
            )
            
            if extrato_sucesso:
                session.commit()
                print('\nDepósito realizado com sucesso!')
            else:
                session.rollback()
                print('\nErro ao registrar depósito.')

        except (InvalidOperation, ValueError):
            print("\nValor inválido. Exemplos válidos: 100, 50.25, 75,10")
            session.rollback()
        except Exception as e:
            print(f"\nOcorreu um erro: {str(e)}")
            session.rollback()

        input('\nAperte qualquer tecla para voltar.')
  
    def sacar(self, conta_logada): 
        limpar_terminal()
        self.resete_limite_diario(conta_logada)
        limite_saque = 3
        limite_por_saque = 500
        print('======= SAQUE =======')

        if conta_logada.saldo <= 0:
            print('Saldo insuficiente para tentativa.')
            input('Aperte qualquer tecla para continuar.')
            return

        if conta_logada.limite_transacao_diaria >= 10:
            print('Você atingiu o limite máximo de transações diárias.')
            input('Aperte qualquer tecla para continuar.')
            return

        print('Valor máximo de saque R$500,00. Com limite de 3 saques diários.')
        print(f'Saques diários realizados {conta_logada.saques_diario_realizado}/{limite_saque}')
        
        try:
            if conta_logada.saques_diario_realizado >= limite_saque:
                print("\nLimite diário de saques atingido.")
                input('Aperte qualquer tecla para voltar.')
                return

    
              # Obter e validar o valor do depósito
            valor_input = input('Digite o valor do saque: R$ ').strip()
            
            # Tratamento da entrada monetária
            valor_str = valor_input.replace('R$', '').replace(' ', '').replace(',', '.')
            saque = Decimal(valor_str)
            if float(saque) <= 0:
                print("\nValor deve ser positivo.")
            elif float(saque) > limite_por_saque:
                print(f"\nLimite por saque: R$ {limite_por_saque:.2f}")
            elif float(saque) > conta_logada.saldo:
                print("\nSaldo insuficiente.")
            else:
                conta_logada.saldo -= saque
                conta_logada.saques_diario_realizado += 1
                conta_logada.limite_transacao_diaria += 1

                # Registrar no extrato
                novo_extrato = Extrato(
                    tipo='Saque',
                    valor=saque,
                    data=datetime.now(),
                    id_conta=conta_logada.id
                )
                session.add(novo_extrato)

                # Salvar as mudanças
                session.commit()

                print('Retire as notas na boca do caixa.')
                sleep(2)
                print("\nSaque realizado com sucesso!")
                    
        except ValueError:
            print("\nValor inválido. Use apenas números.")
    
        input('\nAperte qualquer tecla para voltar')
        return

    def visualizar_extrato(self, conta_logada):
        limpar_terminal()
        self.resete_limite_diario(conta_logada)
        print(f"\n=== EXTRATO BANCÁRIO ===")
        print(f"Agência: {conta_logada.agencia} Conta: {conta_logada.numero_conta}")
        print(f"Cliente: {conta_logada.usuario.nome}")
        print(f"CPF: {conta_logada.usuario.cpf}")
        print("\nMovimentações:")

        # Buscar movimentações (extratos) da conta
        extratos = session.query(Extrato).filter_by(id_conta=conta_logada.id).order_by(Extrato.data).all()

        if not extratos:
            print("Nenhuma movimentação registrada.")
        else:
            for operacao in extratos:
                print(f"{operacao.data.strftime('%d/%m/%Y %H:%M')} - {operacao.tipo}: R$ {operacao.valor:.2f}")

        print(f"\nSaldo atual: R$ {conta_logada.saldo:.2f}")             
        input('\nAperte qualquer tecla para voltar')
        return

    def mostrar_usuarios(self):
        limpar_terminal()
        print("\n--- USUÁRIOS CADASTRADOS ---")

        usuarios = session.query(Usuario).all()  # Busca todos os usuários no banco

        if not usuarios:
            print("\nNenhum usuário cadastrado.")
        else:
            for usuario in usuarios:
                print(f"\nNome: {usuario.nome}")
                print(f"Data de Nascimento: {usuario.data_nascimento}")
                print(f"CPF: {usuario.cpf}")

        input('\nAperte qualquer tecla para voltar')
        return

    def listar_conta(self, cpf):
        limpar_terminal()

        contas = session.query(Contas).filter_by(cpf=cpf).all()

        if not contas:
            print("\nNenhuma conta encontrada para este CPF.")
        else:
            for conta in contas:
                print(f"""
    Agência: {conta.agencia}
    C/C:     {conta.numero_conta}
    Titular: {conta.usuario.nome}
    CPF:     {conta.usuario.cpf}
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
                        self.escolher_conta(cpf)

                    else:
                        continue
                elif login == 2:
                    self.Cadastrar_Usuario()
                
                else:
                    limpar_terminal()
                    print('Opção inválida.')
                    input('\nAperte qualquer tecla para voltar')
                    continue
                
            except ValueError:
                print('Operação inválida. Tente novamente.')   
                input('\nAperte qualquer tecla para voltar')
                continue
    
    def escolher_conta(self,cpf):
        contas = session.query(Contas).filter_by(cpf=cpf).all()
        print("\nContas disponíveis:")
        for i, conta_logada in enumerate(contas, 1):
            print(f"[{i}] Agência: {conta_logada.agencia} Conta: {conta_logada.numero_conta}\n{'-'*30}")
        try:
            escolha = int(input("\nSelecione a conta: ")) - 1
            if escolha not in range(len(contas)):
                print("\nOpção inválida.")
                input('Aperte qualquer tecla para voltar')
                return

        except ValueError:
            print("\nEntrada inválida.")
            input('Aperte qualquer tecla para voltar')
        login_senha = int(input('Digite sua senha: '))
        # senha_conta_logada = session.query(Contas).filter_by( cpf = cpf).first()
        conta_logada = contas[escolha]
        if login_senha == conta_logada.senha: 
            self.tela_principal(cpf,conta_logada)
        else:
            limpar_terminal()
            input('Senha  incorreta!\nAperte qualquer tecla para voltar.')
            return
        
    def tela_principal(self, cpf,conta_logada):
        while True:
            limpar_terminal()
            self.menu()
            try:
                opcao = int(input('Escolha uma opção: '))

                if opcao == 1:
                    self.depositar(conta_logada)
                elif opcao == 2:
                    self.sacar(conta_logada)
                elif opcao == 3:
                    self.visualizar_extrato(conta_logada)

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
                    input('\nAperte qualquer tecla para voltar')

            except ValueError:
                print("\nEntrada inválida. Por favor digite apenas números.")           
                input('\nAperte qualquer tecla para voltar')

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