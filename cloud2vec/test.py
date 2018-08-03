import multiprocessing


process_number = None


	def initializer(queue):
    global process_number

    process_number = queue.get()  # atomic get the process index


def function(value):
    print("I'm process %s" % process_number)

    return value[process_number]


def main():
    queue = multiprocessing.Queue()

    for index in range(multiprocessing.cpu_count()):
        queue.put(index)

    pool = multiprocessing.Pool(initializer=initializer, initargs=[queue])

    tasks = [{0: 'Process-0', 1: 'Process-1', 2: 'Process-2'}, ...]

    print(pool.map(function, tasks))
