#!/bin/bash

while true; do
    echo "Starting bot..."
    python bot.py
    echo "Bot crashed with exit code $?. Restarting..." >&2
    sleep 2
done
