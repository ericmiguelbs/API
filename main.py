from flask import Flask, request, jsonify

app = Flask(__name__)

usuarios = []

current_id = 1

@app.route('/users', methods=['POST'])
def criar_usuario():
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
    return jsonify(usuarios), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def buscar_usuario(user_id):
    for usuario in usuarios:
        if usuario['id'] == user_id:
            return jsonify(usuario), 200
    return jsonify({"erro": "Usuário não encontrado"}), 404

@app.route('/users/<int:user_id>', methods=['PUT'])
def atualizar_usuario(user_id):
    dados = request.json
    for usuario in usuarios:
        if usuario['id'] == user_id:
            usuario['nome'] = dados.get('nome', usuario['nome'])
            usuario['email'] = dados.get('email', usuario['email'])
            return jsonify(usuario), 200
    return jsonify({"erro": "Usuário não encontrado"}), 404

@app.route('/users/<int:user_id>', methods=['DELETE'])
def deletar_usuario(user_id):
    for usuario in usuarios:
        if usuario['id'] == user_id:
            usuarios.remove(usuario)
            return jsonify({"mensagem": "Usuário excluído com sucesso"}), 200
    return jsonify({"erro": "Usuário não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)