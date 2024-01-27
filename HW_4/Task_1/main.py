from http.server import HTTPServer, BaseHTTPRequestHandler
import mimetypes
import os
import urllib.parse
import socketserver
import json
from datetime import datetime
import threading
import socket

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Перевіряємо, чи шлях запиту є кореневим ('/')
        if self.path == '/':
            # Якщо так, обробляємо домашню сторінку
            self.handle_home()
        else:
            # Якщо шлях не кореневий, обробляємо статичний контент
            self.handle_static()

    def do_POST(self):
        # Отримуємо розмір тіла POST-запиту з заголовку Content-Length
        content_length = int(self.headers['Content-Length'])

        # Зчитуємо тіло POST-запиту з вхідного потоку та декодуємо його з UTF-8
        data = self.rfile.read(content_length).decode('utf-8')

        # Використовуємо parse_qs для перетворення рядка даних на словник
        data_dict = urllib.parse.parse_qs(data)

        # Отримуємо значення 'username' та 'message'
        username = data_dict.get('username', [''])[0]
        message = data_dict.get('message', [''])[0]

        # Отримуємо час отримання повідомлення
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        # Створюємо словник для data.json
        new_data = {
            "username": username,
            "message": message
        }
        print(f"Отримано дані з форми: {new_data}")

        # Отримуємо шлях до файлу data.json
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'storage', 'data.json')

        # Перевіряємо, чи існує data.json і завантажуємо наявні дані
        data_dict_all = {}
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                data_dict_all = json.load(f)

        # Додаємо нові дані до словника
        data_dict_all[timestamp] = new_data

        print(f"Нові дані для data.json: {new_data}")

        # Записуємо оновлений словник даних у data.json
        with open(json_path, 'w') as f:
            json.dump(data_dict_all, f, indent=2)

        # Відправляємо перенаправлення клієнту
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()


    def send_to_socket_server(self, data_dict):
        # Надсилання даних на Socket-сервер за допомогою UDP

        # Створення UDP-сокету
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # Адреса та порт Socket-сервера
            server_address = ('localhost', 5000)

            # Підготовка повідомлення для відправки у форматі JSON з використанням поточного часу
            message = json.dumps({str(datetime.now()): data_dict})

            # Відправка повідомлення на Socket-сервер
            client_socket.sendto(message.encode(), server_address)
        except Exception as e:
            print(f"Error sending data to Socket server: {e}")
        finally:
            # Закриття сокету після відправки
            client_socket.close()


    def handle_home(self):
        # Отримання поточної робочої директорії
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Формування шляху до файлу 'index.html' в поточній директорії
        index_path = os.path.join(current_directory, 'index.html')

        # Виклик методу для відправлення HTML-файлу на клієнтську сторону
        self.send_html_file(index_path)


    def handle_static(self):
        # Формування шляху до запитаного статичного файлу на основі шляху в HTTP-запиті
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.path[1:])

        # Перевірка існування файлу за вказаним шляхом
        if os.path.exists(file_path):
            # Відправлення статичного файлу, якщо файл існує
            self.send_static(file_path)
        else:
            # Якщо файл не знайдено, відправлення сторінки з помилкою 404
            error_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'error.html')
            self.send_html_file(error_path, 404)


    def send_html_file(self, filename, status=200):
        # Відправлення відповіді з HTTP-статусом та заголовками
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Відкриття та читання вмісту HTML-файлу
        with open(filename, 'rb') as fd:
            # Відправлення вмісту файлу через вихідний потік (self.wfile)
            self.wfile.write(fd.read())


    def send_static(self, file_path):
        # Встановлення HTTP-статусу 200 для успішного відправлення статичного файлу
        self.send_response(200)
        
        # Визначення MIME-типу файлу
        mt = mimetypes.guess_type(file_path)
        
        # Встановлення заголовка Content-type на основі MIME-типу файлу
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            # Якщо MIME-тип не визначено, встановлення заголовка як 'text/plain'
            self.send_header("Content-type", 'text/plain')
        
        # Завершення заголовків перед відправленням вмісту
        self.end_headers()
        
        # Читання та відправлення вмісту файлу через вихідний потік
        with open(file_path, 'rb') as file:
            self.wfile.write(file.read())


class SocketServerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Отримання та виведення даних від HTTP сервера
        data = self.request[0].decode()
        print(f"Отримані дані від HTTP сервера: {data}")

        try:
            # Розшифрування отриманих даних у форматі JSON
            data_dict = json.loads(data)

            # Створення шляху до директорії для зберігання файлу data.json
            storage_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'storage')
            if not os.path.exists(storage_directory):
                os.makedirs(storage_directory)

            # Формування шляху до файлу data.json
            json_path = os.path.join(storage_directory, 'data.json')
            data_dict_all = {}

            # Перевірка існування файлу data.json та завантаження наявних даних
            if os.path.exists(json_path):
                with open(json_path, 'r') as f:
                    data_dict_all = json.load(f)

            # Додавання нових даних до словника
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            new_data = {
                "username": data_dict.get("username", ""),
                "message": data_dict.get("message", "")
            }
            data_dict_all[timestamp] = new_data

            # Виведення нових даних, які будуть записані в data.json
            print("Нові дані для data.json:")
            print(new_data)

            # Запис оновленого словника даних у файл data.json
            with open(json_path, 'w') as f:
                json.dump(data_dict_all, f, indent=2)
        except json.JSONDecodeError as e:
            print(f"Помилка декодування JSON-даних: {e}")


def run_http_server():
    # Конфігурація адреси та порту для HTTP сервера
    server_address = ('', 3000)
    
    # Створення екземпляру HTTP сервера з вказаною адресою та обробником
    http_server = HTTPServer(server_address, HttpHandler)
    
    try:
        # Запуск HTTP сервера та виведення повідомлення про старт
        print('Starting HTTP server...')
        http_server.serve_forever()
    except KeyboardInterrupt:
        # Обробка переривання з клавіатури та виведення повідомлення про зупинку сервера
        print('Shutting down HTTP server...')
        http_server.server_close()


def run_socket_server():
    # Конфігурація адреси та порту для Socket сервера
    socket_server_address = ('', 5000)
    
    # Створення екземпляру UDP сервера з вказаною адресою та обробником (SocketServerHandler)
    socket_server = socketserver.UDPServer(socket_server_address, SocketServerHandler)
    
    try:
        # Запуск Socket сервера та виведення повідомлення про старт
        print('Starting Socket server...')
        socket_server.serve_forever()
    except KeyboardInterrupt:
        # Обробка переривання з клавіатури та виведення повідомлення про зупинку сервера
        print('Shutting down Socket server...')
        socket_server.server_close()


if __name__ == '__main__':
    # Створення окремого потоку для запуску HTTP сервера
    http_server_thread = threading.Thread(target=run_http_server)
    
    # Створення окремого потоку для запуску Socket сервера
    socket_server_thread = threading.Thread(target=run_socket_server)

    # Запуск потоків для HTTP та Socket серверів
    http_server_thread.start()
    socket_server_thread.start()

    # Очікування завершення виконання потоків
    http_server_thread.join()
    socket_server_thread.join()
    