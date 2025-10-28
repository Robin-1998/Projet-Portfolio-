import { Link } from 'react-router-dom';
import BodyPage from '../components/static_components/Body_page';
import LoginRegister from '../components/dynamic_components/Login_register';
import React, { useState } from 'react';

function Login() {
  return (
    <>
      <BodyPage>
        <LoginRegister />
      </BodyPage>
    </>
  );
}

export default Login;
