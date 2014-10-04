__author__ = 'Phillip Lemons'

from nodebox.graphics import *
from nodebox.graphics.physics import Node, Edge, Graph, GraphSpringLayout


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

        # # Make sure all nodes stay within this layer
        # for node in self.graph.nodes:
        #     if node.x > self.x + self.width:
        #         node.x = self.x + self.width
        #     elif node.x < self.x:
        #         node.x = self.x
        #
        #     if node.y > self.y + self.height:
        #         node.y = self.y + self.height
        #     elif node.y < self.y:
        #         node.y = self.y

    def draw(self):
        #rect(0, 0, self.width, self.height, fill=Color(1))
        self.graph.draw()


class DraggableLayer(Layer):
    def __init__(self, *args, **kwargs):
        Layer.__init__(self, *args, **kwargs)

    def update(self):
        pass

    def on_mouse_scroll(self, mouse):
        print "MOUSE SCROLL"
        print mouse.scroll
        print mouse.scroll.y/10
        if mouse.scroll.y < 0:
            self.scale(1-abs(mouse.scroll.y)/10.0)
        elif mouse.scroll.y > 0:
            self.scale(1+mouse.scroll.y/10.0)

    def on_mouse_drag(self, mouse):
        self.translate(mouse.dx, mouse.dy)


class DraggableCanvas(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        # self.g = Graph(distance=15)
        self.trans_x = 0
        self.trans_y = 0

        self.pressed = False

        self.background = rand_col()

    @property
    def nodes(self):
        return self.g.nodes

    def add_node(self, *args, **kwargs):
        self.g.add_node(*args, **kwargs)

    def add_edge(self, *args, **kwargs):
        self.g.add_edge(*args, **kwargs)

    def on_mouse_scroll(self, mouse):
        if mouse.scroll.y < 0:
            # Through testing, mouse.scroll never seemed to get bigger than 10
            scale(1-abs(mouse.scroll.y)/10.0)
        elif mouse.scroll.y > 0:
            scale(1+mouse.scroll.y/10.0)

    def on_mouse_drag(self, mouse):
        translate(mouse.dx, mouse.dy)


#g = DraggableGraph(resizable=True)
canvas = DraggableCanvas(resizable=True)
g = DirectedGraph(True)
lay = GraphLayer(g, 0, 0, 1000, 1000)
for i in range(50):
    g.add_node(id=i, fill=rand_col(), strokewidth=1, radius=15)
for i in range(50):
    node1 = choice(g.nodes)
    node2 = choice(g.nodes)
    g.add_edge(node1.id, node2.id, weight=1, stroke=Color(0), strokewidth=1)

canvas.append(lay)
canvas.run()