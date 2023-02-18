# Week 0 — Billing and Architecture

# A. Hard Assignments

# 1. C4 Model

- I have used C4 model for understanding System Architecture of Cruddur application.
- C4 Model is a collection of 4 Core Diagrams which are Context, Container, Component and Code.
- https://drive.google.com/file/d/1W1VFxzawAdnSqWF5DtaSBGm2n0gVJd_2/view?usp=sharing

### System Context Diagram
![system context](https://user-images.githubusercontent.com/116954249/218927889-963998ae-89ad-45bf-b424-91e94ba96a01.png)

### Container Diagram
![Container Context](https://user-images.githubusercontent.com/116954249/218928165-b319b3e6-33e2-47aa-ba04-7aec80e69966.png)

### Component Diagram
![component context](https://user-images.githubusercontent.com/116954249/218927723-2d241390-4f9c-411e-a806-6d5778096845.png)

- Code Diagram is not relavent as of now. Will add it as we build on the application.

# 2. Recreated Cruddur Conceptual Diagram and Logical Diagram
- url: https://lucid.app/lucidchart/f0a4d501-b7ed-4be6-90d1-80382b1113bb/edit?invitationId=inv_75deb50a-5b1f-48fb-a344-cf8901d87c1b

![Cruddur - Conceptual Diagram](https://user-images.githubusercontent.com/116954249/219287974-390004c0-b02d-4896-ae22-80c6ece5e987.png)

- url: https://lucid.app/lucidchart/ccf10edc-3fd9-4c1d-8397-b46c6651b7d1/edit?invitationId=inv_cd342678-0116-452f-b6a0-32b3555357f5

![Cruddur Logical Diagram](https://user-images.githubusercontent.com/116954249/219288040-0dd5ad86-43bc-4218-8639-3424cc04fc33.png)

- I have created an Architecture Diagram for my own project
 - Reference: https://github.com/vishnukumarkvs/splashit/blob/main/README.md 

# 3. Added MFA
- Used third-party app on mobile for MFA

![MFA](https://user-images.githubusercontent.com/116954249/219421643-cc5c667e-6870-4ec0-bbdf-1de5a5e44d5c.png)

# 4. Created IAM User and configured access
- Created an alias for my account_id
- Created an iam user and named it *kvs-aws-bootcamp*
- Attached required policies to the user
- Created access and secret keys to the user

![newiamuser](https://user-images.githubusercontent.com/116954249/219422534-64f923be-90f4-428b-ab56-193fc2d674da.png)

# 5. Cloudshell
- AWS CloudShell is a browser-based, pre-authenticated shell that you can launch directly from the AWS Management Console. 
- We can run AWS CLI commands here
- `aws sts get-caller-identity` : Gives us the current aws iam user details
- `aws account get-contact-information` : Gives contact information such as name, address, phone number etc of the user
![cloud shell](https://user-images.githubusercontent.com/116954249/219423464-a209aaff-5173-4f41-9034-911b6a541fa4.png)




# 6. AWS Billing alerts and Budgets (By Andrew and Chirag)
- There are two ways to get notified for AWS Bills. They are **AWS Billing alerts** which is the old way and **AWS Budgets** which is the new way.
- AWS Budgets is preferred over AWS Billing alerts because Budgets are Global and Billing alerts are regional. A Billing alert is just a cloudwatch alarm. You need to create for every AWS Region you work in.

### AWS Billing alert
- I have created 2 alarms, one for 5 dollars and one for 10 dollars as theshold
![image](https://user-images.githubusercontent.com/116954249/219090942-8d35044a-6d21-43ed-a240-9696f789e2b9.png)
### AWS Budget
- I have been experimenting with EKS which explains the below cost. But I have AWS Credits so its fine.
![image](https://user-images.githubusercontent.com/116954249/219094834-fece7b2b-24e0-4917-bf94-81c7594608ed.png)
### AWS Budget with AWS CLI (in gitpod)
- `gp env AWS_ACCESS_KEY=""` : To store env variables permanently in gitpod workspace
- `env | grep AWS_` : To search for env variables
- `aws sts get-caller-identity`

``` 
{
    "UserId": "AIDA5BCKCG47KLMD*****",
    "Account": "895656015678",
    "Arn": "arn:aws:iam::895656015678:user/kvs-aws-bootcamp"
} 
```
- `aws sts get-caller-identity --query Account --output text` : gives us account_id
#### Creating Budget using CLI
- You need two files budgets.json and notifications-with-subscribers.json
- First json file contains details about the actual budget and secind file containes the subscriber. Here, the subscriber is my email address
```
aws budgets create-budget \
    --account-id $AWS_ACCOUNT_ID \
    --budget file://aws/json/budgets.json \
    --notifications-with-subscribers file://aws/json/notifications-with-subscribers.json
```

# 7. AWS Security (by Ashish Rajan)
### AWS Organizations
- It is a Hirerarchial structure.
- This is a free resource
- Used extensively by Enterprises
![image](https://user-images.githubusercontent.com/116954249/219119306-deb59e38-7b9b-40d5-b6ab-de5317d50ec5.png)

### CloudTrail
- It is an auditing service which audits all AWS events in your account
- By default, it audits only in your current region. Enable all regions while creating cloudtrail.
- 3 Types of Events : Management events, Data events, Insight events
- Management events show information about management operations performed on resources in your AWS account.
- Data events show information about the resource operations performed on or within a resource.
- Insight events identify unusual activity, errors, or user behavior in your account.
- CloudTrail has free tier for Management events: up to 5GB of CloudTrail data per month, and up to 100,000 CloudTrail events per month
- Data and insight events have additional cost
![image](https://user-images.githubusercontent.com/116954249/219125834-419a938c-80b7-4e3a-8e4e-a48b2e148f15.png)

### IAM Users vs IAM Roles vs IAM Policies
- IAM User
  - IAM user is a particular person or an application that can access AWS Resources in your account.
  - IAM user have security credentials like access_key and secret_access_key
- IAM Role
  - IAM role is an identity which can be assumed by IAM Users and AWS Services
  - By assuming an iam role, the particular user or service gets all permissions attached to the role
  - Example: EKS service needs EC2 for the worker nodes. So, it needs an IAM role to access EC2 services
- IAM Policy
  - It is a document (written in json) that specifies what actions are allowed or denied, which resources are affected, and who is allowed to perform those actions.
  - These policies can be attached to users, groups and roles

### Service Control Policies
- Definition: Service control policies (SCPs) enable central administration over the permissions available within the accounts in your organization. This helps ensure that your accounts stay within your organization’s access control guidelines.
![scp](https://user-images.githubusercontent.com/116954249/219855004-792fe961-d288-4133-b256-9c32d557e95d.png)
- Reference: https://github.com/hashishrajan/aws-scp-best-practice-policies
