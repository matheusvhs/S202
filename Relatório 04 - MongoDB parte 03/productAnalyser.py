#Relatório 4 - MongoDB parte 3
# Aluno: Matheus Vieira Honorio de Souza - GES - 525

from database import Database
from helper.writeAJson import writeAJson

class ProductAnalyzer:
    def __init__(self, db: Database):
        self.db = db

    def totalVendasDia(self):
        """Return the total sales per day"""
        result = self.db.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {
                "_id": "$data_compra",
                "total_sales": {"$sum": {"$multiply": ["$produtos.quantidade", "$produtos.preco"]}}
            }},
            {"$sort": {"_id": 1}}
        ])
        writeAJson(result, "Vendas por dia")

    def produtoMaisVendido(self):
        """Return the most sold product across all purchases"""
        result = self.db.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {"_id": "$produtos.descricao", "total": {"$sum": "$produtos.quantidade"}}},
            {"$sort": {"total": -1}},
            {"$limit": 1}
        ])
        writeAJson(result, "Produto mais vendido")

    def clienteMaiorGastoEmUmaCompra(self):
        """Find the customer who spent the most in a single purchase"""
        result = self.db.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {
                "_id": {"cliente": "$cliente_id", "compra_id": "$_id"},
                "total_gasto": {"$sum": {"$multiply": ["$produtos.quantidade", "$produtos.preco"]}}
            }},
            {"$sort": {"total_gasto": -1}},
            {"$limit": 1}
        ])
        writeAJson(result, "Cliente que mais gastou em uma compra")

    def produtosQuantidadeVendidaAcimaDeUmaUnidade(self):
        """List all products with quantity sold above 1 unit"""
        result = self.db.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$match": {"produtos.quantidade": {"$gt": 1}}},
            {"$group": {"_id": "$produtos.descricao", "total_vendido": {"$sum": "$produtos.quantidade"}}},
            {"$sort": {"total_vendido": -1}}
        ])
        writeAJson(result, "Produtos com quantidade vendida acima de uma unidade")
    