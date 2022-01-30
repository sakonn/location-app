var map;
var markersGroup;

function showPoints(list) {
  // remove all the markers in one go
  markersGroup.clearLayers();
  // show a marker on the map
  console.log(list);
  let arrayOfMarkers = [];
  for (const [pID, p] of Object.entries(list)) {
    L.marker({lon: p.lon, lat: p.lat}).bindPopup(p.timestamp).addTo(markersGroup);
    arrayOfMarkers.push([p.lat, p.lon]);
  }
  var bounds = new L.LatLngBounds(arrayOfMarkers);
  map.fitBounds(bounds);
}

function loadPoints() {
  let date_to = document.getElementById('date_to').value;
  let date_from = document.getElementById('date_from').value;
  data = {
    'date_to': Date.parse(date_to) / 1000,
    'date_from': Date.parse(date_from) / 1000
  }
  fetch(window.location + 'api/listpoints', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
  .then(response => response.json())
  .then(data => {
    console.log('Success:', data);
    showPoints(data);
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}

window.addEventListener('DOMContentLoaded', (event) => {
  // initialize Leaflet
  map = L.map('map').setView({lon: 0, lat: 0}, 2);

  // add the OpenStreetMap tiles
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
  }).addTo(map);

  // show the scale bar on the lower left corner
  L.control.scale({imperial: false, metric: true}).addTo(map);

  // Markers group 
  markersGroup = L.layerGroup().addTo(map);


  // Show initial list of points on the map
  showPoints(points, map);

  // Initialize all input of date type.
  const calendars = bulmaCalendar.attach('[type="datetime"]', {
    displayMode:      'default'
  });

  // Loop on each calendar initialized
  calendars.forEach(calendar => {
    // Add listener to select event
    calendar.on('select', date => {
      console.log(date);
    });
  });

  // To access to bulmaCalendar instance of an element
  const element = document.querySelector('#my-element');
  if (element) {
    // bulmaCalendar instance is available as element.bulmaCalendar
    element.bulmaCalendar.on('select', datepicker => {
      console.log(datepicker.data.value());
    });
  }

  document.getElementById("filter").addEventListener("click", loadPoints); 
});



