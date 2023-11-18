import numpy as np
try:
	import cv2
except Exception as e:
	print("OpenCV not installed")




if __name__ == "__main__":
	print("-"*50)
	print("testing camera setup")
	
	cap = cv2.VideoCapture(3)


	while(True):
		#Capture frame by frame
		ret, frame = cap.read()

		#Display the frame
		cv2.imshow('frame', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()


