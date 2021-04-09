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
}

function handlePersuitRace() {
  $("#raceLength").show();
}
