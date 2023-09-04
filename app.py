import streamlit as st
import cv2
import numpy as np
import skimage.exposure

st.set_page_config(layout='wide')

# Streamlit UI
st.title("Green Color Range Adjustment")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])

option = st.sidebar.radio('Select the Method', ['Method-I', 'Method-II'])

if option == 'Method-I' and uploaded_file is not None:
# if uploaded_file is not None:
    # Read and display the uploaded image
    col1, col2 = st.columns(2)
    image = cv2.imread(uploaded_file.name)
    col1.image(image, channels="BGR", caption="Uploaded Image", use_column_width=True)

    # Sliders to adjust green color range
    lower_hue = st.sidebar.slider("Lower Hue", 0, 180, 35)
    upper_hue = st.sidebar.slider("Upper Hue", 0, 180, 85)
    lower_saturation = st.sidebar.slider("Lower Saturation", 0, 255, 50)
    upper_saturation = st.sidebar.slider("Upper Saturation", 0, 255, 255)
    lower_value = st.sidebar.slider("Lower Value", 0, 255, 50)
    upper_value = st.sidebar.slider("Upper Value", 0, 255, 255)

    # Convert image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create mask based on green color range
    lower_green = np.array([lower_hue, lower_saturation, lower_value])
    upper_green = np.array([upper_hue, upper_saturation, upper_value])
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # Invert the green mask to get the non-green region
    non_green_mask = cv2.bitwise_not(green_mask)

    # Create an empty image with a white background
    white_background = np.full_like(image, (255, 255, 255))

    # Apply the mask to the original image
    result_image = cv2.bitwise_and(white_background, white_background, mask=green_mask)
    result_image += cv2.bitwise_and(image, image, mask=non_green_mask)

    # Display the adjusted image
    col2.image(result_image, channels="BGR", caption="Adjusted Image", use_column_width=True)

if option == 'Method-II' and uploaded_file is not None:
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    image = cv2.imread(uploaded_file.name)
    col1.image(image, channels="BGR", caption="Uploaded Image", use_column_width=True)

    # convert to LAB
    lab = cv2.cvtColor(image,cv2.COLOR_BGR2LAB)

    # extract A channel
    A = lab[:,:,1]

    thrs = st.sidebar.slider("THRESH", 0, 500, 0)
    maxv = st.sidebar.slider("MAXVAL", 0, 500, 255)
    # threshold A channel
    thresh = cv2.threshold(A, thrs, maxv, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1] ## threshold(src, thresh, maxval, type[, dst]) -> retval, dst

    csx, csy = st.columns(2)
    # blur threshold image
    SIGMAX = st.sidebar.number_input("SigmaX", 0, 500, 5)
    SIGMAY = st.sidebar.number_input("SigmaY", 0, 500, 5)
    blur = cv2.GaussianBlur(thresh, (0,0), sigmaX=SIGMAX, sigmaY=SIGMAY, borderType = cv2.BORDER_DEFAULT)
    
    # stretch so that 255 -> 255 and 127.5 -> 0
    inraga = st.sidebar.number_input("In Range-A",0.0,  255.0, 127.5) 
    inragb = st.sidebar.number_input("In Range-B", 0, 255, 255)
    outrnga = st.sidebar.number_input("Out Range-A", 0.0,  255.0, 0.0)
    outrngb = st.sidebar.number_input("Out Range-B", 0, 255, 255)
    mask = skimage.exposure.rescale_intensity(blur, in_range=(inraga,inragb), out_range=(outrnga,outrngb)).astype(np.uint8)
    
    # add mask to image as alpha channel
    result = image.copy()
    result = cv2.cvtColor(image,cv2.COLOR_BGR2RGBA)
    result[:,:,3] = mask

    # # save output
    # cv2.imwrite('greenscreen_thresh.png', thresh)
    # cv2.imwrite('greenscreen_mask.png', mask)
    # cv2.imwrite('greenscreen_antialiased.png', result)

    # Display the adjusted image
    col2.image(result, caption="Green Screen Antialiased Image", use_column_width=True)

    # Display the adjusted image
    # col3.image(mask,caption="Green Screen Mask Image", use_column_width=True)

    # Display the adjusted image
    # col4.image(thresh, caption="Green Screen Thresh Image", use_column_width=True)