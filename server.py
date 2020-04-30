from flask import Flask, request, make_response, send_file, flash, redirect
from pgist import process
import tempfile

app = Flask(__name__)
app.secret_key = b'545dsf212ez_dfsfz'


def process_text(text):
    try:
        resp = make_response(process(text))
        resp.mimetype = "text/plain"
    except Exception as err:
        resp = make_response(f"""
<html>
<body>
<h1> Error while processing </h1>
<code style="white-space: pre-wrap;">
{err}
</code>
</body>
</html>
""")
        resp.status_code = 500

    return resp


@app.route('/convert', methods=["POST"])
def convert():
    return process_text(request.data.decode("UTF-8"))


ALLOWED_EXTENSIONS = {'txt', 'gf', 'md'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            response = process_text(file.read().decode("UTF-8"))
            if response.status_code == 200:
                with tempfile.TemporaryDirectory() as tmpdirname:
                    result_name = file.filename.replace('.', '-generated.')
                    result_path = f"{tmpdirname}/{result_name}"
                    with open(result_path, "wb") as file:
                        file.write(response.data)
                    print(result_name)
                    return send_file(result_path, as_attachment=True, attachment_filename=result_name)
            return response
    return '''
    <!doctype html>
    <title>Upload a gift file to convert</title>
    <h1>Upload a gift file to convert</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/')
def hello():
    return f"""
<!doctype html>
<title>Upload a gift file to convert</title>
<h1>Upload a gift file to convert</h1>
<form method=post enctype=multipart/form-data action="file">
    <input type=file name=file>
    <input type=submit value=Upload>
</form>        
"""


# <textarea id = "story" name = "story" style = "width:40%; height : 60%; float : left;" >
# {f.read()}
# </textarea >
# <div style = " margin : 1em; float:left; height : 60%; width: 10%;" >
# <button class = "favorite styled" type = "button" >
#     Convert - ->
# </button >
# </div >
# <textarea id = "story" name = "story" style = "width:40%; height : 60%; float : left;" >
# It was a dark and stormy night...
# </textarea >

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
