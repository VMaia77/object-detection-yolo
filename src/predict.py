import numpy as np
import cv2
from ultralytics import YOLO
from PIL import Image
from os.path import splitext

from src.api.error_handlers import InvalidImage
from src.api.endpoint_template import endpoint_template

from src.api.configs import ALLOWED_EXTENSIONS



def allowed_file(filename):
    return '.' in filename and splitext(filename)[1].lower()[1:] in ALLOWED_EXTENSIONS


def load_yolo_model(model_path):
    return YOLO(model_path) 


def yolo_predict(_model: YOLO, img: np.ndarray):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    prediction = _model(img)
    return prediction[0]


def yolo_predict_img(_model: YOLO, img: np.ndarray, threshold = 0.5):
    prediction = yolo_predict(_model, img)
    for result in prediction.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        if score > threshold:
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(img, prediction.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
    return img


@endpoint_template
def yolo_api_prediction(input_instance, _model, file):
    threshold = input_instance.threshold
    detected_objects_cls = []
    assert allowed_file(file.filename), InvalidImage().to_dict()
    img = Image.open(file.file)
    img_array = np.array(img)
    prediction = yolo_predict(_model, img_array)
    for result in prediction.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        if score > threshold:
            detected_objects_cls += prediction.names[int(class_id)].upper(),
    output = {'detected_objects_cls': detected_objects_cls}
    return output
