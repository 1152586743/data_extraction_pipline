// === Import cell predictions into current image (QuPath 0.5.x) ===
// Expects: data_dir/<case_id>/detections_prediction.txt
// TSV no header columns:
// 0:id 1:score 2:label 3:reserved 4:Centroid X µm 5:Centroid Y µm

import qupath.lib.gui.scripting.QPEx
import qupath.lib.geom.Point2

// ---- EDIT THIS ----
def data_dir = "/Users/yhu10/Desktop/VLM/pipline_data_cell_level/cell_level_analysis"
// -------------------

def imageData = QPEx.getCurrentImageData()
def server = imageData.getServer()
def imageName = server.getMetadata().getName()
int dot = imageName.lastIndexOf('.')
def case_id = (dot > 0) ? imageName.substring(0, dot) : imageName
print("Processing case " + case_id + "\n")

def txt_fn = data_dir + File.separator + case_id + File.separator + "detections_prediction.txt"
def fh = new File(txt_fn)
if (!fh.exists()) {
    print("ERROR: File not found: " + txt_fn + "\n")
    return
}

// pixel size (µm/px) with fallback
def cal = server.getPixelCalibration()
double p_sz_w = cal.getPixelWidthMicrons()
double p_sz_h = cal.getPixelHeightMicrons()
if (!p_sz_w || !p_sz_h || Double.isNaN(p_sz_w) || Double.isNaN(p_sz_h)) {
    p_sz_w = 0.4990; p_sz_h = 0.4990
}

// read predictions
List<Point2> cell_loc_list = new ArrayList<>()
List<String> cell_class_list = new ArrayList<>()

fh.eachLine('UTF-8') { ln ->
    if (ln == null || ln.trim().isEmpty()) { return }
    def parts = ln.split('\t', -1)
    if (parts.size() < 6) { return }
    String label = parts[2]
    double cx_um = parts[4] as Double
    double cy_um = parts[5] as Double
    cell_loc_list.add(new Point2(cx_um, cy_um))
    cell_class_list.add(label)
}

print(String.format("Loaded %d predictions\n", cell_loc_list.size()))

int tol_px_x = 10, tol_px_y = 10  // tolerance; increase to 15–20 if needed
def detections = QPEx.getDetectionObjects()
int matched = 0

for (int i = 0; i < detections.size(); i++) {
    def d = detections[i]
    if (!d.isCell()) { continue }
    int cell_x = (int) d.getROI().getCentroidX()
    int cell_y = (int) d.getROI().getCentroidY()

    for (int j = 0; j < cell_loc_list.size(); j++) {
        def loc = cell_loc_list[j]
        int x = (int) (loc.x / p_sz_w)
        int y = (int) (loc.y / p_sz_h)
        if (Math.abs(cell_x - x) <= tol_px_x && Math.abs(cell_y - y) <= tol_px_y) {
            d.setPathClass(QPEx.getPathClass(cell_class_list[j]))
            matched++
            break
        }
    }
}

QPEx.fireHierarchyUpdate()
print(String.format("Done. Matched & updated %d cells.\n", matched))
