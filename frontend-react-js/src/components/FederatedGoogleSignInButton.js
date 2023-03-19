import { Auth } from 'aws-amplify';

function FederatedGoogleSignInButton() {
  const handleGoogleSignIn = async () => {
    try {
      await Auth.federatedSignIn({ provider: 'Google' });
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