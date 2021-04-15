window.onload = function() {
    initWeather();
    initStands();
};

/* Function to display the names of stands that are full, nearly full, empty, or nearly empty.
// It will also display a warning for closed stations.
// Stations are designated nearly empty/full if there are between 1 and 3 bikes/availbe stands there. 
*/
function initStands() {
  fetch("/bike_stand_query").then(response => {
    return response.json();
  }).then(data => {
    console.log("data: ", data);

  result = "<div id='CA'>";

  result += "<div class='TES'>"

  var checker = false;


  // Generation of warning if any statiosn are CLOSED
  data.forEach(availability => {

    if (availability.status != "OPEN") {
      if (checker==false) {
        result += "<div class='closed'><h3><u>Closed Stations</u>&nbsp;</h3><div class='SLC'>";
        checker = true;
      }
      result += "<p>"+availability.name+"</p>";      
    }
  });

  if (checker==true) {
    result += "</div></div>";
    result += "</div><div class='line'></div>";
    checker = false;
  }

  result += "</div></div>";

  
  /* The following will generate divs for full/empty and nearly full/empty
  // This code can be optimised to work only looping throught the data once instead of four times but creates legability issues for anyone working on the code.
  */

  // Generate and populate div for empty stations
  data.forEach(availability => {

    if (availability.available_bikes==0) {
      if (checker==false) {
        result += "<div class='stand_status'><h3><u>Empty Stations</u></h3>&nbsp;<div class='SL'>";
        checker = true;
      }
      result += "<p>"+availability.name+"</p>";      
    }
  });

  if (checker==true) {
    result += "</div></div>";
    checker = false;
  }

  // Generate and populate div for nearly empty stations
  data.forEach(availability => {

    if (availability.available_bikes<=3 && availability.available_bikes!=0) {
      if (checker==false) {
        result += "<div class='stand_status'><h3><u>Nearly Empty Stations</u></h3>&nbsp;<div class='SL'>";
        checker = true;
      }
      result += "<p>"+availability.name+"</p>";      
    }
  });

  if (checker==true) {
    result += "</div></div>";
    checker = false;
  }

  result += "</div><div class='line'></div><div class='TES'>"

  // Generate and populate div for full stations
  data.forEach(availability => {

    if (availability.available_bike_stands==0) {
      if (checker==false) {
        result += "<div class='stand_status'><h3><u>Full Stations</u>&nbsp;</h3><div class='SL'>";
        checker = true;
      }
      result += "<p>"+availability.name+"</p>";      
    }
  });

  if (checker==true) {
    result += "</div></div>";
    checker = false;
  }


  // Generate and populate div for nearly full stations
  data.forEach(availability => {

    if (availability.available_bike_stands<=3 && availability.available_bike_stands!=0) {
      if (checker==false) {
        result += "<div class='stand_status'><h3><u>Nearly Full Stations</u>&nbsp;</h3><div class='SL'>";
        checker = true;
      }
      result += "<p>"+availability.name+"</p>";      
    }
  });

  if (checker==true) {
    result += "</div></div>";
    checker = false;
  }

  result += "</div></div>";

  

  
  document.getElementById("stands").innerHTML = result;
  document.getElementById("loading_box").innerHTML = '';

  }).catch(err => {
    console.log("OOPS!", err);
  })
}









