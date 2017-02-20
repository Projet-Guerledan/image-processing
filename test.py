#!/usr/bin/env python2
# 	Main method
# 	Test
#
#	
import cv2
import sys
#import pywt
import TestPlots as tp

def getOptionsWavelet(family):
	wavelist = pywt.wavelist(family)
	n = 0
	optionsWavelet = dict()
	for i in wavelist:
		optionsWavelet[n] = [i,i]
		n = n+1
	return optionsWavelet

# 1) images directory and input image file name
inputImage = 'test1.jpg'
imagePath = '/home/evbernardes/Dropbox/ENSTA/Projet_Guerleden/'

# 2) creation of plots for each step
# plot1 = plot of the first phase of image processing
# plot2 = plot of the second phase of image processing
# plot3 = plot of wavelet transform after all image processing stages
plot1 = tp.MorphPlot(input = imagePath+inputImage)
plot2 = tp.MorphPlot()
plot3 = tp.WavPlot()

# 3) set order and initialise plots
tp.setOrder([plot1,plot2,plot3],imagePath = imagePath, output = 'output')
plot1.init_image('step1')
plot2.init_image('step2')
plot3.init_image('wavelet transform')

# 4) show all plots
tp.showNow()
