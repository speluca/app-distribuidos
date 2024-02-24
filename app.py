from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para criar a tabela caso não exista
def criar_tabela():
    conn = sqlite3.connect('nomes.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS nomes
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      nome TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Função para inserir um nome na tabela
def inserir_nome(nome):
    conn = sqlite3.connect('nomes.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO nomes (nome) VALUES (?)''', (nome,))
    conn.commit()
    conn.close()

# Função para recuperar todos os nomes da tabela
def listar_nomes():
    conn = sqlite3.connect('nomes.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM nomes''')
    nomes = cursor.fetchall()
    conn.close()
    return nomes

# Rota principal para a página inicial
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        if nome:
            inserir_nome(nome)
            return redirect(url_for('index'))
    nomes = listar_nomes()
    return render_template('./index.html', nomes=nomes)

if __name__ == '__main__':
    criar_tabela()
    app.run(debug=True)
