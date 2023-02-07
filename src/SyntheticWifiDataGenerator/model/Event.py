import random
import datetime
from datetime import timedelta
from typing import List

from src.SyntheticWifiDataGenerator.model.WifiConnectionEvent import WifiConnectionEvent


class Event:
    def __init__(self, name: str, start_times: dict, durations: dict, days_of_week: dict, chance_of_occurring: float):
        """
        Initializes an Event object with the given information.

        Example Event that denotes an individual that goes into the office on average 1 day a week most weeks of the year.
        Event(name="Office", start_times={9: 1.0}, durations={8: 1.0},
                     days_of_week={DaysOfWeek.Monday: 0.2, DaysOfWeek.Tuesday: 0.2, DaysOfWeek.Wednesday: 0.2,
                        DaysOfWeek.Thursday: 0.2, DaysOfWeek.Friday: 0.2}, chance_of_occurring=0.95)
        :param name: name of the event.
        :param start_times: a dictionary of start times, with keys as time in 24 hour format and values as probability
            of the event starting at that time.
        :param durations: a dictionary of durations, with keys as duration in minutes and values as probability of the
            event lasting that long.
        :param days_of_week: a dictionary of days of the week that the event can occur on with probabilities,
            represented as elements of the DaysOfWeek Enum
        :param chance_of_occurring: a float representing the overall chance of the event occurring in a given week.
        """
        self.name = name
        self.start_times = start_times
        self.durations = durations
        self.days_of_week = days_of_week
        self.chance_of_occurring = chance_of_occurring

    def generate_wifi_events(self, date: datetime.date, entity_id: str, start_time_variance=10,
                             duration_variance=5) -> List[WifiConnectionEvent]:
        """
        Generates wifi events based on the input event, date, and entity_id.
        The function will only append disconnection events that start at the event start time and last for the specified duration.
        It will also add random variance to the start_time and duration.

        :param date: Date for which the wifi events need to be generated
        :type date: datetime.date
        :param entity_id: ID of the entity for which the wifi events are being generated
        :type entity_id: str
        :param start_time_variance: Variance to be added to the start_time in minutes (default: 10)
        :type start_time_variance: int
        :param duration_variance: Variance to be added to the duration in minutes (default: 5)
        :type duration_variance: int
        :return: List of wifi events
        :rtype: List[WifiConnectionEvent]
        """
        wifi_events = []
        # check if the event occurs on the input date
        print(random.random())
        print(self.days_of_week.get(date.weekday()))
        print(self.days_of_week.keys())
        print(date.weekday())
        if random.random() < self.chance_of_occurring and self.days_of_week.get(date.weekday()):
            start_time = datetime.datetime.combine(date, datetime.time(hour=random.choices(list(self.start_times.keys()), list(self.start_times.values()))[0]))
            duration = timedelta(minutes=random.choices(list(self.durations.keys()), list(self.durations.values()))[0])
            # Add random variance to start_time and duration
            start_time = start_time + timedelta(minutes=random.randint(-start_time_variance, start_time_variance))
            duration = duration + timedelta(minutes=random.randint(-duration_variance, duration_variance))

            print("START_TIME", start_time)
            end_datetime = start_time + duration
            wifi_events.append(
                WifiConnectionEvent(entity_id, WifiConnectionEvent.Status.DISCONNECTED, start_time,
                                    end_datetime))
        return wifi_events

