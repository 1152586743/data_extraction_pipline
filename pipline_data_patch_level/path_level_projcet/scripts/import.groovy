// === 将“点”转成方块patch并按 prob_tumor 着色（0.6 兼容） ===
import qupath.lib.objects.PathObjects
import qupath.lib.roi.ROIs

String MEAS = 'prob_tumor'
int PATCH = 256              // 方块边长（像素，与你的 patch_size 对齐）
boolean keepPoints = false   // 生成完是否保留原来的点

def anns = getAnnotationObjects()
def tiles = []
int made = 0, colored = 0

for (def o : anns) {
    def roi = o.getROI()
    if (roi == null) continue

    // 取概率：0.6 里需要遍历 measurement 列表
    Double v = null
    def ml = o.getMeasurementList()
    if (ml != null) {
        for (def m : ml.getMeasurements()) {
            if (m.getName() == MEAS) { v = m.getValue(); break }
        }
    }
    if (v == null || Double.isNaN(v)) continue

    // 以点为中心画一个方块（注意坐标是 level-0 像素）
    double cx = roi.getCentroidX()
    double cy = roi.getCentroidY()
    def rect = ROIs.createRectangleROI(cx - PATCH/2.0, cy - PATCH/2.0, PATCH, PATCH)

    // 新建annotation方块；把原 measurementList 也带过去（便于后续用）
    def tile = PathObjects.createAnnotationObject(rect, null, ml)
    // 概率映射到颜色（蓝->红）
    double vv = Math.max(0, Math.min(1, v))
    int r = (int)Math.round(255*vv), g = 0, b = (int)Math.round(255*(1 - vv))
    tile.setColor(r, g, b)
    tile.setName('patch_tile')

    tiles << tile
    made++
    colored++
}

addObjects(tiles)
if (!keepPoints) {
    // 删除原始点，让画面更干净
    removeObjects(anns, true)
}
fireHierarchyUpdate()
print "Made ${made} tiles; colored ${colored} by ${MEAS}. PATCH=${PATCH}px"
