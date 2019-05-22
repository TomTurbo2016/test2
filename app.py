#https://github.com/erm/asgi-examples
#https://github.com/pgjones/quart/blob/master/docs/deployment.rst

import os
import sys
from pathlib import Path
from quart import Quart, request, jsonify, session, render_template, redirect, url_for
from io import BytesIO
from PIL import Image
import base64
import requests
import stylize2
import upscale2
import imageResize2
import asyncio
import threading
import time
#import watermark

####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~To-Be-Edited~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>
START_URL = 'https://testquart.onrender.com/'
PATH_TO_BASE64_TXT_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/base64strings/')
PATH_TO_STYLE_FILES = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/styleModels/')
PATH_TO_SCALE_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/upscaleModel/')
####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<

app = Quart(__name__)
app.secret_key = os.urandom(13)

####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~STYLES-FILES~~~~~~~~~~~~~~~~~~~~~~~>
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

####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~SCALE-FILE~~~~~~~~~~~~~~~~~~~~~~~~~>
def downloadFile2xSize():
	url = 'https://drive.google.com/uc?export=download&id=1KXG30EWad1rdjh5QPdsyCZZldZN0zRKy'
	destination = PATH_TO_SCALE_FILE + '2xSize.pth'
	r = requests.get(url)
	with open(destination, 'wb') as f:
		f.write(r.content)
####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<

####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~FUNCTIONS~~~~~~~~~~~~~~~~~~~~~~~~~~>
def saveBase64StringToFile(_path, _base64string):
	with open(_path,'a') as f:
		f.write('\n' + _base64string)

def openBase64StringFromFile(_path, _id):
	with open(_path, 'r') as file:
		for i, line in enumerate(file, start=0):
			if line[:7] == _id:
				return line[7:]

# https://realpython.com/async-io-python/
async def cpu_background_task(selectedStyle, ioFile, url_id,):
	time.sleep(10)
	# if selectedStyle == 'mosaic':
		# if not os.path.exists(PATH_TO_STYLE_FILES + 'mosaic.pth'):
			# downloadFileMosaic()
		# img = stylize2.main(ioFile, 'mosaic', PATH_TO_STYLE_FILES)
	# elif selectedStyle == 'churchWindow':
		# if not os.path.exists(PATH_TO_STYLE_FILES + 'churchWindow.pth'):
			# downloadFileChurchwindow()
		# img = stylize2.main(ioFile, 'churchWindow', PATH_TO_STYLE_FILES)
###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<
	# if not os.path.exists(PATH_TO_STYLE_FILES + '2xSize.pth'):
		# downloadFile2xSize()
	# img = upscale2.main(img, PATH_TO_SCALE_FILE + '2xSize.pth')
	# img = imageResize2.main2(img) #--> 1/3 downscale
	# img = Image.fromarray(img)#.astype("uint8")
	# rawBytes = BytesIO()
	# img.save(rawBytes, "JPEG")
	# rawBytes.seek(0)
	# img = base64.b64encode(rawBytes.read()).decode("utf-8")
	# prefix = 'S' #Style
	# saveBase64StringToFile(PATH_TO_BASE64_TXT_FOLDER + url_id + '.txt', prefix + url_id + img)

# https://realpython.com/intro-to-python-threading/
def thread_function(selectedStyle, ioFile, url_id):
	print('---> 1', file=sys.stderr)
	if selectedStyle == 'mosaic':
		if not os.path.exists(PATH_TO_STYLE_FILES + 'mosaic.pth'):
			downloadFileMosaic()
		img = stylize2.main(ioFile, 'mosaic', PATH_TO_STYLE_FILES)
	elif selectedStyle == 'churchWindow':
		if not os.path.exists(PATH_TO_STYLE_FILES + 'churchWindow.pth'):
			downloadFileChurchwindow()
		img = stylize2.main(ioFile, 'churchWindow', PATH_TO_STYLE_FILES)
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<
	if not os.path.exists(PATH_TO_STYLE_FILES + '2xSize.pth'):
		downloadFile2xSize()
	print('---> 2', file=sys.stderr)
	# img = upscale2.main(img, PATH_TO_SCALE_FILE + '2xSize.pth')
	# img = imageResize2.main2(img) #--> 1/3 downscale
	# img = Image.fromarray(img)#.astype("uint8")
	# rawBytes = BytesIO()
	# img.save(rawBytes, "JPEG")
	# rawBytes.seek(0)
	# img = base64.b64encode(rawBytes.read()).decode("utf-8")
	# prefix = 'S' #Style
	# saveBase64StringToFile(PATH_TO_BASE64_TXT_FOLDER + url_id + '.txt', prefix + url_id + img)
	print('---> 3', file=sys.stderr)

####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<



@app.route('/', methods=['GET'])
async def Index():
	if session.get('url_id') is not None:
		if os.path.exists(PATH_TO_BASE64_TXT_FOLDER + str(session['url_id']) + '.txt'):
			os.remove(PATH_TO_BASE64_TXT_FOLDER + str(session['url_id']) + '.txt')
	return await render_template('startPage.html')


