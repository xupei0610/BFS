# Soduko

This is a sudoku solver written by Pei Xu (ID#: 5186611) using BFS.

Two spaces used as a tab in this file.

=============================================================================================================
## Usage of this file:
  
   Go to command line
   
   CD to the folder that contains this file whose name is sudoku_5186611.py
   
   Input "python sudoku_5186611.py", and press the enter or return button
   
   Then the program will automatically run with the three examples given in the assignment.
   
=============================================================================================================
 
## Incomplete Parts:
  
  A more intelligent heuristic function should be used to increase the sudoku solver's efficiency.
  
  Without heuristic function, BFS will take too long time to solve hard sudoku games, although some pruning technologies are used already.
  
  
============================================================================================================

## Known Bugs:
  
  None

=============================================================================================================

## The Representation of A Node:
  
  In the class SudokuSolver, the class Node is used to represent a node.
  
  It has a one-dimesional list variable _state to store its state, and we can get the variable via Node.getState().
  
  In the list, the squares in a sudoku game are ordered from left to right and top to bottom.
  
  e.g. For a Sudoku game having n x n squares, the node's state
  
      [ N11, N12, N13, ..., N1n, N21, ..., N2n, ..., Nn1,      ...,      Nnn ]
  represents a state in which **Nij** (i belongs to 1 to n, and j belongs to 1 to n) is the number at the square locating at the joint of the row i and col j.
          
=============================================================================================================

## Prunings Used by the Solver:
  
  (1) Reduce d (the depth of the shallowest goal) via setting the initial value in the initial node for the squares that are given number beforehand.
  
  e.g. For the sudoku game,
  
        1 5 . | . 4 .
        
        2 4 . | . 5 6
        
        _ _ _   _ _ _
        
        4 . . | . . 3
        
        . . . | . . 4
        
        _ _ _   _ _ _
        
        6 3 . | . 2 .
        
        . 2 . | . 3 1
        
  its initial state is
    
        [1, 5, 0, 0, 4, 0,
        
        2, 4, 0, 0, 5, 6,
        
        4, 0, 0, 0, 0, 3,
        
        0, 0, 0, 0, 0, 4,
        
        6, 3, 0, 0, 2, 0,
        
        0, 2, 0, 0, 3, 1]
    
  rather than a list all of whose terms are zero.
    
  Through this way, d in the above example can be reduced from 36 to 20.
    
    This pruning is used in the function Node.assignInitialState()
    
    
  (2) Control the child nodes' amount by the rule that in a sudoku game having n x n square, squares in a row, a column or a subset have different numbers that must belong to the set 1 to n.
  
  We use a dictionary variable {position: [values], ...} to record the possible numbers of an unknown squares when we generate the initial state.
  
  Take the above example, we can get the possible numbers in every squares.
  
      1, 5, [3, 6], [2, 3], 4, [2],
      
      2, 4, [3], [1, 3], 5, 6,
      
      4, [1, 6], [1, 2, 5, 6], [1, 2, 5, 6], [1, 6], 3,
      
      [3, 5], [1, 6], [1, 2, 3, 5, 6], [1, 2, 5, 6], [1, 6], 4,
      
      6, 3, [1, 4, 5], [4, 5], 2, [5],
      
      [5], 2, [4, 5], [4, 5, 6], 3, 1

  We store it to a dictionary variable { 3: [3, 6], 4: [2, 3], 6: [2], ... }
  
  So that we can only generate two (rather than nine) child nodes from the initial node, the two nodes whose 3rd square respectively has the number 3 and 6.
  
    This pruning is used in the function Node.assignInitialState()
  
  
  (3) Discard the node immediately when it is generated if the node's state conflicts with the rule that in a sudoku game having n x n square, squares in a row, a column or a subset have different numbers that must belong to the set 1 to n.
  
  That is to say, a node whose state conflicts with that rule may be generated, but it would be discarded immediately and the child nodes of that illegal node would not be generated.
  
    This pruning is used in the function SudokuSolver.solve()
    

=============================================================================================================

## Modifications Made to BFS:
  
  (1) For a node in the frontier list, if it does not have any zero term, it must be the solution, because the nodes whose state has a number that conflicts with the sudoku's rule will not be stored into the frontier list.
  
  So that the node must be solution if it represent a state in which all squares have a number.
  
  That is to say, we do not need to use the function like isGoal(a_nodes_state) to test if a node's state is the goal state.
  
  This modification is used in the function SudokuSolver.solve()
  
  
  (2) In order to reduce the amount of the action of generating child nodes, we use a heuristic function h(x) to decide which square should be put into a number when generating child nodes from a parent node.
  
  h(x) = the amount of the possible numbers in the square x.
  
  That is to say, every time the program only **tries** to put number into the blank square who has the fewest possible numbers.
  
  Take the above example, the program will first try to generate only one child node of the initial node, the chid node in whose state the last square in the 1st row has a number 2, because that square is only possible to have a number 2.
  
  This modification is used in the function Node.assignInitialState()
  
  **Lots of examples were tested. And it proved that this modification cannot works well frequently.**
  
  Testing data are at the end of this file.

=============================================================================================================

## Question:
   
###1. Write the equation using b and d that represents the size of the search tree when there is no pruning.
Is this different from the search space (briefly justify)?
  
  The size of the search tree is 1 + b + b^2 + ... + b^d if no pruning is used.
  
  It is different to the size of the search space, because not all the node in a search tree has a legal state that belongs to the corresponding search space.

###2. When there is no pruning, what are the minimum and maximum number of nodes you might need to
explore to find a solution? Briefly justify.

  If no pruning is used, the minimum number of nodes we need to explore is 1,
  
  (this situation only happens when the first node (the initial state) is also the goal state; but in general, only when we reach the last depth may we find the solution so that we need to explore all the nodes before the we reach the last depth, then plus at least the 1st node in the last depth, and the number of nodes we need to explore is 1 + b + b^2 + ... + b^(d-1) + 1),
  
  and the maximum number of nodes we need to explore is 1 + b + b^2 + ... + b^d
  
  (this situation happens when the last node in the last depth is the solution; namely, we need to explore all the nodes).

###3. Quantify the effects of pruning on the size of the search tree. You can do this empirically by counting
nodes within your code or derive a theoretical bound.

  For a sudoku game with n * n squares,
  
  if no pruning is used, (1 + n + n^2 + ... + n^(n^2-1) + 1) to (1 + n + n^2 + ... + n^(n^2)) nodes in the search tree needed to be generated and explored.
  
  Through the method Pruning (1), if we have m squares in which a number is given beforehand, only (1 + n + n^2 + ... + n^(n^2-1)) nodes need to be generated. So the method largely reduced the amount of nodes we need to generate even if only one square is given a number beforehand.
  
  As for the method Pruning (2) (3) and the modification to BFS, their effects vary and depend a lot on concrete sudoku games.
  
  Take the sudoku game below as an example.
  
        1 5 . | . 4 .
        2 4 . | . 5 6
        _ _ _   _ _ _
        4 . . | . . 3
        . . . | . . 4
        _ _ _   _ _ _
        6 3 . | . 2 .
        . 2 . | . 3 1
        
  Without any pruning, 1 + 6 + 6^2 + ... + 6^36 = 12377309758188642655406338867 nodes need to be generated.
  
  Through the method Pruning (1), only 1 + 6 + 6^2 + ... + 6^20 = 4387390128075571 nodes need to be generated.
  
  And, through the method Pruning (2) (3) and the modification made to BFS, the number of nodes generated during the process of the program's finding a solution can be further reduced to only 107.
  
=============================================================================================================
