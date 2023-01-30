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
                    const reviews = parsedResults[index]["review_count"];
                    const location = parsedResults[index]["location"]["display_address"];
                    const latitude = parsedResults[index]["coordinates"]["latitude"];
                    const longitude = parsedResults[index]["coordinates"]["longitude"];

                    displaySearch.insertAdjacentHTML('beforeend', `<b>${name}<br></b>`);
                    displaySearch.insertAdjacentHTML('beforeend', `<li>Reviews: ${reviews}</li>`);
                    displaySearch.insertAdjacentHTML('beforeend', `<li>Location: ${location}</li>`);
                    displaySearch.insertAdjacentHTML('beforeend', `<li>Latitude: ${latitude}</li>`);
                    displaySearch.insertAdjacentHTML('beforeend', `<li>Longitude: ${longitude}</li><br>`);
                    displaySearch.insertAdjacentHTML('beforeend', `<button type="button">Add to Itinerary</button><br><br>`);
                }
            });
});