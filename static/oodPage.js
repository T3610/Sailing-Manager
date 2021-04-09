$(document).ready(function () {
  if ($("#radioBoxHcap").is(":checked")) {
    handleHandicapRace();
  }
  if ($("#radioBoxPers").is(":checked")) {
    handlePersuitRace();
  }
});

function handleHandicapRace() {
  $("#raceLength").hide();
  $("#startTimes").hide();
}

function handlePersuitRace() {
  $("#startTimes").show();
  $("#raceLength").show();
}

function handleRaceBegin(raceNum) {
  var currentTime = Math.round(Date.now() / 1000);

  var settings = {
    url:
      "https://racing.dorchestersailingclub.org.uk/beginrace/1/" +
      raceNum +
      "?begintimeTime=" +
      currentTime,
    method: "PATCH",
    timeout: 0,
  };

  $.ajax(settings).done(function (response) {
    console.log(response);
    alert("The race has begun");
  });
}
