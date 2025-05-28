<?php

require_once __DIR__ . '/vendor/autoload.php';  

use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

$uri = $_SERVER['REQUEST_URI'];

header('Content-Type: application/json');

if ($uri == '/equipments' && $_SERVER['REQUEST_METHOD'] == 'GET') {

    $equipments = [
        ['id' => 1, 'name' => 'Bomba de oleo'],
        ['id' => 2, 'name' => 'Tubo de extracao'],
        ['id' => 3, 'name' => 'Valvula de pressao'],
    ];
    echo json_encode($equipments);
    exit();
}

if ($uri == '/dispatch' && $_SERVER['REQUEST_METHOD'] == 'POST') {
    $data = json_decode(file_get_contents('php://input'), true);

    $connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
    $channel = $connection->channel();
    $channel->queue_declare('logistics_queue', false, false, false, false);

    $msg = new AMQPMessage(json_encode($data));
    $channel->basic_publish($msg, '', 'logistics_queue');

    $channel->close();
    $connection->close();

    echo json_encode(['status' => 'Mensagem enviada para RabbitMQ']);
    exit();
}

// Se não reconhee rota
http_response_code(404);
echo json_encode(['error' => 'Rota nao encontrada']);
