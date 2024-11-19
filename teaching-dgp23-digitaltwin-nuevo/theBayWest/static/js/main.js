function supp_room() {
    fetch('/delete')
        .then(response => console.log("OK"))
        .catch(error => console.error(error));
}
// create room
document.addEventListener('DOMContentLoaded', function() {
    var popupButton = document.getElementById("popupCreateRoom");
    var popup = document.getElementById("popup1");
    var closePopupButton = document.getElementById("closePopup1");
    popupButton.addEventListener('click', function() {
        popup.style.display = "block";
    });

    closePopupButton.addEventListener('click', function() {
        popup.style.display = "none";
    });
});

//edit room
document.addEventListener('DOMContentLoaded', function() {
    var popupButtons = document.querySelectorAll(".popupEditRoom"); // Sélectionnez tous les boutons popupEditRoom
    var closePopupButtons = document.querySelectorAll(".closePopup2"); // Sélectionnez tous les boutons closePopup2

    popupButtons.forEach(function(popupButton, index) {
        var popup = document.querySelectorAll(".popup2")[index];

        popupButton.addEventListener('click', function() {
            popup.style.display = "block";
        });

        closePopupButtons[index].addEventListener('click', function() {
            popup.style.display = "none";
        });
    });
});

// Popup Door
document.addEventListener('DOMContentLoaded', function() {
    var popupButtons = document.querySelectorAll(".buttonPopupDoor");
    var closePopupButtons = document.querySelectorAll(".closePopupDoor");
    var popupButtonsAddDoor = document.querySelectorAll(".buttonPopupAddDoor");
    var closePopupButtonsAddDoor = document.querySelectorAll(".closePopupAddDoor");
    var popupButtonsAddDoorSubmit = document.querySelectorAll(".buttonPopupAddDoorSubmit")

    popupButtons.forEach(function(popupButton, index) {
        var popup = document.querySelectorAll(".popupDoor")[index];
        var popupAddDoor = document.querySelectorAll(".popupAddDoor")[index];
        var storageKey = 'popupState_' + index;

        popupButton.addEventListener('click', function() {
            popup.style.display = "block";
            localStorage.setItem(storageKey, 'openDoor'); // Store popup state as 'open'
        });

        closePopupButtons[index].addEventListener('click', function() {
            popup.style.display = "none";
            localStorage.setItem(storageKey, 'closedDoor'); // Store popup state as 'closed'
        });

        popupButtonsAddDoor[index].addEventListener('click', function() {
            popup.style.display = "none";
            popupAddDoor.style.display = "block";
            localStorage.setItem(storageKey, 'openAddDoor');
        });

        closePopupButtonsAddDoor[index].addEventListener('click', function() {
            popupAddDoor.style.display = "none";
            popup.style.display = "block"
            localStorage.setItem(storageKey, 'openDoor');
        });

        popupButtonsAddDoorSubmit[index].addEventListener('click', function() {
            popupAddDoor.style.display = "none";
            popup.style.display = "block"
            localStorage.setItem(storageKey, 'openDoor');
        });

        // Check and restore popup state on page load
        var popupState = localStorage.getItem(storageKey);
        if (popupState === 'openDoor') {
            popup.style.display = "block";
        } else if (popupState === 'closedDoor') {
            popup.style.display = "none";
        } else if (popupState === 'openAddDoor') {
            popupAddDoor.style.display = "block"
        }
    });
});

// Popup Chart
document.addEventListener('DOMContentLoaded', function() {
    var popupButtons = document.querySelectorAll(".buttonPopupGraph");
    var closePopupButtons = document.querySelectorAll(".closePopupGraph");

    popupButtons.forEach(function(popupButton, index) {
        var popup = document.querySelectorAll(".popupGraph")[index];
        var storageKey = 'popupState_' + index;

        popupButton.addEventListener('click', function() {
            popup.style.display = "block";
            localStorage.setItem(storageKey, 'openGraph'); // Store popup state as 'open'
        });

        closePopupButtons[index].addEventListener('click', function() {
            popup.style.display = "none";
            localStorage.setItem(storageKey, 'closedGraph'); // Store popup state as 'closed'
        });

        // Check and restore popup state on page load
        var popupState = localStorage.getItem(storageKey);
        if (popupState === 'openGraph') {
            popup.style.display = "block";
        } else if (popupState === 'closedGraph') {
            popup.style.display = "none";
        }
    });
});

