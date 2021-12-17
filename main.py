import eel
from event import EventType
from controller import Controller

controller = Controller()
eel.init('web')


@eel.expose
def autoMode():
    controller.doAutomaticMode()


@eel.expose
def nextStep():
    controller.doForwardStep()
    state_json = {
        "buffers": getBuffersState(),
        "devices": getDevicesState(),
        "system": getSystemState(),
        "sources": getSourceState(),
    }

    return state_json


@eel.expose
def getBuffersState():
    buffers = []
    for buffer in controller.buffers:
        number_buffer = buffer.bufferNumber
        number_task = None

        if buffer.currentTask:
            number_source = buffer.currentTask.sourceNumber
            number_task = buffer.currentTask.taskId
        else:
            number_source = "Cвободен"

        buffers.append({
            "number_buffer": number_buffer,
            "number_source": number_source,
            "number_task": number_task,
        })

    return buffers


@eel.expose
def getDevicesState():
    devices = []
    for device in controller.devices:
        number_buffer = device.deviceNumber
        if device.busy:
            device_state = 'Занят'
        else:
            device_state = 'Свободен'

        if device.busy:
            start_time = device.currentPosition
        else:
            start_time = '-'
        number_task = None
        duration = None
        if device.currentTask:
            number_task = device.currentTask.taskId
            duration = device.currentTask.duration

        devices.append({
            "number_device": number_buffer,
            "device_state": device_state,
            "start_time": start_time,
            "number_task": number_task,
            "duration": duration
        })

    return devices


@eel.expose
def getSystemState():
    system = []
    for event in controller.events:
        time = controller.currentPosition
        action = None
        designated_device = event.deviceId
        time_event = event.eventTime

        if event.eventType == EventType['GenerateTask']:
            action = "Генерация заявки"
        elif event.eventType == EventType['TaskUnbuffer']:
            action = "Вывод заявки из буфера"
        elif event.eventType == EventType['TaskCompleted']:
            action = "Завершения заявки"
        elif event.eventType == EventType['TaskCancel']:
            action = "Отмена заявки"

        system.append({
            "time": time,
            "action": action,
            "designated_device": designated_device,
            "time_event": time_event
        })

    return system


@eel.expose
def getSourceState():
    sources = []
    for source in controller.sources:
        state = 'Занят'

        sources.append({
            "time": source.currPosition,
            "step": source.lengthStep,
            "state": state,
            "countTasks": source.tasksGenerated,
        })

    return sources


@eel.expose
def initController(source_number_, buffer_number_, device_number_, _lambda, a, b, task_count_):
    global controller
    controller.countTasksReq = int(task_count_)
    controller.lambda_ = float(_lambda)
    controller.a = float(a)
    controller.b = float(b)
    controller.buf_num = buffer_number_
    controller.source_num = source_number_
    controller.device_num = device_number_
    controller.initSource(int(source_number_), float(a), float(b), float(_lambda))
    controller.initDevices(int(device_number_))
    controller.initBuffers(int(buffer_number_))
    controller.initEvent()


eel.start('templates/homepage.html', size=(1700, 1100), jinja_templates='templates')
