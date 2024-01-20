import os
import shutil
import concurrent.futures
from pathlib import Path

def main():
    if len(os.sys.argv) != 2:
        print("Потрібно вказати шлях до папки.")
        return

    source_folder = os.sys.argv[1]

    if not os.path.exists(source_folder):
        print("Зазначений шлях не існує.")
        return

    # Створюємо папку Files, куди будуть переміщені файли
    destination_folder = os.path.join(source_folder, "Files")
    os.makedirs(destination_folder, exist_ok=True)

    # Викликаємо функцію для сортування файлів у папці та її вкладених папках,
    # результат - словник зі списками файлів по групам, відомі та невідомі скрипту розширення
    dict_files, extensions, unknown_extensions = sort_files_parallel(source_folder, destination_folder)
    #print('Словник зі списками файлів по групам:')
    for key, value in dict_files.items():
        #print(key, value)
        pass

    extensions = list(extensions)
    unknown_extensions = list(unknown_extensions)
    #print('Розширення, відомі скрипту:    ', extensions)
    #print('Розширення, невідомі скрипту:  ', unknown_extensions)

    print("Файли були відсортовані в папку 'Files'.")


def process_file(args):
    file, destination_folder = args
    source_path = file
    file_extension = Path(file).suffix.upper()

    try:
        if file_extension in ('.JPEG', '.PNG', '.JPG', '.SVG'):
            destination_path = os.path.join(destination_folder, 'images', os.path.basename(file))
        elif file_extension in ('.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'):
            destination_path = os.path.join(destination_folder, 'documents', os.path.basename(file))
        elif file_extension in ('.MP3', '.OGG', '.WAV', '.AMR'):
            destination_path = os.path.join(destination_folder, 'audio', os.path.basename(file))
        elif file_extension in ('.AVI', '.MP4', '.MOV', '.MKV'):
            destination_path = os.path.join(destination_folder, 'video', os.path.basename(file))
        elif file_extension in ('.ZIP', '.GZ', '.TAR'):
            destination_path = os.path.join(destination_folder, 'archives', os.path.basename(file))
        else:
            destination_path = os.path.join(destination_folder, 'unknown', os.path.basename(file))
            unknown_extensions.add(file_extension)

        # Переміщення файлу
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        shutil.move(source_path, destination_path)

    except Exception as e:
        print(f"Error processing file {file}: {e}")

def sort_files_parallel(source_folder, destination_folder):
    # Ініціалізуємо необхідні множини
    images, documents, audio, video, archives = set(), set(), set(), set(), set()
    extensions, unknown_extensions = set(), set()

    # Отримуємо список файлів
    files = [os.path.join(root, file) for root, _, files in os.walk(source_folder) for file in files]

    # Використовуємо ProcessPoolExecutor для паралельної обробки файлів
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Викликаємо функцію process_file для кожного файлу у окремому процесі
        args_list = [(file, destination_folder) for file in files]
        executor.map(process_file, args_list)

    # Створюємо словник зі списками файлів по групам
    dict_files = {'images': list(images), 'documents': list(documents), 'audio': list(audio),
                  'video': list(video), 'archives': list(archives)}

    return dict_files, extensions, unknown_extensions

if __name__ == "__main__":
    main()