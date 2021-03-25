let map;

function initMap() {

fetch("/mapquery").then(response => {
    return response.json();
    }).then(data => {
      console.log("data: ", data);

  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 53.349804, lng: -6.260310 },
    zoom: 14,
  });

  data.forEach(station => {
    const marker = new google.maps.Marker({
        position: { lat: station.pos_lat, lng: station.pos_lng },
        map: map,
    });
    marker.addListener("click", () => {
    const infowindow = new google.maps.InfoWindow({
        content: station.name,
    });
    infowindow.open(map,marker);
  });
  });

  infoWindow = new google.maps.InfoWindow();
  const locationButton = document.createElement("button");
  locationButton.textContent = "Pan to Current Location";
  locationButton.classList.add("custom-map-control-button");
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);
  locationButton.addEventListener("click", () => {

    // Trying  HTML5 geolocation.

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          };
          infoWindow.setPosition(pos);
          infoWindow.setContent("Location found.");
          infoWindow.open(map);
          map.setCenter(pos);
        },
        () => {
          handleLocationError(true, infoWindow, map.getCenter());
        }
      );
    } else {
      // Browser doesn't support Geolocation
      handleLocationError(false, infoWindow, map.getCenter());
    }
  });


}).catch(err => {
    console.log("OOPS!", err);
    })

 }

 function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(
    browserHasGeolocation
      ? "Error: The Geolocation service failed."
      : "Error: Your browser doesn't support geolocation."
  );
  infoWindow.open(map);
}

