# from flask import Flask, render_template, request, send_file, jsonify
# import os
# import time
# import heapq
# from io import BytesIO
# from graphviz import Digraph

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'uploads'
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size 16MB

# # Node class for Huffman Tree
# class Node:
#     def __init__(self, char, freq):
#         self.char = char
#         self.freq = freq
#         self.left = None
#         self.right = None

#     def __lt__(self, other):
#         return self.freq < other.freq

# # Build Huffman Tree
# def build_huffman_tree(freq_table):
#     heap = [Node(char, freq) for char, freq in freq_table.items()]
#     heapq.heapify(heap)

#     while len(heap) > 1:
#         left = heapq.heappop(heap)
#         right = heapq.heappop(heap)
#         merged = Node(None, left.freq + right.freq)
#         merged.left = left
#         merged.right = right
#         heapq.heappush(heap, merged)

#     return heap[0]

# # Generate Huffman Codes
# def generate_codes(node, current_code, codes):
#     if node is None:
#         return
#     if node.char is not None:
#         codes[node.char] = current_code
#     generate_codes(node.left, current_code + "0", codes)
#     generate_codes(node.right, current_code + "1", codes)

# # Huffman Encoding
# def huffman_encode(text, codes):
#     return ''.join(codes[char] for char in text)

# # Visualize Huffman Tree
# def visualize_huffman_tree(root):
#     dot = Digraph(comment='Huffman Tree')

#     def add_nodes_edges(node, parent=None):
#         if node is not None:
#             dot.node(str(id(node)), label=str(node.char) if node.char else str(node.freq))
#             if parent:
#                 dot.edge(str(id(parent)), str(id(node)))
#             add_nodes_edges(node.left, node)
#             add_nodes_edges(node.right, node)

#     add_nodes_edges(root)
#     return dot

# # Compress Route
# @app.route('/compress', methods=['POST'])
# def compress():
#     file = request.files['file']
#     if not file:
#         return "No file uploaded", 400

#     filename = file.filename
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     file.save(file_path)

#     with open(file_path, 'r') as f:
#         text = f.read()

#     start_time = time.time()

#     freq_table = {char: text.count(char) for char in set(text)}
#     root = build_huffman_tree(freq_table)
#     codes = {}
#     generate_codes(root, "", codes)

#     compressed_text = huffman_encode(text, codes)
#     compressed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename + '.compressed')

#     with open(compressed_file_path, 'wb') as f:
#         f.write(compressed_text.encode())

#     end_time = time.time()

#     original_size = os.path.getsize(file_path)
#     compressed_size = os.path.getsize(compressed_file_path)
#     compression_ratio = compressed_size / original_size
#     space_savings = 100 - (compression_ratio * 100)

#     # Generate and save Huffman tree visualization
#     huffman_tree = visualize_huffman_tree(root)
#     tree_path = os.path.join(app.config['UPLOAD_FOLDER'], filename + '_tree')
#     huffman_tree.render(tree_path, format='png', cleanup=True)

#     metrics = {
#         "original_size": original_size,
#         "compressed_size": compressed_size,
#         "compression_ratio": compression_ratio,
#         "space_savings": space_savings,
#         "encoding_time": end_time - start_time,
#         "tree_visualization": tree_path + ".png"
#     }

#     return render_template('result.html', metrics=metrics, download_link=compressed_file_path)

# # Download Route
# @app.route('/download/<path:filename>')
# def download(filename):
#     return send_file(filename, as_attachment=True)

# # Home Route
# @app.route('/')
# def home():
#     return render_template('index.html')

# if __name__ == "__main__":
#     if not os.path.exists(app.config['UPLOAD_FOLDER']):
#         os.makedirs(app.config['UPLOAD_FOLDER'])
#     app.run(debug=True)


from flask import Flask, render_template, request, send_file
import os
import time
import heapq
from io import BytesIO
from graphviz import Digraph

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size 16MB

