# Week 10 — CloudFormation Part 1

### Summary
- Implemented Cloudformation for below
  - Networking
  - Cluster
  - DynamoDB
  - RDS Postgres
  - Backend Service
  - CI/CD
  - Frontend = Cloudfront
- Architecture Diagram : https://drive.google.com/file/d/1A1DTLOq63YQK8cHq0oqPTSSqt6yYcgwY/view?usp=sharing
- I have created cloudformation templates, written scripts to run each template, executed changesets.
- Imp points: Update CONNECTION_URL in parameter store after RDS deployment. Also update Route53 DNS records to load balancer

### Additional Notes

```
  CloudFormation Structure
  
  Description:
  Parameters:
  Mappings:
  Resources:
  Outputs:
  Metadata:

```
- CFN_PATH="/workspaces/aws-bootcamp-cruddur-2023/aws/cfn/template.yaml"
```
aws cloudformation deploy \
  --stack-name "my-cluster" \
  --template-file $CFN_PATH \
  --no-execute-changeset \
  --capabilities CAPABILITY_NAMED_IAM
```
- This doesnt execute changeset. You need to go to console -> cloudformation and then review the changes and execute changeset.
- You can see all changes like actions performed by you, aws lik create, delete cluster etc in cloudtrail
- validate-template. Checks for valid json or valid yaml. if not, returns error
- pip install cfn-lint
```
Rust installation
- curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
--> option 1
source $HOME/.cargo/env
rustc --version
```
- In AWS CloudFormation, the !Ref intrinsic function is used to retrieve the value of a parameter or resource in the same CloudFormation template. It allows you to reference other resources or parameters within the same template.
- However, the !Ref function cannot be used to reference values from other CloudFormation stacks directly. That's why you cannot use !Ref to reference the value from a parameter in a different stack.
- Instead, to reference values from other stacks, you can use the !ImportValue intrinsic function. This function allows you to import values exported by other stacks and use them in the current stack. In your example, Fn::ImportValue is used to import the value of VpcId from the NetworkingStack stack.
- stack-name present in deploy command. use that in refrencing or importing stacks
- envvars
- aws cloudformation create-stack --stack-name MyStack --template-body file://template.yaml --parameters ParameterKey=MyEnvVar,ParameterValue=example-value
- cfn-guard rulegen --template /workspaces/aws-bootcamp-cruddur-2023/aws/cfn/template.yaml 
- cloudformation designer
- cfn-toml = CFN-TOML stands for CloudFormation Template Object Markup Language. It is a human-readable and user-friendly syntax for authoring AWS CloudFormation templates. CFN-TOML is an alternative to the JSON or YAML formats traditionally used for writing CloudFormation templates.
- gem install cfn-toml

## Ashish security
- check compliance standarad
- use oranizations SCP to retrict actons like creation, deletion of production cloudformation templates
- enable aws cloudtrail
- check aws audity manager, iam access analyzer etc


  
