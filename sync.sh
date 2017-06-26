#!/bin/bash

rsync -avz --delete --exclude 'venv' --exclude '.vscode' --exclude '.git' --exclude '.gitignore' ../pingpong ec2-54-209-250-166.compute-1.amazonaws.com:/home/ubuntu/
