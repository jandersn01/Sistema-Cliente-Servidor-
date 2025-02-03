
# Clínica De Saúde

Este projeto tem por finalidade performar uma arquitetura Cliente e Servidor. Aqui é aplicado conceitos do paradigma OO, API sockets do Python, uso de threads no servidor para que seja possível tratar multiplas conexões de clientes, semáforos Mutex para resolver condições de disputa por recursos.

#### status: concluído

Este projeto foi feito para cumprir a ultima nota das disciplinas de Protocolos de Interconexões de Redes e Sistemas Operacionais do segundo semestre do Curso de Sistemas Para Internet.

## Instalação
Para usar o código é necessário possuir o Python nas versões 3.10 ou posteriores (Até esta data 02/25 está funcionando nas versões mais recentes)

### localhost
Primeiro você deve abrir a pasta do projeto em seu editor e logo após inicializar o servidor:


```bash
  python servidor.py
```
Logo após inicie o(s) cliente(s):
```bash
  python cliente.py
```
![App Screenshot](https://raw.githubusercontent.com/jandersn01/Sistema-Cliente-Servidor-/refs/heads/main/imgs/demonstracaolocalmente.png)

### Mesma rede, máquinas diferentes

É possível realizar a conexão entre máquinas diferentes desde que estejam na mesma rede. 

```bash
  python servidor.py
```
O servidor opera na porta 9000 em localhost, o cliente já sabe disso. Casa esteja operando em máquinas diferentes, você deve especificar o endereço IP do Servidor como argumento no momento de inicializar o cliente:

```bash
  python cliente.py 0.0.0.0 
```
- subistitua 0.0.0.0 pelo endereço IP do servidor.

![App Screenshot](https://raw.githubusercontent.com/jandersn01/Sistema-Cliente-Servidor-/refs/heads/main/imgs/demonstracaoremoto.png)
## Funcionalidades

- Agendar uma consulta
- Conferir uma consulta
- Deletar uma consulta
- Multiplas Conexões




# Protocolo de aplicação

Um dos requisitos a serem cumpridos no projeto foi tentar simular um protocolo de aplicação. Abaixo existe a descrição do protocolo criado.


### ENVIO CLIENTE -----> SERVIDOR

'AGEND' --> AGENDA UMA CONSULTA  
PARAMETROS PASSADOS -> ('AGEND','CPF','NOME','ESPECIALISTA','DATA','DIA_DA_SEMANA')

'BUSCA'---> BUSCA POR UM AGENDAMENTO  
PARAMETROS PASSADOS -------> ('BUSCA','CPF')

'CANCEL'--> CANCELA UM AGENDAMENTO  
PARAMETROS PASSADOS ----> ('CANCEL','CPF')

### RESPOSTAS DO SERVIDOR E PARAMETROS DEVOLVIDOS PARA CADA REQUISIÇÂO DO CLIENTE:

PARA 'AGEND'

AGENDAMENTO REALIZADO --> 'OK-300'('AGEND', 'CPF', 'NOME', 'ESPECIALISTA', 'DATA', 'DIA_DA_SEMANA', 'HORÁRIO' )   
NÃO HÁ VAGAS --> 'ERRO-110'  
CPF JÁ AGENDADO PARA AQUELA ESPECIALIDADE --> 'ERRO-111'

PARA 'BUSCA'

BUSCA FINALIZADA --> 'OK-302'('AGEND', 'CPF', 'NOME', 'ESPECIALISTA', 'DATA', 'DIA_DA_SEMANA', 'HORÁRIO' )   
NENHUM AGENDAMENTO ENCONTRADO --> 'ERRO-112'

PARA 'CANCEL'

AGENDAMENTO CANCELADO --> 'OK-301'('AGEND', 'CPF', 'NOME', 'ESPECIALISTA', 'DATA', 'DIA_DA_SEMANA', 'HORÁRIO' ) 
AGENDAMENTO INEXISTENTE, NADA FOI ALTERADO --> 'ERRO-113'


## Autores

- [@Janderson](www.linkedin.com/in/janderson-lima-064bb9324)

