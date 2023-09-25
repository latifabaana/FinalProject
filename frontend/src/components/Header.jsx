import { useState, useEffect } from 'react'
import axios from 'Axios'
import {useNavigate, Link} from "react-router-dom"

import useApp from "../context/context";
import "../CSS/Header.css"

function Header() {
  const {user, logoutUser} = useApp()

  return(
    // SEARCH BAR     | HOME | LOGOUT |
    <div className = "header">
        <Link className = "header-links" to = '/'>Home </Link>
        <span> | </span>
        {user ? (
            <Link className = "header-links" onClick = {logoutUser}> logout</Link>
        ): (
            <Link className='header-links' to = '/login'> Login</Link>
        )} 
        
    </div>
  )

}

export default Header