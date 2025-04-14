import cv2, sys, pathlib, csv, os
sys.dont_write_bytecode = True
import numpy as np
from PIL import Image
# from torchvision import models, transforms

img_dir_path = pathlib.Path(sys.argv[1])
IMG_EXTS = [".jpg", ".jpeg", ".png", ".bmp", ".JPG", ".JPEG", ".PNG", ".BMP"]
img_paths = sorted([p for p in img_dir_path.iterdir() if p.suffix in IMG_EXTS])
out_dir_path = pathlib.Path(sys.argv[2])
if not os.path.exists(out_dir_path): os.mkdir(out_dir_path)

for i in range(len(img_paths)):
    img = cv2.imread(img_paths[i], cv2.IMREAD_COLOR)
    # threshold = 120
    # _, trans = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    
    mask = np.zeros(img.shape[:2],np.uint8)
    # 引数はx座標, y座標, 幅, 高さ
    rect = (1,1, img.shape[0], img.shape[1])

    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)

    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2) | (mask==0), 0,1).astype('uint8')
    dst_img = img*mask2[:,:,np.newaxis]
    # threshold = 120
    # _, trans = cv2.threshold(dst_img, threshold, 255, cv2.THRESH_BINARY)
    
    cv2.imwrite(str(out_dir_path / f"mask_{img_paths[i].stem}.png"), dst_img)
