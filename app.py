from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Clave para las sesiones

# Inicializamos la sesión con algunos productos de ejemplo
@app.before_request
def init_session():
    if 'products' not in session:
        session['products'] = [
            {'id': 1, 'descripcion': 'Fanta', 'cantidad': 200, 'precio': 10.0, 'categoria': 'Bebidas'},
            {'id': 2, 'descripcion': 'Sprite', 'cantidad': 200, 'precio': 10.0, 'categoria': 'Bebidas'}
        ]

# Ruta principal para mostrar la lista de productos
@app.route('/')
def index():
    return render_template('index.html', products=session['products'])

# Ruta para agregar un nuevo producto
@app.route('/add', methods=['POST'])
def add_product():
    new_product = {
        'id': len(session['products']) + 1,
        'descripcion': request.form['descripcion'],
        'cantidad': int(request.form['cantidad']),
        'precio': float(request.form['precio']),
        'categoria': request.form['categoria']
    }
    session['products'].append(new_product)
    session.modified = True
    return redirect(url_for('index'))

# Ruta para mostrar el formulario de agregar producto
@app.route('/new_product')
def new_product():
    return render_template('new_product.html')

# Ruta para editar un producto
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = next((p for p in session['products'] if p['id'] == id), None)
    if request.method == 'POST':
        product['descripcion'] = request.form['descripcion']
        product['cantidad'] = int(request.form['cantidad'])
        product['precio'] = float(request.form['precio'])
        product['categoria'] = request.form['categoria']
        session.modified = True
        return redirect(url_for('index'))
    return render_template('edit.html', product=product)

# Ruta para eliminar un producto
@app.route('/delete/<int:id>')
def delete_product(id):
    session['products'] = [p for p in session['products'] if p['id'] != id]
    session.modified = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

