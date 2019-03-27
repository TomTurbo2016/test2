import os
import fnmatch
from flask import Flask, request, redirect, url_for, render_template, session
from werkzeug import secure_filename
from uuid import uuid4
import requests
import stylize

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'JPG', 'JPEG'])
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/userUploadImages')
MODELS_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/styleModels')

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = os.urandom(13)


def downloadFileMosaic():
    url = 'https://drive.google.com/uc?export=download&id=1vkb6LgfJZwX_SoXUdHVnP2y9NcnAzb2K'    
    destination = MODELS_FOLDER + '/mosaic.pth'
    r = requests.get(url)
    with open(destination, 'wb') as f:
        f.write(r.content)

def deleteSpecificFilesInDir():
    filelist = [ f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".JPG") or f.endswith(".JPEG") ]
    for f in filelist:
        if fnmatch.fnmatch(f, str(session['randInt']) + 'oT-Ti' + '*') or fnmatch.fnmatch(f, 'out_' + str(session['randInt']) + 'oT-Ti' + '*') or fnmatch.fnmatch(f, 'out_big_' + str(session['randInt']) + '*'):
            os.remove(os.path.join(UPLOAD_FOLDER, f))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if session.get('counter') == True:
        session['counter'] += 1
    else:
        session['counter'] = 0
    if request.method == 'POST':
        session['counter'] += 1
        if 'file' not in request.files:
            return redirect(url_for('file_upload_error_nofile'))
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            session['randInt'] = str(uuid4())
            randInt = str(session['randInt'])
            filename = randInt + 'oT-Ti' + filename
            session['img_filename'] = filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('NEW_uploaded_file', filename=filename))
        else:
            return redirect(url_for('file_upload_error_nojpg'))
    else:
        if session['counter'] >= 1:
            deleteSpecificFilesInDir()
        return render_template('main_page.html')

    
@app.route('/' + str(os.urandom(13)), methods=['GET', 'POST'])
def NEW_uploaded_file():
    if request.method == 'POST':
        fileName = str(session['img_filename'])
        pathInputPic = UPLOAD_FOLDER + '/' + fileName
        pathOutputPic = UPLOAD_FOLDER + '/out_' + fileName
        pathOutputPicBig = UPLOAD_FOLDER + '/out_big_' + fileName
        fileNameOut = 'out_' + fileName
        fileNameOutBig = 'out_big_' + fileName
        ##-----------------------------------------STYLES------------------------------------>
        selectedStyle = request.form['stylize']
        if selectedStyle == 'mosaic':
            downloadFileMosaic()
            styleName = 'mosaic'
            scaleFactor = 1 #0.5=doubleSize; 1=sameSize
            stylize.main(pathInputPic, pathOutputPic, 'mosaic', MODELS_FOLDER, scaleFactor)
            return render_template('showPic_style.html', img_filename=fileNameOut)
        ##-----------------------------------------STYLES------------------------------------>
    else:
        filename = request.args.get('filename')
        return render_template('showPic.html', img_filename=filename)
    

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
    window.location.href='https://gexvo.onrender.com';
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
    window.location.href='https://gexvo.onrender.com';
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
    window.location.href='https://gexvo.onrender.com';
    }
    </script>
    '''

