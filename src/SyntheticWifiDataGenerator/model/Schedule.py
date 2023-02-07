from datetime import datetime
from typing import List

from src.SyntheticWifiDataGenerator.model.Event import Event
from src.SyntheticWifiDataGenerator.model.WifiConnectionEvent import WifiConnectionEvent


class Schedule:
    """
    A class representing a schedule, which contains a list of events.

    Attributes:
        events (List[Event]): A list of events in the schedule.
    """

    def __init__(self):
        """
        Initializes a schedule with an empty list of events.
        """
        self.events = []

    def add_event(self, event: Event):
        """
        Adds an event to the schedule.

        Args:
            event (Event): The event to be added to the schedule.
        """
        self.events.append(event)

    def remove_event(self, event: Event):
        """
        Removes an event from the schedule.

        Args:
            event (Event): The event to be removed from the schedule.
        """
        self.events.remove(event)

    def generate_wifi_events(self, date: datetime.date, entity_id: str, start_time_variance=10, duration_variance=5) -> List[WifiConnectionEvent]:
        """
        Generates a list of wifi events for a given date and entity_id by iterating through the events in the Schedule class
        and calling the generate_wifi_events method on each event.

        :param date: datetime.date object representing the date for which wifi events will be generated
        :param entity_id: string representing the id of the entity for which wifi events will be generated
        :param start_time_variance: int representing the variance in minutes that will be added to the start_time of each wifi event
        :param duration_variance: int representing the variance in minutes that will be added to the duration of each wifi event
        :return: list of WifiConnectionEvent objects representing the wifi events generated for the given date and entity_id
        """
        wifi_events = []
        for event in self.events:
            wifi_events += Event.generate_wifi_events(event, date, entity_id, start_time_variance, duration_variance)
        return wifi_events
