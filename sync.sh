#!/bin/bash

rsync -avz --exclude 'venv' --exclude '.vscode' ../pingpong ec2-54-209-250-166.compute-1.amazonaws.com:/home/ubuntu/
