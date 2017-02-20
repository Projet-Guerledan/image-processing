#
# Create new switch for OpenCV trackbars
#
# Arguments:
#	- switch: STRING to be written in trackbar for options
#	- options: DICT either with kernel type or transform options
#
# Example:
# 	If the given argument is the default_kernel dictionary, the returned
#	string will be:
#	0: Round
#	1: Rect
#
import numpy as np
def createSwitch(options):
	n = 0
	switch = ''
	for i in options.values():
		switch = switch + str(n)+' : '+i[0]+'\n'
		n += 1
	return switch
#
#   toPyWt and toOpCv are functions implementing a simple compability layer
#   between pywavelets and OpenCV
#
#   TODO: better doc
def toPyWt(imArray):
	imArray =  np.float32(imArray)
	imArray /= 255;
	return imArray

def toOpCv(coeffs):
    #~ coeffs=list(coeffs)
    #~ coeffs[0] *= 0;
    coeffs *= 255;
    #~ coeffs =  np.uint8(coeffs)
    return coeffs

#
#   Creation du plot de l'analyse multiresolution
#
#   TODO: better doc
def dwtPlot(coeffs):

	def reshape2(cA,cHVD):
		cH,cV,cD = cHVD
		#cA,(cH,cV,cD) = inTest

		y = min([cA.shape[0],cH.shape[0]])
		x = min([cA.shape[1],cH.shape[1]])
		shape = (x,y)

		def cut(array,shape):
			array = array[:shape[0]]
			array = array.transpose()
			array = array[:shape[1]]
			return array.transpose()

		cA = cut(cA,cH.shape)
		cH = cut(cH,cA.shape)
		cV = cut(cV,cA.shape)
		cD = cut(cD,cA.shape)

		return cA,cH,cV,cD
    #
	# def reshape(cA,coeffs):
	# 	cH,cV,cD = coeffs
	# 	# cA,(cH,cV,cD) = inTest
    #
	# 	def cut(array,shape):
	# 		array = array[:shape[0]]
	# 		array = array.transpose()
	# 		array = array[:shape[1]]
	# 		return array.transpose()
    #
	# 	if cA.shape < cH.shape:
	# 		cH = cut(cH,cA.shape)
	# 		cV = cut(cV,cA.shape)
	# 		cD = cut(cD,cA.shape)
	# 	else:
	# 		cA = cut(cA,cH.shape)
    #
	# 	return cA,cH,cV,cD

	def getNext(plot,coeffs):

		cA,cH,cV,cD = reshape2(plot,coeffs)
		cAH = np.hstack([cA,cH])
		cVD = np.hstack([cV,cD])
		cAHVD = np.vstack([cAH,cVD])
		return cAHVD

	plot = coeffs[0]
	for i in range(0,len(coeffs)-1):
		plot = getNext(plot,coeffs[i+1])
	return plot
