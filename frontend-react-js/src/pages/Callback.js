// import React, { useEffect } from 'react';
// import { Auth } from 'aws-amplify';

// function Callback() {
//   const exchangeCodeForToken = async (code) => {
//     try {
//       const response = await Auth.federatedSignIn('google', { code });
//       console.log(response);
//       // handle successful authentication
//       window.location.href = "/"
//     } catch (error) {
//       console.error('Error exchanging code for token:', error);
//       // handle error
//     }
//   };

//     // extract the authorization code from the URL
//   const queryParams = new URLSearchParams(window.location.search);
//   const code = queryParams.get('code');

//   if (!code) {
//     console.error('No authorization code found in URL');
//     // handle error
//     return null;
//   }

//   exchangeCodeForToken(code);

//   return (
//     <div>
//       <p>Redirecting...</p>
//     </div>
//   );
// }

// export default Callback;

import { useEffect } from 'react';
import { Auth } from 'aws-amplify';

function Callback() {
  useEffect(() => {
    const handleAuthResponse = async () => {
      try {
        // Get the access token from the URL hash fragment
        const hash = window.location.hash.substring(1);
        const params = new URLSearchParams(hash);
        const accessToken = params.get('access_token');

        // Store the access token in localStorage or use it to authenticate requests
        localStorage.setItem('access_token', accessToken);

        // Call the Cognito Post-Confirmation trigger with the access token
        // const response = await fetch('/api/post-confirmation', {
        //   headers: {
        //     Authorization: `Bearer ${accessToken}`
        //   }
        // });
        // const data = await response.json();
        // console.log(data);

        // Redirect to the home page or some other protected route
        window.location.href = '/';
      } catch (error) {
        console.error('Error handling auth response:', error);
      }
    };

    handleAuthResponse();
  }, []);

  return <div>Processing...</div>;
}

export default Callback;
