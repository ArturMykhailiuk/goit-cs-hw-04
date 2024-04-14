import threading
import time

# Функція для пошуку ключових слів у файлі
def search_keywords_in_files(files, keywords, results):
    for file in files:
        try:
            with open(file, 'r') as f:
                for line in f:
                    for keyword in keywords:
                        if keyword in line:
                            results.setdefault(keyword, []).append(file)
        except FileNotFoundError as e:
            print(f"File {file} not found: {e}")
        except PermissionError as e:
            print(f"Permission denied for file {file}: {e}")
        except OSError as e:
            print(f"OS error occurred while processing file {file}: {e}")


files = ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt']

keywords = ['culpa', 'artur', 'reprehenderit']

results = {}

# Розділення файлів між різними потоками
num_threads = 4
files_per_thread = len(files) // num_threads
threads = []
start_time = time.time()

for i in range(num_threads):
    start_index = i * files_per_thread
    end_index = start_index + files_per_thread if i < num_threads - 1 else len(files)
    thread = threading.Thread(target=search_keywords_in_files, args=(files[start_index:end_index], keywords, results))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

end_time = time.time()
execution_time = end_time - start_time

for keyword, files_found in results.items():
    print(f"Keyword '{keyword}' found in files: {', '.join(files_found)}")

print("Час виконання багатопотокового підходу: {:.10f} секунд".format(execution_time))