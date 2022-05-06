import fundus_prep as prep
import glob
import os
import cv2 as cv
import pandas as pd
from PIL import ImageFile
import shutil
ImageFile.LOAD_TRUNCATED_IMAGES = True

def process(image_list, save_path):
    
    radius_list = []
    centre_list_w = []
    centre_list_h = []
    name_list = []
    list_resolution = []
    scale_resolution = []
    
    resolution_list = pd.read_csv('../resolution_information.csv')
    
    for image_path in image_list:
        
        dst_image = '../images/' + image_path
        if os.path.exists('../Results/M0/images/' + image_path):
            print('continue...')
            continue
            
        try:
            resolution_ = resolution_list['res'][resolution_list['fundus']==image_path].values[0]
            list_resolution.append(resolution_)

            img = prep.imread(dst_image)
            r_img, borders, mask, r_img, radius_list,centre_list_w, centre_list_h = prep.process_without_gb(img,img,radius_list,centre_list_w, centre_list_h)
            prep.imwrite(save_path + image_path.split('.')[0] + '.png', r_img)
            #prep.imwrite('../Results/M0/images/' + image_path.split('.')[0] + '.png', mask)


            name_list.append(image_path.split('.')[0] + '.png')
        
        except:
            pass

    scale_list = [a*2/912 for a in radius_list]
    
    scale_resolution = [a*b*1000 for a,b in zip(list_resolution,scale_list)]
    
    Data4stage2 = pd.DataFrame({'Name':name_list, 'centre_w':centre_list_w, 'centre_h':centre_list_h, 'radius':radius_list, 'Scale':scale_list, 'Scale_resolution':scale_resolution})
    Data4stage2.to_csv('../Results/M0/crop_info.csv', index = None, encoding='utf8')
        




if __name__ == "__main__":
    if os.path.exists('../images/.ipynb_checkpoints'):
        shutil.rmtree('../images/.ipynb_checkpoints')
    image_list = sorted(os.listdir('../images'))
    save_path = '../Results/M0/images/'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    process(image_list, save_path)

        



