from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask import Flask,flash,request,redirect,send_file,render_template
import cv2, random, os


UPLOAD_FOLDER = 'uploads/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def dogdeV(x,y):
        return cv2.divide(x, 255 - y, scale = 256)

def transformation(uploaded_file):
    img = cv2.imread(uploaded_file)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_invert = cv2.bitwise_not(img_gray)
    img_smoothing = cv2.GaussianBlur(img_invert, (21,21), sigmaX= 0, sigmaY=0)
    final_img = dogdeV(img_gray, img_smoothing)
    filename = 'sketch' + str(random.randint(1,100)) + '.png'
    cv2.imwrite("uploads/"+filename, final_img)
    return filename

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            uploaded_file = transformation("uploads/"+filename)
            print("saved file successfully")
      #send file name as parameter to downlad
            return redirect('/downloadfile/'+ uploaded_file)
    return render_template('upload.html')

@app.route("/downloadfile/<filename>", methods = ['GET'])
def download_file(filename):
    return render_template('download.html',value=filename)

@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = UPLOAD_FOLDER + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')

if __name__ == '__main__':
   app.run(debug = True)