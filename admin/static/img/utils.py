import cv2

image_path = 'me.jpg'

def crop_image(image_path, x,y,w,h):
    img = cv2.imread(image_path)
    print(img.shape)
    crop_img = img[y:y+h, x:x+w]
    cv2.imwrite('crop.png', crop_img)
    
crop_image(image_path, 0, 0, 500, 500)
