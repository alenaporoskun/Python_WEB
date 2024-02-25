import pika
import json
from models import Contact
from mongoengine import connect
import configparser

def main():
    # Викликаємо функцію підключення до бази даних
    connect_to_mongodb()

    # Після цього ви можете імпортувати вашу модель та використовувати її
    consume_emails()

def connect_to_mongodb():
    config = configparser.ConfigParser()
    config.read('config.ini')

    mongo_user = config.get('DB', 'user')
    mongodb_pass = config.get('DB', 'pass')
    db_name = config.get('DB', 'db_name')
    domain = config.get('DB', 'domain')

    # Підключення до бази даних MongoDB
    connect(host=f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority", ssl=True)

# Функція для обробки отриманих повідомлень з черги
def callback(ch, method, properties, body):
    # Отримання ідентифікатора контакту з отриманого повідомлення
    contact_id = json.loads(body.decode('utf-8'))['contact_id']

    # Звернення до бази даних та оновлення логічного поля
    try:
        contact = Contact.objects.get(id=contact_id)
        contact.email_sent = True
        contact.save()
        print(f"Повідомлення для контакту {contact.fullname} відправлено!")
    except Contact.DoesNotExist:
        print(f"Контакт з ідентифікатором {contact_id} не знайдено у базі даних.")
    except Exception as e:
        print(f"Виникла помилка під час обробки контакту: {str(e)}")

# Головна функція для обробки повідомлень з черги
def consume_emails():
    # Підключення до RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Оголошення черги для споживання повідомлень
    channel.queue_declare(queue='emails', durable=False)

    # Встановлення зв'язку з обробником повідомлень (callback)
    channel.basic_consume(queue='emails', on_message_callback=callback, auto_ack=True)

    # Вивід повідомлення про початок очікування повідомлень
    print("[*] Очікування повідомлень. Для виходу натисніть CTRL+C")

    # Запуск обробки повідомлень
    channel.start_consuming()

if __name__ == '__main__':
    main()
