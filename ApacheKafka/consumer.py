from confluent_kafka import Consumer
import json
import binascii
import multiprocessing

KAFKA_BROKER = 'localhost:9092,localhost:9093'
TOPIC = 'Topic'
GROUP_ID = 'image_consumer'

def save_image(filename, image_hex):
    image_bytes = binascii.unhexlify(image_hex)
    with open(filename, 'wb') as img_file:
        img_file.write(image_bytes)
    print(f'Изображение сохранено как {filename}')

def read_image_from_kafka(coid):
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': GROUP_ID,
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe([TOPIC])
    count = 0
    while True:
        count += 1
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f'Ошибка: {msg.error()}')
            continue
        
        data = json.loads(msg.value().decode('utf-8'))
        save_image(f"./Output/{data['filename'][:-4]}_{coid}_{count}.jpg", data['image_bytes'])

if __name__ == "__main__":
    num_consumers = 4
    processes = []
    
    for i in range(num_consumers):
        p = multiprocessing.Process(target=read_image_from_kafka, args=(i+1,))
        p.start()
        processes.append(p)
    
    for p in processes:
        p.join()