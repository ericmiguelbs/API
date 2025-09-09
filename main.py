from flask import Flask, request, jsonify
from flasgger import Swagger


app = Flask(__name__)
Swagger(app)

usuarios = []
current_id = 1

@app.route('/users', methods=['POST'])
def criar_usuario():
    """
    Cria um novo usuário.
    ---
    tags:
      - Usuários
    description: Cria um novo usuário com nome e email.
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: user
        description: Objeto JSON com os dados do usuário.
        required: true
        schema:
          type: object
          required:
            - nome
            - email
          properties:
            nome:
              type: string
              example: João Silva
            email:
              type: string
              example: joao@email.com
    responses:
      201:
        description: Usuário criado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            nome:
              type: string
              example: João Silva
            email:
              type: string
              example: joao@email.com
      400:
        description: Requisição inválida, faltando nome ou email
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Nome e email são obrigatórios."
    """
    global current_id
    dados = request.json
    if not dados or 'nome' not in dados or 'email' not in dados:
        return jsonify({"erro": "Dados inválidos"}), 400

    novo_usuario = {
        "id": current_id,
        "nome": dados['nome'],
        "email": dados['email']
    }
    usuarios.append(novo_usuario)
    current_id += 1
    return jsonify(novo_usuario), 201

@app.route('/users', methods=['GET'])
def listar_usuarios():
    """
    Lista todos os usuários.
    ---
    tags:
      - Usuários
    description: Retorna uma lista de todos os usuários cadastrados.
    produces:
      - application/json
    responses:
      200:
        description: Lista de usuários obtida com sucesso.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              nome:
                type: string
              email:
                type: string
    """
    return jsonify(usuarios), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def buscar_usuario(user_id):
    """
    Busca um usuário por ID.
    ---
    tags:
      - Usuários
    description: Retorna um único usuário baseado em seu ID.
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID do usuário a ser buscado.
    responses:
      200:
        description: Usuário encontrado com sucesso.
        schema:
          type: object
          properties:
            id:
              type: integer
            nome:
              type: string
            email:
              type: string
      404:
        description: Usuário não encontrado.
    """
    for usuario in usuarios:
        if usuario['id'] == user_id:
            return jsonify(usuario), 200
    return jsonify({"erro": "Usuário não encontrado"}), 404

@app.route('/users/<int:user_id>', methods=['PUT'])
def atualizar_usuario(user_id):
    """
    Atualiza um usuário existente.
    ---
    tags:
      - Usuários
    description: Atualiza os dados de um usuário (nome e/ou email) por ID.
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID do usuário a ser atualizado.
      - in: body
        name: user
        description: Objeto JSON com os dados do usuário a serem atualizados.
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: Maria
            email:
              type: string
              example: maria@email.com
    responses:
      200:
        description: Usuário atualizado com sucesso.
        schema:
          type: object
          properties:
            id:
              type: integer
            nome:
              type: string
            email:
              type: string
      404:
        description: Usuário não encontrado.
    """
    dados = request.json
    for usuario in usuarios:
        if usuario['id'] == user_id:
            usuario['nome'] = dados.get('nome', usuario['nome'])
            usuario['email'] = dados.get('email', usuario['email'])
            return jsonify(usuario), 200
    return jsonify({"erro": "Usuário não encontrado"}), 404

@app.route('/users/<int:user_id>', methods=['DELETE'])
def deletar_usuario(user_id):
    """
    Deleta um usuário.
    ---
    tags:
      - Usuários
    description: Deleta um usuário por ID.
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID do usuário a ser deletado.
    responses:
      200:
        description: Usuário excluído com sucesso.
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: "Usuário excluído com sucesso"
      404:
        description: Usuário não encontrado.
    """
    for usuario in usuarios:
        if usuario['id'] == user_id:
            usuarios.remove(usuario)
            return jsonify({"mensagem": "Usuário excluído com sucesso"}), 200
    return jsonify({"erro": "Usuário não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)