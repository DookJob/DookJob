from graphics import * #graphics
import os
import random													
from win32api import GetSystemMetrics
import simpleaudio as sa #playing audio
import pickle #saving variables as data stream

noteLong = 18 #this one cant be changes, im trying to make my code change to it though
screenX = GetSystemMetrics(0) #these only work on windows... i think
screenY = GetSystemMetrics(1)
IMAGEROOT = os.path.dirname(os.path.abspath(__file__)) #yay no manual input
MUSICROOT = IMAGEROOT + '/soundFiles/'
NOTEFILENAMES = ["bass.wav", "beep.wav", "cat.wav", "dog.wav", "doot.wav", "horn.wav", "piano.wav", "ting.wav", "ufo.wav"]#more convienant than making a bunch of if statements
COLOR_GRAY = color_rgb(128, 128, 128)
COLOR_GREEN = color_rgb(0, 255, 0)
note_file_names = ["bonk.wav", "bonk.wav"]

#its tha main what do you even want to know, idoit
def main():
	#variables
	wid, hei = screenX//2, screenY//2

	#window
	win = GraphWin("Notes", wid, hei)
	win.setBackground('white')
	win.master.iconbitmap(os.path.join(IMAGEROOT, 'note.ico'))

	while True:
		mainmenu(win)

		if win.isClosed():
			break
		else:
			time.sleep(0.25)
			gamestart(win)

#makes the main menu and its functions
def mainmenu(win):
	#get the width and height from current window opened
	wid, hei = win.width, win.height
	#title
	textTitle = Text(Point(wid/2, hei/3.5), "Notes")
	textTitle.setTextColor('black')
	textTitle.setSize(20)
	textTitle.setStyle('bold')
	textTitle.draw(win)

	#text for generate/play
	playText = Text(Point(wid/2, hei/2), "Play")
	playText.setTextColor('black')
	playText.setSize(20)
	playText.setStyle('bold')
	#box fot generate/play
	#height and width of button, this is to make writing and visualizing it easier
	bw, bh = 250, 50
	x0, y0 = wid / 2 - bw / 2, hei / 2 - bh / 2
	x1, y1 = wid / 2 + bw / 2, hei / 2 + bh / 2
	playBox = Rectangle(Point(x0, y0), Point(x1, y1))
	playBox.setOutline(COLOR_GREEN)	
	playBox.setFill(COLOR_GREEN)

	playBox.draw(win)
	playText.draw(win)

	#check for user input to be in box and to do it button actions
	#after this runs and finishes/breaks we should start game, escape wont trigger this because it closes window
	while True:
		pt = win.checkMouse()
		if pt:
			x = pt.getX()
			y = pt.getY()

			if x >= x0 and x <= x1 and y >= y0 and y <= y1:
				playBox.undraw()
				playText.undraw()
				textTitle.undraw()
				break

		#makes the escape key a universal close key for easy navigation
		key = win.checkKey()
		if key == 'Escape':
			win.close()
			break

