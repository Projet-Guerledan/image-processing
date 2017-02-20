#
#	MorphPlot class
#
#		This class simplifies testing of OpenCV morphological operations
#	using the cv2.morphologyEx function
#
# Arguments:
#	- input: [STRING] input file
#	- output: [STRING] output file
#	- *optionsKernel: [DICT] kernel types
#	- *optionsTransform: [DICT] morphological transform operations
#	- kernelMaxSize: [INTEGER] size of transform kernel
#	- **nextProcess: reference to next process
#
#	* See default_transforms and defaul_kernels for an example of how to declare
# 	these variables.
#
#	** nextProcess is a reference to the next step. Should be defined by
#	setOrder function in TestPlots.py
#
import cv2
import numpy as np
import argparse
from Misc import *

# Default options for transforms and kernel types
default_transforms = {
	0: ['Erode',cv2.MORPH_ERODE],
	1: ['Dilate',cv2.MORPH_DILATE],
	2: ['Open',cv2.MORPH_OPEN],
	3: ['Close',cv2.MORPH_CLOSE]}
	#4: ['Top-hat',cv2.MORPH_TOPHAT]}

default_kernels = {
	0: ['Round',cv2.MORPH_ELLIPSE],
	1: ['Rect',cv2.MORPH_RECT]}

class MorphPlot:
	#
	#	Class constructor
	#
	def __init__(self,input='',output='',optionsKernel=default_kernels,optionsTransform=default_transforms,kernelMaxSize = 30,nextProcess = 0):
		self.inputImagePath = input
		self.outputImagePath = output
		self.optionsKernel = optionsKernel
		self.optionsTransform = optionsTransform
		self.switchKernel = createSwitch(self.optionsKernel)
		self.switchTransform = createSwitch(self.optionsTransform)
		self.nextProcess = nextProcess
		self.kernelMaxSize = kernelMaxSize

		# initial kernel and transform
		self.kernelType = self.optionsKernel[0][1]
		self.kernel = cv2.getStructuringElement(self.kernelType,(1,1))
		self.transformType = self.optionsTransform[0][1]

	#
	#	Initialise plot and first image
	#
	def init_image(self,winName):
		self.winName = winName

		# create window and trackbars
		cv2.namedWindow(self.winName)

		self.inputImage = cv2.imread(self.inputImagePath,0)
		cv2.createTrackbar('kernel radius',self.winName,0,self.kernelMaxSize,self.update)
		if len(self.optionsKernel) > 1:
			cv2.createTrackbar(self.switchKernel,self.winName,0,len(self.optionsKernel)-1,self.update)
		if len(self.optionsTransform) > 1:
			cv2.createTrackbar(self.switchTransform,self.winName,0,len(self.optionsTransform)-1,self.update)

		# calculate first transform
		self.outputImage = cv2.morphologyEx(self.inputImage, self.transformType, self.kernel)

		if len(self.outputImagePath) != 0:
			cv2.imwrite(self.outputImagePath,self.outputImage)

		cv2.imshow(self.winName,self.outputImage)


	# 	Update methods called by OpenCV whenever the trackbars are set
	# 	to a new position
	def update(self,x):
		# create and show new image
		def updateImage(kernelType,transformType):
			radius = 1 + cv2.getTrackbarPos('kernel radius',self.winName)
			self.kernel = cv2.getStructuringElement(kernelType,(radius,radius))
			self.outputImage = cv2.morphologyEx(self.inputImage, transformType, self.kernel)
			cv2.imshow(self.winName,self.outputImage)

		# select new kernel
		def updateKernelType(switchKernel,optionsKernel):
			s = cv2.getTrackbarPos(switchKernel,self.winName)
			self.kernelType = optionsKernel[s][1]

		# select new transform type
		def updateTransformType(switchTransform,optionsTransform):
			s = cv2.getTrackbarPos(switchTransform,self.winName)
			self.transformType = optionsTransform[s][1]

		# refresh input image and update
		self.inputImage = cv2.imread(self.inputImagePath,0)
		if len(self.optionsKernel) > 1:
			updateKernelType(self.switchKernel,self.optionsKernel)
		if len(self.optionsTransform) > 1:
			updateTransformType(self.switchTransform,self.optionsTransform)
		updateImage(self.kernelType,self.transformType)

		# save image to output file
		if len(self.outputImagePath) != 0:
			cv2.imwrite(self.outputImagePath,self.outputImage)

		# call update of next process (if it exists)
		if self.nextProcess != 0:
			self.nextProcess.update(0)
