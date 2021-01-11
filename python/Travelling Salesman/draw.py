import tkinter as tk
from tkinter import messagebox

data = [[0,13],[0,26],[0,27],[0,39],[2,0],[5,13],[5,19],[5,25],[5,31],[5,37],[5,43],[5,8],[8,0],[9,10],[10,10],[11,10],[12,10],[12,5],[15,13],[15,19],[15,25],[15,31],[15,37],[15,43],[15,8],[18,11],[18,13],[18,15],[18,17],[18,19],[18,21],[18,23],[18,25],[18,27],[18,29],[18,31],[18,33],[18,35],[18,37],[18,39],[18,41],[18,42],[18,44],[18,45],[25,11],[25,15],[25,22],[25,23],[25,24],[25,26],[25,28],[25,29],[25,9],[28,16],[28,20],[28,28],[28,30],[28,34],[28,40],[28,43],[28,47],[32,26],[32,31],[33,15],[33,26],[33,29],[33,31],[34,15],[34,26],[34,29],[34,31],[34,38],[34,41],[34,5],[35,17],[35,31],[38,16],[38,20],[38,30],[38,34],[40,22],[41,23],[41,32],[41,34],[41,35],[41,36],[48,22],[48,27],[48,6],[51,45],[51,47],[56,25],[57,12],[57,25],[57,44],[61,45],[61,47],[63,6],[64,22],[71,11],[71,13],[71,16],[71,45],[71,47],[74,12],[74,16],[74,20],[74,24],[74,29],[74,35],[74,39],[74,6],[77,21],[78,10],[78,32],[78,35],[78,39],[79,10],[79,33],[79,37],[80,10],[80,41],[80,5],[81,17],[84,20],[84,24],[84,29],[84,34],[84,38],[84,6],[107,27]]


def line(a, b, c, d, color): #connects coords a,b and c,d with a line
	C.create_line(a, b, c, d, fill=color)

def highlight(coord, color, size):
	drawPoint(coord[0], coord[1], size, color)

def drawPoint(x, y, width, color):
	C.create_rectangle(x - width, y - width, x + width, y + width, outline=color)

def scalar(li, scale): #scales up or down coordinates 
	scaled = []
	for i in range(0, len(li)):
		scaled.append([li[i][0]*scale, li[i][1]*scale])
	return scaled

def drawPointsIn(li): #Plots all the point in the input. Input should be a list of tuples.
	for i in li:
		drawPoint(i[0], i[1], 2, 'white')

def flipVert(li): #flips points vertically
	maxY = max(li, key=lambda x: x[1])[1]
	output = []
	for i in li:
		output.append([i[0], maxY - i[1]])
	return output

def padding(li, pad):
		output = []
		for i in li:
			output.append([i[0] + pad, i[1] + pad])
		return output

def setup(li, scale):

	global top
	top = tk.Tk()
	maxX = max(li, key=lambda x: x[0])[0]
	maxY = max(li, key=lambda x: x[1])[1]
	leastX = min(li, key=lambda x: x[0])[0]
	leastY = min(li, key=lambda x: x[1])[1]

	width = scale*(maxX) + 30
	height = scale*(maxY) + 30

	global C
	C = tk.Canvas(top, bg = "black", width = width, height = height)

def render(li):
	drawPointsIn(li)
	C.pack()
	top.mainloop()

# setup(data, 4)
# print(C == 0)
# render(data)