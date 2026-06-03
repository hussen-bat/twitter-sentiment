#!/bin/bash
cd /home/ubuntu/twitter-sentiment
nohup gunicorn run:app --bind 0.0.0.0:5000 > app.log 2>&1 &
