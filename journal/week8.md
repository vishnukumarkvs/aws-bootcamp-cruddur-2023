# Week 8 — Serverless Image Processing

Summary
- implemented cdk stack
- implemented cloudfront for s3 origin
- implemented user profile
- got resigned URL , able to upload image in thunderclient
- not able to complete upload avatar, stuck with cors issue. have done everything.

Referrences
- thecdkbook.com
- cdkday.com
- constructs.dev
- cdkpatterns.com

Notes

```
typescript cdk can run python lambda fns

cdk is built on typescript

npm install aws-cdk -g
cdk init app --language typescript

https://github.com/omenking/aws-bootcamp-cruddur-2023/tree/week-8-serverless-cdk/aws/lambdas/process-images

CDK commands:

cdk init: Initializes a new CDK app in the current directory.
cdk synth: Synthesizes the CDK app into an AWS CloudFormation template.
cdk deploy: Deploys the CDK app to an AWS environment.
cdk diff: Shows the difference between the deployed stack and the local code changes.
cdk destroy: Destroys the deployed stack and deletes all AWS resources created by the app.
cdk list: Lists all the stacks in the AWS environment.
cdk bootstrap: Creates an S3 bucket to store CDK 

create cloudfront distribution
- its for assets
- origin domain - s3 bucket - assets.cruddur.vishnukvs.xyz.s3.us-east-1.amazonaws.com
- access - origin access control settings(recommended) - create control setting with s3 origin type
- redirect http to https
- dont restrict viewers acces
- allowed http methods - GET, HEAD
- cache policy: caching optimised, cors-custom origin, headers - simple cors
- alternate domain: assets-cruddur.vishnukvs.xyz
- add ssl certificate

no need to enable public access for cloudfront s3 origin, just copy policy and add to bucket


To update sql table
./bin/generate/migration add_bio_column

  SELECT
    coalesce(
        (SELECT last_successful_run
        FROM public.schema_information
        LIMIT 1),
        '0') as last_successful_run
  """

only on start
cruddur=# ALTER TABLE public.schema_information ADD COLUMN id integer;
drop table schema_information;

@aws-sdk/client-s3

Ruby
bundle init -> created Gemfile -> Its like package.json
bundle install
bundle exec ruby function.rb


thunderclient - postman in vscode

presignedurl uses your aws credentials

lambda presigned
edit runtime = function.handler
filename to function.rb

aws-jwt-verify npm package to verify jwt token

```

Work
![assets, uploads](https://user-images.githubusercontent.com/116954249/234197929-58e98e92-3507-4efa-a405-9fb73dcfa177.png)
![bucket_cdk](https://user-images.githubusercontent.com/116954249/234197935-7be4de31-b43a-4b21-aabe-b479924f8f48.png)
![crudduravatarlamda](https://user-images.githubusercontent.com/116954249/234197946-c5731add-34e6-4cb6-b418-82e130a2cd4e.png)
![migrate, rollback successfull](https://user-images.githubusercontent.com/116954249/234197947-bd70ff27-6c96-4066-b218-a02370b647aa.png)
![presigned upload done](https://user-images.githubusercontent.com/116954249/234197956-0e90ee9c-1dd4-407b-94a4-4db2adf50c57.png)
![s3 trigger for lambda](https://user-images.githubusercontent.com/116954249/234197959-da9b9891-ad4b-4afa-8027-095d39205c79.png)
![schema table](https://user-images.githubusercontent.com/116954249/234197960-6b50119c-dad2-413f-9781-c29976c9d051.png)
![tbucket kvsvk](https://user-images.githubusercontent.com/116954249/234197962-6591b7b7-f99d-4bc3-806d-89780d4cf298.png)
![user-profile done](https://user-images.githubusercontent.com/116954249/234197965-e6d1c252-2c46-4850-a9a2-5cbd85eff4ac.png)

