#!/bin/sh
sudo docker run -p 5000:5000 -it --rm --entrypoint "python" nnynn/xtdgift /app/server.py