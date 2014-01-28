from graph_layout import _create_layout, SVG, draw, _adjacency_matrix, \
                         _calculate_force, Layout
from StringIO import StringIO
import numpy as np

def complete_graph(n):
    vertices = range(n)
    return {
        "vertices": vertices,
        "edges": [(i,j) for i in vertices for j in vertices if i < j]
    }

def test_create_layout_basic():
    G = complete_graph(4)
    layout = _create_layout(G)
    assert layout.width == 400
    assert layout.height == 400
    assert len(layout.locations) == 4

def test_svg():
    svg = SVG(width=100, height=100)
    svg.add_vertex((40, 40))
    svg.add_vertex((40, 60))
    svg.add_edge((40, 60), (40, 40))
    edge = '<line x1="40" y1="60" x2="40" y2="40" class="edge"/>'
    v1 = '<circle cx="40" cy="40"'
    v2 = '<circle cx="40" cy="60"'
    string_repr = str(svg)
    assert edge in string_repr 
    assert v1 in string_repr
    assert v2 in string_repr


def test_draw():
    G = complete_graph(4)
    buf = StringIO()
    draw(G, buf, height = 200)

def test_adj_matrix():
    G = complete_graph(3)
    matrix = _adjacency_matrix(G)
    actual_matrix = [[0,1,1], [1,0,1], [1,1,0]]
    assert (matrix == actual_matrix).all()


def test_calculate_force():
    vertex = 0
    layout = Layout(100, 100, np.array([[0,0], [1,1], [1,0]]))
    adj_matrix = np.array([[0,1,0], [1,0,1], [0,1,0]])
    print _calculate_force(vertex, layout, adj_matrix)
    assert False
