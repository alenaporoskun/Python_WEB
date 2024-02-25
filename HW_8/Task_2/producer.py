import pika
import json
from faker import Faker
from models import Contact
import configparser
from mongoengine import connect

def connect_to_mongodb():
    config = configparser.ConfigParser()
    config.read('config.ini')

    mongo_user = config.get('DB', 'user')
    mongodb_pass = config.get('DB', 'pass')
    db_name = config.get('DB', 'db_name')
    domain = config.get('DB', 'domain')

    # Підключення до бази даних MongoDB
    connect(host=f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority", ssl=True)

def generate_fake_contacts(num_contacts):
    fake = Faker()
    contacts = []
    for _ in range(num_contacts):
        contact = Contact(
            fullname=fake.name(),
            email=fake.email(),
            email_sent=False  # Поле для відстеження статусу надсилання
            # Додайте інші поля, які необхідно заповнити
        )
        contacts.append(contact)
    return contacts

def save_contacts_to_database(contacts):
    for contact in contacts:
        contact.save()

def publish_contacts(contacts):
    # Підключення до RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Визначення черги
    channel.queue_declare(queue='emails', durable=False)

    # Опублікування кожного контакту у черзі
    for contact in contacts:
        message = {'contact_id': str(contact.id)}
        channel.basic_publish(exchange='', routing_key='emails', body=json.dumps(message))
        print(f"Повідомлення для контакту {contact.fullname} опубліковано у черзі.")

    # Закриття підключення
    connection.close()

if __name__ == '__main__':
    # Підключення до бази даних MongoDB
    connect_to_mongodb()

    # Генерування фейкових контактів
    contacts = generate_fake_contacts(5)

    # Збереження контактів у базі даних
    save_contacts_to_database(contacts)

    # Публікація контактів у черзі
    publish_contacts(contacts)
