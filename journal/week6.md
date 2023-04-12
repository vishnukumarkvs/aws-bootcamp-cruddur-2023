# Week 6 — Deploying Containers

## What I have accomplished this week. A small summary
- Run application in ECS Cluster. 
- Create ECR repositories and upload images of frontend and backend
- Create task definitions and services for frontend and backend.
- Created target groups for frontend and backend.
- Create Loadbalancer.
- Run those services
- Add vishnukvs.zyx domain in Route53.
- Created an ACM certificate
- Added the acm records in Roure53 and pointed to Loadbalancer
- Create  2 listeneres. 
  - Listener 1: redirect 80 to 443
  - Listener 2: 3 rules. Default, hostname = **cruddur.vishnukvs.xyz** -> frontend target group, **api.cruddur.vishnukvs.xyz** -> backend target group
- Created various scripts, used aws cli to create all infra including loadbaclcer, tgs, listeners, rules etc
- Created prod dockerfiles for frontend and backend
- Not able to do XRAY, it is tough. My backend is breaking because of it so decided to try again some other time

# Work

## AWS ECR

Code snippets
```
ECR REPOS
aws ecr create-repository \
  --repository-name cruddur-python \
  --image-tag-mutability MUTABLE
 
 aws ecr create-repository \
  --repository-name backend-flask \
  --image-tag-mutability MUTABLE
 
 aws ecr create-repository \
  --repository-name frontend-react-js \
  --image-tag-mutability MUTABLE
  

ECR LOGIN
aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com"

ENVS
export ECR_PYTHON_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/cruddur-python"
```

- My private repos

![image](https://user-images.githubusercontent.com/116954249/231544485-37f27973-03d5-446d-a5cb-469bb513c0a4.png)


# AWS ECS

## Cluster
Code Snippets
```
ECS CLUSTER
aws ecs create-cluster \
--cluster-name cruddur \
--service-connect-defaults namespace=cruddur
```

![image](https://user-images.githubusercontent.com/116954249/231543878-265e82d7-1864-43c4-969f-e16e2536394c.png)

## Task Definitions

Code Snippets
```
ROLES FOR TASK DEFINITIONS
aws iam create-role --role-name CruddurTaskRole --assume-role-policy-document "file://aws/policies/service-assume-role-execution-policy.json"
aws iam put-role-policy --policy-name SSMAccessPolicy --role-name CruddurTaskRole --policy-document "file://aws/policies/ssm-access-policy.json" 
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/CloudWatchFullAccess --role-name CruddurTaskRole
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess --role-name CruddurTaskRole

REGISTER TASK DEFINITION
aws ecs register-task-definition --cli-input-json file://aws/task-definitions/backend-flask.json
```

- Final Backend Task Definitions
![final-bf-taskdefs](https://user-images.githubusercontent.com/116954249/231545312-c18aa4ae-9cfe-4534-a6e9-afb10374788a.png)
  
- Final Frontend task definitions
![final-frjs-td](https://user-images.githubusercontent.com/116954249/231545527-a524445b-f123-437b-8973-66eef73dffcb.png)

## Service Executions
Code Snippets
```
ROLES FOR SERVICE EXECUTIONS
aws iam create-role --role-name CruddurServiceExecutionRole --assume-role-policy-document "file://aws/policies/service-assume-role-execution-policy.json"
aws iam put-role-policy --policy-name CruddurServiceExecutionPolicy --role-name CruddurServiceExecutionRole --policy-document file://aws/policies/service-execution-policy.json
aws iam attach-role-policy --policy-arn POLICY_ARN --role-name CruddurServiceExecutionRole

CREATE SERVICE
aws ecs create-service --cli-input-json file://aws/json/service-backend-flask.json
aws ecs create-service --generate-cli-skeleton

LOGIN INSIDE SERVICE CONTAINER
Install session manager
- https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html#install-plugin-linux

curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb" -o "session-manager-plugin.deb"
sudo dpkg -i session-manager-plugin.deb

Inside container
aws ecs execute-command  \
--region $AWS_DEFAULT_REGION \
--cluster cruddur \
--task 75483fb0d4574d9bbc7521955852211d \
--container backend-flask \
--command "/bin/bash" \
--interactive
```

  
