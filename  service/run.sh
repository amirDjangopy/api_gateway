#!/bin/sh

echo "Running gRPC server..."
python grpc_server.py &

echo "Running Django server..."
python manage.py runserver 0.0.0.0:8000 &

wait
