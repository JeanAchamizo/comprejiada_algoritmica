from flask import Flask, render_template, request, jsonify
from algoritmoKousaraju import run_kosaraju

app = Flask(__name__, static_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index():
    grafo_original_data = {}  # Aquí almacenaremos los datos del grafo original
    grafo_scc_data = {}  # Aquí almacenaremos los datos del grafo SCC

    if request.method == 'POST':
        csv_filename = request.form['csv_file']
        nodo_lista, sccs = run_kosaraju(csv_filename)

        # Lógica para generar los datos de los gráficos o cualquier otro procesamiento necesario
        # Aquí puedes construir grafo_original_data y grafo_scc_data en el formato requerido

        # Ejemplo de cómo podrías estructurar los datos para enviarlos a index.html
        grafo_original_data['nodes'] = [{'id': nodo} for nodo in nodo_lista]
        grafo_original_data['edges'] = [{'from': nodo, 'to': seguidor} for nodo in nodo_lista for seguidor in nodo_lista[nodo]]
        
        grafo_scc_data['nodes'] = []  # Ajustar según el formato necesario
        grafo_scc_data['edges'] = []  # Ajustar según el formato necesario

        # Devolver los datos en formato JSON
        return jsonify({
            'grafo_original': grafo_original_data,
            'grafo_scc': grafo_scc_data,
            'sccs': sccs
        })

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
