# Week 3 — Decentralized Authentication

## Introduction
- AWS cognito - Authentication Service provided by AWS
- Types
  - Pools : Mainly used for storing users
  - Identities : Give users temporary access to AWS Resources

- Pools
  -  User pools: Your own authentication service where we can store users, manage theri signin, signup, recovery, mfa etc
  -  Federated pools: Thirdparty providers like Google, Facebook, Apple etc
  
 - JWT
   - JsonWebToken, used for authorization of user
   - we can store user metadata in jwt claims
   - jwt has 3 parts: Header, payload and signature. These are seperated by '.'
   - jwts can be verified with public key as well as client secret
   
   
## Assignments

### Have setup cognito user pool
- Created a cognito user pool `cruddur-user-pool`
![cruddur-user-pool](https://user-images.githubusercontent.com/116954249/224546704-7dd5b2c3-0ffe-4c22-a7a0-bbe8b06a2657.png)

### Configured React frontend with SignIn, SignUp, Forgot password
- verification code and user confirmation

<table>
  <tr>
    <td><img src="https://user-images.githubusercontent.com/116954249/224547530-ea8667cd-4a06-401f-aa5b-21fd9e46ac97.png" alt="Sampling Rule"></td>
    <td><img src="https://user-images.githubusercontent.com/116954249/224547542-e4e8a15b-bc12-450b-8da9-68e0f284193d.png" alt="XRay Group"></td>
  </tr>
</table>

- User details in frontend

![username and handle](https://user-images.githubusercontent.com/116954249/224547652-2d8850e3-d4a4-4925-8dd2-217f93572223.png)

## Verifying JWT in flask backend
- Used `python-jose[cryptography]` pip pacakge for jwt verification
- When user is authenticated, we get a jwt. We pass that jwt as a header called `Authorization`

![flask bearer](https://user-images.githubusercontent.com/116954249/224561082-71ea438d-dcdf-421b-a668-d6bb37f70375.png)


- Flask backend fetches this JWT fron the request header. Then it uses for verifying users so it can show protected and unprotected endpoints
- Used variable `token_valid`. If token_valid is true, we can shouw certain page, if it isnt we can shouw another page. 
- We make token_valid to true only if jwt is verified, else in all cases like token not found, expired etc, we set it to false
- Two ways to verify jwt - using client secret or public key
- Here, I am using public key. Amazon Cognito User Pools provide a JSON Web Key (JWK) set that includes the public keys used to verify the JWTs issued by the user pool.
- Fetching the public key from Amazon Cognito User Pools using the JWKS URI does not cost anything.

### Code
- Written ` verify_jwt_token` function inside app.py file of backend
- permalink: https://github.com/vishnukumarkvs/aws-bootcamp-cruddur-2023/blob/070d64f41f2beed43841c37a8d1484ec78549c58/backend-flask/app.py#L97

- Authenticated vs Not-Authenticated based on jwt

<table>
  <tr>
    <td><img src="https://user-images.githubusercontent.com/116954249/224561263-c5c9d677-cb6a-454d-b085-2e97c00beb4e.png" alt="Authenticated"></td>
    <td><img src="https://user-images.githubusercontent.com/116954249/224561367-0f3aa8c3-32cf-42fb-baca-18b510dd8110.png" alt="Not authenticated"></td>
  </tr>
</table>


## Google SignIn
- Tried but still facing issues

#### Known issues that I overcame and also still present
- Federated identities are different from federated pools. Their implementation in aws-amplify is different
- Federated identities gives us temporary creds, no need to implement this in federated user pool
- Callback url : Present in cognito federated user pool, this needs to be a valid public url.
- For Google sigin, you need knowledge of GCP. You need to configure OAuth there


Currently facing below issue
- redirect_uri mismatch
- wrong client-id

# Cloud Security 

## Notes

### Authentication
- SSO
- OAuth
- OpenID

oauth2.0 - authorization
 
### Decentralized authentication
- meaning federated authentication
- username, pass only store at one place

### User pool
- for authentication

### Identity pool
- for aws temporrary credentials

### User life cycle management
- emp joins - create profile - assign apps - onboard emp - additional reqs - changes - emp resigns - offboard
### Token life cycle management
- creation - assignment - activation - suspension - removal - expiration


### Security best practices
- cognito user pools should be in aws region that you are leggaly allowed to be holding data
- use organization scp to manage user pooldeletion, creation, region lock
- enable cloudtrail
- application should use Industry standard authentication like saml, oauth2
- app user lifecycle management - create modify delete users
- aws user access lifecycle management change of roles/ revoke roles
- token lifecycle management - issue new tokens, revoke, expire
- access token scope - should be limited
- jwt shouldnt contain sensitive info
- encryption in transit - api calls

