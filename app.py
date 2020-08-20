from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask import send_file
import cv2, random
app = Flask(__name__)

def dogdeV(x,y):
        return cv2.divide(x, 255 - y, scale = 256)

def transformation(uploaded_file):
    img = cv2.imread(uploaded_file)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_invert = cv2.bitwise_not(img_gray)
    img_smoothing = cv2.GaussianBlur(img_invert, (21,21), sigmaX= 0, sigmaY=0)
    final_img = dogdeV(img_gray, img_smoothing)
    filename = 'sketch' + str(random.randint(1,100)) + '.png'
    cv2.imwrite(filename, final_img)
    return filename




@app.route('/')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['POST'])
def success():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      uploaded_file = transformation(f.filename)  
      return send_file(upload_file, as_attachment=True)



if __name__ == '__main__':
   app.run(debug = True)