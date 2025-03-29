#!/bin/bash
cd /mnt/c/projects
docker compose build app-server
cd ~
docker save --output image.tar app:image_app
scp image.tar user@ip:/home/user/path