import io
import cv2
# from flask import Flask, request, jsonify, json, redirect, render_template, send_file, session, url_for
from flask import Flask, request, send_file
from flask_cors import CORS
import asyncio
import main
import os

loop = asyncio.get_event_loop()
app = Flask(__name__)
CORS(app)
import main

global mezuza_name

@app.route('/upload-file', methods=['POST'])
def uploadFile():
    global mezuza_name
    my_file = request.files['image']
    print(type(my_file))
    print(my_file.filename)
    my_file.save(f'./{my_file.filename}')
    main.MainFunc(f'./{my_file.filename}')

    mezuza_name = os.path.splitext(my_file.filename)[0]
    mezuza_name = os.path.basename(mezuza_name)
    print(mezuza_name)

    return 'http://127.0.0.1:8887' + fr'/images/results/{mezuza_name}.pdf'

# to use it we need to install pip install aioflask
@app.route("/download" , methods=['GET'])
async def get_file():
    global mezuza_name
    mezuza_name = os.path.splitext(mezuza_name)[0]
    mezuza_name = os.path.basename(mezuza_name)
    try:
       return send_file(fr'images/results/{mezuza_name}.pdf', attachment_filename='results.pdf',as_attachment=True)#משהו טוב

    except Exception as e:
        return str(e)


@app.get("/")
async def root():
    return {
        "message2": "welcome to my project"
    }


if __name__ == '__main__':
    asyncio.run(root())
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)
