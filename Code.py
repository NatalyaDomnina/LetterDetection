﻿import cv2
import numpy as np
import os
import random
import time

class Logic:
    def createGrid(img, thickness, count, color):
        h, w, c = img.shape
        h_2, w_2 = int(h/count), int(w/count)
        for i in range(count-1):
            cv2.line(img, (w_2 + i*(w_2), 0), (w_2 + i*(w_2), h), color, thickness)
        for i in range(count-1):
            cv2.line(img, (0, h_2 + i*(h_2)), (w, h_2 + i*(h_2)), color, thickness)
        return img

    def findGrid(img):
        h, w, c = img.shape
        img_output = np.zeros((h, w, 3), np.uint8)
        img_output[0:h,0:w] = (255,255,255)

        img_edge = cv2.Canny(img, 10, 50)

        x, y = 0, 0
        for i in range(h):
            x, y = 0, 0
            for j in range(w):
                if img_edge[i][j] == 255:
                    x = x + 1
                else:
                    y = y + 1
            if x == 0:
                for k in (i-1, i, i+1):
                    if i-1 > 0 and i+1 < w:
                        img_output[k, 0:w] = img[k, 0:w]

        for i in range(w):
            x, y = 0, 0
            for j in range(h):
                if img_edge[j][i] == 255:
                    x = x + 1
                else:
                    y = y + 1
            if x == 0:
                for k in (i-1, i, i+1):
                    if i-1 > 0 and i+1 < h:
                        img_output[0:h, k] = img[0:h, k]

        return img_output

    def subtrGrid(img):
        h, w, c = img.shape
        grid = np.zeros((h, w, 3), np.uint8)
        grid[0:h, 0:w] = (255, 255, 255)

        img_edge = cv2.Canny(img, 10, 50)

        x, y = 0, 0
        for i in range(h):
            x, y = 0, 0
            for j in range(w):
                if img_edge[i][j] == 255:
                    x = x + 1
                else:
                    y = y + 1
            if x == 0:
                for k in (i - 1, i, i + 1):
                    if i - 1 > 0 and i + 1 < w:
                        img[k, 0:w] = (255,255,255)

        for i in range(w):
            x, y = 0, 0
            for j in range(h):
                if img_edge[j][i] == 255:
                    x = x + 1
                else:
                    y = y + 1
            if x == 0:
                for k in (i - 1, i, i + 1):
                    if i - 1 > 0 and i + 1 < h:
                        img[0:h, k] = (255,255,255)

        return img

    def compare(img, images):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = img_gray.shape
        letters = ['A', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й',
                   'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф',
                   'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']
        res = np.zeros(len(letters)+1, dtype = np.int)
        for k in range(len(images)):
            comp = cv2.imread(os.path.join(folder, images[k]), 0) # Load an color image in grayscale
            comp = cv2.resize(comp, (0, 0), fx = resize, fy = resize)
            flag = False
            count_black = 0
            for i in range(h):
                for j in range(w):
                    if img_gray[i][j] == 0:
                        if comp[i][j] != 0:
                            flag = True
                            break
                        else:
                            count_black += 1
                if flag:
                    res[k] = count_black
                    break
            res[k] = count_black
        ind_max = np.argmax(res)
        return letters[ind_max]

s = Logic

thickness = 25      # ширина решетки
count = 7           # количество полосок решетки
color = (0, 0, 0)   # цвет полосок
resize = 1          # коэффициент уменьшения входного изображения
comma = 5           # точность времени (знаки после запятой)

images = os.listdir('C:/Users/Natali/Documents/Letters_color')

random.seed(version = 2)
r = random.randrange(0, len(images), 1)

folder = 'C:/Users/Natali/Documents/Letters_color/'
img_input = cv2.imread(os.path.join(folder,images[r]))
img_input = cv2.resize(img_input, (0,0), fx = resize, fy = resize)
size_h, size_w, _ = img_input.shape

print ("Размер изображения:  " + str(size_h) + "x" + str(size_w))
print ("Создание решетки. ", end = '')
start = time.clock()
img_grid = s.createGrid(img_input, thickness, count, color)
elapsed = round((time.clock() - start), comma)
print ("Затрачено " + str(elapsed) + " s")
cv2.imshow('img_grid', img_grid)

print("Поиск решетки. ", end = '')
start = time.clock()
img_only_grid = s.findGrid(img_grid)
elapsed = round((time.clock() - start), comma)
print ("Затрачено " + str(elapsed) + " s")
cv2.imshow('img_only_grid', img_only_grid)

print("Вычитание решетки. ", end = '')
start = time.clock()
img_no_grid = s.subtrGrid(img_grid)
elapsed = round((time.clock() - start), comma)
print ("Затрачено " + str(elapsed) + " s")
cv2.imshow('img_no_grid', img_no_grid)

print("Сравнение. ", end = '')
start = time.clock()
letter = s.compare(img_no_grid, images)
elapsed = round((time.clock() - start), comma)
print ("Затрачено " + str(elapsed) + " s")

print ("Найденная буква: " + letter)

cv2.waitKey(0)