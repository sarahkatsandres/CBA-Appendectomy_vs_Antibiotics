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
# See figure DecisionTree_Appendicitis.png for the structure of this decision tree
########################

# create the terminal nodes
T1 = TerminalNode('T1', 112421, 70.9)
T2 = TerminalNode('T2', 6058, 94.5)
T3 = TerminalNode('T3', 6058, 0)
T4 = TerminalNode('T4', 4421, 0)
T5 = TerminalNode('T5', 4421, 90.4)
T6 = TerminalNode('T6', 10479, 90.0)
T7 = TerminalNode('T7', 122900, 70.9)
T8 = TerminalNode('T8', 10479, 90.0)

# create C1
C1 = ChanceNode('C1', 15799, 0, [C2, T3], [0.9972, 0.0028]) #p1
# create C2
C2 = ChanceNode('C2', 15843, 0, [T1, T2], [0.092, 0.908]) #p2
# create C3
C3 = ChanceNode('C3', 8675, 0, [T4, C4], [0.00075, 0.99925]) #p3
# create C4
C4 = ChanceNode('C4', 8678, 0, [T5, C5], [0.74, 0.26]) #p4
# create C5
C5 = ChanceNode('C5', 20793, 0, [T6, C6], [0.0028, 0.9972]) #p5
# create C6
C6 = ChanceNode('C6', 20822, 0, [T7, T8], [0.092, 0.908]) #p6

## WHY AREN'T THESE WORKING? Says they are not defined...

# create D1
D1 = DecisionNode('D1', 0, 0, [C1, C3])


# Cost-utility
arm1_cost = C1.get_expected_cost()
arm1_utility = C1.get_expected_utility()
arm2_cost = C2.get_expected_cost()
arm2_utility = C2.get_expected_utility()

print('Expected cost and utility of Appendectomy')
print(arm1_cost)
print(arm1_utility)
print('Expected cost and utility of Antibiotics')
print(arm2_cost)
print(arm2_utility)

# Incremental Cost Effectiveness Ratio (ICER)
ICER_info = (arm2_cost-arm1_cost)/(arm2_utility - arm1_utility)
print('ICER of Antibiotics with respect to Appendectomy:', ICER_info)
