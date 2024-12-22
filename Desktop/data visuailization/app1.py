import os
from flask import Flask, request, jsonify, send_file, render_template
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')  # Render the HTML page

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Get the file and graph type from the form
        file = request.files['file']
        graph_type = request.form['graphType']

        if not file:
            return jsonify({'error': 'No file provided'}), 400

        # Log file details
        print(f"File received: {file.filename}")
        print(f"Graph Type: {graph_type}")

        # Save the file
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        print(f"File saved at: {filepath}")

        # Load the data from the file
        try:
            # Read the file as CSV or Excel
            if file.filename.endswith('.csv'):
                df = pd.read_csv(filepath)
            elif file.filename.endswith('.xlsx'):
                df = pd.read_excel(filepath)
            else:
                return jsonify({'error': 'Unsupported file format'}), 400

            # Log the data loaded from the file
            print(f"Data loaded successfully. Columns: {df.columns}")
        except Exception as e:
            return jsonify({'error': f"Error loading file: {str(e)}"}), 400

        # Generate the graph
        graph = generate_graph(df, graph_type)

        # Save the graph in memory as a PNG
        buffer = BytesIO()
        graph.savefig(buffer, format='png')
        buffer.seek(0)

        return send_file(buffer, mimetype='image/png')

    except Exception as e:
        # Log the error
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

def generate_graph(df, graph_type):
    try:
        # Set up the plot size
        plt.figure(figsize=(10, 6))

        if graph_type == 'bar':
            df.plot(kind='bar')
        elif graph_type == 'line':
            df.plot(kind='line')
        elif graph_type == 'histogram':
            df.hist()
        else:
            raise ValueError("Unsupported graph type")

        plt.tight_layout()
        return plt

    except Exception as e:
        print(f"Error generating graph: {str(e)}")
        raise

if __name__ == '__main__':
    app.run(debug=True)
