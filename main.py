import pyautogui as pag
from tkinter import *
import pytesseract
import cv2
import numpy as np


pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\/tesseract.exe'

class MainApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("PyAutoGUI")
        self.canvas1 = Canvas(self, width=300, height=300, bg="white")
        self.canvas1.pack()
        self.myButton = Button(text='Take Screenshot', command=self.fillscreenWithCanvas,
                               bg='green', fg='white', font=15)
        self.canvas1.create_window(150, 150, window=self.myButton)

        self.rect = None
        self.x = 0
        self.y = 0
        self.start_x = None
        self.start_y = None
        self.im = None

    # fill screen with semi transparent black

    def fillscreenWithCanvas(self):
        self.destroy()
        app = Tk()
        app.attributes("-alpha", 0.3)
        # hide the menu bar
        app.overrideredirect(True)
        # set the window to full screen
        app.geometry("{0}x{1}+0+0".format(app.winfo_screenwidth(), app.winfo_screenheight()))
        # create a canvas with 20% opacity
        canvas = Canvas(app, width=pag.size()[0], height=pag.size()[1], bg='white', bd=0, highlightthickness=0)
        canvas.pack()
        app.focus_force()
        app.bind('<Escape>', lambda e: app.destroy())
        self.drawRectangleUsingMouse(canvas, app)

    def drawRectangleUsingMouse(self, canvas, app):
        # draw a rectangle using mouse
        canvas.bind('<Button-1>', lambda event: self.on_button_press(canvas, event))
        canvas.bind('<B1-Motion>', lambda event: self.on_move_press(canvas, event))
        canvas.bind('<ButtonRelease-1>', lambda event: self.on_button_release(canvas, app))

    def on_button_press(self, canvas, event):
        # save mouse drag start position
        canvas.start_x = event.x
        canvas.start_y = event.y

        # create rectangle if not yet exist
        # if not self.rect:
        self.rect = canvas.create_rectangle(self.x, self.y, 1, 1, fill="black")

    def on_move_press(self, canvas, event):
        curX, curY = (event.x, event.y)
        # expand rectangle as you drag the mouse
        canvas.coords(self.rect, canvas.start_x, canvas.start_y, curX, curY)

    def on_button_release(self,canvas, app):
        self.takeScreenshot(canvas, app)
        pass

    #take screenshot using the bbox coordinates and pyautogui function
    def takeScreenshot(self, canvas, app):
        x1, y1, x2, y2 = canvas.coords(self.rect)
        #calculate the width, height and middle point of the rectangle
        width = x2 - x1
        height = y2 - y1
        self.im = pag.screenshot(region=(x1,y1, width, height))
        #im.save('screenshot.png')

        # close the tkinter window
        app.destroy()
        self.getTextInImage()

    def getTextInImage(self):
        self.im = np.array(self.im)
        # preprocess image and use tesseract to get text
        gray = cv2.cvtColor(self.im, cv2.COLOR_BGR2GRAY)
        #gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        #gray = cv2.medianBlur(gray, 3)
        text = pytesseract.image_to_string(gray)
        print(text)


if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
