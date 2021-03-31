let map;
let marker;

function initCharts() {
    google.charts.load('current', {'packages': ['corechart']});
    google.charts.setOnLoadCallback(initMap);
}

function iconPicker(percentage) {

    if (percentage === 0) {
        return "http://maps.google.com/mapfiles/ms/micons/red-dot.png";
    } else if (percentage < 0.25) {
        return "http://maps.google.com/mapfiles/ms/micons/orange-dot.png";
    } else if (percentage < 0.50) {
        return "http://maps.google.com/mapfiles/ms/micons/yellow-dot.png";
    } else {
        return "http://maps.google.com/mapfiles/ms/micons/green-dot.png";
    }
}



function initMap() {

fetch("/stationsquery").then(response => {
    return response.json();
    }).then(data => {
      console.log("data: ", data);

  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 53.349804, lng: -6.260310 },
    zoom: 14,
  });

  //creating a single infowindow to be used for information display
  const infowindow = new google.maps.InfoWindow({
    content: ''

  });

  //for loop to place markers for each station on the map
  data.forEach(station => {
    const marker = new google.maps.Marker({
        position: { lat: station.pos_lat, lng: station.pos_lng },
        map: map,
        animation: google.maps.Animation.DROP,
        icon: iconPicker(station.available_bikes/station.bike_stands),
    });

    //on click listener that sets the content of the info window to that of the relevant marker
    marker.addListener("click",  () => {



    //updating marker content
    infowindow.setContent("<div class='map_info_div'><h2>"+ station.name + "<h2><h3>Bikes available: "+ station.available_bikes +"<h3>"+
        "<h3>Free stands available: "+ station.available_bike_stands +"<h3>"+
        "<h3>Station status: "+ station.status +"<h3></div>"+
        '</b>');

    //opening the infowindow o
    infowindow.open(map,marker);
    console.log('calling drawOccupancyWeekly' + station.number);
    drawOccupancyWeekly(station.number);
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

          const marker = new google.maps.Marker({
            position: { lat: position.coords.latitude, lng: position.coords.longitude },
            map: map,
            animation: google.maps.Animation.DROP,
            icon: "http://maps.google.com/mapfiles/ms/micons/cycling.png",
          });

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

function drawOccupancyWeekly(station_number) {
    // this is called when the user clicks on the marker
    // use google charts to draw a chart at the bottom of the page

    fetch("/occupancy/" + station_number).then(response => {
        return response.json();
    }).then(data => {
        console.log(data);

        var options = {
            title: data[0].name + " Bike Availability per day",

        }

        var chart = new google.visualization.ColumnChart(document.getElementById('chart1'));
        var chart_data = new google.visualization.DataTable();
        chart_data.addColumn('datetime', "Date");
        chart_data.addColumn('number', 'Bike Availability');
        data.forEach(v => {
          var rounded = Math.round(v.available_bikes);
            chart_data.addRow( [new Date(v.last_update), rounded]);
        })
        chart.draw(chart_data, options);
    });


    fetch("/occupancy/" + station_number).then(response => {
        return response.json();
    }).then(data => {
        console.log(data);

        var options = {
            title: data[0].name + " Bike Stand Availability per day",

        }

        var chart = new google.visualization.ColumnChart(document.getElementById('chart2'));
        var chart_data = new google.visualization.DataTable();
        chart_data.addColumn('datetime', "Date");
        chart_data.addColumn('number', 'Bike Stand Availability');
        data.forEach(v => {
          var rounded = Math.round(v.available_bike_stands);
            chart_data.addRow( [new Date(v.last_update), rounded]);
        })
        chart.draw(chart_data, options);
    });
}

