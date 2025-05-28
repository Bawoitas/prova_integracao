from flask import Flask, request, jsonify
import redis
import threading
import pika
import json

app = Flask(__name__)

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

EVENTS_KEY = 'events-list'

def get_events():
    events_json = r.get(EVENTS_KEY)
    if events_json:
        return json.loads(events_json)
    return []

def save_events(events):
    r.set(EVENTS_KEY, json.dumps(events))

@app.route('/event', methods=['POST'])
def add_event():
    event = request.json
    events = get_events()
    events.append(event)
    save_events(events)
    return 'Evento salvo', 200

@app.route('/events', methods=['GET'])
def list_events():
    events = get_events()
    return jsonify(events)

def consume_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='logistics_queue')

    def callback(ch, method, properties, body):
        event = json.loads(body)
        print('Mensagem recebida do RabbitMQ:', event)
        events = get_events()
        events.append(event)
        save_events(events)

    channel.basic_consume(queue='logistics_queue', on_message_callback=callback, auto_ack=True)
    print('Consumidor RabbitMQ iniciado...')
    channel.start_consuming()

if __name__ == '__main__':
    threading.Thread(target=consume_rabbitmq, daemon=True).start()
    app.run(port=5000)
