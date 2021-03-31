window.onload = function() {
    initWeather();
    initStands();
};

function initStands() {
  fetch("/bike_stand_query").then(response => {
    return response.json();
  }).then(data => {
    console.log("data: ", data);

  result = "<div style='text-align: left;'><h2>Current Availability</h2>";

  var checker = false;

  data.forEach(availability => {

    if (availability.available_bikes==0) {
      if (checker==false) {
        result += "<div class='stand_status'><h3>Empty Stations</h3><div style='background-color: red;'>";
        checker = true;
      }
      result += "<p>"+availability.name+"</p>";      
    }
  });

  if (checker==true) {
    result += "</div>";
  } else {
    result += "<p>No Empty Stands</p>";
  }
  result += "</div>";


  


  var checker = false;

  data.forEach(availability => {

    if (availability.available_bike_stands==0) {
      if (checker==false) {
        result += "<div class='stand_status'><h3>Full Stations</h3><div style='background-color: green;'>";
        checker = true;
      }
      result += "<p>"+availability.name+"</p>";      
    }
  });

  if (checker==true) {
    result += "</div>";
  } else {
    result += "<p>No Full Stands</p>";
  }
  result += "</div>";



  var checker = false;

  data.forEach(availability => {

    if (availability.available_bikes<=3) {
      if (checker==false) {
        result += "<div class='stand_status'><h3>Nearly Empty Stations</h3><div style='background-color: green;'>";
        checker = true;
      }
      result += "<p>"+availability.name+"</p>";      
    }
  });

  if (checker==true) {
    result += "</div>";
  } else {
    result += "<p>No Nearly Empty Stands</p>";
  }
  result += "</div>";






  var checker = false;

  data.forEach(availability => {

    if (availability.available_bike_stands<=3) {
      if (checker==false) {
        result += "<div class='stand_status'><h3>Nearly Full Stations</h3><div style='background-color: green;'>";
        checker = true;
      }
      result += "<p>"+availability.name+"</p>";      
    }
  });

  if (checker==true) {
    result += "</div>";
  } else {
    result += "<p>No Nearly Empty Stands</p>";
  }
  result += "</div>";


  
  document.getElementById("stands").innerHTML = result;

  }).catch(err => {
    console.log("OOPS!", err);
  })
}










function initWeather() {
    fetch("/home_weather_query").then(response => {
      return response.json();
    }).then(data => {
      console.log("data: ", data);

    result = "<div style='text-align: left;'><h2>  Current Weather</h2><iframe src='https://free.timeanddate.com/clock/i7qn1g4m/n78/tlie/ftb/tt0/tw1/tm1/th1/tb4' frameborder='0' width='121' height='34'></iframe>";

    result += "<table id='weaterTable'></table>"

    data.forEach(weather => {
      var icon = weather.WeatherIcon;
      var iconPic = "<img class='loading' src='static/weatherIcons/"+icon+".gif'>";
      var iconList = [1, 2, 3, 4, 6, 7, 11, 12, 13,14, 18, 34, 35, 36, 38, 40];

      result += "<p>Temperature: " + weather.Temperature + "ºC</p>";
      result += "<p>Real Feel Temperature: " + weather.RealFeelTemperature + "ºC</p>";
      if (iconList.includes(icon)==true) {
        result += iconPic;
      } else {
        result += "<img class='loading' src='static/weatherIcons/unknown.gif'>";
      }
      result += weather.IconPhrase;
      result += "<p>Icon: " + icon + "</p>";
      result += "<p>Precipitation Probability: " + weather.PrecipitationProbability + "</p>";
      result += "<p>Rain: " + weather.Rain + "</p>";
      result += "<p>Relative Humidity: " + weather.RelativeHumidity + "</p>";
      result += "<p>Wind Speed: " + weather.WindSpeed + "</p>";
    });
    
    result += "</div>"
      
    
    document.getElementById("weather").innerHTML = result;

    }).catch(err => {
      console.log("OOPS!", err);
    })
  }
  