
### Download and process the pathology dataset 
1. The steps for downloading the dataset are described in [this Jupyter Notebook](./data_preprocessing/download_dataset.ipynb).
2. Visually inspect the dataset examples in [this Jupyter Notebook](./data_preprocessing/data_example_vis.ipynb).
3. To find some pattern, create visualization for all the samples within this dataset [visualize_all.py](./data_preprocessing/visualize_all.py).
4. Load geojson annotations into QuPath. Within QuPath, File–>Import objects from file. 
5. preprocess the labels within this dataset [slide_label_processing.py](./data_preprocessing/slide_label_processing.py). Simplify the label from "Gleason Score 5+3" to "5+3". CSV_FILE = "slide_label_PRAD_label_edited.csv"

### Use CLAM pipeline to get the patches and their embeddings
1. Extract patches
2. Get patch embeddings/features
3. Visualize patch embeddings with UMAP
> Details in [feature_extraction.ipynb](./feature_extraction/feature_extraction.ipynb)
4. TODO: use simplified slide level label and patch level features to train the CLAM model for attentions scores.
5. TODO: visualize the attentions, compare with pathologists' polygon annotations.

### Interactively visualize image embeddings
1. Install the environment to local (MacBook)
``` bash
conda create --prefix=/xxx/marimo python=3.8
conda activate marimo
conda install openslide
conda install marimo
```
2. run the script within ActiveVis
``` bash
cd img_features/ActiveVis/
marimo run tile_representation_umap.py
```
If you would like to edit the code, run 
``` bash
marimo edit tile_representation_umap.py
```




### Voice to text annotation


###### Download the radiology dataset (maybe useful in the future)
Since the public dataset is from TCGA-PRAD, there are also corresponding radiology datasets.
refer to [radiology_dataset.ipynb](./data_preprocessing/radiology_dataset.ipynb)
