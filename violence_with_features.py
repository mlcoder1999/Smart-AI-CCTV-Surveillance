import cv2
import numpy as np
import keras
from keras.layers import *
from keras.models import Model , load_model
from keras.preprocessing import image
from keras.utils import np_utils
from keras.applications.resnet50 import ResNet50
from keras.optimizers import Adam
import matplotlib.pyplot as plt
import random
import os
import playsound
# Python code to illustrate Sending mail from 
# your Gmail account 
import smtplib 
# import reverse_geocoder as rg
import pprint
import smtplib 
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import reverse_geocoder as rg
import pprint
import os
import os
import googlemaps
from twilio.rest import Client
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
from ipregistry import IpregistryClient


count = 0
continous_viol = 0
pred = "Non-Violence"

model = load_model("using_batch_128_notebook_new_data_gray_new_1_epochs.h5")

cam = cv2.VideoCapture("Test.mp4")

while True:
	ret,frame = cam.read()
	mail_send_frame = frame

	if ret==False:
		print("Something Went Wrong!")
		break

	key_pressed = cv2.waitKey(1) & 0xFF
	if key_pressed == ord('q'):
		break

	test_data = cv2.resize(frame, (224,224))

	count = count + 1

	test_data = np.array(test_data)
	test_data.shape = (1,224,224,3)

	if count == 9:
		zz = model.predict(test_data)
		print(zz[0][0])
		count = 0

		if zz[0][0]<0.24:
			pred = "Violence"
			continous_viol = continous_viol + 1
			if continous_viol == 7:
				playsound.playsound('chase_siren.wav')
				continous_viol = 0

				client = IpregistryClient("API KEY OF USER")  
				ipInfo = client.lookup() 
				zzz_lat = ipInfo.location["latitude"]
				zzz_long = ipInfo.location["longitude"]
				print("live location is latitude {0} and longitude {1}".format(zzz_lat,zzz_long))


				filename ="DANGER.jpg"
				cv2.imwrite("%s"%filename, mail_send_frame)

				message = "ALERT VIOLENCE DETECTED and live location is latitude {0} and longitude {1}".format(zzz_lat,zzz_long)

				img_data = open("DANGER.jpg", 'rb').read()
				msg = MIMEMultipart()
				msg['Subject'] = 'ALERT VIOLENCE'
				msg['From'] = "SENDER'S EMAIL ADDRESS"
				msg['To'] = "RECIEVER's EMAIL ADDRESS"

				text = MIMEText(message)
				msg.attach(text)
				image = MIMEImage(img_data, name=os.path.basename("DANGER.jpg"))
				msg.attach(image)

				s = smtplib.SMTP('smtp.gmail.com', 587)
				s.ehlo()
				s.starttls()
				s.ehlo()
				s.login("SENDER'S EMAIL ADDRESS", "SENDER'S EMAIL ADDRESS PASSWORD")
				s.sendmail("SENDER'S EMAIL ADDRESS", "RECIEVER's EMAIL ADDRESS", msg.as_string())
				s.quit()
				print("MAIL SENT")

				account_sid = 'API KEY OF USER (Eg- 337c5e5465e1bd8f31417602d2) '
				auth_token = 'API KEY (Eg- 337c5e5465e1bd8f31417602d2) '
				client = Client(account_sid, auth_token)
				call = client.calls.create(
					url='http://demo.twilio.com/docs/voice.xml',
					to=' RECIEVERs PHONE NUMBER (Eg- +919211733317)',
					from_='SENDERs PHONE NUMBER (Eg- +919211733317)'
					)



				# Your Account Sid and Auth Token from twilio.com/console
				# DANGER! This is insecure. See http://twil.io/secure
				account_sid = 'API KEY OF USER (Eg- 337c5e5465e1bd8f31417602d2)'
				auth_token = 'API KEY OF USER (Eg- 337c5e5465e1bd8f31417602d2)'
				client = Client(account_sid, auth_token)

				message = client.messages \
				                .create(
				                     body=message,
				                     from_='SENDERs PHONE NUMBER (Eg- +919211733317)',
				                     to='RECIEVERs PHONE NUMBER (Eg- +919211733317)'
				                 )

				print(message.sid)
				cv2.putText(frame, "Mail and Call SENT",(100,500), cv2.FONT_HERSHEY_SIMPLEX,1 ,(255, 0 ,0), 2,cv2.LINE_AA)
		else:
			pred = "Non-Violence"
			continous_viol = 0

	cv2.putText(frame, pred,(50,50), cv2.FONT_HERSHEY_SIMPLEX,1 ,(255, 0 ,0), 2,cv2.LINE_AA)

	cv2.imshow("Video frame",frame)


cam.release()
cv2.destroyAllWindows()



