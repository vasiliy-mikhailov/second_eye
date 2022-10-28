from threading import Thread

def run_tasks_in_parallel(tasks):
    threads = [Thread(target=task) for task in tasks]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
        # print("{} done".format(thread))