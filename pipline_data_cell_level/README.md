# Cell-level Pipeline (from QuPath to UMAP)
- Default directory is current one

## 1) QuPath: create a project, draw ROI, detect cells, add a few labels
- Open QuPath, create a project, add your slide(s).
- Draw an ROI.
- Use **StarDist** or **Analyze → Cell detection → Cell detection…** to detect cells inside the ROI.
- Manually label a small subset of cells.

## 2) Export labeled cells for training
- In QuPath, go to **Measure → Export measurements…**.
- **Export type: Cells** (important).
- Export to TSV (this TSV will be used to train the classifier).
- data/measurement.tsv

## 3) Classify and auto-label the remaining cells
- Run the notebook:  
  `cell_level_analysis/classification.ipynb`
- It uses the exported TSV to train a classifier and then labels the other cells in the ROI.
- It writes two files:
  - **TXT**: predictions only (`CMU-2/detections_prediction.txt`)
  - **TSV**: UMAP features (`*_cell_feature_umap.tsv`)

## 4) Import predictions back into QuPath
- Use the Groovy script to import from the TXT:  
  `scripts/import_back.groovy`
- This will assign the predicted labels to cells in QuPath.

## 5) Interactive UMAP
- Update the TSV and image paths, then run:  
  `cell_level_analysis/ActiveVis/cell_representation_umap.py`
- This shows the interactive UMAP and the corresponding slide patches.
