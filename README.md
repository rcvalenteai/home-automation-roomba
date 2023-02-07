Roomba Automation Project
=========================

This project is designed to automate the scheduling and execution of cleaning jobs for a Roomba vacuum cleaner, with the goal of minimizing the amount of time the Roomba runs while the house is occupied and maximizing the time it runs when the house is empty.

1. ChatGPT was used to generate 95% of the code for this project synthetic dataset to train a reinforcement learning model to improve cleaning job runtime optimization.
1. Improving functionality of project with a synthetic dataset using reinforcement learning, relying on ChatGPT for majority of code generation

Functionality
-------------

The project uses a combination of WiFi connection data and job execution history to determine the best times to run the Roomba. A Lambda function is triggered every time a device connects or disconnects from the WiFi network, and it checks the current connection status of all devices to determine if the house is empty. If the house is empty, and it has been at least 2 days since the last Roomba job, the function will trigger an IFTTT webhook to start the Roomba. If the house is not empty, the function will check the job execution history to see if it has been at least 7 days since the last Roomba job. If this condition is met, the function will again trigger the IFTTT webhook to start the Roomba.

The project also includes a separate Lambda function that is triggered every 15 minutes to check if the conditions for running the Roomba are met, even if no device has connected or disconnected from the WiFi network.

Data Collection
---------------

The project collects data on WiFi connection status and Roomba job execution history in two separate DynamoDB tables. The PhoneWifiConnectionStateTest table stores the current connection status of all devices, while the RoombaExecutionJobsTest table stores a timestamp for each Roomba job that is executed.

Future Improvements
-------------------

In the future, the project could be expanded to include more sophisticated decision-making for Roomba scheduling, such as training an AI model to predict the likelihood of the house being empty based on WiFi connection data and job execution history. Additionally, the project could be integrated with other smart home devices to gather more data on the occupancy of the house.

How it works
------------

The Roomba Automation project uses a combination of AWS Lambda, DynamoDB, and IFTTT webhooks to determine when it's a good time to run the Roomba and then invoke the cleaning job. The process is as follows:

1.  A Lambda function, `CheckRoombaExecutionCriteria`, is triggered by updates to the WiFi connection state of certain devices (e.g. phones) in the house. These updates are stored in a DynamoDB table, `PhoneWifiConnectionState`.
    
2.  The `CheckRoombaExecutionCriteria` function checks the WiFi connection state of all devices in the house and compares it to the last Roomba execution job stored in another DynamoDB table, `RoombaExecutionJobs`. It then checks if the following conditions are met:
    
    *   All devices are disconnected
    *   It's currently between 8:00 PM and 6:00 AM PST
    *   The time since the last execution job is greater than or equal to 2 days (if all devices are disconnected) or 7 days (if at least one device is connected).
3.  If the conditions are met, the `CheckRoombaExecutionCriteria` function calls an IFTTT webhook to invoke the Roomba cleaning job. The webhook URL and event name are stored in environment variables.
    
4.  The `CheckRoombaExecutionCriteria` function then stores the current timestamp in the `RoombaExecutionJobs` table to keep track of the last execution job.
    
5.  The Lambda function returns a response with a status code of 200 and a JSON body indicating whether the cleaning job was invoked or not.
    