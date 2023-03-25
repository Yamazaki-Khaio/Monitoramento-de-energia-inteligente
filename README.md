# Monitoramento-de-energia-inteligente
Repositório dedicado ao problema 1 da disciplina de Concorrência e Conectividade

# Diagrama sequencial
![Diagrama sequencial](https://github.com/Yamazaki-Khaio/Monitoramento-de-energia-inteligente/blob/main/Diagrama%20sequencial.png)

# Requisitos 
PYTHON ou DOCKER

# Docker
1. Repoitorio no dockerhub: https://hub.docker.com/repository/docker/khaiioy/pbl1/general
2. A imagem docker pode ser criada diretamente pelo dockerfile que se encontra dentro da pasta models
3. O servidor pode ser executado como imagem docker ultizando o comando docker run -p 5000:5000 -v \endereço_onde_está_salvo_o_arquivo_.json_para_persistencia_de_dados/db.json:/local_dentro_do_container/db.json nome_do_repositorio:nome_da_imagem
4. O medidor pode ser executado como imagem docker ultilizando o comando docker run --it --net=host nome_do_repositorio:nome_da_imagem
5. O servidor e os medidores podem ser simplesmente iniciados via portainer via imagem docker

# Organização das pastas
A solução está organizada em 1 pastas e dois arquivos, com o Diagrama de Sequência básico da arquitetura.
Na pasta models está presente todos os modelos necessários para executar a solução, sendo dois executáveis via PYTHON, sendo eles: o cliente "medidor.py", usuario "usuario.py" e o servidor "servidor.py", .

# Como executar 
1. Passo 1: Execute o Servidor via PYTHON, assim o servidor estará disponível, esperando requisições.
2. Passo 2: Execute os medidores via PYTHON, assim cada medidor estará fazendo requisições POST, para medidores novos, e PUT, para medidores que já estão cadastrados.
Após esses passos, como o problema pede que seja possivel definir, aumentar ou diminuir o consumo de energia em kWh se ultilizou o metodo --limite-alerta: um argumento do tipo inteiro que define o limite de alerta para consumo de energia em quilowatts-hora (kWh). Por padrão, esse valor é definido como 500.
--multiplicador: um argumento do tipo float que define um fator de multiplicação para o consumo de energia em kWh. Por padrão, esse valor é definido como 1.0.
Para utilizar esses argumentos, basta executar o script Python com as opções desejadas. Por exemplo, para definir um limite de alerta de 800 kWh e um fator de multiplicação de 1.5, você poderia executar o seguinte comando: python meu_script.py --limite-alerta 800 --multiplicador 1.5.
3. Passo 3: A interface de acesso do cliente para visualizar os dados do medidor é via qualquer browser e postman/insomnia com endereço http://localhost:5000/?id=888888888 " subistituindo 8888... pelo o id que o seu medidor irá enviar assim que for iniciado" ou executando o usuario Via PYTHON e insirindo o ID pedidor.

# Funcionamento do servidor.py
Este é um servidor simples que fornece uma API REST para acesso a um arquivo de banco de dados json. Aqui está uma breve descrição de cada função no código:
initialize_database(): cria o arquivo de banco de dados json, caso ele não exista.
read_database(): lê o conteúdo do arquivo de banco de dados json e retorna um dicionário de dados.
write_database(data): grava o dicionário de dados fornecido no arquivo de banco de dados json.
create_headers(status_code, status_text, message_body): cria os cabeçalhos HTTP apropriados para a resposta com o código de status, o texto de status e o corpo da mensagem fornecidos.
start_server(): cria um soquete de servidor TCP, liga-o ao host e à porta especificados e entra em um loop para lidar com as solicitações de clientes.
client_thread(client_socket, ip, port): função de thread que é executada para lidar com cada cliente. Recebe a solicitação do cliente e encaminha a solicitação para a função correspondente de acordo com o método HTTP. Envia a resposta de volta ao cliente.
do_GET(data): função para processar solicitações GET. Extrai o nome da chave (id) da solicitação e retorna o valor correspondente se estiver no dicionário de dados, caso contrário, retorna um erro 404.
do_POST(data): função para processar solicitações POST. Adiciona a nova chave e valor fornecidos no dicionário de dados e grava o dicionário atualizado no arquivo de banco de dados json.
do_PUT(data): função para processar solicitações PUT. Atualiza o valor de uma chave existente no dicionário de dados e grava o dicionário atualizado no arquivo de banco de dados json.
do_DELETE(data): função para processar solicitações DELETE. Remove uma chave existente do dicionário de dados e grava o dicionário atualizado no arquivo de banco de dados json.

# Funcionamento do medidor.py
O código em questão é um script Python que simula um medidor de consumo de energia elétrica, que envia dados para um servidor por meio de uma conexão HTTP.
O script começa importando algumas bibliotecas Python e definindo algumas constantes. Em seguida, o script lê os argumentos da linha de comando usando o módulo argparse. Depois disso, o script define uma função increment, que recebe o consumo atual e um incremento e retorna o novo valor do consumo.
Então verifica se o client_id já existe no arquivo JSON que armazena os dados do medidor. Se sim, ele carrega o histórico de consumo a partir do arquivo JSON. Se não, ele cria uma lista vazia para o histórico de consumo. Em seguida, o script entra em um loop infinito que executa o monitor de energia.
Dentro do loop, o script aguarda a entrada do usuário para ajustar o incremento. Em seguida, o script gera um consumo atual aleatório em kWh, calcula o consumo do período atual usando a função increment, adiciona o consumo atual ao consumo total, gera uma fatura com base no consumo total e no valor do kWh e adiciona o consumo atual ao histórico de consumo. O script também verifica se o consumo está acima do limite de alerta definido e gera um alerta se necessário.
Por fim, o script cria um payload com os dados a serem enviados ao servidor, converte o payload em uma string JSON, cria um socket e envia a mensagem para o servidor. O script aguarda dez segundos antes de medir novamente.


# Funcionamento do usuario.py
Este código implementa um cliente que envia uma solicitação HTTP GET para um servidor e recebe uma resposta JSON. Em seguida, ele exibe um menu que permite que o usuário visualize diferentes dados do JSON.
Para executar este código, você precisa primeiro executar o servidor que está fornecendo os dados JSON. Além disso, você precisa garantir que o servidor esteja executando na porta e no host especificados no código.
Quando você executa o código, ele solicita que você digite um ID. Isso é usado para fazer a solicitação HTTP GET para o servidor. Se a resposta contiver dados JSON válidos, o código exibe o menu e aguarda a entrada do usuário. O usuário pode digitar um número correspondente à opção de menu desejada. Dependendo da opção selecionada, o código exibe diferentes dados do JSON.
Para sair do programa, o usuário pode digitar "0" quando solicitado a digitar uma opção de menu.
