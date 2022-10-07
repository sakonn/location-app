## Semestral project for UNIX - vývojové prostredie

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
- [ ] Add paths of equipement on the map

## Used tools
- Flask - web server
- SQLalchemy - db
- Bcrypt - password encryption
- LoginManager - user login session management
- Mail - emails sending
- Misaka - markdown to html conversion
- wtforms - forms creation and handling
- TimedJSONWebSignatureSerializer - password reset tokens

- os, datetime, 