// Function to generate weather widget
function initWeather() {
    fetch("/home_weather_query").then(response => {
      return response.json();
    }).then(data => {
      console.log("data: ", data);

    // This line generates the active clock for the weather widget.
    result = "<div class='icon_phrase'><iframe src='https://free.timeanddate.com/clock/i7qvq4vq/n78/tlie/fs16/tct/pct/ftb/tt0/tw1/tm1/tb2' frameborder='0' width='205' height='20' allowtransparency='true'></iframe></div><br>";

    // This section will check what the icon code for the current weather is and check it against a list of icon codes we have seen to date, and prepared gifs for. If a weather icon code appears we havent seen bofore a gif to say as such is displayed instead.
    data.forEach(weather => {
      var icon = weather.WeatherIcon;
      var iconList = [1, 2, 3, 4, 6, 7, 11, 12, 13,14, 18, 34, 35, 36, 38, 40];

      if (iconList.includes(icon)==true) {
        var iconPic = "<img class='icon_gif' src='static/weatherIcons/"+icon+".gif'>";
        result += iconPic;
      } else {
        result += "<img class='icon_gif' src='static/weatherIcons/unknown.gif'>";
      }
      result += "<br><br><h3 class='icon_phrase'>"+weather.IconPhrase+"</h3>";

      result += "<div class='line'></div><div class='TES'>";


      // This section displays the current temperature on a backgroud that adjusts depending on the temperature.
      if (weather.Temperature >= 15) {
        result += "<div class='float_box2' style='background-image: linear-gradient(to right, #87baff, #87baff, red)'><p>Temperature: ";
      } else if (weather.Temperature >=7) {
        result += "<div class='float_box2' style='background-image: linear-gradient(to right, #87baff, #87baff, orange)'><p>Temperature: ";
      } else {
        result += "<div class='float_box2' style='background-image: linear-gradient(to right, #87baff, #87baff, blue)'><p>Temperature: ";
      }
      result += weather.Temperature + "ºC</p></div>";


      // This section displays the real feel temperature on a backgroud that adjusts depending on the real feel temperature.
      if (weather.RealFeelTemperature >= 15) {
        result += "<div class='float_box2' style='background-image: linear-gradient(to right, #87baff, #87baff, red)'><p>Real Feel Temperature: ";
      } else if (weather.RealFeelTemperature >=7) {
        result += "<div class='float_box2' style='background-image: linear-gradient(to right, #87baff, #87baff, orange)'><p>Real Feel Temperature: ";
      } else {
        result += "<div class='float_box2' style='background-image: linear-gradient(to right, #87baff, #87baff, blue)'><p>Real Feel Temperature: ";
      }
      result += weather.RealFeelTemperature + "ºC</p></div>";

      // This displays the current humidity and windspeed
      result += "<div class='float_box2'><p>Relative Humidity: " + weather.RelativeHumidity + "%</p></div>";
      result += "<div class='line'></div>";
      result += "<div class='float_box2'><p>Wind Speed: " + weather.WindSpeed + "kph</p></div>";

      // This section displays the cloud cover on a backgroud that adjusts depending on the current cloud cover.
      var cc = weather.CloudCover;
      if (cc==0) {
        result += "<div class='float_box2'><p>Cloud Cover: " + cc + "%</p></div>";
      } else if (cc<20) {
        result += "<div class='float_box2' style='background-image: linear-gradient(rgba(169, 169, 169, 0.2), #87baff);'><p>Cloud Cover: " + cc + "%</p></div>";
      } else if (cc<40) {
        result += "<div class='float_box2' style='background-image: linear-gradient(rgba(169, 169, 169, 0.4), #87baff);'><p>Cloud Cover: " + cc + "%</p></div>";        
      } else if (cc<60) {
        result += "<div class='float_box2' style='background-image: linear-gradient(rgba(169, 169, 169, 0.6), #87baff);'><p>Cloud Cover: " + cc + "%</p></div>";
      } else if (cc<80) {
        result += "<div class='float_box2' style='background-image: linear-gradient(rgba(169, 169, 169, 0.8), #87baff);'><p>Cloud Cover: " + cc + "%</p></div>";
      } else {
        result += "<div class='float_box2' style='background-image: linear-gradient(rgba(169, 169, 169, 1), #87baff);'><p>Cloud Cover: " + cc + "%</p></div>";
      }
      result += "<div class='line'></div>";


      /* This section displays the precipitation probability on a backgroud that adjusts depending on the current precipitation probability.
      // It will also display the rain informaion only if either precipitation probability and rain is above 0.
      */
      var pp = weather.PrecipitationProbability;
      if (pp==0) {
        result += "<div class='float_box2'><p>Precipitation Probability: " + pp + "%</p></div>";
      } else if (weather.PrecipitationProbability<10) {
        result += "<div class='float_box2'  style='background-image: linear-gradient(blue, #87baff, #87baff, #87baff, #87baff, #87baff, #87baff, #87baff, #87baff, #87baff, #87baff)'><p>Precipitation Probability: " + pp + "%</p></div>";
      } else if (weather.PrecipitationProbability<20) {
        result += "<div class='float_box2'  style='background-image: linear-gradient(blue, blue, #87baff, #87baff, #87baff, #87baff, #87baff, #87baff, #87baff, #87baff, #87baff)'><p>Precipitation Probability: " + pp + "%</p></div>";
      } else if (weather.PrecipitationProbability<30) {
        result += "<div class='float_box2'  style='background-image: linear-gradient(blue, blue, blue, #87baff, #87baff, #87baff, #87baff, #87baff, #87baff, #87baff, #87baff)'><p>Precipitation Probability: " + pp + "%</p></div>";
      } else if (weather.PrecipitationProbability<40) {
        result += "<div class='float_box2'  style='background-image: linear-gradient(blue, blue, blue, blue, #87baff, #87baff, #87baff, #87baff, #87baff, #87baff, #87baff)'><p>Precipitation Probability: " + pp + "%</p></div>";
      } else if (weather.PrecipitationProbability<50) {
        result += "<div class='float_box2'  style='background-image: linear-gradient(blue, blue, blue, blue, blue, #87baff, #87baff, #87baff, #87baff, #87baff, #87baff)'><p>Precipitation Probability: " + pp + "%</p></div>";
      } else if (weather.PrecipitationProbability<60) {
        result += "<div class='float_box2'  style='background-image: linear-gradient(blue, blue, blue, blue, blue, blue, #87baff, #87baff, #87baff, #87baff, #87baff)'><p>Precipitation Probability: " + pp + "%</p></div>";
      } else if (weather.PrecipitationProbability<70) {
        result += "<div class='float_box2'  style='background-image: linear-gradient(blue, blue, blue, blue, blue, blue, blue, #87baff, #87baff, #87baff, #87baff)'><p>Precipitation Probability: " + pp + "%</p></div>";
      } else if (weather.PrecipitationProbability<80) {
        result += "<div class='float_box2'  style='background-image: linear-gradient(blue, blue, blue, blue, blue, blue, blue, blue, #87baff, #87baff, #87baff)'><p>Precipitation Probability: " + pp + "%</p></div>";
      } else if (weather.PrecipitationProbability<90) {
        result += "<div class='float_box2'  style='background-image: linear-gradient(blue, blue, blue, blue, blue, blue, blue, blue, blue, #87baff, #87baff)'><p>Precipitation Probability: " + pp + "%</p></div>";
      } else if (weather.PrecipitationProbability<100) {
        result += "<div class='float_box2'  style='background-image: linear-gradient(blue, blue, blue, blue, blue, blue, blue, blue, blue, blue, #87baff)'><p>Precipitation Probability: " + pp + "%</p></div>";
      } else {
        result += "<div class='float_box2'  style='background-image: linear-gradient(blue, blue, blue, blue, blue, blue, blue, blue, blue, blue, blue)'><p>Precipitation Probability: " + pp + "%</p></div>";
      }
      if (weather.rain!=0 && weather.PrecipitationProbability!=0) {
        result += "<div class='float_box2'><p>Rain: " + weather.Rain + "mm</p></div>";
      }
      
    });
    
    
      
    
    document.getElementById("weather").innerHTML = result;

    }).catch(err => {
      console.log("OOPS!", err);
    })
  }
  