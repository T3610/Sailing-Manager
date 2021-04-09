function updateRaceType(racetype) {
  var settings = {
    url:
      "development.dorchestersailingclub.org.uk/api/updateracetype/" + racetype,
    method: "GET",
    timeout: 0,
  };

  $.ajax(settings).done(function (response) {
    console.log(response);
  });
}

function handleHandicapRace() {
  $("#raceLength").hide();
  updateRaceType(0)
}

function handlePersuitRace() {
  $("#raceLength").show();
  updateRaceType(1)
}