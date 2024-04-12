## Домашнє завдання #13
   
## Завдання 2

У цьому домашньому завданні необхідно доопрацювати застосунок Django із домашнього завдання 10.  

* Реалізуйте механізм скидання паролю для зареєстрованого користувача;
* Усі змінні середовища повинні зберігатися у файлі .env та використовуватися у файлі settings.py

### Порядок виконання

Щоб запустити віртуальне середовище і запустити [сервер](http://127.0.0.1:8000/):    
```cd project_poetry```  
```poetry shell```  
```cd hw10_project```  
```py .\manage.py runserver```  

## Результат   
  
Головна сторінка сайту з цитатами без авторизації:  
![qoutes_without_authorization](project_poetry/hw10_project/result/qoutes_without_authorization.jpg)  

Сторінка логінізації на сайт:  
![quotes_login](project_poetry/hw10_project/result/quotes_login.jpg)  

Сторінка збросу пароля:  
![quotes_reset_password](project_poetry/hw10_project/result/quotes_reset_password.jpg)   

Лист з переходом на сторінку для збросу пароля:  
![quotes_email_reset_password](project_poetry/hw10_project/result/quotes_email_reset_password.jpg)   

Сторінка для додавання нового автора:   
![create_new_author](project_poetry/hw10_project/result/create_new_author.jpg)  

Сторінка для додавання нової цитати:  
![add_quote](project_poetry/hw10_project/result/add_quote.jpg)  

Останні цитати з новим автором:  
![quotes_end](project_poetry/hw10_project/result/quotes_end.jpg)  
