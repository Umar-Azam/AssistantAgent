# %%

import meshcat
import meshcat.geometry as g
import meshcat.transformations as tf
import numpy as np
import networkx as nx
from meshcat.servers.zmqserver import start_zmq_server_as_subprocess

def initialize_meshcat():
    proc, zmq_url, web_url = start_zmq_server_as_subprocess(server_args=[])
    print(f"MeshCat server running at {web_url}")
    return zmq_url

def create_graph():
    G = nx.erdos_renyi_graph(10, 0.5)  # Create a random graph for demonstration
    return G

def visualize_edge_in_meshcat(viewer, edge, positions):
    start_node, end_node = edge
    start_position, end_position = positions[start_node], positions[end_node]
    
    # Define points for the edge
    points = np.vstack([start_position, end_position]).T
    edge_name = f"{start_node}_to_{end_node}"
    viewer["edges"][edge_name].set_object(g.LineSegments(
        g.PointsGeometry(points),
        g.LineBasicMaterial(color=0x0000ff)))


def visualize_graph_in_meshcat(graph, zmq_url):
    viewer = meshcat.Visualizer(zmq_url=zmq_url)
    
    # Prepare positions for nodes (this can be replaced with a layout algorithm)
    positions = {node: np.random.rand(3) * 10 for node in graph.nodes()}  # Random positions for demonstration
    
    # Visualize nodes
    for node, position in positions.items():
        node_str = str(node)  # Convert node to string
        viewer[node_str].set_object(g.Sphere(0.5), material=g.MeshLambertMaterial(color=np.random.randint(0, 0xFFFFFF)))
        viewer[node_str].set_transform(tf.translation_matrix(position))
    
    # Visualize edges
    for edge in graph.edges:
        visualize_edge_in_meshcat(viewer, edge, positions)


# %%
def main():
    zmq_url = initialize_meshcat()
    graph = create_graph()
    visualize_graph_in_meshcat(graph, zmq_url)

if __name__ == "__main__":
    main()
