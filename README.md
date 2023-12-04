Minesweeper Game

This Minesweeper game is a simple implementation in Python using the Tkinter library for the graphical user interface. The game follows the classic rules of Minesweeper, where the player must reveal cells on a grid while avoiding hidden bombs. The code also includes features like an undo button and a CPU player for automated moves.

Table of Contents

Installation
Usage
Features
Code Structure
Game Rules
Contributing
License
Installation

Clone the repository:
bash
Copy code
git clone https://github.com/your-username/Minesweeper.git
Navigate to the project directory:
bash
Copy code
cd Minesweeper
Run the game:
bash
Copy code
python minesweeper.py
Usage

Left-click on cells to reveal them.
Right-click on cells to place flags.
Use the "Undo" button to undo the last move.
Click on "CPU Player" to let the computer automatically make a move.
Features

Classic Minesweeper gameplay.
Undo feature to reverse the last move.
CPU player for automated moves.
Simple graphical interface using Tkinter.
Win/lose conditions and game over screen.
Code Structure

minesweeper.py: The main Python script containing the Minesweeper game logic.
README.md: This documentation file.
.gitignore: Specifies files and directories to be ignored by version control.
LICENSE: The license file for the project.
Game Rules

The game grid is a 30x16 matrix.
There are 60 hidden bombs randomly placed on the grid.
Left-click to reveal cells.
Numbers indicate the number of adjacent bombs.
Right-click to place flags on potential bombs.
The game ends when all non-bomb cells are revealed or a bomb is clicked.
Contributing

Contributions are welcome! If you'd like to contribute to the project, please follow the contribution guidelines.

License

This Minesweeper game is open-source and available under the MIT License.
