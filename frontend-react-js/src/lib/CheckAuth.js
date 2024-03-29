import { Auth } from 'aws-amplify';


export const getAccessToken = async () => {
  try {
    const cognito_user_session = await Auth.currentSession();
    console.log('cognito_user_session', cognito_user_session);
    const access_token = cognito_user_session.accessToken.jwtToken;
    localStorage.setItem("access_token", access_token);
    return access_token;
  } catch (err) {
    console.log(err);
  }
};



// check if we are authenicated
const checkAuth = async (setUser) => {
    Auth.currentAuthenticatedUser({
      // Optional, By default is false. 
      // If set to true, this call will send a 
      // request to Cognito to get the latest user data
      bypassCache: false 
    })
    .then((cognito_user) => {
      console.log('cognito_user',cognito_user);
      setUser({
        display_name: cognito_user.attributes.name,
        handle: cognito_user.attributes.preferred_username
      })
      return Auth.currentSession()
    }).then((cognito_user_session) => {
        console.log('cognito_user_session',cognito_user_session);
        localStorage.setItem("access_token",cognito_user_session.accessToken.jwtToken)
    })
    .catch((err) => console.log(err));
    
  };


export default checkAuth;