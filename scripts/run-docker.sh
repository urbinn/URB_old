#!/bin/bash
DIRECTORY=$1

if [ -d "$1" ]; then
  docker build -t urbinn/urb -f $1/Dockerfile .
  # Base a development image on the base image
  docker run --name urbinn-urb-dev -v $DIRECTORY:/urb -it urbinn/urb /bin/bash
else
  echo $1
  echo "Excepting second argument: host project directory."
fi