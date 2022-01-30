window.addEventListener('DOMContentLoaded', (event) => {
  // initialize Leaflet
  var map = L.map('map').setView({lon: 0, lat: 0}, 2);

  // add the OpenStreetMap tiles
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
  }).addTo(map);

  // show the scale bar on the lower left corner
  L.control.scale({imperial: true, metric: true}).addTo(map);

  // show a marker on the map
  console.log(points);
  let arrayOfMarkers = [];
  for (const [pID, p] of Object.entries(points)) {
    L.marker({lon: p.lon, lat: p.lat}).bindPopup(p.timestamp).addTo(map);
    arrayOfMarkers.push([p.lat, p.lon]);
  }
  var bounds = new L.LatLngBounds(arrayOfMarkers);
  map.fitBounds(bounds);
  // L.marker({lon: 0, lat: 0}).bindPopup('The center of the world').addTo(map);
});



