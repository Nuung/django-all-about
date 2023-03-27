#!/bin/bash
echo ">> DAA Project Kafak Cluster Docker Init"
docker-compose -f kafka-cluster-compose.yml -p daa-kafka-cluster-app stop
docker-compose -f kafka-cluster-compose.yml -p daa-kafka-cluster-app down
docker-compose -f kafka-cluster-compose.yml -p daa-kafka-cluster-app up -d