// Popup Light
document.addEventListener('DOMContentLoaded', function() {
    var popupButtons = document.querySelectorAll(".buttonPopupLight");
    var closePopupButtons = document.querySelectorAll(".closePopupLight");

    popupButtons.forEach(function(popupButton, index) {
        var popup = document.querySelectorAll(".popupLight")[index];
        var storageKey = 'popupState_' + index;

        popupButton.addEventListener('click', function() {
            popup.style.display = "block";
            localStorage.setItem(storageKey, 'openLight'); // Store popup state as 'open'
        });

        closePopupButtons[index].addEventListener('click', function() {
            popup.style.display = "none";
            localStorage.setItem(storageKey, 'closedLight'); // Store popup state as 'closed'
        });

        // Check and restore popup state on page load
        var popupState = localStorage.getItem(storageKey);
        if (popupState === 'openLight') {
            popup.style.display = "block";
        } else if (popupState === 'closedLight') {
            popup.style.display = "none";
        }
    });
});

// Popup Ventilator
document.addEventListener('DOMContentLoaded', function() {
    var popupButtons = document.querySelectorAll(".buttonPopupVentilator");
    var closePopupButtons = document.querySelectorAll(".closePopupVentilator");

    popupButtons.forEach(function(popupButton, index) {
        var popup = document.querySelectorAll(".popupVentilator")[index];
        var storageKey = 'popupState_' + index;

        popupButton.addEventListener('click', function() {
            popup.style.display = "block";
            localStorage.setItem(storageKey, 'openVentilator'); // Store popup state as 'open'
        });

        closePopupButtons[index].addEventListener('click', function() {
            popup.style.display = "none";
            localStorage.setItem(storageKey, 'closedVentilator'); // Store popup state as 'closed'
        });

        // Check and restore popup state on page load
        var popupState = localStorage.getItem(storageKey);
        if (popupState === 'openVentilator') {
            popup.style.display = "block";
        } else if (popupState === 'closedVentilator') {
            popup.style.display = "none";
        }
    });
});

