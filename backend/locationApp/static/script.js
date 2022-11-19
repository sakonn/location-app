
class Points {
  #map;
  #markersGroup;

  constructor(pMap) {
    // initialize Leaflet
    this.#map = L.map(pMap, {
      gestureHandling: true
    }).setView({lon: 0, lat: 0}, 2);

    // add the OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
    }).addTo(this.#map);
    
    // show the scale bar on the lower left corner
    L.control.scale({imperial: false, metric: true}).addTo(this.#map);

    // Markers group 
    this.#markersGroup = L.layerGroup().addTo(this.#map);
  }

  async loadPoints(that = this) {
    let date_to = document.getElementById('date_to').value;
    let date_from = document.getElementById('date_from').value;
    let equipments = [];
    document.querySelectorAll('[data-filter]:checked').forEach((e) => { equipments.push(e.value) });
    let data = {
      'date_to': Date.parse(date_to) / 1000,
      'date_from': Date.parse(date_from) / 1000,
      'equipment': equipments
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
      that.showPoints(data);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  }

  showPoints(list) {
    // remove all the markers in one go
    this.#markersGroup.clearLayers();
    // show a marker on the map
    let arrayOfMarkers = [];
    for (const [pID, p] of Object.entries(list)) {
      L.marker({lon: p.lon, lat: p.lat}).bindPopup(p.equipment.name + ' -> ' + p.timestamp).addTo(this.#markersGroup);
      arrayOfMarkers.push([p.lat, p.lon]);
    }
    var bounds = new L.LatLngBounds(arrayOfMarkers);
    this.#map.fitBounds(bounds);
  }
}

// Source: https://stackoverflow.com/questions/46155/how-can-i-validate-an-email-address-in-javascript
const validateEmail = (email) => {
  return String(email)
    .toLowerCase()
    .match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
};

function showFormMessage(errorBox, type, message) {
  const messageBox = document.getElementById(errorBox);
  messageBox.innerHTML = '';
  let msgElem = document.createElement('p');
  msgElem.classList.add('help');
  msgElem.classList.add('is-' + type);
  msgElem.innerText = message;
  messageBox.appendChild(msgElem);
}

window.addEventListener('DOMContentLoaded', (event) => {
  let mapHandler;
  if (document.getElementById('map')) {
    mapHandler = new Points('map');
    
    // Show initial list of points on the map
    mapHandler.showPoints(points);
  }
  // Initialize all input of date type.
  const calendars = bulmaCalendar.attach('[type="datetime"]', {
    displayMode:      'dialog'
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

  if (document.getElementById("filter")) {
    document.getElementById("filter").addEventListener("click", () => {
      mapHandler.loadPoints();
    });
  }

  // Get all "navbar-burger" elements
  const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

  // Check if there are any navbar burgers
  if ($navbarBurgers.length > 0) {

    // Add a click event on each of them
    $navbarBurgers.forEach( el => {
      el.addEventListener('click', () => {

        // Get the target from the "data-target" attribute
        const target = el.dataset.target;
        const $target = document.getElementById(target);

        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        el.classList.toggle('is-active');
        $target.classList.toggle('is-active');

      });
    });
  }

  const fileInput = document.querySelector('#equip-image-upload input[type=file]');
  if (fileInput) {
    fileInput.onchange = () => {
      if (fileInput.files.length > 0) {
        const fileName = document.querySelector('#equip-image-upload .file-name');
        fileName.textContent = fileInput.files[0].name;
      }
    }
  }
});


function registerValidator() {
  return {
    username: '',
    usernameError: '',
    email: '',
    emailError: '',
    password: '',
    passwordError: '',
    passConfirm: '',
    passConfirmError: '',
    honeypot: '',
    validateSubmit(e) {
      if (validateEmail(this.email) == null) {
        this.emailError = 'Enter vaild email. Example user@example.com';
      } else {
        this.emailError = '';
      }
      if (this.username.length < 3) {
        this.usernameError = 'Username must be longer then 3 letters.';
      } else {
        this.usernameError = '';
      }
      if (this.password.length < 8) {
        this.passwordError = 'Password must be longer than 8 lettrs.'
      } else {
        this.passwordError = '';
      }
      if (this.passConfirm != this.password) {
        this.passConfirmError = 'Password must match.'
      } else {
        this.passConfirmError = '';
      }
      if (this.honeypot.length > 0) {
        console.log('Spam registered!');
        return;
      }
      document.getElementById("registerForm").submit();
    }
  }
}

function equipmentPage() {
  return {
    equipmentList: [],
    showModal: false,
    token: '',
    newForm: {
      name: '',
      description: '',
    },
    createNewEquip() {
      this.showModal = true;
    },
    async getEquipmentList() {
      // /api/listequip
      var data = await fetch("/api/equipment/list", {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
      }).then((response) => response.json())

      this.equipmentList = data;
    },
    async newEquipmentCreate() {
      var data = await fetch('/api/equipment/new', {
        method: "POST",
        body: JSON.stringify(this.newForm),
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'X-CSRFToken': this.token,
        },
      }).then((response) => response.json());
      this.getEquipmentList();
      this.showModal = false;
    },
    async deleteEquipment(id) {
      var data = await fetch('/api/equipment/delete', {
        method: "POST",
        body: JSON.stringify({'id': id}),
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'X-CSRFToken': this.token,
        },
      }).then((response) => response.json());

      this.getEquipmentList();
    }
  }
}