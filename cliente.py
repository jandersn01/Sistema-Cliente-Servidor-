import socket
import pickle
import sys

CAPACIDADE = 10000
HOST = 'localhost'
ESPECIALIDADE: None | list = None
PORTA = 9000
SET_METODO = ['AGEND', 'BUSCA', 'CANCEL']
mensagem_tupla = ()


protocolo_respostas = {
    'OK-300': 'AGENDAMENTO REALIZADO',
    'OK-301': 'AGENDAMENTO CANCELADO COM SUCESSO',
    'OK-302': 'BUSCA FINALIZADA',
    'ERRO-110': 'NÃO HÁ DISPONIBILIDADE DE VAGAS PARA A ESPECIALIDADE DESEJADA',
    'ERRO-111': 'NÃO FOI POSSÍVEL CONCLUIR O AGENDAMENTO POIS JÁ EXISTE UM AGENDAMENTO PARA ESTE CPF',
    'ERRO-112': 'NENHUM AGENDAMENTO ENCONTRADO',
    'ERRO-113': 'AGENDAMENTO INEXISTENTE, NENHUM REGISTRO FOI APAGADO'
}

#TRATAR RESPOSTA DO SERVIDOR
def tratar_resposta(status):
    entrada = status.split()
    retorno = entrada[0]
    situacao = protocolo_respostas.get(retorno)
    corpo = ''

    if len(entrada) > 1:
        corpo = ' '.join(entrada[1:])
        return f'{situacao}: {retorno} {corpo}'
    return f'{situacao}: {retorno}'


    

#função caso o usuário desejar desmarcar um agendamento
def desmarcar():
    print('''
OK! Voce deseja desmarcar uma consulta.
Agora, forneça os dados necessários:
''')

    met = SET_METODO[2]

    cpf = input('Digite aqui seu CPF com apenas números: ')
    
    return met, cpf 


#função caso o usuário desejar consultar um agendamento já feito
def consultar():
    print('''
OK! Você deseja consultar dados de um agendamento já feito.
Agora, forneça os dados necessários:
''')
    met = SET_METODO[1]
    cpf = input('Digite aqui seu CPF: ')

    return met, cpf


#Função caso o usuario desejar AGENDAR consulta
def agendar():

    global ESPECIALIDADE
    print(f'''
              
OK! A operação escolhida foi agendar.
Agora, digite o número correspondente ao tipo de especialista que voê deseja consultar:
              
    1 - {ESPECIALIDADE[0]} 
    2 - {ESPECIALIDADE[1]} 
    3 - {ESPECIALIDADE[2]} 
                      
''')
    esp = int(input('DIGITE AQUI O NÚMERO RELACIONADO A ESPECIALIDADE MÉDICA DESEJADA: '))

    if ESPECIALIDADE[esp-1] not in ESPECIALIDADE:
        raise Exception
    else:
        print(f'''
OK! Você deseja agendar consulta com um {ESPECIALIDADE[esp - 1][-1]}
Agora, forneça os dados necessários:
''')    
        met = SET_METODO[0]
        cpf = input('Digite aqui seu CPF: ')
        nome = input("Digite aqui o seu nome Completo: ").upper()
        espesc = ESPECIALIDADE[esp - 1][-1]
        day = ESPECIALIDADE[esp - 1][1]
        date = ESPECIALIDADE[esp - 1][0]

    return met, cpf, nome, espesc, date, day        

        

#tratamento de opções do usuario
def opcoes():

    global mensagem_tupla

    print ('''
    =======BEM VINDO=======
           
Por favor, digite o número da operação que você deseja realizar:
           
    1 - Marcar consulta
    2 - Ver consulta
    3 - Desmarcar consulta
    4 - Sair
''')
    
    op = int(input('DIGITE AQUI O NÚMERO DA OPERACAO DESEJADA: '))
#tratar opções do usuário
    if op == 1:
        mensagem_tupla = agendar()
        
    elif op == 2:
        mensagem_tupla = consultar()

    elif op == 3:
        mensagem_tupla = desmarcar()
    else:
        return False


        
    
 



#ABRINDO CONEXÃO NA PARTE DO CLIENTE
# ...

if __name__ == '__main__':
    sock_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if len(sys.argv) == 2:
        HOST = sys.argv[1]
    elif len(sys.argv) == 3:
        HOST = sys.argv[1]
        PORTA = int(sys.argv[2])
    sock_cliente.connect((HOST, PORTA))
    
    try:
        while True:
            medicos_disponíveis = sock_cliente.recv(CAPACIDADE)
            ESPECIALIDADE = pickle.loads(medicos_disponíveis)
            continuar = opcoes()
            if continuar is not False:
                dados_cliente = pickle.dumps(mensagem_tupla)
                sock_cliente.sendall(dados_cliente)
                resposta_serv = sock_cliente.recv(CAPACIDADE)
                status = pickle.loads(resposta_serv)
                saida = tratar_resposta(status)
                print(f'\n{saida}')
            else:
                break
    finally:
        print('CONEXÃO ENCERRADA.')
        sock_cliente.close()
