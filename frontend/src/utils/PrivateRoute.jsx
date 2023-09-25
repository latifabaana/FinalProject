import {Route,useNavigate, Outlet} from 'react-router-dom'
import React, {useState, useEffect} from "react";
import useApp from "../context/context";

const PrivateRoute = () => {
    const navigate = useNavigate();
    const {user} = useApp()

    // if no user then navigate to login 
    useEffect(()=>{ 
        console.log(user)
        !user && navigate("/login")
    }, [user])

    // otherwise navigate to the homepage
    return user && <Outlet />

    
}

export default PrivateRoute