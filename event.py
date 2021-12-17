EventType = {
    'GenerateTask': 0,
    'TaskUnbuffer': 1,
    'TaskCompleted': 2,
    'TaskCancel': 3
}


class Event():
    def __init__(self, eventTime, eventType, deviceId) -> None:
        self.eventTime = eventTime
        self.eventType = eventType
        self.deviceId = deviceId
