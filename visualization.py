from nodebox.graphics import *
from nodebox.gui import *
from nodebox.graphics.physics import Node, Edge, Graph
from user import User
from user_network import UserNetwork

__author__ = 'Phillip Lemons'


def rand_col():
    r = choice(range(256))
    gr = choice(range(256))
    b = choice(range(256))
    return Color(r, gr, b, 255, base=255, colorspace=RGB)


class DirectedGraph(Graph):
    def __init__(self, weighted, *args, **kwargs):
        Graph.__init__(self, *args, **kwargs)
        self.weighted = weighted

    def draw(self, *args, **kwargs):
        Graph.draw(self, weighted=self.weighted, directed=True)


class GraphLayer(Layer):
    def __init__(self, graph, *args, **kwargs):
        Layer.__init__(self, *args, **kwargs)
        # Event methods will be called explicitly by parent layer
        self.enabled = False
        self.graph = graph

    def update(self):
        self.graph.update()

    def draw(self):
        self.graph.draw()


class DraggableCanvas(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        # self.g = Graph(distance=15)
        self.trans_x = 0
        self.trans_y = 0

        self.pressed = False

        self.background = rand_col()

    def on_mouse_scroll(self, mouse):
        # TODO scrolling made the finding a node at a point difficult
        pass
        # if mouse.scroll.y < 0:
        #     # Through testing, mouse.scroll never seemed to get bigger than 10
        #     for layer in self.layers:
        #         layer.scale(1-abs(mouse.scroll.y)/10.0)
        # elif mouse.scroll.y > 0:
        #     for layer in self.layers:
        #         layer.scale(1+mouse.scroll.y/10.0)

    def on_mouse_drag(self, mouse):
        layer_at_mouse = self.layer_at(mouse.x, mouse.y)
        # Make sure we are dragging the graph or the canvas
        if not isinstance(layer_at_mouse, GraphLayer) and layer_at_mouse is not None:
            return

        self.trans_x += mouse.dx
        self.trans_y += mouse.dy
        for layer in self.layers:
            if isinstance(layer, Panel):
                continue
            layer.translate(mouse.dx, mouse.dy)

    def draw(self):
        Canvas.draw(self)
        background(0, 50, 156, 255, base=255, colorspace=RGB)


class UserInterface:
    # Class variable because button action cannot be an instance method
    infection_type = "total"

    def __init__(self):
        self.panel = Panel("Options", width=200, height=200, fixed=True)
        self.num_field = Field(value="1", hint="target num")
        self.panel.append(
            Rows(controls=[
                ("infect", self.num_field),
                ("color", Row([("R", Knob(id="knob_r")),
                               ("G", Knob(id="knob_g")),
                               ("B", Knob(id="knob_b"))])),
                # NOTE: action cannot be an instance method
                Button("Total Infection", action=self.toggle_infection)
            ])
        )
        self.panel.pack()

    @staticmethod
    def toggle_infection(button):
        # Button should show what action you are on
        if UserInterface.infection_type == "limited":
            UserInterface.infection_type = "total"
            button.caption = "Total Infection"
        else:
            UserInterface.infection_type = "limited"
            button.caption = "Limited Infection"

    @property
    def limited_infection_num(self):
        #TODO add error checking for bad values
        return int(self.num_field.value)

    @property
    def node_color(self):
        return Color(self.panel.knob_r.relative,
                     self.panel.knob_g.relative,
                     self.panel.knob_b.relative,
                     0.8)


class VisualUser(User):
    def __init__(self, name, version, *args, **kwargs):
        User.__init__(self, name, version, *args, **kwargs)
        # TODO create id other than using name
        # TODO make text object to use with the node (text should be name)
        if not isinstance(version, Color):
            print "NOT A COLOR INSTANCE"
        self.id = self.name
        self.node = Node(self.id, fill=version, strokewidth=1, radius=15)
        self.edges = list()

    def add_coach(self, other):
        User.add_coach(self, other)
        other.edges.append(Edge(other.node, self.node))
        #other.node.edges.append(Edge(self.node, other.node, weight=1, stroke=Color(0)))

    def add_student(self, other):
        User.add_student(self, other)
        self.edges.append(Edge(self.node, other.node, weight=1, stroke=Color(0)))

    def remove_coach(self, other):
        User.remove_coach(self, other)
        for edge in other.edges:
            if edge.node1 == other.node and edge.node2 == self.node:
                other.edges.remove(edge)

    def remove_student(self, other):
        User.remove_student(self, other)
        for edge in other.edges:
            if edge.node1 == self.node and edge.node2 == other.node:
                other.edges.remove(edge)


class VisualNetwork(UserNetwork):
    def __init__(self, *args, **kwargs):
        UserNetwork.__init__(self, *args, **kwargs)
        self.directed_graph = DirectedGraph(False, distance=20)
        self.directed_graph.force = 1
        self.canvas = None
        self.ui = None

    def on_mouse_click(self, mouse):
        node = self.directed_graph.node_at(mouse.x - self.canvas.trans_x, mouse.y-self.canvas.trans_y)
        if node is None:
            return

        print node.id
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

        # self.total_infection(user, green)

        self.update_user_nodes()

    def add_user(self, user):
        UserNetwork.add_user(self, user)
        self.directed_graph.add_node(user.node)
        for edge in user.edges:
            self.directed_graph.add_edge(edge.node1, edge.node2, weight=edge.weight, stroke=edge.stroke, strokewidth=edge.strokewidth)

    #TODO remove user function

    def update_user_nodes(self):
        for user in self.users:
            user.node.fill = user.version


def test_case_1():
    A = VisualUser("A", red)
    B = VisualUser("B", red)
    C = VisualUser("C", red)
    D = VisualUser("D", red)
    E = VisualUser("E", red)
    F = VisualUser("F", red)
    G = VisualUser("G", red)
    H = VisualUser("H", red)
    I = VisualUser("I", red)
    J = VisualUser("J", red)

    A.add_student(B)
    A.add_student(C)
    A.add_student(D)
    B.add_student(E)
    B.add_student(F)
    C.add_student(F)
    D.add_student(G)
    H.add_student(J)
    I.add_student(J)

    net = VisualNetwork()
    net.add_user(A)
    net.add_user(B)
    net.add_user(C)
    net.add_user(D)
    net.add_user(E)
    net.add_user(F)
    net.add_user(G)
    net.add_user(H)
    net.add_user(I)
    net.add_user(J)

    return net


def test_case_2():
    A = VisualUser("A", red)
    B = VisualUser("B", red)
    C = VisualUser("C", red)
    D = VisualUser("D", red)
    E = VisualUser("E", red)
    F = VisualUser("F", red)
    G = VisualUser("G", red)
    H = VisualUser("H", red)
    I = VisualUser("I", red)
    J = VisualUser("J", red)

    A.add_student(B)
    A.add_student(C)
    A.add_student(D)
    B.add_student(E)
    B.add_student(F)
    C.add_student(F)
    D.add_student(G)
    H.add_student(J)
    I.add_student(J)
    #NEW
    F.add_student(C)
    E.add_student(A)

    net = VisualNetwork()
    net.add_user(A)
    net.add_user(B)
    net.add_user(C)
    net.add_user(D)
    net.add_user(E)
    net.add_user(F)
    net.add_user(G)
    net.add_user(H)
    net.add_user(I)
    net.add_user(J)

    return net

if __name__ == "__main__":
    red = Color(255, 0, 0, 240, base=255, colorspace=RGB)
    green = Color(0, 255, 0, 240, base=255, colorspace=RGB)
    blue = Color(0, 0, 255, 240, base=255, colorspace=RGB)

    #network = test_case_1()
    network = test_case_2()

    lay = GraphLayer(network.directed_graph, 0, 0, 1000, 1000)
    canvas = DraggableCanvas(resizable=True)
    canvas.append(lay)

    ui = UserInterface()
    canvas.append(ui.panel)
    network.ui = ui

    canvas.on_mouse_press = network.on_mouse_click
    lay.enabled = True
    network.canvas = canvas
    canvas.run()