#hub for main game controls and stuff
def gamestart(win):
	activeCircles = []
	#entry and text objects for bpm
	#get the width and height from current window opened
	wid, hei = win.width, win.height
	#do same thing for mp3/wav entry
	bpmEntry = Entry(Point(wid/5 ,hei/6*5.75), 4)
	bpmEntry.setText('120')
	bpmText = Text(Point(wid/5, hei/6*5.35), 'BPM (Max:240)')
	bpmText.setTextColor(COLOR_GRAY)
	bpmText.setSize(16)

	#play button
	bw, bh = 150, 25
	x0, y0 = wid / 2 - bw / 2, hei / 6*5.5 - bh / 2
	x1, y1 = wid / 2 + bw / 2, hei / 6*5.5 + bh / 2
	playMusicBox = Rectangle(Point(x0, y0), Point(x1, y1))
	playMusicBox.setOutline(COLOR_GREEN)	
	playMusicBox.setFill(COLOR_GREEN)
	#playbuttontext
	playMusicText = Text(Point(wid/2, hei / 6*5.5), "Play")
	playMusicText.setTextColor('black')
	playMusicText.setSize(14)
	playMusicText.setStyle('bold')

	#potentially import and export for button for biGrid
	#all buttons built the same
	bw = 50
	x2, y2 = wid / 1.5 - bw / 2, hei / 6*5.5 - bh / 2
	x3, y3 = wid / 1.5 + bw / 2, hei / 6*5.5 + bh / 2
	exportSheetButtonBox = Rectangle(Point(x2, y2), Point(x3, y3))
	exportSheetButtonBox.setOutline(COLOR_GREEN)	
	exportSheetButtonBox.setFill(COLOR_GREEN)
	x4, y4 = wid / 1.3 - bw / 2, hei / 6*5.5 - bh / 2
	x5, y5 = wid / 1.3 + bw / 2, hei / 6*5.5 + bh / 2
	importSheetButtonBox = Rectangle(Point(x4, y4), Point(x5, y5))
	importSheetButtonBox.setOutline('red')	
	importSheetButtonBox.setFill('red')
	exportSheetText = Text(Point(wid/1.5, hei / 6*5.5), "Save")
	importSheetText = Text(Point(wid/1.3, hei / 6*5.5), "Load")

	#draw objects
	bpmEntry.draw(win)
	bpmText.draw(win)
	playMusicBox.draw(win)
	playMusicText.draw(win)
	exportSheetButtonBox.draw(win)
	importSheetButtonBox.draw(win)
	exportSheetText.draw(win)
	importSheetText.draw(win)

	#draws grid onto win
	#assigns biGrid
	xLine, yLine, biGrid = drawGrid(win)
	gridNoteList, r = noteGrid(win)

	#wait for user input
	while True:
		#wait for input just incase something doesnt load intime
		key = win.checkKey()
		pt = win.checkMouse()

		if pt:
			time.sleep(0.01)
			x = pt.getX()
			y = pt.getY()
			#edits the grid and updates the window on notes clicked
			#changes bigrid based on clicks
			#i call it bi grid because it contains booleans... bad name ik
			biGridTemp = checkNotes(gridNoteList, win, x, y, r, biGrid)
			#checks if bpm has entry
			#this is to prevent making my whole grid being set to None
			if biGridTemp is not None:
				biGrid = biGridTemp
			
			#now i must make play buttone and use biGrid to play them
			if x >= x0 and x <= x1 and y >= y0 and y <= y1:
				#plays notes with biGrid
				if bpmEntry.getText():
					playNotes(biGrid, win, bpmEntry.getText())

			if x >= x2 and x <= x3 and y >= y2 and y <= y3:
				exportSheet(biGrid)

			if x >= x4 and x <= x5 and y >= y4 and y <= y5:
				biGrid =  importSheet(win, gridNoteList)



		#returns to main menu if escape is pressed
		if key == 'Escape':
			for line in xLine:
				line.undraw()
			for line in yLine:
				line.undraw()
			for column in gridNoteList:
				for circle in column:
					circle.undraw()
			bpmEntry.undraw()
			bpmText.undraw()
			playMusicBox.undraw()
			playMusicText.undraw()
			exportSheetButtonBox.undraw()
			importSheetButtonBox.undraw()
			exportSheetText.undraw()
			importSheetText.undraw()
			break

	time.sleep(0.25)

