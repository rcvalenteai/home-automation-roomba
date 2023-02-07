from enum import Enum
from datetime import datetime


class WifiConnectionEvent:
    """
    A class representing a wifi connection event for a specific individual.
    """
    class Status(Enum):
        """
        Enum representing the status of the wifi connection event.
        """
        CONNECTED = "CONNECTED"
        DISCONNECTED = "DISCONNECTED"

    def __init__(self, entity_id: str, status: Status, start_time: datetime, end_time: datetime):
        """
        Initializes a WifiConnectionEvent instance.

        :param entity_id: The id of the individual associated with the event.
        :type entity_id: str
        :param status: The status of the wifi connection event (connected or disconnected).
        :type status: WifiConnectionEvent.Status
        :param start_time: The start time of the wifi connection event.
        :type start_time: datetime
        :param end_time: The end time of the wifi connection event.
        :type end_time: datetime
        """
        self.entity_id = entity_id
        self.status = status
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return f"WifiConnectionEvent(entity_id='{self.entity_id}', status='{self.status.value}', start_time='{self.start_time}', end_time='{self.end_time}')"
