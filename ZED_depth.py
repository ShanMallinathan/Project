import pyzed.sl as sl
import cv2
import math
zed = sl.Camera()
# Set configuration parameters
init_params = sl.InitParameters()
init_params.camera_resolution = sl.RESOLUTION.HD1080
init_params.camera_fps = 30

# Open the camera
err = zed.open(init_params)
if err != sl.ERROR_CODE.SUCCESS:
    print("Error {}, exit program".format(err)) # Display the error
    exit()

cv2.namedWindow("Image")
x_coord = None
y_coord = None
def mouse_callback(event, x, y, flags, param):
    global coord, y_coord
    if event == cv2.EVENT_LBUTTONDOWN:
        # Create a sl.Mat with float type (32-bit)
        depth_zed = sl.Mat(zed.get_camera_information().camera_configuration.resolution.width, zed.get_camera_information().camera_configuration.resolution.height, sl.MAT_TYPE.F32_C1)
        if zed.grab() == sl.ERROR_CODE.SUCCESS :
            # Retrieve depth data (32-bit)
            zed.retrieve_measure(depth_zed, sl.MEASURE.DEPTH)
            # Load depth data into a numpy array
            depth_ocv = depth_zed.get_data()
            # print(x, y)
            # Print the depth value at the center of the image
            # print(depth_ocv[y][x])
            point_cloud = sl.Mat()
            zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA)
            point3D = point_cloud.get_value(x, y)
            x_dist = point3D[1][0]
            y_dist = point3D[1][1]
            z_dist = point3D[1][2]
            color = point3D[1][3]
            # print("X = ", x_dist, "\nY = ", y_dist, "\nZ = ", z_dist)
            rad = math.sqrt(x_dist**2 + y_dist**2 + z_dist**2)
            print("Distance = ", rad)



while(True):
    # Create an RGBA sl.Mat object
    image_zed = sl.Mat(zed.get_camera_information().camera_configuration.resolution.width, zed.get_camera_information().camera_configuration.resolution.height, sl.MAT_TYPE.U8_C4)
    # Retrieve data in a numpy array with get_data()
    image_ocv = image_zed.get_data()
    cv2.namedWindow("Left", cv2.WINDOW_NORMAL)
    if zed.grab() == sl.ERROR_CODE.SUCCESS :
        # Retrieve the left image in sl.Mat
        zed.retrieve_image(image_zed, sl.VIEW.LEFT)
        # Use get_data() to get the numpy array
        image_ocv = image_zed.get_data()
        # Display the left image from the numpy array
        cv2.imshow("Left", image_ocv)
        # Create an RGBA sl.Mat object
    image_depth_zed = sl.Mat(zed.get_camera_information().camera_configuration.resolution.width, zed.get_camera_information().camera_configuration.resolution.height, sl.MAT_TYPE.U8_C4)
    if zed.grab() == sl.ERROR_CODE.SUCCESS :
        # Retrieve the normalized depth image
        zed.retrieve_image(image_depth_zed, sl.VIEW.DEPTH)
        # Use get_data() to get the numpy array
        image_depth_ocv = image_depth_zed.get_data()
        # print(image_depth_ocv.shape)
        cv2.setMouseCallback("Left", mouse_callback)
        # Display the depth view from the numpy array
        # cv2.imshow("Image", image_depth_ocv)
        if(cv2.waitKey(1) == 27):
            cv2.destroyAllWindows()
            zed.close()
            break