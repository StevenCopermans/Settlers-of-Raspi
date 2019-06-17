let socket;

const init = function () {
    enableSocketIO();

    jsColor = document.querySelector('.jscolor');
    jsColor.addEventListener('change', changeColor);
}

const enableSocketIO = function () {
    socket = io.connect(window.location.host + ":5000");

    socket.on('ledColor', (color) => {
        jsColor = document.querySelector('.jscolor');
        console.log(color);
        jsColor.jscolor.fromString(color);
    });
}

const changeColor = function (event) {
    socket.emit("changeColor", event.target.value)
}

document.addEventListener('DOMContentLoaded', function () {
    console.info('DOM geladen');
    init();
});