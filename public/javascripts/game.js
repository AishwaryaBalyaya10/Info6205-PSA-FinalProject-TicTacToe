const gameConfig = require("../config");

function new_game() {
  if (gameConfig.playAgain) {
    gameConfig.menace[1]["moves"] = [];
    gameConfig.menace[2]["moves"] = [];
    gameConfig.board = Array(9).fill(0);
    no_winner = true;
    for (var i = 0; i < 9; i++) {
      document.getElementById("pos" + i).innerHTML =
        "<form onsubmit='javascript:play_human(" +
        i +
        ");return false'><input type='submit' value=' '></form>";
    }
    play_menace();
  }
}

function setPlayer(setTo) {
  player = setTo;
  document.getElementById("who").innerHTML = whoA[setTo];
  if (setTo == "m") {
    show_menace(2);
  } else {
    hide_menace(2);
  }
  if (setTo != "h") {
    document.getElementById("speeddiv").style.display = "block";
  } else {
    document.getElementById("speeddiv").style.display = "none";
  }
  if (setTo != "h" && human_turn) {
    play_opponent();
  }
}

function winner(b) {
  var pos = b.join("");
  var th = three(pos);
  if (th != 0) {
    return th;
  }
  if (count(b, 0) == 0) {
    return 0;
  }
  return false;
}

function opposite_result(r) {
  if (r == 0) {
    return 0;
  }
  return 3 - r;
}

function check_win() {
  var who_wins = winner(board);
  if (who_wins !== false) {
    if (who_wins == 0) {
      say("It's a draw.");
    }
    if (who_wins == 1) {
      say("MENACE wins.");
    }
    if (who_wins == 2) {
      say(whoA[player] + " wins.");
    }
    do_win(who_wins);
    human_turn = false;
  }
}

function do_win(who_wins) {
  no_winner = false;
  for (var i = 0; i < 9; i++) {
    if (board[i] == 0) {
      document.getElementById("pos" + i).innerHTML = "";
    }
  }
  menace_add_beads(who_wins);
  if (player == "h") {
    window.setTimeout(new_game, 1000);
  } else {
    window.setTimeout(
      new_game,
      -parseInt(document.getElementById("speed_slider").value)
    );
  }
}

function play_menace() {
  where = get_menace_move(1);
  if (where == "resign") {
    if (count(board, 0) == 9) {
      say("MENACE has run out of beads in the first box and refuses to play.");
      playagain = false;
      return;
    }
    do_win(2);
    say("MENACE resigns");
    return;
  }
  board[where] = 1;
  document.getElementById("pos" + where).innerHTML = pieces[1];
  check_win();
  if (no_winner) {
    play_opponent();
  }
}

function play_opponent() {
  if (player == "h") {
    human_turn = true;
    return;
  }
  human_turn = false;
  var where = undefined;
  if (player == "r") {
    where = get_random_move();
  } else if (player == "m") {
    where = get_menace_move(2);
  } else if (player == "p") {
    where = get_perfect_move();
  }
  if (where == "resign") {
    do_win(1);
    say("MENACE2 resigns");
    return;
  }
  board[where] = 2;
  document.getElementById("pos" + where).innerHTML = pieces[2];
  check_win();
  if (no_winner) {
    window.setTimeout(
      play_menace,
      -parseInt(document.getElementById("speed_slider").value) / 10
    );
  }
}
