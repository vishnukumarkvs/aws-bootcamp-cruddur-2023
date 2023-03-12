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
   
   
## Hard Assignments

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
- When user is authenticated, we get a jwt. We pass that jwt as a header called `Authorization`
- Flask backend fetches this JWT fron the request header. Then it uses for verifying users so it can show protected and unprotected endpoints
