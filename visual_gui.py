from nodebox.graphics import *
from nodebox.gui import *
from prepared_networks import circular_network, large_network, small_network, medium_network

#TODO create random name function

__author__ = 'Phillip Lemons'


def setup():
    canvas = DraggableCanvas(resizable=True)
    network_list = [small_network, medium_network, large_network, circular_network]

    ui = UserInterface()
    canvas.append(ui.panel)

    for network in network_list:
        network.canvas = canvas
        network.ui = ui

    return canvas, network_list


def change_network(button):
    """
    Changes the canvas to the next network in the list.

    :return: None
    """
    for l in canvas.layers:
        if not isinstance(l, Panel):
            canvas.remove(l)

    # Reset translation distance
    canvas.trans_x = 0
    canvas.trans_y = 0

    global network_idx
    network_idx += 1
    new_network = network_list[network_idx % len(network_list)]
    canvas.on_mouse_press = new_network.on_mouse_click

    graph_layer = GraphLayer(new_network.directed_graph)
    graph_layer.enabled = True
    # Insert at beginning so the layer is drawn below the GUI
    canvas.insert(0, graph_layer)


class GraphLayer(Layer):
    """
    Layer that can hold a graph object. This makes it easier to work with
    on the canvas.
    """
    def __init__(self, graph, *args, **kwargs):
        Layer.__init__(self, *args, **kwargs)
        self.graph = graph

    def update(self):
        self.graph.update()

    def draw(self):
        self.graph.draw()


class DraggableCanvas(Canvas):
    """
    A canvas object that implements dragging.
    """
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self.trans_x = 0
        self.trans_y = 0

        self.pressed = False

        self.background = Color(7, 148, 0, 255, base=255, colorspace=RGB)

    def on_mouse_drag(self, mouse):
        """
        If the mouse is dragging the canvas or a graph layer, then translate all the
        layers by however much the mouse is dragged.
        """
        layer_at_mouse = self.layer_at(mouse.x, mouse.y)
        # Make sure we are dragging the graph or the canvas
        if not isinstance(layer_at_mouse, GraphLayer) and layer_at_mouse is not None:
            return

        self.trans_x += mouse.dx
        self.trans_y += mouse.dy
        for layer in self.layers:
            # Don't translate panel objects
            if isinstance(layer, Panel):
                continue
            layer.translate(mouse.dx, mouse.dy)

    def draw(self):
        Canvas.draw(self)
        background(self.background)


class UserInterface:
    # Button action cannot be an instance method so must keep track of state
    # using a class variable.
    infection_type = "total"

    def __init__(self):
        """
        Sets up the user interface panel in the bottom left part of the screen.
        """
        self.panel = Panel("Options", width=200, height=200, fixed=True)
        self.num_field = Field(value="1", hint="target num")
        self.panel.append(
            Rows(controls=[
                ("infect", self.num_field),
                ("color", Row([("R", Knob(id="knob_r")),
                               ("G", Knob(id="knob_g")),
                               ("B", Knob(id="knob_b"))])),
                # NOTE: action cannot be an instance method
                Button("Total Infection", action=self.toggle_infection),
                Button("Next Network", action=change_network)
            ])
        )
        self.panel.pack()

    @staticmethod
    def toggle_infection(button):
        """
        Action called by the button in the bottom part of the panel. The button
        will show whatever action you are currently set to use.

        :param button: instance of the button
        :type button: Button
        :return: None
        """
        if UserInterface.infection_type == "limited":
            UserInterface.infection_type = "total"
            button.caption = "Total Infection"
        else:
            UserInterface.infection_type = "limited"
            button.caption = "Limited Infection"

    @property
    def limited_infection_num(self):
        """
        :return: target number for a limited infection
        """
        try:
            output = int(self.num_field.value)
        except ValueError:
            # TODO make a popup for the user?
            print "That is not an integer!"
            output = None
        return output

    @property
    def node_color(self):
        """
        :return: Color to make nodes when they are infected
        """
        return Color(self.panel.knob_r.relative,
                     self.panel.knob_g.relative,
                     self.panel.knob_b.relative,
                     0.9)


canvas, network_list = setup()
# Starts at -1 so change_method will start at idx 0 when called in __main__
network_idx = -1
if __name__ == "__main__":
    change_network(None)
    canvas.run()