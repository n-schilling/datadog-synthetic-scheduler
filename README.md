Datadog Synthetic Scheduler
----

This solution helps you to schedule Datadog Synthetics (API and Browser tests) for a specific time-slot. This can save you money if you don't need the results 24/7.

:exclamation: This solution will create several resources which will be billed by AWS.

## Base architecture

An AWS EventBridge rule starts an AWS Lambda function at the time you specified. This function retrieves the credentials from the AWS Secrets Manager. After having the credentials, it calls the Datadog Rest API to start the configured Synthetic. A second AWS EventBridge rule starts a second AWS Lambda function to do nearly the same. But this time, the Synthetic is paused.

### Used AWS Services

* AWS Secrets Manager
* AWS EventBridge
* AWS Lambda
* AWS X-Ray
* AWS Cloudwatch

## Implementation guide

Please follow all the steps below to deploy the solution. Please pay attention that the solution only can be deployed in a region where all mentioned services above are available.

## Requirements

* Python 3 (tested with version 3.8.0)
* Node.js (tested with version 12.12.0)
* Serverless (tested with version 1.57.0)

## Deploy the solution

1. Clone this repository
2. Edit the parameters in the serverless.yml
  * syntheticStart: Cron-expression when to start the Synthetic ([see documentation](https://docs.aws.amazon.com/eventbridge/latest/userguide/scheduled-events.html))   
  * syntheticStop: Cron-expression when to stop the Synthetic ([see documentation](https://docs.aws.amazon.com/eventbridge/latest/userguide/scheduled-events.html))  
  * syntheticPublicId: Public ID of the synthetic. You can find the public ID if you switch to the Synthetic in your browser. The url should look like this: `https://app.datadoghq.eu/synthetics/details/123-abc-456a` The Id can be found at the end of the url: `123-abc-456` is the public id in this case.
  * datadogApiEndpoint: Suitable endpoints can be found [here](https://docs.datadoghq.com/api/?lang=bash#api-reference). (EU site: https://api.datadoghq.com/api/ // US site: https://api.datadoghq.com/api/)
3. Deploy the solution to AWS with ```sls deploy --region eu-central-1 --stage dev```.
4. Switch to the AWS Console and the Service `Secrets Manager`. Edit the value for the secret `DatadogSyntheticSchedulerSecret` and enter your Datadog API and APP key.

:exclamation: If you want to use this solution for multiple Synthetic tests in one AWS account, you need to modify the service name in the `serverless.yml` (first line).

### Undeploy the solution

Just follow the next steps to undeploy the solution:

1. Open the AWS Console and clean up the s3 bucket
2. run ```sls remove``` to remove the solution

## ToDo list

### Code

There are surely ways to improve. Just send a pull request. :wink:
