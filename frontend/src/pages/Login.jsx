import { useState, useEffect } from 'react'
import {Navigate, useNavigate} from "react-router-dom"

import useApp from "../context/context";
import "../CSS/Login.css"

function Login() {
    const navigate = useNavigate()

    const {login, setLogin, loginUser, user, loginError} = useApp()
    
    useEffect(()=>{ // if there is user, navigate to the homepage, if there isn't a user => stay on page because need to login.
        user && navigate('/')
    }, [user])  

    const handleChange = (e)=>{ //handle change for login
        e.preventDefault()
        const {name, value} = e.target
        setLogin(prevLogin => ({
            ...prevLogin,
            [name] : value
        }))
    }

    const handleClick = ()=>{ //navigate to sign up if sign up link clicked
        navigate('/signup')
    }

    return(
        <div className="login_wrapper">
            <div className="login_container">
                {/* calls loginUser created in context to authenicate and sign user in. */}
                <form className = "login_form" onSubmit = {loginUser}>
                    <p className = "login_title">Login</p>
                    <p>default username: user default password: pass </p>
                    <div className="form-group login_input-field">
                        <input aria-label="username" 
                        type = "text" 
                        onChange = {handleChange} 
                        name = 'username' 
                        value = {login.username} 
                        placeholder='username'/>
                    </div>
                    
                    <div className="form-group login_input-field">
                        <input aria-label="password" 
                        type = "password" 
                        onChange = {handleChange} 
                        name = 'password' 
                        value = {login.password} 
                        placeholder='password' />
                    </div>
                    {/* if there are login errors => notify them  */}
                    {loginError && <p>Username or password is incorrect</p>}

                    <input className="btn solid" aria-label="submit" type = 'submit' /> 

                    {/* if no account, sign up*/}
                    <p>don't have an account? <button className="signup_btn" onClick = {handleClick}>Sign-up</button></p>
                </form>
            
            </div>
        </div>
    )

}

export default Login