import h5py, os
import geopandas as gpd
from shapely.geometry import Point

def assign_labels_to_patches(anno_data_dir, patch_data_dir, slide_name):
    geojson_anno_fn = os.path.join(anno_data_dir, slide_name + ".geojson")   
    patch_loc_fn = os.path.join(patch_data_dir, slide_name + ".h5") 

    if not os.path.exists(geojson_anno_fn):
        raise FileNotFoundError(f"GeoJSON file {geojson_anno_fn} not found.")
    if not os.path.exists(patch_loc_fn):
        raise FileNotFoundError(f"HDF5 file {patch_loc_fn} not found.") 
    
    # Load the GeoJSON file
    polygons = gpd.read_file(geojson_anno_fn)

    # Function to assign labels to image patches
    
    def assign_labels(image_patches, polygons):
        labeled_patches = []
        count = 0
        for patch in image_patches:
            point = Point(patch['coordinates'])
            label = "None"  # Default label
            for _, row in polygons.iterrows():
                if 'classification'in row.keys():
                    if row['classification'] is not None:
                        if row['geometry'].contains(point):
                            classification = eval(row['classification'])  # Convert the string to a dictionary
                            label = classification['name']
                            count += 1
                            break
                        else:
                            continue
                    else:
                        continue
                else:
                    label = 'None'
            labeled_patches.append({'id': patch['id'], 'coordinates': patch['coordinates'], 'label': label})
        return labeled_patches, count

    # Load the HDF5 file
    with h5py.File(patch_loc_fn, 'r') as h5_file:
        coords = h5_file['coords'][:]

    # Convert coordinates to a list of dictionaries
    image_patches = [{'id': i, 'coordinates': (coord[0], coord[1])} for i, coord in enumerate(coords)]
    print("Number of image patches:", len(image_patches))

    # Assign labels to the image patches
    labeled_patches, cnt = assign_labels(image_patches, polygons)

    # # Print the labeled patches
    # for patch in labeled_patches:
    #     print(f"Patch ID: {patch['id']}, Coordinates: {patch['coordinates']}, Label: {patch['label']}")

    print("Number of labeled patches %d in %d:" % (cnt, len(labeled_patches)))
    return labeled_patches


if __name__ == "__main__":
    anno_data_dir = "/data/jjiang10/Data/ProstatePathology/dataset/PRAD"
    patch_data_dir = "/data/jjiang10/Data/ProstatePathology/processed/patches"
    slide_name = "TCGA-YL-A9WI-01Z-00-DX4.DD0313AF-7339-45F1-B3CF-AE9C20679E7F"

    labeled_patches = assign_labels_to_patches(anno_data_dir, patch_data_dir, slide_name)
