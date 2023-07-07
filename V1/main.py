import machine_vision as mv
import zed_api as zed
import pyzed.sl as sl
import cv2

global zed_invoke #object of zed camera

#Start ZED
def zed_start(init_params):
    
    global zed_invoke
    zed_invoke= sl.Camera()
    # Open the camera
    err = zed_invoke.open(init_params)
    print("Camera Started")

    if err != sl.ERROR_CODE.SUCCESS:
        print("Error {}, exit program".format(err)) # Display the error
        exit()
    return zed_invoke

def zed_close():
    zed_invoke.close()
    print("Camera Closed")

param = zed.zed_init()
cam = zed_start(param)
print("Invoking detection model model")
detection_model = mv.model()

while(True):
    image_ocv, rgb  = zed.zed_rgb(cam)

    response, x, y, x1, y1, x2, y2 = detection_model.objdet_init(rgb)
    
    if response:
        cv2.rectangle(image_ocv, (x1, y1), (x2, y2), (255, 255, 255), thickness=2)
        cv2.circle(image_ocv, (x, y), 2, (0, 123, 222), 5)
        

    cv2.imshow("Image", image_ocv)
    stroke = cv2.waitKey(1)

    if response:
        zed.zed_depth(cam, x, y)

    if stroke == 27:
        zed_close()
        cv2.destroyAllWindows()
        break