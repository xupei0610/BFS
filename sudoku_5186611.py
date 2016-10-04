# -*- coding:utf-8 -*-

"""
This is a sudoku solver written by Pei Xu (ID#: 5186611) using BFS.

=============================================================================================================
  Usage of this file:
  
   Go to command line
   CD to the folder that contains this file whose name is sudoku_5186611.py
   Input "python sudoku_5186611.py", and press the enter or return button
   Then the program will automatically run with the three examples given in the assignment.
   
=============================================================================================================
 
  Incomplete Parts:
  
  A more intelligent heuristic function should be used to increase the sudoku solver's efficiency.
  
  Without heuristic function, BFS will take too long time to solve hard sudoku games, although some pruning technologies are used already.
  
  
============================================================================================================

  Known Bugs: None
 
=============================================================================================================

  The Representation of A Node:
  
  In the class SudokuSolver, the class Node is used to represent a node.
  It has a one-dimesional list variable _state to store its state, and we can get the variable via Node.getState().
  In the list, the squares in a sudoku game are ordered from left to right and top to bottom.
  e.g. For a Sudoku game having n x n squares, the node's state
        [ N11, N12, N13, ..., N1n,
          N21,      ...,      N2n,
          ..., 
          Nn1,      ...,      Nnn ]
        represents a state in which
          Nij (i belongs to 1 to n, and j belongs to 1 to n) is the number at the square
          locating at the joint of the row i and col j.
          
=============================================================================================================

  Prunings Used by the Solver:
  
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
  We store it to a dictionary variable { 3 : [3, 6], 4 : [2, 3], 6 : [2], ... }
  So that we can only generate two (rather than nine) child nodes from the initial node, the two nodes whose 3rd square respectively has the number 3 and 6.
    This pruning is used in the function Node.assignInitialState()
  
  (3) Discard the node immediately when it is generated if the node's state conflicts with the rule that in a sudoku game having n x n square, squares in a row, a column or a subset have different numbers that must belong to the set 1 to n.
  That is to say, a node whose state conflicts with that rule may be generated, but it would be discarded immediately and the child nodes of that illegal node would not be generated.
    This pruning is used in the function SudokuSolver.solve()

=============================================================================================================

  Modifications Made to BFS:
  
  (1) For a node in the frontier list, if it does not have any zero term, it must be the solution, because the nodes whose state has a number that conflicts with the sudoku's rule will not be stored into the frontier list.
  So that the node must be solution if it represent a state in which all squares have a number.
  That is to say, we do not need to use the function like isGoal(a_nodes_state) to test if a node's state is the goal state.
  This modification is used in the function SudokuSolver.solve()
  
  (2) In order to reduce the amount of the action of generating child nodes,
  we use a heuristic function h(x) to decide which square should be put into a number when generating child nodes from a parent node.
  h(x) = the amount of the possible numbers in the square x.
  That is to say, every time the program only tries to put number into the blank square who has the fewest possible numbers.
  Take the above example, the program will first try to generate only one child node of the initial node, the chid node in whose state the last square in the 1st row has a number 2, because that square is only possible to have a number 2.
  This modification is used in the function Node.assignInitialState()
  
  Lots of examples were tested. And it proved that this modification cannot works well frequently.
  Testing data are at the end of this file.

=============================================================================================================

   Question:
   
1. Write the equation using b and d that represents the size of the search tree when there is no pruning.
Is this different from the search space (briefly justify)?
  
  The size of the search tree is 1 + b + b^2 + ... + b^d if no pruning is used.
  It is different to the size of the search space, because not all the node in a search tree has a legal state that belongs to the corresponding search space.

2. When there is no pruning, what are the minimum and maximum number of nodes you might need to
explore to find a solution? Briefly justify.

  If no pruning is used,
  the minimum number of nodes we need to explore is 1,
  (this situation only happens when the first node (the initial state) is also the goal state; but in general, only when we reach the last depth may we find the solution so that we need to explore all the nodes before the we reach the last depth, then plus at least the 1st node in the last depth, and the number of nodes we need to explore is 1 + b + b^2 + ... + b^(d-1) + 1),
  and the maximum number of nodes we need to explore is 1 + b + b^2 + ... + b^d
  (this situation happens when the last node in the last depth is the solution; namely, we need to explore all the nodes).

3. Quantify the effects of pruning on the size of the search tree. You can do this empirically by counting
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
  And, through the method Pruning (2) (3) and the modification made to BFS, the number of nodes generated during the process of the program's finding a solution can be further reduced to only 107 !!!
  
=============================================================================================================
"""


class SudokuSolver:
  """ This is a sudoku solver written by Pei Xu for the assignment using BFS."""
  
  def __init__(self, size="", restraints={}):
    """ The parameter size defines the size of the Sudoku game. e.g. 2x2, 2x3, 2x4, 3x3, 3x4, 3x5
    The parameter restraints { position:value, ... } defines the given requirement of the Sudoku game.
    e.g. If restraints == {AB:1, DC:3},
         the 2nd square in the 1st row has the number of 1,
         and the 3rd square in the 4th row has the number of 3.
    """
    self.showProgressRate(0)
    if size:
      self.setSize(size)
    else:
      self._offset = (0, 0)
      self._size = 0
    
    self._restraints = {}
    if restraints:
      self.setRestraints(restraints)

  def setSize(self, size):
      side = size.split('x')
      self._offset = (int(side[0]), int(side[1]))
      self._size = self._offset[0] * self._offset[1]
  
  def setRestraint(self, value, position):
    """ Set restraint for the Sudoku game.
    The parameter value is the number given beforehand.
    The parameter position is a string that defines the position the given number.
    e.g. setRestraint(1, 1B) means that the number 1 is given at the 2nd square in the 1st row."""
    i = 0
    for s in position:
      if s.isalpha():
        break
      i = i + 1
    row = int(position[0:i])
    col = 0
    for x in position.replace(position[0:i], '').upper():
      col = col + ord(x)-64
    if row > self._size or col > self._size:
      raise TypeError("A illegal position " + position + " is given in the restraints.")
    self._restraints[(row-1) * self._size + (col-1)] = value 

  def setRestraints(self, restraints):
    """ The parameter restraints { position:value, ... } defines the given requirement of the Sudoku game.
    e.g. If restraints == [1B:1, 4C:3],
         the 2nd square in the 1st row has the number of 1,
         and the 3rd square in the 4th row has the number of 3."""
    for k in restraints.keys():
      self.setRestraint(restraints[k], k)
  
  def isSolution(self, state):
    """ This function is useless in the class.
    Because there is no need to check if a node with the state in which all squares has a non-zero number is a solution
    Because node are producing according to the rule of Sudoku.
    That is to say, if all squares in the state of the node produced by Node.childNodes() has a non-zero number must be the solution
    """
    size_range = range(self._size)
    sorted_elements = [i+1 for i in size_range]
    # Check if there are only numbers 1 to N in a row
    start = 0
    for i in size_range:
      end = start + self._size
      if sorted(state[start:end-1]) == sorted_elements:
        start = end
      else:
        return False
    # Check if there are only numbers 1 to N in a col
    for i in size_range:
      col = []
      for j in size_range:
        col.append(state[i+j*self._size])
      if sorted(col) != sorted_elements:
        return False
    # Check if the number given beforehand is the same to the number at the corresponding square in the state.
    for k in self.restraints.keys():
      if state[k] != self.restraints[k]:
        return False
    # Check if there are only numbers 1 to N in a set of squares
    start = 0
    for i in size_range:
      subset = []
      for offset_1 in range(self._offset[1]):
        for offset_0 in range(self._offset[0]):
          position = start + offset_0 * self._size + offset_1
          subset.append(state[position])
      start = position
      if sorted(subset) != sorted_elements:
        return False
  
    return True
    

  def isLegal(self, node):
    """ This function is used to prune search tree during producing child nodes.""" 
    state = node.getState()
    position = node.getPosition()
    x, y = divmod(position + 1, self._size)
    size_range = range(self._size)
    
    # No need to check if the number given beforehand is the same to the number at the corresponding square in the state.
    # Because any node is produced according to the number given beforehand.

    # Check if there are only numbers 1 to N in a row
    if y == 0:
      start = (x-1)*self._size
    else:
      start = x * self._size
    end = start + self._size
    if state[start:end].count(state[position]) > 1:
      return False
    # Check if there are only numbers 1 to N in a col
    if y == 0:
      y_m = self._size - 1
    else:
      y_m = y-1
    for i in size_range:
      pos = i * self._size + y_m
      if state[pos] == state[position]:
        if pos != position:
          return False
    # Check if there are only numbers 1 to N in a subset
    if y == 0:
      y = self._size
    else:
      x = x + 1
    i, j = divmod(x, self._offset[0])
    l, m = divmod(y, self._offset[1])
    if j == 0:
      i = i - 1
    if m == 0:
      l = l -1
    start = i * self._offset[0] * self._size + l * self._offset[1]
    subset = []
    for i1 in range(self._offset[1]):
      for j1 in range(self._offset[0]):
        pos = start + j1 * self._size + i1
        if state[pos] == state[position]:
          if pos != position:
            return False
      
    return True
    
  def generateInitialNode(self, method):
    """Generate the initial node with the initial state"""
    return Node([self._size, self._offset[0], self._offset[1], self._restraints, method])
  
  def solve(self, method = 2, test = False):
    """ Solve a Sudoku game using BFS and according to the restraints and size given beforehand.
    Use TREE-SEARCH here, because no cyclical path exists during producing child nodes.
    Return the node's state if a solution is found, otherwise return []."""
    
    # Put the initial node into the frontier list.
    frontier = [self.generateInitialNode(method)]
    
    # Record the amount of generated nodes
    amount_generated_nodes = 1
    discard_generated_nodes = 0
    
    # Show progress rate
    if self._show_progress_rate > 0:
      import time
      start_time = time.clock()
      if self._show_progress_rate > 1:
        depth = frontier[0].getDepth()
        total_squares = self._size*self._size
        left_squares = total_squares - len(self._restraints)
        print("Initial Node has been generated. %d"%left_squares + " squares needed to be given a number.")
      
    while(frontier):
      current_node = frontier.pop(0)
      # Show progress rate
      if self._show_progress_rate > 1:
        current_time = time.clock()
        if current_node.getDepth() != depth:
          print("Putting number into the %d"%current_node.getPosition() + "th square. %d"%left_squares + "/%d"%total_squares + " squares left.")
          print("%d"%amount_generated_nodes + " nodes have been generated. %d"%discard_generated_nodes + " nodes have been discard.")
          print("RunTime: %f"%(current_time - start_time))
          depth = current_node.getDepth()
          left_squares = left_squares - 1

      # if there is any zero term in a node's state, that node must have child nodes regardless of the legality of those child nodes.
      if 0 in current_node.getState():
        child_nodes = current_node.childNodes()
        for ch in child_nodes:
          amount_generated_nodes = amount_generated_nodes + 1
          if self.isLegal(ch):
            frontier.append(ch)
          else:
            discard_generated_nodes = discard_generated_nodes + 1
      else:
        # No Need to Check if a node with the state in which all squares has a non-zero number is a solution
        # Because node are producing according to the rule of Sudoku.
        # That is to say, if all squares in the state of the node produced by Node.childNodes() has a non-zero number, the node must be the solution
        #if self.isSolution(current_node.getState()):
        
        # Show progress rate
        if self._show_progress_rate > 0:
          current_time = time.clock()
          print("Solution was found!")
          s1 = ''
          s0 = ''
          for i in range(self._size):
            for j in range(self._size):
              if i*self._size + j in self._restraints.keys():
                s0 = s0 + "\t%d"%self._restraints[i*self._size + j]
              else:
                s0 = s0 + "\t."
              s1 = s1 + "\t%d"%current_node.getState()[i*self._size+j]
              if (j+1)%self._offset[1] == 0:
                s1 = s1 + "\t"
                s0 = s0 + "\t"
            s1 = s1 + "\n"
            s0 = s0 + "\n"
            if (i+1)%self._offset[0] == 0:
              s1 = s1 + "\n"
              s0 = s0 + "\n"

          print(s0)
          print("Solution is:")
          print(s1)
          print("Total Runtime: %f"%(current_time-start_time) + "s")
          print("Amount of Generated Nodes: %d"%amount_generated_nodes)
          print("Amount of Discarded Nodes: %d"%discard_generated_nodes)
          print("")
        if test == False:
          return current_node.getState()
        else:
          return [current_node.getState(), current_time-start_time, amount_generated_nodes, discard_generated_nodes]

    #show progress rate
    if self._show_progress_rate > 0:
      print("No Solution!")
      print("Amount of Generated Nodes: %d"%amount_generated_nodes)
      print("Amount of Discarded Nodes: %d"%discard_generated_nodes)
      print("")
    return [[], current_time-start_time, amount_generated_nodes, discard_generated_nodes]
  
  def showProgressRate(self, show):
    self._show_progress_rate = show
  
class Node:
  """ A node in a search tree.
  A one-dimensional list is used to represent a node's state.
  e.g. For a Sudoku game having n x n squares, the node
      [ N11, N12, N13, ..., N1n,
        N21,      ...,      N2n,
        ..., 
        Nn1,      ...,      Nnn ]
      represents a state in which
        Nij is the number at the square
        locating at the joint of the i row and j col."""
        

  def __init__(self, number, parent_node = None):
    """ Generate the initial node if no parent_node is given.
    Generate the node according to parent_node and number.
    The parameter number is the number that will be put at the next square, or a list contains the game's size and restraints if no parent_node is given"""
    
    if parent_node == None:
      self._depth = -1
      self._state = []
      self._size = number[0]
      self._offset = [number[1], number[2]]
      for i in range(self._size*self._size):
        self._state.append(0)
      self._action_lists = {}
      self.assignInitialState(number[3], number[4])
    else:
      self._depth = parent_node.getDepth() + 1
      self._state = parent_node.getState()
      self._state[number[1]] = number[0]
      self._size = parent_node._size
      self._action_lists = parent_node._action_lists
  
  def getState(self):
    """ Return the state of the current node"""
    copy = []
    for i in range(len(self._state)):
      copy.append(self._state[i])
    return copy
  
  def getDepth(self):
    """ Return the depth of current path"""
    return self._depth
    
  def getPosition(self):
    """ Return the position of the square which is given a number in the current node"""
    return self._action_lists[self.getDepth()][0]
  
  def getNextPosition(self):
    """ Return the position of the square which will be given a number in the current node's child nodes."""
    if len(self._action_lists) < self.getDepth()+1:
      return None
    else:
      return self._action_lists[self.getDepth()+1][0]
            
  def getNextPossibleValues(self):
    """ Return the possible values of the square which will be given a number in the current node's child nodes."""
    if len(self._action_lists) < self.getDepth()+1:
      return []
    else:
      return self._action_lists[self.getDepth()+1][1]
        
  def assignInitialState(self, restraints, method = 1):
    """ This is used to generate the initial state and action lists when generating the initial node to set the number given beforehand.
    The variable self._action_lists is a list which records every square's initial possible values.
    If method == 1, the program will sort self._action_lists according to the amount of possible numbers in a square, namely use the modification (2) to BFS.
    Else, the program will generate child nodes according to putting numbers into squares from left to right and top to bottom
    """
    for rk in restraints.keys():
      self._state[rk] = restraints[rk]
    
    size_range = range(self._size)
    sorted_elements = [i+1 for i in size_range] 

    for d in range(self._size * self._size):
      if self.getState()[d] == 0:
        values = []
        x, y = divmod(d + 1, self._size)
        if y == 0:
          start = (x-1)*self._size
          y_m = self._size - 1
          y = self._size
        else:
          start = x * self._size
          y_m = y-1
          x = x + 1
        # get all elements in a row
        row = self.getState()[start:(start + self._size)]
        # get all elements in a col
        col = []
        for i in size_range:
          col.append(self.getState()[i * self._size + y_m])
        # get all elements in a subset
        i, j = divmod(x, self._offset[0])
        l, m = divmod(y, self._offset[1])
        if j == 0:
          i = i - 1
        if m == 0:
          l = l - 1
        start2 = i * self._offset[0] * self._size + l * self._offset[1]
        subset = []
        for i1 in range(self._offset[1]):
          for j1 in range(self._offset[0]):
            position2 = start2 + j1 * self._size + i1
            subset.append(self.getState()[position2])
        self._action_lists[d] = list(set(sorted_elements).difference(set(row).union(set(col)).union(set(subset))))
    if method == 1:
      self._action_lists = sorted(self._action_lists.items(), key = lambda k: len(k[1]), reverse = False)
    else:
      self._action_lists = sorted(self._action_lists.items(), key = lambda k: k[0], reverse = False)

  
  def childNodes(self):
    """ Return all the child nodes without the examination of child nodes' legality."""
    child_nodes = []
    for num in self.getNextPossibleValues():
      child_nodes.append(Node([num, self.getNextPosition()], self))
    return child_nodes


    
if __name__ == "__main__":

  print("This is a Sudoku solver written by Pei Xu (#5186611)")
  
  #"""
  solver = SudokuSolver("2x3", \
    {'1A': 1, '1B':5, '1E':4, \
    '2A':2, '2B':4, '2E':5, '2F':6, \
    '3A':4, '3F':3, \
    '4F':4, \
    '5A':6, '5B':3, '5E':2, \
    '6B':2, '6E':3, '6F':1})
  solver.showProgressRate(1)
  solution = solver.solve()
  #"""
  """
  Solution is:
  1 5 6  3 4 2
  2 4 3  1 5 6
  
  4 1 2  5 6 3
  3 6 5  2 1 4
  
  6 3 1  4 2 5
  5 2 4  6 3 1
  
  Total Runtime: 0.003272s
  Amount of Generated Nodes: 107
  Amount of Discard Nodes: 66
  """

  #"""
  solver = SudokuSolver("2x3", \
    {'1E': 4, \
    '2A':5, '2B':6, \
    '3A':3, '3C':2, '3D':6, '3E':5, '3F':4, \
    '4B':4, '4D':2, '4F':3, \
    '5A':4, '5E':6, '5F':5, \
    '6A':1, '6B':5, '6C':6})
  solver.showProgressRate(1)
  solution = solver.solve()
  #"""  
  """
  Solution is:
  2 3 1  5 4 6
  5 6 4  3 2 1
  
  3 1 2  6 5 4
  6 4 5  2 1 3
  
  4 2 3  1 6 5
  1 5 6  4 3 2
  
  Total Runtime: 0.001581s
  Amount of Generated Nodes: 44
  Amount of Discarded Nodes: 21
  """
  
  #"""
  solver = SudokuSolver("3x3", \
    { '1D':8, '1E':4, '1G':6, '1H':5, \
    '2B':8, '2I':9, '3F':5, '3G':2, '3I':1, \
    '4B':3, '4C':4, '4E':7, '4G':5, '4I':6, \
    '5B':6, '5D':2, '5E':5, '5F':1, '5H':3, \
    '6A':5, '6C':9, '6E':6, '6G':7, '6H':2, \
    '7A':1, '7C':8, '7D':5, '8A':6, '8H':4, \
    '9B':5, '9C':2, '9E':8, '9F':6})
  solver.showProgressRate(1)
  solution = solver.solve()
  #"""
  """
  Solution is:
	7	2	1		8	4	9		6	5	3	
	3	8	5		6	1	2		4	7	9	
	9	4	6		7	3	5		2	8	1	

	2	3	4		9	7	8		5	1	6	
	8	6	7		2	5	1		9	3	4	
	5	1	9		4	6	3		7	2	8	

	1	7	8		5	9	4		3	6	2	
	6	9	3		1	2	7		8	4	5	
	4	5	2		3	8	6		1	9	7
	
  Total Runtime: 0.082983s
	Amount of Generated Nodes: 1867
  Amount of Discarded Nodes: 1247
	"""

  """ An example with 100 squares.
  solver = SudokuSolver("2x5", \
    { '1B':6, '1C':4, '1F':5, \
    '2D':5, '2F':4, '2J':9, \
    '3A':5, '3B':9, '3D':8, '3F':3, '3H':4, '3I':7, \
    '4B':2, '4G':5, '4H':10, \
    '5B':10, '5D':1, \
    '6G':7, '6I':4, \
    '7C':5, '7D':9, '7H':3, \
    '8B':1, '8C':7, '8E':3, '8G':2, '8I':9, '8J':10, \
    '9A':2, '9E':7, '9G':10, \
    '10E':8, '10H':2, '10J':7})
  solver.showProgressRate(2)
  solution = solver.solve(1)
  """
  """
  Solution is:
	8	6	4	10 9		5	1	7	2	 3	
	3	7	2	5	 1		4	8	6	10 9	

	5	9	1	8	10		3	6	4	 7 2	
	4	2	3	7	6		  9	5	10 1 8	

	7	10 6 1 4		2	 3 9 8 5	
	9	3	 8 2 5		10 7 1 4 6	

	10 8 5 9 2		7	4	3	6	1	
	6	 1 7 4 3		8	2	5	9	10	

	2	5	9  6 7		1	10 8 3 4	
	1	4	10 3 8		6	9	 2 5 7	

  Total Runtime: 57.976669s
  Amount of Generated Nodes: 1138415
  Amount of Discarded Nodes: 872626
  """
  

