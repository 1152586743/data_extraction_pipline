
import os

dirs = os.listdir("/data/jjiang10/Data/ProstatePathology/WSIs")
sh_fn = open("extract_command.sh", "w")
# for slide_id in dirs:
#    command = "python create_patches_fp.py --source /data/jjiang10/Data/ProstatePathology/WSIs/%s --save_dir /data/jjiang10/Data/ProstatePathology/patches --patch_size 256 --seg\n" % slide_id
#    sh_fn.write(command)
# sh_fn.close()

for slide_id in dirs:
   command = "cp /data/jjiang10/Data/ProstatePathology/WSIs/%s/*.svs /data/jjiang10/Data/ProstatePathology/WSIs_bak\n" % slide_id
   sh_fn.write(command)
sh_fn.close()
