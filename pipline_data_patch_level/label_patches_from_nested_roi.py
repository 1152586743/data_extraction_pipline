# /Users/yhu10/Desktop/VLM/pipline_data_patch_level/label_patches_from_nested_roi.py
from pathlib import Path
import h5py, json, pandas as pd
from shapely.geometry import shape, Point

slide_id = "CMU-2"

h5_path    = Path("/Users/yhu10/Desktop/VLM/pipline_data_patch_level/data/patches") / f"{slide_id}.h5"
geojson_fn = Path("/Users/yhu10/Desktop/VLM/pipline_data_patch_level/path_level_projcet") / f"{slide_id}.geojson"
out_csv    = Path("/Users/yhu10/Desktop/VLM/pipline_data_patch_level/data/labels") / f"{slide_id}_patch_labels.csv"

assert h5_path.exists(), f"patch h5 not found: {h5_path}"
assert geojson_fn.exists(), f"geojson not found: {geojson_fn}"
out_csv.parent.mkdir(parents=True, exist_ok=True)

def get_class_lower(props: dict) -> str:
    """
    Robustly extract a lowercase class name from various QuPath/GeoJSON schemas.
    """
    if not isinstance(props, dict):
        return ""
    cand = props.get("classification", None)
    # classification may be dict like {"name":"Tumor", ...}
    if isinstance(cand, dict):
        name = cand.get("name") or cand.get("displayName") or ""
        return str(name).lower()
    # or a raw string
    if isinstance(cand, str):
        return cand.lower()
    # fallbacks
    for k in ("name", "class", "pathClass", "classificationName", "Label"):
        v = props.get(k, "")
        if isinstance(v, dict):
            v = v.get("name", "")
        if isinstance(v, str) and v:
            return v.lower()
    return ""

# load polygons
g = json.load(open(geojson_fn))
tumor_polys, outer_polys = [], []
classes_seen = []

for feat in g.get("features", []):
    props = feat.get("properties") or {}
    cls = get_class_lower(props)
    classes_seen.append(cls or "<empty>")
    geom = shape(feat["geometry"])  # handles Polygon/MultiPolygon
    if "tumor" in cls:
        tumor_polys.append(geom)
    else:
        # treat any non-tumor annotation as outer ROI
        outer_polys.append(geom)

print("Found classes in GeoJSON:", sorted(set(classes_seen)))

def inside(polys, x, y):
    p = Point(float(x), float(y))
    # contains() excludes boundary; within/on edge handling:
    return any(poly.contains(p) or poly.touches(p) for poly in polys)

# label patches
rows = []
with h5py.File(h5_path, "r") as f:
    coords = f["coords"][:]  # (N,2) level-0 (x,y)

for i, (x, y) in enumerate(coords):
    if inside(tumor_polys, x, y):
        lab = "tumor"
    elif inside(outer_polys, x, y):
        lab = "benign"
    else:
        continue  # outside outer ROI → ignore
    rows.append({"slide_id": slide_id, "patch_id": i, "x": int(x), "y": int(y), "label": lab})

df = pd.DataFrame(rows)
df.to_csv(out_csv, index=False)
print("Saved:", out_csv)
print(df["label"].value_counts())
