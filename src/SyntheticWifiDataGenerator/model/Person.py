from typing import Tuple, List
from datetime import datetime, timedelta

from src.SyntheticWifiDataGenerator.model.Schedule import Schedule
from src.SyntheticWifiDataGenerator.model.WifiConnectionEvent import WifiConnectionEvent


class Person:
    """
    A class representing a person, with a schedule and an id
    """

    def __init__(self, schedule: Schedule, id: str):
        """
        Initialize a new person object

        :param schedule: schedule of the person
        :type schedule: Schedule
        :param id: the id of the person
        :type id: str
        """
        self.schedule = schedule
        self.id = id

    def generate_wifi_events_for_period(self, start_date: datetime.date, num_days: int):
        """
        Generate wifi events for a given period

        :param start_date: the start date of the period
        :type start_date: datetime.date
        :param num_days: the number of days in the period
        :type num_days: int
        :return: list of wifi events
        :rtype: List[WifiConnectionEvent]
        """
        wifi_events = []
        for i in range(num_days):
            date = start_date + timedelta(days=i)
            wifi_events += self.schedule.generate_wifi_events(date, self.id)
        return wifi_events

    def wifi_events_to_connect_disconnect(self, wifi_events: List[WifiConnectionEvent]) -> List[WifiConnectionEvent]:
        """
        Transforms a list of wifi events into a list of connect and disconnect events.

        Assumes the base state is connected, and for each disconnect event, a following connect event is added.
        If there are multiple overlapping disconnect events at the same time, the device remains disconnected until
        all events have concluded, at which point a connect event is added.

        :param wifi_events: A list of wifi events
        :return: A list of wifi connect and disconnect events
        """
        if wifi_events is []:
            return []
        # get entity_id for events
        entity_id = wifi_events[0].entity_id
        # sort events by start time
        wifi_events.sort(key=lambda x: x.start_time)
        connect_disconnect_events = []
        # the current state of the wifi, connected or disconnected
        wifi_status = WifiConnectionEvent.Status.CONNECTED
        # keep track of the end time of the last disconnect event
        last_disconnect_end_time = None
        for event in wifi_events:
            if event.status == WifiConnectionEvent.Status.DISCONNECTED:
                if wifi_status == WifiConnectionEvent.Status.CONNECTED:
                    # add a disconnect event
                    connect_disconnect_events.append(event)
                    wifi_status = WifiConnectionEvent.Status.DISCONNECTED
                    last_disconnect_end_time = event.end_time
                elif event.start_time > last_disconnect_end_time:
                    # add a connect event
                    connect_disconnect_events.append(WifiConnectionEvent(event.entity_id, WifiConnectionEvent.Status.CONNECTED, last_disconnect_end_time, event.start_time))
                    # add the disconnect event
                    connect_disconnect_events.append(event)
                    last_disconnect_end_time = event.end_time
                else:
                    # update the end time of the last disconnect event
                    last_disconnect_end_time = max(last_disconnect_end_time, event.end_time)
            else:
                if wifi_status == WifiConnectionEvent.Status.DISCONNECTED:
                    # add a connect event
                    connect_disconnect_events.append(WifiConnectionEvent(event.entity_id, WifiConnectionEvent.Status.CONNECTED, last_disconnect_end_time, event.start_time))
                    wifi_status = WifiConnectionEvent.Status.CONNECTED
        if wifi_status == WifiConnectionEvent.Status.DISCONNECTED:
            # add a final connect event if the wifi is currently disconnected
            connect_disconnect_events.append(WifiConnectionEvent(entity_id, WifiConnectionEvent.Status.CONNECTED,
                                                                 last_disconnect_end_time, last_disconnect_end_time))
        return connect_disconnect_events