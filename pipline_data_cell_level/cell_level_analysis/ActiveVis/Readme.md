


``` bash
# COPY files to local Macbook
rsync -avz  jjiang10@eos:/data/jjiang10/Data/Gallbladder/foundation_model_features /Users/jjiang10/Data/Gallbladder/PatchAnalysis/
rsync -avz  jjiang10@eos:/data/jjiang10/Data/Gallbladder/preprocessing /Users/jjiang10/Data/Gallbladder/PatchAnalysis/


cd /Users/jjiang10/Projects/GitHub/GallbladderPath/patch_level_analysis/ActiveVis
conda activate marimo

marimo run tile_representation_umap.py

```


