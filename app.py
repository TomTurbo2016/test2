import os
from flask import Flask, request, redirect, url_for, session #, render_template
from random import randint
import requests
import stylize2
import upscale2
import imageResize
import imageResize2
from cv2 import imencode
import base64
from io import BytesIO
import PIL.Image as Image


####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~To-Be-Edited~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>
PATH_TO_BASE64_TXT_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/base64strings/imgStr.txt')
PATH_TO_STYLE_FILES = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/styleModels/')
PATH_TO_SCALE_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/upscaleModel/')
DOWNSIZE_INPUT_IMAGE = 255 #--> 255 px: Downsize uploaded Image (cv2 Image)
####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'JPG', 'JPEG'])


app = Flask(__name__, static_url_path='/static')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = os.urandom(13)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def saveBase64StringToFile(_base64string):
    with open(PATH_TO_BASE64_TXT_FILE,'a') as f:
        f.write('\n' + session['randInt'] + _base64string)

def openBase64StringFromFile():
    with open(PATH_TO_BASE64_TXT_FILE, 'r') as file:
        for i, line in enumerate(file, start=0):
            if line[:2] == session['randInt']:
                return line[2:]

def deleteLine_Base64String():
    with open(PATH_TO_BASE64_TXT_FILE,'r+') as f:
        new_f = f.readlines()
        f.seek(0)
        for line in new_f:
            if session['randInt'] not in line[:2]:
                f.write(line)
            f.truncate()

####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~To-Be-Edited~STYLES~~~~~~~~~~~~~~~~~~~~~~~~~~~~>
def downloadFileMosaic():
    url = 'https://drive.google.com/uc?export=download&id=1vkb6LgfJZwX_SoXUdHVnP2y9NcnAzb2K'
    destination = PATH_TO_STYLE_FILES + 'mosaic.pth'
    r = requests.get(url)
    with open(destination, 'wb') as f:
        f.write(r.content)
        
def downloadFileChurchwindow():
    url = 'https://drive.google.com/uc?export=download&id=1CqdfpXC5NPYS3VUcySweEVio6MwkU0mu'    
    destination = PATH_TO_STYLE_FILES + 'churchWindow.pth'
    r = requests.get(url)
    with open(destination, 'wb') as f:
        f.write(r.content)
####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<

####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~To-Be-Edited~SCALE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>
def downloadFile2xSize():
    url = 'https://drive.google.com/uc?export=download&id=1KXG30EWad1rdjh5QPdsyCZZldZN0zRKy'
    destination = PATH_TO_SCALE_FILE + '2xSize.pth'
    r = requests.get(url)
    with open(destination, 'wb') as f:
        f.write(r.content)