// Popup Window
document.addEventListener('DOMContentLoaded', function() {
    var popupButtons = document.querySelectorAll(".buttonPopupWindow");
    var closePopupButtons = document.querySelectorAll(".closePopupWindow");

    popupButtons.forEach(function(popupButton, index) {
        var popup = document.querySelectorAll(".popupWindow")[index];
        var storageKey = 'popupState_' + index;

        popupButton.addEventListener('click', function() {
            popup.style.display = "block";
            localStorage.setItem(storageKey, 'openWindow'); // Store popup state as 'open'
        });

        closePopupButtons[index].addEventListener('click', function() {
            popup.style.display = "none";
            localStorage.setItem(storageKey, 'closedWindow'); // Store popup state as 'closed'
        });

        // Check and restore popup state on page load
        var popupState = localStorage.getItem(storageKey);
        if (popupState === 'openWindow') {
            popup.style.display = "block";
        } else if (popupState === 'closedWindow') {
            popup.style.display = "none";
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var popupButton = document.getElementById("popupUploadFile");
    var popup = document.getElementById("popupUpload");
    var closePopupButton = document.getElementById("closePopupUpload");
    popupButton.addEventListener('click', function() {
        popup.style.display = "block";
    });

    closePopupButton.addEventListener('click', function() {
        popup.style.display = "none";
    });
});

function selectRoom(clickedElement, roomName, roomNameToAdd) {
    var allRoomItems = document.querySelectorAll('.room-item');
    allRoomItems.forEach(function(item) {
        item.classList.remove('selected'); // Remove 'selected' class from all items
    });

    clickedElement.classList.add('selected'); // Add 'selected' class to the clicked element
    console.log(clickedElement)

    // Set the selected room value based on the room name
    document.getElementById('selectedRoom' + roomName).value = roomNameToAdd;
    console.log(roomNameToAdd)
}

function validateSelection(roomName) {
    var selectedRoom = document.getElementById('selectedRoom' + roomName).value;
    if (selectedRoom === '') {
        alert('Please select a room.');
        return false;
    }
    console.log("validateSection" + selectedRoom)
    return true;
}

function updateDoorStatus(checkbox, roomName) {
    var doorId = $(checkbox).data('door-id');
    var status = checkbox.checked ? 'on' : 'off';
    console.log(doorId)
    $.ajax({
        url: '/updateDoorStatus',
        method: 'POST',
        contentType: 'application/json', // Specify content type as JSON
        data: JSON.stringify({ doorId: doorId, status: status, room_id: roomName }),
        success: function(response) {
            // Handle the response from the server if needed
            console.log(response);
            initializeDoorsChart(roomName)
        },
        error: function(error) {
            // Handle errors if needed
            console.error(error);
        }
    });
}

function updateLightStatus(checkbox,roomName) {
    var lightId = $(checkbox).data('light-id');
    var status = checkbox.checked ? 'on' : 'off';

    $.ajax({
        url: '/updateLightStatus',
        method: 'POST',
        contentType: 'application/json', // Specify content type as JSON
        data: JSON.stringify({ lightId: lightId, status: status }),
        success: function(response) {
            // Handle the response from the server if needed
            console.log(response);
            initializeLightsChart(roomName)
        },
        error: function(error) {
            // Handle errors if needed
            console.error(error);
        }
    });
}

function updateVentilatorStatus(checkbox,roomName) {
    var ventilatorId = $(checkbox).data('ventilator-id');
    var status = checkbox.checked ? 'on' : 'off';

    $.ajax({
        url: '/updateVentilatorStatus',
        method: 'POST',
        contentType: 'application/json', // Specify content type as JSON
        data: JSON.stringify({ ventilatorId: ventilatorId, status: status }),
        success: function(response) {
            // Handle the response from the server if needed
            console.log(response);
            initializeVentilatorsChart(roomName)
        },
        error: function(error) {
            // Handle errors if needed
            console.error(error);
        }
    });
}

function updateWindowStatus(checkbox, roomName) {
    var windowId = $(checkbox).data('window-id');
    var status = checkbox.checked ? 'on' : 'off';

    $.ajax({
        url: '/updateWindowStatus',
        method: 'POST',
        contentType: 'application/json', // Specify content type as JSON
        data: JSON.stringify({ windowId: windowId, status: status }),
        success: function(response) {
            // Handle the response from the server if needed
            console.log(response);
            initializeWindowsChart(roomName)
        },
        error: function(error) {
            // Handle errors if needed
            console.error(error);
        }
    });
}

function getRandomNumber(min, max, toFloat=false) {
    const num = Math.random() * (max - min) + min;
    
    const ret = toFloat ? parseFloat(num.toFixed(3)): Math.round(num);

    return ret;
  }

// Async Ajax Changes

function initDynamicElements(roomName) {
    let dynamicClasses = [
        ".dynamic-temperature"+roomName, ".dynamic-people"+roomName, ".dynamic-co2"+roomName
    ];
    
    dynamicClasses.forEach(function (className) {
        processDynamicElement(className, roomName);
    }); 
}
    
function processDynamicElement(asyncClass, roomName) {
    let waitMillisecs = getRandomNumber(20,30, true) * 1000;
    
    let currentElementDiv = $(document).find(asyncClass).last();
    let asyncElement = $(currentElementDiv.find(".async-data"))
    updateAsyncContentForElement(asyncElement, asyncClass, roomName);
    setInterval( function() {
        updateAsyncContentForElement(asyncElement, asyncClass, roomName);
    }, waitMillisecs);

}

function updateAsyncContentForElement(dynamicElem, className, roomName) {
    const url = `/update_async_content/${roomName}/${className}`;
    const CO2Thresholds = {
        low: 800,
        high: 1000
    };
    const colors = {
        green: 'rgba(0, 128, 0, 0.3)',
        red: 'rgba(255, 0, 0, 0.3)',
        yellow: 'rgba(255, 255, 0, 0.3)'
    };

    $.ajax({
        url,
        type: 'GET',
        success: function(response) {
            dynamicElem.text(response.data);
            if (className === `.dynamic-co2${roomName}`) {
                addCO2(roomName, response.data)
                const colorElement = $(`.${roomName}Color`).eq(0);
                const co2Data = response.data;

                colorElement.css('backgroundColor', co2Data < CO2Thresholds.low ? colors.green :
                    co2Data > CO2Thresholds.high ? colors.red : colors.yellow);
                
                if (co2Data > 1000){
                    openAllWindows(roomName)
                    activateAllVentilators(roomName)
                }
            }
            if (className === `.dynamic-temperature${roomName}`) {
                addTemperature(roomName, response.data)
                if(response.data > 70){
                    openAllDoors(roomName);
                    showSnackbar(`The temperature in ${roomName} is too high. Opening all doors`)
                }
            }
            if (className === `.dynamic-people${roomName}`) {
                addPeople(roomName, response.data)
                if (response.data > 0){
                    activateAllLights(roomName);
                }else{
                    turnOffLights(roomName)
                    turnOffVentilators(roomName)
                }
                
            }
        },
        error: function(error) {
            console.error('Error en la actualización asíncrona:', error);
        }
    });
}

function addTemperature(roomName, data) {
    var requestData = {
        room_name: roomName,
        temperature_data: data
    };

    fetch('/add_temperature', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => {
        if (response.ok) {
            console.log('Temperature added successfully!');
            // Perform any additional actions if required
            initializeTemperatureChart(roomName)
        } else {
            console.error('Failed to add temperature.');
        }
    })
    .catch(error => {
        console.error('Error adding temperature:', error);
    });
}

function addCO2(roomName, data) {
    var requestData = {
        room_name: roomName,
        co2_data: data
    };

    fetch('/add_co2', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => {
        if (response.ok) {
            console.log('CO2 added successfully!');
            // Perform any additional actions if required
            initializeCO2Chart(roomName)
        } else {
            console.error('Failed to add CO2.');
        }
    })
    .catch(error => {
        console.error('Error adding CO2:', error);
    });
}

function addPeople(roomName, data) {
    var requestData = {
        room_name: roomName,
        people_data: data
    };

    fetch('/add_people', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => {
        if (response.ok) {
            console.log('People added successfully!');
            // Perform any additional actions if required
            initializePeopleChart(roomName)
        } else {
            console.error('Failed to add People.');
        }
    })
    .catch(error => {
        console.error('Error adding People:', error);
    });
}

function openAllWindows(roomName) {
    const container = document.querySelector(`.Windows${roomName}`);
    if (container) {
        const checkboxes = container.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach((checkbox) => {
            if (!checkbox.checked) {
                checkbox.checked = true;
                checkbox.value = true;
                updateWindowStatus(checkbox, roomName);
            }
        });
    }
}

function activateAllVentilators(roomName) {
    const container = document.querySelector(`.Ventilators${roomName}`);
    if (container) {
        const checkboxes = container.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach((checkbox) => {
            if (!checkbox.checked) {
                checkbox.checked = true;
                checkbox.value = true;
                updateVentilatorStatus(checkbox, roomName);
            }
        });
    }
}

function turnOffVentilators(roomName) {
    const container = document.querySelector(`.Ventilators${roomName}`);
    if (container) {
        const checkboxes = container.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach((checkbox) => {
            if (checkbox.checked) {
                checkbox.checked = false;
                checkbox.value = false;
                updateVentilatorStatus(checkbox, roomName);
            }
        });
    }
}

function activateAllLights(roomName) {
    const container = document.querySelector(`.Lights${roomName}`);
    if (container) {
        const checkboxes = container.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach((checkbox) => {
            if (!checkbox.checked) {
                checkbox.checked = true;
                checkbox.value = true;
                updateLightStatus(checkbox, roomName);
            }
        });
    }
}

function turnOffLights(roomName) {
    const container = document.querySelector(`.Lights${roomName}`);
    if (container) {
        const checkboxes = container.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach((checkbox) => {
            if (checkbox.checked) {
                checkbox.checked = false;
                checkbox.value = false;
                updateVentilatorStatus(checkbox, roomName);
            }
        });
    }
}

function openAllDoors(roomName) {
    const container = document.querySelector(`.Doors${roomName}`);
    if (container) {
        const checkboxes = container.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach((checkbox) => {
            if (!checkbox.checked) {
                checkbox.checked = true;
                checkbox.value = true;
                updateDoorStatus(checkbox, roomName);
            }
        });
    }
}

function showSnackbar(message) {
    var customSnackbar = document.getElementById("custom-snackbar");
    customSnackbar.textContent = message;
    customSnackbar.className = "show";
    setTimeout(function(){ customSnackbar.className = customSnackbar.className.replace("show", ""); }, 3000);
  }


$(document).ready(function() {
    $.ajax({
        url: '/get_rooms',
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            console.log(data.rooms);
            data.rooms.forEach(function(room) {
                updateWindowsStatus(room);
                updateDoorsStatus(room);
                updateLightsStatus(room);
                updateVentilatorsStatus(room);
                setInterval(function() {
                    updateWindowsStatus(room);
                    updateDoorsStatus(room);
                    updateLightsStatus(room);
                    updateVentilatorsStatus(room);
                }, 500);
            });
        },
        error: function(xhr, status, error) {
            console.error("Erreur lors de la récupération des données:", error);
        }
    });
});

function updateWindowsStatus(roomName) {
    $.ajax({
        url: `/device_status?room_name=${roomName}&device_name=window`, // Pass roomName as a query parameter
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            const windowsStatusDiv = document.getElementById(`windowsStatus-${roomName}`);
            windowsStatusDiv.innerHTML = '';

            const roomData = data[roomName];

            // Modify the text to include a line break (<br>) between Open and Closed
            const windowStatusText = `Closed - ${roomData.closed_count}<br>Open - ${roomData.open_count}`;

            const pElement = document.createElement('p');
            // Set innerHTML instead of textContent to render HTML tags
            pElement.innerHTML = windowStatusText;
            windowsStatusDiv.appendChild(pElement);
        },
        error: function(xhr, status, error) {
            console.error("Error fetching data:", error);
        }
    });
}


function updateDoorsStatus(roomName) {
    $.ajax({
        url: `/device_status?room_name=${roomName}&device_name=door`, // Pass roomName as a query parameter
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            const doorsStatusDiv = document.getElementById(`doorsStatus-${roomName}`);
            doorsStatusDiv.innerHTML = '';

            const roomData = data[roomName];

            // Modify the text to include a line break (<br>) between Open and Closed
            const doorsStatusText = `Closed - ${roomData.closed_count}<br>Open - ${roomData.open_count}`;

            const pElement = document.createElement('p');
            // Set innerHTML instead of textContent to render HTML tags
            pElement.innerHTML = doorsStatusText;
            doorsStatusDiv.appendChild(pElement);
        },
        error: function(xhr, status, error) {
            console.error("Error fetching data:", error);
        }
    });
}


