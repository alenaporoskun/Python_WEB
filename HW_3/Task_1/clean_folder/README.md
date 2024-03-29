# Завдання 1 (Перша частина для потоків)  
  
Напишіть програму обробки папки "Хлам", яка сортує файли у вказаній папці за розширеннями з використанням кількох потоків. Пришвидшіть обробку великих каталогів з великою кількістю вкладених папок та файлів за рахунок паралельного виконання обходу всіх папок в окремих потоках. Найбільш витратним за часом буде перенесення файлу та отримання списку файлів у папці (ітерація по вмісту каталогу). Щоб прискорити перенесення файлів, його можна виконувати в окремому потоці чи пулі потоків. Це тим зручніше, що результат цієї операції ви в додатку не обробляєте та можна не збирати жодних результатів. Щоб прискорити обхід вмісту каталогу з кількома рівнями вкладеності, ви можете обробку кожного підкаталогу виконувати в окремому потоці або передавати обробку в пул потоків.

├── clean_folder  

│    ├── clean_folder   

│    │   ├── clean.py   

│    │   └── __init__.py   
  
│    └── setup.py    
  
│    └── README.md  
    
* Пакет встановлюється в систему командою ```pip install -e .``` (або ```python setup.py install```, потрібні права адміністратора), там де знаходиться файл setup.py.  
* Після установки в системі з'являється пакет clean_folder.  
* Коли пакет встановлений в системі, скрипт можна викликати у будь-якому місці з консолі командою ```clean-folder [шлях до папки]```  

# Завдання скрипту
Сортування файлів по папкам згідно з розширенням.

# Умови для обробки:
* зображення переносимо до папки images ('JPEG', 'PNG', 'JPG', 'SVG');
* документи переносимо до папки documents ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX');
* аудіо файли переносимо до audio ('MP3', 'OGG', 'WAV', 'AMR');
* відео файли до video ('AVI', 'MP4', 'MOV', 'MKV');
* архіви розпаковуються та їх вміст переноситься до папки archives ('ZIP', 'GZ', 'TAR'). 

Крім того, всі файли та папки треба перейменувати, видалив із назви всі символи, що призводять до проблем. Для цього треба застосувати до імен файлів функцію normalize. Слід розуміти, що перейменувати файли треба так, щоб не змінити розширень файлів.

# Приклад, результату виконання скрипту, окрім сортування:  
C:\Users\Admin>clean-folder C:\Users\Admin\Downloads\TRASH  
Файли були відсортовані в папку 'Files'.  
