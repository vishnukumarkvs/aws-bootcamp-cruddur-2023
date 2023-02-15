# Week 0 — Billing and Architecture

# A. Instructional tasks
## 1. C4 Model

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

## 2. AWS Billing alerts and Budgets
- There are two ways to get notified for AWS Bills. They are **AWS Billing alerts** which is the old way and **AWS Budgets** which is the new way.
- AWS Budgets is preferred over AWS Billing alerts because Budgets are Global and Billing alerts are regional. A Billing alert is just a cloudwatch alarm. You need to create for every AWS Region you work in.

### AWS Billing alert
- I have created 2 alarms, one for 5 dollars and one for 10 dollars as theshold
![image](https://user-images.githubusercontent.com/116954249/219090942-8d35044a-6d21-43ed-a240-9696f789e2b9.png)
### AWS Budget
- I have been experimenting with EKS which explains the below cost. But I have AWS Credits so its fine.
- ![image](https://user-images.githubusercontent.com/116954249/219094834-fece7b2b-24e0-4917-bf94-81c7594608ed.png)
