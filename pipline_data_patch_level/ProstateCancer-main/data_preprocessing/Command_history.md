
#### Copy code from server to local
scp -r jjiang10@eos://data/jjiang10/Projects/GitHub/ProstateCancer /Users/jjiang10/Projects/GitHub/ProstateCancer
rsync -avz jjiang10@eos://data/jjiang10/Projects/GitHub/ProstateCancer /Users/jjiang10/Projects/GitHub/ProstateCancer


rsync -avz jjiang10@eos://data/jjiang10/Data/ProstatePathology/output/features_umap/ /Users/jjiang10/Data/ProstateCancer/output/features_umap/

#### Copy WSI from the server
 scp jjiang10@eos:///data/jjiang10/Data/ProstatePathology/WSIs/9f7fbd02-67ea-4b15-a3ed-98c51daecaa4/TCGA-KK-A8IF-01Z-00-DX1.D89CE36A-8166-4CA5-82DE-A937ABBF14D0.svs ./

#### Copy annotation from the server
scp jjiang10@eos:///data/jjiang10/Data/ProstatePathology/dataset/PRAD/TCGA-KK-A8IF-01Z-00-DX1.D89CE36A-8166-4CA5-82DE-A937ABBF14D0.geojson ./




scp jjiang10@eos:///data/jjiang10/Data/ProstatePathology/WSIs/8afc3e55-fcaf-4328-9b5a-a01bcee181cc/TCGA-EJ-7789-01Z-00-DX1.1fe607cd-e166-4c16-8fc0-74bcca9b5975.svs ./
scp jjiang10@eos:///data/jjiang10/Data/ProstatePathology/dataset/PRAD/TCGA-EJ-7789-01Z-00-DX1.1fe607cd-e166-4c16-8fc0-74bcca9b5975.geojson ./


#### run Patch extraction for the CLAM model
python create_patches_fp.py --source DATA_DIRECTORY --save_dir RESULTS_DIRECTORY --patch_size 256 --seg --patch --stitch 


python create_patches_fp.py --source /data/jjiang10/Data/ProstatePathology/WSIs/f4d3a4e0-65c9-4022-a39f-2901ccd11ced --save_dir /data/jjiang10/Data/ProstatePathology/patches --patch_size 256 --seg

rsync -avz jjiang10@eos://data/jjiang10/Data/ProstatePathology/patches /Users/jjiang10/Downloads
