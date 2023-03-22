#Para este proyecto se necesita una instalacion externa de tesseract
import os
import cv2
import pytesseract
import numpy as np


#detecta la posicion de cada caracter
def detectingCharacters(Path):
    img= cv2.imread(Path)
    hImg,wImg,_= img.shape      #To know the dimension of the image
    newImg= img

    #Pytesseract only accepts RGB values, and opencv read in BGR, which is why we needed to transform.
    imgRGB= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    boxes= pytesseract.image_to_boxes(imgRGB) #Returns result containing recognized characters and their box boundaries
                                            #x and hImg-y are down place of the box, and the w and hImg-h are the up place of the box
    for b in boxes.splitlines():
        #print(b)               #Example 'U 160 700 188 745 0'
        b= b.split(' ')         #To split by spaces
        #print(b)               #Example ['U', '160', '700', '188', '745', '0']
        x,y,w,h= int(b[1]),int(b[2]),int(b[3]),int(b[4]) #w and h are the diagonal points of the bounding box not actual width and height
        
        #For rectangle (image, vertex of rec, vertex of rec opposite, color, thickness)
        cv2.rectangle(newImg,(x,hImg-y),(w,hImg-h),(0,0,139),2) #The 'y' value are the opposite for that hImg-

        #veremos si los caracteres fuero detectados apropiadamente
        #For putText(image,text,org(bottom-left corner of the text in the image),font type,fontScale,color,thickness)
        cv2.putText(newImg, b[0], (x,hImg-h), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0,0,139),1)
    return newImg

#Detector de palabras
def detectingWords(Path):
    img= cv2.imread(Path)
    newImg= img

    #Pytesseract only accepts RGB values, and opencv read in BGR, which is why we needed to transform.
    imgRGB= cv2.cvtColor(newImg, cv2.COLOR_BGR2RGB)
    boxes= pytesseract.image_to_data(imgRGB)

    #se pone los valores de la cuenta en x
    for x,b in enumerate(boxes.splitlines()):
        if x!=0:
            #print(b)            #one result 5       1       1       1       1       1       122     335     109     45      95  "Un
            b= b.split()        #Putting in a list the 12 elements
            print(b)            #one result ['5', '1', '1', '1', '1', '1', '122', '335', '109', '45', '95', '"Un']
            #If the dimension is less than 12, we don't detect any words.
            if len(b)==12:
                x,y,w,h= int(b[6]),int(b[7]),int(b[8]),int(b[9])  #(x,y) Top left corner, w width (anchura), h height (altura)
                
                cv2.rectangle(newImg,(x,y),(w+x,h+y),(0,0,139),2)
                #veremos si los caracteres fuero detectados apropiadamente
                cv2.putText(newImg, b[11], (x,y), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0,0,139),1) #Put the word detected
    return newImg


#Detector solo de numeros
def detectingNumbers(Path):
    img= cv2.imread(Path)
    img.shape      #saber las dimensiones de la imagen
    newImg= img

    #Pytesseract only accepts RGB values, and opencv read in BGR, which is why we needed to transform.
    imgRGB= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    cong= r'--oem 3 --psm 6 outputbase digits'      #Selecting only the digits (para solo escoger los digitos) https://github.com/tesseract-ocr/tesseract/blob/main/doc/tesseract.1.asc
    boxes= pytesseract.image_to_data(imgRGB,config=cong)
    #se pone los valores de la cuenta en x
    for x,b in enumerate(boxes.splitlines()):
        #In raw 0 we have the discriptions of the table
        if x!=0:
            b= b.split()        #las palabras estan solo en las lista con 12 elementos como vimos en la impresion
            #print(b)            #Result ['5', '1', '1', '1', '4', '1', '287', '337', '88', '23', '95', '02199']
            if len(b)==12:
                #if config value high than 85 
                if int(b[10])>85:
                    x,y,w,h= int(b[6]),int(b[7]),int(b[8]),int(b[9])

                    cv2.rectangle(newImg,(x,y),(w+x,h+y),(0,0,139),2)

                    #veremos si los caracteres fuero detectados apropiadamente
                    cv2.putText(newImg, b[11], (x,y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,139),1)
    return newImg


# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd= 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' #full_path_to_your_tesseract_executable

imagePath= os.path.join('.','data','prueba1.jpg')
imageOut_path1= os.path.join('.','assets','output1.jpg')
imageOut_path2= os.path.join('.','assets','output2.jpg')
imageNumPath= os.path.join('.','data','pruebaNum.jpg')
imageOut_path3= os.path.join('.','assets','output3.jpg')

""" #If we just need print the text
img= cv2.imread(imagePath)          #Read the image
#pytesseract solo acepta valores RGB y opencv las lee en BGR por eso transformamos
imgRGB= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
text= pytesseract.image_to_string(imgRGB, lang='spa') #Defauld language in tesseract is english for other we need especify in lang
#Imprimimos las letras que se detectan en la imagen
print("Text: ",text) """

outImg1= detectingCharacters(imagePath)
cv2.imwrite(imageOut_path1, outImg1) #Save the image

outImg2= detectingWords(imagePath)
cv2.imwrite(imageOut_path2, outImg2) #Save the image

outImg3= detectingNumbers(imageNumPath)
cv2.imwrite(imageOut_path3, outImg3) #Save the image

#ahora la mostramos
cv2.imshow('Output 1', outImg1)
cv2.imshow('Output 2', outImg2)
cv2.imshow('Output 3', outImg3)
cv2.waitKey(0)                       #Putting a infinite delay
cv2.destroyAllWindows()