import os
import webbrowser
import time
from fpdf import FPDF
import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab
import ocrmypdf
import platform


#check if the varivable timeSleep is enught for your system
if platform.platform(aliased=True)=="win32" or platform.platform(aliased=True)=="cygwin" or platform.platform(aliased=True)=="msys":
    OS="Win"
    timeSleep = 10
elif platform.platform(aliased=True)=="darwin":
    OS="macOS"
    timeSleep = 5
else:
    OS="Linux" #non supportato
    OS="macOS"
    timeSleep = 7


print("OS: "+OS+ ", STOP PROGRAM IF IS WRONG")

print ("inserisci il nome della presentazione")
nome = input()
nome+=".pdf"
print ("inserisci l'url delle slide su google presentazione")
url = input()


#change the screen size
altezzaSchermo=1800
larghezzaSchermo=2880
#formato slide 4:3
larghezzaSlide=(altezzaSchermo/3)*4
BandeSize=(larghezzaSchermo-larghezzaSlide)/2
largghezzaMM=larghezzaSlide*0.2645833333
altezzaMM=altezzaSchermo*0.2645833333

webbrowser.open(url, new=0, autoraise=True)
time.sleep(timeSleep)

if OS == "macOS":
    pyautogui.hotkey('command','enter')
    time.sleep(timeSleep)
    pyautogui.press('home')
elif OS == "Win":
    pyautogui.hotkey('ctrl', 'f5')
    time.sleep(timeSleep)
    #pyautogui.hotkey('ctrl','f5')
    pyautogui.press('home')

if not os.path.exists("temp") or not os.path.isdir("temp"):
    os.mkdir("temp")

if not os.path.exists("withOCR") or not os.path.isdir("withOCR"):
    os.mkdir("withOCR")

if not os.path.exists("noOCR") or not os.path.isdir("noOCR"):
    os.mkdir("noOCR")

i=0
number_slide=0
boolean=True
pdf = FPDF(orientation="P",unit="mm",format=(largghezzaMM,altezzaMM))
while boolean:
    time.sleep(timeSleep)
    screenshot = ImageGrab.grab(all_screens=True)
    screenshot = screenshot.crop((int(BandeSize), 0, int(larghezzaSchermo-BandeSize),altezzaSchermo))
    screenshot.save("./temp/"+str(i)+".png")
    pyautogui.hotkey('down')
    if i < 5:
        timeSleep/=2
    if i > 0:
        a = cv2.imread("./temp/"+str(i)+".png")
        b = cv2.imread("./temp/"+str(i-1)+".png")
        boolean =not np.all(a==b)
    if boolean:
        if OS == "macOS":
            pdf.add_page(orientation="P", format=(largghezzaMM, altezzaMM))
            pdf.image("./temp/" + str(i) + ".png", 0, 0, w=largghezzaMM, h=altezzaMM, keep_aspect_ratio=True)
        elif OS == "Win":
            pdf.add_page(orientation="P")
            pdf.image("./temp/" + str(i) + ".png", 0, 0, w=largghezzaMM, h=altezzaMM)

    i+=1
    number_slide=i
    screenshot.close()

pyautogui.press('esc')
pdf.output("./noOCR/"+nome)
for i in range(0,number_slide):
    os.remove("./temp/"+str(i)+".png")
os.rmdir("./temp")
ocrmypdf.ocr("./noOCR/"+nome, "./withOCR/"+nome, rotate_pages=True,language="eng",force_ocr=True)











