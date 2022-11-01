## Semestral project for VAII - the vajko

### Object
Simple web application build on Flask, which can store location data from monitoring device in database and represent them on the map. 

### TODO
- [x] Handle user login (hashing password, logout, session)
- [x] API for storing location data (url api, API keys handling, keys storage in database and creation)
- [x] display of map with location data (leaflet.js representation with points on map)
- [x] Create config file with local configuration (db access, app configuration etc.)
- [x] Configure permissions to unpublish sensitive data
- [ ] Make path crossplatform
- [ ] Optimize code
- [ ] Reformat time to local timezone
- [ ] Add option to store more items per user
- [ ] Configure rentals of the equipement
- [ ] Add paths of equipement on the map (http://project-osrm.org/docs/v5.5.3/api/#general-options)

#### Todo semestral project
- [ ] 5 dynamic pages
  - [ ] Points map
  - [ ] My account / keys management - merge two paths into single page to make all editor on one page
  - [ ] Equipement edit page
  - [x] Equipement list page
  - [ ] Content pages
- [ ] 50 lines of javascript code
  - [ ] Improve map behaviour
  - [ ] Validate input on registration page with JS
- [ ] 20 custom css rules
  - [x] 7 rules for key design
- [ ] 4 entites with CRUD operations
  - [ ] Keys
    - [x] create
    - [x] read
    - [x] update
    - [x] delete
  - [ ] Equipement
    - [x] create
    - [x] read
    - [ ] update
    - [ ] Add more fields
    - [x] Make some nice views of data
    - [x] delete
  - [ ] Account
    - [x] create
    - [x] read
    - [x] update
    - [ ] delete
  - [ ] Location point
    - [x] create
    - [x] read
    - [ ] update
    - [ ] delete
- [ ] validation of input on form fields on server side
  - [ ] Data type and valid value of inserted item
  - [ ] Prevention before SQL Injection
- [ ] AJAX comunication
  - [ ] Filters of points
  - [ ] Add new 
- [ ] Check resposive design
- [ ] Check W3C standards
- [ ] Add docker compose file or dockerfile

## Used tools
- Flask - web server
- SQLalchemy - db
- Bcrypt - password encryption
- LoginManager - user login session management
- Mail - emails sending
- Misaka - markdown to html conversion
- wtforms - forms creation and handling
- TimedJSONWebSignatureSerializer - password reset tokens
- os, datetime
- https://icons8.com/line-awesome for icons