def big_data_test(method, difficulty):
  """ This is a function to test 1465 hard sudoku games with 81 squares.
  It will record the time used by the solver and the amount of the nodes generated and discarded."""
  
  hard_data = """4...3.......6..8..........1....5..9..8....6...7.2........1.27..5.3....4.9........
7.8...3.....2.1...5.........4.....263...8.......1...9..9.6....4....7.5...........
7.8...3.....6.1...5.........4.....263...8.......1...9..9.2....4....7.5...........
3.7.4...........918........4.....7.....16.......25..........38..9....5...2.6.....
5..7..6....38...........2..62.4............917............35.8.4.....1......9....
4..7..6....38...........2..62.5............917............43.8.5.....1......9....
.4..1.2.......9.7..1..........43.6..8......5....2.....7.5..8......6..3..9........
7.5.....2...4.1...3.........1.6..4..2...5...........9....37.....8....6...9.....8.
......41.9..3.....3...5.....48..7..........62.1.......6..2....5.7....8......9....
7.5.....2...4.1...3.........1.6..4..2...5...........9....37.....9....8...8.....6.
.8..1......5....3.......4.....6.5.7.89....2.....3.....2.....1.9..67........4.....
8.9...3.....7.1...5.........7.....263...9.......1...4..6.2....4....8.5...........
6.9.....8...7.1...4............6...4.2.....3..3....5...1.5...7.8...9..........2..
......41.9..3.....3...2.....48..7..........52.1.......5..2....6.7....8......9....
1...48....5....9....6...3.....57.2..8.3.........9............4167..........2.....
7.8...3.....6.1...4.........6.....253...8.......1...9..9.5....2....7.4...........
4.3.....2...6.1...8...........5..79.2...3.....1..........84.....9....6...7.....5.
.1.62....5......43....9....7......8...5.....4...1..........36...9....2..8....7...
4.3.....2...6.1...8...........5..97.2...3.....1..........84.....9....6...7.....5.
8.5.....2...9.1...3.........6.7..4..2...5...........6....38.....1....9...4.....7.
....2..4..7...6....1.5.....2......8....3..7..4.9.........6..1.38...9..........5..
8.5.....2...9.1...3.........6.7..4..2...5...........6....38.....4....7...1.....9.
....4...1.3.6.....8........1.9..5.........87....2......7....26.5...94.........3..
3.7..4.2....1..8..9............3..9..5.8......4.6...........5.12...7..........6..
...9.31..6.7....8.2.........5....4......6..2..1.......8...7.......3..5.....4....9
8.5.....2...4.1...3.........6.7..4..2...5...........9....38.....1....7...9.....6.
7.4.....2...8.1...3.........5.6..1..2...4...........9....37.....9....5...8.....6.
7.4.....2...8.1...3.........5.6..1..2...4...........9....37.....8....6...9.....5.
..1.....7...89..........6..26..3.......5...749...........1.4.5.83.............2..
2...4.5...1.....3............6...8.2.7.3.9......1.....4...5.6.....7...9...8......
8.5.....2...9.1...3.........6.7..4..2...5...........6....38.....1....7...4.....9.
.8.....63....4.2............1.8.35..7.....9.....6.....2.9.7...........354........
.9.3...2.....7.5...1.......7.86..4.....9.2...5...........1...634...8.............
...9.31..5.7....8.2.........4....6......5..2..1.......8...7.......6..4.....3....9
5.8.....7...9.1...4............5...4.6.....3..9....6...2.3...1.7...8..........2..
.......71.2.8........5.3...7.9.6.......2..8..1.........3...25..6...1..4..........
......41.6..3.....3...2.....49..8..........52.1.......5..6....7.8....9......3....
5..6.3....2....98.......1...1..9.......3....67.......4....8.25.4..7..............
......41.9..3.....3...5.....48..7..........52.1.......6..2....5.7....8......9....
7.4.....2...8.1...3.........5.6..1..2...4...........5....37.....9....6...8.....9.
4.35...2.....16...7............895.....3..8..2...........4...7..9....6...1.......
.5.4.9......6....12.....3..7.3...2.....5...9.1.........68....4.....8........7....
......41.9..2.....3...5.....48..7..........62.1.......6..5....3.7....8......9....
5.7....3.....61...1.8......62..4.......7...8...........1....6.43..5...........2..
7.....48....6.1..........2....3..6.52...8..............53.....1.6.1.........4.7..
6..1...8..53.............4....8...6..9....7....24.........7.3.9....2.5..1........
...9.3.5.2.....7............59..1......4..6...43......4..67...........91....2....
.6..5.4.3.2.1...........7..4.3...6..7..5........2.........8..5.6...4...........1.
6.9.....8...3.1...4............6...4.2.....3..7....5...1.5...7.8...9..........2..
4.3.....2...7.1...9...........5..18.2...3.....8..........94.....7....6...6.....5.
8.5.....2...4.1...3.........6.7..4..2...5...........6....38.....9....7...1.....9.
....3..715..4.2............2..6..4...38.7..............7..8..1.6..5..2...........
4.3.....2...7.1...9...........5..81.2...3.....8..........94.....7....6...6.....5.
.......91.7..3....82..........1.5...3.....7.....9.......16...5...4.2....7.....8..
48.3............71.2.......7.5....6....2..8.............1.76...3.....4......5....
7.8.2...........913.........46..........3.7.....5......5.9.6......4...1.2.....8..
..36......4.....8.9.....7..86.4...........1.5.2.......5...17...1...9...........2.
2.8.5.......7...4.3........5...2.9.......1......6......7.1.4.6.......3.2.1.......
8.5.....2...9.1...3.........6.7..4..2...5...........6....38.....4....6...9.....7.
4.35...2.....61...7............895.....3..8..2...........4...7..9....6...1.......
...3.9.7.8..4.....1........2..5..6...3.....4.....1....5.....8......2.1.....7....9
.5.1.8.7.4..3.....2.........1.7...8.9.....4............3.....1.....4.2......5.6..
.....1..8.9....3..2........5......84.7.63.......9.....1.4....5.....7.6.....2.....
85.....7.....41...3..........1...4.6.7.5...........2..742.6.......8...3..........
..3...67.5.....3...4.......6..3......8......4...7....12......5.....98.......41...
.4.3............78.......5.7..65....5...9.....1....2.....1.43..8.......6...2.....
....3...27..4......3.....9..6..2....8.....7........1..4..7.1......6...35.....8...
4.3.....2...6.1...8...........5..79.2...3.....7..........84.....9....6...1.....5.
3..8.1....5....6.9......4..5..7...8..4..6...........2.2..3.........9.1....7......
4.3.....2...6.1...8...........5..97.2...3.....7..........84.....9....6...1.....5.
4.1.6....3.....2........8..15.2.....6......1....9......2.7.8..........43.7.......
26.7...........4.15........839.........5...6....1......7.....2.....49.......3.8..
42.....36....3.8...........7.8.1...........54..3.......5.4.6...1.....7.....2.....
...6.37...51...........2.......1..846..7............5.14.58....3.....2...........
.6..7.......8...2..1.............6.54..3...........7..2...6..4.8.31.........5.1..
..1.....8...9..2.......3.......15.4..6....7..3............4..8572.6.....9........
7.....4...2..7..8...3..8..9...5..3...6..2..9...1..7..6...3..9...3..4..6...9..1..5
5.6...3.....8.1...2.........9..6.7...4.7...........2.....1...493...5...........8.
3.7..4.2....1..5..9............3..9..5.8......4.6...........8.12...7..........6..
...6..1.....2...4..59......6.......47....9.......5..8....1..7.6.82............3..
2...6...8.743.........2....62......1...4..5..8...........5..34......1..........7.
.......92.37.......4.......8...6.1.......43.......9...2...5...6...1..74....8.....
7.....48....6.1..........2....3..6.52...8..............63.....1.5.1.........4.7..
56..2......3...9...............7..561......2...84........3.84..71..........9.....
......41.9..3.....3...2.....48..7..........62.1.......5..2....6.7....8......9....
...6.37...51...........2.......1..546..7............8.14.58....3.....2...........
3..4.1....9....7...........6.41.........7.2.9......5......3..8.52..........8...6.
7...3........5.6....4....9.2.....7.1...9.8......4.....53....2.....1...8..6.......
...3..5...5..1..3...7..4..12.....4...6..9......1..6..28..7..2...9..8..5...5..9..7
6.....7.5.3.8................52.3.8.1.9.........4.....42...........9.1......7.6..
......41.9..3.....3...5.....48..7..........52.1.......6..2....5.7....8......3....
...6..9.23.87.....4............95..17......8...........2..6.5.....4...3..1.......
1.37....5...6.4...8...........81.....9....7...6.....9..2....4..5...3...........2.
.4.7...6...39............57.......3.2...8.....19...57.6...4.....5.1......2...6.84
26.7...........4.15........839.........5...6....1......7.....2.....43.......9.8..
4.21......5.....78...3......7..5...6......1.....4.........67.5.2.....4..3........
3..1...6...1.47.......5....68.3...........4.1.2.......4.5...7.....2...8..........
6.1....3....8..2..9.........47...5......7........6.....8.5.2...3.......1...4...9.
.6..2...1...3...7..1.......3.49.....7.....2........5.8....586.........4.9........
8.5.....2...4.1...3.........6.7..4..2...5...........6....38.....1....9...9.....7.
.2.....8.....4.6......1.....3.2.74..1.....5.....8.....2..3...7.4.5......6........
....7..438.....5...........2..5.1..........64...8......34...6.....2..1...7..6....
.2.3...6.....7.5...1.......7.86..4.....9.2...5...........1...394...8.............
5.3.9..........7.12........4...2..5..1.8......6.7........4.86.........3.9........
5.3.9..........8.12........4...2..5..1.8......6.7........4.76.........3.9........
.2.3...6.....7.5...1.......7.86..4.....9.2...5...........1...934...8.............
......31.7..5.....2...4.....39..8..........62.1.......5..6....7.8....9......5....
...7....6.29.......1....3..7..56..........24....8.....4......35....91...8........
......31.6..5.....2...4.....39..8..........42.1.......5..6....7.8....9......5....
......12....3..6.....8.9.......2..6.3.8......7...5.....15...4.....7....9.4.......
..9.7........4.6....1....8....1.9.3.54..........8......5....7.62..3...........2..
1..46...5.2....7......9.....3.7.8..........91...2........3..84.6........5........
5..2..3......8..9...2..4..66..1..9...1.....4...7..3..87..3..4...9..7..2...5..6..9
4.9...5.....8....27..3.........4.7...8.....6..1..........6..12.5...9...........3.
.5..7..83..4....6.....5....83.6........9..1...........5.7...4.....3.2...1........
..1....8....2..5.....6.........41.3.62....7..........927.8.........3...45........
.894............72.3.......1....5.6..4....9......1....5...6...7...3..8..2........
...6..9.23.87.....4............59..17......8...........2..6.5.....4...3..1.......
7..63...........81....2....685..1......7..6...4..........8.4.5.2.....3...........
69....2.....7...4............73.4...5.....6.1...8........5..83.2...9........1....
8.5.....2...9.1...3.........6.7..4..2...5...........1....38.....9....7...4.....6.
...7....2.8....1...9.......7.6....3.....91...2............5.84.3..6........4..5..
69....2.....7...4............73.4...5.....9.1...8........5..83.2...6........1....
56....4....72.................3...7861...............2....461..1...5......8....3.
4..6..3...1..2..6...8..7..19..8..5...4..5..1......2..75.....6...3..8..4......9..5
7..69..........35.......1..2.9.....7...3...4.8.........4.5..6......28....1.......
46.....29....3.5...........1.5.4...........723.........7.6.2.....4...1.....9.....
.5.7.1...2.8....6...........4.3..5..9.2......6...8.....7.1..3......2..9..........
.135.........7.4...........1......892.4.6....7.........8.1.....6.....2.....9.3...
5..4..8......9..1...2..1..56..3..4...5..7......4.....83..6..7...6.....8...8..2..1
...4.5.2.81..............7.3...9.1....5....4...........6..1.8....27........2..9..
.1..3..6.8..................63.9....7..8..4......1.5...9.....1.2..7........5..7..
3..4.6....9....7...........6.41.........7.2.9......5......3..8.52..........8...1.
..9.2........4.6....1....8....1.9.3.54..........8......5....7.67..3...........2..
...8...3...5...7.....1.........5.9..18.......3..4.......7..2..6....7.5...4.....1.
2.7.4.......6...3.9........4...2.8.......5......3......6.1.3.5.......2.9.1.......
1...6........2.7...53........98...........41.......6.742..........3.9......5...8.
.1.65..4.8.......9.......3.15........76..........28......7..5..3..4...........2..
.7.3...6.....8.5...1.......8.96..4.....1.2...5...........7...324...9.............
.6..2...1...3...7..1.......3.49.....7.....2........5.8....856.........4.9........
8.......24...3........5..1...1...56.......9.....7........8.4..7.6....3...9.2.....
.2.....9.....1.6..7...3....5.7...1.....2.4.8....9.....64.8.....3.....5...........
3..4...8.....5.2...........152.......7..1.......9...6..15...7..6..3.4............
..8.17......5...3..........54.....2.63...........76.....6...8.72..4...........1..
.2.....9.....1.3..7...4....6.7...1.....2.5.8....9.....45.8.....3.....6...........
.2.....74.98.1.............7..3.5..6....2.9..1..............83....6.7......4.....
6.....8.5.3.9................52.3.9.1.7.........4.....42...........8.1......7.6..
...46..8.7.....9.....1.....4....53...8.6......2.......3.9.7...........215........
8.5.....2...9.1...3.........6.7..4..2...5...........6....38.....4....7...9.....1.
6.81..........72.............3.5..615....4..........8.47....5.....63.....2.......
.71..8...5......2...............68.14...3..........7.....45..3..16.........2.....
7..4......5....3........1..368..........2..5....7........5...7213...8...6........
.9.....2...5..4.......61.....6...1.8...3...7.......6..23.9.........8.4..7........
......41.7..3.....3...5.....49..8..........52.1.......2..6....7.8....9......7....
17.32...........51....8....5.6..1......7..3..4...........5.4.6..8....2...........
12......9.5..9.2.3........4.3.........18.........246......67.5...2.41.7.9........
.8.....2...5..4.......61.....6...1.7...9...3.......6..23.8.........7.4..9........
9.....7.1.2.4...........5..7.1..5....8.....3.............82..4.1.9.........39....
8...3.....2......6....5.7..5.1...9.....2.4......6.....7.....39....1...8..4.......
63.2............857.........91.........8...4....7..6..2.....3......1...4....95...
1..5.3....7.....84...6.....5..1....2.2.....4..........6.....5......7.3....8.2....
.9.3...6.....7.5...1.......7.86..4.....9.2...5...........1...324...8.............
4.....26..3..7.................8..536.1...8..........7...6.41...5.....8....2.....
...8....2.9....6...1.......8.7....3.....61...2............5.94.3..7........4..5..
...6..2.18.39.....5.........7..2.....6....4.....5...8.....41..79...............3.
.64...9..1..2..................493..7......5.....56......5...17.43..............2
...6.9.3.8.1.........7......6.5...7.....1.4......2....2.....5.4...3..8...9.......
.3..4.......5...9.9......2..6....8..5..7..........1...7.21.........8.3.6......4..
.8..9....3......6....3...4.....1...5..2...9....7...8..65....1.....2.7........4...
.8..51......6...2...........3....8.55.74...........1..4.6....7.....35...2........
.3.6..7......25....1.......2.9....8....4...3.5........8..79..........4.6......1..
1...4........2.5...63........98...........45.......7.172..........3.9......6...8.
6...3.....2......7....5.8..3.1...9.....2.4......7.....8.....59....1...6..4.......
...7..2.18.39.....5.........4..6.....7....1.....5...8.....42..69...............3.
58..3...........219........76.2......4....8......9.5.....4.1.7.3...........6.....
..1....8....2..5.....6.........14.3.62....7..........927.8.........3...45........
3..4.9....8....6...........4.91.........6.2.8......5......3..7.52..........7...1.
1...9..6..5.....4..6..3.......5.7..28..4.....9.........732...........8........1..
8.75.........9.6..4.........6....2.95..7........4..3...3..2......1....8........1.
8..5..4......2..9..........5..3..1...76.........4.........69.241.....3......7....
5..7.........3..7...8..5..36..1..4...8..2..9...9..8..1...4..3...6..9..4...2..6..9
......8...7..9..1...3..7..51..6......5..2..4...8..9..74.....2...6..1..5......6..3
7.2...4.....8.96.....5......8....5..3...1........4..7.1......32...6......9.......
.19.6....2.....7...........3..4.1..........91....5..6....2.34...51.........7.....
63.2............857.........91.........8...4....7..6..2.....3......1...4....59...
6.2...7.....8.95.....4......8....4..3...7........3..1.1......26...5......9.......
6.....3...5..9..8...2..6..98.....7...7..5..4......1..51..3..5...4..2..6...8..7..2
1.....54....9......7..........6.7..9..82.....4.3......62...........1..5.....3.8..
..84...3....3.....9....157479...8........7..514.....2...9.6...2.5....4......9..56
2...4.3......1..75.........8..3.9..........54...2......15...6.....8..9...7.......
...3...1..92.......4...........28.........7.3...5...6....79.4..8.....25.1........
.19....5.4..2..................91.......5..6.7.....3.....3..4.7.61............2..
.342...5.....87....1.........24...3..5....2..6...........3....12.....7..8........
63.2............857.........91.........8...4....7..6..2.....3......5...4....19...
36.1...5.....4.29......7...61............94..8..........2.5.......8....6........3
.2.8..3.....7.....9............6.74..3.2......1.....5.4.5.9..........8.16........
2..7..1......5..9...1..4..3......8......4..6...9..6..27..5..6...5..7..3...6..3..1
2.65....8....413..9............5.73.8..6...............7....4.....2.9....1.......
8.5.....2...9.1...3.........6.7..4..2...5...........6....38.....9....7...4.....1.
6..1..7......7..8...9..8..37..4..5...3.....2...4..5..81..2..4.........5...6..9...
3..5..1...7.....8...8..4..66..4..9...3..6..5...7..1..48..1..3......2..6...2..9...
.1.4.9.........32....7.........56..48...3..........7.95.....8..2......6....1.....
12.4.........8...37....6...........8.....2.45..59...6..1...4.9..7....8..96..1..2.
......94.....9...53....5.7..8.4..1..463...........7.8.8..7.....7......28.5.26....
.......4...2..4..1.7..5..9...3..7....4..6....6..1..8...2....1..85.9...6.....8...3
....3..7..2....8...1.......3...6.2..2..1..5..7.4......6......4....2.5......8.....
53..2.9...24.3..5...9..........1.827...7.........981.............64....91.2.5.43.
1.83..........72..3..6.....642.5...........61.7........5....4.....8...3..........
.8..4....3......1........2...5...4.69..1..8..2...........3.9....6....5.....2.....
1.27...8.....56...3............9.7.4...2.....8...........1...3..9....5...6....4..
2..4......7....6.....5....1...8...2583..9.................6.37.4.1............9..
3.2....4..7..85.............9..6.8.....2...3....1..........95.72..4.....1........
5.4....6.....21...3........27..9...8...5...3...........1....7.96..4...........2..
....28.7.4.1...........5......1..4.6.2..7..........3..6..34.....8.2...5..........
....8.4..4.......7..69....3.......7...7..62.5.9...2..1..3....5..8..14......32..1.
1..........6.....3.8....4.1...6785.4...9........5..76...2......59.814......3..9..
.2..5...9..618..73............5....8...938....1.....6...1....2......4....973..4..
5.2....4.....81...6............3.7..4..5............9..97...3.....2...6..1....8..
24.7.........5...6..........59...3.....1.8....6.......3.....27.8.....14.....9....
5...7........4.6....3....9.2.....7.1...9.8......3.....42....5.....1...8..6.......
5.....3.....1...2....4.6.........5.8.6.2...........9...1.....499...3....8...9....
...1..5..4......6..........6.2.4....5.....8.37.........315..........7.2..5.8.....
.2.41.....8...7.3..........7.5....6....18....3...........6..4.16....5.........2..
....7.94..7..9...53....5.7..874..1..463.8.........7.8.8..7.....7......28.5.268...
.4.5.....8...9..3..76.2.....146..........9..7.....36....1..4.5..6......3..71..2..
..14.7...5.....6.....8.....4.86...7.....2.3...........63..5...........41.2.......
2.4...8.....3.4.............3.5.7...6.....4.2...1......1.....5.8...9........6..7.
.2.4....94..189.......62.5......63..3..94.5.......8.1..........8.2..4...964.....7
6..9..4...4..5..3...8..6..55..7..3...7..2......2..5..41..6.........3..8...6..2..1
4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......
....5...11......7..6.....8......4.....9.1.3.....596.2..8..62..7..7......3.5.7.2..
9..7..3...5..2..1...7.....93..6..7...6..5..3...2..8..61..4..6...4..6..8...6..3..4
.2.8....51.....93............84..2......1........6....61.....7....2.5..43........
.2..5.6.8...7..4.....1.3....6..4....3......5........1.7..3.5.........2......8....
..3......4.6.......8.231..62...9..715.......8....4...3....7...........9...1.68..7
2...9...8...4..7..6.........4.3.7..........92...1.....5...6..........31....5.8...
...3..16..27.........9......48.2.......6..9......8........74.2.3.....5..1........
..1...5.....2.9......8..3..53..4...........726.........2.1...894...3.............
..1...8.....6.4.......3.......72....4......5..9.....3.6.....2.1...8..7..31.......
.......2...43...965....21..1.....7........432....5..1..6.........597...8.9.68....
..345..8..........7.9.31...24...7.....8..9..5....1..2..7....29.8..........2...6.4
...3..18..26.........9......47.2.......5..9......7........64.2.3.....5..1........
52...6.........7.13...........4..8..6......5...........418.........3..2...87.....
2..5..6...9.....3...1..9..44..9..7...5..4..8...7..1..6...1..3...2..7..9...8..3..5
6.....8.3.4.7.................5.4.7.3..2.....1.6.......2.....5.....8.6......1....
9.4..5...25.6..1..31......8.7...9...4..26......147....7.......2...3..8.6.4.....9.
..9..63...72..........17..51..3..9..........86.84....1.6.........1.2....9.3...45.
..24............98..8..16...5....826....4.7..7..8...5...167....3...92.....9......
...85......5..6.1..6.....5..3......147.9............26.9.6.38...8...1.9...3......
......6894......7.....26...2...6.34...49..8.2...........87.5....6.83......7......
.5.3.7.4.1.........3.......5.8.3.61....8..5.9.6..1........4...6...6927....2...9..
.2......6....41.....78....1......7....37.....6..412....1..74..5..8.5..7......39..
.175..6.....4....3.6....5..8.4....2.....51...3............6.7..2..8..............
2.6.9...........847.........8.4......15...........76..9.....2.....3....5...1...3.
.2.4...5......6..44.....91.8.........3.7.4...27.8.3.....95.1.2.5....2.3........8.
.2......5...7...4....3.9....8..62...3..4...7..............5.8.64.1............2..
1..4.8....5....7...........4.63.........7.59........2....8....16.......3.9..2....
.2.4....94..18........62.5......63..3..94.5.......8.1..........8.2..4...964.....7
.2....4..7.......6..8..7.....3..89.........42.541.........6....5....93.....34..81
..8.9.1...6.5...2......6....3.1.7.5.........9..4...3...5....2...7...3.8.2..7....4
..6..3....97..513..2..91.8........7.6.........41.....9...5..8.....3.47....4.16..5
1.....9...64..1.7..7..4.......3.....3.89..5....7....2.....6.7.9.....4.1....129.3.
...9...612.7...3.....8....54.9....5.....5...9.7.6..........314.3.......6.1...2...
...3..18..26.........5......47.2.......1..3......7........64.2.9.....5..1........
.....7.95.....1...86..2.....2..73..85......6...3..49..3.5...41724................
.237....68...6.59.9.....7......4.97.3.7.96..2.........5..47.........2....8.......
24....6......9...8......7..419...5.....3.2......4.....3......4.6..7............1.
....62.9...9.....52.....4.1...8..1.6.9.5...7.1...3......76....83...2.6...1...3...
38.6.......9.......2..3.51......5....3..1..6....4......17.5..8.......9.......7.32
49..6..53.......7.1.6............2..9....4.1...7..5.8..3.7.8....1..9........2.4..
.2.4....94..18.......36..5......63..3..94.5.......8.1........4.8.2......96......7
...5...........5.697.....2...48.2...25.1...3..8..3.........4.7..13.5..9..2...31..
6....38......2...7..95.....96.18....7.........8.....49.........3.2.95...1..6..2.5
.6.........3..15...9.8...716....2.3....75...4....9...82.1.....6..6.......8.5...4.
...2.5......1..7...3......45.17............83....6....1.....25.....4.8...6.......
12.....8.4.......2..9..35.....9.8....7..2..5...1..42......65..7.......61..83.....
.26..4.......3..8........7..97...5.....28.......1..........56.93.....4..1........
...9...86......5......5...1.2......47.85...9.4..36....2....3....4.69..7.67..1.4..
..3.4..1....192......3....7..4.6....5...34..2.8.9.........7...67......58.29....3.
1...5.......2.1.....3.7..6.........962......7.8593.....3..6..8..7....1..5....4.7.
.6.5.1.9.1...9..539....7....4.8...7.......5.8.817.5.3.....5.2............76..8...
2.....9.....3...7....7....69.5.2...........481............1.5...46.......3.8.....
...2.13...7.....9.5........4...9..8.8.....1.....3..2..9...7..5...16..............
.47.2....8....1....3....9.2.....5...6..81..5.....4.....7....3.4...9...1.4..27.8..
....8...7.......5.9..6.1...2.6..4.9.......1.....9..3.64.8.5....6...7.8....23.....
2.....9.....4...7....7....69.5.2...........831............1.5...36.......4.8.....
.27..46..8...9.....5......154.........1.....82...3.91....6...7......2.....28.7.46
....5......913.8..1.6.2.....9......673.9........4....14.............36........352
.52..68.......7.2.......6....48..9..2..41......1.....8..61..38.....9...63..6..1.9
1..53..7..48.........2.........681..3.......2.....1....1....4..5..7...........6..
.98.1....2......6.............3.2.5..84.........6.........4.8.93..5...........1..
.3....2......8........1......7....8..2.5........2..3..1.8....749.....5.......56..
.........9......84.623...5....6...453...1...6...9...7....1.....4.5..2....3.8....9
6.2.5.........4.3..........43...8....1....2........7..5..27...........81...6.....
...8....9.873...4.6..7.......85..97...........43..75.......3....3...145.4....2..1
.26.39......6....19.....7.......4..9.5....2....85.....3..2..9..4....762.........4
1....67.........32..921......4..58..87......69...6...........5..4.138.........4.3
.5..9......12.......6..73.8....2...4...98...53.....91.7.....6...4.8..1..1.8.7....
1.....6........4.8...3.....9..7...2.....8.5..........7.68.4.....45..9..........3.
....1.78.5....9..........4..2..........6....3.74.8.........3..2.8..4..1.6..5.....
....2.7.84.1............9..3..4.1.5..7....2.....6.....6..5......8..9...........3.
........7.2..854..8.5..92.....1.867.....4....7.....3.8..9.1...23......1..6..5....
......7.1..4....3..85....6.6..9.1....1...7..5....3.2...2...8.5.8.1.29....6..7....
....5..6..752.....9.........1...85...3...7..8.....9.433.....6......1.8.478...5...
1.......3.6.3..7...7...5..121.7...9...7........8.1..2....8.64....9.2..6....4.....
.2.3.......6..8.9.83.5........2...8.7.9..5........6..4.......1...1...4.22..7..8.9
.2..........6....3.74.8.........3..2.8..4..1.6..5.........1.78.5....9..........4.
...36....85.......9.4..8........68.........17..9..45...1.5...6.4....9..2.....3...
....75....1..2.....4...3...5.....3.2...8...1.......6.....1..48.2........7........
.....3.879....5...6......4..827.......9....643...9.8......7..1....5......43..1..6
5.1.94....2.6.59................2.17.3..4..6.......5.........2.....3.8...6.8.93..
4......6....94..5.1.9.6...............6..2..5.5231...8.7...8..1......7....8.5.3.6
2....1.9..1..3.7..9..8...2.......85..6.4.........7...3.2.3...6....5.....1.9...2.5
.1.6...8.3.2..........49.....83...........4.7......5..46..........2...9.7...5....
8.2.....4.9......7..5..139..8..17......5.2..1.....8.36..71.....4...7....32...5...
..79..1....36..7..45........2...3.8....8......4..51.3.....9...25.4....1..8...4..6
....7.8..8.5....97...5......1..9.....2...5.3.7....3...2...6.9.......4..246...87..
.1.....8....75.....39...6........8.6.9..2.4..6.1....9.......2....2149.381...3....
.6.....7.2...5....7..12.9....2.....8.18...3...7..9..5.4..9.2......6..1......85..3
.4.3..9...7...5.2.8........6.....352..5....9...4...6.....9....8....42.7..9.16....
........92...6.5...5.72..4.87....6.11.....9.8.......5..4..........612.....3.5....
2..7........68..57.8...3.6.....1....3..4.....6.2....9........7...9...8.5.4.53...6
........5.7..8..3.9...25........9..669..7..5.....1.8.7.8.2.7....61.3....3.....4..
..9.....76..2..8.....3.59.....61..2..64......9..........1.4..8....5..4..8.3.....6
1..4..........2.3..7..8....5..7....86....5..9.4...6.......3.......9..1.5.97..8.63
.2....16.....7.5......1.......6.8.4.3..2.....1.5......5.....7.3...4......8.......
34.6.......7.......2..8.57......5....7..1..2....4......36.2..1.......9.......7.82
1.3..7.89.....93.7.8............34....4..5......6..2.834.....6.....9....8..7....4
1...6......5..31...6...8..97.85...4....4..25......2.......9.3.2..1........3...714
6.2.5.........3.4..........43...8....1....2........7..5..27...........81...6.....
......5...4.......5...37..2.8...64....9..2..8.6...17....36..8.9..78........1.....
.29.46...1..9..3.44..7.....5.......2..8.2..7..4........3..7...17....49....683....
...3...1..14.27........5..6653...1.747.......1......8......49.58......2....5.....
....14....3....2...7..........9...3.6.1.............8.2.....1.4....5.6.....7.8...
1......4..47....3.....5.7...8..7..9......3..6..1..95.4..82....9.........2..517...
.923.........8.1...........1.7.4...........658.........6.5.2...4.....7.....9.....
8..........5.6....37.2...1.6..9..5...5.....36...1..4........7......27.8..2438....
72........6......8..89...4.....8...63....7.2..9..3.4......4...727...3.......5.91.
2..6.34..17.....9............64....59...................53..6...8..7..1.....1....
.524.........7.1..............8.2...3.....6...9.5.....1.6.3...........897........
.2.......3.5.62..9.68...3...5..........64.8.2..47..9....3.....1.....6...17.43....
.6..31...5....2..9...4......2...9..1...6..8..7.5.......3..6.4.....3.....2.1.....5
..7..8.....6.2.3...3......9.1..5..6.....1.....7.9....2........4.83..4...26....51.
......52..8.4......3...9...5.1...6..2..7........3.....6...1..........7.4.......3.
8......21..1..95.6.....53...7.4...6.....7...9..2.9....3.86.....1.5.............42
.2...48...54...6..9.......1...5.7.68....3.1...8...2...3.........7.9.8.52....7....
.2.....74.....6.8...6.4.9..3..........98.....5...19....1.5...32.4.2........4....1
...658.....4......12............96.7...3..5....2.8...3..19..8..3.6.....4....473..
....15.6..3...4.7....8...593...7...6......21.4....1...92..........59.7..8.5..3...
.7.6..3..8.......6..2....9...5.67.....8..1..946..8......9.4..........2.7...2.8..3
8.7..6..2....5....4.....9......2..67..1..4.....63.9..47...6..8...9..2....3....5..
7.8.....4.65.7.....4..5..9.....1..52...8....3..6..49......85.2..7.3....5...2..1..
.29...6....87...2........5...59..3...4..12..6...4.7.....6..9..1.....84...5.....6.
..2..583.7...2...........4...12.7.........9...8.1.34...9.8.....6...5...8.3.7....6
63.8...1..97.............3....1....61...5.....4...6...5..2....1..4...9.73....748.
3...6.1..65.29............881..7.5....43..9....5..2..7...43..9......7..64.....8..
1..........4..1.9..6..8......3.7.8.......51..7..1..........3..8..5..497.4.685..1.
..8..5...3...9......73......216...8......2..35....94.2......6....57..81.4.......7
..2..9..7..6....3.5.......9..9.126...8..4..9.2.......1.....39.5...785.....3....4.
...5.36.2.3.69..5..5.7.....7.9..2....1....9...8.9..........63....1....675..37..1.
1...7........49...9.6.8..3.....9...7.2....5....846.12..618.....3.......8..5.....2
1..6......7.3.9.4...4.7...2.1.7....9.37...2..5.......6.....59....2.3....78..1....
1......8..7...8.3.....5147.5.......6.4...7...21...4.......9......6.2.....8....7..
9..4.1....3........6.3..7.12.......6.....71....8...45...9..48.....9...123..2..6..
9..3....41...2...5..2...3.12..6.9..36.9.5.............48.9...7........4....81....
15..7..........94..8............8.256..2.....3...........9..3....46......7......1
1....759..7..9......64........8.....63.....4..9.54.3.232......4...9...8....1.4..7
..6.3.521...7.....9.3....4...7...6.......4....1.5.27........973.....5.....8.1....
...75........48.2.3.......6..6........1....74.5.4.21...7....3..9....5.18.2.9.....
...4...26.7...9...28.5.....8..3....79......8.....9..64...7..1....6.....2..3.15...
....8.61..53............5.2...4......2..58..74..7.9.5.964..........2.86.3.....7..
.4.2....8..1.5..4.2..8..7....8....97...6..3...957............6.7.4.1...2.....31..
..4..8......7..624...........2...9..6.3....5.7...24....5.3...7..9......8....1.2.5
..3..2.6.9..3.1...1.2.5..8.........2..5..3.98...4..1....7.....5.2..6....4.19.....
.691.7..8..2.....6.8....1.....7...32.9...8.....63..8...7...4.......5..4.5....6...
.46....9...3..4.......6......7.3..4....8...1.5..1..2....1.7.8.9..5.1...7.3.9.....
...58.6......2....974.......16...8...4.9...7.5............6...8.5.4...1...2.9.4..
.8.65...2.9...7....1.3....87......43...4..5..5....1.....2.9.3..9......2...42...6.
.3.......8.5...4.19....1.6....93..1......6.2..4.....76....1...27..8.......135....
...8.......43..8..7.....19..5.....7.3..24......8..9..3.29...........1.2...1..24.9
.....6.5.3..1..86....9..4.34....81...7.3....4.9...1.....5..3...9.8.6..........2.5
15...3......4.9.3.3...8.....3.1..7.65.4..8.......7............24......516....2.9.
.5..9....1.....6.....3.8.....8.4...9514.......3....2..........4.8...6..77..15..6.
....98.........71.2.1...4.......6...8..47....6.7..1..31..5......3....86...4...19.
....4.87..61..................6...312...7....4.........5.1.8...7.....2.....3.....
...3............81.52..9..67.9...1.....4...5....8.6.2.2.8.5..9..952.4.....1......
1.46.5.8.8.62..................6.7..6....7.1...91..2...5.4....3...91...4..8.....2
..23.....85..4....97.5.1...4.....89..2.91...3.....4..6......5.9.....5.1...7.3...8
....147..6.9......3...........6.1.3..5.8............1....93.8...4......2......5..
......8.17..2........5.6......7...5..1....3...8.......5......2..3..8....6...4....
......8.16..2........7.5......6...2..1....3...8.......2......7..4..8....5...3....
..13......6.....2.34..9....4..9..7....946...52..1........6.3..1.....8.5.6.8...4..
1.....7.2.3.1......9..........39..6.5.8...2...........2....85.....6...9.....4....
..61......7...356..9...2....8..7..2........5....5.43..4.....79.1....84.......5..6
..3...78...6..9...7.......5..7.....3....2..9......421.5..3....68....2...9..5.....
...5.1....9....8...6.......4.1..........7..9........3.8.....1.5...2..4.....36....
.2.........678.1.......2.....1..5..4....4....9..32.6.5........8..7....3..6.2.3957
..26..8......1.4...5.....3......5.....1...7.4.6..382....7..6.............982..56.
......8.16..2........7.5......6...2..1....3...8.......2......7..3..8....5...4....
.7.81....9...7....3..4....8..5...43..6...12.....9....7......6.2.8....75....524...
9.24.15....4..8......2................53.71..3...1.46...7.....4.89...32.5..6.....
1.........2......59.68.........3....6.....4.9.7..296.......59.....1..7.683......4
........3.9.6.4.......1.28.....6...173....6...5.4...7...5...7..3.91.....6..97...2
8..4.6....3.2..4...4..5..78.69..5.2.3...........6...1752.....3......36.......2..9
3.6.7...........518.........1.4.5...7.....6.....2......2.....4.....8.3.....5.....
.5.....47....8..2..2......64..35..7..65.9.4...38.........51.6.......9..4..9.7...2
..47.....3...45.....7...6..9..236.7..5.....8...2..........18.27...9..1..7.......3
..35...8.8....1.7.......3.12...1.....7..249..6....7...3.2..6..845...8.........46.
2.5..6....9..7.8....6.5.2....2......98....57....1....4.2.6.8...5...4.7........13.
....6.4..5.83......9.........1....873...5.2.......3.4..6.5........84..7.2....6..9
....1..594...5.8...5.7........59..8..1.2.3....34........38...........6.7.729...1.
...4..5...7...3.....421..6..3..8.1..8..7....695.3........9....1.6.....2...3..6.84
6...4...3.1.....7...5...8.....5.2...3...9...2...1.......8...9...7.....5.2...3...4
5....3......5..29.....7..8...57......46..132...93..8....7...9....4..9..6....6..4.
.5....46.....9......3.8.2......51.....134.58..46.........1.....4.....8.97......1.
.4............12....568..7..57.....3.985..........9.65....42.8.......7....3....5.
...37..5..27.........8..39.....8.......2...4.893......64..31..8.5............65..
.5..4.8...6.5....9...............1.....23...7..1..7..2..4.9.....376....5..87...2.
..5..8..18......9.......78....4.....64....9......53..2.6.........138..5....9.714.
....854.6...2.....9....32....1.7...46....9.5..93..4..8..5.......6..1...747.6.....
.397.4....71............6.....3.5.4.8...2.........69...165...9.....4..6.2....8...
..........72.6.1....51...82.8...13..4.........37.9..1.....238..5.4..9.........79.
1...7...8.4.6.......5..1.......3.95...9.....2.....4.1...1.9.6...52...8..7..2.3...
..57..9.....8....4.1.....2.4....2....6318.........376.95.........854.3.......6.8.
....74....6.29......73....12.....7....8.2..4559....8...3....98.....83......1...2.
82......7..4.1.........9.5.......39..1.45....2.8.3.....7...4..6.....5...1..2..84.
.6..2...3...........3...4.5...8..7.2.1...4...8..23..9..4...3.5.78......19...8.2..
........1...2.9.8..4.....7.8...9..3.9...3..642..1.6......68.5..1....53...75......
2..7.34..18.....6............34....56...................53..7...9..8..1.....1....
15.3......7..4.2....4.72.....8.........9..1.8.1..8.79......38...........6....7423
.9.....2.8..2..........1..8..9..45...5.6..7..6.4.8...........5.2.68....3...14...9
.2.456..9..6......7.9..........1..9....938..2..5..2..4.6.2..8..5.2....3..1.......
..2......1..49.2.5.4.....9..8...14....63....75......6.6...8.3.....7..1.63......5.
7..3.6..4..54....7.4.....3.6....5....14....25......1......8.9..8792..5.......3...
58........4...52.8...9.2...9....3.65...49..2.....5...1...36.....54...7..6........
.2.....9..65.2..4.9.4.....5..6.5.......17....54.....18.....2....59...8..7...4...3
...4.7..6....2.34..5.3...8...5....7..2...8...7.....1....4.5.2.....9....3.61.....7
.....89..8.65....2...32....21.83...7.3..1......5........1.7..2....6....957......4
......1........2.568...4.....3..........73...9..6....1..29..5..1...8.7..49.1....6
249.6...3.3....2..8.......5.....6......2......1..4.82..9.5..7....4.....1.7...3...
..123.........7..16.8..49.....32...4.....5.9.8...7...6..45.....91....6....3....2.
8..6....29.........71...8..765......2....5.7.....6..9..13.4.........64.7....8....
.3..8....8.75...62......4..2...6..945...1...7..92......2.6..7.......3...6.8.5.1..
..3.1..7.....4.1.8.....2.6....8....1.753..6......7.9..8.....4...4.18....6.7......
....6..8...3...2.69....5.....2518.9..14......7....3...2........4...9.1....9..7..5
9....8......9.6..22....3..8......78.5..8.7..6..76..1..6....9..5.1....4...4.......
.32.....58..3.....9.428...1...4...39...6...5.....1.....2...67.8.....4....95....6.
..6..43.....3...7..1...7.4....9....536....1.8.2........9..86.....7......5....12..
.....9.8.8..3....2.675.......27..6...3..45.1.....1...5..1....9...5..71..49.......
1..6.......7.9.4.19.3.5..7...15....93.4.....2.....7.3...5....2...........2.94..13
..2...9..9....6..18..4...3.....6..5..3...82........3.7.2.9..1..6.1.5.....7...4...
.........6.1...9..3..24..1..5...6.....978...........87...5.7...2....43.......36.4
2.4..9.........8.16..7........2...6..8..3.....5.....9....4..7..3.....5..1........
.2..6.4.......5.8....7...3.3.8..9.........2.157........4..1.......2.....8........
..4...23.....72.........1.62.3......1...86..3...7.4.......6..9..9........6..485..
...5....6..4.6...7.7.4..2..12..8....5...9163......3..2..29....5.......6.8....6...
.........4...19........5..1.3.8.....1.5....7...8..62........32..83..2.9...67...4.
1....786...7..8.1.8..2....9........24...1......9..5...6.8..........5.9.......93.4
.8.7..2..19.........5.98..1.4.9..7.2..7..2.4.6.........1.8..5..3...5...6.....93..
.6.....7.9...8...6..3..91....8.95....2.4...6....21.8....5...6..3...4...8.4.....2.
.3........7.6.19...4.....2.2..8.6.....9...1......5....4....2..5.....8.1.....1.734
2....48...95..7.3....6.........1.....43.....5.6.3.84..47.2..5....6.......2....69.
.8..3..6.9..6..4.7....9...5..5.......627.......9....84.2.....7.4...7...3...2.1...
694....1..2..7.9........25.......48.4.1...52......8..39..4......6.7.5.....3.8....
1..7..6...4..9......74.32.....1.............7..5.3841.2.3.4..5.......3.6.79......
......4.18..2........6.7......8...6..4....3...1.......6......2..5..1....7...3....
7956..8.......1....2.3.....2......5.......7.8.46.7.9.....1.......2..5..9854.2....
5..2....9......12.1..8.47...6.5.7..1.5......8....8.2...2.34....6.1.......7..18...
2.3.....75...7..987..4....5.....67......9.1....73.8..91.6....2.3...5.....5...2...
....6...9.7.2..........1.8..1..2....4....7.5272..59....41......5..9...2669.7....5
....2.4.3...1..7...85......3..7........4...1..6...........18...4.3.........6...5.
4...1..8...9.2..5.1.......2.3.9.8..7..5.........63......6...4....1.832..7....6..8
1...8.5...5....24.....24.31..583....6......7....16...23..45.6....8.1.....9.......
.5.3.2........16..8..5...7..7....3.....95...2...2.37.9.4...58..6..82....78.......
.....3...8..2..67..6.......51...2.4.......3..47.5....87..4..8....2.1....6..3..4.5
.......71.2.8........4.3...7...6..5....2..3..9........6...7.....8....4......5....
3...9...8.2.6..5.9.......4.8.423........5...7.....12...8614...........7.15...9.6.
.6.3.......15.....7....1.38..7....9.52..8.1.........56.7..4.6..4..6....5.5..9..2.
..3....9.8...21..6.5........6.25.74.....73..55.....2..2....7.8....49.1...9.5.....
..2....7...4.5.....7...8..1..6..5.8..4.1..2..5.9............9.7.3..278.....54....
....7...56.1.92....95.6....8.......3.6........3..4.7...5.....1...2.5..78...4.95..
......8.17..2........5.6......7...5..1....3...8.......5......2..4..8....6...3....
1......9..65..9......63...22.6.47..5..835..2.........4..9...1.8...9.....75....4..
6.73.........8..2..2...79....1...4..4..........3.5...8.7.1..38..4.63...7...8...9.
5....3.8....4.1...4....7..3....8..64.9....23.2...7....95.......3...4.7....7..8..9
...213....6...9.8........9.5.84......7...8...3.......5..1...7..2...6...1..5.3.46.
....4...1.54.....9...2.1..8....9...3.2.3......8345..........6.5.6..8..9.7..6...8.
9..51...35..3..2....8..2...7.....5.8.96...31....8...9.3.5.7.6.....1.........3..85
.5.4.....8.3..1...9..5...8...6.3..9..9.65.........2..3.2.1..7..6.....8.5....4.2..
.3.4...81....9...5.6...84..5......1...19...4..8.1.7.53..8.3.......6..7.......4.9.
..3...6.......1.9..7..5.....18....5..2..7.1..6.9....72...83..1....2.....4...673..
..3....1.....94...9...2.......7..6.345..............8..96...2.....5..4.....1.....
...4783....7..329..3....4..2...5......68......14....2..93......7...2..1....6....5
9.16....2.8.....4...3.2.5........2....51....6...87...........3..189.......6..59..
1...9..3...2..3.5.7..8.......3..7...9.........48...6...2..........14..79...7.68..
.9...1....8..4.....1.8.2..7..3..7.6.........4...46.71...51...32.....5..62.....9..
.6.........428........31..5....4.39...79....2..8..27....6.2..1948.......7..5.....
.4...9..3...5.79...68.....77...3.....85.2.......9...1..54..3....194....8......3..
.139.....7...........24..1......1...48..6.........39.6.........2.5...74..6...489.
..2...4..9.563.8..........6....6........73.9...8.15...7.63...5.8......4.3...2.1..
...7.....12.....84....8.....945.....3....2..67....45........16.6.1..73.5....5...7
....8...2.7..2....13.5..7.....1.25...4..6....5..9....3......3.9.19.5.4....7....6.
....6...79.3....2....7....1.465......8...2...5.9..4....9...3.4...8....12..5.7.3..
8....4..197.....8...438.9......4...26..2..8.3..5...6...............1..59..189..3.
.3...8.1.42..........9.......9..26.....75.........1.38174...2..2......85.....6..4
.23.....7.6...1....7.6...5...63.4.....8...5......9.2..3....5..9..94...3........4.
.2.7...9...4....71..5.6......9.73...3...56.1........4..1......86....8....9...2..4
.1....63......3...8....5..9...4.7.6..4.....1.....9...51...28...7.8.5...2..21.....
..8.....3.....58..5....2..46.......99...781...1.....3.175.........3.........9.67.
..6......35..1.....17..3.5......9.4..2.35...8...2..6.........9.672.....3.8....7.6
...487....5.9.......7...2..2.1..4.9...4...6.3.9...5...3......2...87...3..6..1.8..
......8....9..852.4...9.......5...6.1..6.4..37....2....63.............39......1.7
2..1....54....9.8......276.....3....51....4.9..6....7...1..5.......7.8..728......
1...6..8..73.....6.6.35.......8.57........1...9..36...4...8.....39..7..2..5...9..
.63...9....78.6...84...1........52.35..1.........74.9..2....8.6.8..5..3.4.......2
896.4..........7.2...9...6..18..9.246..3...8..3..1.......4..2..3....6.....5.3..1.
6......1...7.......5..83.2.....4.3....28.6....7.....5......91....8235.......1...4
......3..6....1.....8.9....4........15.67..4...72...5..4.7...25....6.7...8...5.9.
4....52.....3.....2.......85.8..1..4...7..6...4.....811....9....5..2..1...31...57
4.....7....68....59..72..1....26.....4.5....9.....1....85.....3.....3...7.....8.4
2..3....53...591......7.4..5....8...7.1.4.......2...6.......2.4..5.....889...3...
.3.8....5.....6.49..5.2...79..........4.5....6..1...32..2..7...........3.....41.8
.1...7......85.9....3.....4.2..4....75.96....1....8.2...62............3......57.8
..2...68...3....2..74.82......4.5.9.3.......5..8.7.1.3............897..2....245..
8...1.7......4....4.1..95....2...8.....9.......3.86.9...8.........6.3....7.5...36
8........95..6......6.894..3.8....1.5.4...8.7.1....6....527.3......3..72........4
5...6..........583..3.9.4..6...4.1.....71.....7...2....5...1.2.4..5..6...89......
.23..6.....67....3.8....5......9.......8...4....2379.55..9..3.2.....2..8.7.....5.
.......8..72.....1..6.9...7.4..15.3.5........6..27.........81...98...37......3..5
42..5.73.........48.7...2......6.......941..5.5....1......8..2..1...3..9.75....1.
..1245.6..2.......9..7.....4.7.6..1....5...........9.3...1.6..2.......74.58......
......5.88..651...9..2..3...4.7..9.5....2....5.1.4.....1.56.8.9..3............61.
........5.4.....7..761.43...85.6...........51.6.2.......2.....9...4.8.....37...1.
.1..5.3.......4.7....6...2.2.7..9.........8.146........3..8.......1.....7........
..7....35.1..4..8....3..1..5....18..........2.26...4......8....8..765.9..7.139...
6..3.2....5.....1..........7.26............543.........8.15........4.2........7..
1..3.6.8...6..7...9.5.4....2.3...6..5...2.8...4..........4....9...7.....6...1.2.5
.2....5938..5..46.94..6...8..2.3.....6..8.73.7..2.........4.38..7....6..........5
.....837..7.....2.461..........9..8..1...6..3635.8.........3..7...6....9.2..49...
8...2.1.......9....651...2....5....3.3..61....874......1.24.3......169.4......7..
1.25...78.4...........81...........9.8.....136....7...2..6.89.54...2......9.13.2.
..76.23..9..........6793....6.3..5..7.5...8....4....2.....167..........4..35.72..
..4.8...6.......5..5.6.184..1......8..9..4.3.7...3.......24.98..6..5.......1..6..
..24...5.8.....2...6......1.1..47.....6.5..2.......7.6....9......81.5.3.79..3....
....81.7..3........2...9..1...4.5..........27..8.9.5....1.5.6....9.....446......3
....7.9.6..5..9.4.9....8.7...9...6..87.....2...6..3......1........4.6..25.3.....8
8...3............6....6258.5..9...1.....7.9.3..9...26.4....9.5..9....8..2.58.....
1.25..6..8.5....2.......5...1.....68..817..4..4.6.3......43..7......94...9..1....
..54......4..8.7.......3..5..3.26.891...........3.7.2...9.4...3.......6..2.5....8
..43.7.........3......8.2.141.6...9...9.3.5..7....9..8.6.....5.3.....1..5...1...7
..3....9..5.2.......7361.........71.4....8.......3...6...5..83..85.2....2...14...
..3....8.9.....62....9......8.4....6.4...37..2.5..7.....8.3.........5.1...7..84..
..1.2......3....4....71....2....6..8.4....3...8.2......3..6....1..8.4.7.8...7.5.9
....7...6...3..97...5.62.8.3.....7.1..45.........9..........8..7..8...23..9.4....
......8...2.7.9...9....871.8.4........6.4...55....3.6..7.5.....3....6..2...9....1
......25..7....8...28....19..12.89..3...9........1...6.624.7......32.7.......1...
85.....4..6.5....3.2...87...1....4.........697...9.5..3..9.....4...17.2....2..3..
1.....3.8.7.4..............2.3.1...........958.........5.6...7.....8.2...4.......
.6..8....1..9..2..85...1.....91.26.3.7.564..........7....4..........67.5....198..
.5......37..6...2....1.3.....4.8..1.1.7..2.6.9.........8......9......45.6...9....
85..3.....3....5.61..2.......91....85..7.8.......4....6..9.7.5..2.....1.....2..7.
4.2....5..8.7..1..1..9......9.6....8..5..12......2..7...9.3..4..3......6......8..
4...5...9..3...8.....1.9........4.......8.29.15.6...7.8.6....4.5.......3..9.4.78.
2....35....7....4..6.97...........62...42....9.58.....3.9...2.......18..4..7.....
.5......88..2.3.....3..1.4.23...4.5.6.....7....8.9......654..8...7...1.........3.
.....69...2....6.....75..24..4.....9..2..3.6.59........8....7...5..1...81...39...
3..7...2...8.4...9....5...1..24.....5...3.4.......8.3...46.....9..2.3....1.....67
.6....83..25....1.....16.....7.6....8..4.57.3.......8...2...19..5...8...4....7...
.56.....7...1...92.....7....6..2...1.7...98..3......4.13..........68.5.4......9..
......4.17..2........8.6......7...2..4....3...1.......2......8..5..1....6...3....
57..8.4.........3...32..1.5...4.8........5...2.7.....19.1.....4.8.7.9.....2....6.
.6..51....2...8..1...7..28......61.27.9..........4..3..8.....2.4.5...7.....3..6..
.32..........2..4.9.7..5....1...3.98...2..6...68.1..2....53....57......3....471..
...6.28.........7.14...56...6.2.......7..3.5.....1.29...3..7.......4..359........
...3...86..76..1......5...4..6.1....5.4...3.2.9..4.7..2...3.6....1..54..43...9...
....2.68.9..3.........6.3...9...6..7.1....8..3.6..8.2......5...4.2.1.9...8.9...7.
.....1..8..4..765..5..6.39..13...7...7..3..8.46.7.5........6..9..29........85....
3.2.8...6....9.7.8.5.....2.78..4...9..4.......1...2...1...7.....4...637.5..4...9.
13....6.9...2..54........7..........62..8.7.47.9.461....1.3........15...49.8.....
1..64.....7.......9.4.....1....6..79.3..7...4.4..583...5....9...........4.629.5..
1.....9....27........34.62..1..5.7....7.....359..7...8..1....6..4.......7..6.93..
1.........4..59....653....42..6...47.7..4...6.....58.......3.2...2..7..5......61.
.64.2.........1...8..7...3....13..7...8..2..17....59.....4..5..3.......91...6..8.
..8.5..6....7...83.5............524.8..6....9.7.....1...23.....6...9..7...4..2...
.......76.....51..2..3..9..93..2...1.2....36.7.4...........1..8.5.96.....9..4.7..
9...182....5.......7.93.....29..3.8.3..6..7.27............9....1.73.2..6..8..6..5
17...4...3..6..7..25.....4......58........4......3..155..7...2.....96...7..3.1.9.
1.64....5....2.......3.6.8....2..8...8.9.713...4.....9......59.47.......5..1.3..2
.4.7.1....1.....9...9.8.7..5.6....3.1....6.......2.8....8.....4.5..3..2..7.5....9
....2....9.6.7...88......4.....6.4..6.......9.124...3....3...8...8....71....589..
......1.2...4.....8...3..5.3...895.........7..1.6.......3..8.....25.6..9.6.97...4
.5.9.86....4......3...6.8........7....683.......7.2..12..5..9...9...1..6.......35
.1.....9......4....6..8.2....3.92.5..2.8...1.6...1.4........5......39...2...5186.
..6...5....3..4...2...7.4....93...7....46....8....23...7..9..2....5...161........
..4.8.1......13....5.4....6.......2.....67..3.98....452......7....3....28.6...4..
..5........3.8...4...1..7.56.1......8..4.3..2....1..4.5.8....9..1.7..6......29...
..34........7...3.7....15.62....8..7...94..........9..6.....25.8.53.2..1...6....8
7..3...6.....1...4.3...52......649..9.61........8.......3.2..5.2......1..154...7.
1..46..7...7.....496.....8...6..38...4..1........2..3.........2.8.9..5..7.5..2...
..6..1...8.3..91...9......7...2...5....1..4...3..468.12.9..4.3....5.....65..3..1.
..5.32.....9..1..34........6.....2..2....5.84..7...1..8...6...7.1...85.2.......4.
4..8.......724.....2.....7.25...96...3.75.....4......9.....5........159....9..26.
.8...4.5....7..3............1..85...6.....2......4....3.26............417........
.7.....358..9..4..3...2........1.5.....4.8....6..3..8...........5....1739...42...
.2.4.5........9.......3.28....3....93..8.47..4....652...1......64.9....27.....3..
..4..23..85..6.4..........1.8.7...6......5.8...3.4.......5...7...1..62...9..2....
...1..5......26...4.3..........7.643.65.............8.3..8........4..2...1.......
.....3.1....8.7..28..6...............69...7...2...8.6...43.29....17....43.89.....
39.6.......2.......4..3.85......5....6..1..9....4......15.6..3.......7.......7.82
375.9.2..2....13..1.............572..8...7..1.63...........2...9.4....5....8...7.
.2...3..48..7..39...7....61..3.7...8..6..213.5.........4.8....6..8.1..2..5...9...
..82.4..16...5...9..1...........37..8..6..2....5..2.3.........3.54....7.2..9.5..8
..2..8.7.86.....2..7....3...1.6792....8.......4.....5....1....9....5.46...7.63...
...9.2.....8....753..4..9....5.83....7.......61.2.......1..7.64...8..3.....6...9.
.....3.1...2..68......5.4...2....6..6..4.7.3.1.7.......4....7..9.6...2..5..9....8
4.5.....9.3.......9..1..57......836.1..3.........7..92....9..2.749......5...6...8
2.....3.4.....1.8.3........7..36......4....9.....2.....8.9......5....2.....7..6..
1.....7.9.4...72..8.........7..1..6.3.......5.6..4..2.........8..53...7.7.2....46
.9.8....3..6.7.1..5......4...........79...6.5.1...2.8....2...1....3..9..642..1...
.5...4...7..3....2..49.2..1....617....7.....554...3.1..2.....8.69....3....1......
.3....4..........21..45..9...976..3...8......6...1...74.2.37.......9...6...1...5.
..92....4.....1..3.6.8..52.7..........39.....58..3.94...41.....65....8.......5...
..9.....3.....9...7.....5.6..65..4.....3......28......3..75.6..6...........12.3.8
..248....9....65......9..7...98.54...........5....31.....6..83..28..471...7......
..2......8.13..6.......7..4.1.9..........48.......6.75.24.9.3...6.........9.5...8
....8.....915...3.36.....4..1......623.1.94....5...........6.91....4.2....73.....
.....73.2.6.35...9.8.....4.72......6.19.....4.....52.....51....8...32.....4.7.9..
.....729.......3..9.46....52.....7...3...89.....75.....6.............4..57...2..8
8.4..926..7...2...9..6...475.9..7...4.......3...2..9.....93.854.....8............
62.......4...5.1.7..57.....8..3....6....873.........98.6.....3..7.21..4.1....4...
.65.1....7..4.5........6.13..6....7..2..9..8.5....7.3...4..2...........18....492.
.3..7..9...24....1....8.......6...7...8..5....4...85.6..1...3.93.6....1...712....
.2...........53..9...12.58.9......36....8..1....2..7..7.8..6...3.9.....5.4.....6.
..4...1...6.2..7..5..8.....8..9...3...7.1.9.........4..36.4........7965.....8....
..1.875...34..26..9...5....8.......4.....186.....7.9...8.......2..6......1......2
...9...7.9.5..4..3.3....2...9..7..6...715....1...8.....6....42.8...97..........3.
....43..2..12..6....7..5..8........43......16....52.89.4........853....79.2..7...
.......1.2316....99......7..2..9.......4.1..61..2..5....8......3...8.9..64.9....2
1.2....97...4.....9....13.....2....8.3.84...27....5.......5...........1.4876.....
.7....6...8.3..........62.3...........1...39.....954.22...5..8.51.4.....6....7...
...6.3...74.....1......59.....34...119....7.42...5......1...2...2..6..7....5...6.
....9......3.2.....7..419...2..8.1.......6.5.6......7..4...2.1...15...63......8..
2...4.8.....1..3......98.4..9...34...8..6...9..1.8.....457....1..........6....53.
1..74...69...8...2...3..5..6...9...7..8...15............1...7..4..2......5..643..
..7....9.5...2..7..4679.8..693..1......8...6.........5..167.........8.2.......4.7
..34........7...3.7....15.62....8..7...94..........9..6.....25.8.5..2..1...6....8
...1..3....4.5..8.2....9..554........9...3.....27...1.....68.....73...64.......52
.....8.294..7.........2.1..85.3..7..6......91.1......85.....4...9...3.....765....
7....46.8....6..5..5..38.........8.75.1.47.....9.1........721.642..............3.
6...7.8...9.5.....4....1....5...86.....2..........6.29.3..2..9........4.24.3.9..1
4..7231..1...8.........9....52....7..7....3.58.............648..13...2.....2...53
1.2....9.......5..9......2......6....2....8...8.4.5.6.2.153.4..37.1.4.....56..3..
.682....7.........1..6.89..23...9.4......5.....43..7..3...1..8.......3...9..8..62
.2..914....86....13....7...8....6.7..1.72...4......6..6..9..5....4....8..3.......
..8..5......23....9.24......6.........9.4..578.3.7..1.3......7....5...26.....84..
..6.2.5....3.....4...745.2.....91....4.28......1..7....1......2.5.8..7....2....48
..3.7..6.8..35..........3.127.9..8...9...8.....5...61..1.....4.........27...641..
..3......8......959....42....1..394..6...........75..35..4...8.6....7.....9....1.
....7.9....2..1.5.....6..8.5.......963.........9....16.5.9.76..3....4...4...8.1.2
....7.84..8.....3......2..6.1.4.8..9..86......56.1...874.........9..1.........357
....6..87..9.......31.7.2....6.98.4.1.....7....87....6..4.....2...5.3...32.......
....1.....9.2.87.6.....685...54.....6.43...7..89...5...........3....728..4.1.....
.....1.3.86.........3.....9..56....3.2.51.89..9......6.....4.71....5..2..197.....
...........5.9.17..3...2..84..........94..3...7.86...4..7..8...2.......1..19...56
1...7956.8....2.............61..79..3..1.........6.4....2.9....6.9...14....8...2.
.8....2.9.......6...31..78...56.3...6..4.7....3..8..7.92....53...4...9......2...6
..3.8.95.8...9.......7.3..1.3.....46..8.4..2.7....25....26.4......9..3..59.......
..3.2..7.8..5..9.......7.8.7......93....4.7....6.1.8....7..5.3...12..5..5..1.....
......9...3.2.....8.....4.1.....689...3.47..27....2...5...3.....9.6......7...46.8
......4....5.7..1....3.2..7.6..8......9..5....1....2.9........84..6.....3.79...65
4.27.......7..1.....1.5........7.2.3.....4...6..8..5......1.479.9......5..62...8.
2...8.61..7....4...5..2....4..13.....9.........2..7..93...9...8..7..2......5..1..
1.....3.8.6.4..............2.3.1...........758.........7.5...6.....8.2...4.......
.6......5..7..4.8.....9.2...2.5...3..8......7..43....15...8.4......71...6.......9
.5.6..1......35...67...84..2.....8.......3.1.....7..5......4.6...9.1.3....2.....4
.2...6.....758......5....34..8.....3..1735.8....9........8..........175.2....3.1.
...39.....8...6......14.7..1.....47....5....69...2..8..5....3..32..8...47.1......
....12...6..9...3..1.8...761...8...75.93...4.......8....1..5..8.........794....5.
.....17..5.72.....4...6...23.4....1.......8..2.6.4...5..5....6....3.9..1.4..2..8.
......3..36.........85...79....8..57..........2...4163..9....4.4..8.2...2..4.1...
45.....3....8.1....9...........5..9.2..7.....8.........1..4..........7.2...6..8..
4..6......73.8.......2...9....8..2.3.35.....18....4.7..1..........5.....9...1..48
1.3.....9..6.......8....54.....49..36......2....1...5...89..2.4..73....1.4.......
1..2.37......8...5.....412........7..93.1......6..8...3.2..6.....1.3..8.68..5.3..
.9.5.2.7...84.........1...6..1.7.5.48..6......3.......1....6..5..2...4...5.9...32
.6.....7.87.3..59...54..2....9.564.....9...8.2.78.....7....4..2..8...71.........9
59..2..4....9......4..68......1...72..8...4...1......6..92.3...7......3.25...7...
.75..6..4....7..9.4....1...5....8..6.....9..5..32.........9..1....1..2...48....7.
.672......2...........7.9.5...75.8.9....4..7..8.31..........54.3..8....2..1..3...
.6.......1...93...5...8.46.4...1......8..6.3...6..5.2....74.9............2..68..7
.5.4....8..6....9..4...3..........39..5...8.6..985.....2...4.1.6..1.......8.....2
.2..7.93.........87......5.8....4...3..1...6.....9.1..49.8....5.....3....56..2...
..9..6.1..7...13...3...2....5..6.8....1........7...65.9...23.6......954...4.8...3
..7.....2..149.5..6......1....38..2.......4..73...98..48...7...9....3.....5.....6
.......5...4.3.8......917...9..7...83..5.....8.6..3.4...3......54.7.....9.....62.
7.2.1.....5...4.....92..58.6....82.....7.....1.5.....65....93..........48.7..2.6.
3...5...91.5..3.6..46......41.....5...3..871........4.6...7.........5.31..82.....
.8...57......1.....2...71.3.3.84..5.....3..49..2..........6.....41.7...58......7.
.4...6.5.....8..94.1..3...7283..5.........5......17...4.....2......7...86..3...4.
..3.5.4..7...6.....5.8...6.5....3..4.1..7..8.2..4....7.4...8.5.....4...9..6.1.2..
..3.......6.7.9..1...6......16...8.9.......24.98......5....2.6....5.4.3...9..32..
..27....49.....7...1...6.5...5..........4.2.7..36879..3..5...7......4...859..2...
..2..9....6..31....7.65.4...1.3.....5.......7..8.2...9..19......8..7..95......3.4
...5.3..........62......97.5..4...........19.78..1....2.16....84...753.......2...
...5..94..5.6...8...4.9.3..3...7.1..4........297......6..95...25..2...1..2..8....
...5...6...7..14..2...3...............1.29.7.52.....18..48.73..98..4.............
.....17.....6....3.6.4.95.1.2.......3.9.7.......56.....1..4.6.........8.7.2.....9
.........2..1....7.3.5..1....57..2....9...........2.465....6.93..2.376....8......
8.5.....1.1....7.......1...2..46.9...8.........6.5.2..3..7.6..46......2..243...9.
65.48..12...5......4...35....6..8.......2549.7...9...6.....7.2..69......8...3....
3...8.......7....51..............36...2..4....7...........6.13..452...........8..
.3...4......8..562.........6.......9..1..7..6....2..4...41.2.87.13......8...6.2..
.2.......8.6.9..7.9..35........6...9.7..1.68.........53.1..4.....21.....78...631.
..7..3568.6..1874............64..8.......7..9..485.3.....12....2.......4.53......
..68.3......6....51.2...........13.69....5......9....75.....2..6..1....4.8.74....
..4.....3...7.1....76.....1..2.........9....8.8.2...5.25.8...9..6...7.4......3...
..2..56...47..1........8.2..1.....49.84....32..9...............3..95..1.....125.3
...3.8....4......6..6...5.......12...8..4......3..7.9.1....4..8...51.6....2....7.
....5..2....61...92....3..88......74..3.......1....9...96..57.....9.....4....83..
......5..87.5.4.9..3..9.....6..5...9.8....746.........4.1....2....4..1.7...8.....
1.....68.....6.2...652.1....1.49.8.7........4..7......5..7....8..893....7....2.3.
.4..2......7.8....1..65.....24..3.1...9....48.5..9.7..........5..6...8919......76
.23..4....76.25..1...7...8..1..6.7....91...62.....2...3.....8..5....9..4.9.....1.
.19...6.........8..7.25..4.3........9.6.......2.937.....28...9....4.9..1....6...3
..7..1..9.3......2.....24....4..5..8...4...1..8913..5..1..6.............7.59...8.
..5..91.......36...2....943.......6....7...81.1..9.2..5.7.1...2..8........3.6.8..
..3.8.......5.....7.84...3.8.9..6..74..7...6.......1...32...54.5....367.........9
...4.86.387..3.......5......163....73.82..5.......6....21....68..5...7.......3..4
9.6.....8.4.8....9.....67...9.......83..5...2..1..75......153.....4.2.1.4........
83.....5....9.1...5....72...8.4...97...5....4....1.6....8......67...2.4.3....5.1.
3.51..........7...49...2.7.5..........648..........78.......5...2...9..3...86.4..
15......2......63..8......13.4.69...7...23............2...7..9....8..7........34.
.2.5.9.4...5.....19.4.6.3.....695.....6..8...4.......2.3.7...1.....3...67.8......
..2.....51...23.8.9..7....1....3..52..6.....8.9.1..6..7.8.695.........3..4..57...
...4...1.42......3..1.6...9..5......2.6..7.......5.7...8..9....7..14....59.6...2.
....8.3.425.1...9......3....4..2..3...6.9.8..7..31...9.......8.6.2....53..4..29..
....1.....16..7.9..5..2..6......94.....7......42.....528......3..5.6....3..4..8..
........43...6..9..857..6.........4..9...25..1.2.....9.....4..34.75.8.....6.1....
7....2..1...15..8.3........1..94.6.2..4.1..7...78......7..........2...699....3.1.
35.6.......4.......2..7.89......5....7..1..2....4......36.9..1.......5.......7.82
.3..6......4.5...7.5.7...8......1.........7..3.....465.1...7..4..581.....7....29.
..3...4.....53.68.81......2.......544..8....3..9....7.7...6.....4...52.8.2...9...
..2.4.3.86....2.4...8...7..5.......7......9....4371..5...91....4.32...8..6.......
..1.......6......73...6.89.8....93...3.4..2..2..8.5......1....4.2..4.........8526
....7..9......8..4.42..1.7...4.....88..2.5..95.....7...7.6..13.2..8......6..3....
.....1...9.468...1..6.3...7......6..6....9..44.25...83...8...4.3..19...........78
.......8....78.2....4...6.12.5...13.........9..91.3..6..19....45..........365....
.........2.6.5..4..5...43......4.....7.56.9....9.28.6.6......213.7....85....8....
5..3...8.........9.79.28...1......7.....3..2..8..69.5.8....2....46.......9....4.7
5......9.21...67....63..........1.5.9...........97.346..8.3...1.....8......4..52.
.92.6.5..8....54.6....98.....5..16...786....36..........9.4.....6..13..2.......3.
.5.......8....1.2.9..6....1.1..3...6...2...48.....6.39.....58..4.....6....6.73...
.2....5......6.34.9..3.....2..........91...64..7.9..1..31.78....4...5.........43.
..8..........6.784...73.9...9...7...6..1........9..45.5.7.......2.....19..12..3..
..7...4....61......23.5...7..2.....581....2.....6...1....4...........34...8.327..
....8...1..............947.4.9...76.6.......33.....1...8.7.......4.16.3..1...4.27
....584..8.473...2.5....7..3.5.7..6..46.1.....9...........8.6.....9...73...1...29
96......8....47.......8..63...178...4....21...7.....5.7...2..45..9..4....3...59..
.8...4.2.35..9....7.......5..8..3..7...4...8..9.....12.2.1.5..46.18..........6.7.
.7..1.8.....8...91.....6..2..2.....8...46....7....5...8.3...4..9...3....1......57
.12...6.....8.7......3.....73....4......2...9......5..4..53....8......3........1.
..43...5...38..2....8...7.....5.........3..4.7...2...1....756..9..1...8.5.....4..
...4...25.....1.8..2..9..7.7.....3..6.3.......8..37.5..9.2.....4..1..8......78.9.
87.........53.6..1...2.9...68.......7..1..84....9.......1..42.52.....43..........
84...9..1....8.2......7..4...1..4....83....6...9.....4...7...3..1.8....5.2..3.4..
7.6...42.8.......7......93....2.5.6442........6..8.2.....5.6.....31.4.....5.7..9.
621......9......4....51..........9.7.7...94....2...65..4..7.......1...852..36....
.9..2....6..1...........3.5...91..2.17.8...4...24.....71.....6.85.3...7..2..8....
.7....4.......2...2.6....98..3...5......8.....419....2...23..6......7..9.3.4.5...
.3.4...6..2...14.9..46.....5.....1..6....895...8..7..4..98...........81.3...4...5
.2....9......164..3..94......23...8..............79..6.918..7...3...5.6...5.....3
.1.........5...9..2...8...5...6...7..4.3...1.5.9..1..8....2.4..1..8.3.6......7...
...46....568......3....1....3....96..956........7...4..8.94.3......7..2.1.....89.
8..7.............45..9...2.....63...9.1..5.3...51..........72.3.38...6....25...79
2.9.......8....7...7...15..41.....3..9...2......7....8...6..3.....87..1.....39.4.
1...8...3.534...2.9..........72..16.5......9...1.....7...64........1.2....5.72..8
...2.49...4.....5...37....88...1..64...3..5...9..8..........74..15......6......2.
....716.46.72..8............7..5.........6.2..1.....3..4......2....8.3...58..9..1
9.1...2..5..78..4.........57...4..3.1.8..95.....5....2.4...6......2....12.7.....3
4...7.1....19.46.5.....1......7....2..2.3....847..6....14...8.6.2....3..6...9....
..6..48..47..3....2.3.1...532...8..7....5.6....7.....4...2...9.......4..1.....3.6
..1.935..2..4.5..8........984..7......68......3......4......9..6.8..9....2....173
...39..72.......95.7...53..............1..2....7.48.1..69....5..3...98..5.87...4.
....5...1.8.9...6.....8.7.....765..3.2.......6......18..6.1....3..27.5.4..4......
.......9.....3..51.7..418...13...4......5...37.8....2...1.64....9......2...5.....
3..5..1.....1..5..1.....329..86.............724........2...3.....5..9.8...9..8.6.
14......6..7...93...3........5.7..9.3..41.5...9.8......2...86.......785....1....4
.836.........7..4...........6.1.8..........27...3.....4.2.5....7.....8........1..
.52.......6...9...9...8..53.1.7.2.3.....3.1.7..8....4.....7.89......6.....5.....2
.2..8...7..6..9.......5.48...3....4.5...6.2..67.1....3..14.........17....8.....6.
.2..8......7..9..1.4......52....8..9...16.....785.....3..4.69....9.1...2.......6.
..6.5..9.1..6......5...1.8.2....31....5.....27.9.6....4..3....7...4...3...1..5...
..5....6..3.6.7...1.2.....34.......6.....98...8..3.....2.....78....1..5...39...4.
6...1..2..1.36..5...7..8...4......19...7..4......34....6..2....12.....4..5.....63
49.6..........4.8........5....2...1.....167.2.7...3....689.......25..6..3.......7
37.6.......4.......5..8.19......5....9..1..3....4......85.3..7.......6.......7.42
1..3..5..5..9......6....4.8.4..7..2..32....5...5............8.6....43.......597..
1.....4...65.7..9...7....63..19.......4..5...5..1..83.....9...6.3...7..2...8.6...
.96....73....76.4.......8...6..........5.4...5..281.........1..2.......8.7.94..3.
.3..7...4....25.......9..3.87.......14....6.......4..1......3...89....2...2689...
..4..3...8...9..6......8..1.135.......9...5.7.....6.1..6.72..59...3..1...7...92..
..1.8...7...1.5..3.5.6.9.1.16..2..8.......6....5...7.....8..2....9.57...84.......
...5.........7.1.3...1.3.74..2.6...95....4....74....1..5.8..6.......9.25...3...9.
.....7.....8...5..1...4987.2....46..4.9.2.7.38........7.3....1....6.1.......9....
..........6....312....85.7..57..3..69...1.2...3.......6...9.8..3....17...9...7..1
93......1.67....2.8.....3...2..7....6...3.9......2.46.4..6......9..5...3.....4...
.9...71....8...26........5...6..3..27.1.95......6......738.........4...66.2...7..
.6...13...9.5.........4...52...549.........7....9..5147.14..8..3...6.1.......8.3.
.2.....4..4...62717.3........2.....9..8...7...9...5.1...61.9..4...6...9......21.5
..8....54...25.8.64..8....3.......2...9...7..71..4.5....798.........5...16...7...
..5...987.4..5...1..7......2...48....9.1.....6..2.....3..6..2.......9.7.......5..
..4....89...1.2.6...6...7..2..8.4.1..4....5...3......8....7.......5.1....154398..
...7.6.....1.9.52..9..2.........4...35......69..5....8.8.......6.3..5....42...1..
...68.......9..4....2.....7.7....1.9..45..2..6......5.8...9..2.9.5..3....1...6..5
...58......7...6..3..6.42..97..2.5.3..1.5..4.5.....7..4.59...2........6.....1.3..
...2.5.9..47.........6.....5..9.1.......8.1........3..2.......6....3.8..7...4....
84..1...27.....8.....5.........5..3.65...9.....2.7...1.....628...6.....523....4..
1...9............1.3.6...7.......5.259..6..3.....7.89.6..7...4.94...8..6......2.5
.2..316.......938.9.35....1......8...1.6...4.2.6.97....9....56..........5....2.38
..75...311......4.9..4..68....7.8....9.14..53..4.5......58...2..8.2.51..7........
..5...4.23..............1.6....73....1...95...4...137..6.9.....8...3.7.....24....
..34.....5......47.871.......6.1.8.......2.9.....6...2..9.....1.3.7...5..5.98.3..
...7.........62..53......274.5.1.7..61............3.9...1..4.....625.....7....8..
...1..5.....3....6..7..9.3..16.32..9..5......38.4..............84...71........8.2
.....7..9....2.3....3915.7......2.......8.7..725.9..1..........8.9.3.4.7.5.....63
8..7....4.5....6............3.97...8....43..5....2.9....6......2...6...7.71..83.2
6............5..3..31...2....7.19.6..8.5.64.......8....5..4..71...6.2.4..........
.7.6..3..96...3...1..58...6..9.5.........21.........54...1....8.91.6..2.43..7.6..
.4.2.6.7...1..........34....1..2.5..27.8.9.1..8........3..5.7..........89......61
.3..4.98..6..3.7..9.......25...9....6..4.3.1....8.......1.....7...9.......7.5.2.3
.3....2..9.4.7.5.11...5.3.....4.5.........7.96...3...5.9....6...8...2...4..1.7..3
.1...5.....68....189....5.....79..46...14..8.......9.....2...5.47..3....3....7..9
..748.3....4.65.........9.6.8.......1...5.6....5.48.7........2..7.......39.17....
..72......5...1..34....8...84............2.596...7.3..3...2.....2.6....7...3..4.1
..7..2.....53...7...69..1......2.........46...9.5....35.3...8...8......4.1..6.5..
..4.93.8..68..............9.3..4.6.....6.5..2.8....7..6..71.....179............4.
..19...3..3...2..78..........3.6..4.2........4.53....1.1..49.....4.1.86....5..9..
...6..9...4521...6.....7...5.......2..8....5..32.....4.2.....1.8..369.........8..
...45...9........3..9.....1.6...87....8..2.6.9.46.5......83....6....1.....1...54.
....9.......3...7..8...24..4...6.....175.4..3...7....593....2.....1..6....5.....4
....2....6....48.....9....7....7....8.5.1...3..18....9.5....34.4.2..36...8.....5.
.4....1....265..4..8....5..6.......1..1..9...9.82....3.63..8.2....4.7......5..8..
..7..8.6.1...5...8...6.....7...6..35..4..7....9.2......5.4...2..7....3......16.4.
..2...3...3...92.11......79.8..54.....9...5...7.....13.......6.7..82......56.7.2.
....6...1.3.2..6..8..49.....5....1.72........7.4....3.6...7.5.......2..8..28.476.
..........46.5.9...5.4.1.6..1.7......3...58..7.8.63.....1....9.......4.2....27.56
8.72......4....1.2.5.....9..1...39..4...5.6.8..56............2....37.......8.9..4
7.......4...29....6...8..5....7..8...8...1.9...4.3.2...2.3....6176....2.4........
.3.....82..2.9......4..67......43....1....5..7..6.5.2..9.2....6..65....9......31.
...3...9..2..71.......863..6....2.3.5.1.....97.....4.......3.7....5.81.3.18....6.
......9......45..2514...8..2...3.....65..1.7.7.......4...5.......69.....1.9..35..
6..7....3.8..3.........26..8.........1..2.59....45.12.5..3.9..77.........9.....1.
15...47..8..........47.....2..8....5......2.85.1.6.....1...3..9...4..3...39.58.1.
.7......69..73....8.2.5.9..5........4...96....8.4..2......8.15...35....4...9.....
.2.........6..4.7.1...8.69........2.5..........91.7.56.....6...781..95....5.1...3
..63...........1..82...1..79...4..1.3..297.........5.....51..8...4..8.3......26..
..2.5..1.....6....4..1.7...8....5.....7.3.56.......2.75...936.....5...4.19...48..
...6.......8.9..1...6.154........97152..7...4...8..2..7..3........56...246...7...
....97...8..3....1...86.3....16...9....9.26.35........3.2...4.7.5.7..8..7........
....49...15.6.....7......3.5......262...3..8...7...4.....85...1.7.1.....68......7
....3.9.1.28.9....7..5......8.......5.49.....91..5..7.......6.4...6.....3...7..5.
.......2.......8...15.6.3..1.2.9.5....9.....44...5......45...7....8.6.1..3...2.5.
9...8.7...52...8...7.....9.6.9..8.....5496..2....7.....1..5....4..........714...3
1...9....82..75..3......67.5.3.....1.1.....2.9.....7.6.58.........26..57....1...8
.8......9...1..6.....7.9..5.6.5.....42..3.8.....2.7...59....34...1....2.....4....
.3...2..6........16.7.9..35.1..7...8..35.8...4...........6.5.......2.1..9...3.4..
.1..85.6.4..3........1..9...3......18.14...5.6.....2..25..9..4..6...7..........86
...68..9........259.4...8..2.1965...........3....7....31..............5.7.91.2.3.
....3..8....4....1..5.81....1....9..3.....26...7.2............9..29.5.147..6..85.
...........67....9.2..164...4....9...8.13...........25.179....4....8..6...3.2....
39.6.......7.......6..9.12......5....2..1..6....4......85.6..9.......4.......7.32
.7..............8...98.4.6...61.....5...4.2...4..9..7.....316.26.....5....42....3
...6....4..53.9..1....8.73..1...6...6.3..8...7..91....2..........7...58..9....6.3
...45...9........3..9.....1.6...87....8..2.6.9.46........83....6....1.....1...54.
....4.......6.23..83......9.7.264.1.......4......37.2...1......69....75.5..8....6
....3.8......2....9....163...581...92.4.......8.5..........61....2.4....63....5..
.....7.....8.5.....6....475....2.....3..9.64..94...3...5.....6....8..9.1..71.6...
.....6..7..2.......5.9...863...9.....8.....912..7..8....3..5.7.4...3.2.9...1..4..
9..7..1...2..1...7...5..6........56......32..1...5...824..813...1542...6..9.....2
89.5.........983.6..3..1....3......29.6.8......8.4...7..7...4...5...97......1...3
38.5...29..5.4..3.......5...2.4............8.4.9.8.2...7...6......2.....864.9.3..
3..1...7....9..8....95.....7.......9.2..3.7....8..4.5.......5..1..7.8.........247
1.....3.....2.6......8.7..2..748....94.5..2..5.1.......1......9.69..8.3...5...4.7
.69.1.7....1.2...63.....9....5..7....4.....7....9.6..5..3...54..7...3.6.8.6.....2
.6..9..1..4......83.5.8.........7...1..26..7....9..365.89...43....74...6.....9..1
.6..5.7..1......85..4.9..6...5.6.....1..2.3.......31...3.7..6..4..6....2..89.....
.3.6.........87.....6.1..54.....8.....2..6..14...7.2..7..8.......9..5.3.6.1.9...2
.3.5.......4.3..2....8.6....2..49..66..25.1....1..8.9...3..58.........7.59......4
.3..9...18.....6...17..6...7..2.1.4.......87......3....6...235.4..3.......8.....9
.2...9.8.......29...5...4......7.3..3.71.....4.............69..69...4.327...3.5.6
..14.....57......429.1..3.....5...62....69.57...........795....4...2....13....7..
...47....8.....491.....1..3....1..39..982....5....36..41....7.6..5..........6..1.
......3....9..7.1.78.4.....3..5..2.....32..8.....81........64.........914.5.....6
..........5724...98....947...9..3...5..9..12...3.1.9...6....25....56.....7......6
9..7...6..12.4.......3..29...6....58.7...........5.43..2753........64...1..9....5
6..89..1.....5..........8...274......3......54....7...2..6......85..4..21......39
3...6...5.9...7.....6.....32..69.5.......1..2.4......69...1..7...43...8......8...
..72.....9..3..82.....8...6.8...43....1....5..2.51..48....962............1..5..83
...569...........7.69.2..14..8....4.3.4.71......4.....5..6.......7...18......2..9
...52.....9...3..4......7...1.....4..8..453..6...1...87.2........8....32.4..8..1.
.......42581.........86.......4..9.5.....3....68..7....53.2..84........72.....1..
9...8.3.2.3.6..7..14.2....6...9......26.34.......2.....93.47..56.1.....7........3
67...8......4..7...2...76....2....4...3.8..91...17.8.......1.5..3..5......5.....2
53........79..2.....25..9.....2..68.7.......1.8..9.2....17.........38..2...96.17.
.6...75.9....43.......5......3...48.....6...5.12....6..9..72..44......2...8...1..
.4....37...3.7.49...7.8......16............2359...2...........96.51.........3.51.
.2...34.75...74......6.........1.8...81.....2.....9.7383....9.........6.4..9.2.3.
..2..8.....37..4..9....5..15....2..96.4...8.....1.....2....4......91.6...9......7
...6.378.......5.1.......3..8..5..9.59..4.2...46........98...15..........28.1..7.
...25....65....4..3.9......4.....13..8....6.9....835.......1.4..91.7.3..5...9....
.....9.8.....4.....271.............7..6..29...7185......89..6...5.62...8......25.
.....8.7..13..............4...1.45...9...73....82....65..6..9...2..43.6..6..1....
8.7..46...3..6.9.....7....3.69.....55....973...3.2....7.1..6......51...........2.
3....4..6....2..7..658....113.5..9..6..2.1.....9.........9..7.48...........46..32
1.....9.78..4....6..23.............8.8.5..73.6.498.......1.9..2..5......4...5..7.
.9...4....1.6...4.....9...7.....5...4....152..57...8....8.3.......56..1..7...86.3
...87..2..945..1....34....7..6.5.........7..2.7.....6...9.........326..1.4...8...
...7....2...2.1.4.9...4..7..97..6....1....23.3........73.4...2.5....3..9...15....
...1...9......6.1..2...34.7..79....2....6.9....8.741..6...3..2..5.7..3...4.......
....2...8....64.1...4..73.....5..4.1...7....92.74..........3....8....5...69.....3
2.4...8.......8.36...9..4.5..7...6.....3.7...16........7...1...4...8..9..82..93..
1...9......4.63.9...7.....8..2..6...59.18..2............1...8...7...2.6....91.7..
1...5.6...5.1.9.2.................6437...4.1.8............618.3..7......9....5...
.3.64..2.1.2.5..3..........8..3...793.9.....6..4....1.....7...3...8.9....57....4.
.3....4......8.2..1.4....9..7.....2..156.7........2....93...81....1....7...85..6.
.29..........4....7..1593.......573..........17..835.92.4..6..1...5..8..9........
..8......9.....1...1...74.........25....28...73.1.........5......3.42.8.5.4.1.7.6
..4......2..45..1..6......3..7.6...9...12.38....5..........7.6.....9...28.....5..
....4...1..4.6..3....9....6...5.....986.7....5.......2..2..73..693....5....4.....
8.....4..16.3....2....2...1.3...92....9.....7..85...6..5..4..1.49...78........7..
7...5.......784.3......1....4.....71..7.....9.294...5.8...16....3....6.5......2..
7.....1.8.1..9..3..4...5.....64.......18..39....6..8.1.2.5...........7......43.5.
.62.....5....4.8..8...21...67.....3...1.73...3..1...48...7..9.6.....5..329.......
.4..7....7.3....928....14...672....99..1.......1..7.54...3.....4....5.8.......5.1
..3....7..192....6.4....1...9.7.4...6.....4......36.8..7.6.3.5.......8..2..59....
....7..8..7..2...1..6...5..3..9..8.......7..4....1.26...1.58....9....3..5.....61.
....62...4.73..........137...9.2......1..68......8..32.8...5..36.....1..79.....5.
.....5.3..6....84...51..6.....2...5..9..1...7..47...9......8...9.........27...4.6
......3..84.....9...9..652...8.1.7.......2.4.16........9..3...7.......1.6..7.98..
9.7.5..8..2.........57.3..1....72.........812..398..5.......46..9.......6.83...7.
..5...4..7.8.....3....6...1.....5.2....73..1.1...2.8....4..2..6...4....93.2.7....
...9....7....1.38....5..2..8.7.6...9...1..7....4.....5.1..8....32.....6.6........
...49....8..1...5..1............24...5.8.72..3...4...79....6..3..6....8.....7...9
....85........96..96......2.1.3....9.5..27...48...............4....1..5.7.2....3.
....8...2.6...4....7....8.9..4.2...8.....1.35..3...6....6.......5.79....1....6.5.
.........97.64....1......9.51..7..43...1......96.5.17......753...2.6.41....8.....
.........8..2..37.9.24....5..698.5..7...4.....3...6..4.........3..8.9.1...9.6.4..
8...7....1..6...82........1..6...2....724.5.....73..6...9.64......5..4...2......3
4.....53.81...26......3.....5.9.............4..18..36...2.1......8...2...9..6...8
3...4..6...592...1.8.6.....97.....45......2....6.3..9.2..4.......1..5.....789....
16...89.....7.46.1..........87...3.......2.....9....5..5.......7.8.3.24..3....8.6
.6...9.4...4....1.2.......7..2..65..69..1........78.9.3.8..5....5.1....3....2.8..
.4.6.8.5.6...4.9..1....5....9....3.6..1......4..8...7...89.......7..62..2.......3
.3....8.42...4.5......2.....15.9....6....8....24.53..7......49....1.......793...6
.2.......7..6...1.....8.6.9.9......4......5.25..17..9.....5....3.7.49...4..7....3
..3..8..........75...4..96.........7..1.5..3.9...2..5...46......6.1....47.2.3....
...4..62..16.7.........8......2....8..4...5.75..3..............4....9.8...8.6.13.
....6...4..6.3....1..4..5.77.....8.5...8.....6.8....9...2.9....4....32....97..1..
.....94...15....3...92......4..5.....8....64..61.....8........2.2.78..1...3.6.7..
.......52..7..18...9.....7...2.4......3.28.6.7..1.....6..4.5..32.576..4..........
4.....8.5.3..........7......2.....6.....5.4......1.......6.3.7.5..2.....1.9......
35.1..6...4..6..2....4....3..2......9.....7.25...8..1..9.6..........94.761...5.3.
1.....3.8.6.4..............2.3.1...........958.........5.6...7.....8.2...4.......
..4.....69..7..8...86..4.5...9..3.7....8..2..2.8..6.4..1...8.....5.....9...2.....
...4.6..7..2.9...6......15......892.5......7...7.5.4..63.1.........89....19...5.2
...2.9...9......7..746..........35...48.6...3..68..2.........3.8..1....5.17.9....
48.3.......9.7......5.6.41.1.......2.5........63..7..9.....36....2.8..45...4...9.
1...7.6..8.5.....3..74...51......7....4.2....5..1.6.2....6.93..69............4...
...7..4....6.8..3..1....2.51....6.9....5.73.6....3....8....9.........7.2..7..4.5.
...6..7.8..........4.2.1..........5.5..7..8.683...6..17..5...3......9....628.....
...5..9.....8.1.258.......1.4......3.1.6.......5.7......9.6........136...3.9.4..7
963......1....8......2.5....4.8......1....7......3..257......3...9.2.4.7......9..
9..4.3.....2..7....4.2...9...4...56.5.......86.....4.3.7.315.....9..21......76...
8.63......4.6....9..5..74..1..7..8............84.1.6..5.......8.....37.4.39..2...
1..5....4.64...39...5...2..........8.5.1.........6.12..3...6..96....7...7...38...
.2.5...8...5..9....7......1.......13.....39..3..296..743.8......5..4..7...2...6..
..3.8.5.......9.7......12..2..7......8..5.16....1..84..4.8.5...6......3.7...3....
.....13...7...3..1......4....9......5...4...228...7.5...2....3.3...75..9.9..8.6..
.......34.....5.87....2.1....9......7..3..89686........1.6.......24..3...4.9....1
..61.8....4.....7........2.6...9...58.....3....7..1...5....3...98....6..3...2..59
...6...4.......918..8..7.....5....6.86...2.....93.8...3..1....7.5..4...19...3....
...3..25.....4..3.1.........38....2.....6...4..5.......2.8........5..7..6.....1..
....41...9..5...81.7...96.....4.....3..6..14..8.1....3......83579.........2....1.
.....7....7...8456.1...4..326...9...8.1.....5..4.1.8.........2....496....4..7.5..
718..2.6.........45...7....29...36.......9.5....4....83..7..8.5....1..9...92.8...
6..3.2....1.....5..........7.26............843.........8.15........8.2........7..
1.5.8.......4.6......7...82..6..29..392...8.1.1.......62...749.........57..9....3
.7..6..45.....18..4..8.....62.1........5....1......237..3..4.....2.5.3...9...6.5.
.58.....4..9..7.5...1....6...743.1....35..........1.2.....4.3...7.19...8...7.5...
..7.4..9...83..1..3..1........23...6......8.......67...6..1...2..2..79..41.......
..2..6..........31.7.28.5..5...7........1...3..8..26...5...47..3......9.4.7......
...84..9.....512.....6...815.......776..9.8....3...4...7..63...83.4.5....2....1..
.....2.8..7.6......1.....92....263.99..7.......8.156......61.4.........35...97...
9..6..8...53.8.2..........5..4.1..2..3...4........2.....1..97.3....5...9..87.....
9......4....4...9..3..9.521..9......6..53.4.........5...2..8....1.6.4..2..7..3...
1..........6.2.....4....98..5......6.....74....758...3..4..5.9....8..1.27...1....
.2.3......63.....58.......15....9.3....7........1....8.879..26......6.7...6..7..4
.2..8.1...9....7..5..7...32...2.....1..4..3..98...15.....5..9.......3..6.7.....4.
..635....8..4......3..2..5.37..8.6.4....3..9.4.......8....67......5...4..8....7.2
..2.3...7.57......9..4...2..7.3.....3......1858...96...1..9.8........1..7..5....4
...6.13..85.............4......7..523.1.............8..2.....7....1..6.....9.....
....3..824.1..................4.65...8.....3....7........5..7..6.....4...3..2....
6.....7.3.4.8.................5.4.8.7..2.....1.3.......2.....5.....7.9......1....
39.6.......6.......4..2.81......5....7..1..2....4......85.4..7.......3.......7.42
.56...3...7.....8.8.3..1..7.1.78.9.....9............432856.........2...5.6...91..
.47..........5..2.....1.......3..7.98...........4........7.36..51.....8.2........
..7..69.....73..1....8..6......51..4.3.2..86..........17..9.4...25....8...9....3.
..2.....5.1...36.......4.296.9..7.4..2...1..65..4.......6.9.7.2..8....9....3.....
...869...1......2..4....7...67..43..9.....2...5.1....8...9..6......17.....5....37
....2..19..16..5.....73.8.4.67....5.3...5........9.....89.......5....4.2.......3.
7.96.8...8..2.5.....6.4......8.1.6.3....2..5......4.1...2.....75.......9.3....8..
4...5.....81..2..6.............4...2...1...5.....953.7.3.72.8...5...3.6...7..6.3.
1.5....2..2...5....8..9........8..6.35...4......3...5..1...9..6.......948.2..7...
.9..3.........826.....7.4...1.7.2......8....3.....697..7........4....5..2..5...8.
.834.........7..5...........4.1.8..........27...3.....2.6.5....5.....8........1..
.673.4.....4..8..78..2....36.....9...5.8......7...9.4.....2..1..4.5....8..64...3.
...9.6..44......72..1.......8.37.4..62...8..7....9....73....51...8.5...39........
...1..........84.9..139...5...9.61.....8..9.346.......2.....7...13...2..95.6..3..
.....5.47...3........28.5....352..6...8......6....4.5.24...6..........7..9....1.3
8.......9..71..6...3...5......8.6.2.......7..4.3.7...69..2......78.....3..6...9.8
39....1.............648....5.8.....1.7..2..562..7....3...9.3.6.......2......57..8
28..3.......5...4..........3.....8.2...4.7......1......64....7.....1.3....5......
2......89....57........3..1.....563..2.14....8............9....9.8.3......7....45
.4..56...59.1..2....18.........324.6.8.4.....9.......7.....1.3.......7...65....9.
.4.....8.8....63....9......1...2..393.65.....49...8...5..7.2.9..2..59.........1..
.36....4...75.........3......49...6.7...4.8..6.....37..59.........1..7594..6.....
.3.....1.69..........593...2....13.............76..28..8.7..19.7..2..6.......5..4
..93.7...2..9....4...8..6....36..41.....1....6....2..913....7.5..6.......7.4.....
..6...8..8.......29.7.6......3..4......2..5.14..97........1.6....5.9..84...3....9
..5....1...4..3...2..7.4...5....26....1.6.5...9..7814...9....8...8.2...6......3..
...6.5..........4.857...9...1.9.8...7...361...8....6..3.......4.6.8..5..2.......3
....576...4.....1....3...85.8.........4165...6.....2.7..6..9..8.786..........2...
1..5..2.7.5.2....6....7.8......3.98.5....9..3..9....1.3...86...4..9......9..4..68
1......9....3.1..4....6.......8.67.9.69......78....4..4....3.575...176.......48..
.97.68.......741...5.......91.....8...2..1..5.........4...9..7..8.4.....72..8..6.
..49....25....4....7......8......6.3..1...5.795.......7..5..8.....4.1..9.6.82....
..3..8..2.7..4...1..4...9...18.23..57....6.2...6.17........483.3.......75........
..2..9.6..4...1.....6.3.4......2......97....3..3...1.5......68.3..5.7...4..1.....
..2...6..4..9.......5..6.81.8......5.1.........3.79.4.........6....2..73..73.15..
....8.64......5..3.2.9.........49....3......14..7...687.8....2.......5..6...5..8.
6..3.2....4.....8..........7.26............543.........8.15........8.2........7..
1.2.......6.....9..7..41...2..9..6.5....8..4...8..4.....6.2...7...5.....5..8....3
.8.71.......4...1...9..2.5.3.46.1.........3..2.....6...9...32.7..28..1..6...2....
.2.7..........13......8.2.1.1..589.3.5..9....4..........8.1...9...932.5.7........
.2.....3....1..7...83.6......6.2857...9..7.........46.5...7....4....1..2.....4...
..8.1..2...4689..1..7........9..8.5.8....2.......7.9..3..2...7......74......3...2
..8...4.6..2..3.7.....5.2....7192..4..........3.........62....9..154...2.4...98..
9...5..4......86....5....9.2......3...8..7......1.6...7..6....4..28.9..7.9.....23
.7...93..............483.618....2....1.....5.3......2.4...9.....69.75.3....6...1.
.6.4...8.9.7.3...6....9....5.......4.....37...3.5..16.4......5..8.......35.2.6..9
.6.....7....2.85..9....1..2.9....13...65......38.......4..37.6...71....8......7..
.6.....4.1......72.5.78........6.9.....5..8..9.3..1.....1......28.3....1.7...4...
.5.24...3.6.....2.8.......94..812.....5........83.5.....6...1..3...792.5...1..7..
.5....6...4..7.8....14......8..........15.78.1...2......5..1.2.2..76.5.369.......
.5......2...9......76..4.9...8..6...1......5...2..31....5.....34.......1...87.6.9
.456...9..........9.3...2.5...29..........7...3.8.4..2.5.38........1.8.6..6.7..1.
..82.......9..5..771...86.........4.48....9..1...6............1...5.2..39.5.3..7.
....7..8...6...5...2...3.61.1...7..2..8..534.2..9.......2......58...6.3.4...1....
....327...1...........5....1......294.78......6.......5.....43.2..9........1.....
.....3.5...875...27.3.4...6.9.........1...8.....2.5...9...64..1..7...6...8......4
9....34.....6....5.27..9.685....29.....3......7.....52.3.56.........7.4...89.....
4...8.....7...2..4..5....1.9....46...32..8......7....338...........4.29...96....7
.3....6.7.7.....24..4..1....9......3....1..8.....5.7..6.2..4.....32.8.6..4....5..
.2..58..3.........9.5...6..21..9.......7....44...1..6.53..4..2.6.2....35.9.....1.
..2..4......8..3..3.5..2.4.4.........8..15..6..7...519...4..6......7...1.....6.5.
....2.5..3..8...1......1..261.5......9....87......4....2..9..6.........3861....2.
.7......16....32.....7.269......9..3...5.....5..3.67....8.1.9.4.1.....2.9....5...
.476...5.8.3.....2.....9......8.5..6...1.....6.24......78...51...6....4..9...4..7
..96...2.1......3.4.3...6.9.8..1......2.5..91.....7....9....3.2....917....6....8.
...9.746..96.5...1.3........21....9......4....75.....2.....2.....36...1.2...8...9
...3...798.....3...6...1.....4..5.2.....3..9..8.2....523........5.98.6..6..51....
...2.3..14....83......9......6.....2..5...8..79.....6.5...4.2....1.....79...65.8.
.....9.8..1........724...6....9.8.4.5...32..........35.3.6..4....9..3..6....1..7.
......7..8..3....19.5.8....2...7..4.3...4...6..9..3.5......48..6.89...1...2.5....
8.......49...2.1..74......9......41..5...9.7...3...2.8...4......9...5.3....6.1...
4.8.....2.....3.....19..8......3.......1...4...5..2....3.546..91....9..67.....4..
.89.1..3...43.9..6..2...9...9....3.1...8.......572.......9....56.3..41...........
.7..6...59..21..3.......6.42...3.........6..8.1.7.9.5...4.5.2..1.73..........1...
.3.56...7....4.....59..81......7.8......9.4...2...6.7.3.......1.189.3.....7..5...
..7..2...9..3..4..........6.8..7..2..13....4......9.1.7..9.6.....1...8..2....5...
..7...6..8......53.6.4...9775....1....1.3.....9......6...7.2..8.256..........4...
..3..4..2....6..8....1..69718.4.......75.........71...23.8..4.............1...578
.......7...65.1....9.....6.3...8......2.7.4...649....81.....2....9...54..5...3..9
5...8..13.1....7..8..4........8...94....23...9.......7..6.54.39..2..6.....5.....1
.634.....9...........9..25.........96.9...54........7..176....5.8.2.3.6.....74.2.
..58.19.........2..6.7...3.9.7..6.........14.8.......3...61......4..7...62..9...4
..1.......2..8.3.1..4.63......4...3.....95...9....16.2.6....4.7..57.....7....98..
...9.....9.3..18.2....3.5....7....688...6..3..4...5...2.......3..175.........41..
....1...3.7...2..5..5697...7.93..8..6..1...9.....7.2..5......6...894....1........
..4.3....5...........9.47...1..758.4.6....2..24...1...9......1..2...6..7..1.5...8
....1..8.......5..6..348..1.7......6...96....42....9...4..72...7.1....3....8...5.
.....9..319.....758...7..6....4.1...4...2.....7......8..7..51..2......37.16......
.....1...84...75....5....8......9.23...26.7......7..5.7....24....8....35.21.....8
.........9.....2.4645.......16..2..3...9..7.2.....8.6....5...1...73.....3....95.6
7.4.6.8..25..4...1.....7......8...5..6..251.7...1..28......3.6.9.........25...4..
7.....3..1...5.9..4..6....1.....98..264.........7...5.6....8.....2.6..9..3..4...2
6..3.2....4.....1..........7.26............543.........8.15........4.2........7..
.4.5.2...........1....9..6..5.43..7..62...........1..321.8....4.......5..98.7....
.364.2...8......4...278.....2...873.6....49.87..6..........7.1....1..3..2....6..5
..2..4....46...8.11.......4..5..8..6...9..5...8.41.......7..2..9......6....3....8
......2..1...34...4..9.5......2..98...4.1....5.....3..65.......9..7.......14....6
.579......9......42.......6.....9.7..3.7...8..1..3.96.....24.5...3..........68...
.56.7........91.579........28....3......1.......2.4.9...16.9.2.3.....5....9....4.
.5....1.....16..7....5.9.3.5.9..........3.2.72..4...6..4...1.....7.4...8.6.3.8...
.1.....4...9..2...26...7..972.5..8....1...5......1..2....42.....368..1..........3
...5..28.74.......6...........3.2.5.1.......4...8......2....3......6...7....1....
...45......1....5..93..6..8...64..1.......8..7..3.2.....9.3...6...8....21.6....73
37.6.......9.......2..8.65......5....6..1..8....4......98.2..4.......3.......7.12
.6.184.9...8...4.....5.9...7.........4.......9.6.5...1......84.4...237.......8..6
8..3....19.2.........56...4..8..4.65...7....32.6..........1........8.5427........
37.6.......9.......2..8.16......5....9..1..8....4......58.6..9.......3.......7.42
2.3..............8...5.4.6.9.1..........4...653.9...8.....3.......1.76.4.57.9.1..
2.....9.6...7...4......93....4......3.....5.959.6...7....4.76...4...5.....1.3..2.
.5..4.3..2......7.............6.2.8..31.........7.....6..2...........4.3....1.5..
..5.9..4...7....8....2.8..36..3...2.......7.4..1..........4795....8.....8.......6
......7.2..7.5.....3..69...5..6....8.....413..1........768......5..9.42..9..3....
.......9..6...17..9.....2...1.3.26......7...87...4..1.2...39.6..8.......4..82....
..........2..1.63....4..2...8..7...5.....4..7..68...4.9..........425.7....1693...
1...3.8.....9...2....2.5.6...63....5.8..9......7...1....5......6298.......8.6.4..
.5....8......4..2.6...8...1...........6.....7.1.4325.....3...9..421.93....58...7.
...74...8.96..........2..4.....576..8......21..34........3.....124....5.......7..
39.6.......6.......4..8.52......5....2..1..9....4......18.6..4.......9.......7.32
2.3.8....8..7...........1...6.5.7...4......3....1............82.5....6...1.......
.8....1.9.7..54......9....3..2...8......87..1.9...5...259...........9.1.3......4.
.6..7....2...4.......5.14...8..1.....1.3..247..7...9.......8.968.....3...562.....
.5..2.3.66.93..42.2............1...4.46....89.1..........8........1...7.5..46...8
..1.3..2.....7.6...5.6.1...7...4..3...4..51.8.8...6.........8.2.3...7...5..4...9.
...8....974..6.8.........3...841..5...925...............7..86...6....2.45.......1
......7..2...........5.9.1...9.5..46...8....7..5..3...87.4..65..2......86..3.....
........673.8....1..8.1.9....42.....9...5....2..3..7..39..4.........5...84...3.62
38....1...6..9......2....9.41....9....8.....29.......8.....3.57....86......1.4.2.
1.9.....8.4...9.....6..5.2.........1....62.45.6..74...82.........13...........519
.8.3.......2......6....1..4..7..4...5.......6.1.2.9.7.....5..87.3...7.9...14.....
.4...2...3.....7..8......215...3.1...29....5...1..9......5......6..8.3.5...9..6..
..2..9.3.8.......4..95....8..........8365....46..71..3.18.3.2.7.........7......1.
......8....6.1.....8.5...6.....2.4.....4.9..37.....5..82....3...417....9.5..3...4
7......6.12..........28.31..4.6..8..9.5..42............5..4........75....7.3..4.8
2..81.....48..9..5...........1....3..9...2..7...13.4....624.........67........95.
1..5...2....28..6...7...8..2..7.5..34.............39....6..8.....9.7.5.....4.9..7
..85...6..........9...184......2....8.714...214.8..65.6....3....3..8.......2.71..
..8.6.........9...36..12.....7....51.35.....91...8...2.....34..95.6.1..3.......9.
..2...358.....7...86...........8.2.47...1.....59......5..6....3.8.13..6......98..
...627.....3...1..95.......8.......7.3..19....6.3.8...5......9..97....86..6.....4
63......4..5......74..3..6..2.4.5........19......6...7..4.2..9.25.9.8......5..1..
...7...6.83....7....9...8......4.68..71......6....2.1.59.4......4..73........69..
...5....7.6..21..5....8...1.41..........92...57....2..41..6.8...........7.5..4.62
...4.........61.7.....984....16.9..2.5...39..3..7....57.3..6.8..18...7....4.....9
...27...98...........4.8..132...69.......9.3.7..1....2..........948....6.789...2.
.7.6..4..9.2....71....2.......3.9..83..4....7....6.2..7.19..5...93..5...5...4....
.6....7.....4.1..3.7..289....6.....2...38......7..4..5.91.6.3...5.........41.....
.32....6....6.9...9..2...437...849....4.....6.5..1.....9.8......2...37..5......9.
.3...1...8....2.....279...5....7...8.1..8..2......397..574...1..8...9.....6.....4
..43.1.7...2...3..8.......1....9..2..2...8.6...5.7.1...4..5..9......76...9...67..
....7....2..8....7.....6.5.....9.43...9.....8..41....65..7...6...7.1...33..6...8.
.....534.3849...............15.3.9........1.2....2..8.....8..139.7.........6...5.
.....46...9..2......13.9...........87..6....1.3.59...........7...2....5.6..1..83.
8...9...7...6..9.....3...8.....5..3........527.1..6...4........3...798...9.....13
8....1......4.8..3.6..5.2.1.....79...19..5..42...8....5.8...3.2.3......8.2..3.7..
7..1.......9..3.5.......824....451..3.....4...7.2...9.2...8...6.3.7.....4.6......
.6.9......1...4..5.....539....581.....17.3.4...8........2...81.....2...763.......
.6...........5182.2.....5.9.7...3......1.....9..7682.....6...3...49...5..12.....4
.2.....8....87....5....2.6........5..6.2..4....1..3......9.6.3..4...5.78..5..7..9
..3.......5..8...7874..5.........796.18.9.......2.......63....24.16........8.43..
2..3..1.4..6...5.2.7.2.....8....23......4.6..7..9........65...........1..394.7...
2....8.5...3....6..7...2..4..6..73.....24...7.8.6...........4.....19....91......3
.95..3...3..16....71.9.4....2....87.1..4....3.........8.....3.7....9...4.32....6.
.89.2.......4..5...........16...7......5...89.......2.7.....3..4..6.........9....
.53.......765......8...1.69..1.....8....562.....2.4....3.8..7....79...8.........1
......35.....78...........1.186...7.64.........5.9..2...9.8.....7...64..2..4....7
8...1...6.23..9.........78......84..2......3.....5...96784..1.....5.....4....6...
5...........6.3.2..9451....94.3....7.........1....6..8....3279..8.9.1...........3
.76.....1..1........2...94...9..1.3....5....6.4..2.....8......7.1..9.82.....37...
.4....9..1.6..5...9..4..1.8...6...5.71...........31....8..4........7..29..23....4
..2..5..7..6.....3......69...7.43.6..2..9....1.........69.....2..38....14.1.3..7.
.....8.9.87....4.1..4...3...4..2..5.61...4..8................62...91......85.6..3
.....5.4.8.7........5.....1.3.69...2....23.....4.....9..2...9.3.1..7...4.9.4...5.
......8..2..4.......12...45.4..7....5.2.....98.3...6.....3..5..1.85...9....74.16.
8....9...7.......53......21...69...3.9....51.....47...53....2....1.73..6...4.....
8.....3.26...35.....9...........26.9....7...1.5.....3....9.82.6.2.75.........31..
1.2...6.8..42......5..8.........7835...1.....6...2571....7...694..9..1.2......5..
1..6......35.14.6.........2..8..3.2..2.....93.1..2.5..4693....8....5....8.....7..
8.1.......7..1...45..6.89......63.2....1........7..61..8........1.32..7.3..5.....
6..7..2.9..7......4..2...5....3.........2.46..98.....18...1...6.....6.3......5...
1..5..68............5786...........6..9...24...6.54.17.5.6.2.7...1.7......8.9.1.3
..5.3............8....721.3....6..7.......3.2...8.4.5.5.9..6...4.8.....76.3......
...64.3....5.3.....2..7.9....236.7.4.4............2..9..7....1...6.5...2.1.......
..........1..7...23..1...8..5....67....3.1.....8.4....8........4.9.6.1.......45..
.3..6....8...9.2..9..34...1......8.............9.8.5462.64.......72...5.....5...7
..23..58...36..9..9........215.......36.....8...1..2.....91..7457..4.......8.....
..21......846....5..3.94....2......4........3.....987.8....3..19...1..8..3..4.5..
...23....1.....7.....8..........561..82.........4.....5....14...3..6............2
....2..8..1.....7.4.6..7.952..7..4..95483..................1...5.......3..36..7..
.....46.....5..7.19......8.3.....5....72.6..8.5..9....6..8.5..7..2...1....1....64
42..7.....67......19..4.5.......3.65....9.1..7....8.......5.7.49..6.....5......12
....7....9......2..1...29.7.....168.36..4..1....5......8.2......3...7..41...6.85.
....1....71..9....6..2....8.......5.2..3...7...5.2.....671....41.......3.8267....
4...1..6.9..5.......2...384...4..1...9..51.4........78..6.39...........72....4..6
.34..2..69....1.........7...4.9.82..5......3.....3...829..14........36....6....5.
.1...57.4...7...9...8.....58.4...1...2.14.....9...8.........273..3.8.......5.6...
...1..4...53..67....8...5...3..4....2.5..3.68..........8......7.92....53.71.9....
....4...6.325..7..........56.7.3.5...........9...7.8.....8.2..9.5....1.34....1...
........6..8.9..1...73..2.53..7.65.....8.........5...2.15......2....1..76......9.
8.....5.......2....9..7......4...978.32......1...9..2...1.8..94.5....6....96.....
3.........2..8...9...45.1.6..2..........98.....564.81...7...5.....7..6.81...6...4
...53..91...64.........9.2...436....7.......6.93..51..38.4...57..2.5......9......
8....54...........4.6...8.2..1...6...9...3..42..8..7.......756...29.....64.53....
7....2.4..6.5..9.......81..3.7.........7.1...8..4....5..........96...7..1..8.3..4
32.6.......9.......8..7.15......5....7..1..3....4......15.8..7.......6.......7.82
32......1.9....7..5.....38..6..5.8........92.2.8.9...3....832.94...6.......7....6
1..5..3...7..2...........2....38.17......7..5..51..6.......68...2..1..6..398.....
.8.6....9..4....23......4..3.9.5......2.7.53..4...1....9..........12...4..5.97..1
..82.....6...9..7......541..6....1......5...93..6..2..4..3.7...2.....9...86....5.
..75.....1...6..9.9...7...1.....46.3........54.8....7....3.7....23.1..6...1...8..
..2........37.....74.....36....4.....5....2.1.2....69...5..2......3..1.7.9.1.6...
...37.8........5.1...48..2.5....3....4.......7.9...1..26.....79..5.9......8..76..
.....193.1..986....7.3...8.6.......3....3.59...32..1...5...8....9.....4....4.2...
...5..6..85.7.....9.4.........1...7.......1.4....4925..123..7.......2........8.3.
...2...9..6..947....8..6....16.....5..4.1...9.7..4..3.....53.4.......8..2.......3
....9.....24.5....86...2.91..68..1..5...4.......5..6.7.81......4.......5..2....3.
8...7......4..53...7.2...4...9....2..........5.3.8.1...6...4.7.......5.6....67..3
4.....8.5.3..........7......2.....6.....5.4......1.......6.3.7.5..2.....1.8......
27....4.6...3.1................7..3..5..4....8.....9.....4..57.6..9.......2......
..92...6....4....82.............7.1..........36......2..3..915.1...75...48....9..
..3......47.2....8.6...5..9..7.9.81..4.....5...51.........87......3....4.8.4..2..
....69...8....4....7....6.1........23....17.....8.613.......4..1.4.9..6..23.5....
....6....61...9...2....1.5..8....934..7.....6..3...2.....5......5.8....79...46...
9..2.16.5..67.......5............7.22....9.3..83.............4....6.3.2.64.5...1.
8.1.7..........62....5....7........1.6..43.7......9....94....5.12.8.......7....3.
4.....5.8.3..........7......2.....6.....5.4......1.......6.3.7.5..2.....1.8......
..2..593.....2....1..9...5.3...5..4....4....85.81.2...2....6.754.....6....9......
...5.71.4.......2..3.1.......24..3..5.....7....19.......8.6....3...9..65..5...2..
.....9.616..4...5.2..5....3.3..6......4..1....7....218.....812..5...........5.7..
.....3.8.2....4.6...15....7.37...45..6..........8......154.8..67...1......4.9...1
........1...91.5..2..74.....9...72.4.486....35....3.....1..........3.....34....18
4......6.....8..2...62...89....4....91...87..3........259..........93..2..4...1..
34.6.......2.......7..3.51......5....3..1..7....4......28.5..6.......1.......7.32
.9....3.1..3..48.........6.3.7..8...1....29...6.7...8..7...35..2..47.1...398.....
.56.1...4....69.5.7.14..6...6..8...1....2...9..4..7..............8.4..16.7.8..3..
........31......7...65..91...78.1.6...4.5..92...4......68..4...41.9...5..79.8....
4.....5.8.3..........7......2.....6.....5.8......1.......6.3.7.5..2.....1.8......
35.6.......2.......9..5.48......5....6..1..9....4......18.6..5.......7.......7.32
28...6....4..5.82..1.....9..2.4....33....5.......2.5.9..257..3.1....4...4..1..97.
.7.5.....4.....29..8..4......2.....7..9.......5..28......9....3.....7.157..65..4.
.1.6..9..4......5.....39.4......6.1..2...35...6.....72.8....4..5.3..4........7.2.
..3...1...6.2...9...2.84....19..6.7.7.8.1............5..7..3...3....2....8.75...3
..2...73.....972.....4....639..1........7....8..6..1.....9.3..8..4...3.5.....1.2.
4..9.31..............16...9.52....3......1.7....57.6..6....87..1.....8....92.....
.8.....3...12...9..2.......6...74...9....3.7......1....3...2..1....48..3..8....56
.5....1..3..9.6.4.......3....6...41....279.5...2..1...4.7..59.....73...........6.
.4.....98....61..........2.5.6.7.3.....9..4...........3.....6.5.9.8..............
...59......7.2..5......74.1.1.8.......6.3..4....9....2.5...6.794.........8....3..
....7.1..2.....96.6............126.5...4....8....5....1......9..47..9.....8..425.
....4...35.1.2..4........2..8......9.1..8.....96..58.....2.6.....9..1...2..3....5
8..9.6...........7...3..9...1...2..849.5...36.2......9......54....2......31..7...
6..9..2..3.....6...82.76....5..9..8...1.........72.9.5....3.....2...4..75.8.....2
.89.2.......5..4...........16...7......4...89.......2.7.....3..3..6.........9....
...92......541.8..62..7............791.....4.4.2...3...6...84.........3..8.5.7..1
...1..34......71.2.6.......9......6......1...3.792......4........8..52...5.31.7..
....3.....7..5...25...4..9.4..6..9...9......13.2....7...7.948.....3..1....8....5.
7.....96......5..13......8...69..3...1...8.4.97..4........6.....24.....5...8.1...
3.41...8....2.6.3..8....9....8...65.9............65..3.....3..74..7...2..2...8...
..7.2..9.......5...3......1....15...4.......71.9...6......4682....2...45.2..38...
..4.......2...8.7..7.4..5..9....1.8.83...2.........6.36..5...1...5..43......97...
..2..6.......2.9.4..4.........8.....5.......2.8..49.533...5.6...5......87...6..3.
...5.3.......6.7..5.8....1636..2.......4.1.......3...567....2.8..4.7.......2..5..
....8.......9.....9.53..486.1........4..68..2...1..69.....9..676.8..32....2...1..
4.....3.....8.2......7........1...8734.......6........5...6........1.4...82......
.5.....3...7.4.9.....9...7..6.78...9...3..2...1..5..4.6..1...9.7...3.8..1.2......
...9...4681....3.7.............3....34.....18.7..19......5.......2.489....6.7..5.
...6..8.3.5..1...4..9...1....6.8.....9..673..5.....7.......9...4.1.326...3......2
...456....4.....2...8.1.5..81....9.3....7....6.2....18..1.6.3...3.....9....7.9...
...4....7.479...6..5...7...2..3.......4...6.8..8..4..2.....5.9.6..19..2..3.8.....
....5..6...........95.76.8..6..194..3.............8.217....431...21........78...4
9...6.1.......1......2...76..23.5....8.9....2.6.....8.4.3........57..6......5.93.
.4....9....5.2...3....5..8...12.8.4......4......9.7.6..238..6.........9.65......1
8.2....93....7.6.........2.5....6..8...3....57.49.....4..8......6..4......5.6..1.
.71..9.....5.1..3..2.....5.....2..8..1.4.86.3..6.....1.4......59...........2.3.7.
.1.....826...3...............9...74.3..8.2......1.....4...6.5........9...2.......
.9.2..86..8.53....5......1..6..8..9.8.5.......7.4..2....4.5.6.....8.........79.5.
.9.....7......4.35.31..2...2.716........2...4..6.....81...7.....6........743...8.
..7..53..8.2..9..1....81......6...........18.4.9.1..2...17...6.6...2.5...3.......
..5.8......75..9.....741....143..6...6....5......1.3.........32..3.5.7..7..4....6
..41..8..9.......55.......4.2.3........4...71..8.9.......613.....78...26..1...9..
..2..84...7..9....9...5...7..41...6......2....18..5..........3..5......64..6.79.2
...8.7.5......2.4915.........9......8.29...6...3.7.......68...249......5.....37..
....8..........472.75......3....5.......798.5...2..7..2...53.6.6..........86..1..
2........48..9.1...5.....6.6.5................39.257..1...8.97......2..3.....3..8
.1....8.....7....5............5...73.68......4........3..4...2.....826..7........
....1..2.4..9.......9..2..38...2....6..3..5...3.4.6.1....1.985.58.....4.........6
1.............5...2.463..8.49.3....6....7...3...5...2.7.9.6.....2..481.........62
.9...54.........1...41...6....3.46....6.12....48.....5..5..3...8...7..........287
.8.3...5......4.3.1.......6..7.9.3.4.6...7............3.9.4.2...14...7.....8....3
.6......7..1.95...........8..3..94.1....3...6.8....35..2.6......17......4...1.7.9
.5.4...7.8...5.3.1.6...1...2.....7..3.....25..86.......2..7.....3.92.6.4...1.....
.5...9...6.4..2..3....7...4.......1.8...3....769...2........7.539.1..........6...
..9.......2.39....6....2..1.1...7.288......5....9...6...5.........4.1....7...83.6
..19...6......8....48.3...5..9.72.....5............7.2...8..1...864.1.73...3..4..
...3.7...4.......86...............9.5....1.63.32...7..8...19.4...5.6.1....4.5...6
....1.......8..49.......867.5.......17...3...3......4.5.62........9......426.87..
......57..5..1...........8....7.2.3..4....6.....5.........6.4.17.2......3........
......1.6.5...9.....7.3..5.......347..5......7.4..2.......7..386...2.....8.6.57.1
61.8....9...3.6.........25.7.8.2...3..37..9.........6..5...78...9......5.....1...
53...8.1.......5...79..6..2...7.9.....6..589.....2.........1..43........8...4.7..
1...49....6.3.................5..1.74.2....9.3.........7.6..9........42........1.
7......5.....52....4....38...61.....9.......7.8..3..9.2.74........9.8...4...7...6
43..5.......1....9.....7.....5.8.34....42.5..8........1....46...6...9....2......8
14.3..7..8.........6...1....1.7...2.3.48.5.9........1.4.6...8....5..31.....4.2...
1.....89..8.27......5..82.7..1...4.5....1....7...5....3...........4..97..9.6.7.3.
.9...6...5....7..6..2...3....6..5..48.....79.7....2.......5..1....62...8.3...1.4.
..89....3.....15..6......4.3.57..168..1..............25.4.......8..24.....36....1
...2..7.6..5....9..3.6.........4.5...9.17.86......2.....1...45......4..3..8.1....
....35.69.......8..1.9..3.......68.4.593......7.........25.....5....27.14........
.....42..8....9....64......3..7.5..957.........6..3.4...95..7.2.3.......7..4...16
.3.85.1..7..3..2....5..4.6..........284.....7...9..........6.1.6....5......48.3..
..45....7.2..96............2.....9...438...1.....15.....5...43.78..........18....
..3..........51.....23....4......61...19.8..3.....62..798.........8........1.956.
..2...3..1.4.......3....4.6..91.3.....6....2.....85....7...4.1.3..75.9..6........
...9......85...6..4..2..........6..3..7.......2.43857......79.1......8.539...4...
.....31.....2..7..43....92.8.2....5.65...4........1.....9.67...3...12.........48.
..2......9...4.......671........8.......643.7....53.6.43.8...2.68.....5.7......1.
....7......5.6..4..68..42..9...1.3.77............4..21..12....95......8...7....3.
.....16.......5..82...8.9.3.3.1.2...5....3......74.3...14........6...4.9..7....6.
.9....7..27.4..9..8.43........5713.6.......8......9.....7.3.1......64....6......5
.64...7.....8.1.....3......5......28.7..6...........5.2..5.........4.3..1........
.3..8...4......36..6...1..2..3..2.......3815...8....2.2...64..9.862......7.......
..4....6.....15...6....7.5..9..2.3..3..7....9.....62........8.14..1...7...9..3...
94.....7...2..76......21....7.8....55.9...86...36......9.7..1..7..9.4..8........6
7.8......4.1....5......74...2..5..8...4.9.2.......6.4.893.4................2..3.9
.3.....6....54.2..2...9...7......1.......8.4.....56.7...63....8.45.......87..4...
.264.....85.........95...7...2.36...........6.7...5..8.1......4....92.5......7.3.
...5.1..2......4.12.......798..1.....42.6..19.....2..3.1..9..3.79..8...6.........
....6...58..5..2.....8....641.....9....71....7..4....82....3..7..7.8..6..9.....3.
1....5....3.4..9...7......4..1.........5.97.36.............4.79..8.1.4......8...5
..1..5..6.....9.4.39.....7.2...3...1.8.....9....8.6.....34.........1..8...69..3..
...8...2...6...3...4.2.......3...6.15..9.....8........29.....5.....7........6....
.....7.1.....4.5...4...3..7..36...9..579.....1.....8...3..59...2.6...1.....2.....
72..1.....4....8.3..8..........7..31..952.6......8..4......2.....164...9.5....4.8
6..9.....5..1....71.38....4..6...93.....2.........5.82..1......2.....4138...3....
5..47.....2....9............3.1.9..........87...2.....7.4.6.........31..8........
37.1.....6....5..48........4...8.3...169...8.......2.....7.....9..4..8.6....2...9
16.4...3........7.58..2...1.1.9.....4.......8.28..6.9....738.........5.6..4......
.6.9..3......7....123........7..9..6....6....84.....2.5928...4......58..6....7..1
..8....2.7.4....8.1..9..6...7..6.5.......3.69.2....74...65....3.8...4............
..247..58..............1.4.....2...9528.9.4....9...1.........3.3....75..685..2...
..2....4..1.....328....1.7...7.15.6..5....4.7.........79.5...2...6..2...2..89.6..
...5...4.....132.7....4.6..4.......2.5.........27..3.9.6.3.2.8...7........18..7..
.....21..9.2.7..3..8.3.................5..7.4136.......7..6582....8.4..........6.
.8..7.........46...1...........2..716.53.....4........3....6......7...8.......5..
.7...1...92..8.....64..92.52.....9...9...6.1...7...8.....8..6.........5.4....512.
.3.6..8........7.5...5...126..4......149.....8.2.6...........7.....8.2.19.1....4.
..7........48........123..5...91...46....29...1....2..4.........7....1.9...3.68..
...46....84......3.5..8....312.5.4.....3........1.6...2.....98......7..4.95.2..1.
....3......3.1.75.42.8..........93.56...4....9.8.........2..8.......36.9.17......
1..6........7......74..13..73.....18..89...........26.....5..2....82...5.953.....
..8.5....65..1...4......1.7.....47.9..2.......3....8...6.3.....8....75...9..62...
....92...5...8.6....63..1....12.7....2..4....9..538..........8........977.8.....3
7..9.2..53.....9.7.4.7...8....2.........1..3...46..21..1.......2.7...6...3...1..8
.2..58.9.5.3.6..4..6....8..1...3.....9..1..2....5....7...9........7.....6.4...5..
...6...5....3......2..947..6.9..23.8.1.....26.......4.3....6..9..89.3...4..27....
...4...62.5.81......7......1.29.8.........3..9...6.....241..6....1..67..6.....23.
8.......1...95.................7.42.3.16...............4....57.6..3.8.........2..
.472.........96..1..2........6..4.3...8.1.......8........9....36....274.7.4..8..9
..9..1....7.8.....1....6.3.4....36......5......5.7.24.....6...8.3....1.26....8.5.
..2.4.......5.1..39...8.....1..3..78.9.........8.1...6..5....8.3...2.5.4471......
9...4.5...2.....1....581....8...76..3....4..5.5.....97.......6..32..54..1....2...
1.2..49...4..9....9..7.1.....45....6.3.........8.621....1..9...4..1..5...6....8..
.6..3....1..2.....2...7..5.9........5..8...41.....29.8.......64.....6.....41.95.2
........185....67...64..5..6....2..3..467..1...8...........6.....3.1..49..1.34...
4..8....37.......4..372...6.2.....6..3.5..7.....6..9..8.....4...1...5....5..9....
..24...9..7.3.....9.4..13.5..8...........5.1.74.....2...186.9........4.2...2...5.
....9.......681.4....4..2.1....3...6..1..........26859.47.........9.5...2.8...1..
.....1...9.8....3....36.4...8.1....3.7..5......2...6....3....9.5......84.1...5.7.
.......7...63...1.8794..3.6..8...1.9...26.........45..72..8............3..1...6..
..........73...5...527.8...1......9...6....4.9.4.31..........23......76....6.94..
.47.8...1............6..7..6....357......5....1..6....28..4.....9.1...4.....2.69.
.4..1....5..4.8....612........1.7..3......5..4.3...81.9........7.6.3.9.2....697..
1.....6....769..42..47.....51.9.......8175..4....8...6..1...8.93...17............
....935..........82......47......8...6.4....98...5972.4...2...679...........1....
.362...8......1.3...7..5....1.....4....1.3.5.....6...9...9....847....9..2....4.1.
.3...9...8.5..1....4..8.......2..6.8....7..4.7..4..3.5..1...8...7..5421...6....53
....6...8..2......49....31...6.34........85..94...1......2.94...8.......51.....3.
......82..18.36.....7........34.1...6...7..89........28...4.76..94.5...........4.
5..........42.8..3.....3......6.54...9..3......8.49.........5..7.....64.6.2...17.
...2..7.6.....614.4....8.2.38.....9...53.1.......6....5..9.23..2......7..79......
..4.98...5.9.3.......7...4.......92.3.....8...82..95..9....6..3.2..537..1........
..3.8.2........6.....6.2..1.....9.....7.3.4..94.8.......42..3..718........9..5..8
..3...6......24.....43.1...23.8..4.9.4......87....23......5.89.....7..1.5....3...
.361...2.8...6............7.....5....9..213....4....19.2....7..5..894.........1..
.3.6.8....47..........1.89..7....18....8.23..6......5....4.15....8.2...6.1.......
...2.6....7......59.....34...7..1......6......5....2.3.9..47.3.43......8..5..9..2
....8..5.93....7.....6.1..2698.4.5.........4.5.....2.84...2..7..69.......52...9..
.152............86..4..........4.1..9......3.....1....6..8.9...37.............5..
..1...6.....9...3....5.....6...24.......3..97...1..........24..15.......97.......
.....2.......7...17..3...9.8..7......2.89.6...13..6....9..5.824.....891..........
........4..415..9.9....6....26.75.4.......9..4......8..7.......64..2.7....2...3.6
5....82...2..5.9....69....8..18......4.....72........345.1.9....19..48.......6...
9..5...3...4..3..2....21.5...6.1..4...3.69...2..4...........46978.2..............
9....8.....6.9....3..4....1..9....478..67......7....235......1...316...9.......7.
.761.9...9...6...1......4....5.2....3.......57....523.4..6.........1.......28.7..
....9.7..8....3.6.7.3....2...6.471............2.1....5.9.6........5..68...4....5.
........1.6...379..9......82.61..5......8..2...93....7..2..7.4..5.2.....7...38...
9...2.7...4..6........8.3....8....2.....9....51...7.....1.75..6..........67....82
19.........2..4.793........45..........28..6.2.....73....17.6...4.63..1.........5
12.5.76..8.....4.........5.......9.8....2....7.3....2....8....6..96.38...7...2..4
....4.....14.....6..29.3...2...7..9..9....5..6.5..1..35.....72...6.....1.....7.3.
.....8....3...57....4....61....6.3..7...2....9.2.4......1....9.37....5.....3.....
......6.2.3.8......1..........5..73.9..4.....2........5....6.4.....2.1......9....
.5.8.6..........27...3......6.5..8..7....1...4........2...7..........38.....4....
.5.....8...4...9.6...6.9..1...5.7.4...2.......3......7..19.4...2.....5.4..5..8...
6..........574..6.94.8.......4...2...6...8.4......15.7.3.........7....24.....3..1
2.6953........2....8.....3......9......3..1...53.4..7.1.2........8.....1...4..65.
.2...6....5...72...6..81....1...53....8.9......9......4..6....8......7137........
6......5..1..39.6..8..2...4...8...........9....1..5...9......4..2..7.........4817
..47.8.....8.....2...6..1..3...54..7.....9.....9...5...87....3.....13..4.2.....6.
1..3....7..6.9.....4...5.....3...8..6.1.3....7...6..35.....67984.............8.1.
1......6...72....49......7..3.49.............69...8.5.32.8.7.....6....1....5.683.
.8...6.....9....2..6..1....17..2...33.....471..............28195..3........14....
...4.8.2..3..9..8.....6..94.....5...6..8......12.36..8..1....6.46.5......9.....1.
7.....13....1.64..6....7.8.429.........2.........8.....9.81..........6.9..53.....
.5.6...14.1.7.3..........5...1...63..69..2......3....26.2..14.........2...3.....7
..67......1..5..863....6...6...1...2159..4.........8.....8....7......3...216..9..
.....37..8..72...1.......632...5.8..4...32.......6.3.......9.2...8...4..74.......
..874.9..1..5....7....2...5...8..49.....7....62.93......3......78....1.9.....2...
.6.28......5.......7....318..165........2...5.....7..6..9.48...78.....3.2.......9
....3..7.9.1....52..7.....4....9......2..8..96..7...2..4...6.....6.57..13..1.....
.67....83....4....58....1.26...9...882.5..9.......7..........36.5.8.....9..4.....
.8....1..7..14.2..4..............5.3.4..7...8..64.1.......6..........8.5.53..2..1
9.....2....7.....3.6.2...8.........2649...5...517...6...4..59.....1.46...9.......
1.2.5...4....2.58.....9.2......7.94.518.....6..........952......7..3........69.7.
...7..58.5........4..9............54....31.....8...9.6..7.9.41...1.8.....6.....7.
...45..2.1.2.....4..9........7...31...12.59..........8.....7..6..8.9.1..39.1.....
........934.........6924..........57.8...1...17.....2....26...3.....9..6...8..27.
.........17.6...3..8.7...599....47..3.2.1.......36....7..43...1.....9......1..8.4
.34...8.7.5.8....41....6..3..3....45...6.12.............832.7.....9.5.....5.....9
.4....7.....7....1..5.21..6...8..9..6....2..3.3...5..83.164........5......6..82..
..9..25..13.......8..97..........61....6...4......8..2.......575.21.......6.8...9
.53.......21.8.3.......1.245.28......7.63..........9...6.75..38.........7..2.....
..74..5..6....2...............71.8..2.....1..3........5......3..4.9............26
..6........48...1........5..1..7..349..........5694......3.76...89.6.5.2....8....
.6..1.3.2..8.........9....5.2..6....4.............2.713.7..94....5.........7.56..
....8.7......9......9.4...34.8.....2.5..37....7...5.........61.19.........2..3..4
.....45..6.47...9..1...8.4....59.....5....938..7...........23..1..4...567.6......
...7..35.6.1..9......38.....7..3............65.9..4.8..56...9.42.......53......1.
1....6.8..64..........4...7....9.6...7.4..5..5...7.1...5....32.3....8...4........
.7......5.........24..5...3..97.5.....28..67......92...6...8.4.....9....9...1..2.
.5..812.....5.......9...5.......3..8.1......9..8.9.41.4...3876.8.7.6.....3.......
.9.....7..6.....9...1..8.......92..6...8..4...34.5..19....1....4.....1..5..38.9..
....2...59..3.1...........9....7...26.4.........4.816..9.2.5...4.6.......1...78..
7.1....4....8.56..3.........8.6..5..1......3...........2....8.....47........1....
..4.81.7...3.749....2........5.2.1.....8.6.........4..4...6.51.......6....1..5.29
....714.2.........2.7....3..4.19.25..8.......7....3.4...3..7...5.4....9.....2....
9..4..3......89....3....5...81.7.........57...........5...371...9.2...8...6......
27....1..1...........5.......53.8....3.4...........9....4....836...1........2....
......52....3.1..4.4..57.8.286................3.8..91...1....5..9.7..16..5.....7.
....4...1...2.9..3.731.........8.62..6....83.8.......4.5..1..9.7.16....23.2......
....1...78....562...5..7....58.7..1...26...........7.6........14....38....3.9..5.
..8....47.1.3..8....5.......5.6........2.9...83...4.9...6.8.1..7....2.......5...3
6..3..2....7....49.........32.6............871............47....5....3......9....
1.7..259.4...8.7....2......54.1......8.7..6........94.....7.....65..94..3........
...6...34.....96.....4.89....395....4......2.6.7.....5..1.........5.1.9.....2.7..
...5...........9.1.5...4...6..4......73...8.4..2..6..3...7..6..9.....7.2..48.2.3.
.68..7......3...1....9.2.8...6.5.247.147..5..5........7.......4..5.9.........8.2.
....5...9.6.....3....3.941.3..6.....6..8.1..3.....5..7.315.7..4.5.....2.4...8....
412.3.....7.5.............43.4.98....59....2....2..9...6.78...384......1..7......
....7...1..6.....5......4...9....5..6.81.5..........8731..9....76..2....2..31...9"""

  medium_data = """.94...13..............76..2.8..1.....32.........2...6.....5.4.......8..7..63.4..8
............942.8.16.....29........89.6.....14..25......4.......2...8.9..5....7..
.....7....9...1.......45..6....2.....36...41.5.....8.9........4....18....815...32
.5247.....6............8.1.4.......97..95.....2..4..3....8...9......37.6....91...
.9.........1..6....6..8..7.3......1.....39.......5...217.4...28.....3....86....57
.....5....2...4.1..3..8..2......84..8..6......9..1.7.5..6......95...3.6...3.....1
5...68..........6..42.5.......8..9....1....4.9.3...62.7....1..9..42....3.8.......
.7..21..4....3....6.1.....2.......6...86..7.319.....4..1....2.842.9..............
........1..7.5.3.9..48...2...........3...57....942.........3.....1...4.7.6.278...
.....8..3.16.2.9.7.3...46...........9.5...2...2.13...9..3....2..7...5.........4..
..4.2..3....8.9.........7...5..37..8........5.49.6..1.5.........68........7.4.9.1
.....6..3..9.4...532......8....1......175.6.92......8.....6.......8...4.47....2..
.....8.2......693..98.7...1...........921....7......9624..9.......3..18.........3
..2.46.....4.8...5.7..3...9.....2...3.57.....7.....4....6....93....54.78.........
..3....4.4..2.........9..26....7.....1.9.2...26......85....7.......6.8.33......69
........3..5..2.14....8..6..........946.......3...42.6...7.........3.68..7.291...
.2............48...54.18.3.7....1..4....86.5.......6........1......2...923.4....5
..9.43..........3.41..7.............8..5...6..4...6..2.......1...4.98..67..6..52.
.........4.6.7..9..5..382.........3.9..........426.....7...3..2..16..8...85...7..
...6.4...........3.1...26....2......6...9..158.4.....6.....7...976.5.......2.31..
....4.....5......9..3.784....1......62..........5.38......2......64..7.34.51...2.
...3.56....68..3...4.............8.5.5....412...9.......3.9........8..6..196.45..
.2...7..5.........6...95..1.7...413.......2....1.5...67...1.8...8..7.......2...49
...5....3...82...13....179.17.............3..6..712.4..4..6.....9........6..5.2..
3......4...2..8....912...3...5.1..8..64.9.........5..618.7............65.7.9.....
....4....1..9..64..3....8....7.........1.859.......3...52..1....1.7.3...39..5...4
4....9.....541...3........7.......2..31.7...89.6..3.......9....1..6...8...75...46
.8.4.....13...............84....1...5.7..2..3...9..1......2.78.2....6.3..76..3..9
.5.........6..5.91..9...38.4.......8....38..2.73..........1....28.47.5..6......7.
.1..6.9....9..5....3.....76..1.3...272.....4...8........73....93.5..76.........2.
53..97..........7.....1..5......13....4..2...1.98..2.4........5.7....92..91.5....
..........7...62.81......54..3.5.......3....22..8....69......8.3...7......7.254.1
...6....445....2......893..97......3.63........4..27..6.9.5.............5....3.61
.3..1........427.3.2.9.6.4.5...2....349..............1.....9.....6....8...5..346.
....6.....5....97...2..5......2...8..74.......85.4.2.1..1..7...6....4...92.6..1..
...............731.541....8......5...219.4....4..6...7...58.........7.9..98.1...2
..8.........63...4..1...63..3...9...4......62......14....5..79.17.........54...83
.........9..1....2..4.28...65....7....1.....3..97.2........5.7..4.....61.35.1.9..
.....2....134.9..27.9....15.....5...1...8...6.6.97..8.5....6.....2.........2...3.
.....8..9......28..3..7.....48..........2....6.7..913......39...9..1.4..57.6....1
...71....5..............53.16..2.3......3...9.456......9.2...7.6.....2.3.....6.81
............8.5.492...6.3.1..9..........21.38...3.......5........6..48..13...96.2
.....2.73.8.........57..2..9......1.8.......46..815.9.......46.4.....5.2....96...
..........7.48..9...4.2.37.1....5..2.....3..7..3...64..4.........631.........891.
.............67.....7.8..12..........3...65..5.1...893.7.........9..1.24..439...8
.......13....4......4698...........8.3....7...28.69.....1.3..6...92....76...8...1
.......1..2....93..65.3....94..5......78..2..6..........12....4...6.98........127
5.1.83..7...72...........1...8....2..1..5.9....3.....1...9...8..4...75..39.4.....
.5....8...1.....32..8.....6.9........4.8..6.5.....7.....2.7...33....1..4..562..1.
..5..1.8..4......9..7659.1........7...42......1....8.6....35..........9.97....1.8
..7....3..5...9..19.........2.......5...3..29.8..741.3...4.8.....2.....6....158..
....5...........4...36.1..8......7.1.2..1.8...7...9...4....3........659..59..72.6
9.58...76.........7...49.3.........9..1..82.....37.....7.......43...5.8...8.9...5
...1......98.2...63...4..5.5.......3.61.........7..86...7.8.3..........9..52..4.8
..3..........285..2......7......2..4.1.....2363...1.571....4.8..5....9...9.7.....
.7.....9....4...82..21.9......5..4......1...71.36......2....3....5...1..8.1.26...
.6........4.7...8......613.1..4....5....2.8...5.....76...2..3..8...4..2.79...8...
.......5........21.39......4...51..7.17..49.....36.5......15...9.....16.64.......
3....75.17.8..6......8....38....479..9...........23...962.....7.......6.....4.9..
17.....36....9..4.3.6....8.6....82.12....5.......1....8....7....5...........51.63
.........7...4.....9...612.4...1...7....2.5..5.1.98........1.6.....6.28....4.53..
74..6..3...2..5....18..2..9.8..2.6..9......7...4.8......37.....6...9.....2...4...
9...6........3.....3.8..4.6..5........9.8.3....4...297.2......4...3.....68.2...15
.5367...9.......5.....2..16.....37.29......6....5......2..1...51.6....9....9...4.
.....185...2..8.313..5..4..641......9....5..........8....9.6............5.9.4..72
.....5.3...79..1...3....7.5.51....978....1.56.....8..........28.74.2.....9.......
..1....8......45....5.7......273..........2..358.1....2.3.56...9.......1..6.9.7..
.4........12........82..537......2..3...8...4..53.7.......4..6.9......7.2..79...1
26..7..38....1..7......46.2.1...5....9.23.4.......72...........7......8...1..87..
..1.2.....8...5.9..6.4..1......8..3.....42.5..97................7.....4..32.176.5
..8.91.6....24....9...7..2...2...9....5....8.8..63.7.......7..1.56...4...1.......
...3..59...9.....3....6..7.4.8.1........9.......52.9.86.....7....58..3..1......64
.51..8....7.692.3......3.....7....92....7...1.6....45...........9..8.6..64.5.....
...3.....8..6...154...5.........4...2...6..8..7..9.34.....2...9..1..84..7.8....2.
.....3..1.4....83...5.4.....641...8..1...7......3....75.9....6.....3..5....87...3
.28..5...4..1..........3......4..85....2.....1...7...37...9..4.98.5....656...2...
......5..3.........9..18...1..9..26..6....4..98.1......7.3.........2.316.4.8....5
............1.962..6...7.59..1.......9.8.4..2......346..8.....19.6..3.........58.
........95...6..3..7...25..............7.4.6..32981...........8..5.2....76.39...2
.....6.57...5.....1...8.3..8...32.....6.1.59.........6...1.........2.97.5.17..8..
....16..7...7..93.2.7.....8839..........38..15........7......8..5.1........5.94..
4...187..8.......2.....4..............6.53..1..726.43...1.7...6.3...1.8....6.....
.....24..5.....9.8.2..65.7..8..3...1.74.......6......9.....4..5.......3..12..78..
8.63......13....9....6....27..........5.6......1.492...3..1.........2.47....368..
....91......2..87....6..1......5........6...3..79..2165......2.28..3.5....3..7...
.9.........8.2.3....6......5.....4...1...528......4.73....6.83..6.1...2.18.2.....
..5.......17.53..9.8.1...3...4..1.2...2....95...38.6.....7......2...43.......9...
....6..59.84.1.3.......7.....8.........3....15..4..9..4.........5.78.24..97.....3
......9.2..9....1.....65.....7.2........5..34.2.4...98.5...1....8...7..3.16.....5
.8......36.....9.7....5..6.....9.......4.36..159..2........8.9..2...1.4...35....8
1..9......8..7.4..4.5..2...........39...36.7.....1..9....24....2.45.1..8......7..
..7..6.........1.4.4.2.3..94.8.....69..81.........9..........3...1.35.8.2....85..
..43..8.78....2.3..3...6.....69.5..2.9..7..4................5.6.........389.5..7.
..42..7..2...6.......3..1....5..7..9.8.6....74.9..1.8..........61..52.4.........8
..1....5..36.5...9..79....6.......3.6..8.1.......6.1.5.........598.2.....2..73...
.....8.13......8....7.2..5..3...........965..5.8..7.21.5.3..4...........8...51..7
8....3.577.5..63....2..4......8.9.....9.4.2.1.63.............3...4....7.2...9....
7.......3..8.3.2.......7......9..4.79..46.5..36.8......3.5.......1....2.8....91..
.....1...1.8.4.5...6..9.4.......9.....97....14..1..23...........574.6...8.....3.2
.9..4.2..........35.69...........15..73...4....24...76.2...1.......9.7....5.7..4.
7.89.......6..8.4....25..3.......1..6...1..2..7...5.6.....7....92...3...1...8.6..
..86.7....7...541.9................2.4.2...8...7..35........6.9....5.7...52.9...4
..........2..4...3..1.97.5......463.71.2.6.....2.........6.....2....53.7.3....9.8
...9...4..81.....5..4.52......6.93...7....8..2.......4........16.3...9.....1.6.28
7....6.5..6.....4....7...8..4.......1..3.......3..24......73.92..8.6....6.2..13..
.....2..5.6.5..8....91...3.752.........38.......7......38.....1.....4..342...86..
.7......5....2.9..53....7....924.....285.9...........1.4..1...7..1....437..3.....
...3...747....4....2....15.....2..9...36.....5...9..4.4......6..9.....1..7126....
..2.4....68..51...7......8.....3...5......9..2.59..7.1.....9.78.....6.9...63.....
.5.3.........8.49.8..9...6.97....2.........174.6....8...8..........3.1...94...67.
1..28.59....5.6..17....9..2.7.4.8.1..3.....4...2..........9.....53...........4..9
..76....14...........8.4.92.9.....5.68..72.....2..9.3.......5.6..5.238...........
24......9..3..5.......67.3...5..4...9...8.27...1.....6......6.4.8......7...27.1..
..325.........85.....7....8.......693.2.4....768...1...........8.......45..821.3.
............8...37.98..12..........6.65...9..8..4.53....4.....2....8.....72.561..
..2....9.....1.3........1.7..4....75.8.5.9.6..7......8...1.4.......3.5..1.5.67...
....6..5.4.631...........8...5...46..1....52...3..2...9.........247.....1..25..9.
...64..5..4.......5....8.......813....3.5...81....2..57..........54...36.82..5...
......6...34.9....6....8..3...6........4...5.25....1....8....4..96.2....1...8759.
......29..4....6....7.58...68...7...1.2....6......4.8.............4.19...5.78..13
......9....9.14..664.37......2..1.3..9...5....1..6...72..4...7......68........6..
.6..7....5....36.14......9..94.2..7.8.......4..7.6.5...........3..1.4...756......
7..........9.3....4.8..1..7.......8....627..5....45..95.3..4.....2...6......7.9.8
....1...8.9....7...6...5.....6...3.2.2....4..51..8.....8.....7....6.2.3...3.9..61
6.57....11.......8.9......2..1.3......7.4..6..8....9.5.1.9.3........5....74.8....
............1.5....4...8..2..9..31......1....68.75...4..7.6..3..9....7...54...98.
..1..9..6.....23....96.3.24..........58.....96..7....1..........4..3.7..16....5.8
.7...1..5.....5.4....3.2..1..8.1.....35...6..94.8....3.2....8....9....6....72....
..48.7..31......6..9....8..8.6.....2....1..3..5.9....1.....654.6...5....4....1...
..3......261.........376.......2...4.....9..5.75.4..86..............8..9.34.9.17.
.4..6.17....52....1.......8..8.....5...8.32..627...9...1......6..4.52......7.....
...2..4.......82.5.51..........148.....9......29.......3.1...7...857....1...2.6.4
5.1...3.8....7..2.......51.65.........9..2..4.2..9......47....32.......1.1...6..9
2......8....4........9..746.6.2.5..4...3...7..4..76.2...3.1....6....8....1......2
.74.81.......56.9....4...3....9....1..7..53....6..........2.....3....217...89...6
..7.18..9..4..5..1......5..9217....88..5........4.9.....8.....76.9............28.
.....8...1......95.5....3..2.....64.6..81.....9.4...3..4.......9.6.......3.524..9
....4....3......62..12...3.......52...8674......8..64......18....9....1..6.7.9...
.435....7.......2.25.3.9.6...4..58.1..1..4...7............8..9...21.........3...5
.....1.3.....7...93.....8.19.......7..7...18..2.64......2.....5...2...9.153.6..7.
......9.1..4....7.1.....52.....9...3.73...2...9.75......81...6...19........5.7.32
3......5.92.......86..7..4.....48......19...3.8.6...9.......4.1.4.5..739.....1...
..2..7....1.....3...8..6..4..4....623...82..7...56.3.....4.5.........27.8.17.....
..5.....6.46.9.3..81......22....7..85...2.........6.54...9.....1..8..4.......21.5
.........3.5.4...2...26...8.1..........4..9.5.7.3.62.17........2...184..6..5...8.
....9.5..92.3......7.6....4.....8.5.....3...24.1...69...7..2...1....3..5..2...16.
............14..6...7.59.31........7.3.4..5..8.2.....9.169.4....4.2.7..6........8
...71.9....2....1....9...26.2....3...4569....9.6..1.....8..5....7.2.....2.....53.
.53..617...........6..98..22....1..4.4.8..3.9...........1....6...97..8...2....9.1
..4.8.....5....26491.........7......3......57....54.1.........12..5..6.3.9..438..
.....6.3.....1.8.27..3..95..1.6..3....52...94.389.....1.......5.8............54..
4...7.9.........5...5..9.2.....4.7.1..8.......2..875.3..3.......9.....7818.4...3.
.....17.......6.94.4.35..8.....8......19.7...93.2....5........9...5..47.8.4...5..
.53.2.1..1.....9.....47..583..7.8.....2.......4......9.6..9.71............75..46.
1........7.2...64....2.7.8...5..9...91......3.....21.6........4287.......6.9..82.
...3.5.....7.91..8......3..48......1....835...92...4........13...1.....4.4...9.25
..5.....78..96.....3....9....1.......5...3.28.7.....14.2.6...9....2.8.6...4..9..5
...........74....2..3.5...8.........9.6...5......6281.3....81...9.17.3.475...4...
.64.9..5........18.8.3.2..7425..9....1..3.............3.....7.28..2....6.5.7.....
.....4.7.....2.1..8...6.9.2.26..........3.8.7.5...1.....3.7..1.6..892..3.8.......
....8....1......9..2913...6.........5789...1...236.........4....1...593.4..6..2..
..6.9.........8.5274.....8.............9..5612.3..147............8.4.635....79...
........11...5..8..9.1..7.4.7..8........49....3....479..9.36.....1..8....2...4..6
92...1.4...1.4..2.5..6.9.....4.........314.9....2....3.3....5..4...5.8...7.8.....
........41....4....2..7.6...926..4......39.....7.5...29.3....2....9...4.51.7..8..
.7.6....8.4.35..16.6..19.5...7........6.....5.9..74.....2....9....8.1....84......
.........34.5..2...9.314................71.94..46..5..6.......2.17..8.6..3...78..
....526...1...7.....6...2.1.....3...1.4...5..7.289.....819....3..3..5.8..2.......
...5.1.82.5...9.....7.8...6276.1..5...5......3.....7.........6..839.........248..
.......9..63..2.8....46.7...1.9...65.5......89.8......8.7....4...51......9.7.4...
7........14.9...2....5846......3...8.......4..93......8.....1..21..483....7..1..6
9....2..76...1..4.......532...4.....2...9.3...5...68......5....89.....7..7...861.
......1..72...6.4.13.......4....3..2.6..9......8....5.....2739....8.....87.1..4.6
96.14...8.45...9......2..3.....82....5...6...4..79.25.......4.3..4.....9.1.......
6...5.....8..........4...73......2....93..4.7.1.74..5.7...3...2.91.6.3...4.....8.
....7.6..156...........2...8194....3...1..45............7.5.....6.2.7.8.3...68.2.
..1..2.76.3.......287..14..........8.13...92.7..2.4....9...........85.......3.8.9
...........5.2...9.93.4.7.6.........5.1..8..4...2519....2.......3.....1..849.62..
96.............2..4.59...7........125....893..7..3...8...5.31.....19.....92.8....
.........9.48..6.....714..2.2..6...53.....2..6.81.7.........1...43....5...1.3..6.
.2..94...3......4.8.95........4.2681......4.3.......5...3.5...2...1..3.......61.5
.........4..87..15.3....82...9.3.....8.....6.2..15...3....6...7..7.85..93.....2..
.....4.899......6.....9....4..2......5..3.72.8.7....4...2.....879.3.......8.1.4.6
.......8.3...976.....8.39.....5............3...9.482.5.71.....2...4.....635....47
........73.......87....63..........4..6.27.8..8...5921.51.7.....6...2.3......8..5
8.......64.5..8...1......3.......2.5.518.9..........78.4....12...63...49...4.5...
..8......6.18.3...42..5..........82...62.879...4....1.........37....4....593.7...
..2..1....3...4..5.9...7.12.5.93...8...7.6...8.......6......16........5.9..15...3
32............86.9....54..2......3.8...4...2..85....945.1..6.......3....462.9....
.4..5...6...8.6..3..7.4.....2..3.....5...493...6..8...8....56....43...9....9....1
.3...4..77..23...6.4...5...1...2.......9.6......3..8.5..4...9.......92...95...7.3
....7.6..3..1..5492...8............1.6.7..48...58.4.......2.....213.....43....1..
..69.....1.7.5.3.........5......4..3.8...3.72..1..7...8.5.764...6....1....91.....
....7...41..58.....9......2.35.4......87...91.......3..5....1.8..63.....94...6..3
...6...4..5.19.....13.8...262......8.71......9....4.71.....8...8.....3...6.53....
...........1..2..335....8.6.....3..7...1.8.......4.539.98....2...53.....2..6.9.4.
..2.3...58.....9.4694..7...4.3.....1....8..........29......6......2..31.9....5.62
5.......21...6.5....6.73..8.5...9.2.....1...7....8...9.3.......28..3...5...4...31
.4...95.39.2..7............43.........6.7.3....894....8...94...5......86...7.6..4
..932..6........4.6...4.21...38....4........9.81.65....9...35.....1.....7....2.9.
.......85.81.4.....37..1..4....13......4......2..6.7.....6...4..9...7..1..3...652
...638...3....1........5.8..2...7....8.5..47..4.....2.....9..4..9.7...1...4.1.26.
...1....8...35.....5...9.........4..4....8.9..8.23....6.......77......3..34.76952
...2..4.5....6.3...6...8....1..5......48327.9.3.6....2.......2......35..7.8.....3
..........76..1...8.2..6.5..9..7.3...6......214..6.9......14......3...2...59.2.7.
.65....3.4.7....8...8..7..1.2...1.....68.....9....6........3...7...6.41..14..8..9
..........45..9.2...2..46.1...2...4.4...1.....9...5..7.2.....1.5..7..46...8.6..9.
....8...31......25...69..84..3..2....2.8.9....9..7......1.....9..7.3...63....8.4.
.21..6..4..5....2..6....3......314.....4....85............7.9..8.25.4....3...264.
.3.........2...6.16..5..2.8....1..7..1....8.3.....4..6..36....24..87....2..9....4
..7.6.....5.2..6...6....1.2..3.8...48....5.....1...2.3..2..3.41..........1.75.8..
.....3.6.5...18..9....7..8...9..4.......6...1..6....53.48....2.12...79.....2..7..
..4.56...3.58...9........6..4.91..86.....2....2.7.5.3........1..8.1....4.....4..2
.....7.....6..4..99...6..5.....9.......7..3.22..8.1..7......13.65..18...8.3...7..
..7......4.31...97.1.6.9..5.....2..........8....5..9.6.........9.641.3....8.67..4
..8.....7..63...8....1.5.6..839.....97..1.5.........2..67..2...8...9....4....68..
...........3..68.5.4..8.9...3..7......4.1..7..8.9..3....84....7.7.83.2......91...
.....3.4..7..9....438..5......5.2.1...27......4......8..9.3.82...3.4..6......7..3
..........3.6.......4.2891.............497...82...147..........6..239..13.....846
.8...5...3......47....2.5...2.5...36......2..43..9..7....4.3.1.6.8.7.4..5........
..........4.18..5...89................1..8.495..4.3.26..7......3....9...9..53678.
.6...53..5..4...8...19..........7....9...4.57.58...16...4..3.9.....5..7.9.......8
.............7..5.516.28.4..........6.3.....7.89.52..1..8....9.9..6..8..76..1....
......4...942...5.....5..7.47..1.....5.....3...1..95........2...267..1..7...8.94.
.......9....69..5.52.7.........3...9.8.2.53...4..8...63...46..5..1......2..3..4..
..3.2........8..758.13....696.8...5.....124..1...........6...3...693.8..........7
4..7.1...75...3..82..........51....3....6..5.38...5.47.....4..1....1.8.2.......3.
..........1.....47....563.2..........2..1..3.7..642..1.......1..73.25.8.5...3...4
.73......2....6.....4...3.9.......8.7.1.8.4...2....761....1..2...6.2.......938.4.
.6...3.2.3..9...4.4.....5.8.........2...3......6..23.1.7.46....69.........82.7..9
.6......23....2.9...1...576...........26..31..8.3.54....7.96..8.....7...1...5....
2......7.....4.....76..9.....1..5.9....6....59.....64.6......5..3..8...7.5.3.41.2
.......5...1..46..9...7...8.....7..971..45...4...8.......2.9..7.4..1..6..7....1.2
.....1.....2.8..7..6...4.38...8..1...45...7..7216..4.3.......1.....9...23....6...
..3......9.......4...6...31...8..........73..8.423.56..2...8.1.....5....6981..2..
7..3..2.9.8..1...3..2..65...28.......5...41.....1........58.........9..26.3..2.1.
6.24.......49..2...9.3......59.....1...589..6....1...83......8.....2..5....6..1.4
6.......3.9........52..6.4..2.7..........51.6.79.3....9.4..3.52...9...3...1.....8
..........28.7..1.7.46.......1....9..9.1.4.8.5.....3.....41.5..3....9......7.36.9
3.......71..9.8..2.49..........3...1....523.......4..6.....7...4.8...15.6....9.84
....18....1.63...........897.9..62....2.....58...5.3......93.4.6......3...14...5.
.....8.....367.......91.76.....4.89...8..3.5.....9..7..........31.5......452.9..1
6..........537..9.....1...7.....2.4.14..5.....83...9....6.9..........32.93.48...5
.......1...4...3..36.5....7.35.284.....31.......74.....2...7........15..9.7...8.2
.21..9.....7.1..6....8..31.......53..1..9584..7...8.......3......94..1...6..2....
....5..345..7..8.9.....9.....9..3.....3.....56..8......1...8...7...6.4..9.4.2.6.3
3....8.6...2..54.9.76...21..4...9.....7...9...1.82......93.2....6...........71...
.98.....7.7..8..2....3..5..2.........3..7.....65...9..........46.7..3..89...4625.
............863.2..912...8...........27.......14...8.7....9...3.....5.1...9324.65
..1.....37....2..5.3..942.8....4....2..6..9...183.........17....7......639....5..
.79....1..3...56.7.....9.............8.5....251...6.4..2.8.........714.....29..35
.864.....2...8.....4..7..9....5..6.......19..3.......5..3.4.71..6.....39..8..9.6.
.....6.....3....72521.9.........7..8.98......7.....426..46.37...6.8..5...1.......
3......6..6..3..7.7....5....3.5.......91....4..8....21...6.........9.41..5.81.63.
.5.923...7........92....1.5..........354...1.6.4..53.9.....8.........27.3.8.1....
..........6...1..31.3782............5.29..6..98.57............6.91..6.38..4.....9
2..1..63...4.......5..36.....784.....8.9....71......4......5.....8..97.3..5.8.1..
1.6.......3..4..1..87.2..5.....31.29.7....8.......43.1.........918......2...5...8
9.1.....8..4......3...64.......3.5.7.2.5....1....9.32...28..73......59..13.......
..........1...5..3957..8.2...1.....8.6.4.9.71....57............7...96....35.4...6
.....1....68.3...2...72.3...91............4...8.4.965.5.6.....3....7.8...4....76.
.......2...3..7........147...8......746.....3.5.4..2.9............1.4.5.1..2358.4
31....8..9.4.......7.9...3....69..7.16..7..2.......1.9...5...1.4.72..3.......3...
49...2.....3...1.....716......2..6....86...1.......39.9....32.....49.....5.1..47.
........469.....57..8...2...........2......8..4.3917...5.........3.2..457.2.653..
2..7....6..7..58......16..3...4.8...1..62....9...37....5.......3......2..9.3..1.8
..6.......289....5.....5..7........6..9.14...4....397...5.....3...8.9.5..1..7..29
...3....7..1....4842.........9.....6..86..2.3.1.9.2.......96....9.17..5....2...8.
..9....5.1..4....626....3.8.2....5..7....6...9..823.....6.1.2.......7.9......4.3.
.......7.6.21.....341...2..5....97...1.2.8..4.8.............1.....36.4.8.5...1.6.
....594..2...1..7...638...9..2.3.........8...6.5....2.3..49....5...2.38.........4
....73.2..39.............41...34...6.5.1..9..........25...974....4....7.8.2..6..5
............53.2.8..5..24....92...15..3.....4.863......3.748....78......6......4.
....9.....8.....5....2.59.62...........4.71.9.34.5.7........36...3.4....5.9....12
....2......31.4..7.4...76....48....96.......8....6.71....3...4.9...16....5..7.9..
.87...129..2.4.....3..............91..3.......2.75...4..4.17.3..5..........4.97.2
...4.7..17..95..8.2.....5.......18..5....4.9..2..6...5.........98...6.3.1..74....
8.....9..5.3........69..3...1...2..3....9.82..5...719...2.........751......3...86
..7......1........8365...74.1.....57.2....1.3.5...9...5...6.......1.4.......5.268
589..4....4....8...7......63..56...9...9.32......2......7...18.6.5...........96.2
1..3..8....5...2419.............9..2..6..2.844...6.3.....9.7..........6..74..6..5
...5....738...79.62...9..............629....1...34.2..5.1...7...78..........8.31.
..2..7.6.1..9......86..3.5....5.........3.7.6.3.6.9..4.65........8....93....1.4..
.3........68.19.3....47..5...........9.....26.....61....7..2...9..5...1..82.34..7
9..7.......1..8....85.......94.2.......1...5....94573..3.6..97.....31..6......8..
....74.81....3..46...8......5..19.....83..6..9..5.7.....2....9..6.......149...2..
.....9..4.....67...57...93.....2.....98.......4......5..4.9..1.7.21..5..1....4.78
..5.14....1..7......8..96..1...53..9.2.....7.9.6..1....69.2....8......9......7..8
.7.....2......1.5.6.2.4.9..4.6......8..4.21..3...5.2....3...68....73..........74.
.....5....46...7.51...36....5.2...4...13......3.4.8......9.4..2.8...........279.6
....8.3..6.2......5.1...8.......41.....896..44.......6..7.5.2....6....9.8.4.71...
..1.8..........7.4...352.6.1.....5...6..3..97.5.6....1.74.........2.........46.53
.9......25..4.2..6......518..69.........17..9....45.2.9...8...5..3.......1.3.9...
......917.54....3....8.....8.......3..2.3.69....41...2....7..2.1........467..9..8
.....4....3986........91.....6.8......4..25..25.....968..91.3...2....7.....3....8
9......8.....36...1.....2......487....16.2.483...7.....69.........2..67.78......4
.....3.9...8.....63...2..7.........2.1.8725.....5..64..5...7....2...98.3.4..8....
.........8....9..671..2.3.......1..5.5..3...8.6.74.2...36.5..1......3....7..1..3.
.........6.4..17.93...6.2......9...6..6.7...22......1..9...7..1...8......8.529.3.
...6.....93...5..1....18.6.1...6...2.....2.57.9........57.8.....1.2....34....3.8.
.1...4..5.3...7.89.859.............16....974.4.85......4..........27........35..8
..........7.12..3.9.....876..........58.13..2..39..7....4....2.2...3..8.6...97...
...3...76.8..9.....2....15..39.146....6....8...4.2........7...535.....6....45....
..84.9....7....85.........4..5..4.9.....5..131.......8......6......27.4.3.1.98.2.
.......1......1..8.92.5...3..........61..39....3.2.561..4..........17.8..8.4.6..7
8..6..95...4.........9.4..3.7.....8...8.....1..6..24......9.6.2.43..6...9....35..
..5.........7.1.5..19...26...2..9...1...4.9.......38.6.8..6.5....75...1....1....9
.........652.8.1...3.419...........6..1...2...457..3.1.....8....2........13..675.
..79.31.......6...5..72...9.......32.....75..4......1..465.....8..1....59.3....6.
..89.....365..8..1....1....8..741.6.....5.1.7.3........4.....9.9......23..2.....5
.........342.15..98.9.43..6...........84.........87134.........59.7......1....27.
........35..83.1.28...7....4.2.96.....542.....96...3....4...8...2...1........5.6.
.....7......3.9126.....24...5.........6.1...5.37...9.4.....5.7..9..4..18..2...3..
.....3......2..6....6.7..85.......3......5.192..18.4.....5.....49.....5..27.14..8
4.6...........4....51.39...19...7..4.....27....3.45962.......2..4.......9..8..5..
..5....7...6..5...2...78.95........2..23.1....87.2...9.9...6..7..3....1.......8.3
........267.98.........157......8.....43.......62...39.........9...641..3..1.742.
....2.6....1.........65..9..9.7..13....594....8..3154.......48..45......2.6......
43............9..35.9...86.....2.3.....8.3...6...1...98..5.6.....1.4..9..7..31...
.1.2....4..6..1.3.7...4..8.........327.5..89.3.1......5.....7.2.6..1........3...8
.1..9...28........5...3...6..3.4.7....4.7.......5.2..8....27.6...81.9..3.......19
..6....394............3.45..8...9..6..12.3..4749..12...2.9.......8..5......1.....
..8...2.4.2.....7...6..7.98..2.......8.96.....15..34...............8.5363.9....8.
.........6...5..4....84.29...8.....219.........5..89.1....36.....72..1...1....825
...........8..479.9...76.1......1.4.5.9.4....4..5.7...........2.3....86.6...29..1
...6.........19.....9.83.1...8..6.7...6...4....32.78..........62......894...9..52
....3........9..85.1........4.1..7.2..1.2.8.63..6.4....29...1......7......34..27.
...2...8.684.......5....97...1.7.5...6...2......9....41........2.574..13...8....5
.2....5.......912...68.......7....4.....87....1.5.6.8..32...756....324..1........
3..98..2.4.6.....3.....4..........1......297..3259........651...6......4..5.7..3.
..6..........43...5....8127.5..1...38......7..7.3.5..9..........21..9.8.4..2..6..
.4..71........6...9..2..8....86.3.....4.......72.9...42.53..6.7........2....5.43.
9....645..5.......3..8....6..9.....8.......7.5.4.7..61..2.9........4....7.32.1..9
.....4.3.2..5.7..69.6....58.....84..5.1.........36...5....4.2....87......27...3..
51..3.6..3.......1.6.4...7....21.....3......8..29...5.....4....4.5..2...82....94.
....5.....9....8....5.43..9....2.....89...6.3..46...5......1.....15.24....68...71
2.31..........2..9....85.4.65.3........2..9....97....6.........7.6..4.18318......
..........59..241..42..63.9........58..431....3..6..7..........4....9.8....71...3
....1.3..87.9.........2.7.8...8.4.6.5.6..2..4....6.2.34.2.............85......9.7
..3......2.......6..6.7.5.......9...16....7..9.7.8.6.3..2.....9.8...3...394..6..5
.3..7......7.....256.9..1.7.9..8............8.....5..1.4....5..3.1.9....9...2473.
...769...........9.7...4.........538...345...1......7.8.1..6..2..943..8..43......
.........9.4..1...78..94.........1.2.93...6...2.....84.46..9.38...31....2.8......
......6....3...1...1953...46.19..2...2......9..4..7.1.....738.2.4.....5.........3
.46..3.8.23.....16...1.....4783..5......8.2.......7......7..93...9.42....8.......
............2..4.54.7.9.6.1....4..3..3....1...413..96...3.....8...48.......5.67..
4...9.........7..923.8......1.....8385..6.2.....5...4...........759...2..2.473...
2..5...678.....5.9..3..........2.......78.....2..9.6.1.3.4.....7.1.....3.6..3.7.8
8....3..7.......295.1.2...4.........7.3.....1.1..3.2...857.....1.....648...6..5..
.....7...1.....48....84.............81..3...93...96..5....8..5..2.4...3.6.352...1
.7....3......53......8...6.3..1.....8.6.47.....2.9...7..35....4....84.2.25....1..
..81.9..2....4.9......62...7.2......3.5....78..1.......3........6.8.4..98...2..67
..3......12...8.....594.2....9.81....7.....28.......5...1.....575.1..4.9.3....6..
....64.929....1..47..2......8..4.......5.....527....41..1...73...9.........937...
..........369.....9..5.87.3...26......3..74..8......9..62.4...8.8..7.2..4.......1
39.....5.6..8....34...9..7.....7.1...2....63..8....79..3...........1682...6..7...
..5..9.1..97.2.....1...6..45...........74...6.3...8.7...2.........8.32...6.4...31
........2.........84...15.61....5....3.7..2.4..4.....3..78.3...9.1..4.2.3..6...9.
........3..465..9.8...92.7...6..1.4.........72....89.......4.5..7.2.6..8.....5..6
....9....7.92......5.3...7.5...4..6...35...2...1.7.3...9....53........8.48....7.9
....4.....6...894...9..1......2......2..8..73..85....16...2...953......6....752..
.8...9.5.2..8.3...1......7......41....13674.24.6..............13..2..9...97......
..65.4.1.8....37.......2..8.85....64......2..7.34........2.........7..8316......2
..6....5.1.....692..32..........1...3.........613...84.....68....4875........43.9
..2.....1.....5.6....726.....19.4...3.......52.....43...6..9..2...6..7.89.7....1.
9.5......2.1.....3.7..5.....89....1.1...6.4.....3.56.......1......598...7.62...9.
9.........16.2.5..37...16.4...2.3....8..7....6........4......1....91..8..6.8..3.5
....6......54.1....7.28.....9....7....2..38.....5...63.1...64..9.......8..8.1.2.7
.4..12.5....3....6..8..7..9......1.3317......4....9.8..7..........8......9.62.8.5
..5....8.......931.9..4......7.........5.4..895.....2..4..25....2...61...3.8.9..4
...........89.13...21.67..............7.1..242..3....9.1...9....5....2.77..6.8..3
.......1...6..39.4.4....72.....3.5..85....6..3...1............272.6...9..8..471..
........3.7...2...13...9..6.......7.61.32...5.93..4..8.6..5.........85.9...47....
..7.2....9.465.......4.3...3......917..9.6.3.........5..5...8...2..8...7..8..1.5.
.8.7.6...467..9..........4...4.97...7.1....84.9.....2......2....29.7.......35...6
.....2....2..8..4......1.5......6.1.7.3.4..6.1...7.9.38..7....94.......65...9.4..
.9..85.3...5.3.......7...9.5.1.9..6.......8....32.8....1..6...96..4.....7..8....1
..3...1......9..5...65...4.....6...7.48.5...6.1248....8............4....12.6.3..4
...6..5.17.3..5......8.9..6....2....5.2......97.3.6.......5.7..1......4...8.7..63
..........65.138..21....54.....86....57.....46.......3........9....3.7..9..87.3.2
......5.9.56.9..7..7.6...3.........27.94....33...2...88..........3..8...4..359...
........6....7.1..6.7...594.....9.2..8.7...69.4..5......5..83.71.........6.4.5...
..3..9.172......54....3........4...88.....1...1.9..765...7.........5..3.15...39..
.1...3.7...8....243...975....5..12....493.6......2....2.........8.6......7..52...
8.....1..5..67.3...67.....93..7......91..62.......4.......1...8...2....7..8.4.92.
51..3.4..9.7............89...4........6293.......74.182.....1......5...4.35..8...
..1.9........53...35.67.2.....4.5.....59....79...6...2.....23.1..9.4.....7.3.....
..72.3.9.2.....7.....1.....4.5............369...78..41..23....556...9.3.....6....
....7..2......8.31..........91.8......6......5..93.78..1.....9...7..681..257....4
..4..59.2.......8....3......38.9...45..1....7..7..4......6.1.....5..7..37..48...6
.....9......2..7..875...........4..17......24.84.5...3....1.....1.....3.569.3.1.8
4.....8..9.7.........7.8.1.7.......1......9.5.1.56..2.....3.2...6...9.7.3..2...59
.......5...2148.....6..9.42.....6....5....6.7...98..1.........4.93......6...91.85
.9.......6...2....2.8.....6.4..57.9.....384..3...425.......3..2.14...9.8.......7.
..4..1...6.....95.....9.421..............58...49.....7..89......6.4..1.9.3.2.6..8
...1....35....9.....9...4...2..9..34.5......1..3..17..3.7.4..5..9..8......65...8.
6...1...........47.5..6..3.9..7.....735....6.....2..5.397.8...5.....94......52...
.....9.5........7..7.2.1..4........8.8..7....2...1...58.9.3......7.86.41..4....96
.........1....5...46.9..8.7.......46.8..32..5.45..93.1....8.....37..6......2..7..
....7.........1..8....2697..74.......36..5.4...8.1.3..........756....4....39.2.5.
.4......55.......9.....6.....54...8.6.7..3....2.8.1.9..5.3..8.13...4..6.....25...
..51..........92...3..6.....81...52.........667..3..4.9.4.716...176...........3..
.5....2...6.4.5.....2769.1...3.......8......3475...1..8.......7.2.8..4.....6.1.3.
.32.6.9..4.1.....55....3.64......4...83..4.....9.1..7....7....225..9....9.......6
58....2..3...6.....46...9.....5....4...94..6.9..7....8.9.45..3..6..9..8.4...3....
.7........3.1.5......2.6.57..6..4.1.....5.8..4..72..3...........819.7...7..4..1.5
.9....6...1...8.35.48..5.....5..........32..4.82..49...............5..911.6.7..58
......9....6.4.....49...87....2...61...9.8.52.5..71....148.....9......2.5....6.4.
........4.......37..973...18.........2..16.....6.4.523.....1....64..8...9.362..7.
.......3.9..81.5.45..3.7.81...........2..3..5..158.4.7.9...........5...62.36.....
..17..856.6....9....35.8....7.....6..1983......69...4....6..7.......4.25.2.......
.8.....7..1.93....42...........6.5.4....1.....364..7185.....36....1..8...42....9.
.....17.......3..28...45.9...1....6...73....5.4..5...796........8...7..6.142....3
8.4..9.....5..1...3...4...5....182......5..17...6.2..9.962....1....8.6..15.......
..5....2.6.9.2..8.2.....1......38..........4.18...237.7...4..69.927..........34..
.....854...76....8..3..2....62..98........47..7.......94..5.2....8..765......1.8.
..4...53..61.........8....7.8...637......8..64.....91..75.1.....43....2....6.5..3
..7..2........39..36.7....2...8..4...9.3...5.4.....18984...5....1....693.2.......
...3..5.67.6...8......4...1..5..2.6.2....4.5....9.13...7..6......82...4..29..3...
.6.....9.9..8.13..4.37...6.........819...24....6..5.7.......5...1.6....3..215....
..6...2..8.73....4.5..4...3.....8.4......1.62.8...35.9..5..6....4.7.......35....8
..........6.3.5...3...279..........2.742...8......976...........897..65..27..64.1
..5......46..21......6..2....1.6.....9.3.5.4........5......2.37..3...42884..9...5
..8......46....9.....981..6...2...67..384...99..6.3....19.5..............3...25.4
.418......6....2..2.89.......2..6.3..5.......6.....9.27...4.61..9..2.3..8...37...
.....4..6...5..91..2136...4.48..2...............9.65..91.4..83..3......54.7......
..........1..7.9..9.5.8......6.9...2.52...8....3.521...3...1..6.....54935.8......
..7..4.5.9....7.6884.9.5..1........9.1.........21.3..7.38....7.....6....49....8..
..8.1..3.....78..2.5......6.2..817.3..1....6.64....2...3...5...8...3......2....91
.9...3.....5.....41.26.......81......3...81......697.5...73..4..1.....79.6..4...1
.4..82.3..5....1......37.6.8.2....1.5..316........8.....1.5....26.....433.4......
...........59.8...1..2.7..6...........3...492..973.8.5.....3...45......3.9.14.6.7
....19.2....5......942....69...4.8.7.2............63........6....7.942..5..683..9
.724..1....8..23........4....7..6......8.1..2..1..964.2...7.....9......1....53.69
2.....3..4...3....6..527.1..8..796..1.6..........5..2........8......87.1.2.7.1.5.
.934.6.....27.....1............9.2.7...3.2..47...1..63....5....61....9.....1.874.
....4.9.......3..55..98..7..........97...843.....3.7.66.3..2.4....4.....1.5...2.7
.....3.....5.67...1...54..6.........84....72..29.4..8......1..36.....9.893..2.1..
7..........4.2.5..92..4.3...49..........5..8..5.28.6.1.....2.......18.7...3...865
.5......8..9.....2....1.....769...2.8...35.46.3...6.......7.8.5.4.8..96...3.5....
.......189.5..7..31...6.97...8...5.....4.....4.76...8...1....9....35164....2.....
......94186..9.37.........8.9...8...5...4....4..735....4....7....2..3.84...1....2
......1.4.....3.....195..62...6...7.9.5...21..72...8...8946..5...7.89............
...........461...7.2.8..61..79..........239..4...86..........7.8..1...6...6.348.9
..............795495.6....7....4....1.5....3.2...3.419..7...8...6...41..51..9....
781....69.......322...6.8.......87.5..2.79.1....4...........9.7..46.3.....8..4...
.5...6...........5..8...9...1.......5.6.2...7.741.836.....63.8..372..5....2..9...
.43........8...7....6...241.9.....248.....5..6.5.82.9.....7........6.9..4.19...6.
...2.3.4..5.6...7...89...35...............569..61....7.....6....93...8...8.73..52
.6...8....3....9....91.67....8.....94....98...9..7...2.167.3....8..1.......48..2.
.........72..94..8..5....17....61.7.......1699...8......8..5..41..7....55...4.6..
.........3.51.9.4.1..2..........1.2..3..7....5..6.3..7..9...3.......25144..7.5..2
9...3..5.2..94.1....1..53.838.....2..94.7...........4..4.359..7...7.....1........
....8...1..93....6.....4..8.91........7.....2...576...9..6...45.4...7.8..83..26..
.........23..5..9....9.86.3.48.6........3.15......49...21.........19.7...85..6.1.
...4..3.59.......1.8...3..7..7.........3.8......72..83.7...2..8..9..57..12.97....
.4..5...........84.369...7.1...7.......5.......98.62..4......3......2.16.1.687..5
9......2.........3....34.153.26......6.4.......9.82.....82....6.7..9...113.86....
......6.4.62..38....1.2..5..1..8.......4...9..9....1.62..3.1....5....46...9..2.7.
...4....8....163..24..5...6....9......15......69....81....2....3.....165..6.8..43
...........5.384..71.2.......9...8.....183..64.3..2..7.3...5.2.2..34...8.....1...
.6..5.....98.23.171.....2........859.....57..6.2....4......13..5397........8.....
...........1.26..7..4.596...7..12......87..9...2..5.7.2..........7..1..66....45.3
....9.....981...745.1.2.6....7....9....43..5....51...7.....2...9......8.8.5....21
.....8...6.57........96..52..1.....956......83.4.7.....5..1..2......3.96..8..6..5
.2.....3...4736.9....92.8.......9..5.72......31..4...74.3.9..7.5...........48....
.72..3..9..1......4.....7.......8...628...1....5...26.....2..1.2..94.8....48.7.9.
.3621.4.7..8.....11......6.....42...........5.257...13..4.........129....9..3...8
57....64....2.7.....8.....5...8.....4.5..9.8.......9.1.....4..2..739...6...7285..
..4.1.8.........47.3.58..1..1..3...8...9...63......95..8......92.5.68..4.....5...
............1.3..895..62..3..4.5.8...9.8.1....2....4.9..2..8.3..3...4.....5...2.7
....5.......4.869.1.4.2..7......3..1..8....6.241.....7....7...9...2.....67..942..
..5......63712.....41....73...9.........4.3.28......1.5..2....1.2...1435.......8.
3..6......4.8.........425....4....38....1....59...8.7..7.......9.5..3.8.86.7...54
..5..2.3....1...7..26...9.......7.9.9.8...14545..........6.8..7.4.2.....8....53..
..6...1..4....5...1..6.9..........9.6.89..5...7...4.2...5...6.721...7..8..95....1
.2.......9.1....4.3...8.9.5.1...3..9...87......4.2..8..72.4.......39.12.5.....4..
.....3.......2..4...5861..2..7....8.543..8...8..9..435......9..........1..63.5..4
.6....8.51..6.4.9.9.7..5.2.5...7.........92....8........1.8...6.5....982...7...4.
.5.....6...1..3...698..1....745...9......451.....92..3...139.4....4....8....6....
..9..427.4.......6...2.......7....6..1.8...3...2.4.1...5..1.8....8569....4...8..9
.48.....5.1...5.9.9.2...16......2..9...4..32......94.6....7......4.......61.5.8.7
.9.....4......6.9....37.2.1.......1.43......7.15.8...4.6.5.8......62.4....89..1..
.41..8.....59...6....614....1........27.49........7.13.7......29.......6...2.1.94
..31....8....3..16..2498..37......4...827....9..........93....2..6..1.8.31.......
.......6.9.57..1.47.....925.....2..7...5.8.......6.29.2...14.5....6.....1...3.6..
4............4.8.1..8.5673......4..7..46..1.....9.2.....3.......19.28..5......283
........3....74...2..3..47....81.9..4.2.......9...6.2...86.......694.3.5.1.....67
...........9.7.46.4.3..97.5.8.94....52.7.8....4...2..7...........5...342....6..9.
.6...5.1..8.73.9..3.7........9..3..8...........3.817...9..........62....7..3142.6
.....7.....326....4....5.3...4..27..2.......6.7.....13.2..8..9.1..9.......65.138.
.......5..6..4.....836..............15..7.96.9.....435...8.5..451.7...8...4.6...3
.........315..8....24..196...7.....9.6..85..4.8....3.2....7.......21......69.3.2.
....4..2.6.....4.7.4..36.5128.........1.6.....73....82.....9.3..1..7..6...91.....
.8.4....69....1.5....6...2...4.7.....9.5..2....31.2..7.......98....174.5.3....1..
8.3.54..91..8...42...........87...2..7.4......3....5..9....7.86...3.1..4....49...
...1.....93.....8.4..8.5..1..4...9..7.....2.6.2..9........1.6..1.3....24.95..4..7
........4...5.73.8.5....26.176......2........5..4..716..4.5........6...9..139.5..
....1..7.61...75..9...3.4.6........41..9......937......6....3.5.....4...3.8.75.9.
..85.........7.5.8..2..6....6..17...1.9.4...6..7..5..3......842......1.94.6....7.
........8.76..8....9.....6...4..2..6..1....74.8...72..1.2..3...9...4..21..8..6.3.
9..6...52..1......8.6.52..47.2...........3......9.7.4...9...41....48....2...95..8
.8..2...7....18...6...4.5......8....5.6.....3..34....2..48..2.99...5..6....1..7.5
4....2..596.8........7.........4.3.1.45..32.......9.8.6.1....3..8....1.959...7...
.......8...7.1...3...7..62..82...3..7.3.8...9...4.7......6...1.96.........812.79.
.....69...1.8....3...2...6..2...139.4..3.9....6.4.7.........5...56....3.9387.....
.1.7...5463...5.28......36..4.........19....5.78........7.6........52.4...5.1..8.
.....4....5..1..76....7...43...6.8....97......8...9.23.35..........8..699.14...5.
......8.2......3..82.41.5..2.46.....16...3........4.5.............8.9.6.3.61..498
64..92.....9..4..7.2..8......16....5.5..7....4...2..9.76.....48....36.1..9.......
.....4.2.8....7.....4.3.1...7........8.7...9.43...52......9....34.81.....6.4.3.81
.....4...7..9..5.11.5.7.2.8..1....374.7.......58...6.93..5..........1.72.....2...
..54.........7..8...1..86.9...1...2...3....6...89...1.37...4..58...39.....47....8
9..61.......8....45.2..........8.7...73..2..6......1.2..1.9..3.3..27.4.5.5...3...
...1.6.7......261.....9.....5..4..3.3..5..12...2..7..8.7.9...6.83....2......1.5..
.5..7.6.....6...913....157.9..7...6...2..3...8.6......79..8...2....2...7....5.1..
7...15..3.........2.....185.5..........6...7.127...45..4.3.6.9........6..3.7.8..4
.4.............3....8..45.9..49....2..1...84..3.4.6....6.....78....2865...2.65...
..7..2....3.61.....694....8....7.5..5.1....9...6.....3.2.1.....3.5.9....9..2.4.5.
......1....9..3.8..8.9..34......67.8..1.75.....832..9.......2.....2....1.4..3.9.7
.....5....4...68.3..218......15689..45...3.........1..1..8......39.......7.3..4.1
.........4.18....7...3..541.......2..3.785...1....3.....4.......13.57..69.7.4..1.
...5......4..9.562..1.7..3.....4....1.........5.1.23.47........689..7.21....2...9
..2....8...4.1.96.....2.5.4....5..7.8....7....4..832.1.1......8.7.....16.....93..
.13...86.8....3...9.....13...4..86.2....4.......1.64.....6..3.7....97.....9..2.1.
..5..3...9...2.6.116..................159..7.64..32..........2..5.6..7..37..594..
.......7..36...8.9...9..5.6...4..6...48...7...2..7..1...354.9....4.13........74..
1.7...8.9....7...3...4....1.9...52.46..79........42....7...1....1.95...6.5....3..
.95...2..6.......9..49...6............217.9..1..86..4...1..2...3.....5...29.376..
......1.5.4..9...2..9327.....1..3...9...4..7..5.....2....8...1.8..9....3.9.67...8
......8...149.6.....9.3..1......2...3.........9..1.7.5....5...3.2..98..6.56..1.48
.....4....75.6..2.3..9..4....6......28..357...5......6..2........75.8..983.....54
.........6..8.9..51.9.264............63....54.4...598.............3...129.8.1.5.6
..6853..........3...8...1...314....229...........9.....4..1....1.3.2..98.6...837.
.9............87..148.............4..352.9...824....6....7....9...8....737.69.2.4
5........74.8..6......6.24......3...3.94....1...1...97...3...54..1..8..6.8.....32
..........8456........92..7.....3...1.24...8......85919.7..5...4..2...7...1.3.4..
.............1429.9732.......6.8..........5..79..26..16.........21.....753986....
.......7......982..3.17..........5..38...7...96..51..8......6....98.....873.6.9.1
3...9..56.4....23.5.8.....9.....8..2............37.6...1..4.7....4.67.....69..31.
..........3.8...16.7..214.8...........67....33.9.5.82......3..22....8...6....71.4
4326....1.............5..3.......8698.....4...6...5.1...4..2..3.....39...76..418.
....1....8..4......7...351.......9..6.71..43....7...85.6.235.7........5.93....6..
...32.5...9..5..21.....8....86..4........614.1...9..62.......9.5...6...8..1.4...6
.59.3.1........8.....8...32.2.......9.....58.36...7..4.9.78...5....5..1...2..37..
.9.......78.3.2.....2..64......9....8....47.9..123..........9..6..7..2.4.345....1
........9.24.59..375.....6...........7..3.89.....657428....2........6.1..43..8...
.....3.4.7.8.....9.34.1.5...59...2.8.....1...3.76......9...........3.85.86.....37
.....7..2..6.........168.57......3..6..78.....19..6.74.4...2..1.6..4.2....8....9.
...6..79...2...3........6.88.6..9.4..57...18......4...9....6..3.4..1....2.1.43...
..7.............3642......8..4..3..27....14.9..29..87.......9..29.87......125....
.5..1......8...3.4....5.8...9.........7..9..3..17..9..9....2..1...5.426.6...974..
3...1.....75.....4..8.6.1.52....9....91...2.3..62...1..4........5...86..6...5..7.
.27....8...6....5...89.2..45..6......9...381....58.4...6..........4.9.3..3.2..7..
......4..1....7.92.87.6..5..............56..4.5..42.38.....4..1.49........15..9.7
.9..7....7...2..8....8.1...6....5.4.........3.3...4.16.8..59....14..8..9.6.1...7.
48..2.9....2.9..45...5..1...1...34...938..6.....6...7..5..6.2.........81..9......
.2.......7..5.2.....8.7.4.59.2.1...8.3..6..79.4....3.....1......1...6..2....987..
.....45.3..23...7..3.15.....1.7....6......9......628..9.52......6..4.71.3..5.....
.6......4..14.368.....9......26....3.....781.34.9...7...37.......7....4..54.....1
........8..3..1.5..78..93....6......5....3..7...2.86412.7.15....1....7.....9....6
...........2..4.5..9.17.4.8.......7...1...9259.5..1....3..2..........7.41.468...9
.9......8...8.5.....7.9..3..3..2.......4......2..36.1..14..93..3...1.9....538...4
....8....14........67.9..1......4.85....321...7....6329..32...8.5..6...........23
....5...4.....9.......8.917..5...7.....872....214....8.....8..5..3..127.4..59....
.1.4....3..32..95....8.5......1...78......4.5..7...39.3.9..4.....6..3.8.25.......
.47.....8...2.159.1................6..4..67..8...7...52..9..1....17.8.6.....13.7.
.59..2..6.7....5.9.1..........16....1.....3.79...37..4..7.......23..6.985.....4..
.....56.2...4.7.8...4.......49..8....3.1..4....6..2....5.2....79..7..3.6...5.1.9.
....8..45.5....8...6.49..7.4.......75..73.9....39.......1....8.7..1..2.3..8.2....
...53......5...6.....19.5.3.....4.........1641..37.8....8....4..1......8..47..921
.3126...44...19........4..6.......5..6...8.2.....563...1.9......28.....1..3...29.
8..............35.2.3.7....4...9...31.76.5.8..3..2..76.......64.5.8.......43.9...
..5..94....18.6.7......35.......1..4...4..698.86.3....8......6..5......2.37.....5
5......6.4.85.7....26........3.5...86.....52.1.....9.72...4...67....9.....573....
.5....9..6...91.....175.....2..4.3...1.....9.3.6.....4.3..682........4..1653.....
6.7...1..4..9..6.3.9..........5...2..3.....4..493.....1..4.5..93....2.6.....1..38
.13....4.6..3.......5...8.1..96.5....8.23..76.3...8..5...8.6....5....4......2...3
..2..8...4..7.61......2.9.8...........386........54.837.......91...9.46.2....3.5.
..........7.2.56.8..89...72.2.....6...9..6285..7..........42.....53....7.4...75..
.4.......3......675..9....1..679..3.1.23.........2.9.5.15....832..4.....4...3....
28....1..3..162......4......5...7...........3......98.6...78.317.3.....482.6.3...
2..4.56.1.....2.....3.7.5.8..72.9.1.85....9...9......4.2.1.............31..8....6
14...7.........2..7......9....3......9.4....2.3.95..1.....613...53.....1..2.3.974
..8..9..32..1....6.7..8.2...46..........32...3....6.4..32..75.........615.1....2.
...8........62...44.9..3.1........7..4.13.....61...9......6...8.95....473.8....59
.4.......3..2.5.....93.4..2.26....7....58....53..........1.876....73.9.8..5.6....
....6..1...2...45...3.....9.9.1.....2..8.6.....12.5.9.3.....6..62..7...44.....17.
..3....9..9.3.5.1....9....2..2..8..61.46..5.........84....9..7.61.....5..2.....61
..3..5.49..9....3165........1.9...7...6.4......7.86.53....6..9...........9..3.1.8
...4...7....5...2..9...8.....93.2.1.72..54..6..4....9....2...3..36.8...1......7.9
.418.5..9..9.7..58.3............26..3...6..25...5...97.....69.2.1..4......7......
....5.3...18...4.....1.6852.....5...8...7..1.7.6..3..9..2..8......94........2.5.8
............1876.....92.57....6.......2..9..5.9....8632.............4.9..6..93781
....1..2...9....67.54.32...4........3.25.178....78..3....2.........58...5.8.....6
...........5.63..9..84...........6....2..1..75..6..483.9..3.......7...9.63..59.24
...6......75.4..3.8....9.4..3...2.58..2....91..9................231.6.8...83.74..
9....361...........36..5...8.3.5.1...6...4.7.4...2........7........129.5.41...86.
..9......3.1...8..587.....2...1..4...4.7.36......52..77...1..6..5...........3.251
.....5....9..4.218..4.2..9.........79...61..4..6......2...8.3...7.6..8.91..59....
.....29....4....51.....1..2.739.4...8...7......1..38.7.5.....9.42..3......6.58...
4..9.3..73..7.8.91........6.8..24......6.....64...5..3.5..8..1.1.7.............45
..2..9.....65...1..3.216..9.8........239.86..4.1..........4..7.3..........5..32.8
........5....793.64.....9.7.........21.6.8...85.4..1.2..........9..37...7..51.8.4
.9......8..34..52..81.5.....1...5....2.9...47....7...2....6.7.5...58.3..7....9...
.....4....79....6..2..6.415..5.2....7.6.53..9..2.7...1.67.8...2......85..........
.63....5....8....1.5...6..9..6.9.1.7..91..4......72....75.....4...24...5......96.
.............98.2.....51.3......4..9.5.9.....2.87....5..14..3...64.7..52..5...8.4
9.632..1......625...5.7.....3......7..9.5.1....7863...5.3....6.....1.......5.7...
.........4.......3.51..462...........4.5...16.23716.94..........6..23..1..5..98..
3.....4...1.8.9...78...........74.......3..16.23.9.7....73....8........1.58.2..64
.....5..2.3.7....45..962.81......8.5.93.8......1....3........43......1.....3549..
.8...3.4..35.94...9..6.8..51.....2...2..8..54.7...6...................3.3.25..9.8
....1.3.......6.74.53....8.56.......7.4...138.1.......6...7..5..4..6..2..2..45...
...6.97....9.72.5....8...9.6..78.4.........7.1...23....2..........5...613.6..75..
.5...7.1....2.9....148...7...3.......2.5....8.4.378...5......9.....82..71..4....6
.............37.95...69.2.7.........2...59.7.3..26.54.....42.....8....3...9.7.42.
..9...........5628.....15..82..4.........3.......1.456.5.12..6...7..4..2.8..7.9..
..3.2.1...6......2.2.61........31.4.........6.5.....3...89.....6.52....137...865.
.7.9..5........2.8...768..3.........5...9.12..21.8....3.........5..29...4..815.9.
51.....433...5...........8.7...........4...292.318..65.........49.2..3...71.9...6
..........8..3..9..7....8534.......6.5.1..4.....74..3.1..48...95.9..3..1...6.1...
.........4..67...5..2..3.......1..2...6..8..97..3..1...1...9..8247.....3.387...4.
8.1.....2......5...2...147..6.57.1..21.9.3...........53...9...8...2..36...2.4....
...7.....7.52...9..12..4......3...87...5..1...2.14...5.4..6.3.91....5...9.......1
.56.....4.4...1.6....8.....7...9..58.....8..3....5.2.9.........569....27.874....5
....7..3.8....5.7....83.92.7.....4..4..6......2...97..13..6.....4....5...87..32..
42.....161....3.....84....7..........9.51.....6....1....5.6.8.9......67.71...45.3
18.....4..3.4.6.....2.7........5.....73...2.5.283....6......4.......9.5....2.4973
......4...53.........7.1.8.....72.6....36...5.2....934.....4..758.2....19.2..7...
.7.......6..5.2......874.1..5.1.......72.3.5...9....24.2..6..7.3...1...8.1.....3.
54.9.86...7...........6.4...61....58........24.8.23.......8......56.2...8..1.5.6.
9.1..5.3....4.6.81.6......943....8....2.14......2......15...74...38...........39.
...........9...3.7.4813.6...8....4.6.24.7....1.7..3.8..1...8...........5.364.9...
.4...8...2.5....7..8..2......93....7..36...51..1.4.6.3...9...........92...273...6
........87.6..2.....3...1429...8..64....26.9.4..59....6....7.5..5....82......4...
.......58...7.....8...923............3.26...7.1.8392....9.7...5..1.53.2...4...9..
.............7...4...946578......4.6..75.....6841.......2.5.6....9..8..1.76....4.
.7....54.14...........15..8..4..7..3.....4.15..26.1.......9.3....7....2.6.957....
.4......88.6..5...7.......5...1..5..9.....61.46...72.35..98....2....6.....4....91
6.......797.25..1..48.9...2...76....21........8..45.......79...42....3.....5...8.
.2...8..4.6...9.2...1.73....92.1.8..7..8......8..6..1.8....52........4...34..1...
...71..8..5.....3.79...8.1.....5....36...78..4...2..5.........51..54...3..41.2...
....1...4....243687.......1...5.......3..897.....73.85.96..........9..1623.......
.56.....198.......3....7.6..........46..23.......9.35..9.8......153.2.7..3.74....
1........4...73..1......456....9.......4876...4...2..53.....5...61..9.4..9.5...8.
........1286..4...3...9.52.......8...483....79...8.26..6.1...7.......4.5..94.....
..........21.79..4.....3821.........6..45...3.3...85..........6...1..43..46..2.79
.....6.8.95....6...2.75.4......8........2.356.9.3.5...1....4....8..3.....326....8
...............85..735..........2.6...2.7..91..89.45.7........4.67.5.2..2...96.7.
..9........2.5693...3..95.6........4...8..67.3.....85..6.1.....4...2...8.8.7.3...
.98....7.......1...546....9..9847....6........4...6.13........5...5..7.2.8..7.34.
.....9..53.4.........1..93.26...............91.8..674.5....83....7.1..92....4.56.
.....3......7...4.7...1..3.....8179.9..42.1....7..6.....3...21...8...4..51...8..9
....4..8...62.....54......2.....8.6..15.6...4..2.7..5...4..7..3.2......1.3.15...7
..2.3.....1.......6.8.179.2.7.........67.42...23....4.......7..9.7....64...9.81..
...........78..356.8.6.3.29..........5...2......3..587..9....6...1...7.3.6..54..2
.......38..4.......6234.....9......6..7..5.4.2.3..6..5..68.47...85..32......7....
.6...3......51....4...8...3.3....95...8.6...7...75...1..1...3...5.8...1...2...574
....5......5..4.2..7.....31.1..........4.92.....23.6.4.........13..45.89.49..1..5
8.........47.....99.......1.....18...5..947.....6.731...41.6......7..4.3..5..3..6
...........35....8128..93...........6.1...9...94..5683........9..7.982..4..36....
.........9...12.8..6...8..4.........1....9.766..5..3.8....4...757.2.....3.6.7..59
...1.........5.96....3..147..65....2519..........7..1..3..26...9..814.5..8.......
......8.6.7.............532..9..8.....59..3...3..4..9....8.6.25.2.193.8.6..5.....
.....2....3..1.2.48.46.5.9...6........71..5.8...3.49....1..........5.....5..4.871
.1........3.....7.....9.2.6....2...7.67.1..42...6.59...8.....6.1.48.....6..2.3..4
.......8..7.....6..4..63.579......4.......1....158....4..37...515...6....9.8.16..
......9...1...35.2..9.2..17.61.........35..4...76....56..7.5.......3812......9...
8......3...7..2.5...5.4.28...2......96...1...4...7...3..65.......4.9......96.3.25
.87.2..16.5....7......9.....65.........6..9.4.9...2.83.......47..3..8..15...1..3.
..1.........3..19...529..64.....4......53.48.7.......9.3.4....6..8..6..5..7.1...8
5.3.8..9.8..74...6...32...198.1......7.45..28......3...47..........6....6..8.....
568.......7.8...9..2..7.1...........6...1.8.248.3.2.....7..4..3......7.93.19.....
.1......4.......6.3.5.1..7..8.9....3....85..69..1....5.56....2.4....1.....3..748.
4....1..9.8...2..7..78..............39...74.1..81...32.5...8.....6........2794.1.
.....8.9...41..3..5.2.6................381.5......5.787........68.9.74..9.5.16...
..7......3...1.4...865...23.....3..8.7..8..4......1.76....95.....1..6.5.....3.76.
.4..1..68......594.8..59.....7..3.8.3.4..6......1......5.8..7.3.........8...32..9
.....34...7..9....5..12..78........6.59....1....3.295..6........412...6...39.5...
....9...81......7.....672....67....14..3...2.27...6.....5..21.3.4...8....6..3...5
.8.........73..8141.3..6.2.........8.3.....51..4...2.3.9.73............27..8.16..
...6......1....8.76.8.1.......7..62.....5.4......349781...9...2..53.......75...3.
.23..4..............983..4....7...815...8.4...8...6......2...1.15......9.923..5.8
.....2....1....7..627.4.........9.........8.17...18695...1....6..2....495.3.24...
.........7.4..5.6..862....3........7....3.9.6.6..1..3......1......84...9893..6.15
..........654.....7..5.6.1...9...1..54..7..9..87...5.3.......2.2...1.3..8.67..9..
.....9.........1..6.2.8.39.7...1.....46.7...11...56.3.......5..39.2..8...741.....
.7..6.2...4...5..3.5.18..4.....5.7.6..1.79..2.......1.3...1.8.78...3.........6...
...1......7...8.2.13...59...17.....4...7..6..362.....7.2..4.....9...18.....96...5
...........2..36.5.73.6.2...1..3..5....6.794....4..8..1....85...........8.4.92.7.
.8..57..........6..2.3..7.416..............8.7..9.461.69.5......3.....4...5.38..6
..............265.1..865.27.........9..658...86...3..9.....7....483....15....92..
.........4..5.1..998.7.6.1...........94..8.....3...185.....3......9..2..3.81549..
..8..93.1...8....7.9..15.......4...66.5....2.24..7..1......7......26...88.1...6..
6..1......137.2...2...4..8..76.3...5.....9...3...1...8..24.....9.1.7.3...4......9
9....8..4....1.26..36......5..94.6...7.2............52.98..1..6...8.471.....5....
.......1...8.....5......894.2..6....5..49...7....713...5...9...892..5...73..4..2.
........6.96..482..3...........86...172..9.....37........47....5...9...2.612..5.7
..36.....2.........9........5...3..99..4...5748..65.3...1....2.7..3....554...2..1
..9..7.6......98...2....4....3......96.1.4....8.2....5....4.9.2..19...462..3...7.
.........8.2.....3.153.9...3.........2..8.6.79765.....6.3...1.....8..2.4.4....5.6
.......6.....845....5...4..1...7.....27.....6.94.....254...9.1..79..52...3.4...7.
32..6..1....1.......1...8721.2..9..89...7....7.....3..........4..6..1....75..498.
.......2452....9....4...57..4.7...6..1..9..4......3..7...9.....36..2...8.8..1.7.5
..7......4.5.6.....1...9.357...........62..191.49..3.......74......1...2..8452...
8..5.....45...3..1....4......361..79.....25...8.7..61.61.4...9..3..2......9..6...
..7.......8.7...51...82...4.........73.5..6...124...891...35..8..89.......3.4.1..
............8.1...18.927.6........73263...1...5..9............28.7.5.63.34.7....9
2..9..1....6..45..7...52.46...6....383...1.65.......7...4.78...5.14......8.......
3.8.............921...673...4.9......9..31724..372..6.....1..486......3.........6
....5...7.49.3..8..5.4..2..8.........367....1..26...7..6...1.281..2...56........9
..12....8.8.51..4......3.5.........34.57....1..3...52.....7.....1...2.7.9.78..43.
.....8..64..9.2.....1.74.....2....3...4..7.25..7.5.4.9...1.....6....9.51.3...5..4
...3.....8...2.54.9517...8...2..6.5......2..91....7.2..1......6.3...8.....6...498
..7.2....3..514..7.5......2.........7...38.59695..1....21......4....5.8..7....4.3
.3............946...7135........1..6.8637..4......8.....5...7...29.1...5..45..39.
.......1....69..38......6.9.8..1.3....7..6.9...9..3864...3..........1.879...645..
..8.25.1..2......3.47..35...15..9...9..3.....38..1..4......4....5.79.8....26.....
.1.......9.....5.3.5.12.79.4....8.6...69..1.8.7.3...2....48...7..5.3.4.......5...
..2....1.4.8.1...6.7.....4....9..4.7746........9....8.5..3.2...8.4......6..4.957.
...4.81.2.8..9....45..32........7.....7..128..3...94..7.....6..59....87.......9.4
....2......2..5.93154.38....8.......4.9...6.2..5......5.....13..4...3.6.7....42.5
.............7.3.9.38..965..2.5...9..5...2..68..71..2..1..........1..73.7.465....
....3...8..16...5.6.89.51..1........32..7...6.7..68.........2.....4.69......1756.
.2..543...98.....7..4.9...66.9.2...8..38.....2..9.3..5....35......27.......4....2
............2.7..1.67..32.4........8..475..9..85.1.4....1..49..83...........8531.
......6..8..9.1..3..123..............39...5...57.19.46....62....2.5.836...8.....5
..1....25.........94.3..87...3.265...2...5..4....3..1.3.97..6..4...9........6..93
.......3..764......3..297.............196..4.8.3.17...5.7..1..3684.....5...8....2
...43.6...9.........7.1..93...3......5..219...216....58.....2.9..6....8...2.4..56
....39..2.17.8.......6.75....4......8......5...589.1....2....49.4..238..3.1..4...
.4......8.....6...2.784.6.37.81..26....7...3...9.3.....5..........3..1253...21...
..7..........8.56.5.8.67........3.8..7.92.....2.746..5..9....46.4...1.....26..1..
.6......8....4....83...79....2..1...9...3..7.6..5.2..1..6..3....8.2..1.3.5...94.6
.....5......72.1.3...8.1.....1..6...73..5.96.....1.52...8..2....5...4.3..7.58...4
.2.....1..3....7.21..9.7........42...4.3...5.38.7.9.6..6...1.2.8.......1..5..6..8
..4..1....2..76..4..7.9...2......2...1.36.........45.1.3.1.....1.29.3..7.....73.5
2.78..4..6.......7.4.....8..5...9.32......9...3.28......4..56.....4..57.3..6.1..9
5...4.......8..2....2..584...96..4......5.......12495...8.6....1..4.7.2..63..9...
........1..56..42....15..63.3.......4...72....968.......42....7..1.6...56794.....
..3..6..25...217..8.1.3..................592.6.5.8.34.....9......7..35...4.5.7..1
1.....98.6...8..1..25....6...64.2.....9...63...876..9.........3....541.....2.8..9
.........4.738........52.4.....745.....53.28..6..9..7...84..7.17.3.....6..6....9.
..1........397..85.9...8.23.....7...932....7...4.9.81...5.8....76....4.....4...6.
.78....9..1..7.5....59.31.....1.....29....3.1...4.2..97.9.....6....2..5..5...6..2
.........96...41.8543..............6.8...9.537.5.8.9....7..348..54..2.......48...
..9....4.2...3.17.8.......2........6..2.53..83.6.917.....14....6...853....1.....7
........1.2.16.3.7....386....9..3...1...492...627..4........1....48....5.7.....46
..3......9.....3..485..37..2....1....648.....3...27.8.....1..7....7.46..8....693.
25...1........8.6...3...4.1..48.6.9...9.4.8...1..29.4.9.53.7....6..5...7.........
.9.....8.3..5....128.4.....51..6......4.....99.23..7..1..87.2.....9.485......3...
..2.19.3.8......1...18....9.....1.76..4....81...67.2........5..9...2..484....89..
.584.3....4.....5......8........6..99..54.3..4.7.2.5...7.6....1.....2.4.5.1.8..9.
.....9.....7.86...6..3......4...7..8.......32..36.51...6.7...8.3.2...49..548....3
...........7.8...5......893.....1.5....3..9.64.6..5.87....7.....2...85..7.4.396.8
74...5...5.1.4.9.6.9.............1.....4.268...87...42..2.....3...62.7..98...3...
9....1.8..6..381...1.6......9...68.2..2.....3.3..7..6.75.........9.17.34....8....
..8....12....19..59..4..8.6.42.37....915....7..........8....7.....398.2.1.6......
....4...3...9...8...43...196....9..7..81.......37..15..4.......1.6..35..7.5...23.
..5.......34....1.816.35....7..8.......9.324.2......5........81.....1..33....6592
...........1..6..873......1....2...33..9.5.27.72.4.8...2........8.1..39..47.92...
........9...7.46..9.4..15.2..3...8..8.6....2....16.9......5.......8.9....3..76198
..1...2.73..7.541........3......7.........9.2.2.4.6381..9.......1...48.3...1.8.4.
26..1...8.1...3.2...4.2..5....9.4.7..3........98...2.1............4.6.17.4.1..3.5
..1.2...5945..1........9....74...2.1...5.....2...4..6..9....64...7.6.3...2.93..1.
.....9.........84.4.8..21.5..4.1..8..86...7.....6......3..76.1.76.53..9....82....
..............9.32.52.47..6...........9.2..6..6..78.25.....3....94.....8.2159..43
......2....3..514....9....6...2.1..4....93.2.5..4.8...654..2..9..9...37.3..8.....
.18.4....5.2..7..8......24.............1.938..36...5.....4.1....745.6.......9271.
..8.426......6.....4.8.75...6......1....5.27..7....8...876.9..5.932.....4.......9
61..........8.9.......5.......9..7....3....164..1...35.3..1...2.25..8..1.4.27.5.3
...6.....4...8...77......26..........7..46.3.8.1.7..54..8..51...5.....831....357.
.........3546.....69....5.4....4......6..17.3.4.85.1.9...........9.7...64.1.2.39.
.1...8..44.....8.6...3.4...1.67..3.93.2....5......2.......17...5.92.31.....4...6.
..1.....23....54...5.2...8....49..1....5....4.....17.8...8..265594..6.71.........
....82.6.827........1..4...3...9.71..1.5..63.9......8.2.3...45....2.3....8..7....
2.....6...57.....8.4....239...91.......5....6..3..7.1.47..68.9...9...8...6.1....7
..3.58...17.........2..7.9...9..........3594.3....91.2.2.....5.94.....638...16...
.284.1....4...698...5.89.....1..23...8....6......3..9.........1.....3.7..6.7.84.9
.3.8.7....68.1...951...28.........5.2......6..95..3.....1.79..2.....6..3.2...14..
.........1..4.8..7...67......9...7.3.5..9...8....43....96.31..4.45.8...9.7....38.
..........13..9.2.28..76..1...........7.9.53..6.783..2......1..........37516..8.9
....5.....5....746...6...85.2.1.6.5...74..1.8..8....2.9.......4.1.7..8..7..83....
...7.........6.5...873.1.4..93.1.7...6.....218..5..3.4.7.4..6.8.........9...5..7.
..59.1.8..7.6....46......3.24.....1..5...4....63.....2...8.7.43......9..3....98.6
.3...5...9.72.3..1...79..........5....3..61..6...518.72.536....3....8.....4....9.
.8.1...543...97.8..7.8....6.5.7.4.....3....4..2...........85.3....4.....61897....
.312....8..5..16..8....3.......3..91.....72847........1.....4....46..9.2..2....16
2..17......7.8...46..................46...397.3.4.7..1...3......617.8.29....2.1.6
..6.....227..39.6.9.5...3.7.6..........1.5.......92.513..9.8......4..8..1...27...
.134.25.....9..7.247.................61..8...8..2.5.16........15.68.4.2....65....
..7.......436.2..9....3.8.............5...69.216.4.35..........5..81.4.38.1...92.
2....8......5..3.9..6237......18.7.3.5..4....1.....4..6.7.1......13....6..5..6.8.
...29.7.........451....423.....1...65..97....8.143.....1....8...94...6.12......7.
..........9.174...4718....9............2.7....5..9.237..6..3.4...5.2....13.5..67.
..76..........7.2...138.5......3.....8...41.5..52..74....4.....6.48..35..1...3..9
........5.25..87....1....4......3....7.9.4..8.82..691..1.........7.6.8.363.7...9.
...2....4...37...26.24..93..8...4......6.5.....179...51....64.....9..3.6..8.....9
...1.35...1..45...7..2.9.....1.....2.2.....59..752.6....67......89...2....3.8..4.
....53..2.39.....78.1..79..1..7.826...85.1......62....4........9731............8.
..1..3......1..832.8........1...52...759.6.8..6...8...7..3.4..9.......58.5..9.3..
...6.....2..1...6...982......8...71...6...4825.......31..9.4..7.7..61...9.4.5....
.3.....8.....1.2.....5.69...9..4..653....5.19....63..29....21.7.7........61.....8
...1....5.9...7....21.59...1.......7..37..56.4...65.132...3..........4.....5812..
1.67...........97...423.6.8..3..97.........4.7...2.1.98.5......2413.7....3.......
..7.....9..95..8..2.....3....1..27.3...75...15.3..4.8.1..........5.7.1.....38..92
.9.2.........14...4.....862.........961.42.3..2.8...9.34......5....317.....48...9
..........72.1...658....9..1..79..6......6..84.....7..259.3......38..5...4.9...73
...6..17...3...........2.83.49..1...8..7..4......943....5...2..6...57.4..8.26.7..
..4..2...1...6875.7..9....1..7..3.8.....1.3.....6895.2...........1...6..5..7.12..
.........3.254.....5.3.1.7.........44.9..6..5.23.5479........5.7..81.....8..6...9
5..4...7.6...9.52...3.254.........67....148..8..6.......52.....3....7...79.35....
..........47.56...9.84...61....7..9.4.9...1.......9.8.........7...2846..3.269...5
............53..416..412..59.....16..4.6....2..52........1.32.......5.89.7..8...6
.9..6......4.....6..3...942...2......86...2....7.816947....8.....951.....5.....73
....7.36.3.1.......42.....8..3..64....48....2.....31....5.8...72..76.......3..856
...1.29..1.3.97.....9....7..34.6.8.......45..5...21.3....4.....95...........153.7
8......9..752.9.8..4.5..1....3.8.6.....3...7.28...5........4....1..27.3..6.9...2.
.....2..84.1..6..7..21.79.3..7.......65.4...9..4...56......1.....8.....691..8..7.
..6.29...4....6..2.9....6..2....51.4.......8.85..1.263....92.4.51..........4..8..
..........1.72....7...14826...........6...9...419.6.3..5...1....2..9768....58...9
..51...2623...9...............9..8..59..83.....65..1.7.6......1..4.....8853..16..
68.4........71...9.13......8.....3.....8.4.9.462..9......9...37.2...71.8.......26
...9....7.2...7.613..81...2....78..9..73...2.1...4...........5...5.....3.1..52.78
.......6....13.9.79..2...31..2........45.17.3.1...6..4.46....2.....1....2..6.5..8
..............2891.8..3.5.7..........47..1.85..6427..3..........3...5.7.719...2.4
.1..5....362.1...5.7.2.64.......5.7...5.9.6..9........7....1..8...3749..6.1......
.....1.86.763..5.2.....93....7....6.9.....8...54...2.7..8.359...3.9........4.7...
3.7..9........3.6...64....1..31...94.25.4.8.3.6.3....2........6...2..9..58.....4.
.21....5.......7.8...4...2....6...35.6........83.2.6...59..2.86.3...1.....69.42..
.5.........4.8.639..1..34.52........6..45.8..41.8....6.......94...2.7....8...9..2
.9.....3..2.49.8....6....4.5.8.....4........3...62.5.89....72....528..6.2..9....5
....52.8......76544...9...395..7.......9..7...4.3....5......53619.........6.2..1.
....573.67.5..38.....2..7..1...........8.9...9...2..5...41.......2..618.....326.7
2..........6...53..4.86.2.7.7..........6....35.2.7......41........296.4.62..8.7.1
.....3...3.67...845...9.2..............6.2.13..51...29..4.......52.....6.91.645..
.......1...59.2.4..9..68.7...48....38.....45...3.4..6..6......73..69......2..71..
........36...........9.38.......93.....245.865.1..6.927.........8..74..9.168...4.
.......3....1..6....1642...4..7......934.1.2.......1....7...28415....3..8.4.37...
...7...9......65.....913.6...6..5....3..79....7.84..2...2...1...6...42.94.51.....
.....6.49..3.7.......5..1...17...6..3.2.5.....54.....87......8..65.2.4.7...4..5.6
.7.4.82..........34.3....5...7.6..3.6.....5.1.59....7...4.81.........76.39..5...8
..2......93...2..6.5.869.2.......9.5....8..4....347.....475..3..13......6..1....4
...........26.89...643...52.......652.17.5.3..7..3.........7.......86.9.7...1..28
.....1...9.8.5.6..2...8..4...98..4...2.74.983...........1.7..9........6.56..1.2.7
2.48........7.5....13.....9..7.......26....3.3...26.4...9..845.87.....16....6.2..
4....1....5.....1.1..9.2..8.6..1....9......56.275....9..8...9..5..7...8...28.4.6.
.2............1.7.1....268.......43.37..6.........419...2.18....37.5.8....62.7.5.
..2.........7.5...45.......5.8....9..461.......32.9..6.....1.638.4.3...7..547.8..
3..7....9.52.......7.9.24.......6148....1.....2..8.76.......3..8..5.....5.3.24.8.
.4.876.2.....9.5..9...4........6.24......98.....4.1.5.81.......47.....122..3..6..
.5......6..674.31.2...8..4..1.3...24...8...7......41....26......6...9.815....8...
.2...4...4.31...9.9....2.....9........2571..91..8..5.6....8..65......3....62.38..
........4..8.3..19342.16.....9.....6.8...4...65...2.8.1......5...5.21..8....4.3..
.3.9.....25.7.8.3.6.7...........3.8........7..7.2853....1.....5..3..4..6..5.197..
.........2.3.41.8..6...84....2....7....3759.8......1.4........55.86.....3248....6
..1........5.17....2.8...5.8..7...2...7..3.9.....9.6.7.42..983.......2...182.5...
.......9.....42..19.1...3....8.1......4..8...13.2...8.8..4..6...235...1....3..958
...9.....7.12.3..8.....87....9.2..1..1....47.42..8...3......6...63..1...542.3....
.7......31......29..8.5.7......9.4.....51....9.78.6....6.283............41.6.538.
....3..6.........569....7...49..1.....7.8...1...4..5.2.651..9..7...9.2.6.8.7....4
..........5..83..9...72.16...2..9.7...43.7..1..1.64..8.........4.8.31....15.....7
.8.1...9.1.6..5....74.23.1.6..7.....4..5...78........5...9.8....4.........5.17.89
....1..28.....4...2.39.5.7......83.7..9.6....3.....98...4..9..6.92..7.1.....4.2..
........9....18.6..3.75......4.......7214....3....247.........5..82...969.6.85.2.
........88..2..5...5.9....7..8.549..1......8..428....3..74.....43..1..656...2....
........76.......3.7.16......2..1...8.7.3.92..4...6.8...6....4.53.84...9..8..93..
983.......1..2........5.....2.9..3...9..1542.1...468........6.1..24....8.4.5....3
..........7..51.98..9..72.6..3...1...54....2..9.2..5.4...3..7.2..6.8....4.1.....5
...........859.72..2..3.8.97........23..8.5.7..5...1.4.....7..8.5.6.1...9..85....
....9..6....75.18.67.......5..3..2....3.14...4.2...3.......8..9......71.3..147..5
...39.8...95.....1..4..1.......7.38..5......9...98.1.66.8.......7....2...4.2..638
.......1..436..2..8...1.9...7..3...43817......54...8.....8........24.35.....6.4.1
..........7.4.5.8.....2.6.9.........8.37...2.42.9..517.........5..1.8.4.71..54.9.
5....8.3...8...4..31..5......6.4...9.....1..6...6..7...3.2.5...9...6.2.348..9...5
.7.........6..179....9.8.3...4......13..6....2...3..54.....4...8...169.3.1..9.4.2
.5.....977..8.2......9...3.3.7.9.1...4....6...65..1...6.3.........72...18...16.5.
...........5..781....5.8.73........1.9...3.4..7.219.5...1......8..39.5...59..4..2
..2....1..482..5...3...492.3....6..8.....3....948.57...2..3...7...7.8...8.....3..
..3............384.851....9.......678...9......14.......967..4.36..4.9..4....971.
.81....65..59..2..4...6.1....7.......36..7....4....52......9...6....2.51....784.2
..5.4..62....3..7937.21.........1....31..8..62......4...4.7........8.69.5..6...2.
..9.7..6..4..52.......46.92.6.5...87..3..9..4.8.4....5..5.....667............73..
.7.2...9...2...1.5...9..38.....9...4.58312....9..8..2..8....2.......69..1.3....4.
.6....49.....5..7.3..9.1.8......2.5....31....4.....36...2.8...68..1.52..1...7.8..
....82......5......1..9.6....24..5....926..4.4......61..3.......9.3...566.817...4
5...9...4..7......9.2..7........9...3..7.61..2.41....9.3...27....9.84.1.......348
..4......3.....5....94.5..3.3.........56..8...8.2541.76....97..2.....9.5...82..6.
..8..3.17..26....89.6....3.....5...32.....546.6...28......3.1....5.9....1....4..5
..4....7.........5.874...695....69...2.....169..3.12..8..5.......9.74.3.7.......8
....4..7..295.634..14........8.....91...........7.2.1......38.6.9.6...5.3..8..49.
..........84....531...3.82.........96.....3..83519...7..1..5....6.8.....9...6.412
3.1..7..4.....6...846..3.......7.5..6.41..8..73...4....8.9..71.1.3.8......2......
.8..3....3.92.....6528.......4...7.1.93.5...2........5....8.........2.4...7.14359
..38....48..5.......5..3.8.......8..65.7.2.4.78...19....694..1.........731...6...
....946....286...9.....3.48..9.....1..13.7....74...5..8.....42..9348........7....
1..82.6.......4...5.2.9..7....9....66..5..49...9....81........7.9..3.....3..12.48
.....8......3..148.4.....62..7.1...5..5.67..4.8...5...6.1....2...2......3.46..91.
......96...7.31.......89.21.5........728.3....63.24..5........831....5.....318...
.2.....5.......6.3.6.1..7....7....89.9.5.....8...7.3.5...9.4.7..14......5.28.3.9.
.8...4...2....8..4..729.......3..5.2.9.5...6...2..68.3...1......63..5.7.7.....94.
.5...7....1.....8.8.....654.4.2....52.1.6..485...4.3..............3.8.6.3..49...2
5....6..4..62...8.4.8.5.....8.3.....2.......9..4....1......24..659.8.7......675.8
26......3.5.1.9.62......5...4...6...6...8.3..87.3..2.............9.6.4.5...5.4.79
............8752..7.86.......5......8.4....2.637.5.4.......1...14.3.8..5..3.9..14
.......7......1..8.7..8...62..6.9.3.1....3.85..3...2..92..3..5.3.12..9....5..4...
4....5....324..89..7.28......6...2..34.9..........7..4........9213.4..8..9.6...3.
..4.37.....9.5..4.5....4..3........7....4.68.6.5.......6..82..99.2..5.3.3.....7.8
....7..3...7.3.21..........6........5..29....389...57..2.6..94..6..49..3.4...3..8
6..3....4..5......2...47......9....69...1...5.7.2..93......1.5.5..42.....176.52..
2.5.....4...46..2..8.....39.5...7...7.6321.....28...9...9..23...2.........1.7.4..
.....9......8..9.6.61....3......7.....4...37...9.415.2....2...73.....1.58..51.42.
348.....2....6..83.6....1...9..8....6831...7.2.1......9....43..........8....312.9
..5.6.....9.5.48...73..8..4............1.6.5.5.7..39.1..9......4.2....19.3....7.2
.........4...68.35......24...5..1..4....8....9.4..36.175.3.4..6..9.1.....617.....
..........7....8.6362.1..7...3....4..9.7.2.1..864...3...5.8.....1...4....4..21.85
.....6......93.1......7.962.6.4.......3....5.45...76...34....9.19..4.7.66......81
.............2964.29....5.3.......5..83.17..957.2.4..1.....1...7...423......6.7.5
....8.......5.42..54..7286..63.1...5.81...6.........4.....3..2..547.....8.2...5.6
.......1.2...1.3.7.1.8739.5.31....58......6..76...1....9.......38..6.1.4.....2.8.
.6...2.7.......5...3..71.92.92.65.87.1...4..97..9.....8.1........4.9..1........45
.....8..6..61.57.8............2.......798.23..2.3...71..1...5..7.3...86..52.7...9
......8...182..6..7.4..3.....1.58..6...7....1.7..2..8...5...36.3.65.4.2.....3.4..
36..2.7.99..3..21...4....3.5.6.....8..92.8......5..4...5.......49...538.....7...2
..1..5.....5.7..2.437.19...1.8.............78.6....23.........6...8.74....6.41592
.9..3.2....4..713....4...7......5....4.7.638..6.1..7.28513.4.6...6.......3.......
...98..1.7...3.6...9.1....2.....2......79.2.69.2...3.81........8.746.....5....763
.86..9...1.5.8.2....413.7............6...4.38...392..5....5...2.......6..1.92.8.4
..........2...3.4...57.8.36...........283.....74265.8...1.....558...21.4...3..87.
.....3.2....4....6.745.6..3.58....3.1..8..7...2.....4....7....15..64.2...81..56..
5...2.......374....74....9......8..1..273..4...825.3.6.6..1.........3.8.7.3...1.9
....83...58312.6..4.1..9........6....4....9..6.2...38.3...7.81...9.6....81......7
......3..2.483.....83..1..4.76...12......9.3.9.5..........75......6..4186..4.8.7.
......9..2.1.6.7....72...65.6...8.9...23...4...3..48.2.1...2.....6.3..5...974....
..3.4........7...6...128....21.8..3..7.....4.3....7..1.1.6.28.42...9..1...8...36.
..........1.9....88....3.2.2....9.1..9..61.72.6.72.4.3.74...5..9.......1...4.7..9
..7.13.4.2.4.9..17....4....92....7.4...93...5..1.....3....7.9.....3......3.4.56.1
48..9.3..3.7..2..6.......8..3...6..28..25.....65.37.........43.5...78....9.4....5
.....8....6..31...2.7.9.....42.....1.....348..1.....76..9.......2...7.3..3862519.
...9.......2..4.56.31........5...1.9.1.25.36...4....2....7....21....26...26.93..5
7...6.....8..41.....29...41.......1.....39287.27...3....3....9..951.3..6.....5.7.
.....1....2......86912............141.25.6..38...2.5.6..5......73.........63194.5
9..5....83...4.92..68..3.5....96..1......7..4..743.6.27..3.9..........8..5.1.....
7....6..3....1........9.4..3...2579....16.....4..37.5..62...5371.8...6.........19
..............1..6.8.4657.......7.....9...2....3159.6..97.......467..9.2.21.43..7
...........5..28.3.6...9.54..........9356..1..2..91.47.......71.3....4...721.4..6
.18.4..6...3..6.91..4..3..2..658.....8..1..23.45..............6......13....3..289
............7...2313...94......43....4.8..19258.9.......8..2...4..1..2.6.1..7..38
....132.7.14..28.3.....5.......3....569.7.....235..1.8..6.....1......7.529...7...
.185....2...23...4.3...1.59.....9.1..45....96.93.1.2...84.....5..6..4..........7.
...........426....9.6.57..4.5...........8..29.8.9...56..1..8.9...85..34.7..6.3..1
2...6.....7.9...5.8.9..57.6.......39..3..8..2.4....5......7.....9.286.1.1.65.3...
.........1.6.5.3...37.186.4.....9....5123.7...69.8...........8..1......328...316.
..12..7....36...187.....2......5..2.42.1.8.....5..21.......4..5649..18...3.9.....
5...7.....63....9.7..3.25.4.76.2...1..16....8.5.1....9.4.....2....9.3.....7.1..8.
8...1.4.5.......6..63...7..7............72.39...8.....68.3..9.4.1...438..479....6
..4.......6.523..835.1....7....5.2..4..2.876...1..6....3...........95.....78..359
.6.......3.7.....818..62.4...3..8..2...4.518....72.4...1.5.....7.8..1...2....67..
4..........93.1...385.64..7.4.............3686..7..2...6.57....8..4.9..6.941.....
....7..98...6...5...6...1.4.2......13.49.6.2...1.27.8.........915.3.....94...58..
..1..2..9.74......9327..4.68.....6.3....6.9.43....9.5.....23.4.7..5........1..3..
...17.43...3..9..1...2....5.........7...23..4.36.547..8.53.......25.......4.9.6.8
..67...244....59.7.7..1.6.53....68...41...........2....2...149.........6....497.2
........42.7.6.19.6...93........1.....2.8.7.91..9.685.8.6...4.7.......8.7...5..2.
....7.5..2....4.63..6..2.8..9..85...5..26...7.21.4......5..9..4......63.....3.97.
.8..1.........72.83...4.16....7..3..4.93..85.6........9.3..2.84...93.5...5..7....
....2.9.7...4...8...6..3.5...........9..6..4....2.9518....14.7..81.72..4.6..3..9.
1.8...5...279.....9..7.18..8.43.9.....2.4.1.3....2...9.....43.....2..95.4....8...
...56........7.31..8..31..6.........96..8...7..5....321......4..3..17.65..63.41..
...8....1....27.96..75..83..4.3.....3...5...7.956.8.....19.2..8..4...3.......6.1.
..9.8.......1.....68...7.19.2...4..71...3..4.46.79.....7..6...3.....2.9..963...2.
......71......9.2..6.571..95.....8...738......4.3..2.7154.2.9....7...1......45...
.1.2.8.......5.6.7...671.2.3..5....1..1....4..6...2.5......7....27....9.6.519...2
.8.........2654.1.4.5...........8.41..8....2.17....86......9....5.34..892....16.4
.81.94...25...........7....72..1..3...5....9..9638...7.....84..51......9..81...25
..3.....612.7.8..45.4..1.7...89..5...4.3.67..3.......2...8..4....1..58......1..9.
.1..8....69...4..2.....65....6.3924..4..1..5.839....6..6254....4.....1.........2.
6.7.8...1......7...9....3.5.2..1.8....5.....78....64...1.93...49....5.....28.15.9
......6..96........84.5.1....3..9..42...178..85..4..2.5.6.28....2.7.....4....5.7.
.9...5..68..1..9............84......52..16...6.39.8..5....3.5..3...5.8..75...214.
.....7.....3.56.2.97..1.64.........2..7.2.93..2....16...........615..49...964..7.
4.....5.1..5.64.....9..........5.1....1..97.5.5.1..924..45.3..7.....76.22...9....
...9....4....7.8..28....1.367........3....2.1.21.9..6..9.5.....8..234..7...71..8.
.....4.....5..76..1.85..27......6...3......825.9.481...5.....1.8.1.9.72.6...7....
.97..16..6.4.7..3.53......4.1..6..72.....3.....87..3.1....2.....4..96.8..7....9..
.....8..6.5.3...1...71.6..2......9.4913....2..65.3...7.3..8......15..8..5......43
.......7..68...2...579.2..38...1.......8...1...4.....2.7.2.4....83.9.5..5..13.79.
..........5..3.9....41...522.68....35.8.6..1..31.2.6..........5.....23.8...5.1.24
.4...23..8...1......96.5.2...........74..3.6.9.1427.........1...9....23...523..74
....8..6.8....7..394.25........2....6..3.1....2867.3...........31.....964.9..8.21
.6.....5.9.2....613....64.24...6.....3..52.9.5..4.3....89....4......72.....82..1.
..........54.9..67..1.2..48...6.....73......458.....3..6.9.7....4.86..79..8.4...3
.73.9.......48..7.8.4...2.39..3..8......5....3169..........51.7.6.7.....5...19..8
.5..6..2..4....7.......2.81.6..4.8.......6.4...4.98.3..86...3........27..97.836..
.54...8..98..3.6..6.19.8.4..1..........89.7..5..62...8....5..6..9.....7347..6....
.9...4.25.36...91.........43........2..67.4.8..45....294.15.......7....9178.9....
..3........8..71..56..9...2..53.46......7....32.6..57..3...2..7..2......67.813.5.
.5.......21..5.9.3..92.846...........923..58.....856....5..4..9.2.....4..4...97.6
..46.91...6..5..271..4.2..63......92.....3.4.475.....389...62..............9.73..
.8..6......2...18..7...3........12...43....1..51.76438.2........38...72...67.9.5.
......5....43.1.6.69.8.42.3....3.45.9....87.2...2.9..6.........2..983....89.7....
.........76..45...9.5.3.746.1.....5..86..1.73..9..2.....8....6..9..8.5.7....2..38
.....89..6.3.49.1....5..6....4.....923......1.5...2.6...7......3.2.51...5.896.2.3
3.76....2.....18.4.9....57......3.4995346...8.2......5..2......58..36.....95.....
.....5.....7.6.43.4.6..82.5..2........8.749..6.18.......35......6...1.2.1..327.9.
.1...7......59.23..5.8.......6......2..9..3..59.7.2.8.1.4.7...3...2..64..29.4...5
.........54..9...3....1.764.....3...6.4...2.129.....3......4.16.1..693.77.6....45
......76......8..54..26.....1..5...47...8.53.3....61.......1....87.....364..35871
........4.....5.79.9..2.531....79....6.5.8....7....35......1....15.928.72..8.7.15
25...7..1.....4.5..1..2.367...6.........81.3..8..4.7.662.1...7...94....88....6..3"""

  time = 0.0
  generated_nodes = 0
  discarded_nodes = 0
  solved = 0
  no_solution = 0
  
  if difficulty == 'hard':
    data = hard_data.splitlines()
  else:
    data = medium_data.splitlines()
    
  print("%d"%len(data) + " entries of data are loaded.")
  
  for d in data:
    solver = SudokuSolver('3x3')
    solver.showProgressRate(0)
    if len(d) == 81:
      s = d.replace('.', '0')
      for i in range(81):
        v = int(s[i])
        if v != 0:
          solver._restraints[i] = v
    result = solver.solve(method, True)
    solved = solved + 1
    print("Finish %d"%solved + " puzzles already.")
    if result[0] == []:
      no_solution = no_solution + 1
    time = time + result[1]
    generated_nodes = generated_nodes + result[2]
    discarded_nodes = discarded_nodes + result[3]
    if d == 2:
      break
  
  if method == 1:
    print("Order Method 1: Put numbers into squares in turn. i.e. from left to right, top to bottom.\n")
  else:
    print("Order Method 2: Put numbers into squares according to the possible numbers of that squares.\n")
  print("Puzzles Solved: %d"%solved)
  print("Puzzles Found Solutions: %d"%(solved - no_solution))
  print("Total Nodes Generated: %d"%generated_nodes)
  print("Total Nodes Discarded: %d"%discarded_nodes)
  print("Total Time Used: %f"%time + "s")
  print("Average Time Used to Solve One Puzzle: %f"%(time/solved))
  print("Average Nodes Generated/Discarded: %d"%(generated_nodes/solved) + "/%d"%(discarded_nodes/solved))
  
if __name__ == "__main__":

  # This function will try to solve 1465 top hard sudoku games or 1001 medium-hard sudoku games with 81 squares via method 1 or 2, and record the time used by the solver and the amount of the nodes generated and discarded.
  # Method 1 means that the program will use the modfication (2) to BFS (Line 95) to decide the order of squares that will be put a number.
  # Mehtod 2 means that the program will generated nodes according to putting numbers from the left to right and top to bottom.
  # This function would take more than one day in my MacBook Pro 2012. So, take the time-consuming into your account before you run it.
  # big_data_test(1, 'hard')
  # big_data_test(2, 'medium')
  pass
