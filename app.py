import os
import fnmatch
from flask import Flask, request, redirect, url_for, render_template, session
from werkzeug import secure_filename
from uuid import uuid4
import requests
import stylize
import upscale
import imageResize


ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'JPG', 'JPEG'])
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/userUploadImages')
STYLE_MODELS_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/styleModels')
UPSCALE_MODEL_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/upscaleModel')

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = os.urandom(13)


def deleteSpecificFilesInDir():
    filelist = [ f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".JPG") or f.endswith(".JPEG") ]
    for f in filelist:
        if fnmatch.fnmatch(f, str(session['randInt']) + 'oT-Ti' + '*') or fnmatch.fnmatch(f, 'out_' + str(session['randInt']) + 'oT-Ti' + '*') or fnmatch.fnmatch(f, 'out_big_' + str(session['randInt']) + '*'):
            os.remove(os.path.join(UPLOAD_FOLDER, f))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



##-------------------------------DOWNLOAD-STYLES------------------------------------------------>
def downloadFileMosaic():
    url = 'https://drive.google.com/uc?export=download&id=1vkb6LgfJZwX_SoXUdHVnP2y9NcnAzb2K'    
    destination = STYLE_MODELS_FOLDER + '/mosaic.pth'
    r = requests.get(url)
    with open(destination, 'wb') as f:
        f.write(r.content)
        
def downloadFileChurchwindow():
    url = 'https://drive.google.com/uc?export=download&id=1CqdfpXC5NPYS3VUcySweEVio6MwkU0mu'    
    destination = STYLE_MODELS_FOLDER + '/churchWindow.pth'
    r = requests.get(url)
    with open(destination, 'wb') as f:
        f.write(r.content)
        
def downloadFileFireworks():
    url = 'https://drive.google.com/uc?export=download&id=1kJ1A06bAptFeS14yi-eQyEtVyJrMHhsl'    
    destination = STYLE_MODELS_FOLDER + '/fireworks.pth'
    r = requests.get(url)
    with open(destination, 'wb') as f:
        f.write(r.content)
        
def downloadFileRainprincess():
    url = 'https://drive.google.com/uc?export=download&id=1wGKXEboB3oTFAi8g3gQelNhxbQ53yPsp'    
    destination = STYLE_MODELS_FOLDER + '/rainPrincess.pth'
    r = requests.get(url)
    with open(destination, 'wb') as f:
        f.write(r.content)
        
def downloadFileTiger():
    url = 'https://drive.google.com/uc?export=download&id=1Bm9WqLLVliWK49lYW9C1CjqPehrMLanI'    
    destination = STYLE_MODELS_FOLDER + '/tiger.pth'
    r = requests.get(url)
    with open(destination, 'wb') as f:
        f.write(r.content)
        
##-------------------------------DOWNLOAD-SCALE------------------------------------------------>      
def downloadFile2xSize():
    url = 'https://drive.google.com/uc?export=download&id=1KXG30EWad1rdjh5QPdsyCZZldZN0zRKy'    
    destination = UPSCALE_MODEL_FOLDER + '/2xSize.pth'
    r = requests.get(url)
    with open(destination, 'wb') as f:
        f.write(r.content)
        
def downloadFile3xSize():
    url = 'https://drive.google.com/uc?export=download&id=1cnzlliVlL4wsuP-mrf8HfllC8qGLZbaS'    
    destination = UPSCALE_MODEL_FOLDER + '/3xSizec.pth'
    r = requests.get(url)
    with open(destination, 'wb') as f:
        f.write(r.content)
        
##--------------------------------------------------------------------------------------------->      



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
            maxWidthHeight = 400 #900 & 500 works!!!
            imageResize.main(maxWidthHeight, UPLOAD_FOLDER + '/' + filename)
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
            stylize.main(pathInputPic, pathOutputPic, styleName, STYLE_MODELS_FOLDER)
            return render_template('showPic_style.html', img_filename=fileNameOut)
        
        elif selectedStyle == 'rainPrincess':
            downloadFileRainprincess()
            styleName = 'rainPrincess'
            stylize.main(pathInputPic, pathOutputPic, styleName, STYLE_MODELS_FOLDER)
            return render_template('showPic_style.html', img_filename=fileNameOut)
        
        elif selectedStyle == 'churchWindow':
            downloadFileChurchwindow()
            styleName = 'churchWindow'
            stylize.main(pathInputPic, pathOutputPic, styleName, STYLE_MODELS_FOLDER)
            return render_template('showPic_style.html', img_filename=fileNameOut)
        
        elif selectedStyle == 'tiger':
            downloadFileTiger()
            styleName = 'tiger'
            stylize.main(pathInputPic, pathOutputPic, styleName, STYLE_MODELS_FOLDER)
            return render_template('showPic_style.html', img_filename=fileNameOut)
        
        elif selectedStyle == 'fireworks':
            downloadFileFireworks()
            styleName = 'fireworks'
            stylize.main(pathInputPic, pathOutputPic, styleName, STYLE_MODELS_FOLDER)
            return render_template('showPic_style.html', img_filename=fileNameOut)
        
        ##-----------------------------------------UPSCALE----------------------------------->
        elif selectedStyle == 'enlarge':
            downloadFile2xSize()
            #downloadFile3xSize
            upscaleName = '2xSize'
            upscale.main(pathOutputPic, pathOutputPicBig, upscaleName, UPSCALE_MODEL_FOLDER)
            return render_template('showPic_upscale.html', img_filename=fileNameOutBig)
        ##----------------------------------------------------------------------------------->
    else:
        filename = request.args.get('filename')
        return render_template('showPic.html', img_filename=filename)


@app.errorhandler(Exception)
def exception_handler(error):
    return "!!!!"  + repr(error)


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
def file_too_big_error():
    return '''
    <!doctype html>
    <title>File too big ERROR</title>
    <h1>Something went wrong!</h1>
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


