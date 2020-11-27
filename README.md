# games-analysis
Interesting approaches to solving interesting games.

## sudoku-solver.py

#### Solves sudoku puzzles as a human would; using intuitive strategies. It gives a walkthrough to the solution.
It follows the popular strategies named [here](https://bestofsudoku.com/sudoku-strategy). As an experimental aside, I'm working on a _hypothesize_ function that guesses a move, then spawns a new puzzle from that, attempting to recursively solve that one, and if that fails, it backtracks and guesses again. This idea is based on how most people, having not discovered the logically sound and exhaustive strategies, actually try their hand at sudoku. It's mathematically redundant to the strategies and hence unnecessary, but it turns out to give some of the more interesting walkthroughs ;)