#dis draws grid
def drawGrid(win):
	#get the width and height from current window opened
	wid, hei = win.width, win.height

	#grid must be 9 tall, 9 notes
	#starting from top
	#f e d c b a g f e
	# or left side = face from bottom
	# right side every good boy does fine, e g b d f, from bottom

	#set values for grid because having it not be modular will really help speed
	#up this process and i dont think i really want to change it atm
	yLine = []
	for j in range(noteLong):
		line = Line(Point(wid/19*(j+1) ,hei/6), Point(wid/19*(j+1) ,hei*(5/6)))
		line.setFill(COLOR_GRAY)
		line.draw(win)
		yLine.append(line)

	xLine = []
	for i in range(5):
		line = Line(Point(0, (hei/6)*(i+1)), Point(wid, (hei/6)*(i+1)))
		line.setWidth(6)
		line.draw(win)
		xLine.append(line)

	#grid of Falses
	biGrid = []
	for w in range(noteLong):
		biGrid.append([])
		for h in range(9):
			biGrid[w].append(False)
	return xLine, yLine, biGrid

#this will make a list of lists aka a grid bigrid called (gNL)
#will fill the lists with circle objects to be interacted with
def noteGrid(win):
	#grid note list
	heightGrid = 9
	widthGrid = noteLong
	wid, hei = win.width, win.height
	gNL = []
	r = 15
	for w in range(widthGrid): #height of grid / number of notes
		gNL.append([])
		for h in range(heightGrid): #this is debateable/changable

			noteCircle = Circle(Point( wid/19*(w+1) , (hei/6*(h+2))/2) , r)
			noteCircle.setFill(COLOR_GREEN)
			#noteCircle.draw(win) #use to debug

			gNL[w].append(noteCircle) #gird of circle objects for interaction
			

	return gNL, r

#check if notes are interacted with
def checkNotes(gridNoteList, win, px, py, radius, biGrid):
	#this one was made badly, didnt have enough time to redo it
	#its run by magic

	#px and py is the location of where the mouse clicked
	#make a list of all the x and y values of the circles
	cx, cy = [], []
	for w in gridNoteList:
		for circle in w:
			cx.append(circle.getCenter().getX())
			cy.append(circle.getCenter().getY())

	#get number of circles by either measuring the num of x or y values
	for i in range(len(cx)):
		#send back circle that has are point in it
		#check its proximity to circle
		ptc = (((px - cx[i])**2) + ((py - cy[i])**2))**0.5
		#check if its in circle
		if ptc <= radius:
			#checks to see if to undraw or draw circle
			#meaning remove or add a note
			if biGrid[i//9][i%9] == True:

				circle = gridNoteList[i//9][i%9]
				circle.undraw()
				biGrid[i//9][i%9] = False
			else:

				circle = gridNoteList[i//9][i%9]
				circle.draw(win)
				biGrid[i//9][i%9] = True

			return biGrid


#needs redoing 
#plays the notes on the grid and animates it
def playNotes(biGrid, win, bpm):
	#var
	wid, hei = win.width, win.height
	bpm = int(bpm)
	#just in case it goes 2 fast and breaks
	if bpm > 240:
		bpm = 240
	bpm = 60/bpm
	bpm = round(bpm,2)
	count = 0
	count2 = 0
	for i in biGrid:

		circle = Circle(Point(wid/19*(count2+1), hei/8), 8)
		count2 += 1
		circle.setFill('black')
		circle.draw(win)
		for j in i:
			if j == True:
				#play audio
				audio = NOTEFILENAMES[count]
				wave_obj = sa.WaveObject.from_wave_file(MUSICROOT+audio)
				wave_obj.play()
			count+=1
		count=0
		time.sleep(bpm)
		circle.undraw()
	
#plan to make export and inport function for saving patterns
def exportSheet(biGrid):
	with open('test.pkl', 'wb') as f:
		pickle.dump(biGrid, f)

#returns imported list
def importSheet(win, gridNoteList):
	with open('test.pkl', 'rb') as f:
		biGrid = pickle.load(f)

		#loops through both lists and redraws
		#should do this for checknotes but that would take time 
		for x1, x2 in zip(biGrid, gridNoteList):
			for y1, y2 in zip(x1, x2):
				if y1 == True:
					y2.undraw()
					y2.draw(win)
				if y1 == False:
					y2.undraw()

	return biGrid

if __name__ == '__main__':
	main()