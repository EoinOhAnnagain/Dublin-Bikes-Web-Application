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
