import { useState, useEffect } from 'react'
import axios from 'Axios'
import {useNavigate} from "react-router-dom"

import Rating from '../components/Rating'
import useApp from "../context/context";

const SignUp = () => {

    const {user} = useApp()
    const [signupErrors, setSignupErrors] = useState([])
    const navigate = useNavigate()

    useEffect(()=>{ //if user already logged in navigate to homepage
        user && navigate('/')
    }, [user]) 

    // sign up state
    const [signup, setSignup] = useState({
        'username': '',
        'email': '',
        'password1': '',
        'password2':''
    })

    const handleChange = (e)=>{ //handle signup form 
        e.preventDefault()
        const {name, value} = e.target
        setSignup(prevSignup => ({
            ...prevSignup,
            [name] : value
        }))
      
    }

    const submitForm = (e) => {
        e.preventDefault()
        // post sign up to django
        axios.post(`http://127.0.0.1:8000/api/signup/`, {signup})
        .then(res => res.data)
        .then(data => {
            // if there are errors add them to be presented, else if successful redirect to login
            !data.registered ? setSignupErrors(data['form-errors']) : navigate('/login')
        }).catch((e) => { //catch errors if 400 and set errors to be displayed
            if(e.response.status == 400){
                console.log(e.response.data)
                !e.response.data.registered && setSignupErrors(e.response.data['form-errors'])
            }
        })
    }

    const handleClick = ()=>{ //navigate to login if login link clicked.
        navigate('/login')
    }

    return( //sign up form
       <div className = 'login_wrapper'>
            <div className = 'login_container'>
                {/* calls submitForm function above on submit. */}
                <form className = "login_form" onSubmit={submitForm}>
                    <p className = "login_title">Sign Up</p>

                    <div className="form-group login_input-field">
                        <input aria-label="username" 
                        type = "text" 
                        onChange = {handleChange} 
                        name = 'username' 
                        value = {signup.username} 
                        placeholder='username'/>
                        
                    </div>
                    <div>
                        {/* display signup errors */}
                        {signupErrors.username && <p>{signupErrors.username}</p>}
                    </div>

                    <div className="form-group login_input-field">
                        <input aria-label="email" 
                        type = "email" 
                        onChange = {handleChange} 
                        name = 'email' 
                        value = {signup.email} 
                        placeholder='email' />
                    </div>
                    <div>
                        {signupErrors.email && <p>{signupErrors.email}</p>}
                    </div>
                
                    <div className="form-group login_input-field">
                        <input aria-label="password" 
                        type = "password" 
                        onChange = {handleChange} 
                        name = 'password1' 
                        value = {signup.password1} 
                        placeholder='password' />
                        
                    </div>
                    <div>
                        {signupErrors.password1 && <p>{signupErrors.password1}</p>}
                    </div>

                    <div className="form-group login_input-field">
                        <input aria-label="password" 
                        type = "password" 
                        onChange = {handleChange} 
                        name = 'password2' 
                        value = {signup.password2} 
                        placeholder='password' />
                    </div>
                    <div>
                        {signupErrors.password2 && <p>{signupErrors.password2}</p>}
                    </div>

                    <input className="btn solid" aria-label="submit" type = 'submit' /> 

                    {/* already have an account then login page redirect */}
                    <p>Already have an account? <button className="signup_btn" onClick = {handleClick}>Login</button></p>
                </form>
             
            </div>
       </div>
    )
}

export default SignUp