import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3'
import * as s3n from 'aws-cdk-lib/aws-s3-notifications'
import * as lambda from 'aws-cdk-lib/aws-lambda'
import { Construct } from 'constructs';
import * as dotenv from 'dotenv';
// import * as sqs from 'aws-cdk-lib/aws-sqs';

dotenv.config();

export class ThumbingServerlessCdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

   const bucketName: string = process.env.THUMBING_BUCKET_NAME as string;
   const functionPath: string = process.env.THUMBING_FUNCTION_PATH as string;
   const folderInput: string = process.env.THUMBING_S3_FOLDER_INPUT as string;
   const folderOutput: string = process.env.THUMBING_S3_FOLDER_OUTPUT as string;

   const bucket = this.createBucket(bucketName)
   const lambda = this.createLambda(functionPath, bucketName, folderInput, folderOutput)

   this.createS3NotifyToLambda(folderInput,lambda,bucket)

  }

  createBucket(bucketName: string): s3.IBucket{
    const bucket = new s3.Bucket(this,"ThumbingBucket",{
      bucketName: bucketName,
      removalPolicy: cdk.RemovalPolicy.DESTROY
    });
    return bucket;
   }

   createLambda(functionPath: string, bucketName: string, folderInput: string, folderOutput: string): lambda.IFunction{
     const lambdaFunction = new lambda.Function(this, 'ThumbLambda', {
        runtime: lambda.Runtime.NODEJS_18_X,
        handler: 'index.handler',
        code: lambda.Code.fromAsset(functionPath),
        environment: {
          DEST_BUCKET_NAME: bucketName,
          FOLDER_INPUT: folderInput,
          FOLDER_OUTPUT: folderOutput,
          PROCESS_WIDTH: '512',
          PROCESS_HEIGHT: '512'
        }
     })
     return lambdaFunction;
   }

  // description below
   createS3NotifyToLambda(prefix: string, lambda: lambda.IFunction, bucket: s3.IBucket): void{
    const destination = new s3n.LambdaDestination(lambda);
    bucket.addEventNotification(
      s3.EventType.OBJECT_CREATED_PUT,
      destination,
      {prefix:prefix}
     )
   }
}

// createS3NotifyToLambda
// This is a TypeScript/JavaScript function that creates an S3 event notification that triggers an AWS Lambda function when an object is created and PUT into an S3 bucket. The function takes three parameters: a string prefix, an AWS Lambda function lambda, and an S3 bucket bucket.
// The function creates a new LambdaDestination object, which represents the destination of the S3 event notification. This destination is set to the lambda function passed as a parameter.
// Then, the bucket is configured to send an event notification when an object is created and PUT into the bucket. The event type is specified as s3.EventType.OBJECT_CREATED_PUT. The destination is set as the destination of the event notification. 
// The prefix parameter is used to specify a folder path within the bucket, where the original images are stored. 
   
