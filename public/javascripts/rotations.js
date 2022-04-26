
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

// function 