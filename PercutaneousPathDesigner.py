import os
import unittest
from __main__ import vtk, qt, ctk, slicer

class PercutaneousPathDesigner:
  def __init__(self, parent):
    parent.title = "PercutaneousPathDesigner" # TODO make this more human readable by adding spaces
    parent.categories = ["IGT"]
    parent.dependencies = []
    parent.contributors = ["Atsushi Yamada (Shiga University of Medical Science)"] # replace with "Firstname Lastname (Org)"
    parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    """
    #parent.acknowledgementText = """
    #This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc. and Steve Pieper, Isomics, Inc.  and was partially funded by NIH grant 3P41RR013218-12S1.
#""" # replace with organization, grant and thanks.
    parent.acknowledgementText = """ """
    self.parent = parent

    # Add this test to the SelfTest module's list for discovery when the module
    # is created.  Since this module may be discovered before SelfTests itself,
    # create the list if it doesn't already exist.
    try:
      slicer.selfTests
    except AttributeError:
      slicer.selfTests = {}
    slicer.selfTests['PercutaneousPathDesigner'] = self.runTest

  def runTest(self):
    tester = PercutaneousPathDesignerTest()
    tester.runTest()

#
# qPercutaneousPathDesignerWidget
#

class PercutaneousPathDesignerWidget:
  def __init__(self, parent = None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()

  def setup(self):
    # Instantiate and connect widgets ...

    import numpy

    #
    # Reload and Test area
    #
    reloadCollapsibleButton = ctk.ctkCollapsibleButton()
    reloadCollapsibleButton.text = "Reload && Test"
    #reloadCollapsibleButton.collapsed = True
    self.layout.addWidget(reloadCollapsibleButton)
    reloadFormLayout = qt.QFormLayout(reloadCollapsibleButton)

    # reload button
    # (use this during development, but remove it when delivering
    #  your module to users)
    self.reloadButton = qt.QPushButton("Reload")
    self.reloadButton.toolTip = "Reload this module."
    self.reloadButton.name = "PercutaneousPathDesigner Reload"
    reloadFormLayout.addWidget(self.reloadButton)
    self.reloadButton.connect('clicked()', self.onReload)

    # reload and test button
    # (use this during development, but remove it when delivering
    #  your module to users)
    self.reloadAndTestButton = qt.QPushButton("Reload and Test")
    self.reloadAndTestButton.toolTip = "Reload this module and then run the self tests."
    reloadFormLayout.addWidget(self.reloadAndTestButton)
    self.reloadAndTestButton.connect('clicked()', self.onReloadAndTest)

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    parametersCollapsibleButton.collapsed = False
    self.parametersList = parametersCollapsibleButton   
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    #
    # Target point (vtkMRMLMarkupsFiducialNode)
    #
    self.targetSelector = slicer.qMRMLNodeComboBox()
    self.targetSelector.nodeTypes = ( ("vtkMRMLMarkupsFiducialNode"), "" )
    self.targetSelector.addEnabled = False
    self.targetSelector.removeEnabled = False
    self.targetSelector.noneEnabled = True
    self.targetSelector.showHidden = False
    self.targetSelector.showChildNodeTypes = False
    self.targetSelector.setMRMLScene( slicer.mrmlScene )
    self.targetSelector.setToolTip( "Pick up the target point" )
    parametersFormLayout.addRow("Target Point: ", self.targetSelector)

    #
    # Entry point list (vtkMRMLMarkupsFiducialNode)
    #
    self.entryPointsSelector = slicer.qMRMLNodeComboBox()
    self.entryPointsSelector.nodeTypes = ( ("vtkMRMLMarkupsFiducialNode"), "" )
    self.entryPointsSelector.addEnabled = False
    self.entryPointsSelector.removeEnabled = False
    self.entryPointsSelector.noneEnabled = True
    self.entryPointsSelector.showHidden = False
    self.entryPointsSelector.showChildNodeTypes = False
    self.entryPointsSelector.setMRMLScene( slicer.mrmlScene )
    parametersFormLayout.addRow("Output Fiducial List: ", self.entryPointsSelector)

    #
    # target model (vtkMRMLModelNode)
    #
    self.targetModelSelector = slicer.qMRMLNodeComboBox()
    self.targetModelSelector.nodeTypes = ( ("vtkMRMLModelNode"), "" )
    self.targetModelSelector.addEnabled = False
    self.targetModelSelector.removeEnabled = False
    self.targetModelSelector.noneEnabled =  True
    self.targetModelSelector.showHidden = False
    self.targetModelSelector.showChildNodeTypes = False
    self.targetModelSelector.setMRMLScene( slicer.mrmlScene )
    self.targetModelSelector.setToolTip( "Pick the target model to the algorithm." )

    #
    # Skin model (vtkMRMLModelNode)
    #
    self.skinModelSelector = slicer.qMRMLNodeComboBox()
    self.skinModelSelector.nodeTypes = ( ("vtkMRMLModelNode"), "" )
    self.skinModelSelector.addEnabled = False
    self.skinModelSelector.removeEnabled = False
    self.skinModelSelector.noneEnabled =  True
    self.skinModelSelector.showHidden = False
    self.skinModelSelector.showChildNodeTypes = False
    self.skinModelSelector.setMRMLScene( slicer.mrmlScene )
    self.skinModelSelector.setToolTip( "Pick the skin model to the algorithm." )
    parametersFormLayout.addRow("Skin Model: ", self.skinModelSelector)

    #
    # Skin model opacity slider
    #
    self.skinModelOpacitySlider = ctk.ctkSliderWidget()
    self.skinModelOpacitySlider.decimals = 0
    self.skinModelOpacitySlider.maximum = 1000
    self.skinModelOpacitySlider.minimum = 0
    self.skinModelOpacitySlider.value = 1000
    self.skinModelOpacitySlider.enabled = True#False
    parametersFormLayout.addRow("      Opacity:", self.skinModelOpacitySlider)

    #
    # Obstacle model (vtkMRMLModelNode)
    #
    self.obstacleModelSelector = slicer.qMRMLNodeComboBox()
    self.obstacleModelSelector.nodeTypes = ( ("vtkMRMLModelNode"), "" )
    self.obstacleModelSelector.addEnabled = False
    self.obstacleModelSelector.removeEnabled = False
    self.obstacleModelSelector.noneEnabled =  True
    self.obstacleModelSelector.showHidden = False
    self.obstacleModelSelector.showChildNodeTypes = False
    self.obstacleModelSelector.setMRMLScene( slicer.mrmlScene )
    self.obstacleModelSelector.setToolTip( "Pick the obstacle model to the algorithm." )
    parametersFormLayout.addRow("Obstacle Model: ", self.obstacleModelSelector)

    #
    # Obstacle model opacity slider
    #
    self.obstacleModelOpacitySlider = ctk.ctkSliderWidget()
    self.obstacleModelOpacitySlider.decimals = 0
    self.obstacleModelOpacitySlider.maximum = 1000
    self.obstacleModelOpacitySlider.minimum = 0
    self.obstacleModelOpacitySlider.value = 1000
    self.obstacleModelOpacitySlider.enabled = True#False
    parametersFormLayout.addRow("      Opacity:", self.obstacleModelOpacitySlider)
   
    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Path Analysis Start")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False    
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.targetSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.targetModelSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.obstacleModelSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.skinModelSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.entryPointsSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    self.skinModelOpacitySlider.connect('valueChanged(double)', self.skinModelOpacitySliderValueChanged)
    self.obstacleModelOpacitySlider.connect('valueChanged(double)', self.obstacleModelOpacitySliderValueChanged)

    #
    # Outcomes Area
    #
    outcomesCollapsibleButton = ctk.ctkCollapsibleButton()
    outcomesCollapsibleButton.text = "Outcomes"
    outcomesCollapsibleButton.collapsed = True
    self.layout.addWidget(outcomesCollapsibleButton)

    self.outcomesList = outcomesCollapsibleButton

    # Layout within the dummy collapsible button
    outcomesFormLayout = qt.QFormLayout(outcomesCollapsibleButton)

    #
    # Check box for displaying all paths
    #
    self.allPathsCheckBox = ctk.ctkCheckBox()
    self.allPathsCheckBox.text = "All Paths (Yellow)"
    self.allPathsCheckBox.enabled = False
    self.allPathsCheckBox.checked = True
    outcomesFormLayout.addRow(self.allPathsCheckBox)

    #
    # Numbers of approchable polygons
    #
    self.numbersOfAllpathsSpinBox = ctk.ctkDoubleSpinBox()
    self.numbersOfAllpathsSpinBox.decimals = 0
    self.numbersOfAllpathsSpinBox.minimum = 0
    self.numbersOfAllpathsSpinBox.maximum = 10000000
    self.numbersOfAllpathsSpinBox.enabled = False
    self.numbersOfAllpathsSpinBox.suffix = ""
    outcomesFormLayout.addRow("      Numbers of All Paths: ", self.numbersOfAllpathsSpinBox)

    #
    # Opacity slider
    #
    self.allPathsOpacitySlider = ctk.ctkSliderWidget()
    self.allPathsOpacitySlider.decimals = 0
    self.allPathsOpacitySlider.maximum = 1000
    self.allPathsOpacitySlider.minimum = 0
    self.allPathsOpacitySlider.value = 10
    self.allPathsOpacitySlider.enabled = False#True
    outcomesFormLayout.addRow("      Opacity:", self.allPathsOpacitySlider)

    #
    # Check box for displaying each path
    #
    self.maximumLengthPathCheckBox = ctk.ctkCheckBox()
    self.maximumLengthPathCheckBox.text = "The Longest Path (Green)"
    outcomesFormLayout.addRow(self.maximumLengthPathCheckBox)

    #
    # Maximum Length
    #
    self.maximumLengthSpinBox = ctk.ctkDoubleSpinBox()
    self.maximumLengthSpinBox.decimals = 1
    self.maximumLengthSpinBox.minimum = 0
    self.maximumLengthSpinBox.maximum = 10000000
    self.maximumLengthSpinBox.enabled = False
    self.maximumLengthSpinBox.suffix = ""
    outcomesFormLayout.addRow("      Length (mm): ", self.maximumLengthSpinBox)

    #
    # Maximum Length Path
    #
    self.maximumLengthPathSpinBox = ctk.ctkDoubleSpinBox()
    self.maximumLengthPathSpinBox.decimals = 0
    self.maximumLengthPathSpinBox.minimum = 0
    self.maximumLengthPathSpinBox.maximum = 10000000
    self.maximumLengthPathSpinBox.enabled = False
    self.maximumLengthPathSpinBox.suffix = ""
    outcomesFormLayout.addRow("      Path (No.): ", self.maximumLengthPathSpinBox)

    #
    # Check box for displaying each path
    #
    self.minimumLengthPathCheckBox = ctk.ctkCheckBox()
    self.minimumLengthPathCheckBox.text = "The Shortest Path (Blue)"
    outcomesFormLayout.addRow(self.minimumLengthPathCheckBox)

    #
    # Minimum Length
    #
    self.minimumLengthSpinBox = ctk.ctkDoubleSpinBox()
    self.minimumLengthSpinBox.decimals = 1
    self.minimumLengthSpinBox.minimum = 0
    self.minimumLengthSpinBox.maximum = 10000000
    self.minimumLengthSpinBox.enabled = False
    self.minimumLengthSpinBox.suffix = ""
    outcomesFormLayout.addRow("      Length (mm): ", self.minimumLengthSpinBox)

    #
    # Minimum Length Path
    #
    self.minimumLengthPathSpinBox = ctk.ctkDoubleSpinBox()
    self.minimumLengthPathSpinBox.decimals = 0
    self.minimumLengthPathSpinBox.minimum = 0
    self.minimumLengthPathSpinBox.maximum = 10000000
    self.minimumLengthPathSpinBox.enabled = False
    self.minimumLengthPathSpinBox.suffix = ""
    outcomesFormLayout.addRow("      Path (No.): ", self.minimumLengthPathSpinBox)

    #
    # Check box for displaying each path
    #
    self.pathCandidateCheckBox = ctk.ctkCheckBox()
    self.pathCandidateCheckBox.text = "Path Candidate (Red)"
    self.pathCandidateCheckBox.enabled = False 
    self.pathCandidateCheckBox.checked = False    
    outcomesFormLayout.addRow(self.pathCandidateCheckBox)

    # Path slider
    self.pathSlider = ctk.ctkSliderWidget()
    self.pathSlider.decimals = 0
    self.pathSlider.enabled = False
    outcomesFormLayout.addRow("      Path Candidate (No.):", self.pathSlider)

    # Point slider
    self.pointSlider = ctk.ctkSliderWidget()
    self.pointSlider.decimals = 0
    self.pointSlider.maximum = 5000
    self.pointSlider.minimum = -5000
    self.pointSlider.enabled = False
    outcomesFormLayout.addRow("      Point Candidate on the Path:", self.pointSlider)

    #
    # Length of the path
    #
    self.lengthOfPathSpinBox = ctk.ctkDoubleSpinBox()
    self.lengthOfPathSpinBox.decimals = 1
    self.lengthOfPathSpinBox.minimum = 0
    self.lengthOfPathSpinBox.maximum = 10000000
    self.lengthOfPathSpinBox.enabled = False
    self.lengthOfPathSpinBox.suffix = ""
    outcomesFormLayout.addRow("      Length (mm): ", self.lengthOfPathSpinBox)

    # create point on the path
    self.createPointOnThePathButton = qt.QPushButton("Create Point on the Path")
    self.createPointOnThePathButton.enabled = False
    outcomesFormLayout.addRow("      Point on the Path:", self.createPointOnThePathButton)

    # connections
    self.pathCandidateCheckBox.connect("clicked(bool)", self.onCheckPathCandidate)
    self.allPathsCheckBox.connect("clicked(bool)", self.onCheckAllPaths)
    self.createPointOnThePathButton.connect('clicked(bool)', self.onCreatePointOnThePathButton)
    self.pathSlider.connect('valueChanged(double)', self.pathSliderValueChanged)
    self.pointSlider.connect('valueChanged(double)', self.pointSliderValueChanged)
    self.allPathsOpacitySlider.connect('valueChanged(double)', self.allPathsOpacitySliderValueChanged)

    self.maximumLengthPathCheckBox.connect("clicked(bool)", self.onCheckTheLongestPath)
    self.minimumLengthPathCheckBox.connect("clicked(bool)", self.onCheckTheShortestPath)

    #
    # Configuration Area
    #
    configurationCollapsibleButton = ctk.ctkCollapsibleButton()
    configurationCollapsibleButton.text = "Configurations"
    configurationCollapsibleButton.collapsed = True
    self.layout.addWidget(configurationCollapsibleButton)

    # Layout within the dummy collapsible button
    configurationFormLayout = qt.QFormLayout(configurationCollapsibleButton)

    #
    # Delete Models Button
    #
    self.deleteModelsButton = qt.QPushButton("Delete Paths")
    self.deleteModelsButton.toolTip = "Delete Created Paths and Transforms"
    self.deleteModelsButton.enabled = False    
    #configurationFormLayout.addRow(self.deleteModelsButton)
    configurationFormLayout.addWidget(self.deleteModelsButton)
 
    self.deleteModelsButton.connect('clicked()', self.onDeleteModelsButton)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Switch to distinguish between a point target and a target model
    self.targetSwitch = 0

    # Create an array for all approachable points
    # tempolary solution 
    self.apReceived = numpy.zeros([10000,3])
  
    self.nPointsReceived = 0
    self.nPathReceived = 0
    self.frameSliderValue = 0

    self.pathSliderValue = 0
    self.pointSliderValue = 0

    # avoid initializing error for frameSliderValueChanged(self, newValue) function
    self.tmpSwitch = 0

    self.pointMarker = slicer.vtkMRMLModelDisplayNode()
    self.pointMarkerTransform = slicer.vtkMRMLLinearTransformNode()
    self.virtualMarker = slicer.vtkMRMLModelDisplayNode()
    self.virtualMarkerTransform = slicer.vtkMRMLLinearTransformNode()

    self.allPaths = slicer.vtkMRMLModelDisplayNode()
    self.candidatePath = slicer.vtkMRMLModelDisplayNode()

    self.pathReceived = numpy.zeros([10000,3])

    self.markerPosition = numpy.zeros([3])
    self.virtualMarkerPosition = numpy.zeros([3])

    self.onePathDistance = 0
    self.virtualPathDistance = 0

    self.distanceDummy = 0;

    # switch
    self.ON = 1
    self.OFF = 0
    self.VISIBLE = 1
    self.INVISIBLE = 0

    # model variables
    self.modelReceived = slicer.vtkMRMLModelNode()
    self.singlePathModel = slicer.vtkMRMLModelNode()
    self.virtualPathModel = slicer.vtkMRMLModelNode()   
    self.selectedPathTipModel = slicer.vtkMRMLModelNode()
    self.extendedPathTipModel = slicer.vtkMRMLModelNode()
    self.longestPathTipModel = slicer.vtkMRMLModelNode()
    self.shortestPathTipModel = slicer.vtkMRMLModelNode()
    self.plannedEntryPointModel = slicer.vtkMRMLModelNode()

    self.minimumPoint = 0
    self.maximumPoint = 0
    self.minimumDistance = 0
    self.maximumDistance = 0

    # line colors
    self.yellow = [1, 1, 0]
    self.red = [1, 0, 0]
    self.green = [0, 1, 0]
    self.blue = [0, 0, 1]

    # line models
    self.allLines = vtk.vtkPolyData()
    self.singleLine = vtk.vtkPolyData()
    self.extendedLine = vtk.vtkPolyData()
    self.longestLine = vtk.vtkPolyData()
    self.shortestLine = vtk.vtkPolyData()

  def cleanup(self):
    pass

  def pathSliderValueChanged(self,newValue):
    logic = PercutaneousPathDesignerLogic()
    self.pathSliderValue = newValue

    self.onePath, self.onePathDistance = logic.makeSinglePath(self.apReceived, self.pathSliderValue)
    NeedlePathModel().modify(self.onePath, 1, self.VISIBLE, self.red, "pathCandidate", self.singleLine)

    self.markerPosition = SphereModel().move(self.apReceived, self.pathSliderValue, 0, self.pointMarkerTransform)
    self.virtualMarkerPosition = SphereModel().move(self.apReceived, self.pathSliderValue, self.pointSliderValue, self.virtualMarkerTransform)
 
    self.virtualPath, self.virtualPathDistance = logic.makeVirtualPath(self.apReceived, self.pathSliderValue, self.virtualMarkerPosition)
    NeedlePathModel().modify(self.virtualPath, 1, self.VISIBLE, self.red, "extendedPath", self.extendedLine)
   
    self.lengthOfPathSpinBox.value = self.virtualPathDistance + self.onePathDistance

  def pointSliderValueChanged(self,newValue):
    logic = PercutaneousPathDesignerLogic()
    self.pointSliderValue = newValue

    self.virtualMarkerPosition = SphereModel().move(self.apReceived, self.pathSliderValue, self.pointSliderValue, self.virtualMarkerTransform)
    
    self.virtualPath, self.virtualPathDistance = logic.makeVirtualPath(self.apReceived, self.pathSliderValue, self.virtualMarkerPosition)
    NeedlePathModel().modify(self.virtualPath, 1, self.VISIBLE, self.red, "extendedPath", self.extendedLine)

    self.lengthOfPathSpinBox.value = self.virtualPathDistance

  def skinModelOpacitySliderValueChanged(self,newValue):
    if(self.skinModelSelector.currentNode() != None):
        skinModel = self.skinModelSelector.currentNode()
        modelDisplay = skinModel.GetDisplayNode()
        modelDisplay.SetOpacity(newValue/1000.0)

  def obstacleModelOpacitySliderValueChanged(self,newValue):
    if(self.obstacleModelSelector.currentNode() != None):
        obstacleModel = self.obstacleModelSelector.currentNode()
        modelDisplay = obstacleModel.GetDisplayNode()
        modelDisplay.SetOpacity(newValue/1000.0)
        
  def allPathsOpacitySliderValueChanged(self,newValue):
    self.allPaths.SetOpacity(newValue/1000.0)

  def onSelect(self):
    if (self.targetSelector.currentNode() != None) and (self.obstacleModelSelector.currentNode() != None) and (self.skinModelSelector.currentNode() != None):
    	self.applyButton.enabled = True
    if (self.targetModelSelector.currentNode() != None) and (self.obstacleModelSelector.currentNode() != None) and (self.skinModelSelector.currentNode() != None):
      self.applyButton.enabled = True
      self.targetSwitch = 1

  def onCreatePointOnThePathButton(self):
    entryPointsNode = self.entryPointsSelector.currentNode()

    n = entryPointsNode.AddFiducial(self.virtualMarkerPosition[0], self.virtualMarkerPosition[1], self.virtualMarkerPosition[2])
    entryPointsNode.SetNthFiducialLabel(n, "FiducialTest")
    entryPointsNode.SetNthFiducialVisibility(n,0)

    self.plannedEntryPointModel, droppedMarker, droppedMarkerTransform = SphereModel().make(self.VISIBLE, self.red, "plannedEntryPoint")
    SphereModel().drop(self.virtualMarkerPosition[0], self.virtualMarkerPosition[1], self.virtualMarkerPosition[2], droppedMarkerTransform)

  def onCheckAllPaths(self):
    if self.allPathsCheckBox.checked == True:
      self.allPaths.SetVisibility(self.ON)
      self.allPathsOpacitySlider.enabled = True
    else:
      self.allPaths.SetVisibility(self.OFF)
      self.allPathsOpacitySlider.enabled = False

  def onCheckTheLongestPath(self):
    print(self.maximumPoint-1)
    if self.maximumLengthPathCheckBox.checked == True:
      self.theLongestPath.SetVisibility(self.ON)
      self.theLongestPathPointMarker.SetVisibility(self.ON)
    else:
      self.theLongestPath.SetVisibility(self.OFF)       
      self.theLongestPathPointMarker.SetVisibility(self.OFF)    

  def onCheckTheShortestPath(self):
    print(self.minimumPoint-1)
    if self.minimumLengthPathCheckBox.checked == True:
      self.theShortestPath.SetVisibility(self.ON)
      self.theShortestPathPointMarker.SetVisibility(self.ON)
    else:
      self.theShortestPath.SetVisibility(self.OFF)       
      self.theShortestPathPointMarker.SetVisibility(self.OFF)    

  def onCheckPathCandidate(self):
    #print(self.pointMarkerTransform)
    if self.pathCandidateCheckBox.checked == True:
      self.singlePath.SetVisibility(self.ON)
      self.pointMarker.SetVisibility(self.ON)
      self.virtualPath2.SetVisibility(self.ON)
      self.virtualMarker.SetVisibility(self.ON) 
      self.pointSlider.enabled = True
      self.pathSlider.enabled = True
      self.createPointOnThePathButton.enabled = True
    else:
      self.singlePath.SetVisibility(self.OFF)       
      self.pointMarker.SetVisibility(self.OFF)    
      self.virtualPath2.SetVisibility(self.OFF)       
      self.virtualMarker.SetVisibility(self.OFF)
      self.pointSlider.enabled = False
      self.pathSlider.enabled = False
      self.createPointOnThePathButton.enabled = False
     
  def onApplyButton(self):
    #self.pushApplyButton = 1
    logic = PercutaneousPathDesignerLogic()
    print("onApplyButton() is called ")
    targetPoint = self.targetSelector.currentNode()
    targetModel = self.targetModelSelector.currentNode()
    obstacleModel = self.obstacleModelSelector.currentNode()
    skinModel = self.skinModelSelector.currentNode()

    # make all paths candidates
    self.pathReceived, self.nPathReceived, self.apReceived, self.minimumPoint, self.minimumDistance, self.maximumPoint, self.maximumDistance = logic.makePaths(targetPoint, targetModel, 0, obstacleModel, skinModel)
    # display all paths model
    self.modelReceived, pReceived, self.allPaths = NeedlePathModel().make(self.pathReceived, self.nPathReceived, self.VISIBLE, self.yellow, "candidatePaths", self.allLines)

    # display sphere model
    self.selectedPathTipModel, self.pointMarker, self.pointMarkerTransform = SphereModel().make(self.INVISIBLE, self.red, "selectedPathTip")
    self.markerPosition = SphereModel().move(self.apReceived, self.pathSliderValue, self.pointSliderValue, self.pointMarkerTransform)
    self.extendedPathTipModel, self.virtualMarker, self.virtualMarkerTransform = SphereModel().make(self.INVISIBLE, self.red, "extendedPathTip")
    self.virtualMarkerPosition = SphereModel().move(self.apReceived, self.pathSliderValue, self.pointSliderValue, self.virtualMarkerTransform)

    # make single path candidate
    self.onePath, self.onePathDistance = logic.makeSinglePath(self.apReceived, self.pathSliderValue)

    # display single path candidate model
    self.singlePathModel, self.singleP, self.singlePath = NeedlePathModel().make(self.onePath, 2, self.INVISIBLE, self.red, "selectedPath", self.singleLine)
    self.virtualPath, self.virtualPathDistance = logic.makeVirtualPath(self.apReceived, self.pathSliderValue, self.virtualMarkerPosition)
    self.virtualPathModel, self.virtualP, self.virtualPath2 = NeedlePathModel().make(self.virtualPath, 2, self.INVISIBLE, self.red, "extendedPath", self.extendedLine)
    self.lengthOfPathSpinBox.value = self.virtualPathDistance
  
    # make the longest path
    self.theLongestPathTmp, self.distanceDummy = logic.makeSinglePath(self.apReceived, self.maximumPoint-1)
    # display the longest path
    self.theLongestPathModel, self.theLongestPathP, self.theLongestPath = NeedlePathModel().make(self.theLongestPathTmp, 2, self.INVISIBLE, self.green, "longestPath", self.longestLine)
    # make the point marker on the longest path 
    self.longestPathTipModel, self.theLongestPathPointMarker, self.theLongestPathPointMarkerTransform = SphereModel().make(self.INVISIBLE, self.green, "longestPathTip")
    self.theLongestPathPointMarkerPosition = SphereModel().move(self.apReceived, self.maximumPoint-1, 0, self.theLongestPathPointMarkerTransform)

    # make the shortest path
    self.theShortestPathTmp, self.distanceDummy = logic.makeSinglePath(self.apReceived, self.minimumPoint-1)
    # display the shortest path
    self.theShortestPathModel, self.theShortestPathP, self.theShortestPath = NeedlePathModel().make(self.theShortestPathTmp, 2, self.INVISIBLE, self.blue,"shortestPath", self.shortestLine)
    # make the point marker on the shortest path 
    self.shortestPathTipModel, self.theShortestPathPointMarker, self.theShortestPathPointMarkerTransform = SphereModel().make(self.INVISIBLE, self.blue, "shortestPathTip")
    self.theShortestPathPointMarkerPosition = SphereModel().move(self.apReceived, self.minimumPoint-1, 0, self.theShortestPathPointMarkerTransform)

    # update outcomes
    self.numbersOfAllpathsSpinBox.value = self.nPathReceived
    self.pathSlider.maximum = self.nPathReceived-1
    self.allPathsCheckBox.checked = True
    self.allPathsCheckBox.enabled = True
    self.pathCandidateCheckBox.enabled = True
    self.outcomesList.collapsed = False
    self.allPathsOpacitySlider.enabled = True
    self.deleteModelsButton.enabled = True

    self.allPaths.SetOpacity(10.0/1000.0)

    self.maximumLengthSpinBox.value = self.maximumDistance
    self.maximumLengthPathSpinBox.value = self.maximumPoint-1
    self.minimumLengthSpinBox.value = self.minimumDistance
    self.minimumLengthPathSpinBox.value = self.minimumPoint-1

  def onReload(self,moduleName="PercutaneousPathDesigner"):
    """Generic reload method for any scripted module.
    ModuleWizard will subsitute correct default moduleName.
    """
    import imp, sys, os, slicer

    widgetName = moduleName + "Widget"

    # reload the source code
    # - set source file path
    # - load the module to the global space
    filePath = eval('slicer.modules.%s.path' % moduleName.lower())
    p = os.path.dirname(filePath)
    if not sys.path.__contains__(p):
      sys.path.insert(0,p)
    fp = open(filePath, "r")
    globals()[moduleName] = imp.load_module(
        moduleName, fp, filePath, ('.py', 'r', imp.PY_SOURCE))
    fp.close()

    # rebuild the widget
    # - find and hide the existing widget
    # - create a new widget in the existing parent
    parent = slicer.util.findChildren(name='%s Reload' % moduleName)[0].parent().parent()
    for child in parent.children():
      try:
        child.hide()
      except AttributeError:
        pass
    # Remove spacer items
    item = parent.layout().itemAt(0)
    while item:
      parent.layout().removeItem(item)
      item = parent.layout().itemAt(0)

    # delete the old widget instance
    if hasattr(globals()['slicer'].modules, widgetName):
      getattr(globals()['slicer'].modules, widgetName).cleanup()

    # create new widget inside existing parent
    globals()[widgetName.lower()] = eval(
        'globals()["%s"].%s(parent)' % (moduleName, widgetName))
    globals()[widgetName.lower()].setup()
    setattr(globals()['slicer'].modules, widgetName, globals()[widgetName.lower()])

  def onReloadAndTest(self,moduleName="PercutaneousPathDesigner"):
    try:
      self.onReload()
      evalString = 'globals()["%s"].%sTest()' % (moduleName, moduleName)
      tester = eval(evalString)
      tester.runTest()
    except Exception, e:
      import traceback
      traceback.print_exc()
      qt.QMessageBox.warning(slicer.util.mainWindow(), 
          "Reload and Test", 'Exception!\n\n' + str(e) + "\n\nSee Python Console for Stack Trace")

  def onDeleteModelsButton(self):
    if self.deleteModelsButton.enabled == True:
        # reset all status
        self.deleteModelsButton.enabled = False
        self.allPathsCheckBox.checked = True
        self.allPathsCheckBox.enabled = False
        self.numbersOfAllpathsSpinBox.enabled = False
        self.maximumLengthSpinBox.enabled = False
        self.maximumLengthPathSpinBox.enabled = False
        self.minimumLengthSpinBox.enabled = False
        self.minimumLengthPathSpinBox.enabled = False
        self.pathCandidateCheckBox.checked = False
        self.pathCandidateCheckBox.enabled = False
        self.pathSlider.enabled = False
        self.pointSlider.enabled = False
        self.lengthOfPathSpinBox.enabled = False
        self.createPointOnThePathButton.enabled = False
        self.maximumLengthPathCheckBox.checked = False
        self.maximumLengthPathCheckBox.enabled = False
        self.minimumLengthPathCheckBox.checked = False
        self.minimumLengthPathCheckBox.enabled = False
        self.allPathsOpacitySlider.enabled = False
        # delete all models
        logic = PercutaneousPathDesignerLogic()
        logic.removeModel(self.modelReceived)
        logic.removeModel(self.singlePathModel)
        logic.removeModel(self.virtualPathModel)
        logic.removeModel(self.theLongestPathModel)
        logic.removeModel(self.theShortestPathModel)
        #
        logic.removeModel(self.selectedPathTipModel)
        logic.removeModel(self.extendedPathTipModel)
        logic.removeModel(self.longestPathTipModel)
        logic.removeModel(self.shortestPathTipModel)

#
# PercutaneousPathDesignerLogic
#

class PercutaneousPathDesignerLogic:
  """This class should implement all the actual 
  computation done by your module.  The interface 
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget
  """
  def __init__(self):
    pass

  def hasImageData(self,volumeNode):
    """This is a dummy logic method that 
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      print('no volume node')
      return False
    if volumeNode.GetImageData() == None:
      print('no image data')
      return False
    return True

  def delayDisplay(self,message,msec=1000):
    #
    # logic version of delay display
    #
    print(message)
    self.info = qt.QDialog()
    self.infoLayout = qt.QVBoxLayout()
    self.info.setLayout(self.infoLayout)
    self.label = qt.QLabel(message,self.info)
    self.infoLayout.addWidget(self.label)
    qt.QTimer.singleShot(msec, self.info.close)
    self.info.exec_()

  def removeModel(self, model):
    scene = slicer.mrmlScene
    scene.RemoveNode(model)    

  def makeSinglePath(self, p, pointNumber):  
    import numpy 

    tipPoint = numpy.zeros([2,3])

    targetP = [p[pointNumber*2][0], p[pointNumber*2][1], p[pointNumber*2][2]]
    skinP = [p[pointNumber*2+1][0], p[pointNumber*2+1][1], p[pointNumber*2+1][2]]

    tipPoint[0] = targetP
    tipPoint[1] = skinP

    onePath = [targetP]
    onePath.append(skinP)

    distance = numpy.sqrt(numpy.power(p[pointNumber*2]-p[pointNumber*2+1],2).sum())

    self.tmpSwitch = 1      

    return (onePath, distance)

  def makeVirtualPath(self, p, pointNumber, virtualPosition):
    import numpy

    tipPoint = numpy.zeros([2,3])

    targetP = [virtualPosition[0], virtualPosition[1], virtualPosition[2]]
    skinP = [p[pointNumber*2+1][0], p[pointNumber*2+1][1], p[pointNumber*2+1][2]]

    tipPoint[0] = targetP
    tipPoint[1] = skinP

    onePath = [targetP]
    onePath.append(skinP)

    distance = numpy.sqrt(numpy.power(p[pointNumber*2+1]-virtualPosition,2).sum())

    return (onePath, distance)

  def makePaths(self, targetPointNode, targetModelNode, targetSwitch, obstacleModelNode, skinModelNode):
    """
    Run the actual algorithm
    """
    print ('makePaths() is called')

    import numpy
    
    # The variable nPoints represents numbers of polygons for skin model
    poly = skinModelNode.GetPolyData()
    polyDataNormals = vtk.vtkPolyDataNormals()
    polyDataNormals.SetInput(poly)
    polyDataNormals.Update()
    polyData = polyDataNormals.GetOutput()
    nPoints = polyData.GetNumberOfPoints()
    nPoints2 = nPoints*2

    # The variable nPointsT represents numbers of polygons for target model
    if targetSwitch == 1:
      polyT = targetModelNode.GetPolyData()
      polyTDataNormals = vtk.vtkPolyDataNormals()
      polyTDataNormals.SetInput(polyT)
      polyTDataNormals.Update()
      polyTData = polyTDataNormals.GetOutput()
      nPointsT = polyTData.GetNumberOfPoints()
      nPointsT2 = nPointsT*2
      p2 = [0.0, 0.0, 0.0]
    else:
      nPointsT = 1
      nPointsT2 = nPointsT*2
      tPoint = targetPointNode.GetMarkupPointVector(0, 0)
      p2 = [tPoint[0], tPoint[1], tPoint[2]]

    # The variable approachablePoints represents number of approachable polygons on the skin model 
    approachablePoints = 0 #nPointsT*nPoints

    p1=[0.0, 0.0, 0.0]
    
    tolerance = 0.001
    t = vtk.mutable(0.0)
    x = [0.0, 0.0, 0.0] # The coordinate of the intersection 
    pcoords = [0.0, 0.0, 0.0]
    subId = vtk.mutable(0)

    bspTree = vtk.vtkModifiedBSPTree()
    bspTree.SetDataSet(obstacleModelNode.GetPolyData())
    bspTree.BuildLocator()

    maximumDistance = 0.0
    minimumDistance = 1000.0 
    distance = 0.0
    maximumPoint = 0
    minimumPoint = 0

    # Create an array for needle passing points 
    self.p = numpy.zeros([nPointsT*nPoints2,3])

    for indexT in range(0, nPointsT):

      p2 = [tPoint[0], tPoint[1], tPoint[2]]

      for index in range(0, nPoints):
        polyData.GetPoint(index, p1)
        iD = bspTree.IntersectWithLine(p1, p2, tolerance, t, x, pcoords, subId)
  
        if iD == 0:
          coord1 = [p2[0],p2[1],p2[2]]
          self.p[approachablePoints*2] = coord1        
          coord2 = [p1[0],p1[1],p1[2]]
          self.p[approachablePoints*2+1] = coord2
          approachablePoints = approachablePoints + 1 

          #
          # Create length calculation algorithm
          # 
          coord1Array = numpy.array(coord1)          
          coord2Array = numpy.array(coord2)

          distance = numpy.sqrt(numpy.power(coord1Array-coord2Array,2).sum())
          if distance >= maximumDistance:
            maximumDistance = distance
            maximumPoint = approachablePoints
          if distance <= minimumDistance:
            minimumDistance = distance
            minimumPoint = approachablePoints

    # Create the list for needle passing points to draw virtual ray 
    self.path = [self.p[0]]
    #for index2 in range(1, nPointsT*nPoints2):
    for index in range(1, approachablePoints*2):
      self.path.append(self.p[index])  
  
    # Create an array for all approachable points 
    pReceived = numpy.zeros([approachablePoints,3])

    return (self.path, approachablePoints, self.p, minimumPoint, minimumDistance, maximumPoint, maximumDistance)

class SphereModel:

  def __init__(self):
    pass

  def make(self, visibilityParam, color, modelName):
    scene = slicer.mrmlScene

    sphere = vtk.vtkSphereSource()
    sphere.SetRadius(0.5)
    sphere.SetPhiResolution(100)
    sphere.SetThetaResolution(100)
    sphere.Update()

    sphere1 = vtk.vtkSphereSource()
    sphere1.SetRadius(2.5)
    sphere1.SetPhiResolution(100)
    sphere1.SetThetaResolution(100)
    sphere1.SetCenter(20,20,20)
    sphere1.Update()

    # Create model node
    sphereCursor = slicer.vtkMRMLModelNode()
    sphereCursor.SetScene(scene)
    sphereCursor.SetName(scene.GenerateUniqueName(modelName))
    sphereCursor.SetAndObservePolyData(sphere.GetOutput())

    # Create display node
    cursorModelDisplay = slicer.vtkMRMLModelDisplayNode()
    cursorModelDisplay.SetColor(color[0], color[1], color[2])
    cursorModelDisplay.SetOpacity(0.3)    
    cursorModelDisplay.SetScene(scene)
    cursorModelDisplay.SetVisibility(visibilityParam)
    cursorModelDisplay.SetSliceIntersectionVisibility(True) # Show in slice view
  
    scene.AddNode(cursorModelDisplay)
    sphereCursor.SetAndObserveDisplayNodeID(cursorModelDisplay.GetID())

    # Add to scene
    cursorModelDisplay.SetInputPolyData(sphere.GetOutput())
    scene.AddNode(sphereCursor)

    # Create transform node
    transform = slicer.vtkMRMLLinearTransformNode()
    transformName = modelName + "Transform"
    transform.SetName(scene.GenerateUniqueName(transformName))
    scene.AddNode(transform)
    sphereCursor.SetAndObserveTransformNodeID(transform.GetID())

    return (sphereCursor, cursorModelDisplay, transform)

  def move(self, p, pointNumber, pointSliderValue, transform):

    r = p[pointNumber*2+1][0]
    a = p[pointNumber*2+1][1]
    s = p[pointNumber*2+1][2]
    
    targetR = p[pointNumber*2][0]
    targetA = p[pointNumber*2][1]
    targetS = p[pointNumber*2][2]
    
    dirVectorR = r - targetR
    dirVectorA = a - targetA
    dirVectorS = s - targetS
    
    movedR = r + pointSliderValue*0.001*dirVectorR
    movedA = a + pointSliderValue*0.001*dirVectorA
    movedS = s + pointSliderValue*0.001*dirVectorS
    
    coordinate = transform.GetMatrixTransformToParent()
    coordinate.SetElement(0, 3, movedR)
    coordinate.SetElement(1, 3, movedA)
    coordinate.SetElement(2, 3, movedS)

    movedRAS = [movedR, movedA, movedS]

    return movedRAS

  def drop(self, r, a, s, transform):

    coordinate = transform.GetMatrixTransformToParent()
    coordinate.SetElement(0, 3, r)
    coordinate.SetElement(1, 3, a)
    coordinate.SetElement(2, 3, s)

# NeedlePathModel class is based on EndoscopyPathModel class for Endoscopy module
class NeedlePathModel:
  """Create a vtkPolyData for a polyline:
       - Add one point per path point.
       - Add a single polyline
  """
  def __init__(self):
    pass

  def modify(self, path, approachablePoints, visibilityParam, color, modelName, polyData):
    import numpy

    # Create an array for all approachable points 
    p = numpy.zeros([approachablePoints*2,3])
    p1 = [0.0, 0.0, 0.0]

    scene = slicer.mrmlScene
    
    points = vtk.vtkPoints()
    polyData.SetPoints(points)

    lines = vtk.vtkCellArray()
    polyData.SetLines(lines)
    linesIDArray = lines.GetData()
    linesIDArray.Reset()
    linesIDArray.InsertNextTuple1(0)

    polygons = vtk.vtkCellArray()
    polyData.SetPolys( polygons )
    idArray = polygons.GetData()
    idArray.Reset()
    idArray.InsertNextTuple1(0)

    if approachablePoints != 0:

      for point in path:
        pointIndex = points.InsertNextPoint(*point)
        linesIDArray.InsertNextTuple1(pointIndex)
        linesIDArray.SetTuple1( 0, linesIDArray.GetNumberOfTuples() - 1 )
        lines.SetNumberOfCells(1)

        # Save all approachable points 
        p1[0] = linesIDArray.GetTuple1(1)
        p1[1] = linesIDArray.GetTuple1(2)
        p1[2] = linesIDArray.GetTuple1(3)

        coord = [p1[0], p1[1], p1[2]]
        p[pointIndex] = coord

    polyData.Update()

  def make(self, path, approachablePoints, visibilityParam, color, modelName, polyData):

    import numpy

    # Create an array for all approachable points 
    p = numpy.zeros([approachablePoints*2,3])
    p1 = [0.0, 0.0, 0.0]

    scene = slicer.mrmlScene
    
    points = vtk.vtkPoints()
    polyData.SetPoints(points)

    lines = vtk.vtkCellArray()
    polyData.SetLines(lines)
    linesIDArray = lines.GetData()
    linesIDArray.Reset()
    linesIDArray.InsertNextTuple1(0)

    polygons = vtk.vtkCellArray()
    polyData.SetPolys( polygons )
    idArray = polygons.GetData()
    idArray.Reset()
    idArray.InsertNextTuple1(0)

    if approachablePoints != 0:

      for point in path:
        pointIndex = points.InsertNextPoint(*point)
        linesIDArray.InsertNextTuple1(pointIndex)
        linesIDArray.SetTuple1( 0, linesIDArray.GetNumberOfTuples() - 1 )
        lines.SetNumberOfCells(1)

        # Save all approachable points 
        p1[0] = linesIDArray.GetTuple1(1)
        p1[1] = linesIDArray.GetTuple1(2)
        p1[2] = linesIDArray.GetTuple1(3)

        coord = [p1[0], p1[1], p1[2]]
        p[pointIndex] = coord

    # Create model node
    model = slicer.vtkMRMLModelNode()
    model.SetScene(scene)
    model.SetName(scene.GenerateUniqueName(modelName))
    model.SetAndObservePolyData(polyData)

    # Create display node
    modelDisplay = slicer.vtkMRMLModelDisplayNode()
    modelDisplay.SetColor(color[0], color[1], color[2])
    modelDisplay.SetScene(scene)
    modelDisplay.SetVisibility(visibilityParam)
    modelDisplay.SetSliceIntersectionVisibility(True) # Show in slice view
    scene.AddNode(modelDisplay)
    model.SetAndObserveDisplayNodeID(modelDisplay.GetID())

    # Add to scene
    modelDisplay.SetInputPolyData(model.GetPolyData())
    scene.AddNode(model)

    return (model, p, modelDisplay)    

class PercutaneousPathDesignerTest(unittest.TestCase):
  """
  This is the test case for your scripted module.
  """

  def delayDisplay(self,message,msec=1000):
    """This utility method displays a small dialog and waits.
    This does two things: 1) it lets the event loop catch up
    to the state of the test so that rendering and widget updates
    have all taken place before the test continues and 2) it
    shows the user/developer/tester the state of the test
    so that we'll know when it breaks.
    """
    print(message)
    self.info = qt.QDialog()
    self.infoLayout = qt.QVBoxLayout()
    self.info.setLayout(self.infoLayout)
    self.label = qt.QLabel(message,self.info)
    self.infoLayout.addWidget(self.label)
    qt.QTimer.singleShot(msec, self.info.close)
    self.info.exec_()

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_PercutaneousPathDesigner1()

  def test_PercutaneousPathDesigner1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests sould exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import urllib
    downloads = (
        ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
        )

    for url,name,loader in downloads:
      filePath = slicer.app.temporaryPath + '/' + name
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        print('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader:
        print('Loading %s...\n' % (name,))
        loader(filePath)
    self.delayDisplay('Finished with download and loading\n')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = PercutaneousPathDesignerLogic()
    self.assertTrue( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
