function updateTime() {
  var settings = {
    url: "https://racing.dorchestersailingclub.org.uk/startTime",
    method: "GET",
    timeout: 0,
  };

  $.ajax(settings).done(function (response) {
    //console.log(response);

    let d = new Date(); // Creates a Date Object using the clients current time

    let now = new Date();

    let [hours, minutes] = response.split(":"); // Using ES6 destructuring
    // var time = "18:19:02".split(':'); // "Old" ES5 version

    d.setHours(+hours); // Set the hours, using implicit type coercion
    d.setMinutes(minutes); // You can pass Number or String. It doesn't really matter
    d.setSeconds(0);
    // If needed, adjust date and time zone

    //console.log(d.toString()); // Outputs your desired time (+current day and timezone)

    if (now < d) {
      var timeDiff = d - now;
      var secDiff = (timeDiff / 1000) % 60; //in s
      var minDiff = (timeDiff / 60 / 1000) % 60; //in minutes
      var hDiff = timeDiff / 3600 / 1000; //in hours
      //console.log(Math.floor(hDiff)+":"+Math.floor(minDiff)+":"+secDiff)
      $("#raceCountdown").text(
        ("0" + Math.floor(hDiff)).slice(-2) +
          ":" +
          ("0" + Math.floor(minDiff)).slice(-2) +
          ":" +
          ("0" + Math.floor(secDiff)).slice(-2)
      );
    } else {
      $("#raceCountdown").text("OUT OF TIME");
    }
  });
}

$(document).ready(function () {
  var d = new Date();
  var n = d.getDay();

  if (n == 0) {
    var intervalId = window.setInterval(function () {
      updateTime();
    }, 1000);
  } else {
    $("#countdownDesc").remove();
  }

  $(".signupbtn").click(function (e) {
    window.location = "signup";
  });
  $(".signupclosedbtn").click(function (e) {
    alert(
      "The last signup time has passed. Please speak to the OOD. Thank You"
    );
  });
  $(".entrylistbtn").click(function (e) {
    window.location = "entries";
  });
  $(".startorderbtn").click(function (e) {
    window.location = "startingorder";
  });
  $(".oodbtn").click(function (e) {
    window.location = "oodracesetup";
  });
});
