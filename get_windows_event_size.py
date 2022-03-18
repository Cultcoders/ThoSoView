import tkinter as tk

class Fenster(object):
    def __init__(self):
        self.weite = 108
        self.hoehe = 200
        self.gui()

    def gui(self):
        self.fenster = tk.Tk()
        self.fenster.geometry('%dx%d' % (self.weite, self.hoehe))
        # self.fenster.bind("<Configure>", self.callback)   # Configure the exact but hard way
        self.fenster.bind("<Enter>", self.callback)
        self.fenster.bind("<Leave>", self.callback)
        self.fenster.mainloop()

    def callback(self, event):
        weite_neu = self.fenster.winfo_width()
        hoehe_neu = self.fenster.winfo_height()
        print(f'widht: {event.x}')
        if self.weite != weite_neu:
            print(f'Weite geändert: {weite_neu}')
            self.weite = weite_neu
        if self.hoehe != hoehe_neu:
            print(f'Höhe geändert: {hoehe_neu}')
            self.hoehe = hoehe_neu

if __name__ == '__main__':
    Fenster()