function updateLightsStatus(roomName) {
    $.ajax({
        url: `/device_status?room_name=${roomName}&device_name=light`, // Pass roomName as a query parameter
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            const lightsStatusDiv = document.getElementById(`lightsStatus-${roomName}`);
            lightsStatusDiv.innerHTML = '';

            const roomData = data[roomName];

            // Modify the text to include a line break (<br>) between On and Off
            const lightsStatusText = `Off - ${roomData.off_count}<br>On - ${roomData.on_count}`;

            const pElement = document.createElement('p');
            // Set innerHTML instead of textContent to render HTML tags
            pElement.innerHTML = lightsStatusText;
            lightsStatusDiv.appendChild(pElement);
        },
        error: function(xhr, status, error) {
            console.error("Error fetching data:", error);
        }
    });
}


function updateVentilatorsStatus(roomName) {
    $.ajax({
        url: `/device_status?room_name=${roomName}&device_name=ventilator`, // Pass roomName as a query parameter
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            const ventilatorsStatusDiv = document.getElementById(`ventilatorsStatus-${roomName}`);
            ventilatorsStatusDiv.innerHTML = '';

            const roomData = data[roomName];

            // Modify the text to include a line break (<br>) between On and Off
            const ventilatorsStatusText = `Off - ${roomData.off_count}<br>On - ${roomData.on_count}`;

            const pElement = document.createElement('p');
            // Set innerHTML instead of textContent to render HTML tags
            pElement.innerHTML = ventilatorsStatusText;
            ventilatorsStatusDiv.appendChild(pElement);
        },
        error: function(xhr, status, error) {
            console.error("Error fetching data:", error);
        }
    });
}


