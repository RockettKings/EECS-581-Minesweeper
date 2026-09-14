
class Difficulty:
    def __init__(self, rows, columns, mineCount):
        self.gridSize = {"row": rows, "column": columns}
        self.mineCount = mineCount

BEGINNER = Difficulty(9, 9, 10)
INTERMEDIATE = Difficulty(16, 16, 40)
EXPERT = Difficulty(16, 30, 99)

