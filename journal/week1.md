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
