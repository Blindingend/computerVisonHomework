import numpy as np
from PIL import Image

class ImageMorphological():
    def __init__(self, threshold = 120, image_path = './test.jpg'):
        self.image_orignal = Image.open(image_path)
        self.image = np.asarray(self.image_orignal) # load image
        self.wb = self.gray2wb(threshold=threshold)

    def gray2wb(self, threshold = 120):
        wb = (self.image>=threshold)*255
        wb = wb.astype(np.uint8)
        return wb
    
    def imgsave(self, imarray, path = './wb.png'):
        tmp = Image.fromarray(np.uint8(imarray))
        tmp.save(path, 'png')

    def pad(self, img, row=1, col=1, mode = 'constant'):
        return np.pad(img, ((row,row), (col,col)), mode)

    def isCover(self, kernel, img_slice):
        for i, row in enumerate(kernel):
            for j, value in enumerate(row):
                # if value == 255 and img_slice[i,j] == 255:
                #     continue
                if value == 255 and img_slice[i,j] == 0:
                    return False
        return True

    def isInterset(self, kernel, img_slice):
        for i, row in enumerate(kernel):
            for j, value in enumerate(row):
                if value == 255 and img_slice[i,j] == 255:
                    return True
                # else if value == 255 and img_slice[i,j] == 0:
                #     continue
        return False

    def local_min(self, mask, img_slice):
        index = np.sum(mask).astype(np.int64)
        tmp = img_slice * mask
        return np.sort(tmp.reshape((1, -1)))[0][-index]

    def local_max(self, mask, img_slice):
        tmp = img_slice * mask
        return np.max(tmp)

    def erosion_bin(self, img, kernel, is_save = True, save_path = './erosion.png'):
        w, h = kernel.shape
        img_pad = self.pad(img, (w-1)//2, (h-1)//2)
        tmp = np.zeros(img.shape)
        for r, row in enumerate(img):
            for c, value in enumerate(row):
                covered = self.isCover(kernel, img_pad[r:r+w, c:c+h])
                if covered:
                    tmp[r,c] = 255
                else:
                    tmp[r,c] = 0

        if is_save:
            self.imgsave(tmp,save_path)
        else:
            return tmp
    
    def dilation_bin(self, img, kernel, is_save = True, save_path = './dilation.png'):
        w, h = kernel.shape
        img_pad = self.pad(img, (w-1)//2, (h-1)//2)
        tmp = np.zeros(img.shape)
        for r, row in enumerate(img):
            for c, value in enumerate(row):
                interseted = self.isInterset(kernel, img_pad[r:r+w, c:c+h])
                if interseted:
                    tmp[r,c] = 255
                else:
                    tmp[r,c] = 0
        if is_save:
            self.imgsave(tmp,save_path)
        else:
            return tmp
    
    def erosion_gray(self, img, kernel, is_save = True, save_path = './erosion_grey.png'):
        w, h = kernel.shape
        img_pad = self.pad(img, (w-1)//2, (h-1)//2)
        tmp = np.zeros(img.shape)
        for r, row in enumerate(img):
            for c, value in enumerate(row):
                tmp[r,c] = self.local_min(kernel, img_pad[r: r+w, c:c+h])
        
        if is_save:
            self.imgsave(tmp, save_path)
        else:
            return tmp

    def dilation_gray(self, img, kernel, is_save = True, save_path = './diliation_grey.png'):
        w, h = kernel.shape
        img_pad = self.pad(img, (w-1)//2, (h-1)//2)
        tmp = np.zeros(img.shape)
        for r, row in enumerate(img):
            for c, value in enumerate(row):
                tmp[r,c] = self.local_max(kernel, img_pad[r: r+w, c:c+h])
        
        if is_save:
            self.imgsave(tmp, save_path)
        else:
            return tmp



if __name__ == '__main__':
    img_path = input('please input the image you want to modify: ')
    picname = str(str(img_path).split('/')[-1]).split('.')[0]
    mod_way = input('Please Choose the way you want modify the picture\nA. Binary\nB. Grey\n')
    while mod_way not in ['A','a','B','b']:
        mod_way = input('WRONG FORMAT!\nPlease Choose the way you want modify the picture\nA. Binary\nB. Grey\n')
    img = ImageMorphological(threshold=120, image_path=img_path)
    image = img.image

    #Binary
    # Define 4 kernels
    kernel1 = np.array([[0, 255, 0],
                        [255, 255, 255],
                        [0, 255, 0]])
    kernel2 = np.ones((3,3))*255
    kernel3 = np.array([[0, 0, 255, 0, 0],
                        [0, 255, 255, 255, 0],
                        [255, 255, 255, 255, 255],
                        [0, 255, 255, 255, 0],
                        [0, 0, 255, 0, 0]])
    kernel4 = np.ones((5,5))*255

    #grey mask
    mask1 = np.array([[0,1,0],
                    [1,1,1],
                    [0,1,0]])
    mask2 = np.ones((3,3))
    mask3 = np.array([[0,0,1,0,0],
                    [0,1,1,1,0],
                    [1,1,1,1,1],
                    [0,1,1,1,0],
                    [0,0,1,0,0]])
    mask4 = np.ones((5,5))

    if mod_way == 'A' or mod_way == 'a':
        img.erosion_bin(img.wb, kernel1, save_path='./pics/{}_e_b_k1.png'.format(picname))
        img.erosion_bin(img.wb, kernel2, save_path='./pics/{}_e_b_k2.png'.format(picname))
        img.erosion_bin(img.wb, kernel3, save_path='./pics/{}_e_b_k3.png'.format(picname))
        img.erosion_bin(img.wb, kernel4, save_path='./pics/{}_e_b_k4.png'.format(picname))

        img.dilation_bin(img.wb, kernel1, save_path='./pics/{}_d_b_k1.png'.format(picname))
        img.dilation_bin(img.wb, kernel2, save_path='./pics/{}_d_b_k2.png'.format(picname))
        img.dilation_bin(img.wb, kernel3, save_path='./pics/{}_d_b_k3.png'.format(picname))
        img.dilation_bin(img.wb, kernel4, save_path='./pics/{}_d_b_k4.png'.format(picname))
    elif mod_way == 'B' or mod_way == 'b':
        img.erosion_gray(img.image, mask1, save_path='./pics/{}_e_g_k1.png'.format(picname))
        img.erosion_gray(img.image, mask2, save_path='./pics/{}_e_g_k2.png'.format(picname))
        img.erosion_gray(img.image, mask3, save_path='./pics/{}_e_g_k3.png'.format(picname))
        img.erosion_gray(img.image, mask4, save_path='./pics/{}_e_g_k4.png'.format(picname))

        img.dilation_gray(img.image, mask1, save_path='./pics/{}_d_g_k1.png'.format(picname))
        img.dilation_gray(img.image, mask2, save_path='./pics/{}_d_g_k2.png'.format(picname))
        img.dilation_gray(img.image, mask3, save_path='./pics/{}_d_g_k3.png'.format(picname))
        img.dilation_gray(img.image, mask4, save_path='./pics/{}_d_g_k4.png'.format(picname))

   