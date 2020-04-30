#!/bin/sh
sudo docker run -p 5000:5000 -v $(pwd):/work -it --rm nnynn/xtdgift /app/cli.py