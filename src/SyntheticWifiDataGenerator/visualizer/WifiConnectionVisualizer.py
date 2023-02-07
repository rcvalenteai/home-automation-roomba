from typing import List

import plotly.express as px
import pandas as pd
from datetime import timedelta

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, AutoDateLocator, DateFormatter
from datetime import timedelta
from typing import List

import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from datetime import timedelta

from src.SyntheticWifiDataGenerator.model.WifiConnectionEvent import WifiConnectionEvent


def visualize_wifi_events(events):
    fig, ax = plt.subplots(figsize=(15,5))

    connected_events = []
    disconnected_events = []

    for event in events:
        if event.status == WifiConnectionEvent.Status.CONNECTED:
            connected_events.append([event.start_time, event.end_time])
        else:
            disconnected_events.append([event.start_time, event.end_time])

    start_time = min(event.start_time for event in events)
    end_time = max(event.end_time for event in events)

    current_time = start_time
    while current_time <= end_time:
        current_status = WifiConnectionEvent.Status.CONNECTED
        for event in disconnected_events:
            if event[0] <= current_time <= event[1]:
                current_status = WifiConnectionEvent.Status.DISCONNECTED
                break
        if current_status == WifiConnectionEvent.Status.CONNECTED:
            ax.axvspan(current_time, current_time + timedelta(hours=1), color='green', alpha=0.5)
        else:
            ax.axvspan(current_time, current_time + timedelta(hours=1), color='red', alpha=0.5)
        current_time += timedelta(hours=1)

    plt.xticks(rotation=30)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    ax.set_xlim([start_time, end_time])
    ax.set_ylim([0, 1])
    ax.set_yticks([])
    plt.show()


def visualize_wifi_event_2(events):
    fig, ax = plt.subplots(figsize=(15,5))

    connected_events = []
    disconnected_events = []

    for event in events:
        if event.status == WifiConnectionEvent.Status.CONNECTED:
            connected_events.append([event.start_time, event.end_time])
        else:
            disconnected_events.append([event.start_time, event.end_time])

    start_time = min(event.start_time for event in events)
    end_time = max(event.end_time for event in events)

    current_time = start_time
    while current_time <= end_time:
        current_status = WifiConnectionEvent.Status.CONNECTED
        for event in disconnected_events:
            if current_time >= event[0] and current_time <= event[1]:
                current_status = WifiConnectionEvent.Status.DISCONNECTED
                break
        if current_status == WifiConnectionEvent.Status.CONNECTED:
            ax.axvspan(current_time, current_time + timedelta(minutes=1), color='green', alpha=0.5)
        else:
            ax.axvspan(current_time, current_time + timedelta(minutes=1), color='red', alpha=0.5)
        current_time += timedelta(minutes=1)

    plt.xticks(rotation=30)
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%a'))
    ax.grid(True, which='minor')
    ax.set_xlim([start_time, end_time])
    ax.set_ylim([0, 7])
    ax.set_yticks(range(1, 8))
    ax.set_yticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    plt.show()


def plot_wifi_events(events_data):
    # Define the default state
    default_state = "CONNECTED"
    default_color = "green"

    # Create a list to store the dates and states
    dates = []
    states = []
    colors = []

    # Loop through the events and add the state for each minute to the list
    for event in events_data:
        start_time = event.start_time
        end_time = event.end_time
        event_status = event.status

        # If the status is the default state, add it to the states list as the default color
        if event_status == default_state:
            while start_time < end_time:
                dates.append(start_time)
                states.append(event_status)
                colors.append(default_color)
                start_time += timedelta(minutes=1)
        # If the status is not the default state, add it to the states list as the status color
        else:
            while start_time < end_time:
                dates.append(start_time)
                states.append(event_status)
                colors.append("red")
                start_time += timedelta(minutes=1)

    # Create the figure and axis objects
    fig, ax = plt.subplots()

    # Plot the events as a vertical line on the x-axis for each minute
    ax.vlines(dates, 0, 1, color=colors)

    # Format the x-axis to show the minutes
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=60))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=5))

    # Remove the top and right spines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Set the y-axis limit to only show the status labels
    ax.set_ylim(0, 1)
    ax.set_yticks([0, 1])
    ax.set_yticklabels([default_state, "DISCONNECTED"], fontsize=10)

    # Remove the y-axis labels
    ax.set_yticks([], minor=True)

    # Show the plot
    plt.show()


def plotly_visualization(events):
    wifi_events = [
        {'timestamp': '2022-01-01T00:00:00', 'status': 'CONNECTED'},
        {'timestamp': '2022-01-02T00:00:00', 'status': 'DISCONNECTED'},
        {'timestamp': '2022-01-03T00:00:00', 'status': 'CONNECTED'},
        {'timestamp': '2022-01-04T00:00:00', 'status': 'DISCONNECTED'},
        {'timestamp': '2022-01-05T00:00:00', 'status': 'CONNECTED'},
    ]

    df = pd.DataFrame(wifi_events)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    fig = px.line(df, x='timestamp', y='status', color='status',
                  line_group='status', hover_name='status',
                  height=400)

    fig.show()


def visualization_four(events: List[WifiConnectionEvent]):
    # Group events by entity_id
    events_by_entity = {}
    for event in events:
        if event.entity_id not in events_by_entity:
            events_by_entity[event.entity_id] = []
    events_by_entity[event.entity_id].append(event)
    # Plot events for each entity_id
    for entity_id, entity_events in events_by_entity.items():
        if not entity_events:
            continue
        start_times = [event.start_time for event in entity_events]
        end_times = [event.end_time for event in entity_events]
        statuses = [event.status.value for event in entity_events]

        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 5))
        for i in range(len(entity_events)):
            if statuses[i] == 'CONNECTED':
                color = 'green'
            else:
                color = 'red'
            ax.broken_barh([(start_times[i], (end_times[i] - start_times[i]).total_seconds() / 3600)], (i, 1),
                           color=color)
        ax.set_yticks([0.5, 1.5, 2.5])
        ax.set_yticklabels([entity_id])
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
        ax.set_xlim(min(start_times), max(end_times) + timedelta(hours=1))
        plt.tight_layout()
        plt.show()