####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if session.get('counter') == True:
        session['counter'] += 1
    else:
        session['counter'] = 0
    if request.method == 'POST':
        session['counter'] += 1
        doStyle = request.form.get('doStyle','')
        if doStyle != '1' and doStyle != '2':
            if 'file' not in request.files:
                return redirect(url_for('file_upload_error_nofile'))
            fileStorage = request.files['file']
            if fileStorage and allowed_file(fileStorage.filename):
                img = imageResize.main2(DOWNSIZE_INPUT_IMAGE, fileStorage)
                img = imencode('.jpg', img)[1].tostring()
                img = base64.b64encode(img).decode("utf-8")
                session['randInt'] = str(chr(randint(36,126)) + chr(randint(36,126)))
                saveBase64StringToFile(img)
                del fileStorage
                return("<!DOCTYPE html>"
                    "<html lang='en'>"
                        "<head>"
                            "<link rel='shortcut icon' type='image/png' href='static/otherStuff/favicon.ico'/>"
                            "<title>Style-Transfer</title>"
                            "<meta charset='utf-8'>"
                            "<meta name='viewport' content='width=device-width, initial-scale=1'>"
                            "<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css'/>"
                        "</head>"
                        "<body style='background-color:white;'>"
                            "<div class='container-fluid'>"
                                "<div class='col-sm-9'>"
                                    "<h4>"
                                        "<small>"
                                            "Style-Transfer by gexvo"
                                        "</small>"
                                    "</h4>"
                                    "<h4>"
                                        "<form id='select1' method='post' runat='server'>"
                                            "<input type='hidden' value='1' name='doStyle'>"
                                            "<div style='width:200px;'>"
                                                "<select name='stylize' "
                                                        "style='height:50px; font-size:20px; font-weight:bold; background-color:#b0e05e; color:black;' "
                                                        "onchange='this.form.submit(); hideFunction()'>"
                                                    "<option selected disabled>Choose style</option>"
                                                    "<option value='mosaic'>Mosaic</option>"
                                                    "<option value='churchWindow'>Church-Window</option>"
                                                "</select>"
                                            "</div>"
                                        "</form>"
                                    "</h4>"
                                    "<p id='loadingText1' style='display:none; margin-left:2em;'>"
                                        "<b>"
                                            "Your pictue is being style-transferred. Please wait!"
                                        "</b>"
                                    "</p>"
                                    "<p id='loadingText2' style='color:red; display:none; margin-left:2em;'>"
                                        "<b>"
                                            "This process can take about 1 minute."
                                        "</b>"
                                    "</p>"
                                    "<hr>"
                                    "<img id='inputPic' src='data:image/jpg;base64," + img + "' hspace='20'/>"
                                    "<img id='loading' src='static/otherStuff/loading.gif' style='display:none' hspace='20'/>"
                                    "<hr>"
                                    "<button type='button'"
                                            "id='deleteB'"
                                            "onclick='goBack2Start()'"
                                            "style='height:50px; font-size:20px'"
                                            "class='btn btn-danger'>"
                                        "Delete picture"
                                    "</button>"
                                "</div>"
                            "</div>"
                            "<script>"
                                "history.pushState(null, document.title, location.href);"
                                "window.addEventListener('popstate', function (event) {"
                                "history.pushState(null, document.title, location.href);"
                                "});"
                                "function goBack2Start() {"
                                "window.location.href='https://gexvo.onrender.com/';"
                                "}"
                                "function hideFunction() {"
                                "document.getElementById('select1').style.visibility = 'hidden';"
                                "document.getElementById('deleteB').style.visibility = 'hidden';"
                                "document.getElementById('inputPic').style.display = 'none';"
                                "document.getElementById('loading').style.display = 'block';"
                                "document.getElementById('loadingText1').style.display = 'block';"
                                "document.getElementById('loadingText2').style.display = 'block';"
                                "}"
                            "</script>"
                            "<p style='color:white'>.</p>"
                        "</body>"
                    "</html>")
            else:
                return redirect(url_for('file_upload_error_nojpg'))
        elif doStyle != '2':
            ioFile = BytesIO()
            ioFile.write(base64.b64decode(openBase64StringFromFile()))
            ioFile.seek(0)
####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~To-Be-Edited~STYLES~~~~~~~~~~~~~~~~~~~~~~~~~~~~>
            selectedStyle = request.form['stylize']
            if selectedStyle == 'mosaic':
                downloadFileMosaic()
                img = stylize2.main(ioFile, 'mosaic', PATH_TO_STYLE_FILES)
            elif selectedStyle == 'churchWindow':
                downloadFileChurchwindow()
                img = stylize2.main(ioFile, 'churchWindow', PATH_TO_STYLE_FILES)
            else:
                return redirect(url_for('style_error_nostyle'))
