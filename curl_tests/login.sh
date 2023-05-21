#!/bin/bash

echo "Testing login"
curl -X POST -H "Content-Type: application/json" -d '{"username": "koosha", "password": "chehreh1234"}' http://localhost:8000/api/token/