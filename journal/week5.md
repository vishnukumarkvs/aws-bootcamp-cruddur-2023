# Week 5 — DynamoDB and Serverless Caching


# Introduction


### Nosql
- its precomputed
- just asking particularly
- you are not asking database like give me these etc

### Ddb
- DynamoDb acts like a database.
- In Dynamodb, we create tables.
- 3 core components: tables, Items, attributes
- Tables is a collection of items, and each items contains set of attributes
- DDb uses primary keys to uniquely identify an Item in table, and secondary indexes for more querying flexibility
- DDb streams are used to capture data modification events in DDB tables

### Imp points
- Each item has a primary key. PK is one or set of attributes which should be present in each and every item.
- DDb tables are schemaless. neither attrs nor data types needed to be defined before hand.
- You can define a

### DynamoDb core
Reference - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html

### Other stuff
- `chmod -R u+x ddb/` - To make whole folder executable
- `aws cognito-idp list-users --user-pool-id <id>  --limit 20`


# Work

- I have written two setup scripts, one for db and other for ddb. ddb script is for prod
- I have mostly used python for the scripts as I was familiar

```
./bin/db/setup
./bin/ddb/setup
```

- I created a table 'cruddur-messages' and created schema, loaded seed data. I have added two users in my cognito pool as we use cognito authentication. 
- I updated your users with mine and was able to perform all tasks

**My cognito users**

![cognito users output](https://user-images.githubusercontent.com/116954249/228728108-ff410d6b-296c-4c5f-82ed-3d54350d2b2e.png)

**Schema load and list-tables**

<table>
  <tr>
    <td><img src="https://user-images.githubusercontent.com/116954249/228728602-a773476d-924c-4eb4-aef5-0f5469b72042.png" alt="Ddb schema"></td>
    <td><img src="https://user-images.githubusercontent.com/116954249/228728630-4bc2ec2f-7fb1-43d3-90ba-ec7311022736.png" alt="list tables"></td>
  </tr>
</table>

**Messages**

![messages done](https://user-images.githubusercontent.com/116954249/228728887-6dd54be8-1500-4520-a604-c264cdd90693.png)

**Create Message**

![createmessagedone](https://user-images.githubusercontent.com/116954249/228729046-795d9921-96ad-4680-a8ee-44fa07ba2179.png)


**New user implementation**

![new user done](https://user-images.githubusercontent.com/116954249/228729091-d4d7608a-d864-4346-b565-8011d9a27948.png)


# Security bu Ashish

- NoSql are speedy

### DynamoDb usecases
- Banking and Finance
  - Fraud detection
  - user transactions
  - mainframe offloading

- Gaming
  - Game stats
  - Leaderboard
  - Player data stores

- Software and Internet
  - metadata
  - relational graph data stores

- Ad Tech
  - user profile stores
  - metadata stpres for assets
  - popular-item cache

- Retail
  - shopping carts
  - workflow engines
  - customer profiles

- Media 
  - User data stores
  - Media meta data stores

 
### Access dynamodb
- through internet - wrong
- throgh vpc endpint, gateway endpoint - correct

### Dynamodb accelarator (DAX)
- cache within vpc
- access with cross account iam role
- dax cluster present in subnet inside vpc . we will point to dynamodb table

### Best practices
- use vpc endpoint, private link for access
- choose your aws region
- scp, cloudtrail, aws config rules
- AWS Config Rules is a service provided by Amazon Web Services (AWS) that allows you to define and enforce desired configurations for your AWS resources. It helps you ensure that your AWS resources comply with your organization's security and compliance policies.
- dont have access from internet for ddb
- DAX to have read only on ddb table


