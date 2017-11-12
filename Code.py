import cv2
import os
import numpy as np
from scipy.spatial import distance

def createGrid(img, thickness, count, color):
    #cv2.imshow('0', img)
    h, w, c = img.shape
    h_2, w_2 = int(h / count), int(w / count)
    for i in range(count - 1):
        cv2.line(img, (w_2 + i * (w_2), 0), (w_2 + i * (w_2), h), color, thickness)
    for i in range(count - 1):
        cv2.line(img, (0, h_2 + i * (h_2)), (w, h_2 + i * (h_2)), color, thickness)
    return img

def subtrGrid(img):
    h, w, c = img.shape
    grid = np.zeros((h, w, 3), np.uint8)
    grid[0:h, 0:w] = (255, 255, 255)

    img_edge = cv2.Canny(img, 10, 50)
    #cv2.imshow('1', img_edge)

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
    #cv2.imshow('2', img)
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
    #cv2.imshow('3', img_output)
    return img_output

def filters(img):
    black_bool = True
    white_bool = False

    G = img.copy()
    gpA = [G]
    for i in range(4):
        G = cv2.pyrDown(G)
        gpA.append(G)

    img = gpA[2]
    h, w = img.shape
    #cv2.imshow('img', img)

    filter_0 = np.ones((h, w), bool)

    filter_1 = np.ones((h, w), bool)
    filter_1[0:h, 0:int(w / 2)] = white_bool

    filter_2 = np.ones((h, w), bool)
    filter_2[int(h / 2):h, 0:w] = white_bool

    filter_3 = np.logical_not(np.logical_xor(filter_1, filter_2))

    filter_4 = np.ones((h, w), bool)
    filter_4[0:h, 0:int(w / 4)] = white_bool
    filter_4[0:h, int(3 * w / 4):w] = white_bool

    filter_6 = np.logical_not(np.logical_xor(filter_4, filter_2))

    filter_9 = np.ones((h, w), bool)
    filter_9[0:int(h / 4), 0:w] = white_bool
    filter_9[int(3 * h / 4):h, 0:h] = white_bool

    filter_7 = np.logical_not(np.logical_xor(filter_1, filter_9))

    filter_8 = np.logical_not(np.logical_xor(filter_4, filter_9))

    filter_5 = np.ones((h, w), bool)
    filter_5[0:h, int(w / 4):int(2 * w / 4)] = white_bool
    filter_5[0:h, int(3 * w / 4):w] = white_bool

    filter_10 = np.ones((h, w), bool)
    filter_10[0:int(h / 4), 0:w] = white_bool
    filter_10[int(2 * h / 4):int(3 * h / 4), 0:w] = white_bool

    filter_11 = np.logical_not(np.logical_xor(filter_2, filter_5))

    filter_12 = np.logical_not(np.logical_xor(filter_1, filter_10))

    filter_13 = np.logical_not(np.logical_xor(filter_5, filter_9))

    filter_14 = np.logical_not(np.logical_xor(filter_4, filter_10))

    filter_15 = np.logical_not(np.logical_xor(filter_5, filter_10))

    filters = [filter_0, filter_1, filter_2, filter_3, filter_4, filter_5,
               filter_6, filter_7, filter_8, filter_9, filter_10, filter_11,
               filter_12, filter_13, filter_14, filter_15]
    filtet_number = 0
    full_res = []
    for filter in filters:
        res = 0
        for i in range(h):
            for j in range(w):
                if filter[i][j] == black_bool:
                    res += 255 - img[i][j]
                    # print('+ ' + str(i) + ' ' + str(j))
                elif filter[i][j] == white_bool:
                    res -= 255 - img[i][j]
                    # print('- ' + str(i) + ' ' + str(j))
        # print('filter ' + str(filtet_number) + ' = ' + str(res))
        filtet_number += 1
        '''
        if res > 0:
            res = 1
        elif res < 0:
            res = -1
        else:
            res = 0
            '''
        full_res.append(res)

    #print('full_res = ' + str(full_res))
    return full_res

def create_sign():
    images = os.listdir('C:/Users/Natali/Documents/Letters_color')
    print (images)
    for img in images:
        folder = 'C:/Users/Natali/Documents/Letters_color/'
        img_input = cv2.imread(os.path.join(folder,img))
        img_input = cv2.resize(img_input, (256, 256))
        print(os.path.join(folder,img))
        h, w, c = img_input.shape
        f = open('sign2lab2lvl.txt', 'a')
        img_input_gray = cv2.cvtColor(img_input, cv2.COLOR_BGR2GRAY)
        res_no_grid = filters(img_input_gray)
        for index in res_no_grid:
            f.write(str(index))
            f.write(' ')
        f.write('\n')
        f.close()

def sign_to_list():
    f = open('sign2lab2lvl.txt', 'r')
    sign = []
    line = f.readline()
    sign.append(line.rstrip())
    while line:
        line = f.readline()
        sign.append(line.rstrip())
    sign = [i.split(' ') for i in sign]
    sign = sign[:-1]
    for i in range(len(sign)):
        sign[i] = [int(n) for n in sign[i]]
    return sign


thickness = 30      # ширина решетки
count = 9           # количество полосок решетки
color = (0, 0, 0)   # цвет полосок
resize = 1          # коэффициент уменьшения входного изображения
comma = 5           # точность времени (знаки после запятой)

#create_sign()
sign = sign_to_list()

img_input = cv2.imread('C:/Users/Natali/Documents/Letters_color/23.png')
img_grid = createGrid(img_input, thickness, count, color)
findGrid(img_grid)
cv2.imshow('234', img_grid)

asd = img_grid.copy()
asd = cv2.resize(asd, (256,256))
#cv2.imshow('334', asd)

img_no_grid = subtrGrid(img_grid)
#cv2.imshow('344', img_no_grid)
img_no_grid_gray = cv2.cvtColor(img_no_grid, cv2.COLOR_BGR2GRAY)
img_no_grid_gray = cv2.resize(img_no_grid_gray, (256,256))

res_grid = filters(img_no_grid_gray)
res_grid = np.asarray(res_grid)
res_coef = []

for i in range(len(sign)):
    sign[i] = np.asarray(sign[i])
    res_coef.append(distance.euclidean(sign[i], res_grid))
#print(res_coef)

letters = ['A', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й',
            'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф',
            'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']
ind_max = np.argmin(res_coef)
print ("Найденная буква: " + letters[ind_max])
cv2.waitKey(0)