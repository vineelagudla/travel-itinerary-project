

let publicItnCount = 0;
let itnCount = 0;

const url = "/public-itineraries-list";
fetch(url)
    .then((response) => response.text())
    .then((publicItineraries) => {
        const publicItns = JSON.parse(publicItineraries);
        const mySlider = document.querySelector("#itn-slider");

        publicItnCount = publicItns.length;
        mySlider.innerHTML = "";

        for (const itn of publicItns) {
            const itnId = itn["itn_id"];
            const queryString = new URLSearchParams({ itnId: `${itnId}` }).toString();
            const itnInfoUrl = `/get-experiences-carousel?${queryString}`;
            fetch(itnInfoUrl)
                .then((response) => response.text())
                .then((itnInfoResultsJson) => {
                    const itnInfo = JSON.parse(itnInfoResultsJson);
                    const itnName = itnInfo["itn_name"];
                    let destintation = "";

                    let imgUrl = "https://t3.ftcdn.net/jpg/02/48/42/64/360_F_248426448_NVKLywWqArG2ADUxDq6QprtIzsF82dMF.jpg";
                    if (itnInfo["experiences"].length != 0) {
                        const image = itnInfo["experiences"][0]["exp_image"];
                        if (image != null) imgUrl = image;
                        destintation = (itnInfo["experiences"][0]["dest_name"]).split(",");
                        console.log(destintation);
                        destintation = destintation[destintation.length - 2];
                    }

                    mySlider.insertAdjacentHTML('beforeend', `<div><div class="slide"><div class="slide-img"><a href="show_itinerary?itn_id=${itnId}"><img src="${imgUrl}" width="230" height="130"></a> </div><br><div><h6><a href="show_itinerary?itn_id=${itnId}">${itnName}</a></h6><h5>${destintation}</h5></div></div></div>`);

                    itnCount++;
                    if (itnCount >= publicItnCount) {
                        let slider = tns({
                            container: ".my-slider",
                            "slideBy": 1,
                            "speed": 400,
                            "nav": false,
                            "autoplay": true,
                            "autoplayTimeout": 2000,
                            "autoplayButtonOutput": false,
                            controlsContainer: "#controls",
                            prevButton: ".previous",
                            nextButton: ".next",
                            responsive: {
                                1600: {
                                    items: 4,
                                },
                                1024: {
                                    items: 4,
                                },
                                768: {
                                    items: 2,
                                },
                                480: {
                                    items: 1,
                                }
                            }
                        });
                    }
                });
        }
    });



