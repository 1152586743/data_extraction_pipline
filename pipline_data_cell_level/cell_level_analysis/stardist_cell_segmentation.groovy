import qupath.ext.stardist.StarDist2D

// Specify the model directory (you will need to change this!)
def pathModel = '/Users/jjiang10/Data/Gallbladder/CellSegmentation/Pretrained_models/he_heavy_augment.pb'
def stardist = StarDist2D.builder(pathModel)
      .threshold(0.5)              // Prediction threshold
      .normalizePercentiles(1, 99) // Percentile normalization
      .pixelSize(0.1213)              // Resolution for detection
      .cellExpansion(5.0)
      .cellConstrainScale(1.5)
      .measureShape()
      .measureIntensity()
      .build()
// Run detection for the selected objects
def imageData = getCurrentImageData()
def pathObjects = getSelectedObjects()
if (pathObjects.isEmpty()) {
    Dialogs.showErrorMessage("StarDist", "Please select a parent object!")
    return
}
stardist.detectObjects(imageData, pathObjects)
println 'Done!'

