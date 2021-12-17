import task


class Device:
    def __init__(self, deviceNumber: int):
        self.deviceNumber = deviceNumber
        self.currentPosition = 0
        self.currentTask = None
        self.busy = False
        self.durations = []

    def setTask(self, task_: task.Task, position):
        self.busy = True
        self.currentPosition = position
        self.currentTask = task_
        self.durations.append(task_.duration)

    def completeTask(self):
        self.busy = False
        self.currentTask = None
