import base64

def compress(imagestr,filename):
    imgstring = imagestr.replace('data:image/jpeg;base64,','')
    if(imgstring == ''):
        return None
    try:
        imgdata = base64.b64decode(imgstring)
    except:
        return None

    image =  'static/media/' + filename
    with open(image, 'wb') as f:
        f.write(imgdata)
    return image


