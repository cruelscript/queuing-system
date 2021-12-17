class Task:
    def __init__(self, startPosition: int, sourceNumber: int,  taskId: str, duration: int) :
        self.startPosition = startPosition  #Начальная позиция заявки на временной диаграмме
        self.sourceNumber = sourceNumber    #Номер источника
        self.taskId = taskId                #Номер заявки
        self.duration = duration            #Время обработки заявки
        self.startTimeInBuffer = 0
        self.endTimeInBuffer = 0
