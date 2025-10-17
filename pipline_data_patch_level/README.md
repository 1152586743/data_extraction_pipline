# Patch-level Pipeline 

## Step 1: Export Annotation from QuPath
- Open your WSI (whole slide image) in QuPath.
- Annotate the desired ROI regions (e.g., tumor vs stroma).
- Select the annotation.
- Go to File → Export → Export selected objects.
- Save it as a GeoJSON file (e.g., CMU-2.geojson).

## Step 2: Using CLAM to Create Patches from Whole Slide

cd /Users/yhu10/Desktop/VLM/pipline_data_patch_level/ProstateCancer-main/CLAM

PYTHONPATH=. python create_patches_fp.py \
  --source /Users/yhu10/Desktop/VLM/pipline_data_patch_level/data/slides \
  --save_dir /Users/yhu10/Desktop/VLM/pipline_data_patch_level/data \
  --patch_size 256 --step_size 256 \
  --seg --patch --stitch \
  --patch_level 0
**Expected outputs:**
- data/patches/CMU-2.h5
- data/masks/CMU-2.jpg
- data/stitches/CMU-2.jpg

## Step 3: Label Patches Using ROI (Nested ROI → CSV)
python /Users/yhu10/Desktop/VLM/pipline_data_patch_level/label_patches_from_nested_roi.py \
  --wsi_id CMU-2 \
  --wsi_h5 /Users/yhu10/Desktop/VLM/pipline_data_patch_level/data/patches/CMU-2.h5 \
  --roi_geojson /Users/yhu10/Desktop/VLM/pipline_data_patch_level/path_level_projcet/CMU-2.geojson \
  --out_csv /Users/yhu10/Desktop/VLM/pipline_data_patch_level/data/labels/CMU-2_patch_labels.csv

**Expected outputs:**
data/labels/CMU-2_patch_labels.csv

## Step 4: Train Patch-level Classifier
python /Users/yhu10/Desktop/VLM/pipline_data_patch_level/train_patch_clf.py \
  --labels_csv /Users/yhu10/Desktop/VLM/pipline_data_patch_level/data/labels/CMU-2_patch_labels.csv \
  --h5_file /Users/yhu10/Desktop/VLM/pipline_data_patch_level/data/patches/CMU-2.h5 \
  --out_dir /Users/yhu10/Desktop/VLM/pipline_data_patch_level/runs/patch_clf

**Expected outputs:**
runs/patch_clf/resnet18_best.pt

## Step 5: Apply Classifier to Whole Slide
python /Users/yhu10/Desktop/VLM/pipline_data_patch_level/infer_slide_patch_probs.py \
  --model /Users/yhu10/Desktop/VLM/pipline_data_patch_level/runs/patch_clf/resnet18_best.pt \
  --h5_file /Users/yhu10/Desktop/VLM/pipline_data_patch_level/data/patches/CMU-2.h5 \
  --out_csv /Users/yhu10/Desktop/VLM/pipline_data_patch_level/runs/patch_clf/CMU-2_pred.csv

**Expected outputs:**
runs/patch_clf/CMU-2_pred.csv

## Step 6: Convert Predictions to GeoJSON (for QuPath)
python /Users/yhu10/Desktop/VLM/pipline_data_patch_level/pred_csv_to_geojson.py

**Expected outputs:**
runs/patch_clf/CMU-2_pred.geojson

## Step 7: Visualize in QuPath
- Open the slide in QuPath.
- Go to File → Import objects from file…
- Select:
/Users/yhu10/Desktop/VLM/pipline_data_patch_level/runs/patch_clf/CMU-2_pred.geojson
- Click any patch → Check the Measurements tab → You should see
- prob_tumor (predicted tumor probability).

## Step 8: Heatmap
- Finally, use the provided Groovy script to create heatmap:
pipline_data_patch_level/path_level_projcet/scripts/import.groovy/import.groovy