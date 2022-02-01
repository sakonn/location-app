#!/usr/bin/env bash

docker-compose exec backend env TERM=xterm sh -c "exec bash -l"
