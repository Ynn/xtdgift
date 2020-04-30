# Extended Gift

A converter of gift extended by pandoc and jinja to gift (https://docs.moodle.org/38/en/GIFT_format)

It allows the use of pandoc (and thus to be able to write the code of a question on several lines and to have the formatting of the source code) in GIFT format. Besides, it also allows to integrate the Jinja template engine to generate questions and use variable. This prototype has been rushed to meet my own needs. It is most likely imperfect. It is advised not to use it for too big files to ease debugging.

Example :


<pre>
::Question 1:: How tall is John ? {}

```java
//Change the category into which the following questions are added
$CATEGORY: stupid


//This question uses pandoc, source code and images
//is converted to images. Resulting html is minified and
//styles is inlined.
::Question 2::
[html][pandoc]

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