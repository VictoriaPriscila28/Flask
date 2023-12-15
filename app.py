
import pymysql
import mysql.connector
from flask import Flask, render_template, redirect, request
from getpass import getpass


app = Flask(__name__)
# Função para conectar ao banco de dados
conexao = pymysql.connect(host="127.0.0.1",
                     user="root",
                     password="password",
                     database="charnelle")

#route

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/autenticar', methods=['POST'])
def login_validar():
    cursor = conexao.cursor()
    query = "SELECT * FROM usuarios WHERE nome = %s and senha = %s"
    nome = request.form['nome']
    senha = request.form['senha']
    valores = (nome, senha)
    cursor.execute(query, valores)
    login = cursor.fetchone()
    if login is not None:
        return redirect('/inventario')

    else:
        return redirect('/login')

    cursor.close()
    conexao.close()

    return request.form


@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastrar.html')


@app.route('/inventario')
def inventario():
    return render_template('inventario.html')
# Função para exibir o menu do usuario
@app.route('/usuarios_menu')
def usuarios_menu():
    return render_template('usuarios_menu.html')

# Função para o usuario fazer o login
@app.route('/login')
def login_usuario():
    return render_template('login.html')


#Função para inserir um item na tabela de itens
@app.route('/inserir_item', methods=['POST'])
def inserir_item():
    conexao = conectar_bd()
    cursor = conexao.cursor()

    nome = input("Digite o nome do item: ")
    descricao = input("Digite a descrição do item: ")
    preco = float(input("Digite o preço do item: "))

    if preco > 200:
        desconto = preco * 0.1  # Aplicar um desconto de 10%
        preco_com_desconto = preco - desconto
        mensagem_desconto = f"Desconto aplicado! Valor com desconto: R$ {preco_com_desconto:.2f}"
    else:
        mensagem_desconto = "Valor do item não atende aos critérios para aplicar desconto."

    # Mostra a mensagem de desconto
    print(mensagem_desconto)

    # Insere os dados no banco de dados
    query = "INSERT INTO itens (nome, descricao, preco) VALUES (%s, %s, %s)"
    valores = (nome, descricao, preco)

    cursor.execute(query, valores)
    conexao.commit()

    print("Item inserido com sucesso!")

    cursor.close()
    conexao.close()

# Função para consultar um item na tabela de itens
@app.route('/consultar_item')
def consultar_item():
    conexao = conectar_bd()
    cursor = conexao.cursor()

    id = int(input("Digite o codigo a ser consultado: "))

    # Consulta o item no banco de dados
    query = "SELECT * FROM itens WHERE id = %s"
    valores = (id,)

    cursor.execute(query, valores)
    item = cursor.fetchone()

    if item is not None:
        print("Id:", item[0])
        print("Nome:", item[1])
        print("Descrição:", item[2])
        print("Preço:", item[3])
    else:
        print("Item não encontrado.")

    cursor.close()
    conexao.close()

# Função para alterar um item na tabela de itens
def alterar_item():
    conexao = conectar_bd()
    cursor = conexao.cursor()

    id_item = int(input("Digite o ID do item a ser alterado: "))

    nome = input("Digite o novo nome do item: ")
    descricao = input("Digite a nova descrição do item: ")
    preco = float(input("Digite o novo preço do item: "))

    # Atualiza os dados no banco de dados
    query = "UPDATE itens SET nome = %s, descricao = %s, preco = %s WHERE id = %s"
    valores = (nome, descricao, preco, id_item)

    cursor.execute(query, valores)
    conexao.commit()

    if cursor.rowcount > 0:
        print("Item alterado com sucesso!")
    else:
        print("Falha ao alterar o item.")

    cursor.close()
    conexao.close()

# Função para remover um item na tabela de itens
def remover_item():
    conexao = conectar_bd()
    cursor = conexao.cursor()

    id_item = int(input("Digite o ID do item a ser removido: "))

    # Remove o item do banco de dados
    query = "DELETE FROM itens WHERE id = %s"
    valores = (id_item,)

    cursor.execute(query, valores)
    conexao.commit()

    if cursor.rowcount > 0:
        print("Item removido com sucesso!")
    else:
        print("Falha ao remover o item.")

    cursor.close()
    conexao.close()

# Função para consultar o inventário
def consultar_inventario():
    conexao = conectar_bd()
    cursor = conexao.cursor()

    query = "SELECT * FROM itens"
    cursor.execute(query)

    # Recuperar os resultados da consulta
    resultados = cursor.fetchall()

    # Exibir os resultados na forma de inventário
    print("Inventário:")
    for item in resultados:
        codigo= item[0]
        nome = item[1]
        descricao = item[2]
        preco = item[3]
        print(f"Id: {codigo}, Nome: {nome}, Descrição: {descricao}, Preço: {preco}")

    cursor.close()
    conexao.close()


# Função para cadastrar um novo usuário no sistema
"""""@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    conexao = conectar_bd()
    cursor = conexao.cursor()

    nome = input("Digite o nome do usuário: ")
    senha = input("Digite a senha: ")
    if len(senha) <5:
        print("Sua senha é curta demais para ser aceita, por favor insira a partir de 5 caracteres")
    else:# Insere os dados do usuário no banco de dados
        query = "INSERT INTO usuarios (nome, senha) VALUES (%s, %s)"
        valores = (nome, senha)

        cursor.execute(query, valores)
        conexao.commit()

        print("Usuário cadastrado com sucesso!")

        cursor.close()
        conexao.close()"""


# Função para alterar a senha de um usuário
@app.route('/alterar_senha', methods=['POST'])
def alterar_senha():
    conexao = conectar_bd()
    cursor = conexao.cursor()

    nome = input("Digite o nome do usuário: ")
    nova_senha = input("Digite a nova senha: ")

    # Atualiza a senha do usuário no banco de dados
    query = "UPDATE usuarios SET senha = %s WHERE nome = %s"
    valores = (nova_senha, nome)

    cursor.execute(query, valores)
    conexao.commit()

    if cursor.rowcount > 0:
        print("Senha alterada com sucesso!")
    else:
        print("Falha ao alterar a senha.")

    cursor.close()
    conexao.close()

def main():
    executar = True
    checkin = True

    while checkin:
        usuarios_menu()
        opcao1=int(input("Escolha uma opção: "))

        if opcao1 == 1:
            cadastrar_usuario()
        elif opcao1 == 2:
            alterar_senha()
        elif opcao1 == 3:
            login = login_usuario()
            logado = login is not None
            if logado:
                checkin = False


        elif opcao1 == 4:
            executar = False

            checkin = False


    while executar:
        exibir_menu()
        opcao2 = int(input("Escolha uma opção: "))

        if opcao2 == 1:
            inserir_item()
        elif opcao2 == 2:
            consultar_item()
        elif opcao2 == 3:
            alterar_item()
        elif opcao2 == 4:
            remover_item()
        elif opcao2 == 5:
            consultar_inventario()
        elif opcao2 == 6:
            executar = False
        else:
            print("Opção inválida. Tente novamente!")
        #input("Aperte enter para voltar ao menu")


    print("Até breve!")

if __name__ == '__main__':
    app.run(debug=True)