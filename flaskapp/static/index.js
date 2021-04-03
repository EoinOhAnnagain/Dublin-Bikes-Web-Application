window.onload = function() {
    initWeather();
    initStands();
};

function initStands() {
  fetch("/bike_stand_query").then(response => {
    return response.json();
  }).then(data => {
    console.log("data: ", data);

  result = "<div id='CA'>";

  result += "<div class='TES'>"

  var checker = false;


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










function initWeather() {
    fetch("/home_weather_query").then(response => {
      return response.json();
    }).then(data => {
      console.log("data: ", data);

    result = "<div class='icon_phrase'><iframe src='https://free.timeanddate.com/clock/i7qvq4vq/n78/tlie/fs16/tct/pct/ftb/tt0/tw1/tm1/tb2' frameborder='0' width='205' height='20' allowtransparency='true'></iframe></div><br>";

    
    data.forEach(weather => {
      var icon = weather.WeatherIcon;
      var iconPic = "<img class='loading' src='static/weatherIcons/"+icon+".gif'>";
      var iconList = [1, 2, 3, 4, 6, 7, 11, 12, 13,14, 18, 34, 35, 36, 38, 40];

  








      if (iconList.includes(icon)==true) {
        result += iconPic;
      } else {
        result += "<img class='loading' src='static/weatherIcons/unknown.gif'>";
      }
      result += "<h3 class='icon_phrase'>"+weather.IconPhrase+"</h3>";

      result += "<div class='line'></div><div class='TES'>";

      
      if (weather.Temperature >= 15) {
        result += "<div class='float_box2' style='background-image: linear-gradient(to right, #87baff, #87baff, red)'><p>TEMPERATURE: ";
      } else if (weather.Temperature >=7) {
        result += "<div class='float_box2' style='background-image: linear-gradient(to right, #87baff, #87baff, orange)'><p>TEMPERATURE: ";
      } else {
        result += "<div class='float_box2' style='background-image: linear-gradient(to right, #87baff, #87baff, blue)'><p>TEMPERATURE: ";
      }
      result += weather.Temperature + "ºC</p></div>";

      if (weather.RealFeelTemperature >= 15) {
        result += "<div class='float_box2' style='background-image: linear-gradient(to right, #87baff, #87baff, red)'><p>REAL FEEL TEMPERATURE: ";
      } else if (weather.RealFeelTemperature >=7) {
        result += "<div class='float_box2' style='background-image: linear-gradient(to right, #87baff, #87baff, orange)'><p>REAL FEEL TEMPERATURE: ";
      } else {
        result += "<div class='float_box2' style='background-image: linear-gradient(to right, #87baff, #87baff, blue)'><p>REAL FEEL TEMPERATURE: ";
      }
      result += weather.RealFeelTemperature + "ºC</p></div>";

      result += "<div class='float_box2'><p>Relative Humidity: " + weather.RelativeHumidity + "%</p></div>";

      result += "<div class='line'></div>";

      result += "<div class='float_box2'><p>Wind Speed: " + weather.WindSpeed + "kph</p></div>";
      result += "<div class='float_box2'><p>Cloud Cover: " + weather.CloudCover + "%</p></div>";
      
      result += "<div class='line'></div>";

      result += "<div class='float_box2'><p>Precipitation Probability: " + weather.PrecipitationProbability + "%</p></div>";
      if (weather.rain!=0 && weather.PrecipitationProbability!=0) {
        result += "<div class='float_box2'><p>Rain: " + weather.Rain + "mm</p></div>";
      }
      
    });
    
    
      
    
    document.getElementById("weather").innerHTML = result;

    }).catch(err => {
      console.log("OOPS!", err);
    })
  }
  