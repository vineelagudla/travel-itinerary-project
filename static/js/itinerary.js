'use strict';

//JS for displaying search results after clicking on search button.
let markers = [];

function initMap() {
  const sfBayCoords = {
      lat: 37.8,
      lng: -122.20287,
    };
      const basicMap = new google.maps.Map(document.querySelector('#map'), {
      center: sfBayCoords,
      zoom: 11,
    });

    const searchButton = document.querySelector("#search-button");
    searchButton.addEventListener('click', () => {
       
      //document.querySelector("#search-title").innerHTML = "Activities for";
      const searchLocation = document.querySelector("#search-location").value;
      const searchExperience = document.querySelector("#search-for-experience").value;
      const displaySearch = document.querySelector("#display-search");
      
      //Empty search display panel before displaying new search results.
      displaySearch.innerHTML = "";
  
      const queryString = new URLSearchParams({ location: `${searchLocation}`, experience: `${searchExperience}`}).toString();
      const url = `/search-results?${queryString}`;
      let latLongDict = [];
      //Making a fetch request to server from DOM search textbox value and display the parsed data in the #display-search section of search.html page.
      fetch(url)
        .then((response) => response.text())
        .then((searchResultsJson) => {
          //parsing the text formated JSON 
          const parsedResults = JSON.parse(searchResultsJson);

          //The returned parsed JSON is a list of dict, so looping over each element in the list starting from 0th index
          for(let index = 0; index < parsedResults.length; index++) {

            //storing all the required data in const variables that are returned from the fetch request in the form of dict of dicts 

            //storing location coordinates in this dict to use for pinning the markers
            const latLong = {}

            const name = parsedResults[index]["name"];
            latLong["name"] = name;
            const expUrl = parsedResults[index]["url"];
            latLong["expUrl"] = expUrl;
            const imageUrl = parsedResults[index]["image_url"]
            latLong["image"] = imageUrl;
            const reviews = parsedResults[index]["review_count"];
            const location = parsedResults[index]["location"]["display_address"];
            latLong["location"] = location;
            const latitude = parsedResults[index]["coordinates"]["latitude"];
            
            latLong["latitude"] = latitude;
            const longitude = parsedResults[index]["coordinates"]["longitude"];

            latLong["longitude"] = longitude;
            latLongDict.push(latLong);
          
            
            displaySearch.insertAdjacentHTML('beforeend', `<b><a href=${expUrl} target="_blank">${name}</a><br><br></b>`);
            displaySearch.insertAdjacentHTML('beforeend', `<img src=${imageUrl} width="300" height="300">`);
            displaySearch.insertAdjacentHTML('beforeend', `<li>Reviews: ${reviews}</li>`);
            displaySearch.insertAdjacentHTML('beforeend', `<li>Location: ${location}</li>`);
            displaySearch.insertAdjacentHTML('beforeend', `<li>Latitude: ${latitude}</li>`);
            displaySearch.insertAdjacentHTML('beforeend', `<li>Longitude: ${longitude}</li><br>`);

            displaySearch.insertAdjacentHTML('beforeend', `<button id="add-itinerary-btn${index}">Add to Itinerary</button><br><br>`);
            
            const addItineraryBtn = document.querySelector(`#add-itinerary-btn${index}`);

            addItineraryBtn.addEventListener("click", (evt) => {
              const queryString = new URLSearchParams({name: `${name}`,expUrl: `${expUrl}`, image: `${imageUrl}`,location: `${location}`, latitude: `${latitude}`, longitude: `${longitude}`}).toString();
              const url = `/load-itinerary?${queryString}`;

              addItineraryBtn.disabled = true;
              
              document.querySelector("#finish-itinerary").disabled = false;
              fetch(url)
                .then((response) => response.text())
                .then((response) => {
                    console.log(response);
                });
            }); 
          }
        //calling this function to place markers on the map and passing dict of coords
        addMarkers(latLongDict);

        displaySearch.insertAdjacentHTML('beforeend', `<button id="finish-itinerary">Finish</button><br><br>`);
        const finishBtn = document.querySelector("#finish-itinerary");finishBtn.disabled = true;
    
        finishBtn.addEventListener('click', () => {
          location.assign("/view-itineraries");
        });
      });          
    });

  function addMarkers(latLongDict) {
    for(const marker of markers) {
      marker.setMap(null);
  }

    markers = [];

    //instatiating info window
    const locationInfo = new google.maps.InfoWindow({maxWidth: 200});

  //puting the markers on map
    for(let index in latLongDict) {
      const coords = {
        lat: latLongDict[index]["latitude"],
        lng: latLongDict[index]["longitude"],
      }
      basicMap.setCenter(coords); //Here center the map.

      markers.push(
        new google.maps.Marker({
          position: coords,
          title: latLongDict[index]["name"],
          expUrl: latLongDict[index]["expUrl"],
          image: latLongDict[index]["image"],
          location: latLongDict[index]["location"],
          map: basicMap,
      }),
      );
  }

 

  //Content to put in the marker infoWindow
    for (const marker of markers) {
      const markerInfoContent = `
        <b>
          <p>
            <a href=${marker.expUrl}target="_blank">${marker.title}</a>
          </p>
        </b>
        <div text-align:center>
          <img src=${marker.image} width="165" height="100">
        </div>
        <p>
          Address:
            <code>${marker.location}.</code><br>
        </p>
        <p>
          Located at: 
            <code>${marker.position.lat()}</code>,
            <code>${marker.position.lng()}</code>
        </p>
      `;

      //eventListner for marker clicks
      marker.addListener('click', () => {
        //closes previous infoWindow
        locationInfo.close();
        locationInfo.setContent(markerInfoContent)
        locationInfo.open(basicMap, marker);

      });  
    }      
  }
}

