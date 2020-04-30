# Extended Gift

A converter of gift extended by pandoc and jinja to gift

It allows the use of pandoc (and thus to be able to write the code of a question on several lines and to have the formatting of the source code) in GIFT format. Besides, it also allows to integrate the Jinja template engine to generate questions and use variables.

This prototype has been rushed to meet my own needs. It is most likely imperfect. It is advised not to use it for too big files to ease debugging.

## Installing

After cloning the project, you have two choices :

### docker
You go to the docker directory, build the image with `build.sh` and start the command with `cli.sh`

### python
You will need pandoc, pillow and requirements :

Example on Debian :
```shell
pip install pillow
pip install -r requirements
apt install pandoc
```


## Using