####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<
            del ioFile
            downloadFile2xSize()
            img = upscale2.main(img, PATH_TO_SCALE_FILE + '2xSize.pth')
            img = imageResize2.main2(img) #--> 1/3 downscale
            img = Image.fromarray(img)#.astype("uint8")
            rawBytes = BytesIO()
            img.save(rawBytes, "JPEG")
            rawBytes.seek(0)
            del img
            return("<!DOCTYPE html>"
            "<html lang='en'>"
                "<head>"
                    "<link rel='shortcut icon' type='image/png' href='static/otherStuff/favicon.ico'/>"
                    "<title>Style-Transfer</title>"
                    "<meta charset='utf-8'>"
                    "<meta name='viewport' content='width=device-width, initial-scale=1'>"
                    "<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css'>"
                "</head>"
                "<body style='background-color:white;'>"
                    "<div class='container-fluid'>"
                        "<div class='col-sm-9'>"
                            "<h4>"
                                "<small>"
                                    "Style-Transfer by gexvo"
                                "</small>"
                            "</h4>"
                            "<p id='loadingText1' style='display:none; margin-left:2em;'>"
                                "<b>"
                                    "Your pictue is being enlarged. Please wait!"
                                "</b>"
                            "</p>"
                            "<hr>"
                            "<img id='inputPic' src='data:image/jpg;base64," + base64.b64encode(rawBytes.read()).decode("utf-8") + "' hspace='20'/>"
                            "<img id='loading' src='static/otherStuff/loading.gif' style='display:none' hspace='20'/>"
                            "<hr>"
                            "<table>"
                                "<tr>"
                                    "<th>"
                                        "<form method='post' runat='server'>"
                                            "<input type='hidden' value='2' name='doStyle'>"
                                            "<button type='button' "
                                                "id='backB' "
                                                "onclick='this.form.submit();' "
                                                "style='height:50px; font-size:20px' "
                                                "class='btn btn-primary'>"
                                                    "Select style"
                                            "</button>"
                                        "</form>"
                                    "<th>"
                                    "<th>"
                                        "<button type='button' "
                                           "id='deleteB' "
                                           "onclick='goBack2Start()' "
                                           "style='height:50px; font-size:20px' "
                                            "class='btn btn-danger'>"
                                                "Delete picture"
                                        "</button>"
                                    "<th>"
                                "<tr>"
                            "<table>"
                        "</div>"
                    "</div>"
                    "<script>"
                        "history.pushState(null, document.title, location.href);"
                        "window.addEventListener('popstate', function (event) {"
                        "history.pushState(null, document.title, location.href);"
                        "});"
                        "function goBack2Start() {"
                        "window.location.href='https://gexvo.onrender.com/';"
                        "}"
                        "function hideFunction() {"
                        "document.getElementById('backB').style.visibility = 'hidden';"
                        "document.getElementById('deleteB').style.visibility = 'hidden';"
                        "document.getElementById('inputPic').style.display = 'none';"
                        "document.getElementById('loading').style.display = 'block';"
                        "document.getElementById('loadingText1').style.display = 'block';"
                        "document.getElementById('loadingText2').style.display = 'block';"
                        "}"
                    "</script>"
                    "<p style='color:white'>.</p>"
                "</body>"
            "</html>")
        else:
            return("<!DOCTYPE html>"
            "<html lang='en'>"
                "<head>"
                    "<link rel='shortcut icon' type='image/png' href='static/otherStuff/favicon.ico'/>"
                    "<title>Style-Transfer</title>"
                    "<meta charset='utf-8'>"
                    "<meta name='viewport' content='width=device-width, initial-scale=1'>"
                    "<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css'/>"
                "</head>"
                "<body style='background-color:white;'>"
                    "<div class='container-fluid'>"
                        "<div class='col-sm-9'>"
                            "<h4>"
                                "<small>"
                                    "Style-Transfer by gexvo"
                                "</small>"
                            "</h4>"
                            "<h4>"
                                "<form id='select1' method='post' runat='server'>"
                                    "<input type='hidden' value='1' name='doStyle'>"
                                    "<div style='width:200px;'>"
                                        "<select name='stylize' "
                                                "style='height:50px; font-size:20px; font-weight:bold; background-color:#b0e05e; color:black;' "
                                                "onchange='this.form.submit(); hideFunction()'>"
                                            "<option selected disabled>Choose style</option>"
                                            "<option value='mosaic'>Mosaic</option>"
                                            "<option value='churchWindow'>Church-Window</option>"
                                        "</select>"
                                    "</div>"
                                "</form>"
                            "</h4>"
                            "<p id='loadingText1' style='display:none; margin-left:2em;'>"
                                "<b>"
                                    "Your pictue is being style-transferred. Please wait!"
                                "</b>"
                            "</p>"
                            "<p id='loadingText2' style='color:red; display:none; margin-left:2em;'>"
                                "<b>"
                                    "This process can take about 1 minute."
                                "</b>"
                            "</p>"
                            "<hr>"
                            "<img id='inputPic' src='data:image/jpg;base64," + openBase64StringFromFile() + "' hspace='20'/>"
                            "<img id='loading' src='static/otherStuff/loading.gif' style='display:none' hspace='20'/>"
                            "<hr>"
                            "<button type='button'"
                                    "id='deleteB'"
                                    "onclick='goBack2Start()'"
                                    "style='height:50px; font-size:20px'"
                                    "class='btn btn-danger'>"
                                "Delete picture"
                            "</button>"
                        "</div>"
                    "</div>"
                    "<script>"
                        "history.pushState(null, document.title, location.href);"
                        "window.addEventListener('popstate', function (event) {"
                        "history.pushState(null, document.title, location.href);"
                        "});"
                        "function goBack2Start() {"
                        "window.location.href='https://gexvo.onrender.com/';"
                        "}"
                        "function hideFunction() {"
                        "document.getElementById('select1').style.visibility = 'hidden';"
                        "document.getElementById('deleteB').style.visibility = 'hidden';"
                        "document.getElementById('inputPic').style.display = 'none';"
                        "document.getElementById('loading').style.display = 'block';"
                        "document.getElementById('loadingText1').style.display = 'block';"
                        "document.getElementById('loadingText2').style.display = 'block';"
                        "}"
                    "</script>"
                    "<p style='color:white'>.</p>"
                "</body>"
            "</html>")
    else:
        if session['counter'] >= 1:
            deleteLine_Base64String()
        return ("<!DOCTYPE html>"
        "<html lang='en'>"
            "<head>"
                "<link rel='shortcut icon' type='image/png' href='static/otherStuff/favicon.ico'/>"
                "<title>gexvo - Upload a Picture</title>"
                "<meta charset='utf-8'>"
                "<meta name='viewport' content='width=device-width, initial-scale=1'>"
                "<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css'>"
            "</head>"
            "<body style='background-color:white;'>"
                "<div class='container-fluid'>"
                    "<div class='col-sm-9'>"
                        "<h4>"
                            "<small>"
                                "Welcome to Neural Style Transfer by gexvo"
                            "</small>"
                        "</h4>"
                        "<h4>"
                        "<hr>"
                            "<p style='margin-left:25px;'>"
                                "Upload  an image and apply"
                            "</p>"
                            "<p style='margin-left:25px;'>"
                                "a pre-trained style model."
                            "</p>"
                            "<!--<img src='static/otherStuff/startPic4.jpg' hspace='10'/>-->"
                            "<img id='upLo' src='static/otherStuff/uploading2.gif' style='display:none'/>"
                            "<form method=post enctype=multipart/form-data runat='server'>"
                                "<div>"
                                    "<p style='color:white'>.</p>"
                                    "<p>"
                                        "<label id='lab'>"
                                            "<b style='border-style:solid; margin-left:12px; color:black; font-size:200%; background-color:#f6fc9c; font-weight:bold; cursor: pointer;'>"
                                                "Click to upload"
                                            "</b>"
                                            "<input type='file' "
                                                "name='file' "
                                                "onchange='this.form.submit(); this.form.onsubmit=hideFunction();' "
                                                "style='visibility: hidden;'/>"
                                        "</label>"
                                    "</p>"
                                "</div>"
                            "</form>"
                        "<hr>"
                    "</div>"
                "</div>"
                "<script>"
                    "history.pushState(null, document.title, location.href);"
                    "window.addEventListener('popstate', function (event) {"
                    "history.pushState(null, document.title, location.href);"
                    "});"
                    "function hideFunction() {"
                    "document.getElementById('lab').style.visibility = 'hidden';"
                    "document.getElementById('upLo').style.display = 'block';"
                    "}"
                "</script>"
            "</body>"
        "</html>")


