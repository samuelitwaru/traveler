import cv2

def crop_image(image_path, x,y,w,h):
    img = cv2.imread(image_path)
    crop_img = img[y:y+h, x:x+w]
