import time
import pytest
from confluent_kafka import Producer, Consumer, KafkaException

BROKER = "localhost:9092"
TOPIC_INPUT = "meu_topico_inicial"
TOPIC_SUCCESS = "meu_topico_sucesso"
GROUP_ID = "meu_grupo_consumer"

@pytest.fixture
def kafka_producer():
    return Producer({"bootstrap.servers": BROKER})

@pytest.fixture
def kafka_consumer():
    consumer = Consumer({
        "bootstrap.servers": BROKER,
        "group.id": GROUP_ID,
        "auto.offset.reset": "earliest"
    })
    consumer.subscribe([TOPIC_SUCCESS])
    yield consumer
    consumer.close()

def test_kafka_workflow(kafka_producer, kafka_consumer):
    # ID da mensagem que será enviada
    mensagem_id = "12345"
    
    # Produz a mensagem para o tópico inicial
    kafka_producer.produce(TOPIC_INPUT, key=mensagem_id, value="Mensagem de teste")
    kafka_producer.flush()

    # Verifica se a mensagem de sucesso chegou no tópico de sucesso
    timeout = 10  # Tempo máximo de espera (segundos)
    start_time = time.time()

    while time.time() - start_time < timeout:
        msg = kafka_consumer.poll(1.0)  # Poll com timeout de 1 segundo
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())

        # Verifica se a mensagem no tópico de sucesso corresponde ao ID esperado
        if msg.key().decode("utf-8") == mensagem_id:
            assert msg.value().decode("utf-8") == "Sucesso"
            print("Mensagem de sucesso encontrada!")
            return

    pytest.fail(f"Mensagem de sucesso para ID {mensagem_id} não encontrada no tópico {TOPIC_SUCCESS}.")