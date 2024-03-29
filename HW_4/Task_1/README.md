## Завдання 1

## Завдання

Ваша мета реалізувати найпростіший веб-додаток. За основу взяти наступні файли.  

За аналогією з розглянутим прикладом у конспекті, створіть веб-додаток з маршрутизацією для двох html сторінок: index.html та message.html.  

Також:

* Обробіть під час роботи програми статичні ресурси: style.css, logo.png;  
* Організуйте роботу з формою на сторінці message.html;   
* У разі виникнення помилки 404 Not Found повертайте сторінку error.html
* Ваша програма працює на порту 3000
  
Для роботи з формою створіть Socket сервер на порту 5000. Алгоритм роботи такий. Ви вводите дані у форму, вони потрапляють у ваш веб-додаток, який пересилає його далі на обробку за допомогою socket (протокол UDP), Socket серверу. Socket сервер переводить отриманий байт-рядок у словник і зберігає його в json файл data.json в папку storage.

Формат запису файлу data.json наступний:  

```
{
  "2022-10-29 20:20:58.020261": {
    "username": "krabaton",
    "message": "First message"
  },
  "2022-10-29 20:21:11.812177": {
    "username": "Krabat",
    "message": "Second message"
  }
}
```

Де ключ кожного повідомлення - це час отримання повідомлення: datetime.now(). Тобто кожне нове повідомлення від веб-програми дописується до файлу storage/data.json з часом отримання.

Використовуйте для створення вашої веб-програми один файл main.py. Запустіть HTTP сервер і Socket сервер у різних потоках.

## Запуск програми

Для початку роботи треба виконати файл main.py.

За адресою
```
http://localhost:3000/ 
```
можна переглянути завантажену сторінку та відправити повідомлення. 

## Результат виконання програми 

Повідомлення зберігаються в файлі data.json:  
```
{
  "2024-01-27 13:50:27.146230": {
    "username": "olena",
    "message": "Please send me more information about Python WEB."
  },
  "2024-01-27 13:51:21.060830": {
    "username": "lily",
    "message": "Good topics!"
  }
}
```