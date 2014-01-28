from random import randint
from collections import namedtuple

CSS = """
<style type="text/css"><![CDATA[
.edge {
    stroke-width: 2px; 
    stroke: black;
}

.node {
    fill: white;
    stroke-width: 2px; 
    stroke: black;
}
]]></style>
"""

Layout = namedtuple('Layout', 'width height locations')

class SVG(object):
    """ etc etc """
    def __init__(self, width, height, directed=False):
        self.width = width
        self.height = height
        self.edges = []
        self.vertices = []
    
    def add_vertex(self, (x,y)):
        vertex = '<circle cx="{cx}" cy="{cy}" r="{r}" class="node"/>'
        vertex = vertex.format(cx=x, cy=y, r=5)
        self.vertices.append(vertex)
    
    def add_edge(self, (x1,y1), (x2,y2)):
        edge = '<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="edge"/>'
        edge = edge.format(x1=x1, y1=y1, x2=x2, y2=y2)
        self.edges.append(edge)
    
    def write(self, buffer_or_filename):
        if hasattr(buffer_or_filename, 'write'):
            buffer_or_filename.write(str(self))
        else:
            with open(buffer_or_filename, 'w') as f:
                f.write(str(self))

    def __repr__(self):
        return "SVG(width=%d, height=%d)" % (self.width, self.height)
    
    def __str__(self):
        # We need to draw the edges before the vertices so 
        # that the circles are on top
        start = "<svg width='{width}px' height='{height}px'>".format(width=self.width, height=self.height)
        edges = ''.join(self.edges)
        vertices = ''.join(self.vertices)
        end = "</svg>"
        return start + CSS + edges + vertices + end
    
    def display(self):
        return display.SVG(str(self))

def draw(graph, filename, width=None, height=None, directed=False):
    layout = _create_layout(graph, width, height)
    _draw_svg(layout, graph, filename, directed)

def _create_random_layout(vertices, width, height):
    locations = {
        vertex: (randint(0, width), randint(0, height)) 
        for vertex in vertices
    }
    return Layout(width, height, locations)

def _draw_svg(layout, graph, filename, directed):
    svg = SVG(layout.width, layout.height, directed)
    locations = layout.locations
    for vertex in graph["vertices"]:
        svg.add_vertex(locations[vertex])
    for v_from, v_to in graph["edges"]:
        svg.add_edge(locations[v_from], locations[v_to])
    svg.write(filename)

def _create_layout(graph, width=None, height=None):
    vertices = graph["vertices"]
    edges = graph["edges"]
    if width is None:
        width = 400
    if height is None:
        height = 400
    return _create_random_layout(vertices, width, height)
