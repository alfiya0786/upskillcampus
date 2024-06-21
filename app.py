from flask import Flask, request, render_template_string
import pymysql
import boto3

app = Flask(__name__)

db = pymysql.connect(
    host='mydbinstance.xxxxxxxxxx.us-east-1.rds.amazonaws.com',
    user='admin',
    password='Ask1234',
    database='healthcare'
)

s3_client = boto3.client('s3')

@app.route('/')
def index():
    return render_template_string('''
    <h2>Patient Registration Form</h2>
    <form method="post" action="/register">
        Name: <input type="text" name="name"><br>
        Date of Birth: <input type="date" name="dob"><br>
        Gender: <input type="text" name="gender"><br>
        Address: <input type="text" name="address"><br>
        <input type="submit">
    </form>

    <h2>Upload Medical Record</h2>
    <form method="post" action="/upload" enctype="multipart/form-data">
        Select file to upload:
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    ''')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    dob = request.form['dob']
    gender = request.form['gender']
    address = request.form['address']

    cursor = db.cursor()
    sql = "INSERT INTO patients (name, date_of_birth, gender, address) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (name, dob, gender, address))
    db.commit()
    return "New record created successfully"

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file_name = file.filename
    file_path = '/tmp/' + file_name
    file.save(file_path)

    s3_client.upload_file(file_path, 'my-healthcare-data', file_name)
    return "File uploaded successfully. File URL: " + s3_client.generate_presigned_url('get_object', Params={'Bucket': 'my-healthcare-data', 'Key': file_name}, ExpiresIn=3600)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
