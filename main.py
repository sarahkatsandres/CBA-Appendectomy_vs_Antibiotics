# FINAL PROJECT - Antibiotics vs. Appendectomy for acute non-ruptured appendicitis in adults
# A population-level cost-benefit analysis

# ATTEMPT AT USING A DECISION TREE INSTEAD OF A MARKOV MODEL

class Node:
    """ base (master) class for nodes """
    def __init__(self, name, cost, utility):
        """
        :param name: name of this node
        :param cost: cost of visiting this node
        :param utility: utility of visiting this node
        """

        self.name = name
        self.cost = cost
        self.utility = utility

    def get_expected_cost(self):
        """ abstract method to be overridden in derived classes
        :returns expected cost of this node """

    def get_expected_utility(self):
        """ abstract method to be overridden in derived classes
        :returns expected utility of this node """


class ChanceNode(Node):

    def __init__(self, name, cost, utility, future_nodes, probs):
        """
        :param name: name of this node
        :param cost: cost of visiting this node
        :param utility: utility of visiting this node
        :param future_nodes: (list) future nodes connected to this node
        :param probs: (list) probability of future nodes
        """

        Node.__init__(self, name, cost, utility)
        self.futureNodes = future_nodes
        self.probs = probs

    def get_expected_cost(self):
        """
        :return: expected cost of this chance node
        E[cost] = (cost of visiting this node)
                  + sum_{i}(probability of future node i)*(E[cost of future node i])
        """

        # expected cost initialized with the cost of visiting the current node
        exp_cost = self.cost

        # go over all future nodes
        i = 0
        for node in self.futureNodes:
            # increment expected cost by
            # (probability of visiting this future node) * (expected cost of this future node)
            exp_cost += self.probs[i]*node.get_expected_cost()
            i += 1

        return exp_cost

    def get_expected_utility(self):
        """
        :return: expected utility of this chance node
        E[utility] = (utility of visiting this node)
                  + sum_{i}(probability of future node i)*(E[utility of future node i])
        """

        # expected utility initialized with the cost of visiting the current node
        exp_utility = self.utility

        # go over all future nodes
        i = 0
        for node in self.futureNodes:
            # increment expected utility by
            # (probability of visiting this future node) * (expected utility of this future node)
            exp_utility += self.probs[i]*node.get_expected_utility()
            i += 1

        return exp_utility


class TerminalNode(Node):

    def __init__(self, name, cost, utility):
        """
        :param name: name of this node
        :param cost: cost of visiting this node
        :param utility: utility of visiting this node
        """

        Node.__init__(self, name, cost, utility)

    def get_expected_cost(self):
        """
        :return: cost of this visiting this terminal node
        """
        return self.cost

    def get_expected_utility(self):
        """
        :return: utility of this visiting this terminal node
        """
        return self.utility


class DecisionNode(Node):

    def __init__(self, name, cost, utility, future_nodes):
        """
        :param name: name of this node
        :param cost: cost of visiting this node
        :param utility: utility of visiting this node
        :param future_nodes: (list) future nodes connected to this node
        (assumes that future nodes can only be chance or terminal nodes)
        """

        Node.__init__(self, name, cost, utility)
        self.futureNode = future_nodes

    def get_expected_costs(self):
        """ returns the expected costs of future nodes
        :return: a dictionary of expected costs of future nodes with node names as dictionary keys
        """

        # a dictionary to store the expected cost of future nodes
        exp_costs = dict()
        # go over all future nodes
        for node in self.futureNode:
            # add the expected cost of this future node to the dictionary
            exp_costs[node.name] = self.cost + node.get_expected_cost()

        return exp_costs

    def get_expected_utilities(self):
        """ returns the expected utilities of future nodes
        :return: a dictionary of expected utilities of future nodes with node names as dictionary keys
        """

        # a dictionary to store the expected cost of future nodes
        exp_utilities = dict()
        # go over all future nodes
        for node in self.futureNode:
            # add the expected cost of this future node to the dictionary
            exp_utilities[node.name] = self.utility + node.get_expected_utility()

        return exp_utilities


#######################
# See figure DecisionTree.png (from the project menu) for the structure of this decision tree
########################

# create the terminal nodes
T1 = TerminalNode('T1', 10, 0.5)
T2 = TerminalNode('T2', 20, 0.6)
T3 = TerminalNode('T3', 30, 0.7)
T4 = TerminalNode('T4', 40, 0.8)
T5 = TerminalNode('T5', 50, 0.9)

# create C2
C2 = ChanceNode('C2', 35, 0, [T1, T2], [0.7, 0.3])
# create C1
C1 = ChanceNode('C1', 25, 0, [C2, T3], [0.2, 0.8])
# create C3
C3 = ChanceNode('C3', 45, 0, [T4, T5], [0.1, 0.9])

# create D1
D1 = DecisionNode('D1', 0, 0, [C1, C3])


# ANSWER TO QUESTION 3
arm1_cost = C1.get_expected_cost()
arm1_utility = C1.get_expected_utility()
arm2_cost = C3.get_expected_cost()
arm2_utility = C3.get_expected_utility()

print('Expected cost and utility of Arm 1')
print(arm1_cost)
print(arm1_utility)
print('Expected cost and utility of Arm 2')
print(arm2_cost)
print(arm2_utility)

# ANSWER TO QUESTION 4
ICER_info = (arm2_cost-arm1_cost)/(arm2_utility - arm1_utility)
print('ICER of Arm 2 with respect to Arm 1:', ICER_info)
