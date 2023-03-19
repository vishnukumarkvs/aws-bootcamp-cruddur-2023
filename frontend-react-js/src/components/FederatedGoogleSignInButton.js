import { Auth, Cache } from 'aws-amplify';

function FederatedGoogleSignInButton() {
  const handleGoogleSignIn = async () => {
    try {
      // Sign in with Google using Amplify Auth
      await Auth.federatedSignIn({ provider: 'Google' });
      // Get the user session
      const session = await Auth.currentSession();
      // Get the JWT token from the session
      const token = session.getIdToken().getJwtToken();
      // Store the token in local storage
      localStorage.setItem('access_token', token);
    } catch (error) {
      console.log('Error signing in with Google:', error);
    }
  };

  return (
    <button onClick={handleGoogleSignIn}>
      Sign In with Google
    </button>
  );
}

export default FederatedGoogleSignInButton;