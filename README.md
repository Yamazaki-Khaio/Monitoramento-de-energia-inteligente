# Monitoramento-de-energia-inteligente
Repositório dedicado ao problema 1 da disciplina de Concorrência e Conectividade

# Requisitos 
PYTHON 

# Organização das pastas
A solução está organizada em 1 pastas e dois arquivos, com o Diagrama de Sequência básico da arquitetura.
Na pasta models está presente todos os modelos necessários para executar a solução, sendo dois executáveis via PYTHON, sendo eles: o cliente "medidor.py" e o servidor "servidor.py".

# Como executar 
1. Passo 1: Execute o Servidor via PYTHON, assim o servidor estará disponível, esperando requisições.
2. Passo 2: Execute os medidores via PYTHON, assim cada medidor estará fazendo requisições POST, para medidores novos, e PUT, para medidores que já estão cadastrados.
Após esses passos, a solução estará funcionando.
3. Passo 3: Acessar via qualquer browser com endereço http://127.0.0.1:5000/?id=888888888 " subistituindo 8888... pelo o id que o seu medidor irá enviar assim que for iniciado" para ter acesso GET dos dados cadastrado do medidor
