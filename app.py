from flask import Flask, render_template, request
import boto3
import requests
import os

app = Flask(__name__)

BUCKET_NAME = os.getenv('BUCKET_NAME')

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)

        img_id = f.filename
        print(img_id)
        s3 = boto3.resource('s3')
        s3.Bucket(BUCKET_NAME).upload_file(img_id, f'uploads/{img_id}.jpg', ExtraArgs={'ACL': 'public-read'})

        img_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/uploads/{img_id}.jpg"

        data = {"img_url": img_url, "img_id": img_id}
        url = 'http://host.docker.internal:5000/v1/predict'

        response = requests.post(url, json=data)
        response_json = response.json()

        print(response_json)
        prediction = response_json["prediction"]
    else:
        prediction = (
        "                                 ...,**//////**,,...                               \n" +
        "                       .,**///(((/**,,,,,,.           .,**,,.                      \n" +
        "                  .,/(/,.                                   .*/*.                  \n" +
        "               .*//,.                         .,..,/%&&&%%%%#///((/,.              \n" +
        "           .,*/*,. ..,,*//,.                  .,***,..  ...,/(#/*/(#(*.            \n" +
        "       .,*/*,,*/#%&&%(/,..                  .,,..             .,***/(#/.           \n" +
        "     .*//,..*(%##(//*,.....,,,,,.          .,*,.     ,(%@@&(,    .,,,,/#(*.        \n" +
        "   ..,***.   .,,,    ./%&%#/,..,*//*.        .,*,.    ..,,,.      .**.,/((/*.      \n" +
        "  ,*//*,.    ,**,.  .,(&@@%(,...***.            ..***,,,.......,,**,.   ,*/(/,.    \n" +
        " .,/((*.      .**.         .,*/*.                                        .*((/,    \n" +
        " .,/(/,.       .,***,,,,,,*,.            ,,..,**,.                        ,*((,    \n" +
        "  .,//.                                 .**,  ..**.                       .,**.    \n" +
        "   .,*,.                                  .,*****,.             .,,.      ..,.     \n" +
        "      ....                                                  .,,,,.                 \n" +
        "                         .,,,..                     ..,,,,,..                      \n" +
        "                               ..,,*****/**************,..                         \n" +
        "                                         .......                                   \n"
        )#Чел ты...
    return render_template('result.html', result=prediction)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
