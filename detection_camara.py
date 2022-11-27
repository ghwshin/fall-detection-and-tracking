import cv2
from model import FallDetectionModel

class DetectionCamara:
    def __init__(self, model_path):
        self.video_source = '/dev/video0'
        self.view_name = 'Fall Detection'
        self.cam = None
        self.rval = None
        self.frame = None
        self.model = FallDetectionModel(model_path)

    def cam_init(self):
        cv2.namedWindow(self.view_name)
        self.cam = cv2.VideoCapture(self.video_source)
        if self.cam.isOpened():
            self.rval, self.frame = self.cam.read()
            print('Camara Started!')
        else:
            print('Camara Failed!')
            self.rval = False

        return self.rval

    def read_and_detect_frame(self):
        while self.rval:
            self.rval, self.frame = self.cam.read()
            after_img, detected_infos = self.detection(self.frame)
            cv2.imshow(self.view_name, after_img)
            key = cv2.waitKey(20)
            if key == 27: # ESC key
                break

    def detection(self, before_frame):
        after_frame_img, detection_infos = self.model.interfere(before_frame)
        return after_frame_img, detection_infos

    def end_cam(self):
        if self.cam.isOpened():
            self.cam.release()
        cv2.destroyWindow(self.view_name)