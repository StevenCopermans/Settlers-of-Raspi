let socket, tiles, tileID;

const init = function () {
    tiles = document.querySelector('.js-pawns').children;
    tileID = 0;

    enableSocketIO();
}

const enableSocketIO = function () {
    socket = io.connect(window.location.host + ":5000");
    console.log("Uhmm");

    socket.on('GO', (data) => {
        console.log("Uhmm");

        changeTile(data);
    });
}

const changeTile = function (data) {
    if (data) {
        if (data[1]) {
            tiles[data[0]].removeAttribute("hidden");
        } else {
            tiles[data[0]].setAttribute("hidden", "");
        }
    }
}

document.addEventListener('DOMContentLoaded', function () {
    console.info('DOM geladen');
    init();
});