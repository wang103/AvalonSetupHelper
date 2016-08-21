var numGoodEl = document.getElementById("num_good");
var numEvilEl = document.getElementById("num_evil");

function toggleNumPlayers(el) {
  var num = parseInt(el.options[el.selectedIndex].value);

  var numGood = 3;
  var numEvil = 2;
  if (num == 6) {
    numGood = 4;
  }
  else if (num == 7) {
    numGood = 4;
    numEvil = 3;
  }
  else if (num == 8) {
    numGood = 5;
    numEvil = 3;
  }
  else if (num == 9) {
    numGood = 6;
    numEvil = 3;
  }
  else if (num == 10) {
    numGood = 6;
    numEvil = 4;
  }

  numGoodEl.innerHTML = numGood;
  numEvilEl.innerHTML = numEvil;
}

