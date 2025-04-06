# Small example of using the STACK API

The javascript code in `/web/js` is based on a modification by Sam Fearn of some of the STACK API code from https://github.com/maths/moodle-qtype_stack

## Setup

1. Run `sudo docker compose up` (you can omit `sudo` if you've set up rootless docker)
2. Navigate to `http://localhost:8080/`

Note: The Example question page that ships with the STACK API is found at `http://localhost:3080/stack.php`. 

## Production remarks

The following changes are referring to `docker-compose.xml`.

To ease development, we have mounted the volume
```
    volumes:
      - ./web:/usr/share/nginx/html
```
It serves the purpose so we don't have to restart the container each time we make any changes content in the `web` folder.

We serve our content on port 8080.
```
    ports:
      - "8080:80"
```
This can be changed e.g. to port 80 if we want to serve our API on the default port.

Comment out
```
    ports:
      - '3080:80'
```

if you don't want to expose the STACK API itself and its example page to the outside.

