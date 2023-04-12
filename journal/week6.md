# Week 6 — Deploying Containers

## What I have accomplished this week. A summary
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

ECS service connect
- service discovery + service mesh
- uses namespace instead of vpc

ECR
- dont pull images from dockerhub in production
- push all base images to your private registries like ecr

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
export ECR_BACKEND_FLASK_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/backend-flask"
```

### Docker work

```
PYTHON DOCKER PUSH
docker pull python:3.10-slim-buster
docker tag python:3.10-slim-buster $ECR_PYTHON_URL:3.10-slim-buster
docker push $ECR_PYTHON_URL:3.10-slim-buster

BACKEND DOCKER PUSH
docker build -t backend-flask .
docker tag backend-flask:latest $ECR_BACKEND_FLASK_URL:latest
docker push $ECR_BACKEND_FLASK_URL:latest

FRONTEND DOCKER PUSH
docker build \
--build-arg REACT_APP_FRONTEND_URL="https://cruddur.vishnukvs.xyz" \
--build-arg REACT_APP_BACKEND_URL="https://api.cruddur.vishnukvs.xyz" \
--build-arg REACT_APP_AWS_PROJECT_REGION="$AWS_DEFAULT_REGION" \
--build-arg REACT_APP_AWS_COGNITO_REGION="$AWS_DEFAULT_REGION" \
--build-arg REACT_APP_AWS_USER_POOLS_ID="*****" \
--build-arg REACT_APP_COGNITO_CLIENT_ID="*****" \
--build-arg REACT_APP_GOOGLE_CLIENT_ID="******" \
-t frontend-react-js \
-f Dockerfile.prod \
.
docker tag frontend-react-js:latest $ECR_FRONTEND_REACT_URL:latest
docker push $ECR_FRONTEND_REACT_URL:latest
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

Services running
![image](https://user-images.githubusercontent.com/116954249/231551514-13e17a4a-e852-41c5-8e8c-abe2da559d6b.png)

Tasks running
![image](https://user-images.githubusercontent.com/116954249/231551804-18629d1a-c6ef-4c3a-bf7d-cccb9e2dc921.png)

# Route53
Steps done
- create hosted zone
- update nameservers in godaddy(domain registrar)
- create acm with vishnukvs.xyz , *.vishnukvs.xyz

Certificates
![image](https://user-images.githubusercontent.com/116954249/231552866-7fbeb8d6-d3d0-4ace-9844-cfea1695bd24.png)

```
ACM CERTIFICATE FOR DOMAIN
export ACM_CERTIFICATE=$(aws acm list-certificates --query "CertificateSummaryList[?DomainName=='vishnukvs.xyz'].CertificateArn" --output text)
```

Records
![two A records](https://user-images.githubusercontent.com/116954249/231552692-23cf804b-f46a-4d5c-ba52-aabe3d629bbf.png)

## SECURITY GROUPS AND TARGET GROUPS

Code Snippets
```
SECURITY GROUPS

export DEFAULT_VPC_ID=$(aws ec2 describe-vpcs \
--filters "Name=isDefault, Values=true" \
--query "Vpcs[0].VpcId" \
--output text)
echo $DEFAULT_VPC_ID

export CRUD_ALB_SG=$(aws ec2 create-security-group \
  --group-name "crud-alb-sg" \
  --description "Security group for Cruddur ALB" \
  --vpc-id $DEFAULT_VPC_ID \
  --query "GroupId" --output text)
echo $CRUD_ALB_SG

aws ec2 authorize-security-group-ingress \
  --group-id $CRUD_ALB_SG \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
  --group-id $CRUD_ALB_SG \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0


TARGET GROUPS
aws elbv2 create-target-group \
    --name cruddur-backend-flask-tg \
    --protocol HTTP \
    --port 4567 \
    --target-type ip \
    --vpc-id $DEFAULT_VPC_ID \
    --health-check-path /api/health-check

aws elbv2 create-target-group \
    --name cruddur-frontend-reactjs-tg \
    --protocol HTTP \
    --port 3000 \
    --target-type ip \
    --vpc-id $DEFAULT_VPC_ID
    
TG ARN
export FRONTEND_TARGET_GROUP_ARN=$(aws elbv2 describe-target-groups --names cruddur-frontend-reactjs-tg --query "TargetGroups[*].TargetGroupArn" --output text)
export BACKEND_TARGET_GROUP_ARN=$(aws elbv2 describe-target-groups --names cruddur-backend-flask-tg --query "TargetGroups[*].TargetGroupArn" --output text)
```


## LOAD BALANCER

Code Snippets
```
CREATE ALB
aws elbv2 create-load-balancer \
--name cruddur-alb \
--subnets subnet-03068d4e subnet-1045814f subnet-81fa01e7 subnet-c263decc subnet-b871b799 subnet-7db0bf43 \
--security-groups sg-0c250257fafae3ef7 \
--type application

LOADBALANCER ARN
export LB_ARN=$(aws elbv2 describe-load-balancers --names cruddur-alb --query "LoadBalancers[*].LoadBalancerArn" --output text)
echo $LB_ARN

LISTENER 1
aws elbv2 create-listener --load-balancer-arn $LB_ARN \
--protocol HTTP \
--port 80 \
--default-actions Type=redirect,RedirectConfig="{Protocol=HTTPS,Port=443,StatusCode=HTTP_301}"

LISTENER 2
aws elbv2 create-listener --load-balancer-arn $LB_ARN --protocol HTTPS --port 443 --certificates CertificateArn=$ACM_CERTIFICATE --default-actions Type=fixed-response,FixedResponseConfig="{StatusCode=404,ContentType=text/plain,MessageBody=\"Visit cruddur.vishnukvs.xyz\"}"

RULES FOR LISTENER 2
aws elbv2 create-rule --listener-arn $LISTENER_ARN \
--priority 1 \
--conditions Field=host-header,Values=cruddur.vishnukvs.xyz --actions Type=forward,TargetGroupArn=$FRONTEND_TARGET_GROUP_ARN

aws elbv2 create-rule --listener-arn $LISTENER_ARN \
--priority 2 \
--conditions Field=host-header,Values=api.cruddur.vishnukvs.xyz --actions Type=forward,TargetGroupArn=$BACKEND_TARGET_GROUP_ARN
```

# Final application
### Frontend
![certificate not yet valid, but fr working](https://user-images.githubusercontent.com/116954249/231554771-6503eae4-3f52-44f2-92bc-9accfff1d11c.png)

### Backend
![not valid backend](https://user-images.githubusercontent.com/116954249/231554833-f336af2d-208c-4f76-8aae-30e04df5fcb8.png)

### Messages
![messages ddb working](https://user-images.githubusercontent.com/116954249/231554958-43a67773-9862-466e-bcc0-da69c11328ee.png)


# Security Best Practices by Ashish

### Container security best practices
- 2022 stats: 75% containers run with high or critical vulnerability
- 50% containers have no limits defined
- 76% of containers run as root

### AWS Fargate Security Challenges
- No visibility, control on infrastructure
- Threat detection is hard, especially due to ephermal resources
- No file, network monitoring
- Cannot run traditional security agents in fargate
- user can run unverified container images
- containers can run by root privilege

### ECS Security best practices
- Cloud control plane(AWS Console)
- Chossing right public or private ECR for images
- ECR Scan - Scan on Push - Basic or Enhanced(Inspector + Snyk)
- VPC Endpoints or Security Groups with known sources
- Compliance reqs
- Organization SCP - to manage ECS Task deletion, Creation, Region lock
- CloudTrail
- AWS Config Rules - as no GuardDuty available
