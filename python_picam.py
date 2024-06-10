import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders
import time
import picamera
import datetime
import base64
import requests
import urllib
import json


# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'cciotcw2@gmail.com'
SMTP_PASSWORD = 'kayqkerqsnpwroyh'


# Email contents
EMAIL_FROM = 'cciotcw2@gmail.com'
EMAIL_TO = ['cciotcw2@gmail.com', 'dantaiyearemu@gmail.com']
EMAIL_SUBJECT = 'Image attachment from Raspberry Pi'
EMAIL_BODY = 'Hey! I took a photo from the Raspberry PI Zero'


# API Data configuration
x = datetime.datetime.now()
def getAPIData():
    year = x.strftime('%y')
    month = x.strftime('%m')
    day = x.strftime('%d')
    hour = x.strftime('%H')
    minute = x.strftime('%M')
    second = x.strftime('%S')

    return {
        "userKey": "mnbvcxz012345",
        "params": {
            "data": {
                "filename": "image_" + year + month + day + hour + minute + second,
                'year': year,
                'month': month,
                'day': day,
                'hour': hour,
                'minute': minute,
                'second': second
            },
            "name": "image_" + year + month + day + hour + minute + second,
            "img": ""
        }
    }
    
APIDATA = getAPIData()
APIURL = 'http://20.0.96.102/iotsecure/data_push.php'
print(APIDATA)


# Image configuration
IMAGE_PATH = './intruders/'
IMAGE_NAME = IMAGE_PATH + APIDATA['params']['name'] + '.png'


# Create the email message
msg = MIMEMultipart()
msg['From'] = EMAIL_FROM
msg['To'] = COMMASPACE.join(EMAIL_TO)
msg['Subject'] = EMAIL_SUBJECT
msg.attach(MIMEText(EMAIL_BODY, 'plain'))


# Take Image using Raspberry-Picamera
print('Starting to make a photo.')
with picamera.PiCamera() as camera:    # create a camera instance
    camera.resolution = (1280, 720) # set camera resolution
    camera.start_preview()  # start the camera preview
    time.sleep(1)  # wait for camera to warm up
    camera.capture(IMAGE_NAME)  # capture image
    camera.stop_preview()  # stop the camera preview
print('Image saved')


# Add image attachment
print('Attaching Image')
with open(IMAGE_NAME, 'rb') as f:
    print('Converting Image to Base64')
    APIDATA['params']['img'] = base64.b64encode(f.read())
    
    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(f.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename=IMAGE_NAME)
    msg.attach(attachment)
print('Image Attached')


# Send data to API
print('Sending data through API')
payload=[('payload', json.dumps(APIDATA))]
payload=urllib.parse.urlencode(payload)
utf8 = bytes(payload, 'utf-8')
response = urllib.request.urlopen(APIURL, utf8, 300).read()
print('Data Sent')


# Connect to the SMTP server and send the email
with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls()
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    server.quit()
print('Email Sent')
