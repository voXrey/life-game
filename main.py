from tkinter import Tk
import tkinter
from model import Tab, Options
from view import View
from controller import Controller


class Application(Tk):
    def __init__(self):
        super().__init__()

        LINES = 11
        COLUMNS = 12
        BOX_SIZE = 50

        self.title(f'Life Game {COLUMNS}x{LINES}')

        # create models
        tab = Tab(width=COLUMNS, height=LINES)
        options = Options(columns=COLUMNS, lines=LINES, box_size=BOX_SIZE)

        # create the view
        view = View(parent=self)
        view.grid.configure(width=options.width, height=options.height)
        view.pack()

        # create controller
        controller = Controller(tab, options, view)

        # set the controller to view
        view.setController(controller)

        # update view to see grid
        controller.updateView()

        # start auto generation on the view
        view.after(options.auto_generation_delay, controller.autoGeneration)

if __name__ == '__main__':
    app = Application()
    app.mainloop()
