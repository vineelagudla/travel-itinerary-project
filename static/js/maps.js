
let latLongDict = [];
const searchButton1 = document.querySelector("#search-button");
function testDict() {

    searchButton1.addEventListener('click', () => {
        //document.querySelector("#search-title").innerHTML = "Activities for";
        const searchLocation = document.querySelector("#search-location").value;
        const searchExperience = document.querySelector("#search-for-experience").value;
        const displaySearch = document.querySelector("#display-search");
        
        

        //Empty search display panel before displaying new search results.
        displaySearch.innerHTML = "";
    
        const queryString = new URLSearchParams({ location: `${searchLocation}`, experience: `${searchExperience}`}).toString();
        const url = `/search-results?${queryString}`;

        //Making a fetch request to server from DOM search textbox value and display the parsed data in the #display-search section of search.html page.
        fetch(url)
            .then((response) => response.text())
            .then((searchResultsJson) => {
                //parsing the text formated JSON 
                const parsedResults = JSON.parse(searchResultsJson);

                //The returned parsed JSON is a list of dict, so looping over each element in the list starting from 0th index
                for(let index = 0; index < parsedResults.length; index++) {
                    latLong = {}
                    const latitude = parsedResults[index]["coordinates"]["latitude"];
                    latLong["latitude"] = latitude;
                    const longitude = parsedResults[index]["coordinates"]["longitude"];
                    latLong["longitude"] = longitude;
                    latLongDict.push(latLong);
                }
                console.log(latLongDict);

                
                initMap();
            });

        });
    }

testDict();


function initMap() {
    const sfBayCoordsold = {
        lat: 37.5,
        lng: -121.6
      };
      const sfBayCoords = {
        lat: latLongDict[1]["latitude"],
        lng: latLongDict[1]["longitude"],
    };
      
      const basicMap = new google.maps.Map(document.querySelector('#map'), {
        center: sfBayCoords,
        zoom: 11,
      });

      const sfMarker = new google.maps.Marker({
        position: sfBayCoords,
        title: 'SF Bay',
        map: basicMap,
      });
      
}
