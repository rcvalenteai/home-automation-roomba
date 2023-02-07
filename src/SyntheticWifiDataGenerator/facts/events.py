from src.SyntheticWifiDataGenerator.model.DaysOfWeek import DaysOfWeek
from src.SyntheticWifiDataGenerator.model.Event import Event
from src.SyntheticWifiDataGenerator.model.Schedule import Schedule
from src.SyntheticWifiDataGenerator.model.Person import Person

from datetime import datetime


# create even chance across day dict
from src.SyntheticWifiDataGenerator.visualizer.WifiConnectionVisualizer import visualize_wifi_events, plot_wifi_events, \
    visualize_wifi_event_2, plotly_visualization, visualization_four

spread_start_time = dict()
for i in range(5, 23):
    spread_start_time[i] = (1.0 / len(range(5, 23)))

spread_duration = dict()
for i in range(5, 120, 5):
    spread_duration[i] = (1.0 / len(range(5, 120, 5)))

rich = Person(Schedule(), "Rich")

# Office event
office_event = Event(name="Office", start_times={9: 1.0}, durations={8: 1.0},
                     days_of_week={DaysOfWeek.MONDAY.value: 0.2, DaysOfWeek.TUESDAY.value: 0.2, DaysOfWeek.WEDNESDAY.value: 0.2,
                                   DaysOfWeek.THURSDAY.value: 0.2, DaysOfWeek.FRIDAY.value: 0.2}, chance_of_occurring=0.95)
rich.schedule.add_event(office_event)

# Weekday Workout event
weekday_workouts_event = Event(name="Workout", start_times={7: 0.35, 12: 0.15, 17: 0.25, 18: 0.25}, durations={45: 1.0},
                               days_of_week={DaysOfWeek.MONDAY.value: 0.6, DaysOfWeek.TUESDAY.value: 0.6, DaysOfWeek.WEDNESDAY.value: 0.6,
                                             DaysOfWeek.THURSDAY.value: 0.6, DaysOfWeek.FRIDAY.value: 0.6},
                               chance_of_occurring=0.95)
rich.schedule.add_event(weekday_workouts_event)

# Weekend Workout event
weekend_workouts_event = Event(name="Workout", start_times={9: 0.3, 10: 0.7}, durations={60: 1.0},
                               days_of_week={DaysOfWeek.SATURDAY.value: 0.9, DaysOfWeek.SUNDAY.value: 0.1},
                               chance_of_occurring=0.95)
rich.schedule.add_event(weekend_workouts_event)

swimming_event = Event(name="Swimming", start_times={20: 1.0}, durations={60: 1.0},
                       days_of_week={DaysOfWeek.THURSDAY.value: 1.0, DaysOfWeek.FRIDAY.value: 1.0},
                       chance_of_occurring=0.9)
rich.schedule.add_event(swimming_event)

# Sauna
sauna_event = Event(name="Sauna", start_times={19: 1.0}, durations={90: 1.0},
                    days_of_week={DaysOfWeek.WEDNESDAY.value: 1.0},
                    chance_of_occurring=0.95)
rich.schedule.add_event(sauna_event)

# Week Vacation
vacation_event = Event(name="Workout", start_times={0: 1.0}, durations={24: 1.0},
                       days_of_week={DaysOfWeek.MONDAY.value: 1.0, DaysOfWeek.TUESDAY.value: 1.0, DaysOfWeek.WEDNESDAY.value: 1.0,
                                     DaysOfWeek.THURSDAY.value: 1.0, DaysOfWeek.FRIDAY.value: 1.0, DaysOfWeek.SATURDAY.value: 1.0,
                                     DaysOfWeek.SUNDAY.value: 1.0},
                       chance_of_occurring=0.06)
rich.schedule.add_event(vacation_event)

# Random Event Noise
random_event = Event(name="Workout", start_times=spread_start_time, durations=spread_duration,
                     days_of_week={DaysOfWeek.MONDAY.value: 0.05, DaysOfWeek.TUESDAY.value: 0.05, DaysOfWeek.WEDNESDAY.value: 0.05,
                                   DaysOfWeek.THURSDAY.value: 0.05, DaysOfWeek.FRIDAY.value: 0.05, DaysOfWeek.SATURDAY.value: 0.05,
                                   DaysOfWeek.SUNDAY.value: 0.05},
                     chance_of_occurring=1.0)
rich.schedule.add_event(random_event)

events = rich.generate_wifi_events_for_period(datetime.now(), 7)
all_events = rich.wifi_events_to_connect_disconnect(events)
print(events)
print(all_events)
visualization_four(all_events)