##Error-Messages:
@app.route('/FILE_UPLOAD_ERROR_NoFileSelected')
def file_upload_error_nofile():
    return '''
    <!doctype html>
    <title>Upload File ERROR - No File selected</title>
    <h1>No file selected</h1>
    <button onclick="goBack()">Go Back</button>
    <script>
    function goBack() {
    window.location.href='https://gexvo.onrender.com/';
    }
    </script>
    '''

@app.route('/STYLE_ERROR_NoStyleSelected')
def style_error_nostyle():
    return '''
    <!doctype html>
    <title>Style ERROR - No Style selected</title>
    <h1>No style selected</h1>
    <button onclick="goBack()">Go Back</button>
    <script>
    function goBack() {
    window.location.href='https://gexvo.onrender.com/';
    }
    </script>
    '''

@app.route('/FILE_UPLOAD_ERROR_NoJPGformat')
def file_upload_error_nojpg():
    return '''
    <!doctype html>
    <title>Upload File ERROR - No jpg Format</title>
    <h1>File needs to end with .jpg</h1>
    <button onclick="goBack()">Go Back</button>
    <script>
    function goBack() {
    window.location.href='https://gexvo.onrender.com/';
    }
    </script>
    '''

@app.route('/GENERALERROR')
def generalError():
    return '''
    <!doctype html>
    <title>ERROR</title>
    <h1>Something went wrong!</h1>
    <button onclick="goBack()">Go Back</button>
    <script>
    function goBack() {
    window.location.href='https://gexvo.onrender.com/';
    }
    </script>
    '''


