// src/components/Home.js
import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div>
      <h1>Home Page</h1>
      <nav>
        <ul>
          <li><Link to="/login">Login</Link></li>
          <li><Link to="/register">Register</Link></li>
          <li><Link to="/dashboard">Dashboard</Link></li>
          <li><Link to="/resume-upload">Resume Upload</Link></li>
          <li><Link to="/job-description">Job Description Input</Link></li>
        </ul>
      </nav>
    </div>
  );
};

export default Home;