import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { DynamoDB } = require("aws-sdk");
const https = require('https');

const dynamoDB = new DynamoDB.DocumentClient();
const tableName = 'RoombaExecutionJobsTest';
const ssid = process.env.SSID;
const iftttKey = process.env.IFTTT_KEY;
const eventName = process.env.IFTTT_EVENT;

export const handler = async (event) => {
    const now = new Date().toISOString();

    const item = {
        id: ssid,
        job_date: now
    };

    const iftttUrl = `https://maker.ifttt.com/trigger/${eventName}/with/key/${iftttKey}`;
    let responseCode = 0;
    let attempts = 0;
    while (responseCode !== 200 && attempts < 3) {
        https.get(iftttUrl, (res) => {
            responseCode = res.statusCode;
            if (responseCode === 200) {
                console.log(`Successfully started Roomba cleaning job for SSID: ${ssid}`);
            } else {
                console.log(`Webhook call failed with response code: ${responseCode}`);
            }
        });
        await new Promise(resolve => setTimeout(resolve, 1000));
        attempts++;
    }
    console.log(`Attempts: ${attempts}`);
    if (responseCode !== 200) {
        console.log(`Webhook call failed after ${attempts} attempts`);
    }
    if(responseCode === 200){
        await dynamoDB.put({
            TableName: tableName,
            Item: item
        }).promise();
    }
    const response = {
        statusCode: 200,
        body: JSON.stringify('Respnse Code From API: ' + responseCode),
    };
    return response;
};