# Node class for Huffman Tree
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# Build Huffman Tree
def build_huffman_tree(freq_table):
    heap = [Node(char, freq) for char, freq in freq_table.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]

# Generate Huffman Codes
def generate_codes(node, current_code, codes):
    if node is None:
        return
    if node.char is not None:
        codes[node.char] = current_code
    generate_codes(node.left, current_code + "0", codes)
    generate_codes(node.right, current_code + "1", codes)

# Huffman Encoding
def huffman_encode(text, codes):
    return ''.join(codes[char] for char in text)

# Huffman Decoding
def huffman_decode(encoded_text, root):
    decoded_text = ""
    current_node = root
    for bit in encoded_text:
        current_node = current_node.left if bit == '0' else current_node.right
        if current_node.char:
            decoded_text += current_node.char
            current_node = root  # Reset to the root after decoding a character
    return decoded_text

# Visualize Huffman Tree
def visualize_huffman_tree(root):
    dot = Digraph(comment='Huffman Tree')

    def add_nodes_edges(node, parent=None):
        if node is not None:
            dot.node(str(id(node)), label=str(node.char) if node.char else str(node.freq))
            if parent:
                dot.edge(str(id(parent)), str(id(node)))
            add_nodes_edges(node.left, node)
            add_nodes_edges(node.right, node)

    add_nodes_edges(root)
    return dot

# Compress Route
@app.route('/compress', methods=['POST'])
def compress():
    file = request.files['file']
    if not file:
        return "No file uploaded", 400

    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    with open(file_path, 'r') as f:
        text = f.read()

    start_time = time.time()

    # Frequency table and Huffman tree
    freq_table = {char: text.count(char) for char in set(text)}
    root = build_huffman_tree(freq_table)
    codes = {}
    generate_codes(root, "", codes)

    # Encode the text
    compressed_text = huffman_encode(text, codes)
    compressed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename + '.compressed')

    # Save the compressed file
    with open(compressed_file_path, 'wb') as f:
        f.write(compressed_text.encode())

    # Save the frequency table to a file
    freq_table_path = os.path.join(app.config['UPLOAD_FOLDER'], filename + '.freq')
    with open(freq_table_path, 'w') as f:
        f.write(str(freq_table))

    end_time = time.time()

    # Metrics
    original_size = os.path.getsize(file_path)
    compressed_size = os.path.getsize(compressed_file_path)
    compression_ratio = compressed_size / original_size
    space_savings = 100 - (compression_ratio * 100)

    # Visualize Huffman tree
    huffman_tree = visualize_huffman_tree(root)
    tree_path = os.path.join(app.config['UPLOAD_FOLDER'], filename + '_tree')
    huffman_tree.render(tree_path, format='png', cleanup=True)

    metrics = {
        "original_size": original_size,
        "compressed_size": compressed_size,
        "compression_ratio": compression_ratio,
        "space_savings": space_savings,
        "encoding_time": end_time - start_time,
        "tree_visualization": tree_path + ".png"
    }

    return render_template('result.html', metrics=metrics, download_link=compressed_file_path)

# # Download Route
@app.route('/download/<path:filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

# Decode Route
@app.route('/decode', methods=['POST'])
def decode():
    compressed_file = request.files['file']
    freq_file = request.files['freq']

    if not compressed_file or not freq_file:
        return "Both compressed file and frequency table file are required", 400

    # Save files
    compressed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], compressed_file.filename)
    compressed_file.save(compressed_file_path)

    freq_file_path = os.path.join(app.config['UPLOAD_FOLDER'], freq_file.filename)
    freq_file.save(freq_file_path)

    # Load compressed text
    with open(compressed_file_path, 'rb') as f:
        compressed_text = f.read().decode()

    # Load frequency table
    with open(freq_file_path, 'r') as f:
        freq_table = eval(f.read())

    # Rebuild Huffman tree
    root = build_huffman_tree(freq_table)

    # Decode text
    decoded_text = huffman_decode(compressed_text, root)

    return render_template('decoded_result.html', decoded_text=decoded_text)


# Home Route
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
