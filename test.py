import numpy as np
import pandas as pd
import cv2

clicked = False
r = g = b = xpos = ypos = 0
img = cv2.imread("colours.jpg")
csv_columns=["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv("colours.csv", names=csv_columns, header=None)

font_colours = {
	"white": (255, 255, 255),
	"black": (0, 0, 0),
}

def recognize_color(R,G,B):
	minimum = 10000
	for i in range(len(csv)):
		d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
		if (d <= minimum):
			minimum = d
			cname = csv.loc[i, "color_name"]
	return cname

def mouse_click(event, x, y, flags, param):
	if event == cv2.EVENT_LBUTTONDOWN:
		print("Mouse clicked")
		global b, g, r, xpos, ypos, clicked
		clicked = True
		xpos = x
		ypos = y
		b,g,r = img[y,x]
		r = int(r) 
		g = int(g)
		b = int(b)

def add_text(img, text, colour):
	text_position = (50, 50)
	font_scale = 0.5
	thickness = 1
	cv2.putText(img, text, text_position, cv2.FONT_HERSHEY_COMPLEX, font_scale, colour, thickness, cv2.LINE_AA)

def main():
	global clicked
	main_window_name = "Color Recognition App"

	cv2.namedWindow(main_window_name)
	cv2.setMouseCallback(main_window_name, mouse_click)
	cv2.imshow(main_window_name, img)

	while (1):
		if (clicked):
			clicked=False
			#cv2.rectangle(img, startpoint, endpoint, color, thickness)-1 fills entire rectangle 
			cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1) #Creating text string to display( Color name and RGB values )
			text = recognize_color(r,g,b) + " R="+ str(r) +  " G="+ str(g) +  " B="+ str(b)
		
			#cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
			print(text)

			if (r + g + b >= 600):
				# For very light colours we will display text in black colour
				print("Add white text")
				add_text(img, text, font_colours["white"])
			else:
				# Otherwise, black text
				print("Add black text")
				add_text(img, text, font_colours["black"])
			
		#Break the loop when user hits "esc" key    
		if cv2.waitKey(20) & 0xFF ==27:
			break
	cv2.destroyAllWindows()

main()
