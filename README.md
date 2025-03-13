# Small example of using the STACK API

This code is based on a modification by Sam Fearn of some of the STACK API code from https://github.com/maths/moodle-qtype_stack

## Setup

1. Run `docker-compose up`
2. Navigate to `http://localhost:8080/`

Note: The Example question page that ships with the STACK API is found at `http://localhost:3080/stack.php`

Remark: In `docker-compose.xml`, the line

```
    volumes:
      - ./web:/usr/share/nginx/html
```

is a setting to ease development. It serves the purpose so we don't have to restart the container each time we make any changes content in the `web` folder.
