import json
import boto3
from datetime import datetime, timedelta

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("PhoneWifiConnectionStateTest")
connection_history_table = dynamodb.Table("PhoneConnectionHistoryTest")
lambda_client = boto3.client("lambda")
stepfunctions = boto3.client('stepfunctions')


def lambda_handler(event, context):
    # Parse Connection Data from Request
    body = json.loads(event["body"])
    ssid = body["SSID"]
    device_name = body["deviceName"]
    connection_status = body["connectionStatus"].split()[0]
    date_time = datetime.utcnow().isoformat()[:23] + "Z"
    print(ssid, device_name, connection_status)

    # Update DynamoDB
    update_phone_status(ssid, device_name, connection_status)
    write_connection_history(device_name, ssid, connection_status, date_time)

    # Invoke criteria check Lambda function
    invoke_step_function_criteria_check()

    return {
        'statusCode': 200,
        'invocation_type': 'update_status',
        'body': json.dumps('Successfully updated phone state')
    }


def update_phone_status(ssid, device_name, connection_status):
    response = table.update_item(
        Key={
            "id": ssid,
            "device_name": device_name
        },
        UpdateExpression="set connectionStatus = :cs",
        ExpressionAttributeValues={
            ":cs": connection_status
        },
        ReturnValues="UPDATED_NEW"
    )
    return response


def write_connection_history(device_name, ssid, connection_status, date_time):
    response = connection_history_table.put_item(
        Item={
            'device_name': device_name,
            'ssid': ssid,
            'connection_status': connection_status,
            'datetime': date_time,
        }
    )
    return response


def invoke_criteria_check_lambda():
    # Calculate the invocation time as 1 minute from the current time
    invocation_time = datetime.now() + timedelta(minutes=1)

    # Invoke the function
    response = lambda_client.invoke(
        FunctionName='CheckRoombaExecutionCriteriaTest',
        InvocationType='Event'
    )
    return response


def invoke_step_function_criteria_check():
    # Get the ARN of the Step Function to execute
    step_function_arn = "config" #"arn:aws:states:us-east-1:362049109890:stateMachine:RoombaCleaningJobSchedulerTest"
    # Get the input data for the Step Function execution
    input_data = {"invocation_type": "update_status"}
    # Start the execution of the Step Function
    response = stepfunctions.start_execution(
        stateMachineArn=step_function_arn,
        input=json.dumps(input_data)
    )
