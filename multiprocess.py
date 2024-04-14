from multiprocessing import Process, Queue
import time

def search_keyword(files, keywords, output_queue):
    results = {}
    for file in files:
        try:
            with open(file, 'r') as f:
                for line in f:
                    for keyword in keywords:
                        if keyword in line:
                            results.setdefault(keyword, []).append(file)
        except Exception as e:
            output_queue.put((file, str(e)))

    output_queue.put(results)

if __name__ == '__main__':
    files = ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt', 'file5.txt']
    keywords = ['culpa', 'artur', 'reprehenderit']

    num_processes = 2  # Number of processes to split the files
    files_per_process = len(files) // num_processes

    output_queue = Queue()

    processes = []

    start_time = time.time()
    
    for i in range(num_processes):
        start_index = i * files_per_process
        end_index = start_index + files_per_process if i != num_processes - 1 else len(files)
        process_files = files[start_index:end_index]

        process = Process(target=search_keyword, args=(process_files, keywords, output_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    # Main process continues to output the results
    results = {}
    while not output_queue.empty():
        result = output_queue.get()
        if isinstance(result, dict):
            for keyword, files_found in result.items():
                results.setdefault(keyword, []).extend(files_found)
        else:
            print(f"Error processing file: {result[0]} - {result[1]}")

    end_time = time.time()
    execution_time = end_time - start_time
    
    for keyword, files_found in results.items():
        print(f"Keyword '{keyword}' found in files: {', '.join(files_found)}")
    
    print("Час виконання багатопроцесового підходу: {:.10f} секунд".format(execution_time))