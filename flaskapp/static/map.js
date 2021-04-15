let map;
let marker;

window.onload = function() {
    Predictor();
    populateDirectionSelection()
    populateDirectionSelection2()
};

function calculateAndDisplayRoute(directionsService, directionsRenderer) {
// code sourced from: https://developers.google.com/maps/documentation/javascript/examples/directions-simple#maps_directions_simple-javascript

var originCoord = document.getElementById("originDropDown").value;
var destinationCoord = document.getElementById("destinationDropDown").value;

console.log(originCoord[0],originCoord[1],originCoord[0]);
console.log(destinationCoord[0],destinationCoord[0],destinationCoord[1]);
  directionsService.route(
    {
      origin: {
        query: document.getElementById("originDropDown").value,
      },
      destination: {
        query: document.getElementById("destinationDropDown").value,
      },
      travelMode: google.maps.TravelMode.DRIVING,
    },
    (response, status) => {
      if (status === "OK") {
        directionsRenderer.setDirections(response);
      } 
    }
  );
}

function populateDirectionSelection() {
// used to populate selection drop downs for routing

    //retrieving data
    fetch("/stationsquery").then(response => {
        return response.json();
        }).then(data => {
        console.log("data: ", data);





        data.forEach(station => {
            //adding option for ever station available
            var originDropDown = document.getElementById("originDropDown");

            var opt = document.createElement("option");

            //using an array here as creating latlng here generates an error
            opt.value = [station.pos_lat, station.pos_lng];
            opt.innerHTML = station.name;

            originDropDown.add(opt);
        });

    }).catch(err => {
        console.log("OOPS!", err);
    })
 }

 function populateDirectionSelection2() {
// used to populate selection drop downs for routing

    //retrieving data

    fetch("/stationsquery").then(response => {
        return response.json();
        }).then(data => {
        console.log("data: ", data);

        data.forEach(station => {
        //adding option for ever station available

            var destinationDropDown = document.getElementById("destinationDropDown");

            var opt = document.createElement("option");

            //using an array here as creating latlng here generates an error
            opt.value= [station.pos_lat, station.pos_lng];
            opt.innerHTML = station.name;

            destinationDropDown.add(opt);
        });

    }).catch(err => {
        console.log("OOPS!", err);
    })
 }

function displayDirectionsDiv() {
//used to display routing div as otherwise page gets overloaded
  var x = document.getElementById("directionsSelection");
  if (x.style.opacity === "0") {
    x.style.opacity = "1";
    x.style.height = "fit-content";
    x.style.padding = "1%";
    x.style.marginBottom = "1%";
  } else {
    x.style.opacity = "0";
    x.style.height = "0";
    x.style.padding = "0";
    x.style.marginBottom = "0";
    x.style.margintop = "0";
  }
}


function initCharts() {
    google.charts.load('current', {'packages': ['corechart']});
    google.charts.setOnLoadCallback(initMap);
}



function iconPicker(percentage) {
//choses which icon to use based on availability percentage
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
    clickableIcons: false,
  });

  //creating a single infowindow to be used for information display, allows to only ever have one open at a time
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
    infowindow.setContent("<div class='map_info_div' style='background-color: rgba(135,186,255,0.9); border-radius: 0px; margin: 1%; padding: 1%;'><h2>"+ station.name + "<h2><h3>Bikes available: "+ station.available_bikes +"<h3>"+
        "<h3>Free stands available: "+ station.available_bike_stands +"<h3>"+
        "<h3>Station status: "+ station.status +"<h3></div>"+
        '</b>');

    //opening the infowindow
    infowindow.open(map,marker);
    console.log('calling drawOccupancyWeekly' + station.number);
    drawOccupancyWeekly(station.number);
  });


  });

    //boiler plate directions code
    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map);

    const onChangeHandler = function () {
    calculateAndDisplayRoute(directionsService, directionsRenderer);
    };

    //picking up any changes to the station selected
    document.getElementById("originDropDown").addEventListener("change", onChangeHandler);
    document.getElementById("destinationDropDown").addEventListener("change", onChangeHandler);


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
 // standard geolocation code sourced from here: https://developers.google.com/maps/documentation/javascript/geolocation
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
            legend: 'none'

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
            legend: 'none'

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


