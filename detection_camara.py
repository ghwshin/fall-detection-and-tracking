import time

import cv2
from model import FallDetectionModel
from control_motor import MotorControler

class DetectionCamara:
    def __init__(self, model_path):
        self.video_source = '/dev/video0'
        self.view_name = 'Fall Detection'
        self.cam = None
        self.rval = None
        self.frame = None
        self.width = None
        self.height = None
        self.frame_number = 0
        self.model = FallDetectionModel(model_path)
        self.motor = MotorControler()

    def cam_init(self):
        cv2.namedWindow(self.view_name)
        self.cam = cv2.VideoCapture(self.video_source)
        if self.cam.isOpened():
            self.rval, self.frame = self.cam.read()
            self.width = self.cam.get(3)
            self.height = self.cam.get(4)
            print(f'Camara Started! {self.width} X {self.height}')

            self.motor.start_motor()
        else:
            print('Camara Failed!')
            self.rval = False

        return self.rval

    def read_and_detect_frame(self):
        while self.rval:
            self.rval, self.frame = self.cam.read()
            self.frame_number += 1
            after_img, detected_infos = self.detection(self.frame)

            if self.frame_number % 10 == 0:
                b_center = self.bbox_to_midpoint(detected_infos)
                self.rotate(b_center)

            cv2.imshow(self.view_name, after_img)
            key = cv2.waitKey(20)
            if key == 27: # ESC key
                break

    def detection(self, before_frame):
        after_frame_img, detection_infos = self.model.interfere(before_frame)
        return after_frame_img, detection_infos

    def bbox_to_midpoint(self, det):
        if len(det) > 0:
            val = det.values[0]
            mid_x = (int(val[0]) + int(val[2])) // 2
            mid_y = (int(val[1]) + int(val[3])) // 2
            return mid_x, mid_y
        else:
            return self.width // 2, self.height // 2

    def rotate(self, bbox_center):
        # x 좌표만 계산 (y축 적용 x)
        # 오차 추가하기
        center = (self.width // 2, self.height // 2)
        if bbox_center[0] > center[0]:
            # print('turn right!')
            self.motor.moving_motor(False)
            time.sleep(0.05)
        elif bbox_center[0] < center[0]:
            self.motor.moving_motor(True)
            time.sleep(0.05)
        else:
            self.motor.stop_motor()


    def end_cam(self):
        self.motor.end_motor()
        if self.cam.isOpened():
            self.cam.release()
        cv2.destroyWindow(self.view_name)