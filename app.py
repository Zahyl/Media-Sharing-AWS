from flask import Flask, render_template, request, redirect, flash, url_for, Response
import boto3
from io import BytesIO
from PIL import Image

app = Flask(__name__, template_folder='/home/ec2-user/project/templates')
app.secret_key = 'justakey'

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1') #change your region if needed.
table = dynamodb.Table('<enter your dynamodb table name>')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        location = request.form['location']
        file = request.files['file']
        s3.upload_fileobj(file, '<enter your s3 bucket name>', file.filename)

        # add metadata to DynamoDB table 
        key = file.filename
        table.put_item(
            Item={
                'id': key,
                'name': name,
                'description': description,
                'location': location
            }
        )

        flash('File uploaded successfully')
        return redirect('/')
    else:
        try:
            objects = s3.list_objects(Bucket='<enter your s3 bucket name>')['Contents']
            files = []
            for obj in objects:
                if obj['Key'].endswith('.jpg') or obj['Key'].endswith('.png'):
                    url = url_for('thumbnail', key=obj['Key'])
                    # retrieving metadata from DynamoDB
                    response = table.get_item(
                        Key={
                            'id': obj['Key']
                        }
                    )
                    name = response['Item']['name']
                    description = response['Item']['description']
                    location = response['Item']['location']
                    files.append({'key': obj['Key'], 'url': url, 'name': name, 'description': description, 'location': location})
        except:
            files = []
        return render_template('index.html', files=files)

@app.route('/delete', methods=['POST'])
def delete_file():
    key = request.form['key']
    s3.delete_object(Bucket='<enter your s3 bucket name>', Key=key)
    # deleting metadata from Dynamo db
    table.delete_item(
        Key={
            'id': key
        }
    )
    flash('File deleted successfully')
    return redirect('/')

@app.route('/thumbnail/<key>')
def thumbnail(key):
    response = s3.get_object(Bucket='<enter your s3 bucket name>', Key=key)
    image = Image.open(BytesIO(response['Body'].read()))
    image.thumbnail((200, 200))
    image = image.convert('RGB')
    with BytesIO() as output:
        image.save(output, format='JPEG')
        contents = output.getvalue()
    return Response(contents, mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
