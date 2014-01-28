from random import randint
from collections import namedtuple
import numpy as np

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
    locations = np.array([[randint(0, width), randint(0, height)] for _ in vertices])
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
    layout = _create_random_layout(vertices, width, height)
    for _ in range(2):
        _force_update(layout, graph)
    return layout

def _force_update(layout, graph):
    """
    Constants are taken from chapter 12 of the "Handbook of Graph
    Drawing and Visualization"
    """
    c1, c2, c3, c4 = 2, 1, 1, 0.1
    locations = layout.locations
    adj_matrix = _adjacency_matrix(graph)
    for vertex, _ in enumerate(locations):
        force = _calculate_force(vertex, layout, adj_matrix)
        locations[vertex] = locations[vertex] + force * c4

def _adjacency_matrix(graph, directed=False):
    n_vert = len(graph['vertices'])
    edges = set(graph['edges'])
    matrix = np.zeros((n_vert, n_vert), dtype=int)
    for i in range(n_vert):
        for j in range(n_vert):
            if directed:
                matrix[i, j] = (i,j) in edges
            else:
                matrix[i, j] = (i,j) in edges or (j,i) in edges
    return matrix

def _calculate_force(vertex, layout, adj_matrix):
    c1, c2, c3, c4 = 2, 1, 1, 0.1
    locations = layout.locations
    neighbors = adj_matrix[vertex]
    non_neighbors = 1 - adj_matrix[vertex]

    differences = locations[vertex] - locations
    distances = np.apply_along_axis(np.linalg.norm, 1, differences)
    distances[vertex] = 1e-10

    neighbor_forces = c1 * np.log(distances * neighbors / c2)
    non_neighbor_forces = non_neighbors * (c3 / distances * 2)
    forces = neighbor_forces + non_neighbor_forces
    forces[vertex] = 0

    amount_to_move = np.sum(differences.T / distances * forces, axis=1)
    print differences.T / distances * forces
    return amount_to_move
