from buffer import Buffer
from event import Event, EventType
from source import Source
from device import Device
import sys

from sympy.solvers import solve
from sympy import Symbol
import matplotlib.pyplot as plot


class Controller:
    def __init__(self) -> None:
        self.currentPosition = 0  # Position in time
        self.totalTasksRequired = 0
        self.countTasks = 0

        self.sources = []
        self.devices = []
        self.buffers = []
        self.events = []

        self.countTasksReq = 0
        self.currentCountTasks = 0
        self.completedTasksCount = 0

        self.currentDevice = 0
        self.currentBuffer = 0
        self.lastBufferWithTask = None

        self.a = 0
        self.b = 0
        self.lambda_ = 0.1
        self.buf_num = 0
        self.device_num = 0
        self.source_num = 0

    # =================== INITIALIZATION ====================
    def initSource(self, countSource, a, b, lambda_):
        if countSource < 1:
            return None
        self.sources = []
        for source_index in range(0, countSource):
            temp_source = Source(source_index)
            temp_source.setDistribution(a, b)
            self.sources.append(temp_source)

    def initDevices(self, countDevices):
        if countDevices < 1:
            return None
        self.devices = []
        for devices_index in range(0, countDevices):
            self.devices.append(Device(devices_index))

    def initBuffers(self, countBuffers):
        if countBuffers < 1:
            return None
        self.buffers = []
        for buffer_index in range(0, countBuffers):
            self.buffers.append(Buffer(buffer_index))

    def initEvent(self):
        self.events = []
        self.events.append(Event(0, EventType['GenerateTask'], 0))

    # =================== ANALYTICS ====================
    def findP(self):
        t = 1.643
        q = 0.1
        p = Symbol('p')
        return solve(self.countTasksReq - (t * t * (1 - p)) / (p * q * q), p)

    def findN(self, p):
        t = 1.643
        q = 0.1
        N = Symbol('N')
        return solve(N - (t * t * (1 - p)) / (p * q * q), N)

    def findOptimalN(self):
        # self.countTasksReq = 100
        old_p = self.findP()[0]
        while True:
            self.countTasksReq = self.findN(old_p)[0]
            if (self.findP()[0] - old_p) / old_p < 0.1:
                break
            else:
                old_p = self.findP()[0]
        return self.countTasksReq

    def reinitController(self):
        self.currentPosition = 0  # Position in time
        self.countTasks = 0
        self.currentCountTasks = 0
        self.completedTasksCount = 0
        self.currentDevice = 0
        self.currentBuffer = 0
        self.lastBufferWithTask = None
        self.initSource(self.source_num, self.a, self.b, self.lambda_)
        self.initDevices(self.device_num)
        self.initBuffers(self.buf_num)
        self.initEvent()

    def doAutomaticMode(self):
        figure, ox = plot.subplots()

        # =============== DEVICES ===============
        self.source_num = 20
        self.buf_num = 20
        self.countTasksReq = 500
        cancel_prob = []
        residence_task_time = []
        using_coeff = []

        for i in range(1, 50, 2):
            self.device_num = i
            self.reinitController()
            while True:
                self.doForwardStep()
                if self.completedTasksCount == self.countTasksReq:
                    break

            stat_sources = self.getSourcesStatistic()
            cancel_prob.append(sum(stat_sources['cancel_prob']) / len(stat_sources['cancel_prob']))
            residence_task_time.append(sum(stat_sources['residence_task_time']) / len(stat_sources['residence_task_time']))

            stat_devices = self.getDevicesStatistic()
            using_coeff.append(sum(stat_devices['using_coeff']) / len(stat_devices['using_coeff']))

        ox.title.set_text('Device number')
        ox.plot(cancel_prob)
        figure.savefig('web/images/1.png')
        ox.cla()

        ox.title.set_text('Device number')
        ox.plot(residence_task_time)
        figure.savefig('web/images/2.png')
        ox.cla()

        ox.title.set_text('Device number')
        ox.plot(using_coeff)
        figure.savefig('web/images/3.png')
        ox.cla()

        # =============== BUFFERS ===============
        self.source_num = 20
        self.device_num = 20
        self.countTasksReq = 500
        cancel_prob = []
        residence_task_time = []
        using_coeff = []

        for i in range(1, 50, 2):
            self.buf_num = i
            self.reinitController()
            while True:
                self.doForwardStep()
                if self.completedTasksCount == self.countTasksReq:
                    break

            stat_sources = self.getSourcesStatistic()
            cancel_prob.append(sum(stat_sources['cancel_prob']) / len(stat_sources['cancel_prob']))
            residence_task_time.append(sum(stat_sources['residence_task_time']) / len(stat_sources['residence_task_time']))

            stat_devices = self.getDevicesStatistic()
            using_coeff.append(sum(stat_devices['using_coeff']) / len(stat_devices['using_coeff']))

        ox.title.set_text('Buffer number')
        ox.plot(cancel_prob)
        figure.savefig('web/images/4.png')
        ox.cla()

        ox.title.set_text('Buffer number')
        ox.plot(residence_task_time)
        figure.savefig('web/images/5.png')
        ox.cla()

        ox.title.set_text('Buffer number')
        ox.plot(using_coeff)
        figure.savefig('web/images/6.png')
        ox.cla()

        # =============== SOURCES ===============
        self.buf_num = 20
        self.device_num = 20
        self.countTasksReq = 500
        cancel_prob = []
        residence_task_time = []
        using_coeff = []

        for i in range(1, 50, 2):
            self.source_num = i
            self.reinitController()
            while True:
                self.doForwardStep()
                if self.completedTasksCount == self.countTasksReq:
                    break

            stat_sources = self.getSourcesStatistic()
            cancel_prob.append(sum(stat_sources['cancel_prob']) / len(stat_sources['cancel_prob']))
            residence_task_time.append(sum(stat_sources['residence_task_time']) / len(stat_sources['residence_task_time']))

            stat_devices = self.getDevicesStatistic()
            using_coeff.append(sum(stat_devices['using_coeff']) / len(stat_devices['using_coeff']))

        ox.title.set_text('Source number')
        ox.plot(cancel_prob)
        figure.savefig('web/images/7.png')
        ox.cla()

        ox.title.set_text('Source number')
        ox.plot(residence_task_time)
        figure.savefig('web/images/8.png')
        ox.cla()

        ox.title.set_text('Source number')
        ox.plot(using_coeff)
        figure.savefig('web/images/9.png')
        ox.cla()

    def getSourcesStatistic(self):
        statistic = {
            "cancel_prob": [],
            "total_task": [],
            "residence_task_time": [],
            "in_buffers_time": [],
            "in_devices_time": [],
        }

        for source in self.sources:
            if source.tasksGenerated > 0:
                statistic['cancel_prob'].append(source.taskCanceled / source.tasksGenerated)
                statistic['total_task'].append(source.tasksGenerated)
                statistic['residence_task_time'].append(sum(source.durations) / self.countTasks + sum(
                    source.taskWaitedTimes) / self.completedTasksCount)
                statistic['in_buffers_time'].append(sum(source.taskWaitedTimes) / self.completedTasksCount)
                statistic['in_devices_time'].append(sum(source.durations) / self.completedTasksCount)

        return statistic

    def getDevicesStatistic(self):
        statistic = {
            "using_coeff": []
        }

        for device in self.devices:
            using_coeff = sum(device.durations) / self.currentPosition
            if using_coeff > 1:
                using_coeff = 1
            statistic["using_coeff"].append(using_coeff)

        return statistic

    # =================== STEP MODE ====================

    def doForwardStep(self):
        self.events = []

        free_device = self.findFreeDeviceRound()
        free_buffer = self.findFreeBufferRound()
        complete_device = self.findCompleteDevice()
        unbuff_buffer = self.findBufferWithLastAddedTask()
        current_source = self.findSourceGen()

        objects = []

        if complete_device and complete_device.busy:
            objects.append({0: complete_device.currentTask.startPosition + complete_device.currentTask.duration})
        if current_source:
            objects.append({1: current_source.currPosition})

        minEventTime = [-1, sys.float_info.max]

        # Поиск ближайшего ивента
        for obj in objects:
            for index, eventTime in obj.items():
                if eventTime < minEventTime[1]:
                    minEventTime = [index, eventTime]

        # Обработка ивента - завершение заявки и освобождения прибора
        if complete_device and minEventTime[0] == 0:
            self.events.append(Event(self.currentPosition, EventType["TaskCompleted"], complete_device.deviceNumber))
            self.currentPosition = complete_device.currentTask.startPosition + complete_device.currentTask.duration
            self.sources[complete_device.currentTask.sourceNumber].durations.append(
                self.sources[complete_device.currentTask.sourceNumber].currDuration)
            complete_device.completeTask()
            free_device = self.findFreeDeviceRound()
            self.completedTasksCount += 1
            return

        # Обработка ивента - вывод заявки и освобождения буфера
        if self.findFreeDeviceRound() != None and unbuff_buffer != None:
            unbuff_task = unbuff_buffer.getTask()
            if free_device != None:
                unbuff_task.startPosition = self.currentPosition
                unbuff_task.endTimeInBuffer = self.currentPosition
                waited_task_time = unbuff_task.endTimeInBuffer - unbuff_task.startTimeInBuffer
                if waited_task_time > 0:
                    self.sources[unbuff_task.sourceNumber].taskWaitedTimes.append(waited_task_time)
                free_device.setTask(unbuff_task, self.currentPosition)
                free_buffer = self.findFreeBufferRound()
                self.events.append(Event(self.currentPosition, EventType["TaskUnbuffer"], unbuff_buffer.bufferNumber))
                self.currentPosition = unbuff_task.startPosition
                return
            else:
                print('Error...')

        # Обработка ивента - генерация заявки
        if minEventTime[0] == 1:
            current_source.setNextDuration(self.lambda_)
            self.currentPosition = current_source.currPosition
            free_device = self.findFreeDeviceRound()
            free_buffer = self.findFreeBufferRound()

            # Ставим новую заявку в свободный прибор
            if free_device != None:
                task = current_source.generateNewTask(self.countTasks, self.currentPosition)
                self.countTasks += 1
                self.events.append(Event(self.currentPosition, EventType["GenerateTask"], current_source.sourceNumber))
                free_device.setTask(task, task.startPosition)
                return

            # Ставим новую заявку в свободный буфер, если все приборы заняты
            elif free_buffer != None:
                task = current_source.generateNewTask(self.countTasks, -1)
                task.startTimeInBuffer = self.currentPosition
                self.countTasks += 1
                self.events.append(Event(self.currentPosition, EventType["GenerateTask"], current_source.sourceNumber))
                free_buffer.setTask(task)
                return

            # Дисц-на отказа (самая старая заявка в буфере)
            else:
                task = current_source.generateNewTask(self.countTasks, -1)
                task.startTimeInBuffer = self.currentPosition
                self.events.append(Event(self.currentPosition, EventType["TaskCancel"], -1))
                self.findBufferWithOldestTask().setTask(task, True)
                self.countTasks += 1
                current_source.taskCanceled += 1

    # Возвращает свободный буфер, поиск по кольцу
    def findFreeBufferRound(self):
        buffer_to_task = None
        start_buffer = self.currentBuffer

        while True:
            if self.currentBuffer >= len(self.buffers):
                self.currentBuffer = 0
            elif not self.buffers[self.currentBuffer].busy:
                buffer_to_task = self.buffers[self.currentBuffer]
                break
            else:
                self.currentBuffer += 1
            if self.currentBuffer == start_buffer:
                break

        return buffer_to_task

    # Возвращаем буфер с самой новой заявкой
    def findBufferWithLastAddedTask(self):
        max_task_num = 0
        buffer_to_return = None
        for buffer_ in self.buffers:
            if buffer_.busy and buffer_.currentTask.taskId > max_task_num:
                max_task_num = buffer_.currentTask.taskId
                buffer_to_return = buffer_

        return buffer_to_return

    # Возвращаем буфер с самой старой заявкой
    def findBufferWithOldestTask(self):
        min_task_num = sys.maxsize
        buffer_to_return = None
        for buffer_ in self.buffers:
            if buffer_.currentTask.taskId < min_task_num:
                min_task_num = buffer_.currentTask.taskId
                buffer_to_return = buffer_

        return buffer_to_return

    # Ищем свободный прибор (приоритет по номеру прибора)
    def findFreeDeviceRound(self):
        device_to_return = None
        for device in self.devices:
            if not device.busy:
                device_to_return = device
                break

        return device_to_return

    # Ищем прибор, где должна завершится заявка
    def findCompleteDevice(self):
        min_time_device = None
        min_time_device_time = sys.maxsize
        for device in self.devices:
            if device.busy:
                if device.currentTask.startPosition + device.currentTask.duration <= min_time_device_time:
                    min_time_device = device
                    min_time_device_time = device.currentTask.startPosition + device.currentTask.duration

        return min_time_device

    # Ищем источник для генерации заявки
    def findSourceGen(self):
        current_source = self.sources[0]
        for source in self.sources:
            if source.currPosition < current_source.currPosition:
                current_source = source

        return current_source
