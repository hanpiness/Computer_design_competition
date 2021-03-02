from flask import Flask, request, render_template, jsonify
from PIL import Image
from yolo import YOLO
from PIL import Image

app = Flask(__name__)
labels = []
def return_img_stream(img_local_path):
  """
  工具函数:
  获取本地图片流
  :param img_local_path:文件单张图片的本地绝对路径
  :return: 图片流
  """
  import base64
  img_stream = ''
  with open(img_local_path, 'rb') as img_f:
    img_stream = img_f.read()
    img_stream = base64.b64encode(img_stream)
  return img_stream

@app.route('/')
def index():
    return "123"


@app.route('/submit', methods=['GET','POST'])
def send_img():
    f = request.files['content']
    f.save('1.jpg')
    yolo = YOLO()

    img = f

    try:
        image = Image.open(img)
    except:
        print('Open Error! Try again!')
    else:
        r_image, label = yolo.detect_image(image)
        labels.clear()
        for i in label:
            labels.append(i)
        r_image.save("img.jpg")
    img_path = "img.jpg"
    img_stream = return_img_stream(img_path)
    return img_stream
@app.route('/label', methods=['GET'])
def label():
    lables = {}
    j = 0
    for i in labels:
        lables[j] = i
        j = j + 1
        print(i)
    return jsonify(lables)

if __name__ == '__main__':
    app.run()