# Monitoramento-de-energia-inteligente
Repositório dedicado ao problema 1 da disciplina de Concorrência e Conectividade

# Diagrama sequencial
![Diagrama sequencial](https://github.com/Yamazaki-Khaio/Monitoramento-de-energia-inteligente/blob/main/Diagrama%20sequencial.png)

# Requisitos 
PYTHON 

# Organização das pastas
A solução está organizada em 1 pastas e dois arquivos, com o Diagrama de Sequência básico da arquitetura.
Na pasta models está presente todos os modelos necessários para executar a solução, sendo dois executáveis via PYTHON, sendo eles: o cliente "medidor.py" e o servidor "servidor.py".

# Como executar 
1. Passo 1: Execute o Servidor via PYTHON, assim o servidor estará disponível, esperando requisições.
2. Passo 2: Execute os medidores via PYTHON, assim cada medidor estará fazendo requisições POST, para medidores novos, e PUT, para medidores que já estão cadastrados.
Após esses passos, como o problema pede que seja possivel definir, aumentar ou diminuir o consumo de energia em kWh se ultilizou o metodo --limite-alerta: um argumento do tipo inteiro que define o limite de alerta para consumo de energia em quilowatts-hora (kWh). Por padrão, esse valor é definido como 500.
--multiplicador: um argumento do tipo float que define um fator de multiplicação para o consumo de energia em kWh. Por padrão, esse valor é definido como 1.0.
Para utilizar esses argumentos, basta executar o script Python com as opções desejadas. Por exemplo, para definir um limite de alerta de 800 kWh e um fator de multiplicação de 1.5, você poderia executar o seguinte comando: python meu_script.py --limite-alerta 800 --multiplicador 1.5.
3. Passo 3: A interface de acesso do cliente para visualizar os dados do medidor é via qualquer browser ou postman/insomnia com endereço http://localhost:5000/?id=888888888 " subistituindo 8888... pelo o id que o seu medidor irá enviar assim que for iniciado"
