#!/bin/bash

auth_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg0NjkxMjI0LCJpYXQiOjE2ODQ2ODc2MjQsImp0aSI6IjM0ZjA5OTliYzhhYzQ0ZmNiMjFjNjBhNDg4ZTczNTI3IiwidXNlcl9pZCI6Mn0.ik8fHOePhZgPqgi_py2XGb_kaB7jAh07sIf8b_gJGDs"
echo "Testing rating a content"
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer ${auth_token}" -d '{"content": 2, "score": 5}' http://localhost:8000/api/content/rate/