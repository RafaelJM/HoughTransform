import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


def detectarRetas(imgNum):
    img = cv.imread("image"+imgNum+".png",0)
    
    #img = cv.equalizeHist(img)
    
    img = cv.Canny(img, 200, 180) 
    
    img = cv.bitwise_not(img)
    
    diag = int((np.sqrt(pow(len(img),2)+pow(len(img[0]),2)))+1)
    
    matrix = np.zeros((diag*2,180))
    matrix2 = np.zeros((diag*2,180))
    
    for x in range(0,len(img)):
        for y in range(0,len(img[x])):
            if img[x][y] == 0:
                for theta in range(0,180):
                    p = int(x*np.sin(np.deg2rad(theta)) + y*np.cos(np.deg2rad(theta)))
                    matrix[p+diag,theta] += 1
    
    lines = []
    
    for x in range(0,len(img)):
        for y in range(0,len(img[x])):
            if img[x][y] == 0:
                auxx = 0
                auxy = 0
                maxx = -100
                for theta in range(0,180):
                    p = int(np.round(x*np.sin(np.deg2rad(theta)) + y*np.cos(np.deg2rad(theta))))
                    if matrix[p+diag,theta] >= maxx:
                        auxx = p+diag
                        auxy = theta
                        maxx = matrix[auxx,auxy]
                if maxx >= 0:
                    matrix2[auxx,auxy] += 1
    
    for x in range(0,len(matrix2)):
        for y in range(0,len(matrix2[x])):
            if matrix2[x][y] != 0:
                lines.append([x,y])
    
    semiretas = []
    
    for line in lines:
        theta = np.deg2rad(line[1])
        c = np.cos(theta)
        s = np.sin(theta)
        point = (int((line[0]-diag)*c), int((line[0]-diag)*s)) 
        vetorReta = (-s,c)
        if abs(c) >= abs(s):
            deslocamento = -(point[1]/vetorReta[1])
        else:
            deslocamento = -(point[0]/vetorReta[0])
        point = (int(point[0] + deslocamento*vetorReta[0]),int(point[1] + deslocamento*vetorReta[1]))
        mudou = True
        while mudou:
            mudou = False
            if point[0] > (len(img[0]) -1):
                deslocamento = (len(img[0]) -1 -point[0])/vetorReta[0]
                mudou = True
            if point[1] > (len(img) - 1):
                deslocamento = (len(img) -1 -point[1])/vetorReta[1]
                mudou = True
            if point[0] < 0:
                deslocamento = -(point[0]/vetorReta[0])
                mudou = True
            if point[1] < 0:
                deslocamento = -(point[1]/vetorReta[1])
                mudou = True
            if mudou:
                point = (int(point[0] + deslocamento*vetorReta[0]),int(point[1] + deslocamento*vetorReta[1])) 
        if (point[0] == 0 and vetorReta[0] < 0) or (point[0] == (len(img[0]) - 1) and vetorReta[0] >0):
            vetorReta = (-vetorReta[0],-vetorReta[1])
        if (point[1] == 0 and vetorReta[1] < 0) or (point[1] == (len(img) - 1) and vetorReta[1] >0):
            vetorReta = (-vetorReta[0],-vetorReta[1])
        sequenciaPreto = 15
        sequencia = 0
        possivelSR = [(0,0),(0,0),0]
        while int(np.round(point[0])) < len(img[0]) and int(np.round(point[1])) < len(img) and int(np.round(point[0])) >= 0 and int(np.round(point[1])) >= 0:
           preto = False
           for auxx in range(-1,2):
               for auxy in range(-1,2):
                   try:
                       if img[int(np.round(point[1]))+auxx][int(np.round(point[0]))+auxy] == 0:
                           preto = True
                       if preto: break
                   except: {}
           if preto:
               if sequencia == 0:
                   possivelSR[0] = (int(np.round(point[0])),int(np.round(point[1])))
               sequencia += 1
           else:
               if sequencia >= sequenciaPreto:
                   possivelSR[1] = (int(np.round(point[0])),int(np.round(point[1])))
                   possivelSR[2] = sequencia
                   semiretas.append(possivelSR)
                   possivelSR = [(0,0),(0,0),0]
               sequencia = 0
           point = (point[0] + vetorReta[0], point[1] + vetorReta[1])
        if sequencia >= sequenciaPreto:
           possivelSR[1] = (int(np.round(point[0])),int(np.round(point[1])))
           possivelSR[2] = sequencia
           semiretas.append(possivelSR)
           possivelSR = [(0,0),(0,0),0]
           sequencia = 0
    
    img = np.zeros([len(img),len(img[0]),1])
    img.fill(255)
    
    for semireta in semiretas:
        cv.line(img,semireta[0],semireta[1],(0,0,0),1)

    plt.imshow(matrix, cmap='hot', interpolation='nearest')
    plt.savefig(str("Hough"+imgNum+".jpg"))
    cv.imwrite(str("NewImage"+imgNum+".png"),img)
    with open("linesImage"+imgNum+".txt", mode='w') as file:
        for i in range(0,len(semiretas)):
            file.write("Line "+ str(i) + ": " + str(semiretas[i][0]) + " to " + str(semiretas[i][1])+"\n")
        

detectarRetas("1")
detectarRetas("2")


