# Test the Grad-CAM on eos
## Install the environment
``` bash
conda create --prefix=/data/jjiang10/conda_envs/grad_cam
conda activate grad_cam
conda install pip
pip install grad_cam
pip install transformers

cd /data/jjiang10/Projects
git clone https://github.com/jacobgil/pytorch-grad-cam.git

cd pytorch-grad-cam/usage_examples/
python clip_example.py 

```
## Test pathology images

Make directory on server and copy test data from local data path
``` bash
cd /data/jjiang10/Data/ProstatePathology/
mkdir attention_demo_imgs
cd attention_demo_imgs/
mkdir input
mkdir output

scp /Users/jjiang10/Data/ProstateCancer/MultipleScaleAttention/*.jpeg jjiang10@eos:/data/jjiang10/Data/ProstatePathology/attention_demo_imgs/input

```
Run testing code
``` bash
cd /data/jjiang10/Projects/pytorch-grad-cam/usage_examples
cp ../../GitHub/ProstateCancer/AttentionMap/my_clip_example.py  ./
conda activate grad_cam
python my_clip_example.py --image-path /data/jjiang10/Data/ProstatePathology/attention_demo_imgs/input --output_dir /data/jjiang10/Data/ProstatePathology/attention_demo_imgs/output
```
inputs are 
``` bash
SCR-20250216-0.jpeg
SCR-20250216-10x.jpeg
SCR-20250216-1.jpeg
SCR-20250216-20x.jpeg
SCR-20250216-40x.jpeg
SCR-20250216-4.jpeg
SCR-20250216-60x.jpeg
SCR-20250216-6x.jpeg
SCR-20250216_80x.jpeg
SCR-20250216-8x.jpeg
```
Outputs are
``` bash
a cat: 0.3761
a dog: 0.2877
a car: 0.0179
a person: 0.3093
a shoe: 0.0090
a cat: 0.3377
a dog: 0.3904
a car: 0.0204
a person: 0.2506
a shoe: 0.0009
a cat: 0.2324
a dog: 0.3517
a car: 0.0451
a person: 0.3686
a shoe: 0.0021
a cat: 0.2097
a dog: 0.2552
a car: 0.0512
a person: 0.4820
a shoe: 0.0019
a cat: 0.3553
a dog: 0.4566
a car: 0.0256
a person: 0.1602
a shoe: 0.0022
a cat: 0.2553
a dog: 0.2994
a car: 0.0360
a person: 0.4077
a shoe: 0.0016
a cat: 0.2801
a dog: 0.1882
a car: 0.0420
a person: 0.4882
a shoe: 0.0015
a cat: 0.3136
a dog: 0.4023
a car: 0.0185
a person: 0.2632
a shoe: 0.0023
a cat: 0.2800
a dog: 0.4116
a car: 0.0313
a person: 0.2743
a shoe: 0.0028
a cat: 0.2842
a dog: 0.2320
a car: 0.0400
a person: 0.4432
a shoe: 0.0006
```
scp -r jjiang10@eos:/data/jjiang10/Data/ProstatePathology/attention_demo_imgs/output ~/Downloads/

# Test CLAM heatmap
``` bash
conda activate clam_latest
cd CLAM
```
Modify the config file, copy a config_template.yaml to config_prostate_cancer.yaml

``` bash
raw_save_dir
production_save_dir
data_dir
# add the files into process_list
process_list 


```

``` bash
CUDA_VISIBLE_DEVICES=0,1 python create_heatmaps.py --config config_prostate_cancer.yaml



```