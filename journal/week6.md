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
