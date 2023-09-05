import streamlit as st
import cv2
import numpy as np
import skimage.exposure

st.set_page_config(layout='wide')

# Streamlit UI
st.title("Remove Image Background")

option = st.sidebar.selectbox('SELECT BACKGROUND COLOR', ['GREEN', 'BLUE', 'OTHERS'])
if option == 'GREEN':
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])
    if uploaded_file is not None:
        x=1
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)
        col1, col2 = st.columns(2)
        col1.image(image, channels="BGR", caption="Uploaded Image", use_column_width=True)
        lab = cv2.cvtColor(image,cv2.COLOR_BGR2LAB)
        channel = lab[:,:,x]
        thcol, maxcol = st.sidebar.columns(2)
        with thcol:
            thrs = st.slider("THRESH", 0, 500, 0)
        with maxcol:
            maxv = st.slider("MAXVAL", 0, 500, 255)
        thresh = cv2.threshold(channel, thrs, maxv, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    
        csx, csy = st.sidebar.columns(2)
        with csx:
            SIGMAX = st.slider("SigmaX", 0, 500, 5)
        with csy:
            SIGMAY = st.slider("SigmaY", 0, 500, 5)
        blur = cv2.GaussianBlur(thresh, (0,0), sigmaX=SIGMAX, sigmaY=SIGMAY, borderType = cv2.BORDER_DEFAULT)
        
        ina, inb = st.sidebar.columns(2)
        outa, outb = st.sidebar.columns(2)
        with ina:
            inraga = st.slider("In Range-A",0.0,  255.0, 127.5) 
        with inb:
            inragb = st.slider("In Range-B", 0, 255, 255)
        with outa:
            outrnga = st.slider("Out Range-A", 0.0,  255.0, 0.0)
        with outb:
            outrngb = st.slider("Out Range-B", 0, 255, 255)
        mask = skimage.exposure.rescale_intensity(blur, in_range=(inraga,inragb), out_range=(outrnga,outrngb)).astype(np.uint8)
        
        result = image.copy()
        result = cv2.cvtColor(image,cv2.COLOR_BGR2RGBA)
        result[:,:,3] = mask
    
        col2.image(result, caption=f"{option} Screen Antialiased Image", use_column_width=True)

        if st.toggle('SHOW CODE'):
            code = f"import cv2\nimport numpy as np\nimport skimage.exposure\ndef rembgfun(InImage, OutImage):\n    '''\n    InImage = image.jpg\n    OutImage = image.png\n    '''\n    image = cv2.imread(InImage)\n    lab = cv2.cvtColor(image,cv2.COLOR_BGR2LAB)\n    channel = lab[:,:,{x}]\n    thresh = cv2.threshold(channel, {thrs}, {maxv}, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]\n    blur = cv2.GaussianBlur(thresh, (0,0), sigmaX={SIGMAX}, sigmaY={SIGMAY}, borderType = cv2.BORDER_DEFAULT)\n    mask = skimage.exposure.rescale_intensity(blur, in_range={inraga,inragb}, out_range={outrnga,outrngb}).astype(np.uint8)\n    result = img.copy()\n    result = cv2.cvtColor(img,cv2.COLOR_BGR2BGRA)\n    result[:,:,3] = mask\n    cv2.imwrite(OutImage, result)"
            st.code(code, language='python')
    
elif option == 'BLUE':
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])
    if uploaded_file is not None:
        x=2
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)
        col1, col2 = st.columns(2)
        col1.image(image, channels="BGR", caption="Uploaded Image", use_column_width=True)
        lab = cv2.cvtColor(image,cv2.COLOR_BGR2LAB)
        thcol, maxcol = st.sidebar.columns(2)
        channel = lab[:,:,x]
        with thcol:
            thrs = st.slider("THRESH", 0, 500, 0)
        with maxcol:
            maxv = st.slider("MAXVAL", 0, 500, 255)
        thresh = cv2.threshold(channel, thrs, maxv, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

        csx, csy = st.sidebar.columns(2)
        with csx:
            SIGMAX = st.slider("SigmaX", 0, 500, 5)
        with csy:
            SIGMAY = st.slider("SigmaY", 0, 500, 5)
        blur = cv2.GaussianBlur(thresh, (0,0), sigmaX=SIGMAX, sigmaY=SIGMAY, borderType = cv2.BORDER_DEFAULT)
        
        ina, inb = st.sidebar.columns(2)
        outa, outb = st.sidebar.columns(2)
        with ina:
            inraga = st.slider("In Range-A",0.0,  255.0, 127.5) 
        with inb:
            inragb = st.slider("In Range-B", 0, 255, 255)
        with outa:
            outrnga = st.slider("Out Range-A", 0.0,  255.0, 0.0)
        with outb:
            outrngb = st.slider("Out Range-B", 0, 255, 255)
        mask = skimage.exposure.rescale_intensity(blur, in_range=(inraga,inragb), out_range=(outrnga,outrngb)).astype(np.uint8)
        
        result = image.copy()
        result = cv2.cvtColor(image,cv2.COLOR_BGR2RGBA)
        result[:,:,3] = mask
    
        col2.image(result, caption=f"{option} Screen Antialiased Image", use_column_width=True)

        if st.toggle('SHOW CODE'):   
            ccode = f"import cv2\nimport numpy as np\nimport skimage.exposure\ndef rembgfun(InImage, OutImage):\n    '''\n    InImage = image.jpg\n    OutImage = image.png\n    '''\n    image = cv2.imread(InImage)\n    lab = cv2.cvtColor(image,cv2.COLOR_BGR2LAB)\n    channel = lab[:,:,{x}]\n    thresh = cv2.threshold(channel, {thrs}, {maxv}, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]\n    blur = cv2.GaussianBlur(thresh, (0,0), sigmaX={SIGMAX}, sigmaY={SIGMAY}, borderType = cv2.BORDER_DEFAULT)\n    mask = skimage.exposure.rescale_intensity(blur, in_range={inraga,inragb}, out_range={outrnga,outrngb}).astype(np.uint8)\n    result = img.copy()\n    result = cv2.cvtColor(img,cv2.COLOR_BGR2BGRA)\n    result[:,:,3] = mask\n    cv2.imwrite(OutImage, result)"
            st.code(code, language='python')
    
elif option == 'OTHERS':
    st.write("Coming Soon...")
    # uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])
    # if uploaded_file is not None:
    #     image = cv2.imread(uploaded_file.name)
    #     col1, col2 = st.columns(2)
    #     col1.image(image, channels="BGR", caption="Uploaded Image", use_column_width=True)
        
    #     lb, lg, lr = st.sidebar.columns(3)
    #     with lb:
    #         lvb = st.slider('Lower Blue', 0, 500, 200)
    #     with lg:
    #         lvg = st.slider('Lower Green', 0, 500, 200)
    #     with lr:
    #         lvr = st.slider('Lower Red', 0, 500, 200)
    #     lower_color = np.array([lvb, lvg, lvr])
        
    #     ub, ug, ur = st.sidebar.columns(3)
    #     with ub:
    #         uvb = st.slider('Lower Blue', 0, 500, 255)
    #     with ug:
    #         uvg = st.slider('Lower Green', 0, 500, 255)
    #     with ur:
    #         uvr = st.slider('Lower Red', 0, 500, 255)
    #     upper_color = np.array([uvb, uvg, uvr])
        
    #     mask = cv2.inRange(image, lower_color, upper_color)

    #     csx, csy = st.sidebar.columns(2)
    #     with csx:
    #         SIGMAX = st.slider("SigmaX", 0, 500, 5)
    #     with csy:
    #         SIGMAY = st.slider("SigmaY", 0, 500, 5)
    #     blur = cv2.GaussianBlur(mask, (0,0), sigmaX=SIGMAX, sigmaY=SIGMAY, borderType = cv2.BORDER_DEFAULT)

    #     # ina, inb = st.sidebar.columns(2)
    #     # outa, outb = st.sidebar.columns(2)
    #     # with ina:
    #     #     inraga = st.slider("In Range-A",0.0,  255.0, 127.5) 
    #     # with inb:
    #     #     inragb = st.slider("In Range-B", 0, 255, 255)
    #     # with outa:
    #     #     outrnga = st.slider("Out Range-A", 0.0,  255.0, 0.0)
    #     # with outb:
    #     #     outrngb = st.slider("Out Range-B", 0, 255, 255)
    #     # mask = skimage.exposure.rescale_intensity(blur, in_range=(inraga,inragb), out_range=(outrnga,outrngb)).astype(np.uint8)
    #     mask = 255 - blur
    #     result = image.copy()
    #     result = cv2.cvtColor(image,cv2.COLOR_BGR2RGBA)
    #     result[:,:,3] = mask
    
    #     col2.image(result, caption=f"{option} Screen Antialiased Image", use_column_width=True)


    #     # if st.toggle('SHOW CODE'):
    #     #     code = f"def rembgfun(InImage, OutImage):\n'''\nInImage = image.jpg\nOutImage = image.png\n'''\nimage = cv2.imread(InImage)\nlab = cv2.cvtColor(image,cv2.COLOR_BGR2LAB)\nchannel = lab[:,:,{x}]\nthresh = cv2.threshold(channel, {thrs}, {maxv}, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]\nblur = cv2.GaussianBlur(thresh, (0,0), sigmaX={SIGMAX}, sigmaY={SIGMAY}, borderType = cv2.BORDER_DEFAULT)\nmask = skimage.exposure.rescale_intensity(blur, in_range=({inraga,inragb}), out_range=({outrnga,outrngb})).astype(np.uint8)\nresult = img.copy()\nresult = cv2.cvtColor(img,cv2.COLOR_BGR2BGRA)\nresult[:,:,3] = mask\ncv2.imwrite(OutImage, result)"
    #     #     st.code(code, language='python')
