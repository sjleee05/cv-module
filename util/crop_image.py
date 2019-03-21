import cv2
import numpy as np
import time

def find_top_bottom_line(input_img):
    top_list = []
    bottom_list = []
    
    print(input_img.shape)
    for col in range(input_img.shape[1]):
        if input_img[0][col] == 255:
            top_list.append(0)

        if input_img[input_img.shape[0]-1][col] == 255:
            bottom_list.append(input_img.shape[0]+1)
        
        for row in range(input_img.shape[0]):
            pix = input_img[row][col]

            if row >0:
                prev_pix = input_img[row-1][col]

                if (pix == 255) & (prev_pix == 0):
                    top_list.append(row)
                    
                if (pix == 0) & (prev_pix == 255):
                    bottom_list.append(row)
                    break

    return top_list, bottom_list

def preprocess_img(input_img, size):
    # resize image
    re_img = cv2.resize(input_img, dsize = size)
    
    # convert color
    gray = cv2.cvtColor(re_img,cv2.COLOR_BGR2GRAY)
    
    # binary
    ret, thresh = cv2.threshold(gray, 2, 255.0, 0)

    # morphology
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.erode(thresh, kernel, iterations=1)
    thresh = cv2.dilate(thresh, kernel, iterations=1)
    
    return thresh

def crop_img(img, top_list, bottom_list):
    
    # TODO: need to cutting by x-axis
    # top_list[-3] is temporal solution.

    top_line = max(top_list[:-3])
    bottom_line = min(bottom_list[:-3])
    
    print('top_line: ', top_line, 'bottom_line: ', bottom_line)
    crop_img = img[top_line:bottom_line, :, :]
    
    return crop_img
    

def main():
    
    startTime = time.time()

    # read image
    img = cv2.imread('test.jpg')
    img = cv2.resize(img, dsize = (int(img.shape[1]/4),int(img.shape[0]/4)))

    # image pre-processing
    processed_img = preprocess_img(img, (img.shape[1],img.shape[0]))
    
    # find top, bottom line
    top_list, bottom_list = find_top_bottom_line(processed_img)
    
    pixbrowseTime = time.time()-startTime
    print('elpased Time (find top, bottom line): ', pixbrowseTime)

    '''
    # draw line
    for col in range(processed_img.shape[1]):
        img[int(top_list[col]),col,:] = (255,0,0)
        img[int(bottom_list[col]),col,:] = (255,0,0)
    '''    
    
    cropped_img = crop_img(img, top_list, bottom_list)

    # show image

    cv2.imshow('original', img)
    cv2.imshow('src',cropped_img)
            
    cv2.waitKey(0)

if __name__ == '__main__':
    main()

