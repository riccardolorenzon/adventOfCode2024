#!/bin/bash
DAY=$1

echo "setting up $DAY..."
mkdir $DAY
uv python pin 3.13 --directory ./$DAY
touch ./$DAY/main.py ./$DAY/data.txt ./$DAY/input.txt