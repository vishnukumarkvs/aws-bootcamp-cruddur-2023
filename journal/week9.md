# Week 9 — CI/CD with CodePipeline, CodeBuild and CodeDeploy

## Summary
- Created pipeleine in AWS Codepipeline for backend-flask microservice
- Create build project in CodeBuild, configured permissions to access ECR
- Added codebuild project in codepipeline
- Able to build successfully with merge_pullrequest trigger


## Notes

### CI/CD

- It is a devops process to seamlessly deploy the application to production
- CI = Continuos Integration
- CD = Continuous Deployment/Delivery

### Source Code repositery
-  repository or a place where our code exists
- Ex: github, gitlab

### AWS Services
- CodeCommit
- CodeBuild
- CodeDeploy
- CodePipeline - Stage orchestrator

## CodeBuild
- AWS CodeBuild is a fully-managed continuous integration service that compiles source code, runs tests, and produces software packages that are ready to deploy.

### Steps
- connect to github
- source version - prod
- choose repository in my github
- push, pull_request_merged
- enable privilege for docker builds

### issues
- dont add vpc to codebuild as it cant access internet, ECR
- (ERROR) The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8) and no specific platform was requested
- choose environment image : x86_64 =  amd

### Codebuild policy

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "VisualEditor0",
      "Effect": "Allow",
      "Action": [
        "ecr:BatchCheckLayerAvailability",
        "ecr:CompleteLayerUpload",
        "ecr:GetAuthorizationToken",
        "ecr:InitiateLayerUpload",
        "ecr:PutImage",
        "ecr:UploadLayerPart",
        "ecr:BatchGetImage",
        "ecr:GetDownloadUrlForLayer"
      ],
      "Resource": "*"
    }
  ]
}
```

### Build succeeded (on 11th try)

![build succeeded](https://user-images.githubusercontent.com/116954249/236178525-0232f3e1-279a-418a-b9b9-ed1a7d8db08a.png)

## CodePipeine
- connect to github
- use prod branch
- 3 STAGES: Source, Build and Deploy
- Match the artifacts directory in Build and Deploy Stage

![deploy successful](https://user-images.githubusercontent.com/116954249/236179163-30314d20-5552-456e-a216-c137ccf3506c.png)

## Final Check
- Updated Health Check

![update-health-check](https://user-images.githubusercontent.com/116954249/236179343-4053c553-488b-43dd-a7f1-0b024c84e746.png)

# Security Best Practices

### Top 10 OWASP Security Risks
- Insufficient flow control mechanisms
- Inadequate IAM
- Dependency Chain Abuse
- Poisones Pipeline Exceution
- Insufficient PBAC(Pipeline based access control)
- Insufficient Credential Hygene
- Insuficient System Configuration
- Ungoverned usage of 3rd party
- Improper Artifact Integrity Validation
- Insufficient logging and visibility

### From AWS
- Check compliance standard
- Enable SCP for ci/cd services
- cloudtrail enabled
- GuardDuty for dns coms monitoring
- aws config rules for codebuild

### Security best practices
- access control - IAM
- security for source control, secret management, containers
- SAST, DAST
- entry point - no bypass of production stage
- encryption at transit
- use trusted source control





