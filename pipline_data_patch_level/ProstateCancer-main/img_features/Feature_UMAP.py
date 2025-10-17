
from PatchLabels import assign_labels_to_patches
import h5py, os
from glob import glob
import numpy as np
from scipy.stats import entropy
import matplotlib.patches as mpatches

def get_embedding_folder(root_dir, feature_option):
    if feature_option == "default":
        return os.path.join(root_dir, "features/h5_files")
    elif feature_option == "CONCH":
        return os.path.join(root_dir, "features_CONCH/h5_files")
    else:
        raise ValueError("Invalid feature option")


def get_slide_name_list(slide_file_dir, extension=".h5"):
    slide_fn_list = glob(os.path.join(slide_file_dir, "*" + extension))
    slide_names = [os.path.splitext(os.path.basename(fn))[0] for fn in slide_fn_list]
    return slide_names

def get_img_features(feature_folder, slide_name):
    feature_fn = os.path.join(feature_folder, slide_name + ".h5")
    with h5py.File(feature_fn, "r") as h5_file:
        features = h5_file["features"][:]
    return features

# calculate the Kullback-Leibler (KL) divergence between each pair of image labels
def calculate_label_pairwise_KL_divergence(patch_labels, patch_embeddings):
    # Group patch embeddings by labels
    label_to_embeddings = {}
    for patch, embedding in zip(patch_labels, patch_embeddings):
        label = patch['label']
        if label not in label_to_embeddings:
            label_to_embeddings[label] = []
        label_to_embeddings[label].append(embedding)

    # Calculate the mean of the embeddings for each label
    label_to_mean = {label: np.mean(embeddings, axis=0) for label, embeddings in label_to_embeddings.items()}

    # Calculate KL divergence between each pair of label means
    labels = list(label_to_mean.keys())
    kl_divergences = {}
    for i in range(len(labels)):
        for j in range(i + 1, len(labels)):
            label1 = labels[i]
            label2 = labels[j]
            mean1 = label_to_mean[label1]
            mean2 = label_to_mean[label2]
            kl_div = entropy(mean1, mean2)
            kl_divergences[(label1, label2)] = kl_div

    # Print KL divergences
    for (label1, label2), kl_div in kl_divergences.items():
        print(f"KL Divergence between {label1} and {label2}: {kl_div}")

    return kl_divergences


if __name__ == "__main__":
    import umap
    import matplotlib.pyplot as plt

    slide_file_dir = "/data/jjiang10/Data/ProstatePathology/processed/patches"
    slide_name_list = get_slide_name_list(slide_file_dir, extension=".h5")

    anno_data_dir = "/data/jjiang10/Data/ProstatePathology/dataset/PRAD"
    feature_root_dir = "/data/jjiang10/Data/ProstatePathology" # patch embeddings root directory

    feaute_options = ["default", "CONCH"]


    region_labels = ['Pattern 5', 'None', 'benign', 'Gleason Pattern 4+5', 'Gleason Pattern 4+4', 'Gleason Pattern 5+5', 'Gleason Pattern 5+3', 'Pattern 4 Glands', 'Gleason Pattern 4+3', 'Gleason Pattern 3+5', 'Gleason Pattern 5+4', 'Pattern 3 Glands', 'Gleason Pattern 3+4', 'Gleason Pattern 3+3']

    # Define a color map for the labels
    label_to_color = {
        'Pattern 5': 'purple',
        'None': 'gray',
        'benign': 'green',
        'Gleason Pattern 4+5': 'orange',
        'Gleason Pattern 4+4': 'yellow',
        'Gleason Pattern 5+5': 'brown',
        'Gleason Pattern 5+3': 'pink',
        'Pattern 4 Glands': 'blue',
        'Gleason Pattern 4+3': 'red',
        'Gleason Pattern 3+5': 'cyan',
        'Gleason Pattern 5+4': 'magenta',
        'Pattern 3 Glands': 'lime',
        'Gleason Pattern 3+4': 'navy',
        'Gleason Pattern 3+3': 'teal'
    }

    ump = umap.UMAP(random_state=12)

    for slide_name in slide_name_list:
        print("Processing slide:", slide_name)
        patch_labels = None
        for feature_option in feaute_options:
            output_dir = os.path.join(feature_root_dir, "output", "features_umap", feature_option)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            save_to = os.path.join(output_dir, slide_name + "_embed_umap.png")
            if os.path.exists(save_to):
                print(f"File {save_to} already exists. Skipping...")
                continue
            try:
                if patch_labels is None:
                    patch_labels = assign_labels_to_patches(anno_data_dir, slide_file_dir, slide_name)
                
                feature_folder = get_embedding_folder(feature_root_dir, feature_option)
                patch_embeddings = get_img_features(feature_folder, slide_name)

                ump_f = ump.fit_transform(patch_embeddings)

                colors = [label_to_color.get(p_label['label'], 'gray') for p_label in patch_labels]

                plt.figure(figsize=(8, 6), dpi=200)
                plt.scatter(ump_f[:, 0], ump_f[:, 1], marker=".", c=colors, alpha=0.6, s=2)
                plt.title("Image embeddings UMap")
                # Create legend
                legend_handles = [mpatches.Patch(color=color, label=label) for label, color in label_to_color.items()]
                plt.legend(handles=legend_handles, title="Labels", bbox_to_anchor=(1.05, 1), loc='upper left')

                plt.savefig(save_to, bbox_inches='tight')
                plt.close()
                # plt.show()
            except FileNotFoundError as e:
                print(e)
                continue
        

            
            





