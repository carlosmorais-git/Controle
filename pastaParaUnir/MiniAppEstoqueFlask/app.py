from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necessário para usar flash messages

# Configuração do banco de dados
DATABASE = 'inventory.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Rota para exibir o estoque
@app.route('/')
def index():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM inventory').fetchall()
    conn.close()
    return render_template('inventory.html', items=items)

# Rota para adicionar um novo item
@app.route('/add', methods=('GET', 'POST'))
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']

        if not name or not quantity:
            flash('Nome e quantidade são obrigatórios!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO inventory (name, quantity) VALUES (?, ?)', (name, quantity))
            conn.commit()
            conn.close()
            flash('Item adicionado com sucesso!')
            return redirect(url_for('index'))

    return render_template('add_item.html')

# Rota para atualizar a quantidade de um item
@app.route('/update/<int:item_id>', methods=('GET', 'POST'))
def update_item(item_id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM inventory WHERE id = ?', (item_id,)).fetchone()

    if request.method == 'POST':
        quantity = request.form['quantity']

        if not quantity:
            flash('A quantidade é obrigatória!')
        else:
            conn.execute('UPDATE inventory SET quantity = ? WHERE id = ?', (quantity, item_id))
            conn.commit()
            conn.close()
            flash('Item atualizado com sucesso!')
            return redirect(url_for('index'))

    conn.close()
    return render_template('update_item.html', item=item)

# Inicializa o banco de dados com uma tabela
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
