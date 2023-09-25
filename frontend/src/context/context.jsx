import React, {useState,useEffect, createContext, useContext} from "react";
import jwt_decode from "jwt-decode";
import {useNavigate} from "react-router-dom"

const AppContext = createContext(null);

export const AppProvider = ({ children }) => {

  const navigate = useNavigate();

  const [login, setLogin] = useState({
    'username': '',
    'passwords': ''
  })

  // sets authtoken before rendering homepage and login. 
  const [authTokens, setAuthTokens] = useState(()=> localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null)
  const [user, setUser] = useState(()=>localStorage.getItem('authTokens') ? jwt_decode(localStorage.getItem('authTokens')) : null)
  const [loginError, setLoginError] = useState(false)

  const [dataSet, setDataSet] = useState(false)

  const [areaId, setAreaId] = useState('')

  // set rating for the home page
  const [rating, setRating] = useState({
    "homeless_sightings": 0,
    "cig_but_count": 0,
    "swearing_count": 0,
    "litter_count" : 0,
    "description": "",
  })

  // login user function for login page
  const loginUser = async (e)=>{
    e.preventDefault() 
    // call axios to backend to get token for user
    let response = await fetch('http://127.0.0.1:8000/api/token/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body:JSON.stringify(login)
    })
    let data = await response.json()
    if(response.status === 200){
      // set the token
      setAuthTokens(data)
      // set the user so can be accessed for description bar and conditional rendering
      setUser(jwt_decode(data.access))
      // set in local storage so access is not lost even after re-rendering
      localStorage.setItem('authTokens', JSON.stringify(data))
      // navigate to home page after login success
      navigate('/')

    }else{ // if unsuccessful login
      setLoginError(true)
    }
  }

  // logout user functionality for logout on homepage.
  const logoutUser = ()=>{
    // remove access after logging out
    setAuthTokens(null)
    setUser(null)
    setLoginError(false)
    localStorage.removeItem('authTokens')
    // redirect to login page
    navigate('/login')
  }

  const updateToken = async ()=>{
    // refresh token and blacklists the previous token so only new token can access homepage.
    let response = await fetch('http://127.0.0.1:8000/api/token/refresh/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body:JSON.stringify({'refresh': authTokens?.refresh})
    })
    let data = await response.json()
    if(response.status === 200){
      // set the new tokens.
      setAuthTokens(data)
      setUser(jwt_decode(data.access))
      localStorage.setItem('authTokens', JSON.stringify(data)) 
    }else {
      // logout user if the token is expired and cannot be refreshed.
      logoutUser()
    }
  }

  useEffect(()=>{ // updates token every four minutes, 
    // because token only valid for 5 mins. so refreshes it 1 minute before just in case.
    console.log(authTokens)
    const fourMinutes = 1000 * 60 * 4
    const interval = setInterval(()=>{
      // only if there is a token already auotomatically refresh the token.  
      if (authTokens){
        updateToken()
      }
    }, fourMinutes)
    return ()=> clearInterval(interval)
                       
  }, [authTokens])


    return (
      <AppContext.Provider value={{  loginError, setLoginError, authTokens, user, loginUser, login, setLogin, logoutUser, dataSet, setDataSet, rating, setRating, areaId, setAreaId }}>
        {children}
      </AppContext.Provider>
    );
  };

  const useApp = () => {
    const context = useContext(AppContext);
  
    if (context === undefined) {
      throw new Error("useTheme must be used within a AppProvider");
    }
    return context;
  };
  
  export default useApp;