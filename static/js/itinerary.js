'use strict';

//JS for displaying search results after clicking on search button.
const searchButton = document.querySelector("#search-button");
searchButton.addEventListener('click', () => {
    document.querySelector("#search-title").innerHTML = "Activities for";
    const searchLocation = document.querySelector("#search-location").value;
    const displaySearch = document.querySelector("#display-search");

    //Empty search display panel before displaying new search results.
    displaySearch.innerHTML = "";

    const queryString = new URLSearchParams({ location: `${searchLocation}`}).toString();
    const url = `/search-results?${queryString}`;

    //Making a fetch request to server from DOM search textbox value and display the parsed data in the #display-search section of search.html page.
    fetch(url)
        .then((response) => response.text())
        .then((searchResultsJson) => {
            //parsing the text formated JSON 
            const parsedResults = JSON.parse(searchResultsJson);

            //The returned parsed JSON is a list of dict, so looping over each element in the list starting from 0th index
            for(let index = 0; index < parsedResults.length; index++) {

                //storing all the required data in const variables that are returned from the fetch request in the form of dict of dicts 
                const name = parsedResults[index]["name"];
                const exp_url = parsedResults[index]["url"];
                const reviews = parsedResults[index]["review_count"];
                const location = parsedResults[index]["location"]["display_address"];
                const latitude = parsedResults[index]["coordinates"]["latitude"];
                const longitude = parsedResults[index]["coordinates"]["longitude"];

                
                displaySearch.insertAdjacentHTML('beforeend', `<b><a href=${exp_url} target="_blank">${name}</a><br></b>`);
                displaySearch.insertAdjacentHTML('beforeend', `<li>Reviews: ${reviews}</li>`);
                displaySearch.insertAdjacentHTML('beforeend', `<li>Location: ${location}</li>`);
                displaySearch.insertAdjacentHTML('beforeend', `<li>Latitude: ${latitude}</li>`);
                displaySearch.insertAdjacentHTML('beforeend', `<li>Longitude: ${longitude}</li><br>`);
                displaySearch.insertAdjacentHTML('beforeend', `<button id="add-itinerary-btn${index}">Add to Itinerary</button><br><br>`);
                
                const addItineraryBtn = document.querySelector(`#add-itinerary-btn${index}`);
                console.log(addItineraryBtn);
                addItineraryBtn.addEventListener("click", (evt) => {
                    const queryString = new URLSearchParams({name: `${name}`, location: `${location}`, latitude: `${latitude}`, longitude: `${longitude}`}).toString();
                    const url = `/load-itinerary?${queryString}`;
                    
                    document.getElementById(`add-itinerary-btn${index}`).disabled = true;

                    fetch(url)
                    .then((response) => response.text())
                    .then((response) => {
                        console.log(response);
                    });
                }); 
            }
            displaySearch.insertAdjacentHTML('beforeend', `<button id="finish-itinerary">Finish</button><br><br>`);
            const finishBtn = document.querySelector("#finish-itinerary");

            finishBtn.addEventListener('click', () => {
                location.assign("/dashboard");
            });
        });
});

