// replace the user pool region, id, and app client id details
export default {
    "REGION": process.env.REACT_APP_AWS_COGNITO_REGION,
    "USER_POOL_ID": process.env.REACT_APP_AWS_USER_POOLS_ID,
    "USER_POOL_APP_CLIENT_ID": REACT_APP_COGNITO_CLIENT_ID
}