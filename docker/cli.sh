#!/usr/bin/env bash
sudo docker run -u $(id -u ${USER}):$(id -g ${USER}) -v $(pwd):/work -it --rm nnynn/xtdgift $@