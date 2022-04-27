
const gameConfig = require("../../config");


function applyGivenRotation(position, rotation) {
    let newPosition = "";
    for(let i = 0; i< 9 ; i++) {
        newPosition += position[rotation[i]];
    }
    return newPosition;
}

function findAllBoardRotations(position) {
    let max = -1;
    let max_rotation = [];
    for(let i = 0; i< gameConfig["rotations"].length; i++) {
        let tryPosition = applyGivenRotation(position, gameConfig["rotations"][i]);
        if(tryPosition > max) {
            max = tryPosition;
            max_rotation = [];
        }
        if(tryPosition == max) {
            max_rotation.push(i);
        }
    }
    return max_rotation;
}

function findARotation(position) {
    let max_rotation = findAllBoardRotations(position);
    return max_rotation[Math.floor(Math.random() * max_rotation.length)];
}

function isMaxRotation(position) {
    let rotations = findAllBoardRotations(position);
    return rotations[0] == 0;
}

function isWin(position) {
    let winStates = gameConfig["winStates"];
    for(let i = 0; i < winStates.length; i++) {
        if(pos[winStates[i][0]] != "0"  && pos[winStates[i][0]] == pos[winStates[i][1]] && pos[winStates[i][1]] == pos[winStates[i][2]]) {
            return parseInt(pos[winStates[i][0]]);
        }       
    }
    return 0;
}

