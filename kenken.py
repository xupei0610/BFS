"""
 This is a KenkenSolver written by Pei Xu using BFS
 
 
 I use a simple way to prune the search tree during producing child nodes for the purpose of decreasing the time and memory used by the program.
 That is to discard the node in the state which conflicts with the rule that all elements in a row are unique.
 e.g. Discard the node [[1,1],[0,0]] in the process of generating the child nodes of the node [[1, 0], [0, 0]]
 
 The example and the runtime of solving 3X3, 4X4, 5X5 KenKen games are at the end of the program.
"""

class KenKenSolver:
  """ A KenKen Solver """

  def __init__(self, size):
    self.size = size
    self._goal = []
    self.operatorAction = {
      "+": self.operator_plus,
      "-": self.operator_minus,
      "*": self.operator_multiply,
      "/": self.operator_divide,
    }
    self.initial_state = []
    for i in range(size):
      self.initial_state.append([])
      for j in range(size):
        self.initial_state[-1].append(0)
  
  def setGoal(self, operator, value, elements):
    self._goal.append([operator, value, elements])
      
  def operator_plus(self, value, elements):
    if sum(elements) == value:
      return True
    return False

  def operator_minus(self, value, elements):
    if abs(elements[0] - elements[1]) == value:
      return True 
    return False
  
  def operator_multiply(self, value, elements):
    result = 1
    for x in elements:
      result = result * x
    if result == value:
      return True
    return False
  
  def operator_divide(self, value, elements):
    if elements[0] > elements[1]:
      result = elements[0] / elements[1]
    else:
      result = elements[1] / elements[0]
    if result == value:
      return True
    return False
      
  def isGoal(self, node):
    range_size = range(self.size)
    element_size = []
    for i in range_size:
      element_size.append(i+1)
      
    for i in range_size:
      if sorted(node[i]) != element_size:
        return False

    for g in range(len(self._goal)):
      elements = []
      for e in self._goal[g][2]:
        x, y = divmod(e-11, 10)
        elements.append(node[x][y])
      if self.operatorAction.get(self._goal[g][0])(self._goal[g][1], elements) == False:
        return False
    
    return True
    
  def getChildNodes(self, parent_node, iter_times):
    
    # iter_times decides which square is being operated now
    i, j = divmod(iter_times, self.size)
    if i == self.size:
      return []
    
    child_nodes = []
    
    for k in range(self.size):
      ch = []
      
      # copy parent_node
      for l in range(self.size):
        ch.append([])
        for m in range(self.size):
          ch[l].append(parent_node[l][m])
          
      # generate child_node
      ch[i][j] = k + 1
      
      # check validity of child_node
      # check the uniqueness of the elements in a row
      discard = False
      for l in range(self.size):
        for x in ch[l]:
          if x != 0:
            if ch[l].count(x) > 1:
              discard = True
              break
      if discard == False:
        for c in range(self.size):
          tmp = []
          for r in range(self.size):
            tmp.append(ch[r][c])
          for x in tmp:
            if x !=0:
              if tmp.count(x) > 1:
                discard = True
                break
        if discard == False:
          child_nodes.append(ch)
    return child_nodes

  
  def output(self, node):
    for i in range(self.size):
      s = ''
      for j in range(self.size):
        s = s + '%d'%node[i][j] + ' '
      print(s)
  
  def solve(self):
    frontier = [self.initial_state]
    i = 0
    depth = 0
    max_depth = self.size * self.size
    print(max_depth)
    while(frontier):
      node = frontier.pop(0)

      if depth == max_depth:
        if self.isGoal(node) == True:
          return node
      
      for ch in self.getChildNodes(node, depth):
        frontier.append(ch)
          
      if i == 0:
        print(depth)
        depth = depth + 1
        i = len(frontier)
      else:
        i = i - 1

    return []
    
      
if __name__ == "__main__":

  print("KenKen Solver by Pei Xu")
  
  """
  solver = KenKenSolver(3)
  solver.setGoal("+", 2, [13])
  solver.setGoal("-", 2, [11, 12])
  solver.setGoal("*", 3, [22, 23])
  solver.setGoal("/", 2, [21, 31])
  solver.setGoal("-", 1, [32, 33])
  """
  """
  Solution:
  3 1 2 
  2 3 1 
  1 2 3 
  RunTime: 0.003714s
  """
  
  """
  solver = KenKenSolver(4)
  solver.setGoal("+", 5, [11, 12])
  solver.setGoal("*", 8, [13, 14, 24])
  solver.setGoal("/", 2, [21, 31])
  solver.setGoal("-", 2, [22, 32])
  solver.setGoal("*", 4, [41, 42])
  solver.setGoal("+", 9, [23, 33, 43])
  solver.setGoal("-", 2, [34, 44])
  """
  """
  Solution:
  3 2 1 4 
  4 1 3 2 
  2 3 4 1 
  1 4 2 3 
  RunTime: 0.441849s
  """
  
  #"""
  solver = KenKenSolver(5)
  solver.setGoal("+", 10, [11, 12, 13])
  solver.setGoal("-", 3, [14, 24])
  solver.setGoal("-", 1, [15, 25])
  solver.setGoal("/", 2, [21, 31])
  solver.setGoal("*", 6, [22, 32])
  solver.setGoal("-", 2, [23, 33])
  solver.setGoal("+", 5, [34, 44])
  solver.setGoal("+", 6, [35, 45])
  solver.setGoal("-", 2, [41, 42])
  solver.setGoal("/", 2, [43, 53])
  solver.setGoal("*", 5, [51, 52])
  solver.setGoal("*", 6, [54, 55])
  #"""
  """
  Solution:
  1 4 5 2 3 
  2 3 1 5 4 
  4 2 3 1 5 
  3 5 2 4 1 
  5 1 4 3 2 
  RunTime: 575.798663s
  """
  
  import time
  start = time.clock()
  
  goal = solver.solve()
  
  end = time.clock()
  
  if goal:
    print("Solution:")
    solver.output(goal)
  else:
    print("No Solution")
    
  print("RunTime: %fs"%(end-start))
    
 
