# %%
import meshcat
import meshcat.geometry as g
import meshcat.transformations as tf
import numpy as np
import networkx as nx
from meshcat.servers.zmqserver import start_zmq_server_as_subprocess
import time

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
    
    points = np.vstack([start_position, end_position]).T
    edge_name = f"{start_node}_to_{end_node}"
    viewer["edges"][edge_name].set_object(g.LineSegments(
        g.PointsGeometry(points),
        g.LineBasicMaterial(color=0x0000ff)))

def visualize_graph_in_meshcat(graph, zmq_url, node_radius=0.2):
    viewer = meshcat.Visualizer(zmq_url=zmq_url)
    positions = {node: np.random.rand(3) for node in graph.nodes()}
    
    for node, position in positions.items():
        node_str = str(node)
        viewer[node_str].set_object(g.Sphere(node_radius),
                                    material=g.MeshLambertMaterial(color=np.random.randint(0, 0xFFFFFF)))
        viewer[node_str].set_transform(tf.translation_matrix(position))
    
    for edge in graph.edges:
        visualize_edge_in_meshcat(viewer, edge, positions)

    return viewer, positions

def interpolate_positions(start_positions, end_positions, alpha):
    interpolated_positions = {}
    for node in start_positions:
        start_pos = start_positions[node]
        end_pos = end_positions[node]
        interpolated_pos = (1 - alpha) * start_pos + alpha * end_pos
        interpolated_positions[node] = interpolated_pos
    return interpolated_positions

def update_node_positions_in_meshcat(viewer, graph, start_positions, end_positions, steps, duration):
    for step in range(steps):
        alpha = step / float(steps)
        interpolated_positions = interpolate_positions(start_positions, end_positions, alpha)
        for node, position in interpolated_positions.items():
            node_str = str(node)
            viewer[node_str].set_transform(tf.translation_matrix(position))
        time.sleep(duration/steps)

def update_positions(graph):
    updated_positions = {node: np.random.rand(3) for node in graph.nodes()}
    return updated_positions

# %%
def main():
    zmq_url = initialize_meshcat()
    graph = create_graph()
    viewer, initial_positions = visualize_graph_in_meshcat(graph, zmq_url)

    # Update the graph after a delay to show initial positions
    time.sleep(10)
    updated_positions = update_positions(graph)
    update_node_positions_in_meshcat(viewer, graph, initial_positions, updated_positions, steps=100, duration=5)

if __name__ == "__main__":
    main()

# %%
