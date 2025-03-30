from confluent_kafka import Producer
import asyncio
import json

KAFKA_BROKER = 'localhost:9092,localhost:9093'
TOPIC = 'Topic'

def read_image(image_path):
    with open(image_path, 'rb') as img_file:
        return img_file.read()

async def send_image_to_kafka():
    image_path = 'image.jpg'
    producer = Producer({'bootstrap.servers': KAFKA_BROKER})
    while True:
        image_data = read_image(image_path)
        message = {
            'filename': image_path,
            'image_bytes': image_data.hex()
        }
        json_message = json.dumps(message)
        producer.produce(TOPIC, key=image_path, value=json_message)
        producer.flush()
        print(f'Изображение {image_path} отправлено в Kafka')
        await asyncio.sleep(1)

async def wait_func():
    while True:
        print(f'wait')
        await asyncio.sleep(0.1)

async def main():
    task0 = asyncio.create_task(send_image_to_kafka())
    task1 =  asyncio.create_task(wait_func())
    await asyncio.gather(task0, task1)

if __name__ == "__main__":
    asyncio.run(main())