@app.route('/upload', methods=['POST'])
async def UploadImage():
	if request.method == "POST":
		try:
			data_url = await request.get_data()
			data_url = str(data_url.decode('utf-8'))
			data_url_trimmed = data_url[6:-2]
			id_url = data_url_trimmed[len(data_url_trimmed)-6:];
			b64_url = data_url_trimmed[:-6]; #png-Image!!!          
			## Create txt file for user:
			if not os.path.exists(PATH_TO_BASE64_TXT_FOLDER + id_url + '.txt'):
				f = open(PATH_TO_BASE64_TXT_FOLDER + id_url + '.txt', 'x')
				f.close()       
			## Save uploaded pic to txt file:
			prefix = 'O' #Original
			saveBase64StringToFile(PATH_TO_BASE64_TXT_FOLDER + id_url + '.txt', prefix + id_url + b64_url)
			del data_url
			del data_url_trimmed
			del id_url
			del b64_url
			del prefix
		except Exception as e:
			print(str(e), file=sys.stderr) #output to Error-Log-File!
			print('Error: ' + str(e))
		return jsonify('Success')


@app.route('/showPic', methods=['GET', 'POST'])
async def ShowPic():
	if request.method == 'GET':
		url_id = request.args.get('id')
		if url_id is not None:
			prefix = 'O' #Original
			img = openBase64StringFromFile(PATH_TO_BASE64_TXT_FOLDER + url_id + '.txt', prefix + url_id)
			session['url_id'] = url_id
			del prefix
			del url_id
			return ("<!DOCTYPE html>"
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
                                "window.location.href='" + START_URL + "';"
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
			return await render_template('startPage.html')
	else:
		if request.method == 'POST':
			doStyle = (await request.form).get('doStyle','')
			if doStyle == '1':
				prefix = 'O' #Original
				url_id = str(session['url_id'])
				ioFile = BytesIO()
				ioFile.write(base64.b64decode(openBase64StringFromFile(PATH_TO_BASE64_TXT_FOLDER + url_id + '.txt', prefix + url_id)))
				ioFile.seek(0)
				selectedStyle = (await request.form)['stylize']
				
				#asyncio.get_running_loop().run_in_executor(None, await cpu_background_task(selectedStyle, ioFile, url_id))
				x = threading.Thread(target=thread_function, args=(selectedStyle, ioFile, url_id,))
				x.start()
				
				prefix = 'S' #Style
				return ("<!DOCTYPE html>"
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
                                    "<hr>"
                                    "<p><h2><a href='"+ START_URL + "showStyledPic/" + prefix + url_id +"'>Style-Pic</a></h2></p>"
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
                                                    "class='btn btn-warning'>"
                                                        "Upload new Picture"
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
                                "window.location.href='" + START_URL + "';"
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
				if doStyle == '2':
					url_id = str(session['url_id'])
					prefix = 'O' #Original
					img = openBase64StringFromFile(PATH_TO_BASE64_TXT_FOLDER + url_id + '.txt', prefix + url_id)
					del url_id
					del prefix
					return ("<!DOCTYPE html>"
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
                                        "window.location.href='" + START_URL + "';"
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


@app.route('/showStyledPic/<picID>', methods=['GET'])
async def ShowStylePic(picID):
	if request.method == 'GET':
		picID = str(picID)
		fileName = picID[1:]
		try:
			img = openBase64StringFromFile(PATH_TO_BASE64_TXT_FOLDER + fileName + '.txt', picID)
			return "<img id='inputPic' src='data:image/png;base64," + img + "' hspace='0'/>"
		except Exception as e:
			return str(e)


##Error-Messages:
@app.route('/FILE_UPLOAD_ERROR_NoFileSelected')
def file_upload_error_nofile():
	return (
	"<!doctype html>"
	"<title>Upload File ERROR - No File selected</title>"
	"<h1>No file selected</h1>"
	"<button onclick='goBack()'>Go Back</button>"
	"<script>"
	"function goBack() {"
	"window.location.href='" + START_URL + "';"
	"}"
	"</script>")

@app.route('/STYLE_ERROR_NoStyleSelected')
def style_error_nostyle():
	return (
	"<!doctype html>"
	"<title>Style ERROR - No Style selected</title>"
	"<h1>No style selected</h1>"
	"<button onclick='goBack()'>Go Back</button>"
	"<script>"
	"function goBack() {"
	"window.location.href='" + START_URL + "';"
	"}"
	"</script>")

@app.route('/FILE_UPLOAD_ERROR_NoJPGformat')
def file_upload_error_nojpg():
	return (
	"<!doctype html>"
	"<title>Upload File ERROR - No jpg Format</title>"
	"<h1>File needs to end with .jpg</h1>"
	"<button onclick='goBack()'>Go Back</button>"
	"<script>"
	"function goBack() {"
	"window.location.href='" + START_URL + "';"
	"}"
	"</script>")

@app.route('/GENERALERROR')
def generalError():
	return (
	"<!doctype html>"
	"<title>ERROR</title>"
	"<h1>Something went wrong!</h1>"
	"<button onclick='goBack()'>Go Back</button>"
	"<script>"
	"function goBack() {"
	"window.location.href='" + START_URL + "';"
	"}"
	"</script>")



if __name__ == '__main__':
	app.run()
