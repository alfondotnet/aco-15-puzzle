import multiprocessing

class Consumer(multiprocessing.Process):
    
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        
        while True:
            
            next_task = self.task_queue.get()

            if next_task is None:
                
                # Poison pill means shutdown
                print ("soy "+ proc_name + " y estoy saliendo!")
                self.task_queue.task_done()
                break

            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)
            
        return
