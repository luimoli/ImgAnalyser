import cv2
import numpy as np
import io
import seaborn as sns
import matplotlib.pyplot as plt

from PIL import Image


def plt2cvimg(data):
    """transform plt-plot img to cvimg.
    Args:
        data (arr): 
    Returns:
        opencv-img: _description_
    """
    plt.figure(figsize=(12,8))
    plt.subplot(1, 1, 1)
    plt.plot(data)
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='jpg', bbox_inches="tight")
    plt.close()
    im = Image.open(img_buf)
    cv2_img = cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)
    return cv2_img  

def pltimshow2cvimg(data, showaxis=True):
    """transform plt-imshow img to cvimg.
    Args:
        data (arr): _description_
    Returns:
        _type_: _description_
    """
    plt.figure(figsize=(15,10))
    plt.subplot(1, 1, 1)
    if not showaxis:
        plt.axis('off')
    plt.imshow(data)
    img_buf = io.BytesIO()
    if showaxis:
        plt.savefig(img_buf, format='jpg', bbox_inches="tight")
    else:
        plt.savefig(img_buf, format='jpg', bbox_inches="tight", pad_inches=0.0)
        
    plt.close()
    im = Image.open(img_buf)
    cv2_img = cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)
    return cv2_img  


def plt2cvimg_multisubplots(data_list,title_list):
    """ this function includes several subplots into one figure and returns cvimg.
    Args:
        data_list (list): [data1, data2, data3..] for the subplots.
        fig_num (int): num of subplot figures.
    Returns:
        cvimg: plt img to cv2 img.
    """
    fig_num = len(data_list)
    assert (fig_num % 2) == 0 or fig_num <= 3
    if fig_num <= 3:
        rows = 1
        cols = fig_num
    else:
        rows = 2
        cols = fig_num // rows
    plt.figure(figsize=(12,9))
    for i in range(len(data_list)):
        plt.subplot(rows, cols, i+1)
        plt.plot(data_list[i])
        plt.title(title_list[i])
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='jpg', bbox_inches="tight")
    plt.close()
    im = Image.open(img_buf)
    cv2_img = cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)
    return cv2_img


def plotHeatmap(arr_raw):
    """[plot the heatmap of a 2D array and transform the result to cvimg]

    Args:
        arr ([np array]): [2-dimention]
        save_path ([str]): [r'xxxxx.png']
    """
    arr = np.round(arr_raw, 4)
    f, ax = plt.subplots(figsize=(20, 15))
    res = sns.heatmap(arr, cmap='RdYlGn_r',annot=False, ax=ax,cbar=False, xticklabels=False,yticklabels=False,square=True)
    fig = res.get_figure()
    img_buf = io.BytesIO()
    fig.savefig(img_buf, format='jpg', bbox_inches="tight", pad_inches=0.0)
    plt.close()
    im = Image.open(img_buf)
    cv2_img = cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)
    return cv2_img



if __name__ =='__main__':
    data = np.ones((255))
    # cv2_img = plt2cvimg(data)

    cv2_img = plt2cvimg_multisubplots([data,data,data,data], 4)
    cv2.imwrite('./test2.png', cv2_img)