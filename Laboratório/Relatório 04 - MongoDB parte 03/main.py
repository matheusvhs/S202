from database import Database
from helper.writeAJson import writeAJson
from productAnalyser import ProductAnalyzer

db = Database(database="mercado", collection="compras")


analyzer = ProductAnalyzer(db)
analyzer.totalVendasDia()
analyzer.produtoMaisVendido()
analyzer.clienteMaiorGastoEmUmaCompra()
analyzer.produtosQuantidadeVendidaAcimaDeUmaUnidade()

