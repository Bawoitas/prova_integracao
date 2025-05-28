# Explicação das APIs e execução\
### ' API 1 – Node.js (Módulo de Sensores) ' \
Esta API simula sensores instalados nos poços de petróleo. Ela possui dois endpoints principais:\

- ** GET /sensor-data ** : retorna dados simulados de temperatura e pressão. Esses dados são cacheados no Redis para acelerar as respostas e evitar a geração repetida dos mesmos dados em curto espaço de tempo. 

- ** POST /alert ** : recebe alertas e envia via requisição HTTP para a API Python, para que ela registre o evento. \

## Como executar: \
- Na pasta da API Node.js, execute o comando node app.js. A API ficará disponível na porta 3000. \

###' API 2 – Python (Módulo de Eventos Críticos) ' \
Esta API recebe os alertas enviados pela API Node.js e armazena esses eventos em uma lista temporária. Possui dois endpoints: \

- ** POST /event ** : recebe um alerta e adiciona à lista de eventos. 

- ** GET /events ** : retorna todos os eventos armazenados até o momento. \

Essa API consome mensagens enviadas pela API PHP através da fila RabbitMQ, adicionando essas mensagens à lista de eventos. \

## Como executar: \
- Na pasta da API Python, execute o comando python app.py. A API ficará disponível na porta 5000. \

### ' API 3 – PHP (Módulo de Logística) ' \
Esta API gerencia a logística de transporte de peças e equipamentos. Ela possui dois endpoints: \

- ** GET /equipments ** : retorna uma lista simulada de equipamentos.

- **POST /dispatch ** : envia mensagens urgentes de logística para uma fila no RabbitMQ, para que a API Python possa consumir essas mensagens. \

## Como executar: \
- Na pasta da API PHP, execute o comando php -S localhost:8000. A API ficará disponível na porta 8000. \

# Comunicação entre as APIs \
A API Node.js envia alertas para a API Python via requisição HTTP (POST no endpoint /event).

A API PHP envia mensagens urgentes para a API Python através de uma fila no RabbitMQ, utilizando o padrão produtor/consumidor.

A API Python consome essas mensagens da fila RabbitMQ e as adiciona à lista de eventos.

# Uso do cache Redis \
Na API Node.js, o cache Redis é usado para guardar temporariamente os dados simulados do sensor (/sensor-data), evitando a geração repetida dos mesmos dados em um curto intervalo.

Na API Python, o Redis é usado para armazenar a lista de eventos, garantindo que os dados fiquem disponíveis mesmo que a aplicação seja reiniciada rapidamente.

# Papel do RabbitMQ no fluxo \
O RabbitMQ é usado para comunicação assíncrona entre a API PHP e a API Python.

A API PHP publica mensagens de logística urgente na fila do RabbitMQ.

A API Python fica consumindo essa fila, recebendo as mensagens enviadas pelo PHP, para processar e registrar esses eventos na lista de eventos.
