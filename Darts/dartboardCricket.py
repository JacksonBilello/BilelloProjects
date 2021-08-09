import tkinter as tk
from pygame_functions import *


class Darts:
    root = tk.Tk()

    def __init__(self, numof20t1, numof19t1, numof18t1, numof17t1, numof16t1, numof15t1, numofbullt1, numof20t2, numof19t2, numof18t2, numof17t2, numof16t2, numof15t2, numofbullt2, t1name, t2name):
        self.numof20t1 = numof20t1
        self.numof19t1 = numof19t1
        self.numof18t1 = numof18t1
        self.numof17t1 = numof17t1
        self.numof16t1 = numof16t1
        self.numof15t1 = numof15t1
        self.numofbullt1 = numofbullt1
        self.numof20t2 = numof20t2
        self.numof19t2 = numof19t2
        self.numof18t2 = numof18t2
        self.numof17t2 = numof17t2
        self.numof16t2 = numof16t2
        self.numof15t2 = numof15t2
        self.numofbullt2 = numofbullt2
        self.team1name = t1name
        self.team2name = t2name

    def addt1(self, number):
        if number == 20:
            if self.numof20t1 < 3:
                l20 = tk.Label(text="20", fg="black", bg="green", width=5, height=5)
                l20.place(x=220+self.numof20t1*80, y=140)
                self.numof20t1 += 1
        elif number == 19:
            if self.numof19t1 < 3:
                l19 = tk.Label(text="19", fg="black", bg="green", width=5, height=5)
                l19.place(x=220+self.numof19t1*80, y=240)
                self.numof19t1 += 1
        elif number == 18:
            if self.numof18t1 < 3:
                l18 = tk.Label(text="18", fg="black", bg="green", width=5, height=5)
                l18.place(x=220+self.numof18t1*80, y=340)
                self.numof18t1 += 1
        elif number == 17:
            if self.numof17t1 < 3:
                l19 = tk.Label(text="17", fg="black", bg="green", width=5, height=5)
                l19.place(x=220+self.numof17t1*80, y=440)
                self.numof17t1 += 1
        elif number == 16:
            if self.numof16t1 < 3:
                l18 = tk.Label(text="16", fg="black", bg="green", width=5, height=5)
                l18.place(x=220+self.numof16t1*80, y=540)
                self.numof16t1 += 1
        elif number == 15:
            if self.numof15t1 < 3:
                l19 = tk.Label(text="15", fg="black", bg="green", width=5, height=5)
                l19.place(x=220+self.numof15t1*80, y=640)
                self.numof15t1 += 1
        elif number == 10:
            if self.numofbullt1 < 3:
                l18 = tk.Label(text="Bull", fg="black", bg="green", width=5, height=5)
                l18.place(x=220+self.numofbullt1*80, y=740)
                self.numofbullt1 += 1

    def addt2(self, number):
        if number == 20:
            if self.numof20t2 < 3:
                l20 = tk.Label(text="20", fg="black", bg="red", width=5, height=5)
                l20.place(x=600+self.numof20t2*80, y=140)
                self.numof20t2 += 1
        elif number == 19:
            if self.numof19t2 < 3:
                l19 = tk.Label(text="19", fg="black", bg="red", width=5, height=5)
                l19.place(x=600+self.numof19t2*80, y=240)
                self.numof19t2 += 1
        elif number == 18:
            if self.numof18t2 < 3:
                l18 = tk.Label(text="18", fg="black", bg="red", width=5, height=5)
                l18.place(x=600+self.numof18t2*80, y=340)
                self.numof18t2 += 1
        elif number == 17:
            if self.numof17t2 < 3:
                l19 = tk.Label(text="17", fg="black", bg="red", width=5, height=5)
                l19.place(x=600+self.numof17t2*80, y=440)
                self.numof17t2 += 1
        elif number == 16:
            if self.numof16t2 < 3:
                l18 = tk.Label(text="16", fg="black", bg="red", width=5, height=5)
                l18.place(x=600+self.numof16t2*80, y=540)
                self.numof16t2 += 1
        elif number == 15:
            if self.numof15t2 < 3:
                l19 = tk.Label(text="15", fg="black", bg="red", width=5, height=5)
                l19.place(x=600+self.numof15t2*80, y=640)
                self.numof15t2 += 1
        elif number == 10:
            if self.numofbullt2 < 3:
                l18 = tk.Label(text="bull", fg="black", bg="red", width=5, height=5)
                l18.place(x=600+self.numofbullt2*80, y=740)
                self.numofbullt2 += 1

    def checkwinner(self):
        if (self.numof20t1 == 3) & (self.numof19t1 == 3) & (self.numof18t1 == 3) & (self.numof17t1 == 3) & (
                self.numof16t1 == 3) & (self.numof15t1 == 3) & (self.numofbullt1 == 3):
            self.congrats(team1name)
        elif (self.numof20t2 == 3) & (self.numof19t2 == 3) & (self.numof18t2 == 3) & (self.numof17t2 == 3) & (
                self.numof16t2 == 3) & (self.numof15t2 == 3) & (self.numofbullt2 == 3):
            self.congrats(team2name)

    def congrats(self, name):
        winlabel = tk.Label(text="Congrats " + name, fg="white", bg="black", width=20, height=5)
        winlabel.place(x=420, y=15)

    canvas = tk.Canvas(root, height=850, width=1000, bg="#263D42")
    canvas.pack()

    frame = tk.Frame(root, bg="white")
    frame.place(relwidth=1, relheight=1, relx=0, rely=0)

    titleLabel = tk.Label(text="Wooftop Saloon Dartboard", fg="white", bg="black", width=20, height=2)
    titleLabel.place(x=420, y=0)


