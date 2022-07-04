import cv2
from util import public_tools as tool
from util import io_tools as io
from service import recognize_service as rs
from service import hr_service as hr

#全局变量
ESC_KEY=27
ENTER_KEY=13

#打开摄像头进行登记
def regsiter(code):
    cameraCapture=cv2.VideoCapture(0)
    success,frame=cameraCapture.read()
    shooting_time=0
    while success:
        cv2.imshow('regsiter',frame)
        success,frame=cameraCapture.read()
        key=cv2.waitKey(1)
        if key==ESC_KEY:
            break
        if key==ENTER_KEY:
            photo=cv2.resize(frame,(io.IMG_WIDTH,io.IMG_HEIGHT))
            img_name=io.PIC_PATH+str(code)+str(tool.randomNumber(8))+'.png'
            cv2.imwrite(img_name,photo)
            shooting_time+=1
            if shooting_time==3:
                break
    cv2.destroyAllWindows()
    cameraCapture.release()
    io.load_employee_pic()

#打开摄像头打卡
def clock_in():
    cameraCapture=cv2.VideoCapture(0)
    success,frame=cameraCapture.read()
    while success and cv2.waitKey(1)==-1:
        cv2.imshow('check in',frame)
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        if rs.found_face(gray):
            gray=cv2.resize(gray,(io.IMG_WIDTH,io.IMG_HEIGHT))
            code=rs.recognise_face(gray)
            if code!=-1:
                name=hr.get_name_with_code(code)
                if name!=None:
                    cv2.destroyAllWindows()
                    cameraCapture.release()
                    return name
        success,frame=cameraCapture.read()
    cv2.destroyAllWindows()
    cameraCapture.release()