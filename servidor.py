import socket
import threading
import pickle
from datetime import datetime, timedelta


class Clinica_agendamento:
    def __init__(self):
#CRIANDO O SOCKET DO SERVIDOR
        self.__socket_serv= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#ROTINAS BIND E LISTEN
        self.__socket_serv.bind(('0.0.0.0',9000))
        self.__socket_serv.listen(5)
    
#DEMAIS ATRIBUTOS OS VARIÁVEIS DA CLASSE
        self.__capacidade = 5
        self.__especialidades_disp = []
        self.__consultas_agenda = {'SEGUNDA-FEIRA': {}, 'QUARTA-FEIRA':{}, 'SEXTA-FEIRA':{}}
        self.__tamanhomsg = 10000
        self.__horario_ini = '08:00'
        self.__mutex = threading.Semaphore(1) #SEMÁFORO CRIADO
        

#VERIFICAR SE EM UM DETERMINADO DIA TEM VAGAS
    def _tem_vaga(self,dia) -> bool:
        if len(self.__consultas_agenda[dia]) <= self.__capacidade:
            return True

#DEFINIR HORARIOS
    def _set_hora(self, dia):      
        # Converte a string de hora inicial para um objeto datetime
        horario_ini_datetime = datetime.strptime(self.__horario_ini, "%H:%M")

        # Verifica o número de agendamentos para calcular o novo horário
        num_agendamentos = len(self.__consultas_agenda[dia])
        novo_horario = horario_ini_datetime + timedelta(minutes=30 * num_agendamentos)

        # Retorna o novo horário formatado como string
        return novo_horario.strftime("%H:%M")


#DEFINIR ESPECIALIDADES DISPONÍVEIS NA SEMANA       
    def _set_especialidade(self,data:str, dia:str, hora: int ,especialidade:str):
        if len(self.__especialidades_disp) >2:
            raise Exception
        else:
            dt = data.upper()
            di = dia.upper()
            hr = str(hora)
            es = especialidade.upper()
            if di not in ['SEGUNDA-FEIRA','QUARTA-FEIRA','SEXTA-FEIRA']:
                raise Exception
            else:
                especialidade = [dt, di, hr, es]
                self.__especialidades_disp.append(especialidade)

#EXCLUIR UM AGENDAMENTO
    def _excluir(self, msgm):
        with self.__mutex: #SEMAFORO AQUI
            cpf_busca  = msgm[1]
            for dia, agendado in self.__consultas_agenda.items():
                if cpf_busca in agendado:
                    tupla_removida = agendado.pop(cpf_busca)
                    return f'OK-301 {tupla_removida}'
            return 'ERRO-113 '


#INSERIR NA TABELA UM AGENDAMENTO
    def _inserir_na_agenda(self,msgm):
        with self.__mutex: #UM SEMAFORO AQUI
            hora = self._set_hora(msgm[-1])
            msge_c_h = msgm + (hora,)
            if self._tem_vaga(msgm[-1]):
                if msgm[1] not in self.__consultas_agenda.get(msgm[-1], {}):
                    self.__consultas_agenda[msgm[-1]][msgm[1]] = msge_c_h
                   # back = self.__consultas_agenda[msgm[-1]].get(msgm[1])
                    #str(back)
                    return f'OK-300 {msge_c_h}'
                else:
                    return 'ERRO-111 '
            else:
                return 'ERRO-110 '
        
#BUSCAR NA LISTA DE AGENDAMENTOS
    def _buscar(self,msgm):
        cpf_busca = msgm[1]
        for dia, agendado in self.__consultas_agenda.items():
            tupla_associada = agendado.get(cpf_busca)
            if tupla_associada is not None:
                return f'OK-302 ' + str(tupla_associada)
        return 'ERRO-112 '
        
#TRATAMENTO DAS MENSAGENS DO CLIENTE
    def _tratar_cliente(self, cliente, endereco):
        try:
            while True:
                cliente.sendall(pickle.dumps(self.__especialidades_disp))
                info = cliente.recv(self.__tamanhomsg)
                if not info:
                    break  # Cliente se desconectou
                msgm = pickle.loads(info)
                print('MENSAGEM DO CLIENTE', endereco, ' = ', msgm)
                print()
                if msgm[0] == 'AGEND':
                    status = self._inserir_na_agenda(msgm)
                    resposta_serv = pickle.dumps(status)
                    cliente.sendall(resposta_serv)
                    print(F'\nLISTA ATUAL DO {msgm[3]} : {self._imprimir_dic(msgm[-1])} --')


                elif msgm[0] == 'BUSCA':
                    status = self._buscar(msgm)
                    resposta_serv = pickle.dumps(status)
                    cliente.sendall(resposta_serv)

                elif msgm[0] == 'CANCEL':
                    status = self._excluir(msgm)
                    resposta_serv = pickle.dumps(status)
                    cliente.sendall(resposta_serv)
        

        except (ConnectionResetError, socket.error):
            print('CLIENTE DESCONECTADO:', endereco)
        finally:
            cliente.close()


#PRINTAR DICIONARIO
    def _imprimir_dic(self,dia: str) -> str:
        if dia.upper() not in ['SEGUNDA-FEIRA', 'QUARTA-FEIRA', 'SEXTA-FEIRA']:
            raise Exception
        else:
            saida = ''
            agendado = self.__consultas_agenda.get(dia, {})
            for valor in agendado.values():
                saida += str(valor) + '\n'
            return saida  


#INICIAR SERVIDOR E ACEITAR CONEXÕES
    def _iniciar(self):
        print('==servidor funcionando==')
        try:
            while True:
                cliente, endereco = self.__socket_serv.accept()
                print('\nNOVO CLIENTE CONECTADO',endereco)
                thread_cliente = threading.Thread(target=self._tratar_cliente, args=(cliente, endereco))
                thread_cliente.start()            
        finally:
            self.__socket_serv.close()

if __name__ == '__main__':
    servidor = Clinica_agendamento()
    servidor._set_especialidade('18/12/2023','segunda-feira','8h','CLINICO GERAL')
    servidor._set_especialidade('20/12/2023','quarta-feira','8h','DERMATOLOGISTA')
    servidor._set_especialidade('22/12/2023','sexta-feira','8h','NUTRICIONISTA')
    servidor._iniciar()

