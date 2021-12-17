import task
import numpy
import random


class Source:
    def __init__(self, sourceNumber: int):
        self.sourceNumber = sourceNumber  # Номер источника
        self.tasksGenerated = 0  # Количество сгенерированных задач
        self.taskCanceled = 0  # Кол-во отмененных заявок
        self.currPosition = 0  # Текушая позиция новой заявки
        self.currDuration = 0  # Текущее время обработки заявки
        self.lengthStep = 0  # Шаг между заявками
        self.durations = []
        self.taskWaitedTimes = []

    def generateNewTask(self, taskId, Pos):
        self.currPosition += self.lengthStep
        self.tasksGenerated += 1
        return task.Task(Pos, self.sourceNumber, taskId, self.currDuration)

    def setDistribution(self, a: float, b: float):
        self.lengthStep = numpy.random.uniform(a, b)
        self.currPosition = self.lengthStep

    def setNextDuration(self, lambda_):
        self.currDuration = random.expovariate(lambda_)
