from ultralytics import YOLO as yolo
import os

#os.environ['KMP_DUPLICATE_LIB_OK']='True'

if __name__ == '__main__':
    eight='yolov8n.pt'
    version='C:/Users/CAU/Desktop/Alert/runs/detect/train2/weights/best.pt'
    model = yolo(eight)
    model.train(data='C:/Users/CAU/Desktop/Alert/yolov8/data.yaml', epochs=20, workers=0)
    #model.predict(source='C:/Users/CAU/Desktop/Alert/yolov8/valid/images', save=True, conf=0.5, show=True)

    print('done')
