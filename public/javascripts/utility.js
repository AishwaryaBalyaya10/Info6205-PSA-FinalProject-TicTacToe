

function findArrayMin(arr) {
    let min = arr[0];
    for(let i = 0; i< arr.length; i++) {
        min = Math.min(min,arr[i]);
    }
    return min;
}

function findArrayMax(arr) {
    let max = arr[0];
    for(let i = 0; i < arr.length; i++) {
        max = Math.max(max,arr[i]);
    }
    return max;
}

function countVal(arr,val) {
    let count = 0;
    for(let i =0; i < arr.length; i++) {
        if(arr[i] == val) {
            count++;
        }
    }
    return count;
}

function fillArray(from, length,val) {
    let result =  [];
    for(let i = from; i < length; i++) {
        result[i] = val;
    }
    return result;
}

