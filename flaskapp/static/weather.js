window.onload = function() {
    initList();
};

function initList() {
    fetch("/home_weather_query").then(response => {
      return response.json();
    }).then(data => {
      console.log("data: ", data);

    result = "<div style='text-align: left;'><h3>  Current Weather</h3><iframe src='https://free.timeanddate.com/clock/i7qk59en/n78/tlie/tt0/tw1/tm1' frameborder='0' width='182' height='18'></iframe><p>----------------------------------------------</p>";
    data.forEach(weather => {
      result += "<p>Temperature: " + weather.Temperature + "ºC</p>";
    });
    
    result += "</div>"
      
    
    document.getElementById("weather").innerHTML = result;

    }).catch(err => {
      console.log("OOPS!", err);
    })
  }
