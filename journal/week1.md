# Week 1 — App Containerization

# Hard Assignments

## Docker Introduction
- Docker is a software that enables us to build and ship applications quickly
- Core concepts of Docker are Docker Container and Docker Image.
- A docker image contains your application code with all its dependencies
- A docker container is instance of docker image. You can run your application by running the container .You can create, start, stop, move, or delete a container using the Docker API or CLI.
<br>


## Cruudur up and running
- Followed the week1 stream and was able to create Dockerfiles for Frontend and Backend
### Backend
- Created docker image from Dockerfile.

![image built](https://user-images.githubusercontent.com/116954249/220102496-6702795b-cc3e-4440-9258-7552ac6397d2.png)

- Started a container from Image and was able to get 200OK status from */api/activities/home* endpoint

![200ok](https://user-images.githubusercontent.com/116954249/220102899-9da7d7ef-0837-4ed1-9331-1a6aaf15d0ea.png)

### Frontend
- Created a docker-compose.yml file for frontend and backend
- docker-compose up


![compose up](https://user-images.githubusercontent.com/116954249/220103513-9ae26bdc-7e1d-47c1-a043-1ac1293b1f05.png)

- WebPage

![compose up 2](https://user-images.githubusercontent.com/116954249/220103672-b9d2205f-8c54-4673-9dc4-f5547d35cb70.png)
<br>
<br>

## Adding Notifications
- Added Notifications API in flask backend. Endpoint */api/activities/notifications*
- Implemented notifications page in react frontend

<table>
  <tr>
    <td><img src="https://user-images.githubusercontent.com/116954249/221242035-ebef00ad-834d-4964-a016-dd0eaefa17e5.png" alt="Notifications Backend"></td>
    <td><img src="https://user-images.githubusercontent.com/116954249/221242084-a01ed4b1-96eb-4763-94a0-41604b98dd5e.png" alt="Notifications Frontend"></td>
  </tr>
</table>
<br>
<br>


## DynamoDB local
- DynamoDB local is a downloadable version of Amazon DynamoDB where we can develop and test applications without accessing the DynamoDB web service. Instead, the database is self-contained on your computer. 
- When we are ready, we can simply remove the local endpoint and point it to DynamoDB service
- Created a dynamodb local service inside *docker-compose.yml* file.
<br>


```
dynamodb-local:
    # https://stackoverflow.com/questions/67533058/persist-local-dynamodb-data-in-volumes-lack-permission-unable-to-open-databa
    # We needed to add user:root to get this working.
    user: root
    command: "-jar DynamoDBLocal.jar -sharedDb -dbPath ./data"
    image: "amazon/dynamodb-local:latest"
    container_name: dynamodb-local
    ports:
      - "8000:8000"
    volumes:
      - "./docker/dynamodb:/home/dynamodblocal/data"
    working_dir: /home/dynamodblocal
```
<br>

- Docker image used here is **amazon/dynamodb-local:latest**
- command: `-jar DynamoDBLocal.jar -sharedDb -dbPath ./data`: This sets the command to run in the container, which launches the DynamoDB Local server with shared database mode and specifies the location of the database files.

![dynamodblocal done](https://user-images.githubusercontent.com/116954249/221244286-8314227f-6969-4aca-baf5-43f414fa38da.png)

## Postgres
- Created a postgres service in docker-compose file
- Installed postgres client
- Installed postgres plugin in vscode which is a Database viewer

![postgres done](https://user-images.githubusercontent.com/116954249/221256007-e87d331b-a9df-449a-82d0-919c9e8648f1.png)


# Cloud Security(By Ashish Rajan)

### Container security componenets
- Docker and Host Configuration
- Securing Images
- Secret Management
- Application Security
- Data Security
- Monitoring Containers
- Compliance Framework

### Security Best Practices
- Keep host and docker updated to latest security patches
- Docker daemon and containers should run in non-root user mode
- Image vulnerability scanning
- Trusting a Private registry vs Public registry
- No senditive data in Dockerfiles or images
- Use secret management service
- Read only file system and Volume for Docker
- Seperate database for long-term storage
- Use Devsecops practices
- Ensure all code is tested for vulnerabbilities before production use

### Snyk - Free software
- scans code repo for vulnerability. Mostly docker related

### Secrets Manager
- AWS Secrets Manager : for aws services - paid(no free tier)
- Hashicorp vault : Free=run your own server and manage, Paid=Server managed by them

### Image vulnerability scanning
- Amazon Inspector - Integration with ECR, EC2, AMI, Lambda - 15 day trail
- Clair
- Snyk
  - snyk auth, snyk container test redis:alpine

### Running containers in AWS
- ECS
- EKS
- App runner
- fargate
- AWS CoPilot

### Snyk implementation
- I have tried snyk for one of my other demo projects
![splashit_snyk](https://user-images.githubusercontent.com/116954249/221358423-7f1e9ad3-1918-4e21-a19c-bb0cab02637a.png)


# Spending Considerations (by Chirag)
- **Gitpod**: 500 credits -> 50 hours free per month
- **Github Codespaces**:  60 hours -> 2 cores :: 30 hours -> 4 cores
- **Cloud9** : Free tier(if present) : t2.micro
- Created a trail with AWS CloudTrail in week0 

<br>
<br>

# Homework Assignments
## Run the application in local environment
- Already had Docker installed in my laptop
- Created docker-compose.local.yml file
- Removed Gitpod specific urls and used localhost urls

Docker containers running
![local_docker](https://user-images.githubusercontent.com/116954249/221280379-66088c6f-e56c-4de7-9c81-ecbfaf47af90.png)

Frontend and backend running locally
<table>
  <tr>
    <td><img src="https://user-images.githubusercontent.com/116954249/221280484-b81f7897-5b82-4bf5-bf36-3cda5c1726c9.png" alt="Notifications Backend"></td>
    <td><img src="https://user-images.githubusercontent.com/116954249/221280579-1e517a97-1bd8-4a0f-a61b-473419271e42.png" alt="Notifications Frontend"></td>
  </tr>
</table>

## Pushed Images to Dockerhub
- I have built docker images for frontend and backend and pushed it to Dockerhub.
```
docker build -t cruddur-backend:v1 .
docker build -t cruddur-frontend:v1 .

docker tag cruddur-frontend:v1 vishnukumarkvs/cruddur-frontend:v1
docker push vishnukumarkvs/cruddur-frontend:v1

docker tag cruddur-backend:v1 vishnukumarkvs/cruddur-backend:v1
docker push vishnukumarkvs/cruddur-backend:v1
```
- To pull images
```
docker pull vishnukumarkvs/cruddur-backend:v1
docker pull vishnukumarkvs/cruddur-frontend:v1
```

![dockerhub](https://user-images.githubusercontent.com/116954249/221358749-5dbe6651-1734-49d0-aad0-6a9c329c7755.png)

## ECR and AWS App Runner
- AWS App Runner is a fully managed service provided by Amazon Web Services (AWS) that allows you to quickly and easily deploy containerized applications without having to worry about the underlying infrastructure.
- Right now, App Runner supports only ECR.
- So, I used default ECR public registry pf my account and pushed my two docker images into it. I just followed the push commands provided by ECR
- Then I created two services in app runner. 
- First I created backend service. Got the url.
- Then created frontend service. Passed backend url as Environment variable.
- Backend service normally takes two env vars: FRONTEND_URL and BACKEND_URL. These vars are used in CORS insdie the app.py. As the backend service is the first service we deploy, we dont get the urls before. So, i have disabled CORS in backend for this demo.

Both ECR and App Runner dont have any free tier. Well ECR has but might not useful.

App Runner pricing basic:-
- $0.064 / vCPU-hour*
- $0.007 / GB-hour*

ECR:-
- $0.10 per month per GB

**I have Deleted all resources after able to run the application as it will incur costs. I have provided snapshots below.**

ECR Repos

![ECR repos](https://user-images.githubusercontent.com/116954249/221359304-f0fe1076-3833-4f6f-b9d6-a3394df282ba.png)

App Runner Services

![app runner services](https://user-images.githubusercontent.com/116954249/221359530-c7baaeeb-d48f-41ac-8fa4-3517391ed1a4.png)

App Runner frontend and Backend

<table>
  <tr>
    <td><img src="https://user-images.githubusercontent.com/116954249/221359579-24000ef9-d6a9-4c85-aa4c-5e76a10620e5.png" alt="Notifications Backend"></td>
    <td><img src="https://user-images.githubusercontent.com/116954249/221359582-90397615-c36c-45a4-b50d-f0c3ea588c3e.png" alt="Notifications Frontend"></td>
  </tr>
</table>

# Additional Tasks

### TruffleHog
- TruffleHog is a tool to find sensitive data like Credentials(ex: aws_access_key, aws_secret_access_key) in your git repo
- TruffleHog scans all your commits for credentials and outputs it to you.
- It can only find real credentials: either active or inactive
- docker run --rm -it trufflesecurity/trufflehog:latest github --repo https://github.com/vishnukumarkvs/splashit
- docker run --rm -it trufflesecurity/trufflehog:latest github --repo https://github.com/vishnukumarkvs/splashit --only-verified

### BFG
- BFG is a repo cleaner tool
- We have used this tool to replace credentials in all our commits
- This cannot replace credentials in latest commit. If you have it, then remove all credentials and commit again.
- Find all credentails using Trufflehog and paste it in a text file
  #### Steps
   - Mirror the repo:
   git clone --mirror https://github.com/vishnukumarkvs/test_repo.git bfgtest
   
   - Find all texts you wanna replace and paste it in `replace.txt` file

   - Run bfg
   `java -jar bfg.jar --replace-text replace.txt bfgtest`

   - cd into repo
   `cd bfgtest`

   - Run git reflog command from previous output
   `git reflog expire --expire=now --all && git gc --prune=now --aggressive`

   - Now push the changes
   `git push (or) git push --force`
