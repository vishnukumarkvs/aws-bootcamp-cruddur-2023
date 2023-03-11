import './SigninPage.css';
import React from "react";
import {ReactComponent as Logo} from '../components/svg/logo.svg';
import { Link } from "react-router-dom";
import { Auth } from 'aws-amplify';
import jwt from 'jwt-decode';
import { useEffect } from 'react';
import { CognitoHostedUIIdentityProvider } from "@aws-amplify/auth/lib/types";

export default function SigninPage() {

  useEffect(() => {
    // Check for an existing Google client initialization
    if (!window.google && !window.google?.accounts) createScript();
  }, []);

  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [errors, setErrors] = React.useState('');
  // const [cognitoErrors, setCognitoErrors] = React.useState('');

  const onsubmit = async (event) => {
    setErrors('')
    event.preventDefault();
    Auth.signIn(email, password)
      .then(user => {
        console.log('user',user)
        localStorage.setItem("access_token", user.signInUserSession.accessToken.jwtToken)
        window.location.href = "/"
      })
      .catch(error => {
        if (error.code == 'UserNotConfirmedException') {
          window.location.href = "/confirm"
        }
        setErrors(error.message)
      });
    return false
  }

  const email_onchange = (event) => {
    setEmail(event.target.value);
  }
  const password_onchange = (event) => {
    setPassword(event.target.value);
  }

  let el_errors;
  if (errors){
    el_errors = <div className='errors'>{errors}</div>;
  }

  // Federated setup
  const createScript = () => {
    const script = document.createElement('script');
    script.src = 'https://accounts.google.com/gsi/client';
    script.async = true;
    script.defer = true;
    script.onload = initGsi;
    document.body.appendChild(script);
  }

  // Initialize Google client and render Google button
  const initGsi = () => {
    console.log(process.env.GOOGLE_CLIENT_ID);
    if (window.google && window.google?.accounts) {
      window.google.accounts.id.initialize({
        client_id: "1032693418393-1o23v8ar87v69setpcmhgbpns5c7m3f3.apps.googleusercontent.com",
        callback: (response) => {
          getAWSCredentials(response.credential);
        },
      });
      window.google.accounts.id.renderButton(
        document.getElementById("googleSignInButton"),
        { theme: "outline", size: "large" }
      );
    }
  }

  // Exchange Google token for temporary AWS credentials
  const getAWSCredentials = async (credential) => {
    const token = jwt(credential);
    const user = {
      email: token.email,
      name: token.name
    };      
    await Auth.federatedSignIn(
      'google',
      { token: credential, expires_at: token.exp },
      user
    );
    // await Auth.federatedSignIn({
    //   provider: CognitoHostedUIIdentityProvider.Google
    // });
    window.location.href = "/";
  }

  return (
    <article className="signin-article">
      <div className='signin-info'>
        <Logo className='logo' />
      </div>
      <div className='signin-wrapper'>
        <form 
          className='signin_form'
          onSubmit={onsubmit}
        >
          <h2>Sign into your Cruddur account</h2>
          <div className='fields'>
            <div className='field text_field username'>
              <label>Email</label>
              <input
                type="text"
                value={email}
                onChange={email_onchange} 
              />
            </div>
            <div className='field text_field password'>
              <label>Password</label>
              <input
                type="password"
                value={password}
                onChange={password_onchange} 
              />
            </div>
          </div>
          {el_errors}
          <div className='submit'>
            <Link to="/forgot" className="forgot-link">Forgot Password?</Link>
            <button type='submit'>Sign In</button>
          </div>

        </form>
        <div>
          <button id="googleSignInButton"/>
        </div>
        <div className="dont-have-an-account">
          <span>
            Don't have an account?
          </span>
          <Link to="/signup">Sign up!</Link>
        </div>
      </div>

    </article>
  );
}