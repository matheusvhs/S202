from flask import Flask, request, jsonify
from bson import ObjectId
from db import pedidos_collection
from redis_cache import cache

app = Flask(__name__)

@app.route("/pedido", methods=["POST"])
def criar_pedido():
    data = request.json
    cliente = data["cliente"]
    pedido = {
        "cliente": {
            "nome": cliente["nome"],
            "endereco": cliente["endereco"],
            "telefone": cliente["telefone"]
        },
        "itens": data["itens"],
        "status": "recebido"
    }
    result = pedidos_collection.insert_one(pedido)
    return jsonify({"message": "Pedido criado", "id": str(result.inserted_id)})

@app.route("/pedidos", methods=["GET"])
def listar_pedidos():
    pedidos = list(pedidos_collection.find())
    for p in pedidos:
        p["_id"] = str(p["_id"])
    return jsonify(pedidos)

@app.route("/pedido/<id>", methods=["PUT"])
def atualizar_status(id):
    status = request.json["status"]
    status_permitidos = ['aceito', 'cancelado', 'preparando', 'saiu para entrega', 'entregue']
    if status not in status_permitidos:
        return jsonify({'erro': 'Status inválido. Opções válidas: ' + ', '.join(status_permitidos)}), 400
    pedidos_collection.update_one({"_id": ObjectId(id)}, {"$set": {"status": status}})
    cache.set(id, status)
    return jsonify({"message": "Status atualizado"})

@app.route("/cliente/<valor>", methods=["GET"])
def pedidos_cliente(valor):
    pedidos = list(pedidos_collection.find({
        "$or": [
            {"cliente.nome": valor},
            {"cliente.telefone": valor}
        ]
    }))
    for p in pedidos:
        p["_id"] = str(p["_id"])
    return jsonify(pedidos)

@app.route("/pedido/<id>", methods=["DELETE"])
def deletar_pedido(id):
    pedidos_collection.delete_one({"_id": ObjectId(id)})
    cache.delete(id)
    return jsonify({"message": "Pedido deletado"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
