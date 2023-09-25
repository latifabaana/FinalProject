import { useState, useEffect } from 'react'
import { AppProvider } from './context/context';
import {Routes, Route} from "react-router-dom"

import PrivateRoute from './utils/PrivateRoute'

import './App.css'
import Rating from './components/Rating'
import Home from './pages/Home';
import CreateArea from './components/createArea';
import SignUp from './pages/SignUp';
import Header from './components/Header';
import Login from './pages/Login';

function App() {
  return (
    <AppProvider>
      <div className="App">
      <Header />
        <Routes>
          <Route exact element={<PrivateRoute  />}>
            <Route path="/" element={<Home />} />
          </Route>
          {/* <Route path = "/myMeals" element = {<MyMeals />} /> */}
          <Route path = "/login" element = {<Login />} />
          {/* sign up cannot be accessed if user is already logged in, so check for that */}
          <Route path = "/signup" element = {<SignUp />} />
          <Route path = "/rating" element = {<Rating />} />
          <Route path = "/createArea" element = {<CreateArea/>} />
        </Routes>
        
      </div>
    </AppProvider>
  );
}

export default App;
