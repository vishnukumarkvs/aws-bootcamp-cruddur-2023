# Week 1 — App Containerization

# Hard Assignments

## Docker Introduction
- Docker is a software that enables us to build and ship applications quickly
- Core concepts of Docker are Docker Container and Docker Image.
- A docker image contains your application code with all its dependencies
- A docker container is instance of docker image. You can run your application by running the container .You can create, start, stop, move, or delete a container using the Docker API or CLI.

## Cruudur up and running
- I have followed the week1 stream and was able to create Dockerfiles for Frontend and Backend
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

# Cloud Security(By Ashish Rajan)
- Done with Snyk

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
