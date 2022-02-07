class Controller:
    def __init__(self, tab, options, view):
        self.tab = tab # set the tab
        self.tab.list = self.createList(self.tab.height, self.tab.width) # create the default tab's list
        self.options = options # set options

        self.view = view # set view
    
    def createList(self, lines_count:int, columns_count:int):
        """
        Create a list of list\n
        Return a list of list with False for each element in all sublists
        """
        return [[False for column in range(columns_count)] for line in range(lines_count)]
        
    def addCrown(self, tab):
        """
        Add a crown arround a tab list
        """
        lines_count = len(tab.list)
        columns_count = len(tab.list[0])

        new_list = self.createList(lines_count+2, columns_count+2)

        for i in range(lines_count):
            for j in range(columns_count): new_list[i+1][j+1] = tab.list[i][j]
        
        tab.list = new_list
    
    def aliveInCrown(self, tab):
        """
        Detect if they are alive cells in tab list crown\n
        Return `False` if not, else `True`
        """
        for line in tab.list:
            if line[0] or line[-1]: return True

        for column in tab.list[0]:
            if column: return True
        
        for column in tab.list[-1]:
            if column: return True
        
        return False
    
    def removeCrown(self, tab):
        """
        Remove the tab list crown if no alive cell in crown
        """
        lines_count = len(tab.list)
        columns_count = len(tab.list[0])

        if lines_count <= tab.height or columns_count <= tab.width: return
        elif self.aliveInCrown(tab): return

        new_list = self.createList(lines_count-2, columns_count-2)
        for i in range(1, lines_count-1):
            for j in range(1, columns_count-1):
                new_list[i-1][j-1] = tab.list[i][j]

        tab.list = new_list

    def onsideAlivesCount(self, tab, case:tuple[int]):
        """
        Calcul how many they are alive cells arround another cell\n
        Return the sum of the alive cells
        """
        line, column = case
        sum_ = 0

        for i in range(line-1, line+2):
            for j in range(column-1, column+2):
                sum_ += int(tab.list[i][j])
        
        if tab.list[line][column]: return sum_-1
        return sum_

    def toggleCase(self, tab, case:tuple[int]):
        """
        Change cell state in the tab list
        """
        line, column = case
        tab.list[line][column] = not tab.list[line][column]
    
    def editCase(self, tab, case:tuple[int]):
        """
        Decide if a cell must be alive or not\n
        Return `True` if yes, else `False`
        """
        alives = self.onsideAlivesCount(tab, case)
        line, column = case
        
        if tab.list[line][column]:
            if 2 <= alives <= 3:
                return True
        else:
            if alives == 3:
                return True
        
        return False

    def nextGeneration(self, tab):
        """
        Create new generation of cells from the old
        """
        # add crowns
        ## add 2 crown to can modify first and don't tuch the second
        self.addCrown(tab)
        self.addCrown(tab) 

        new_list = self.createList(len(tab.list), len(tab.list[0]))

        for i in range(1, len(tab.list)-1):
            for j in range(1, len(tab.list[0])-1):
                edit = self.editCase(tab, (i, j))
                new_list[i][j] = edit

        tab.list = new_list

        # remove crowns
        self.removeCrown(tab)
        self.removeCrown(tab)

    def updateView(self):
        """
        Update view
        """
        self.view.update(self.tab, self.options.lines, self.options.columns, self.options.box_size)

    def mouseDown(self, event):
        """
        Called by view when user clicks on grid
        """
        if (event.y >= self.options.lines*self.options.box_size) or (event.x >= self.options.columns*self.options.box_size): return
        line_difference = (len(self.tab.list)-self.options.lines)//2
        col_difference = (len(self.tab.list[0])-self.options.columns)//2

        line = int(event.y//self.options.box_size)+(line_difference)
        col = int(event.x//self.options.box_size)+(col_difference)
        
        self.toggleCase(self.tab, (line, col))
        self.updateView()

    def nextButtonClicked(self):
        """
        Called by view when user clicks on next button
        """
        self.nextGeneration(self.tab)
        self.updateView()

    def resetButtonClicked(self):
        """
        Called by view when user clicks on reset button
        """
        self.tab.list = self.createList(self.tab.height, self.tab.width)
        self.updateView()

    def toggleAutoGeneration(self):
        """
        Change auto generation state
        """
        self.options.auto_generation = not self.options.auto_generation
    
    def get_auto_generation_state(self):
        """
        Get auto generation state
        """
        return self.options.auto_generation

    def autoGeneration(self):
        """
        Called every [options.auto_generation_delay]ms to create new generation and update view
        """
        if self.options.auto_generation:
            self.nextGeneration(self.tab)
            self.updateView()

        self.view.after(self.options.auto_generation_delay, self.autoGeneration)

    def set_auto_generation_delay(self, delay:int):
        """
        Change auto generation speed delay
        """
        self.options.auto_generation_delay = delay
