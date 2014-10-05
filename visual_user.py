from uuid import uuid4
from nodebox.graphics import Color, Text, RGB
from nodebox.graphics.physics import Node, Edge, Graph
from user import User
from user_network import UserNetwork

__author__ = 'Phillip Lemons'


# Can be used as default colors
red = Color(255, 0, 0, 240, base=255, colorspace=RGB)
green = Color(0, 255, 0, 240, base=255, colorspace=RGB)
blue = Color(0, 0, 255, 240, base=255, colorspace=RGB)
DEFAULT_NODE_COLOR = Color(230, 230, 230, 240, base=255, colorspace=RGB)


class DirectedGraph(Graph):
    """
    A directed graph is just like a graph except it's draw function automatically
    assumes the graph is directed. You can also specify whether the graph should
    be weighted in the constructor.
    """
    def __init__(self, weighted, *args, **kwargs):
        Graph.__init__(self, *args, **kwargs)
        self.weighted = weighted

    def draw(self, *args, **kwargs):
        Graph.draw(self, weighted=self.weighted, directed=True)


class VisualUser(User):
    EDGE_COLOR = Color(255, 149, 0, 230, base=255)

    def __init__(self, name, version, *args, **kwargs):
        User.__init__(self, name, version, *args, **kwargs)
        if not isinstance(version, Color):
            # Because this is a visual user we should make the version a color
            raise TypeError(str(version) + " is not a Color")

        # Generates a unique id for the node
        self.id = uuid4()
        node_text = Text(self.name, fontname="Droid Sans", fontsize=14)
        self.node = Node(self.id, fill=version, strokewidth=1, radius=15)
        self.node.text = node_text
        self.edges = list()

    def add_coach(self, other):
        """
        Adds coach to self.coaches and adds an edge for the connection on the graph

        :param other: The coach of self
        :type other: VisualUser
        :return: None
        """
        User.add_coach(self, other)
        other.edges.append(Edge(other.node, self.node, weight=1, stroke=VisualUser.EDGE_COLOR, strokewidth=2))

    def add_student(self, other):
        """
        Adds student to self.students and adds an edge for the connection on the graph

        :param other: Student of self
        :type other: VisualUser
        :return: None
        """
        User.add_student(self, other)
        self.edges.append(Edge(self.node, other.node, weight=1, stroke=VisualUser.EDGE_COLOR, strokewidth=2))

    def remove_coach(self, other):
        """
        Removes the coach from self.coaches and removes the edge for the graph connection

        :param other: Coach to remove
        :type other: VisualUser
        :return: None
        """
        User.remove_coach(self, other)
        for edge in other.edges:
            if edge.node1 == other.node and edge.node2 == self.node:
                other.edges.remove(edge)

    def remove_student(self, other):
        """
        Removes the student from self.students and removes the edge for the graph connection

        :param other: Student to remove
        :type other: VisualUser
        :return: None
        """
        User.remove_student(self, other)
        for edge in other.edges:
            if edge.node1 == self.node and edge.node2 == other.node:
                other.edges.remove(edge)


class VisualNetwork(UserNetwork):
    """
    A visual network that can be used to show how the algorithms in UserNetwork actually look
    when used.
    """
    def __init__(self):
        """
        Creates a network of VisualUser objects and a directed graph to hold all the nodes and
        connections for the user nodes.
        """
        UserNetwork.__init__(self)
        self.directed_graph = DirectedGraph(False, distance=20)
        self.directed_graph.force = 1
        self.canvas = None
        self.ui = None

    def on_mouse_click(self, mouse):
        """
        When a node on the graph is clicked this function is called. This function gets information from the
        UserInterface to see what action it needs to perform on the given node.

        If there is no user interface then the default behavior is to do a limited infection trying to infect
        2 users.

        :return: None
        """
        node = self.directed_graph.node_at(mouse.x - self.canvas.trans_x, mouse.y-self.canvas.trans_y)
        if node is None:
            return

        print node.text.text
        user = None
        for u in self.users:
            if u.id == node.id:
                user = u

        if self.ui is not None:
            if self.ui.infection_type == "limited":
                self.limited_infection(user, self.ui.limited_infection_num, self.ui.node_color)
            else:
                self.total_infection(user, self.ui.node_color)
        else:
            self.limited_infection(user, 2, green)

        self.update_user_nodes()

    def add_user(self, user):
        """
        Adds the user to the user network and then adds a node to the user graph.

        :param user: user to be added
        :type user: VisualUser
        :return: None
        """
        UserNetwork.add_user(self, user)
        self.directed_graph.add_node(user.node)
        for edge in user.edges:
            self.directed_graph.add_edge(edge.node1, edge.node2, weight=edge.weight,
                                         stroke=edge.stroke, strokewidth=edge.strokewidth)

    def remove_user(self, user):
        """
        Removes a user from the network and removes the edges for the user's node from the graph.

        :param user: User to remove
        :type user: VisualUser
        :return: None
        """
        UserNetwork.remove_user(self, user)
        self.directed_graph.remove(user.node)
        for edge in user.edges:
            edge_to_remove = self.directed_graph.edge(edge.node1.id, edge.node2.id)
            self.directed_graph.remove(edge_to_remove)

    def update_user_nodes(self):
        for user in self.users:
            user.node.fill = user.version