import { useState, useEffect } from 'react'
import axios from 'Axios'
import {useNavigate} from "react-router-dom"
import jwt_decode from "jwt-decode";
import useApp from "../context/context";
import "../CSS/Home.css"

// image imports
import homeless from "../assets/homeless_sightings.png"
import swear from "../assets/swearing_count.png"
import smoking from "../assets/cig_but_count.png"
import litter from "../assets/litter_count.png"
import homeImg from "../assets/home.png"

function Home() {

  const [myData, setMyData] = useState([])
  const [searchArea, setSearchArea] = useState([])
  const [areaData, setAreaData] = useState({areas: []})
  // default count for description
  const [descriptionCount, setDescriptionCount] = useState(3)

  const [areaSearched, setAreaSearched] = useState(false)

  const {rating, setRating, areaId, setAreaId, user} = useApp()

  const [ratingChanged, setRatingChanged] = useState('')

  const [addedDescription, setAddedDescription] = useState([])

  const [ratingIcons, setRatingIcons] = useState({
    'homeless_sightings': homeless,
    'cig_but_count': smoking,
    'swearing_count': swear,
    'litter_count': litter
  })

  const navigate = useNavigate();


  useEffect(()=>{ // if any of the icon rating changed then submit the rating to database
    submitRating(ratingChanged.name, ratingChanged.id)
  }, [ratingChanged])

  const handleChange = (event) => { // handle change of the search bar 
    setSearchArea(event.target.value)
    event.preventDefault()

  }

  const handleSubmit = (event) => { //handle submit of the search bar
    axios.get(`http://127.0.0.1:8000/ratings/getArea/${searchArea}`)
    .then(res => res.data)
    .then(data => {
      // sets the area data conditionally so they can be mapped. 
        data && setAreaData(data)
        data.length > 0 && setAreaId(data.areas[0].id)
    })
    // error handling for 404 error
    .catch((e)=>{
      console.log(e)
      setAreaData(prevAreaData => ({...prevAreaData, 'areas': []})) 
    })
    event.preventDefault()
    // state change if user entered search 
    setAreaSearched(true)
  }

  function handleRatingChange(e, id){ //handle rating change
    const {name, value} = e.target;
    // set the ratings 
    setRating(prevRating => ({
        ...prevRating,
        [name] : !prevRating[name]

    }))
    // set which rating changed
    setRatingChanged({
      'name': name,
      'id': id
    })

    // set rating icon images
    handleRatingIconChange(name)
    
    e.preventDefault()
  }

  function submitRating(name, id){
    // get the value that they clicked, if it's true, then post, 
    // if it's not delete it.
    if (rating[name] == true || rating[name] == 1 ){
      // add record
      axios.post(`http://127.0.0.1:8000/ratings/submitForm`, {rating: name, id : id})
      .then(res => res.data)
      .then(data => {
      console.log(data)
      })
     } else if (rating[name] == false || rating[name] == 0 ){
        // delete the record
        console.log('deleting ...')
        axios.post(`http://127.0.0.1:8000/ratings/deleteRating`, {rating: name, id : id})
        .then(res => res.data)
        .then(data => {
          console.log(data)
        })

      }

  }

  const handleRatingIconChange = (name) => { //toggle icon picture change upon click
    console.log(ratingIcons)
    setRatingIcons(prevIcons => ({
      ...prevIcons,
      // change icon from black and white to green 
      [name]: rating[name] == true ? `/src/assets/${[name]}.png` : `/src/assets/${[name]}_green.png`
    }))

  }

  const handleDescriptionChange = (e) => { //handle description bar change
    const {name, value} = e.target;
    setRating(prevRating => ({
        ...prevRating,
        [name] : value,

    }))
  }

  const submitDescription = (e, id)=> { //submit description to database
    console.log(user)
    axios.post(`http://127.0.0.1:8000/ratings/submitDescription`, {description: rating.description, area_id:id, user : jwt_decode(localStorage.getItem('authTokens'))})
    .then(res => res.data)
    .then(data => {
  
      // clear the description input bar.
      setRating(prevRating => ({
        ...prevRating,
        description: ""
      }))
      // add the description
      setAddedDescription(prevDescription => [...prevDescription, rating.description])
    })
    
    e.preventDefault()
  }


  return (
    <div className="App">
        
      <div className="card">
        
        <form className = "search-bar" onSubmit={handleSubmit}>
          <input type="search" placeholder = "search an area" value = {searchArea} onChange= {handleChange}></input>
        </form>

        {/* if seach area submitted and areaData.areas.length < 1 && <p>there is no area with that name, please try again or create a new area. </p> */}
        {areaSearched && areaData.areas.length <1 && (<p>There is no area with that name, please try again or create a new area</p>)}

        {areaData.areas.length > 0 && areaData.areas.map((item, i)=> {
          return(
            // should return a div with picture and everything
            <div className = "area-container" key = {i}>
              <div className='area-name-container'>
                <h1 className = "area-name">{item.name} <span className='area-country'> {item.country} </span></h1>
              </div>
              <div className="area-image">
                <div className = "likes-container">
                  <form>
                  {/* icons */}
                  {/* increment the ratings from database with the ones they just added.  */}
                    <img name = "homeless_sightings" onClick = {(e) => handleRatingChange(e, item.id)} src = {ratingIcons.homeless_sightings}></img>
                    <p>{item.homeless_sightings + rating.homeless_sightings}</p>
                    <img name = "litter_count" onClick = {(e) => handleRatingChange(e, item.id)} src = {ratingIcons.litter_count}></img>
                    <p>{item.litter_count + rating.litter_count}</p>
                    <img name = "swearing_count" onClick = {(e) => handleRatingChange(e, item.id)} src = {ratingIcons.swearing_count}></img>
                    <p>{item.swearing_count + rating.swearing_count}</p>
                    {/* <div> Icons made by <a href="https://www.flaticon.com/authors/iyikon" title="IYIKON"> IYIKON </a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com'</a></div> */}
                    <img name=  "cig_but_count" onClick = {(e) => handleRatingChange(e, item.id)} src = {ratingIcons.cig_but_count}></img>

                    <p>{item.cig_but_count + rating.cig_but_count}</p>
                  </form>
                </div>
                {/* default home image if none is added to the database */}
                {item.image ? (<img src = {`http://127.0.0.1:8000/ratings${item.image}`}></img>) : (<img src = {homeImg}></img>)}
              </div>
                
              {/* map the rating descriptions and display them as comments of the area with who said it */}
              <div className='description-container'>
                {item.rating_item.map((rating, i) => {
                  while(i<descriptionCount){
                    return(
                      // shows only a limited amount of descriptions, see more button allows them to see more 
                      <p className='description-name' >{rating.author.username}: <span className='description' >{rating.description}</span></p>
                    )
                  }
                  
                })}
                {/* add the new descriptions that were just added after rendering */}
                {addedDescription.length != 0 && (
                  addedDescription.map((item)=>{
                    return(<p className='description-name'>{user.username}: <span className='description' >{item}</span> </p>)
                  })
                )}
                
              </div>

              {/* if description is more than 6 show the "see less" */}
              {descriptionCount > 6 && (
                <a onClick = {() => setDescriptionCount(count => (count-5))} className='see-more'>see less</a>
              )}
              <br></br>
              {descriptionCount > 3 && (
                // if description count is more than 3 show the see more
                <a onClick = {() => setDescriptionCount(count => (count+5))} className='see-more'>see more</a>
              )}
              {/* description bar  */}
              <div className='add-description-container'>
                <form onSubmit={(e) => submitDescription(e, item.id)}>
                  <input type="text" placeholder = 'write a description for this area' onChange = {handleDescriptionChange}  name="description" value = {rating.description}/>
                </form>
              </div>  

            </div>   
          )
        }) }
        <br></br>
        {/* create area button always there */}
        <div className = "create-area-div"> <button className='create-area-btn' onClick = {()=> navigate('/createArea')}> <strong></strong> create area</button> </div>
      </div>
    </div>
  )
}

export default Home
