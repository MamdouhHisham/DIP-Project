import cv2
import numpy as np
import imutils

def apply_filter_to_image(image, filter_name, param=None):
    if filter_name == "Grayscale":
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    elif filter_name == "Binary":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        return binary
    
    elif filter_name == "RGB":
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    elif filter_name == "HSV":
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    elif filter_name == "Rotate":
        return imutils.rotate(image, angle=param)
    
    elif filter_name == "Resize":
        if param is None or param <= 0:
            raise ValueError("Resize must be greater than 0")
        height = int(image.shape[0] * param)
        width = int(image.shape[1] * param)
        return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    
    elif filter_name == "Histogram Equalization":
        ## technique for improving the appearance of a poor image
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.equalizeHist(gray_img)
    
    elif filter_name == "Average Filter":
        # It is used in reduction of the detail in image. All coefficients are equal.
        return cv2.blur(image, (5, 5))
    
    elif filter_name == "Weighted Filter":
        #  pixels are multiplied by different coefficients. Center pixel is multiplied by a higher value than average filter.
        kernel = 1 / 16 * np.array([
            [1, 2, 1],
            [2, 4, 2],
            [1, 2, 1]
        ])
        return cv2.filter2D(image, kernel)
    
    elif filter_name == "Gaussian Filter":
        return cv2.GaussianBlur(image, (5, 5), 0) 
    
    elif filter_name == "Median Filter":
        # Each pixel in the image is considered. First neighboring pixels are sorted, and original values of the pixel is replaced by the median of the list
        return cv2.medianBlur(image, 5)
    
    elif filter_name == "Minimum Filter":
        # The value of the center is replaced by the smallest value in the window
        kernel = np.ones((3, 3), np.uint8)
        return cv2.erode(image, kernel)
    
    elif filter_name == "Maximum Filter":
        # The value of the center is replaced by the largest value in the window
        kernel = np.ones((3, 3), np.uint8)
        return cv2.dilate(image, kernel)
    
    elif filter_name == "Laplacian Filter":
        return cv2.Laplacian(image, -1, ksize=5) 
    
    elif filter_name == "LOG Filter":
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gauss_img = cv2.GaussianBlur(gray_img, (3, 3), 0)
        filtered_img = cv2.Laplacian(gauss_img, -1, ksize=5)
        return filtered_img
    
    elif filter_name == "Sharpening Filter":
        kernel = np.array([[-1, -1, -1],
                           [-1, 9, -1],
                           [-1, -1, -1]])
        return cv2.filter2D(image, -1, kernel)
    
    else:
        raise ValueError("Invalid filter selected. Available filters: Grayscale, Binary, RGB, HSV, Rotate, Resize, Histogram Equalization, Average Filter, Weighted Filter, Gaussian Filter, Median Filter, Minimum Filter, Maximum Filter, Laplacian Filter, LOG Filter, Sharpening Filter.")
