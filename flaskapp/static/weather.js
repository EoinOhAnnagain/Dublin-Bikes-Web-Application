window.onload = function() {
    initWeather();
};

function initWeather() {
    fetch("/home_weather_query").then(response => {
      return response.json();
    }).then(data => {
      console.log("data: ", data);

    result = "<div style='text-align: left;'><h2>  Current Weather</h2><iframe src='https://free.timeanddate.com/clock/i7qk59en/n78/tlie/tt0/tw1/tm1' frameborder='0' width='182' height='18'></iframe>";

    result += "<table id='weaterTable'></table>"

    data.forEach(weather => {
      var temp = weather.Temperature;
      var RFTemp = weather.RealFeelTemperature;
      var icon = weather.WeatherIcon;
      var iconPic = "<img class='loading' src='static/weatherIcons/"+icon+".gif'>";
      var iconPhrase = weather.IconPhrase;
      var pp = weather.PrecipitationProbability;
      var rain = weather.Rain;
      var humid = weather.RelativeHumidity;
      var wind = weather.WindSpeed;
      var iconList = [1, 2, 3, 4, 6, 7, 11, 12, 13,14, 18, 34, 35, 36, 38, 40];

      result += "<p>Temperature: " + temp + "ºC</p>";
      result += "<p>Real Feel Temperature: " + RFTemp + "ºC</p>";
      if (iconList.includes(icon)==true) {
        result += iconPic;
      } else {
        result += "<img class='loading' src='static/weatherIcons/unknown.gif'>";
      }
      result += iconPhrase;
      result += "<p>Icon: " + icon + "</p>";
      result += "<p>Precipitation Probability: " + pp + "</p>";
      result += "<p>Rain: " + rain + "</p>";
      result += "<p>Relative Humidity: " + humid + "</p>";
      result += "<p>Wind Speed: " + wind + "</p>";
    });
    
    result += "</div>"
      
    
    document.getElementById("weather").innerHTML = result;

    }).catch(err => {
      console.log("OOPS!", err);
    })
  }
