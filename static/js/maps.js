function initMap() {
    const sfBayCoords = {
        lat: 37.601773,
        lng: -122.20287,
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
