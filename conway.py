# Definition of Cell object, will hold all the properties of cell
class Cell:
    def __init__(self, row, col, status, surface):
        """
        Create a cell
        params
        row : Row index of cell in 2D array
        col : Column index of cell in 2D array
        status : Boolean to show if the cell is on/alive
        surface : PyGame surface object for surface on which cell is drawn
        """
        self.row = row
        self.col = col
        self.status = status
        self.surface = surface

    def show(self):
        """
        Draws each cell, according to if it's on/alive
        """
        if self.status:
            pygame.draw.rect(self.surface, ON_COLOR, pygame.Rect(
                self.col * CELL_WIDTH, self.row * CELL_HEIGHT, CELL_WIDTH * 0.99, CELL_HEIGHT * 0.99))
        else:
            pygame.draw.rect(self.surface, CELL_COLOR, pygame.Rect(
                self.col * CELL_WIDTH, self.row * CELL_HEIGHT, CELL_WIDTH * 0.99, CELL_HEIGHT * 0.99))

    def highlight(self):
        """
        Draws a highlight on the current cell
        """
        temp = pygame.Surface((CELL_HEIGHT, CELL_WIDTH), pygame.SRCALPHA)
        pygame.draw.rect(temp, HIGHLIGHT, pygame.Rect(
            0, 0, CELL_WIDTH, CELL_HEIGHT))
        self.surface.blit(
            temp, (self.col * CELL_WIDTH, self.row * CELL_HEIGHT))

    def check_neighbours(self):
        """
        Return number of alive neighbours
        """
        indices = [
            self.index(self.row - 1, self.col - 1),
            self.index(self.row - 1, self.col),
            self.index(self.row - 1, self.col + 1),

            self.index(self.row, self.col - 1),
            self.index(self.row, self.col + 1),

            self.index(self.row + 1, self.col - 1),
            self.index(self.row + 1, self.col),
            self.index(self.row + 1, self.col + 1),
        ]

        count = 0

        # For every neighbour, if it is exists and is not visited, add it to the list of neighbours
        for i in indices:
            if (i != None) and cells[i].status:
                count += 1

        return count

    def iterate(self):
        """
        Iterate over time, set new frame according to Conway's rules
        """
        c = self.check_neighbours()
        if self.status:
            if (c < 2) or (c > 3):
                next_frame[self.index(self.row, self.col)] = False
        else:
            if c == 3:
                next_frame[self.index(self.row, self.col)] = True

    @staticmethod
    def index(row, col):
        """
        Get the 1D array index of an element in a 2D array. Rows are stacked next to each other without seperation in the 1D array
        params
        row : Row index of the cell in 2D array
        col : Column index of the cell in 2D array
        """
        if (row < 0) or (col < 0) or (row >= VERTICAL_BLOCKS) or (col >= HORIZONTAL_BLOCKS):
            return None
        return col + (row * HORIZONTAL_BLOCKS)


if __name__ == "__main__":
    import pygame
    import time
    import sys
    import conway_reader

    FILEPATH = "./hilbert.rle"
    FPS = 15

    # Read in file
    game = conway_reader.read_rle(FILEPATH)
    config = game.board

    # Set for Window size
    HORIZONTAL_BLOCKS = game.width
    VERTICAL_BLOCKS = game.height

    CELL_WIDTH = 10
    CELL_HEIGHT = 10

    # Color constants
    CELL_COLOR = 255, 255, 255
    ON_COLOR = 0, 0, 0
    HIGHLIGHT = 255, 0, 0, 75
    BG_COLOR = 180, 180, 180

    # Initialise PyGame
    pygame.init()

    # Create screen for showing viusalisation
    size = width, height = HORIZONTAL_BLOCKS * \
        CELL_HEIGHT, VERTICAL_BLOCKS * CELL_HEIGHT
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Conway's Game of Life")

    # Create a 1D list of cells, and append cells to it
    cells = []

    # Create board
    for i in range(VERTICAL_BLOCKS):
        for j in range(HORIZONTAL_BLOCKS):
            cells.append(
                Cell(i, j, config[i*HORIZONTAL_BLOCKS + j], screen)
            )

    print("Initial Config...")
    screen.fill(BG_COLOR)

    # Show every cell
    for k in cells:
        k.show()

    pygame.display.update()

    # Tick the display as per FPS
    pygame.time.Clock().tick(FPS)
    time.sleep(2)

    print("Starting game...")

    # While game is running, for every frame,
    while True:

        # Store events to process quit and KeyDown events
        events = pygame.event.get()

        # Handle exit event
        for event in events:
            # Let user exit
            if event.type == pygame.QUIT:
                sys.exit()

        # Fill the screen with BG_COLOR
        screen.fill(BG_COLOR)

        next_frame = [x.status for x in cells]

        # Iterate every cell
        for k in cells:
            k.iterate()

        # Show every cell after copying details
        counter = 0
        for k in cells:
            k.status = next_frame[counter]
            k.show()
            counter += 1

        # Update the display
        pygame.display.update()

        # Tick the display as per FPS
        pygame.time.Clock().tick(FPS)
