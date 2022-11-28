import cv2
from model import FallDetectionModel

def model_test():
    model_instance = FallDetectionModel('./pretrained/best.pt')
    test_image = cv2.imread('assets/fall.jpg')
    test_image_rendered, test_image_detected = model_instance.interfere(test_image)
    print(test_image_detected)
    cv2.imshow('test model', test_image_rendered)
    cv2.waitKey(0)
    cv2.destroyWindow('test model')


if __name__ == '__main__':
    model_test()
