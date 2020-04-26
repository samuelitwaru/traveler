import cv2
import os
from application import app


def crop_image(image_path, crop_path, x,y,w,h):
    img = cv2.imread(image_path)
    crop_img = img[y:y+h, x:x+w]
    cv2.imwrite(crop_path, crop_img)


def name_file():
    print(app.config["UPLOADS_FOLDER"])