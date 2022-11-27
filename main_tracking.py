from detection_camara import DetectionCamara

if __name__ == '__main__':
    cam = DetectionCamara('pretrained/best.pt')
    if cam.cam_init():
        cam.read_and_detect_frame()
        cam.end_cam()
    else:
        print('error : invaild frame')
    print('finished detection.')