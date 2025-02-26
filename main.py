import graphviz

class TreeNode:
    """
    This class creates a TreeNode object that represents a node in the centipede.

    Args:
        key (str): A string representing the unique id for the node.
        player (Optional[str]): A string representing the player making the choice as well as the cycle number. It will be presented as "{player}{cycle number}", where player can be either "S" or "T" and cycle number will range from 1 to number of cycles.
        payoff (tuple[int, int]): A tuple containing the respective payoffs for both players
        parent (Optional[TreeNode]): The parent node to this TreeNode
        right (Optional[TreeNode]): The right child node to this TreeNode, representing the "R" option in the binary tree
        down (Optional[TreeNode]): The down child node to this TreeNode, representing the "D" option in the binary tree

    Attributes:
        key (str): A string representing the unique id for the node.
        player (Optional[str]): A string representing the player making the choice as well as the cycle number. It will be presented as "{player}{cycle number}", where player can be either "S" or "T" and cycle number will range from 1 to number of cycles.
        payoff (tuple[int, int]): A tuple containing the respective payoffs for both players
        parent (Optional[TreeNode]): The parent node to this TreeNode
        right (Optional[TreeNode]): The right child node to this TreeNode, representing the "R" option in the binary tree
        down (Optional[TreeNode]): The down child node to this TreeNode, representing the "D" option in the binary tree
    """
    def __init__(self, 
                 key: str, 
                 player: str = None, 
                 payoff: tuple[int, int] = (float('inf'),float('inf')), 
                 parent: "TreeNode" = None, 
                 right: "TreeNode" = None, 
                 down: "TreeNode" = None
                 ):
        self.player = player
        self.key = key
        self.payoff = payoff
        self.parent = parent
        self.down = down
        self.right = right

def build_tree(number_of_cycles):
    id = "S"
    root = pointer = TreeNode(id, player = "T1")

    for cycle in range(1, number_of_cycles+1):
        # generating initial node for cycle
        pointer.down = TreeNode(key = id+"D", payoff = (cycle if cycle == 1 else cycle+1 , max(cycle-1, 0)), parent = pointer)

        if cycle == number_of_cycles:
            pointer.right = TreeNode(key = id + "R", payoff=(number_of_cycles, number_of_cycles), parent=pointer)

        else:
            # updating id
            id += "R"
            pointer.right = TreeNode(id, player="S"+str(cycle), parent=pointer)

            # moving pointer to the right node
            pointer = pointer.right

            pointer.down = TreeNode(id+"D", payoff=(max(cycle-1, 0), cycle+1), parent = pointer)

            # updating id with choice
            id += "R"
            pointer.right = TreeNode(key = id, player="T"+str(cycle+1), parent=pointer)
            pointer = pointer.right
    
    return root, pointer

def find_better(node: TreeNode):
    if node:
        turn = node.player[0]
        if turn == "T":
            payoff1 = node.down.payoff[0]
            payoff2 = node.right.payoff[0]
        elif turn == "S":
            payoff1 = node.down.payoff[1]
            payoff2 = node.right.payoff[1]
        else:
            return None
        
        node.payoff = node.down.payoff if payoff1 > payoff2 else node.right.payoff
        
        return node
    return node

def find_spe(node:TreeNode):
    best_node = find_better(node)
    while best_node.parent:
        best_node = find_better(best_node.parent)
    best_node = find_better(best_node)
    return best_node

def calculate_poa(node:TreeNode, spe_node:TreeNode):
    best_payoff = node.right.payoff
    social_optimal_outcome = sum(best_payoff)
    spe_payoff = spe_node.payoff

    poa = social_optimal_outcome/sum(spe_payoff)
    return poa
    


def visualize_binary_tree(root: TreeNode, spe_node: TreeNode = None) -> None:
    """
    This function is used to generate an image visualization of the binary tree. The resulting image will be of 'png' format and the resulting node from rational NE is highlighted in red. 

    This function does not run any algorithms, instead it is purely used for visualization of the binary tree and the resulting solution.

    Functions:
        add_node_edges: refer to documentation of the function below

    Args:
        root (TreeNode): TreeNode referencing the root node of the binary tree
        spe_node (TreeNode): TreeNode referencing the node from rational NE
    
    Return:
        None
    """
    # creating the graphviz digraph object
    dot = graphviz.Digraph()

    def add_nodes_edges(node: TreeNode) -> None:
        """
        This function is used to add the directed edges to the respective nodes

        Args:
            node (TreeNode): TreeNode referencing the target node
            unique_id (str): unique id for the node on graphviz diagram

        Return:
            None
        """
        if node.down.payoff == spe_node.payoff:
            dot.node(node.down.key, label = str(node.down.payoff), style='filled', fillcolor='red')
        else:
            dot.node(node.down.key, label = str(node.down.payoff))


        if node.right.right:
            if node.right.payoff == spe_node.payoff:
                dot.node(node.right.key, label = node.right.player, style='filled', fillcolor='red')
            else:
                dot.node(node.right.key, label = node.right.player)

        else:
            if node.right.payoff == spe_node.payoff:
                dot.node(node.right.key, label = str(node.right.payoff), style='filled', fillcolor='red')

            else:
                dot.node(node.right.key, label = str(node.right.payoff))

        dot.edge(node.key, node.down.key, label = "D")
        dot.edge(node.key, node.right.key, label = "R")

    dot.node(root.key, label = root.player)
    while root.right:
        add_nodes_edges(root)
        root = root.right

    # output png file showing a visual of the generated binary tree
    dot.render('binary_tree', view=True, format='png')



if __name__ == "__main__":
    k = int(input("Number of cycles: "))
    root, lowest_parent_node = build_tree(number_of_cycles=k)
    spe_node = find_spe(lowest_parent_node)
    poa = calculate_poa(node = lowest_parent_node, spe_node=spe_node)
    print("The SPE payoff will be", spe_node.payoff)
    print("The PoA is", poa)
    visualize_binary_tree(root, spe_node)
            