# Week 4 — Postgres and RDS

## Assignments

### Overall tasks done
- Configured github codespaces
- Created RDS instance
- written db scripts shortcuts for schema-load, creting tables etc
- worked with CONNECTION_URL and PROD_CONNECTION_URL
- implemented activities
- implemented Google auth. 90% done

### Creating RDS instance
- Using AWS CLI

```
aws rds create-db-instance \
  --db-instance-identifier cruddur-db-instance \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version  14.6 \
  --master-username cruddurroot \
  --master-user-password .... \
  --allocated-storage 20 \
  --availability-zone us-east-1a \
  --backup-retention-period 0 \
  --port 5432 \
  --no-multi-az \
  --db-name cruddur \
  --storage-type gp2 \
  --publicly-accessible \
  --storage-encrypted \
  --enable-performance-insights \
  --performance-insights-retention-period 7 \
  --no-deletion-protection
```

### Postgres
- POSTGRES has namespaces . default is public
- \dt -> To see the tables
- SELECT uuid FROM public.users WHERE users.handle = 'vvvv' LIMIT 1; -> use '' not ""
- \x on
  - to view data clearly
  - good for very few records
- echo $1 -> first parameter
- https://www.postgresql.org/docs/9.5/functions-json.html
- It is recommended to use parameterized queries to avoid SQL injection attacks. You can use cur.execute() method to pass the values as parameters to the query. 


### Bash
- No spaces in assignments in bash. In loops, spaces are required
- whereis bash
- chmod u+x bin/db-create
- ./bin/db-drop

### Other commands
- curl ifconfig.me -> ip address for gitpod or codespace or anything
- Modify SEcurity group rule

```
aws ec2 modify-security-group-rules \
    --group-id $DB_SG_ID \
    --security-group-rules SecurityGroupRuleId=$DB_SG_RULE_ID,SecurityGroupRule={Description="CODESPACE",IpProtocol=tcp,FromPort=5432,ToPort=5432,CidrIpv4=$CODESPACE/32}
```

### RDS
- arn for psycopg: arn:aws:lambda:us-east-1:898466741470:layer:psycopg2-py38:2
- Policy

```
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action":[
            "ec2:CreateNetworkInterface",
            "ec2:DeleteNetworkInterface",
            "ec2:DescribeNetworkInterfaces"
            ],
            "Resource":"*"
    }]
}
```
- steps for lambda
  - add pscog2 layer
  - add policy ec2 for basic role
  - attach vpc
  - add connection url env
  - update sg with codespace ip
  - add lambda trigger to cognito

### My Work
- RDS Instance

![cruddur rds instance](https://user-images.githubusercontent.com/116954249/226827648-98a99a69-7704-4514-8917-93e684fd4ec7.png)

- DB Setup

![db setup](https://user-images.githubusercontent.com/116954249/226827754-18b4d7cf-a9fb-4889-867f-e89a5739700f.png)

- Cruddur database

![cruddur databasew](https://user-images.githubusercontent.com/116954249/226827799-be557d21-a945-4121-8d16-6e4848315088.png)

- Exceutables

![executables](https://user-images.githubusercontent.com/116954249/226827967-573da9b1-0439-45c6-8407-e7c92082787a.png)


- Connect and load

![connect and load](https://user-images.githubusercontent.com/116954249/226827900-b5d72233-1eda-47f5-ad04-f7466f0fc668.png)

- Seed data

![import seed data in frontend](https://user-images.githubusercontent.com/116954249/226828112-1c392bc8-70c3-4353-a1b0-6b2941d142be.png)

- Activities

![done activities](https://user-images.githubusercontent.com/116954249/226828226-cceaac65-4b3f-4772-9211-6abb14442871.png)


## Homework
- Google Auth
- Minor Issue: congito_user object of federated google user doesnt have attributes section. Trying to fix it.

![image](https://user-images.githubusercontent.com/116954249/226828445-8a417c4e-62e4-4c38-a0d7-f19bb12fd2f8.png)


## Security
#### RDS
- SQL vs NoSQL
- Make sure you are in right region. use your region(if India, can use Mumbai)
- good practice: publicy not accessible
- In production, enable Multi-Az and Deletion protection
- postgres connection: DBweaver
- Use SCP, CloudTrail, Guarduty
- for, auth to rds instance, use IAM or kerberos(not the default)
- Db lifecycle management - CRUD
- Dont have RDS internet accessible
- encryption at Transit
- Use Secrets Manager



