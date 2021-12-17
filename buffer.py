import task


class Buffer:
    def __init__(self, buffer_index):
        self.currentTask = None
        self.currPosition = 0
        self.busy = False
        self.bufferNumber = buffer_index
        self.currentBuffer = 0

    def setTask(self, task_: task.Task, flag=False):
        if not self.busy or flag:
            self.busy = True
            self.currentTask = task_
            self.currPosition = task_.startPosition

    def getTask(self):
        return_task = self.currentTask
        self.busy = False
        self.currentTask = None

        return return_task
