import os
import boto3
import datetime
import json
from dateutil import tz, parser


def lambda_handler(event, context):
    # Get the SSID from the environment variable
    SSID = os.environ['SSID']

    # Connect to DynamoDB
    dynamodb = boto3.resource('dynamodb')
    phone_table = dynamodb.Table("PhoneWifiConnectionStateTest")
    job_table = dynamodb.Table("RoombaExecutionJobsTest")

    # Query the phone table for all devices with the given SSID
    response = phone_table.query(
        KeyConditionExpression="id = :ssid",
        ExpressionAttributeValues={
            ":ssid": SSID
        }
    )

    # Check if all devices are disconnected
    print(response)
    all_devices_disconnected = all(item["connectionStatus"] == "disconnected" for item in response["Items"])

    # Query the job table for the last execution job with the given SSID
    job_response = job_table.query(
        KeyConditionExpression="id = :ssid",
        ExpressionAttributeValues={
            ":ssid": SSID
        },
        ScanIndexForward=False,
        Limit=1
    )

    # Check if there's a previous execution job
    if job_response["Count"] == 0:
        last_execution_job = None
    else:
        last_execution_job = job_response["Items"][0]

    # Check if the function should be invoked
    should_invoke = check_invocation_conditions(all_devices_disconnected, last_execution_job)

    return {
        'statusCode': 200,
        'run_cleaning_job': should_invoke,
        'body': json.dumps('Successfully updated phone state')
    }


def check_invocation_conditions(all_devices_disconnected, last_execution_job):
    # Define the time zone for the execution window
    pacific = tz.gettz('America/Los_Angeles')

    # Get the current time in PST
    now = datetime.datetime.now(pacific)

    # Check if it's currently between 8:00 PM and 6:00 AM PST
    if now.hour < 6 or now.hour >= 20:
        print("Cleaning jobs are blocked during the hours of 8:00 PM to 6:00 AM PST")
        return False

    # Check if there's no previous execution job
    if last_execution_job is None:
        print("Condition: No previous execution job")
        return True

    # Convert the last execution job timestamp to a datetime object
    last_execution_time = parser.parse(last_execution_job["job_date"]).replace(tzinfo=pacific)

    # Calculate the time since the last execution job
    time_since_last_execution = now - last_execution_time
    print(time_since_last_execution)
    print(all_devices_disconnected)

    # Check the conditions based on whether all devices are disconnected or not
    if all_devices_disconnected:
        if time_since_last_execution.days >= 2:
            print("Condition: All devices disconnected and time since last execution >= 2 days")
            return True
    else:
        if time_since_last_execution.days >= 7:
            print("Condition: Devices not disconnected and time since last execution >= 7 days")
            return True

    print("Condition: No conditions met")
    return False
