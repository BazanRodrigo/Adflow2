import numpy as np
import time
import os
from flask import Flask, request, Response, jsonify, render_template
from werkzeug.utils import secure_filename
import io
from PIL import Image
import cv2
from corrector import extract_text
from paletronic import study_image

# construct the argument parse and parse the arguments
#sudo apt-get install libhunspell-dev
#wget 'https://www.dropbox.com/s/q2f2wnw6708iulf/AdFlow.weights?dl=0' -O AdFlow.weights

predictionNichos = []
ext = ''
corr = ''
diccionario = {'Datos Extraidos':[{'Nichos':'', 'Texto Extraido':'', 'Texto Sugerido':''}]}
labelsPath="adflowXyolo/obj.names"
cfgpath="adflowXyolo/yolov4.cfg"
wpath="adflowXyolo/AdFlow.weights"
confthres = 0.3
nmsthres = 0.1
yolo_path = 'adflowXyolo'

def get_labels(labels_path):
    # This is to load the labels to make the prediction
    lpath=labels_path
    LABELS = open(lpath).read().strip().split("\n")
    return LABELS

def get_colors(LABELS):
    # initialize a list of colors to represent each possible class label
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),dtype="uint8")
    return COLORS

def load_model(configpath,weightspath):
    # load our YOLO object detector trained on COCO dataset (80 classes)
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configpath, weightspath)
    return net

def image_to_byte_array(image:Image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

def get_time():
    tiempo_segundos = time.time()
    tiempocadena = str(time.ctime(tiempo_segundos))
    tiempo = tiempocadena.replace(':','-')
    file = tiempo + '.json'
    imagen = tiempo + '.jpg'
    imagenOut = tiempo + '.png'
    paletaOut = 'paleta'+tiempo +'.png'
    txtOut = os.path.join('static/Outputs' , file)
    imgOut = os.path.join('static/Outputs', imagenOut)
    paletOut = os.path.join('static/Outputs', paletaOut)
    txtIn = os.path.join('Inputs' , file)
    imgIn = os.path.join('Inputs', imagen)
    datos = [txtOut, imgOut, txtIn, imgIn, paletOut]
    return datos

txtOut = get_time()[0]
imgOut = get_time()[1]
io = imgOut
imgIn =  get_time()[3]
paletOut = get_time()[4]

def get_predection(image,net,LABELS,COLORS):    
    f = open(txtOut,'w')
    f.close()
    (H, W) = image.shape[:2]

    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # construct a blob from the input image and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes and
    # associated probabilities
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    #print(layerOutputs)
    end = time.time()

    # show timing information on YOLO
    print("[INFO] YOLO took {:.6f} seconds".format(end - start))

    # initialize our lists of detected bounding boxes, confidences, and
    # class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []
    predictionNichos.clear()
    

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > confthres:
                # scale the bounding box coordinates back relative to the
                # size of the image, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use the center (x, y)-coordinates to derive the top and
                # and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # update our list of bounding box coordinates, confidences,
                # and class IDs
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    # apply non-maxima suppression to suppress weak, overlapping bounding
    # boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confthres, nmsthres)

    # ensure at least one detection exists
    if len(idxs) > 0:
        # loop over the indexes we are keeping
        for i in idxs.flatten():
            # extract the bounding box coordinates
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            # draw a bounding box rectangle and label on the image
            color = [int(c) for c in COLORS[classIDs[i]]]
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)            
            if len(LABELS[classIDs[i]]) != 0:                
                predictionNichos.append(str(LABELS[classIDs[i]])+' ('+str(boxes[i][0]) +', '+ str(boxes[i][1])+', '+str(boxes[i][2])+', '+ str(boxes[i][3])+')')                
                text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 2)
                cv2.imwrite(imgOut, image)
    else:
        cv2.imwrite(imgOut, image)
    #diccionario = {'Nicho': predictionNichos}    
    cadenaNichos = ''
    cadenaNichos = cadenaNichos.join(predictionNichos)            
    diccionario["Datos Extraidos"][0] = str(predictionNichos)
    out_txt, ext, corr = extract_text(imgOut, 'eng', 'L', 2, diccionario, get_time()[0])        
    
    return image, cadenaNichos,ext, corr



Lables=get_labels(labelsPath)   
nets=load_model(cfgpath,wpath)
Colors=get_colors(Lables)
# Initialize the Flask application
app = Flask(__name__)
@app.route("/")
def upload_file():
    # renderiamos la plantilla "formulario.html"    
    return render_template('formulario.html')

app.config['UPLOAD_FOLDER'] = './Inputs'

def treat_as_plain_text(response):
    response.headers["content-type"] = "text/plain"
    return response

# route http posts to this method
#@app.route('/upload', methods=['POST'])
@app.route('/upload', methods=['POST'])

def main():
    # load our input image and grab its spatial dimensions    
    if request.method == 'POST':
        # obtenemos el archivo del input "archivo"
        f = request.files['archivo']
        filename = secure_filename(f.filename)
        # Guardamos el archivo en el directorio
        f.save(imgIn)
        # Retornamos una respuesta satisfactoria     
        study_image(imgIn)   
        img = Image.open(imgIn)
        npimg=np.array(img)
        image=npimg.copy()
        image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        res, cadenaN,ext, corr, =get_predection(image,nets,Lables,Colors)
        po = '../' + paletOut
        imgOut = '../' + io              
        print('Se detectaron ', len(corr), ' palabras')
        
    return render_template('fetch.html', nicho=cadenaN, 
    TextoExtraido=ext, TextoSugerido=corr, img=imgOut, po=po,
    npalabras = len(corr))
    

    # start flask app
    #     
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=8080, ssl_context="adhoc")
    #app.run(debug=False)
#https://medium.com/analytics-vidhya/object-detection-using-yolo-v3-and-deploying-it-on-docker-and-minikube-c1192e81ae7a
