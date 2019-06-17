let socket;

const init = function () {
    enableSocketIO();
    getSensorData();
}

const enableSocketIO = function () {
    socket = io.connect(window.location.host + ":5000");

    socket.on('SensorData', (data) => {
        console.log("Data gotten");

        showSensorData(data);
    });


}

const showSensorData = function (data) {
    sensors = JSON.parse(data);
    table = document.querySelector('.js-table');

    for (let i = 0; i < sensors.length; ++i) {
        table.innerHTML += `
            <div class="c-table-row">
                                <div class="c-table-cell c-cell">
                                    <div class="c-table-cell--heading">Entry ID</div>
                                    <div class="c-table-cell--content js-Date">${sensors[i]['EntryID']}</div>
                                </div>
                                <div class="c-table-cell c-cell">
                                    <div class="c-table-cell--heading">Sensor ID</div>
                                    <div class="c-table-cell--content ">${sensors[i]['SensorID']}</div>
                                </div>
                                <div class="c-table-cell c-cell topic-cell">
                                    <div class="c-table-cell--content js-Title">${sensors[i]['Name']}</div>
                                </div>
                                <div class="c-table-cell c-cell">
                                    <div class="c-table-cell--heading">Time</div>
                                    <div class="c-table-cell--content">${sensors[i]['Time']}
                                    </div>
                                </div>
                                <div class="c-table-cell c-table-cell--foot c-cell">
                                    <div class="c-table-cell--heading">Value</div>
                                    <div class="c-table-cell--content">${sensors[i]['Value']}</div>
                                </div>
                            </div>
        `;

    }
}

const getSensorData = function () {
    socket.emit("sensors");
    console.log("Requesting");

}

document.addEventListener('DOMContentLoaded', function () {
    console.info('DOM geladen');
    init();
});