# Extended Gift (moodle) format

A converter of gift extended by pandoc and jinja to gift (https://docs.moodle.org/38/en/GIFT_format)

It allows the use of [pandoc](https://pandoc.org) (and thus to be able to write the code of a question on several lines and to have the formatting of the source code) in GIFT format. Besides, it also integrates the [Jinja template engine](https://jinja.palletsprojects.com/en/2.11.x/) to help generate questions (via loops) and use variables and simple operations. This prototype has been rushed to meet my own needs. It is most likely imperfect. It is advised not to use it for too big files to ease debugging.

## Installing

After cloning the project, you have two choices :

### 1) use docker (recommanded)

#### Pulling/Using directly

An image has been pushed to docker hub. You can use it this way (see Using section below) :

```bash
docker run -v $(pwd):/work -it --rm nnynn/xtdgift:latest /work/filetoconvert.txt > converted.txt
```

#### Building 
You go to the docker directory, build the image with `build.sh` and start the command with `cli.sh`




### 2) use python (you'll have to install dependencies)
You will need pandoc, pillow and requirements :

Example on Debian :
```shell
pip install pillow
pip install -r requirements
apt install pandoc
```

## Using CLI

If using the code :
```bash
python xtdgift.py source.txt > generated.txt
```

or 

```bash
python xtdgift.py source.txt generated.txt
```


If using docker :

```bash
docker run -v $(pwd):/work -it --rm nnynn/xtdgift:latest /work/filetoconvert.txt > /work/converted.txt
```

or :

```bash
docker run -v $(pwd):/work -u $(id -u ${USER}):$(id -g ${USER}) -it --rm nnynn/xtdgift:latest /work/filetoconvert.txt /work/converted.txt
```

For instance (if you want to build example from the current directory)
```bash
docker run -v $(pwd):/work -it --rm nnynn/xtdgift:latest /work/example/example.txt > example/generated.txt
```

or you can also use the scripts contained in the docker directory.

```bash
docker/cli.sh /work/source.txt > generated.txt
```

## Using Server

launch with :
```
./docker/server.sh
```

or

```bash
sudo docker run -p 5000:5000 -it --rm --entrypoint "python" nnynn/xtdgift /app/server.py
```

connect to http://localhost:5000

## Examples :

An example source file `example.txt` and the generated file `generated.txt` can be found in example directory

### Pandoc (source code formatting)

You can use pandoc with `[pandoc] .. [/pandoc]` shortcodes. The resulting html code will be inlined.
The [use of pandoc is detailled here](https://pandoc.org/demos.html)


The following gift file 
<pre>
::Question 1:: How tall is John ? {}

//Change the category into which the following questions are added
$CATEGORY: stupid

//This question uses pandoc, source code and images
//is converted to images. Resulting html is minified and
//styles is inlined.
::Question 2::
[pandoc]

What is the **result** of this code ?

```java
int a = 1;
int b = a;
b = 2
System.out.println(a+b)
```

[/pandoc]
{3}
```
</pre>

Is converted to :

```html
::Question 1:: How tall is John ? {}

//Change the category into which the following questions are added
$CATEGORY: stupid

//This question uses pandoc, source code and images
//is converted to images. Resulting html is minified and
//styles is inlined.
::Question 2::
// 
// 
// What is the **result** of this code ?
// 
// java
// int a = 1;
// int b = a;
// b = 2
// System.out.println(a+b)
// 
// 
// 
<p>What is the <strong>result</strong> of this code ?</p><p></p><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAATMAAABgCAIAAAD+VwLkAAAXUUlEQVR4nO2deVwT19rHTwhJhrCEVSKyCChKxCBLFVFBRS2L1aBQpbRXVKRVKqX3vXr9vNYderX2VYtaxArqFaPGUtzADQVEFIGyC2g0oGFfQtgjEHj/GJtGcJmQgQQ8308+7Zkzc57zHMyTM2eZ3xAEgudgeDl .....">
{3}
```

### Jinja (generate variants)

You can call jinja with `[jinja] ... [/jinja]` shortcodes. For the use of jinja see [the jinja documentation](https://jinja.palletsprojects.com/en/2.11.x/)

Jinja command are triggered by `$$>` and variables can be accessed via `${varname}`


The following file :
```
//Change the category into which the following questions are added
$CATEGORY: jinja

[jinja]

$$> set dict = {"Alice":44, "Bob":12, "Bernard":45}
$$> for k,v in dict.items():

//Classical gift questions
::Jinja ${k}:: How old is ${k} ? {=${v}}

$$>endfor

[/jinja]
```

is converted into :

```
//Change the category into which the following questions are added
$CATEGORY: jinja

//Classical gift questions
::Jinja Alice:: How old is Alice ? {=44}

//Classical gift questions
::Jinja Bob:: How old is Bob ? {=12}

//Classical gift questions
::Jinja Bernard:: How old is Bernard ? {=45}

```


