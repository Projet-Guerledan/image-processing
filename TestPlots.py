import cv2
from WavPlot import WavPlot
from MorphPlot import MorphPlot

def setOrder(plotList,imagePath = '',output = 'outputImage',extension = 'png'):
	for i in range(0,len(plotList)-1):
		plotList[i].nextProcess = plotList[i+1]

		path = 'INTERMEDIARY_STEP_'+str(i)+'_'+str(i+1)+'.'+extension
		path = imagePath+path
		plotList[i].outputImagePath = path
		plotList[i+1].inputImagePath = path
		#print(path)

	lastPath = plotList[-1].outputImagePath+output+'.'+extension
	#print(lastPath)
	plotList[-1].outputImagePath = lastPath

def showNow():
	while(1):
		k = cv2.waitKey(0)
		if k&255==27 or k==-1:    # Esc key to stop
			cv2.destroyAllWindows()
			break
		else:
			continue
