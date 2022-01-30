from tkinter import ALL, HORIZONTAL, BooleanVar, Canvas, Button, Checkbutton, Scale, IntVar
from tkinter.ttk import Frame

class View(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = None
        self.createView()

    def createView(self):
        """
        Create widgets
        """
        self.createGridCanvas()
        self.createNextGenerationButton()
        self.createResetButton()
        self.createAutoGenerationButton()
        self.createAutoGenerationScale()

    def createGridCanvas(self):
        """
        Create grid on a canvas
        """
        self.grid = Canvas(self)
        self.grid.bind("<Button-1>", self.mouseDown)
        self.grid.pack()
 
    def createNextGenerationButton(self):
        """
        Add next generation button
        """
        self.next_button = Button(self, text='Next Generation', command=self.nextButtonClicked)
        self.next_button.pack()

    def createResetButton(self):
        """
        Add reset button
        """
        self.reset_button = Button(self, text='Reset', command=self.resetButtonClicked)
        self.reset_button.pack()
    
    def createAutoGenerationButton(self):
        """
        Add auto generation check button
        """
        self.auto_generation_check_button = Checkbutton(self, text='Auto-generation', command=self.toggleAutogenerationClicked)
        self.auto_generation_check_button.pack()
    
    def createAutoGenerationScale(self):
        """
        Add scale to change auto generation speed
        """
        self.auto_generation_scale_var = IntVar()
        self.auto_generation_scale_state = BooleanVar(value=False)
        self.auto_generation_scale = Scale(self,
                                            command=self.autoGenerationScaleChanged,
                                            orient= HORIZONTAL,
                                            from_=200,
                                            to=2000,
                                            resolution=10,
                                            length=350,
                                            label='Speed (ms)'
                                            )
        self.auto_generation_scale.set(1000)
        self.auto_generation_scale.pack()

    def setController(self, controller):
        """
        Set view controller
        """
        self.controller = controller

    def drawGrid(self, grid_lines_count:int, grid_columns_count:int, grid_box_size:int):
        """
        Draw grid on canvas
        """
        for i in range(grid_lines_count):
            self.grid.create_line(0, i*grid_box_size, grid_columns_count*grid_box_size, i*grid_box_size)
        
        for j in range(grid_columns_count):
            self.grid.create_line(j*grid_box_size, 0, j*grid_box_size, grid_lines_count*grid_box_size)
        
    def clearGrid(self, grid_lines_count:int, grid_columns_count:int, grid_box_size:int):
        """
        Delete all elements in grid canvas, then draw grid
        """
        self.grid.delete(ALL)
        self.drawGrid(grid_lines_count, grid_columns_count, grid_box_size)

    def drawCell(self, x:int, y:int, grid_box_size:int):
        """
        Draw a cell in grid canvas
        """
        self.grid.create_rectangle(x*grid_box_size,
                                    y*grid_box_size,
                                    (x+1)*grid_box_size,
                                    (y+1)*grid_box_size,
                                    fill='black')
    
    def drawCells(self, tab, grid_lines_count:int, grid_columns_count:int, grid_box_size:int):
        """
        Draw all cells which are alived on canvas grid
        """
        line_difference = (len(tab.list)-grid_lines_count)//2
        col_difference = (len(tab.list[0])-grid_columns_count)//2

        for i in range(line_difference, line_difference+tab.height):
            for j in range(col_difference, col_difference+tab.width):
                if tab.list[i][j]:
                    self.drawCell(j-col_difference, i-line_difference, grid_box_size)

    def update(self, tab, grid_lines_count:int, grid_columns_count:int, grid_box_size:int):
        """
        Update grid canvas
        """
        self.clearGrid(grid_lines_count, grid_columns_count, grid_box_size)
        self.drawCells(tab, grid_lines_count, grid_columns_count, grid_box_size)

    def mouseDown(self, event):
        """
        When user clicks on grid canvas
        """
        self.controller.mouseDown(event)
    
    def nextButtonClicked(self):
        """
        When user clicks on next generation button
        """
        self.controller.nextButtonClicked()
    
    def resetButtonClicked(self):
        """
        When user clicks on reset button
        """
        self.controller.resetButtonClicked()

    def toggleAutogenerationClicked(self):
        """
        When user clicks on auto generation button
        """
        self.controller.toggleAutoGeneration()
        self.auto_generation_scale_state = self.controller.get_auto_generation_state()

    def autoGenerationScaleChanged(self, value):
        """
        Called when user change value of auto generation speed scale
        """
        self.controller.set_auto_generation_delay(value)
    