let map;

  function initMap() {
  fetch("/stations").then(response => {
    return response.json();
    }).then(data => {
      console.log("data: ", data);


    map = new google.maps.Map(document.getElementById("map") as HTMLElement, {
      center: { lat: 53.349804, lng: -6.260310 },
      zoom: 14,
    });

    data.forEach(station => {
        const marker = new google.maps.Marker({
          position: { lat: station.pos_lat, lng: station.pos_lng},
          label: station.name
          map: map,
        });
        marker.addListener("click", () => {
          const infowindow = new google.maps.Infowindow({
            content: '<h1>'+ station.name + '<h1><br><h3>Bikes available<h3>'+ station.bike_stands + '</b>',
           });
          infowindow.open(map, marker);
         });
    });


    }).catch(err => {
    console.log("OOPS!", err);
    })
   }
