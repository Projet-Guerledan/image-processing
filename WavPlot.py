#
#	WavPlot class
#
#		This class simplifies testing of pywavelets wavelet transforms
#
# 	Arguments:
#	- input: [STRING] input file
#	- output: [STRING] output file
#	- *optionsWavelet: [DICT] wavelet types
#	- maxLevel: [INTEGER] max level of multiresolution analysis
#
#	* See default_wavelets for an example of how to declare
# 	these variables.
#
import cv2
import numpy as np
import argparse
import pywt
from Misc import *

default_wavelets = {
	0: ['Haar','haar'],
	1: ['Daubechies 2','db2']}

class WavPlot:

	def __init__(self,input='',output='',optionsWavelet=default_wavelets,maxLevel = 3,nextProcess = 0):

		self.inputImagePath = input
		self.outputImagePath = output
		self.maxLevel = maxLevel
		self.optionsWavelet = optionsWavelet
		self.nextProcess = nextProcess
		self.maxLevel = maxLevel

	#
	#	Initialise plot and first image
	#
	def init_image(self,winName):
		self.winName = winName

		# initialise switches
		self.switchWavelet = createSwitch(self.optionsWavelet)

		# initialise window and trackbars
		self.waveletType = self.optionsWavelet[0][1]
		cv2.namedWindow(self.winName)
		cv2.createTrackbar('levels',self.winName,0,self.maxLevel,self.update)
		if len(self.optionsWavelet) > 1:
			cv2.createTrackbar(self.switchWavelet,self.winName,0,len(self.optionsWavelet)-1,self.update)

		# load input image
		self.inputImage = toPyWt((cv2.imread(self.inputImagePath,0)))

		# initialise image
		self.levels = 0
		self.coefficients = pywt.wavedec2(self.inputImage, self.waveletType, level=self.levels)
		self.outputImage = dwtPlot(self.coefficients)
		if len(self.outputImagePath) != 0:
			cv2.imwrite(self.outputImagePath,self.outputImage)
		cv2.imshow(self.winName,self.outputImage)

	# 	Update methods called by OpenCV whenever the trackbars are set
	# 	to a new position
	def update(self,x):

		def updateImage(waveletType):
			self.levels = cv2.getTrackbarPos('levels',self.winName)
			coefficients = pywt.wavedec2(self.inputImage, waveletType, level=self.levels)
			self.outputImage = dwtPlot(coefficients)
			#self.outputImage = toOpCv(self.outputImage)
			cv2.imshow(self.winName,self.outputImage)

		def updateWaveletType(switchWavelet,optionsWavelet):
			s = cv2.getTrackbarPos(switchWavelet,self.winName)
			self.waveletType = optionsWavelet[s][1]

		# refresh input image and update
		self.inputImage = toPyWt(cv2.imread(self.inputImagePath,0))
		if len(self.optionsWavelet) > 1:
			updateWaveletType(self.switchWavelet,self.optionsWavelet)
		updateImage(self.waveletType)

		# save image to output file
		if len(self.outputImagePath) != 0:
			cv2.imwrite(self.outputImagePath,toOpCv(self.outputImage))

		# call update of next process (if it exists)
		if self.nextProcess != 0:
			self.nextProcess.update(0)
