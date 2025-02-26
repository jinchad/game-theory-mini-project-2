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

def build_tree(number_of_cycles:int) -> tuple[TreeNode, TreeNode]:
    """
    This function is used to build a binary tree with depth number_of_cycles. 

    The binary tree will only be expanded on the right child and will carry a "centipede"-like structure.

    Args:
        number_of_cycles (int): the depth of the binary tree to be generated
    
    Returns:
        root (TreeNode): TreeNode reference to the root node
        pointer (TreeNode): TreeNode reference to the parent node at the lowest depth
    """
    # string id for each node generated, with "S" representing start
    id = "S"

    # initializing the root and pointer references, both pointing to the root node
    root = pointer = TreeNode(id, player = "T1")

    # for loop iterating for number_of_cycles times, from 1 to number_of_cycles + 1
    for cycle in range(1, number_of_cycles+1):
        # generating "down" child node
        pointer.down = TreeNode(key = id+"D", 
                                payoff = (cycle if cycle == 1 else cycle+1 , max(cycle-1, 0)), 
                                parent = pointer
                                )
        
        # if statement checking if this is the final iteration of the for loop. 
        if cycle == number_of_cycles:
            # setting the final "right" child node
            pointer.right = TreeNode(key = id + "R", 
                                     payoff = (number_of_cycles, number_of_cycles), 
                                     arent = pointer
                                     )
        else:
            # updating id with "R" which represents the pointer moving right
            id += "R"

            # setting the "right" child node to be an "empty" choice node
            pointer.right = TreeNode(key = id, 
                                     player = "S"+str(cycle), 
                                     parent = pointer
                                     )

            # moving pointer to the right child node
            pointer = pointer.right
            
            # setting the "down" child node with it's respective payoff
            pointer.down = TreeNode(key = id+"D", 
                                    payoff=(max(cycle-1, 0), cycle+1), 
                                    parent = pointer
                                    )

            # updating id with "R" which represents the pointer moving right
            id += "R"

            # setting the "right" child node to be an empty choice node
            pointer.right = TreeNode(key = id, player="T"+str(cycle+1), parent=pointer)

            # moving the pointer to the right child node
            pointer = pointer.right
    
    return root, pointer

def find_better(node: TreeNode) -> TreeNode | None:
    """
    This function is used to determine the node with better payoffs that will be returned with backtracking.

    Args:
        node (TreeNode): TreeNode referencing the target node whose child nodes will be compared
    
    Return:
        node (TreeNode): TreeNode with it's payoff replaced with the "best payoff"
    """
    # if statement checking if node is None
    if node:
        # obtaining the first character which determines the player who will be making the choice this turn
        turn = node.player[0]

        # if statement checking if it's the "T" player turn to choose
        if turn == "T":
            # obtaining the respective payoffs for "T" players from both child nodes
            payoff1 = node.down.payoff[0]
            payoff2 = node.right.payoff[0]
        # elif statement checking if it's the "S" player turn to choose
        elif turn == "S":
            # obtaining the respective payoffs for "S" players from both child nodes
            payoff1 = node.down.payoff[1]
            payoff2 = node.right.payoff[1]
        else:
            # None returned if the player's turn could not be determined. Error handling will be required for a more refined project here.
            return None
        
        # setting the payoff of the target node to the payoff of the "better node"
        node.payoff = node.down.payoff if payoff1 > payoff2 else node.right.payoff
        
        # returning original input node with new payoffs
        return node

    # returning the node (which will be None), if it's None
    return node

def find_spe_node(node:TreeNode) -> TreeNode:
    """
    This function is used to find the subgame perfect equilibrium (spe) payoff.

    This function works by working up a binary tree from the lowest parent node of the binary tree and iteratively comparing the payoffs of the child nodes.

    Args:
        node(TreeNode): usually the lowest parent node of the binary tree, which will find the node with the spe payoff

    Return:
        best_node(TreeNode): TreeNode referencing a node containg the spe payoff
    """
    # finding and storing the node with the better payoff
    best_node = find_better(node)

    # while loop that loops while best_node has a parent node
    while best_node.parent:
        # replacing best_node with the node with better payoff at the parents level
        best_node = find_better(best_node.parent)

    # final comparison between child nodes at the root level to determine the best payoff
    best_node = find_better(best_node)

    # returning the node containing the best spe payoff
    return best_node

def calculate_poa(node:TreeNode, spe_node:TreeNode) -> float:
    """
    This function is used to calculate the price of anarchy (poa) of the generated binary tree.

    This function assumes that the centipede pattern holds through to the final node, hence the social optimum outcome will be at the final leaf node. 

    Args:
        node (TreeNode): lowest parent node of the binary tree
        spe_node (TreeNode): TreeNode with the spe payoff

    Return:
        poa (float): the poa of the binary tree
    """
    # obtaining the best payoff from the binary tree
    best_payoff = node.right.payoff

    # obtaining the social optimal outcome from the best payoff
    social_optimal_outcome = sum(best_payoff)

    # obtaining the spe payoff
    spe_payoff = spe_node.payoff

    # calculating the poa, which is the social optimum outcome divided by the spe outcome
    poa = social_optimal_outcome/sum(spe_payoff)

    # returning the calculated poa
    return poa

def visualize_binary_tree(root: TreeNode, spe_node: TreeNode) -> None:
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
        This function is used to add child nodes and directed edges to the respective nodes

        Args:
            node (TreeNode): TreeNode referencing the target node

        Return:
            None
        """
        # if statement checking if the payoff for the "down" child is equal to the payoff for the spe_node
        if node.down.payoff == spe_node.payoff:
            # creates a node with red fill if so
            dot.node(node.down.key, label = str(node.down.payoff), style='filled', fillcolor='red')
        else:
            # else create a regular leaf node
            dot.node(node.down.key, label = str(node.down.payoff))

        # if statement checking if the right child has a right child node of its own. Essentially checking if the right child node is a leaf node of the tree.
        if node.right.right:
            # creating a child node with player move as the node label
            dot.node(node.right.key, label = node.right.player)
        else:
            # if statement checking if the payoff of the right child node is equal to that of the spe_node
            if node.right.payoff == spe_node.payoff:
                # creating a node with red fill if so
                dot.node(node.right.key, label = str(node.right.payoff), style='filled', fillcolor='red')
            else:
                # else create a regular leaf node 
                dot.node(node.right.key, label = str(node.right.payoff))
        # creating the edge connecting the parent node to the respective childs with labels representing the choice
        dot.edge(node.key, node.down.key, label = "D")
        dot.edge(node.key, node.right.key, label = "R")

    # creating the root node
    dot.node(root.key, label = root.player)

    # while loop that loops while root is not a leaf node
    while root.right:
        # add node edges for the root node
        add_nodes_edges(root)

        # shifting root pointer to the right
        root = root.right

    # output png file showing a visual of the generated binary tree
    dot.render('binary_tree', view=True, format='png')

if __name__ == "__main__":
    # user input for the number of cycles
    k = int(input("Number of cycles: "))

    # building the centipede structured binary tree and obtaining the root and lowest_parent_nodes
    root, lowest_parent_node = build_tree(number_of_cycles=k)

    # obtaining the spe_node for the binary tree
    spe_node = find_spe_node(lowest_parent_node)

    # calculating the poa of the binary tree
    poa = calculate_poa(node = lowest_parent_node, spe_node=spe_node)

    # print statements for the spe payoffs and the PoA
    print("The SPE payoff will be", spe_node.payoff)
    print("The PoA is", poa)

    # creating png visualization of the generated binary tree
    visualize_binary_tree(root, spe_node)
            