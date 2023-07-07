import pyzed.sl as sl
import cv2
import math



#initialise and start the camera
def zed_init(resolution = sl.RESOLUTION.HD1080, fps = 30):
    
    # Set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = resolution
    init_params.camera_fps = fps
    return init_params


def zed_rgb(zed, show_image = False):
    # Create an RGBA sl.Mat object
    image_zed = sl.Mat(zed.get_camera_information().camera_configuration.resolution.width, zed.get_camera_information().camera_configuration.resolution.height, sl.MAT_TYPE.U8_C4)
    # Retrieve data in a numpy array with get_data()
    image_ocv = image_zed.get_data()
    if zed.grab() == sl.ERROR_CODE.SUCCESS :
        # Retrieve the left image in sl.Mat
        zed.retrieve_image(image_zed, sl.VIEW.LEFT)
        # Use get_data() to get the numpy array
        image_ocv = image_zed.get_data()
    rgb = cv2.cvtColor(image_ocv, cv2.COLOR_BGR2RGB)
    return image_ocv, rgb

def zed_depth(zed, x = None, y = None):
    if (x is not None and y is not None):
        depth_zed = sl.Mat(zed.get_camera_information().camera_configuration.resolution.width, zed.get_camera_information().camera_configuration.resolution.height, sl.MAT_TYPE.F32_C1)
        if zed.grab() == sl.ERROR_CODE.SUCCESS :
            # Retrieve depth data (32-bit)
            zed.retrieve_measure(depth_zed, sl.MEASURE.DEPTH)
            # Load depth data into a numpy array
            depth_ocv = depth_zed.get_data()
            # Print the depth value at the center of the image
            print(depth_ocv[y][x])
            point_cloud = sl.Mat()
            zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA)
            point3D = point_cloud.get_value(x, y)
            x_dist = point3D[1][0]
            y_dist = point3D[1][1]
            z_dist = point3D[1][2]
            color = point3D[1][3]
            print("X = ", x_dist, "\nY = ", y_dist, "\nZ = ", z_dist)
            rad = math.sqrt(x_dist**2 + y_dist**2 + z_dist**2)
            print("Distance = ", rad) 