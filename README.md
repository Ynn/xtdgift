# Extended Gift

A converter of gift extended by pandoc and jinja to gift (https://docs.moodle.org/38/en/GIFT_format)

It allows the use of pandoc (and thus to be able to write the code of a question on several lines and to have the formatting of the source code) in GIFT format. Besides, it also allows to integrate the Jinja template engine to generate questions and use variable. This prototype has been rushed to meet my own needs. It is most likely imperfect. It is advised not to use it for too big files to ease debugging.

## Example :

An example source file `example.txt` and the generated file `generated.txt` can be found in example directory

### Pandoc (source code formatting)

You can use pandoc with [pandoc] .. [/pandoc] shortcodes. The resulting html code will be inlined.


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
[html]// 
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

You can call jinja with [jinja] ... [/jinja] shortcodes.

Jinja command are triggered by `$$>` and variable can be accessed via `${varname}`


The following file :
```
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