pygame.init()
screenSize(400, 150)
instructionLabel = makeLabel("TEAM 1 NAME", 40, 55, 25, "blue", "Agency FB", "white")
showLabel(instructionLabel)

wordBox = makeTextBox(55, 80, 240, 2, "Enter text here", 0, 24)
showTextBox(wordBox)
team1name = textBoxInput(wordBox)

screenSize(400, 150)
instructionLabel = makeLabel("TEAM 2 NAME", 40, 55, 25, "blue", "Agency FB", "white")
showLabel(instructionLabel)

wordBox = makeTextBox(55, 80, 240, 2, "Enter text here", 0, 24)
showTextBox(wordBox)
team2name = textBoxInput(wordBox)
pygame.quit()

D = Darts(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, team1name, team2name)


# Team 1
t1Label = tk.Label(text=D.team1name, fg="white", bg="green", width=25, height=2)
t1Label.place(x=220, y=70)

button20t1 = tk.Button(D.root, text="20", padx=30, pady=30, command=lambda: D.addt1(20))
button20t1.place(x=10, y=140)

button19t1 = tk.Button(D.root, text="19", padx=30, pady=30, command=lambda: D.addt1(19))
button19t1.place(x=10, y=240)

button18t1 = tk.Button(D.root, text="18", padx=30, pady=30, command=lambda: D.addt1(18))
button18t1.place(x=10, y=340)

button17t1 = tk.Button(D.root, text="17", padx=30, pady=30, command=lambda: D.addt1(17))
button17t1.place(x=10, y=440)

button16t1 = tk.Button(D.root, text="16", padx=30, pady=30, command=lambda: D.addt1(16))
button16t1.place(x=10, y=540)

button15t1 = tk.Button(D.root, text="15", padx=30, pady=30, command=lambda: D.addt1(15))
button15t1.place(x=10, y=640)

buttonbullt1 = tk.Button(D.root, text="Bullseye", padx=15, pady=30, command=lambda: D.addt1(10))
buttonbullt1.place(x=10, y=740)

# team 2
t2Label = tk.Label(text=D.team2name, fg="white", bg="red", width=25, height=2)
t2Label.place(x=600, y=70)

button20t2 = tk.Button(D.root, text="20", padx=30, pady=30, command=lambda: D.addt2(20))
button20t2.place(x=900, y=140)

button19t2 = tk.Button(D.root, text="19", padx=30, pady=30, command=lambda: D.addt2(19))
button19t2.place(x=900, y=240)

button18t2 = tk.Button(D.root, text="18", padx=30, pady=30, command=lambda: D.addt2(18))
button18t2.place(x=900, y=340)

button17t2 = tk.Button(D.root, text="17", padx=30, pady=30, command=lambda: D.addt2(17))
button17t2.place(x=900, y=440)

button16t2 = tk.Button(D.root, text="16", padx=30, pady=30, command=lambda: D.addt2(16))
button16t2.place(x=900, y=540)

button15t2 = tk.Button(D.root, text="15", padx=30, pady=30, command=lambda: D.addt2(15))
button15t2.place(x=900, y=640)

buttonbullt2 = tk.Button(D.root, text="Bullseye", padx=15, pady=30, command=lambda: D.addt2(10))
buttonbullt2.place(x=900, y=740)

D.checkwinner()

D.root.mainloop()
