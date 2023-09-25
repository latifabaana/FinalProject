import { useState, useEffect } from 'react'
import axios from 'Axios'
import {useNavigate} from "react-router-dom"

import useApp from "../context/context";
import "../CSS/Create-area.css"
import homeImg from "../assets/home.png"

function CreateArea(){
    // new area form fields
    const [newArea, setNewArea] = useState({
        "name": "",
        "country": "",
        "city" : "",
        "borough": ""
    })

    // file states for image
    const [selectedFile, setSelectedFile] = useState('')
    const [urlFile, setUrlFile]= useState()

    // store form errors
    const [errors, setErrors] = useState('')

    const navigate = useNavigate();

    useEffect(()=>{ //set the url of image once a file is chosen
        selectedFile && setUrlFile(URL.createObjectURL(selectedFile))
    }, [selectedFile])

    const handleChange =(e) => { //handle change for new area form
        const {name, value} = e.target;
        setNewArea(prevArea => ({
            ...prevArea,
            [name]: value,
        }))
    }

    const submitForm = async () => { //submit form including image to the database
        let form_data = new FormData();
        form_data.append('name', newArea.name);
        form_data.append('country', newArea.country);
        form_data.append('city', newArea.city);
        form_data.append('borough', newArea.borough);
        try {
            form_data.append('image', selectedFile, selectedFile.name);
        }catch(error){
            // maybe change this. it doesn't really matter if the image is not filled in. 
            console.log(error)
        }
        axios.post(`http://127.0.0.1:8000/ratings/createArea`, form_data, { //create an area based on form data
            headers: {
              'content-type': 'multipart/form-data'
            }
        })
        .then(res => res.data)
        .then(data => {
            // get the errors of the invalid form and display it first. if there are no errors then navigate.
            // after creating area, navigate back to the home page so they can search and rate areas.  
            data['validation_errors'] == true ? setErrors(data['area_form_errors']) : navigate('/', {state: { area_exists: data['area_exists'] } })
        }).catch((e) => {
            if(e.response.status == 400){
                console.log(e.response.data)
                // set errors and display it to the user if there are errors
                e.response.data['validation_errors'] == true && setErrors(e.response.data['area_form_errors'])
            }
            else if (e.response.status= 409){
                //if area already exists
                e.response.data['area_exists'] == true && setErrors({'name' : 'An area with this name and country already exists'})
            }
        })
    }

    return(
        // loop through the errors like we did in the sign-up 
        <div className='create-area-container'>
            {/* if image selected, display selected image otherwise display default image*/}
            <div className='preview-image'>
                <img src = {selectedFile ? urlFile : homeImg}></img>
            </div>

            {/* new area form */}
            <form method = 'POST' encType='multipart/form-data'>
                {/* area names and their errors */}
                <input className = "new-area" name = 'name' value={newArea.name} onChange = {handleChange} placeholder='name'></input>
                {errors.name && (<p>{errors.name}</p>)}
                <input className = "new-area" name = 'country' value = {newArea.country} onChange = {handleChange} placeholder='country'></input>
                {errors.country && (<p>{errors.country}</p>)}
                <input className = "new-area" name = 'city' value={newArea.city} onChange = {handleChange} placeholder='city'></input>
                {errors.city && (<p>{errors.city}</p>)}
                <input className = "new-area" name = 'borough' value={newArea.borough} onChange = {handleChange} placeholder='borough'></input>
                {errors.borough && (<p>{errors.borough}</p>)}
                {/* image field to choose image. */}
                <input name = 'image' accept="image/*" type="file" onChange={(e) => setSelectedFile(e.target.files[0])}/>
                <input id = "create-area-btn" type="button" value="Create" onClick ={submitForm} />
            </form>
        </div>
    )


}

export default CreateArea