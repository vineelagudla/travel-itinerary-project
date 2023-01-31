'use strict';

const searchButton = document.querySelector("#search-button");
searchButton.addEventListener('click', () => {
    const searchLocation = document.querySelector("#search-location").value;
    const displaySearch = document.querySelector("#display-search");
    const queryString = new URLSearchParams({ location: `${searchLocation}`}).toString();
    const url = `/search-results?${queryString}`;

    fetch(url)
        .then((response) => response.text())
        .then((searchResultsJson) => {
            const parsedResults = JSON.parse(searchResultsJson);
            for(let index = 0; index < parsedResults.length; index++) {
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
            });
});
