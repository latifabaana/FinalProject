import { useState, useEffect } from 'react'
import axios from 'Axios'
import {useNavigate, useParams, useLocation} from "react-router-dom"

import useApp from "../context/context";

function Rating({ route, navigation }){
    // should all fields HAVE to be filled in? 
        // i think: overall rating HAS to be

 
    const {state} = useLocation();
    const { area_exists } = state;

    const {rating, setRating, areaId} = useApp()

    const navigate = useNavigate();

    useEffect(()=>{
        console.log(area_exists)
        console.log(areaId)
    }, [])
  

    useEffect(()=>{
        console.log(rating)
    },[rating])

    const handleRatingChange = (e) => {
        const {name, value} = e.target;
        setRating(prevRating => ({
            ...prevRating,
            [value] : !prevRating[value]

        }))

        e.preventDefault()
      }

    const handleDescriptionChange = (e) => {
        const {name, value} = e.target;
        setRating(prevRating => ({
            ...prevRating,
            [name] : value,

        }))
    }

    const submitForm = async () => {//maybe this doesnt have to be async because theres already a .then
       await axios.post(`http://127.0.0.1:8000/app/api/submitForm`, {rating: rating, id : areaId })
    //    get the navigation history and go back to the previous page and show the area. 
    // or send to a page that displays all ratings. 
        .then(navigate(-1))//send to home page with message that their review has been added.

    
    }

    return(
        <div>
            {area_exists == true && <p>This area already exists, fill in the form. </p> }
            <form>
                

                {/* onClick should call axios to true homeless sighting to the location id. */}
                <p>Click on the ones you've spotted to record a sighting</p>
                {/* highlight when they are clicked, when they are clicked again unhighlight. */}
                <input type="submit" onClick = {handleRatingChange} value = "homeless_sightings" />
                <br></br>
                <input type="submit" onClick = {handleRatingChange} value= "cig_but_count" />
                <br></br>
                <input type="submit" onClick = {handleRatingChange} value="swearing_count"  />
                <br></br>
                <input type="submit" onClick = {handleRatingChange} value="litter_count" />
                <br></br>

                
                <label> Overall Rating:
                    {/* instead of inputs replace with interactive stars */}
                    <input type="text" name="litter" />
                </label>
                <br></br>

                <label> Description:
                    {/* input needs to be bigger */}
                    <input type="text" onChange = {handleDescriptionChange} name="description" value = {rating.description}/>
                </label>
                {/* submit axios to django.  */}
                <input type="button" value="Submit" onClick ={submitForm} />
            </form>
        </div>
    )
}

export default Rating