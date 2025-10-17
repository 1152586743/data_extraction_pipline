
from huggingface_hub import hf_hub_download
import pandas as pd
from natsort import natsorted
from glob import glob
import openslide
import os
import matplotlib.pyplot as plt
import geopandas as gpd  
import matplotlib.patches as patches
import numpy as np

def get_thumbnails(wsi_obj, rescale_rate=100):
    wsi_w, wsi_h = wsi_obj.dimensions
    thumb_size_x = wsi_w / rescale_rate
    thumb_size_y = wsi_h / rescale_rate
    thumbnail = wsi_obj.get_thumbnail([thumb_size_x, thumb_size_y]).convert("RGB")
    return  thumbnail

def get_slide_id(img_fn):
    slide_id = os.path.split(os.path.split(img_fn)[0])[1] # 
    return slide_id

df = pd.read_csv("hf://datasets/Codatta/Refined-TCGA-PRAD-Prostate-Cancer-Pathology-Dataset/dataset/PRAD/PRAD.csv")

img_dir_root = "/data/jjiang10/Data/ProstatePathology/WSIs/"  # + slide_id + slide_name
geojson_dir_root = "/data/jjiang10/Data/ProstatePathology/dataset/PRAD/"  # + slide_name.replace(".svs", ".geojson")
out_dir = "/data/jjiang10/Data/ProstatePathology/output/vis_out"

wsi_info_csv = os.path.join(out_dir, "All_WSI_Info.csv")
wsi_info_csv_header = "TCGA_slide_id,slide_name,dim_width,dim_height,pixel_size\n"
fp = open(wsi_info_csv, 'w')
fp.write(wsi_info_csv_header)

slide_name_list = natsorted(list(df.slide_name))

anno_name_list = glob(os.path.join(geojson_dir_root, "*.geojson"))
anno_name_list = natsorted([os.path.split(fn)[1] for fn in anno_name_list])

print("There are {} WSIs, and {} annotation files.".format(len(slide_name_list), len(anno_name_list)))

anno_fn_list = [anno_fn.replace(".geojson", "") for anno_fn in anno_name_list]
slide_fn_list = [slide_fn.replace(".svs", "") for slide_fn in slide_name_list]

intersection = set(anno_fn_list).intersection(set(slide_fn_list))

down_sample_rate = 100
for sample_idx_intersection in range(len(intersection)):
    slide_name = list(intersection)[sample_idx_intersection] + ".svs"
    print("Processing {}".format(slide_name))
    img_fn = glob(os.path.join(img_dir_root, "*", slide_name))[0]

    geojson_fn = os.path.join(geojson_dir_root, slide_name.replace(".svs", ".geojson"))
    # Read image, down sample it
    wsi_obj = openslide.OpenSlide(img_fn)
    width, height = wsi_obj.dimensions
    wsi_prop = dict(wsi_obj.properties)
    if wsi_prop.get("openslide.mpp-x") == None:
        pixel_size = ""
        print("Don't know the pixel size")
    else:
        pixel_size = wsi_prop["openslide.mpp-x"]
    
    slide_id = get_slide_id(img_fn)
    wrt_str = ",".join([slide_id, slide_name,str(width),str(height),str(pixel_size)]) + "\n" 
    fp.write(wrt_str)

    sv_fn = os.path.join(out_dir, slide_name.replace(".svs", ".jpg"))
    if not os.path.exists(sv_fn):
        thumbnail = get_thumbnails(wsi_obj, down_sample_rate)
        roi_data = gpd.read_file(geojson_fn)

        fig, ax = plt.subplots(dpi=250)
        ax.imshow(thumbnail)
        for g in roi_data.geometry:
            coords = np.array(g.exterior.coords, dtype=float)/down_sample_rate
            polygon_vertices = list(coords)
            polygon = patches.Polygon(polygon_vertices, closed=True, fill=False, edgecolor='red', linewidth=2)
            ax.add_patch(polygon)
        plt.show()
        plt.axis(False)
        
        plt.savefig(sv_fn)
    else:
        print("File already saved")

fp.close()

# TODO: make the output compatible to this tool?
# https://github.com/Nenotriple/img-txt_viewer 
# for model LoRA: https://github.com/microsoft/LoRA

