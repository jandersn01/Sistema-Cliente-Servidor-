Nome do projeto: Clinica Agendamento

Aluno: Janderson Lima dos Santos

Disciplinas: Sistemas Operacionais, professor Gustavo Wagner,
             PIRC, professor Leonidas Lima.

 Descrição: Trata-se de uma aplicação a qual o servidor "Clinica_agendamento" armazena dados do usuário a fim de realizar um agendamento do mesmo para uma consulta com um especialista médico disponível
 em uma determinada semana. É proposta da aplicação a possibilidade de realizar um agendamento, buscar por um agendamento que fora realizado previamente e cancelar um agendamento caso o mesmo exista.

 Pré-requisitos para execução: 

 É necessário atentar-se a ordem de inicialização de cada entidade (servidor e cliente); primeiro deve-se inicializar o servidor e logo após os respectivos clientes.
 O servidor funciona na porta 9000 e o IP deve ser sabido (comando ipconfig no windows para se obter o IP do servidor).
 O cliente aceita como argumento  o IP do servidor, e caso necessário também é possível 'setar' também a porta (python3 cliente.py 'end_ip' porta: int), caso nenhum argumento seja passado, o IP addr assume 'localhost'.
 É recomendado a versão 10 do python.

 protocolo de aplicação: 'JAND'

ENVIO CLIENTE ------------------------------------------------> SERVIDOR

'AGEND' ------------------------------------------------------> AGENDA UMA CONSULTA
PARAMETROS PASSADOS  ----------------------------------------> ('AGEND','CPF','NOME','ESPECIALISTA','DATA','DIA_DA_SEMANA')

'BUSCA'------------------------------------------------------> BUSCA POR UM AGENDAMENTO
PARAMETROS PASSADOS  ----------------------------------------> ('BUSCA','CPF')

'CANCEL'------------------------------------------------------> CANCELA UM AGENDAMENTO
PARAMETROS PASSADOS  ----------------------------------------> ('CANCEL','CPF')

RESPOSTAS DO SERVIDOR E PARAMETROS DEVOLVIDOS PARA CADA REQUISIÇÂO DO CLIENTE:

PARA 'AGEND'

AGENDAMENTO REALIZADO --> 'OK-300'('AGEND', 'CPF', 'NOME', 'ESPECIALISTA', 'DATA', 'DIA_DA_SEMANA', 'HORÁRIO' )
NÃO HÁ VAGAS --> 'ERRO-110'
CPF JÁ AGENDADO PARA AQUELA ESPECIALIDADE --> 'ERRO-111'

PARA 'BUSCA'

BUSCA FINALIZADA --> 'OK-302'('AGEND', 'CPF', 'NOME', 'ESPECIALISTA', 'DATA', 'DIA_DA_SEMANA', 'HORÁRIO' )
NENHUM AGENDAMENTO ENCONTRADO --> 'ERRO-112'

PARA  'CANCEL' 

AGENDAMENTO CANCELADO --> 'OK-301'('AGEND', 'CPF', 'NOME', 'ESPECIALISTA', 'DATA', 'DIA_DA_SEMANA', 'HORÁRIO' )
AGENDAMENTO INEXISTENTE, NADA FOI ALTERADO --> 'ERRO-113'






  
