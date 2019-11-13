from tkinter.filedialog import askopenfilename			#this should allow user inserted wav/mp3 files for play
from graphics import *							      	#graphics									
import simpleaudio as sa
from win32api import GetSystemMetrics
#first window to start program and request inputs
def main():

	win = GraphWin("QUestions", 500, 200)

	#text object
	bpmText = Text(Point(100, 20), 15)
	bpmText.setText("Bpm")
	bpmText.draw(win)

	nonText = Text(Point(250, 20), 15)
	nonText.setText("Notes Wanted")
	nonText.draw(win)

	#entry object
	bpmEntry = Entry(Point(100,40), 15)
	bpmEntry.setFill("white")
	bpmEntry.setText("1")
	bpmEntry.draw(win)

	numOfNotes = Entry(Point(250,40), 15)
	numOfNotes.setFill("white")
	numOfNotes.setText("1")
	numOfNotes.draw(win)

	# Add button object
	buttonGenText = Text(Point(400,30), "Generate")
	buttonGenText.setSize(15)

	buttonGen = Rectangle(Point(350, 20),Point(450, 40))
	buttonGen.setFill('white')
	buttonGen.setWidth(1)

	buttonGen.draw(win)
	buttonGenText.draw(win)

	#as long as window is open, allow multiple inputs from user
	while True:
		#wait for user input
		win.getMouse()

		#12 pitches seperated by spaces of 20 = x
		#notes = notes wanted seperated by 30's = y
		sysMetWid = GetSystemMetrics(0)
		width = 30*int(numOfNotes.getText())
		widthloop = 0
		height = GetSystemMetrics(1)//2

		if width > sysMetWid:
			widthloop = width//sysMetWid
			width = width%sysMetWid

		win.close()
		musicWin(width, widthloop, height, bpmEntry.getText(), sysMetWid)

def musicWin(width, widthloop, height, bpm, sysMetWid):

	mWin = GraphWin("MUSIC oi YEAH", width, (height*widthloop))
	#adds lines between music
	for i in range(widthloop):
		line = line(Point(0, height*i), Point(sysMetWid, height*i) )
		line.setWidth(10)
		line.draw(mWin)

	#adds grid to manage notes and the such
	#for i in range(widthloop+1):

	#	for i in range(width):


	while True:
		mWin.getMouse()

main()