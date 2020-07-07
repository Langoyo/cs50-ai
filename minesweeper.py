import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        mines = []
        if len(self.cells) <= self.count:
            for cell in self.cells:
                mines.append(cell)
        return mines
                

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        safe = []
        if self.count == 0:
            for cell in self.cells:
                safe.append(cell)
        return safe

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        self.moves_made.add(cell)

        self.mark_safe(cell)

        neighboring_cells = self.get_neighbours(cell)

        if len(neighboring_cells) > 0:
            sentence = Sentence(neighboring_cells,count)
            self.knowledge.append(sentence)

        self.update_knowledge()

        self.inference()


    def get_neighbours(self, cell):
        neighboring_cells = []
        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Append the unkown valid cells
                if 0 <= i < self.height and 0 <= j < self.width and (i,j) not in self.moves_made:
                    neighboring_cells.append((i,j))
        return neighboring_cells   

    def inference(self):
        """
        Tries to obtain new knowledge
        """

        new_knowledge = []
        for sen1 in self.knowledge:
            for sen2 in self.knowledge:
                # Check that one is subset of the other
                if sen1 != sen2 and sen2.cells.issubset(sen1.cells):
                    cell_diff = sen1.cells - sen2.cells
                    count_diff = sen1.count - sen2.count

                    # If the new sentence is safe we update the cells
                    if count_diff == 0:
                        for cell in cell_diff:
                            self.mark_safe(cell)

                    #If the new sentence contains mines we mark them
                    elif count_diff == len(cell_diff):
                        for cell in cell_diff:
                            self.mark_mine(cell)

                    # Otherwise it is added to the knowledge
                    else:
                        new_sentence = Sentence(cell_diff,count_diff)
                        if not self.already_contained(self.knowledge,new_sentence):
                            new_knowledge.append(new_sentence)

        for sentence in new_knowledge:
            self.knowledge.append(sentence)
    
    def update_knowledge(self):
        """
        Removes empty sentences and searches for new mines and safes
        """

        for sentence in self.knowledge:
            if (len(sentence.cells) == 0):
                self.knowledge.remove(sentence)
            else:   
                mines_found = sentence.known_mines()
                for mine in mines_found:
                    self.mark_mine(mine)

                safes_found = sentence.known_safes()
                for safe in safes_found:
                    self.mark_safe(safe)


            

    def already_contained(self, knowledge, new_sentence):
        """
        Checks if a sentence is already contained in the knowledge base
        """
        for sentence in knowledge:
            if new_sentence.__eq__(sentence):
                return True
        return False
    
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        
        for cell in self.safes:
            if cell not in self.moves_made and cell not in self.mines:
                return cell
        return None
        
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        attempts = 0

        while(attempts < 10 ):
            i = random.randrange(0,self.height)
            j = random.randrange(0,self.width)

            if (i,j) not in self.mines and (i,j) not in self.moves_made:
                return (i,j)
            attempts += 1

        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                    return (i,j)
        return None