// Function to initialize the chart for a specific room
function initializeTemperatureChart(roomName) {
    var canvasId = 'temperature_' + roomName;
    var existingChart = null;  // Variable to store the existing chart instance

    // Check if the canvas already exists
    var existingCanvas = document.getElementById(canvasId);

    if (existingCanvas) {
        // If canvas exists, check if the chart is already created
        existingChart = Chart.getChart(existingCanvas);
    }

    // If the chart doesn't exist, create a new one
    if (!existingChart) {
        var ctx = existingCanvas.getContext('2d');

        existingChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Temperature',
                    data: [],
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Function to update chart data using AJAX for each room
    function updateChartData() {
        fetch('/update_temperature_chart', {
            method: 'POST',
            body: JSON.stringify({ room_name: roomName }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            existingChart.data.labels = data.labels;
            existingChart.data.datasets[0].data = data.data;
            existingChart.update();
        });
    }

    // Call the function to update chart data for each room every 3 seconds
    updateChartData();
}

// Function to initialize the chart for a specific room
function initializeCO2Chart(roomName) {
    var canvasId = 'co2_' + roomName;
    var existingChart = null;  // Variable to store the existing chart instance

    // Check if the canvas already exists
    var existingCanvas = document.getElementById(canvasId);
    
    if (existingCanvas) {
        // If canvas exists, check if the chart is already created
        existingChart = Chart.getChart(existingCanvas);
    }

    // If the chart doesn't exist, create a new one
    if (!existingChart) {
        var ctx = existingCanvas.getContext('2d');
        
        existingChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'CO2',
                    data: [],
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Function to update chart data using AJAX for each room
    function updateChartData() {
        fetch('/update_co2_chart', {
            method: 'POST',
            body: JSON.stringify({ room_name: roomName }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            existingChart.data.labels = data.labels;
            existingChart.data.datasets[0].data = data.data;
            existingChart.update();
        });
    }

    // Call the function to update chart data for each room every 3 seconds
    updateChartData();
}

// Function to initialize the chart for a specific room
function initializePeopleChart(roomName) {
    var canvasId = 'people_' + roomName;
    var existingChart = null;  // Variable to store the existing chart instance

    // Check if the canvas already exists
    var existingCanvas = document.getElementById(canvasId);
    
    if (existingCanvas) {
        // If canvas exists, check if the chart is already created
        existingChart = Chart.getChart(existingCanvas);
    }

    // If the chart doesn't exist, create a new one
    if (!existingChart) {
        var ctx = existingCanvas.getContext('2d');
        
        existingChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'People',
                    data: [],
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Function to update chart data using AJAX for each room
    function updateChartData() {
        fetch('/update_people_chart', {
            method: 'POST',
            body: JSON.stringify({ room_name: roomName }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            existingChart.data.labels = data.labels;
            existingChart.data.datasets[0].data = data.data;
            existingChart.update();
        });
    }

    // Call the function to update chart data for each room every 3 seconds
    updateChartData();
}

// Function to initialize the chart for a specific room
function initializeVentilatorsChart(roomName) {
    var canvasId = 'ventilators_' + roomName;
    var canvas = document.getElementById(canvasId);

    // Check if the canvas element exists
    if (!canvas) {
        console.error('Canvas element not found with ID:', canvasId);
        return;
    }

    var ctx = canvas.getContext('2d');

    // Check if a chart with the same canvas ID already exists
    var existingChart = Chart.getChart(ctx);

    // Destroy the existing chart if it exists
    if (existingChart) {
        existingChart.destroy();
    }

    // Create a new chart
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: []
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    function updateChartData() {
        fetch('/update_ventilators_chart', {
            method: 'POST',
            body: JSON.stringify({ room_name: roomName }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            myChart.data.labels = data.labels;
            myChart.data.datasets = data.data.map((ventilatorData, index) => ({
                label: 'Ventilator ' + (index + 1),
                data: ventilatorData,
                borderWidth: 1,
                fill: false
            }));
            myChart.update();
        })
        .catch(error => {
            console.error('Error fetching or updating data:', error);
        });
    }

    // Call the function to update chart data for each room every 3 seconds
    updateChartData();
}

// Function to initialize the chart for a specific room
function initializeWindowsChart(roomName) {
    var canvasId = 'windows_' + roomName;
    var canvas = document.getElementById(canvasId);

    // Check if the canvas element exists
    if (!canvas) {
        console.error('Canvas element not found with ID:', canvasId);
        return;
    }

    var ctx = canvas.getContext('2d');

    // Check if a chart with the same canvas ID already exists
    var existingChart = Chart.getChart(ctx);

    // Destroy the existing chart if it exists
    if (existingChart) {
        existingChart.destroy();
    }

    // Create a new chart
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: []
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    function updateChartData() {
        fetch('/update_windows_chart', {
            method: 'POST',
            body: JSON.stringify({ room_name: roomName }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            myChart.data.labels = data.labels;
            myChart.data.datasets = data.data.map((windowData, index) => ({
                label: 'Window ' + (index + 1),
                data: windowData,
                borderWidth: 1,
                fill: false
            }));
            myChart.update();
        })
        .catch(error => {
            console.error('Error fetching or updating data:', error);
        });
    }

    // Call the function to update chart data for each room every 3 seconds
    updateChartData();
}

// Function to initialize the chart for a specific room
function initializeLightsChart(roomName) {
    var canvasId = 'lights_' + roomName;
    var canvas = document.getElementById(canvasId);

    // Check if the canvas element exists
    if (!canvas) {
        console.error('Canvas element not found with ID:', canvasId);
        return;
    }

    var ctx = canvas.getContext('2d');

    // Check if a chart with the same canvas ID already exists
    var existingChart = Chart.getChart(ctx);

    // Destroy the existing chart if it exists
    if (existingChart) {
        existingChart.destroy();
    }

    // Create a new chart
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: []
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    function updateChartData() {
        fetch('/update_lights_chart', {
            method: 'POST',
            body: JSON.stringify({ room_name: roomName }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            myChart.data.labels = data.labels;
            myChart.data.datasets = data.data.map((lightData, index) => ({
                label: 'Light ' + (index + 1),
                data: lightData,
                borderWidth: 1,
                fill: false
            }));
            myChart.update();
        })
        .catch(error => {
            console.error('Error fetching or updating data:', error);
        });
    }

    // Call the function to update chart data for each room every 3 seconds
    updateChartData();
}

// Function to initialize the chart for a specific room
function initializeDoorsChart(roomName) {
    var canvasId = 'doors_' + roomName;
    var canvas = document.getElementById(canvasId);

    // Check if the canvas element exists
    if (!canvas) {
        console.error('Canvas element not found with ID:', canvasId);
        return;
    }

    var ctx = canvas.getContext('2d');

    // Check if a chart with the same canvas ID already exists
    var existingChart = Chart.getChart(ctx);

    // Destroy the existing chart if it exists
    if (existingChart) {
        existingChart.destroy();
    }

    // Create a new chart
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: []
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    function updateChartData() {
        fetch('/update_doors_chart', {
            method: 'POST',
            body: JSON.stringify({ room_name: roomName }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            myChart.data.labels = data.labels;
            myChart.data.datasets = data.data.map((doorData, index) => ({
                label: 'Door ' + (index + 1),
                data: doorData,
                borderWidth: 1,
                fill: false
            }));
            myChart.update();
        })
        .catch(error => {
            console.error('Error fetching or updating data:', error);
        });
    }

    // Call the function to update chart data for each room every 3 seconds
    updateChartData();
}

function openChart(evt, chartName, room_name) {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent_"+room_name);
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(chartName).style.display = "block";
    evt.currentTarget.className += " active";
  }