// Function which predicts bike availability
function Predictor() {

    // populating stations dropdown menu
    fetch("/stationsquery").then(response => {
      return response.json();
    }).then(data => {
      console.log("data: ", data);

      result = "<form method=post action='/prediction'>" +
          "<label for='stations'>Select a station: </label>" +
      "<select name='a' id='selectedStation'>" +
      "<option value='' disabled selected>Select station</option><br>";

      data.forEach(station => {
        result += "<option value=" + station.number + ">" + station.name + "</option><br>";
     });
    result += "</select><br>"



    // populating date dropdown menu
    result += "<label for='dates'>Select a date: </label>" +
        "<select name='b' id='selectedDate'>" +
        "<option value='' disabled selected>select date</option><br>";

    for (var i = 0; i < 7; i++) {
        var date = new Date();
        date.setDate(date.getDate() + i);
        var dd = date.getDate();
        var mm = date.getMonth() + 1;
        var y = date.getFullYear();
        var weekDay = date.getDay();

        if (weekDay == 0) {
            formattedWeekday = 'Sun';
        }
        else if (weekDay == 1) {
            formattedWeekday = 'Mon';
        }
        else if (weekDay == 2) {
            formattedWeekday = 'Tue';
        }
        else if (weekDay == 3) {
            formattedWeekday = 'Wed';
        }
        else if (weekDay == 4) {
            formattedWeekday = 'Thu';
        }
        else if (weekDay == 5) {
            formattedWeekday = 'Fri';
        }
        else if (weekDay == 6) {
            formattedWeekday = 'Sat';
        }

    var formattedDate = dd + '/' + mm + '/' + y;

    result += "<option value=" + y + "-" + mm + "-" + dd + ">" + formattedWeekday + ' ' + formattedDate + "</option><br>";
    }
    result += "</select><br>";




    // populating time dropdown menu
    result += "<label for='times'>Select a time: </label>" +
              "<select name='c' id='selectedTime'>" +
              "<option value='' disabled selected>select time</option><br>";

      var date = new Date();
      date.setDate(date.getDate() );
      var dd = date.getDate();
      var mm = date.getMonth() + 1;
      var y = date.getFullYear();
      var h = date.getHours();

     // var chosenDate = document.getElementById('selectedDate').value;

    //  if (chosenDate == y + "-" + mm + "-" + dd) {
    //      for (var i=h*60; i<1400; i+=60) {
    //        var hours = Math.floor(i/60);
    //        var valueHours = Math.floor(i/60);
    //            if (hours < 10) {
    //                hours = '0' + hours;
    //            }
    //    result += "<option value=" + valueHours  + ">" + hours + ":" + "00" + "</option><br>";
   //   }
    //  }
    //  else {
          for (var i=0; i<1400; i+= 60) {
          var hours = Math.floor(i/60);
          var valueHours = Math.floor(i/60);
          if (hours < 10) {
            hours = '0' + hours;
        }
        result += "<option value=" + valueHours  + ">" + hours + ":" + "00" + "</option><br>";
      }

     // }
      result += "</select><br>";

    result += "<input type=submit value='submit'>" + "</form>";
    document.getElementById("predictor").innerHTML = result;

    })
}

function displayPredictionsDiv() {
//used to display routing div as otherwise page gets overloaded
  var x = document.getElementById("predictionSelection");
  if (x.style.opacity === "0") {
    x.style.opacity = "1";
    x.style.height = "fit-content";
    x.style.padding = "1%";
    x.style.marginBottom = "1%";
  } else {
    x.style.opacity = "0";
    x.style.height = "0";
    x.style.padding = "0";
    x.style.marginBottom = "0";
    x.style.margintop = "0";
  }
}