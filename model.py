import torch

class FallDetectionModel:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = self.get_model()

    def get_model(self):
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=self.model_path)
        return model

    def interfere(self, frame):
        interfered = self.model(frame)
        interfered.render()
        return (interfered.ims[0], interfered.pandas().xyxy[0])