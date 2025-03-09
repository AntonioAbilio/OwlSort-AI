class TreeNode:
    def __init__(self, state, from_idx=None, to_idx=None, parent=None):
        self.state = state
        self.from_idx = from_idx
        self.to_idx = to_idx
        self.parent = parent
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self
    
    def set_parent(self, parent_node):
        self.parent = parent_node
    
    def __eq__(self, other):
        if not isinstance(other, TreeNode):
            return False
        if (self.state != other.state):
            return False
        return True
    
def trace_path(node):
    parent = node.parent
    path = []
    while parent is not None:
        path.append((parent.from_idx, parent.to_idx, parent.state)) 
        parent = parent.parent
    else:
        print("No solution found.") 
    path.reverse()
    path.append((node.from_idx, node.to_idx, node.state))
    return path
