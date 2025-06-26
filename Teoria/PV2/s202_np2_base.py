#Aluno: Matheus Vieira
#Matricula: 525
#Curso: GES

from datetime import datetime

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import dict_factory

import redis

from s202_np2_models import Usuario, Produto, Venda

class CassandraDBConnector:
    # client_id="..." 
    # client_secret="..." 
    # cloud_config={ "secure_connect_bundle": "secure-connect.zip" }  #TODO use your credentials to connect to cloud provider
    
    nodes = ['localhost']
    port = 9042   

    key_space = "loja"  # TODO use your key space
    
    session = None

    staticmethod
    def get_session():
        if CassandraDBConnector.session == None:
            # auth_provider = PlainTextAuthProvider(CassandraDBConnector.client_id, CassandraDBConnector.client_secret)
            # cluster = Cluster(cloud=CassandraDBConnector.cloud_config, auth_provider=auth_provider) # TODO use this when using cloud provider
            cluster = Cluster(
                CassandraDBConnector.nodes, 
                port=CassandraDBConnector.port
            ) # TODO comment this when using cloud provider
            CassandraDBConnector.session = cluster.connect()
            CassandraDBConnector.session.row_factory = dict_factory
            CassandraDBConnector.session.execute(""" CREATE KEYSPACE IF NOT EXISTS {} WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': '1' }} """.format(CassandraDBConnector.key_space))  # TODO comment this when using cloud provider
            CassandraDBConnector.session.set_keyspace(CassandraDBConnector.key_space)

            CassandraDBConnector.clean_database() # TODO comment this to keep database

        return CassandraDBConnector.session
    
    staticmethod
    def clean_database():
        cassandra_clean_query = f"""
            SELECT table_name FROM system_schema.tables
            WHERE keyspace_name = '{CassandraDBConnector.key_space}';
        """
        tables = CassandraDBConnector.session.execute(cassandra_clean_query)

        # Apagar todas as tabelas do Cassandra
        for table in tables:
             if "table_name" in table.keys():
                table_name = table["table_name"]
                print(f"Apagando tabela: {table_name}")
                CassandraDBConnector.session.execute(f"DROP TABLE IF EXISTS {table_name}")

    def close():
        CassandraDBConnector.session.shutdown()

class RedisDBConnector:

    redis_host = "localhost" #TODO use your credentials to connect
    redis_port = 6379

    connection = None

    staticmethod
    def get_connection():
        if RedisDBConnector.connection == None:
            #RedisDBConnector.connection = redis.Redis(host=self.redis_host, port=self.redis_port, username=self.redis_username, password=self.redis_password, decode_responses=True)
            RedisDBConnector.connection = redis.Redis(
                host=RedisDBConnector.redis_host, 
                port=RedisDBConnector.redis_port, 
                decode_responses=True
            )
            RedisDBConnector.connection.flushall()
        return RedisDBConnector.connection
    
    def close():
        RedisDBConnector.connection.close()
                                
class UsuarioDAO:   

    def __init__(self):
        self.cassandra_session = CassandraDBConnector.get_session()
        self.redis_connection = RedisDBConnector.get_connection()
    
    def criar_tabela(self):
        
        query = '''
        CREATE TABLE usuarios(
            id INT,
            estado TEXT,
            cidade TEXT,
            endereco TEXT,
            nome TEXT,
            email TEXT,
            interesses LIST<text>,
            PRIMARY KEY((estado, cidade), id));'
        )
        '''
        self.cassandra_session.execute(query)
    

    def adicionar(self, usuario : Usuario):
        query = '''
        INSERT INTO usuarios(id, estado, cidade, endereco, nome, email, interesses)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        self.cassandra_session.execute(query, (usuario.id, usuario.estado, usuario.cidade, usuario.endereco, usuario.nome, usuario.email, usuario.interesses))

    def get_quantidade_usuarios(self):
        query = """
            SELECT id, estado, cidade FROM usuarios
            """
        users = self.cassandra_session.execute(query)
        print(len(users))
        

    def get_usuarios_estado(self, estado : str):
        query = ''' SELECT * FROM usuarios WHERE estado = "Minas Gerais"; '''
        self.cassandra_session.execute(query)
        

    def adicionar_cache(self, usuario : Usuario):
        #---------------------------------------------------------------------Questão 2
        pass
       
    def get_cache(self):
        #---------------------------------------------------------------------Questão 2
        pass

    def get_interesses_cache(self, usuario_id : int):
        #---------------------------------------------------------------------Questão 3
        pass

    def adicionar_carrinho_cache(self, usuario_id : int, carrinho : list):
        #---------------------------------------------------------------------Questão 4
        pass

    def get_carrinho_cache(self, usuario_id : int):
        #---------------------------------------------------------------------Questão 4
        pass

class ProdutoDAO:
    def __init__(self):
        self.cassandra_session = CassandraDBConnector.get_session()

    def criar_tabela(self):
        query = '''
        CREATE TABLE produtos(
            id INT,
            categoria TEXT,
            nome TEXT,
            custo FLOAT,
            preco FLOAT,
            quantidade INT,
            PRIMARY KEY(id);'
        )
        '''
        self.cassandra_session.execute(query)
     


    def adicionar(self, produto : Produto):
        query = '''
        INSERT INTO produtos(id, categoria, nome, custo, preco, quantidade)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''
        self.cassandra_session.session.execute(query, (produto.id, produto.categoria, produto.nome, produto.custo, produto.preco, produto.quantidade))

    def get_custo_total(self):
        #---------------------------------------------------------------------Questão 1 b.
        pass

    def get_produtos_categoria(self, categoria):
        #---------------------------------------------------------------------Questão 3
        pass

class VendaDAO:
    def __init__(self):
        self.cassandra_session = CassandraDBConnector.get_session()

    def criar_tabela(self):
        query = '''
        CREATE TABLE venda(
            id int,
            dia int,
            mes int,
            ano int,
            hora text,
            valor float,
            produto_quantidade list<map<int, int>>,
            usuario_id int
            PRIMARY KEY(id);
        )
        '''
        self.cassandra_session.execute(query)

    def adicionar(self, id: str, data_hora : datetime, usuario_id: int, carrinho : list):
        query = '''
        INSERT INTO vanda(id, dia, mes, ano, hora, valor, produto_quantidade, usuario_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        self.cassandra_session.execute(query, ())


    def get_vendas(self, data_hora : datetime):
        #---------------------------------------------------------------------Questão 5
        pass




usuario_dao = UsuarioDAO()
produto_dao = ProdutoDAO()
        
def test_questao_1_a():

    usuarios = [
        {"id":1, "estado": "Minas Gerais", "cidade": "Santa Rita do Sapucaí", "endereco": "Rua A, 45", "nome":"Serafim Amarantes", "email":"samarantes@g.com", "interesses": ["futebol", "pagode", "engraçado", "cerveja", "estética"]},
        {"id":2, "estado": "São Paulo", "cidade": "São Bento do Sapucaí", "endereco": "Rua B, 67", "nome":"Tamara Borges", "email":"tam_borges@g.com", "interesses": ["estética", "jiujitsu", "luta", "academia", "maquiagem"]},
        {"id":3, "estado": "Minas Gerais", "cidade": "Santa Rita do Sapucaí", "endereco": "Rua C, 84", "nome":"Ubiratã Carvalho", "email":"bira@g.com", "interesses": ["tecnologia", "hardware", "games", "culinária", "servers"]},
        {"id":4, "estado": "Minas Gerais", "cidade": "Pouso Alegre", "endereco": "Rua D, 21", "nome":"Valéria Damasco", "email":"valeria_damasco@g.com", "interesses": ["neurociências", "comportamento", "skinner", "laboratório", "pesquisa"]}
    ]

    output = len(usuarios)


    usuario_dao.criar_tabela()

    for usuario in usuarios:
        usuario_obj = Usuario(
            id=usuario['id'],
            estado=usuario['estado'],
            cidade=usuario['cidade'],
            endereco=usuario['endereco'],
            nome=usuario['nome'],
            email=usuario['email'],
            interesses=usuario['interesses'],
        )
        usuario_dao.adicionar(usuario_obj)

    quantidade_usuarios = usuario_dao.get_quantidade_usuarios()

    assert output == quantidade_usuarios

def teste_questao_1_b():
    produtos = [
        {"id":1, "categoria": "escritório", "nome":"Cadeira HM conforto", "custo": 2000.00, "preco": 3500.00, "quantidade": 120},
        {"id":2, "categoria": "culinária", "nome":"Tábua de corte Hawk", "custo": 360.00, "preco": 559.90, "quantidade": 40},
        {"id":3, "categoria": "tecnologia", "nome":"Notebook X", "custo": 3000.00, "preco": 4160.99, "quantidade": 76},
        {"id":4, "categoria": "games", "nome":"Headset W", "custo": 265.45, "preco": 422.80, "quantidade": 88},
        {"id":5, "categoria": "tecnologia", "nome":"Smartphone X", "custo": 2000.00, "preco": 3500.00, "quantidade": 120},
        {"id":6, "categoria": "games", "nome":"Gamepad Y", "custo": 256.00, "preco": 519.99, "quantidade": 40},
        {"id":7, "categoria": "estética", "nome":"Base Ismusquim", "custo": 50.00, "preco": 120.39, "quantidade": 76},
        {"id":8, "categoria": "cerveja", "nome":"Gutten Bier IPA 600ml", "custo": 65.45, "preco": 122.80, "quantidade": 88}
    ]

    output = 765559.20

    produto_dao.criar_tabela()

    for produto in produtos:
        produto_obj = Produto(
            id=produto['id'],
            categoria=produto['categoria'],
            nome=produto['nome'],
            custo=produto['custo'],
            preco=produto['preco'],
            quantidade=produto['quantidade']
        )
        produto_dao.adicionar(produto_obj)

    custo_total = produto_dao.get_custo_total()
    
    assert output == custo_total

def test_questao_2():

    estado = "Minas Gerais"

    output = [
        {"id":'1', "estado": "Minas Gerais", "cidade": "Santa Rita do Sapucaí", "endereco": "Rua A, 45", "nome":"Serafim Amarantes", "email":"samarantes@g.com", "interesses": ["futebol", "pagode", "engraçado", "cerveja", "estética"]},
        {"id":'3', "estado": "Minas Gerais", "cidade": "Santa Rita do Sapucaí", "endereco": "Rua C, 84", "nome":"Ubiratã Carvalho", "email":"bira@g.com", "interesses": ["tecnologia", "hardware", "games", "culinária", "servers"]},
        {"id":'4', "estado": "Minas Gerais", "cidade": "Pouso Alegre", "endereco": "Rua D, 21", "nome":"Valéria Damasco", "email":"valeria_damasco@g.com", "interesses": ["neurociências", "comportamento", "skinner", "laboratório", "pesquisa"]}
    ]

    usuarios = usuario_dao.get_usuarios_estado(estado)

    for usuario_obj in usuarios:
        usuario_dao.adicionar_cache(usuario_obj)

    usuarios_cache_dict = [usuario_cache.to_dict() for usuario_cache in usuario_dao.get_cache()]

    assert output == sorted(usuarios_cache_dict, key=lambda d: d['id'])

def test_questao_3():

    usuario_id = 3

    output = [
        {"id":2, "nome":"Tábua de corte Hawk", "preco": 559.90},
        {"id":3, "nome":"Notebook X", "preco": 4160.99},
        {"id":4, "nome":"Headset W", "preco": 422.80},
        {"id":5, "nome":"Smartphone X", "preco": 3500.00},
        {"id":6, "nome":"Gamepad Y", "preco": 519.99}
    ]

    interesses = usuario_dao.get_interesses_cache(usuario_id)
    produtos_dict = []
    for interesse in interesses:
        produtos = produto_dao.get_produtos_categoria(interesse)
        for produto in produtos:
            produto_dict = {
                "id": produto.id,
                "nome": produto.nome,
                "preco": produto.preco
            }
            produtos_dict.append(produto_dict)

    assert output == sorted(produtos_dict, key=lambda d: d['id'])

def test_questao_4():

    usuario_id = 3

    carrinho = [
        {"id":'4', "nome":"Headset W", "preco": '422.80', "quantidade": '1'},
        {"id":'6', "categoria": "games", "nome":"Gamepad Y", "preco": '519.99', "quantidade": '2'},
    ]

    usuario_dao.adicionar_carrinho_cache(usuario_id, carrinho)

    carrinho_cache = usuario_dao.get_carrinho_cache(usuario_id)

    assert carrinho == sorted(carrinho_cache, key=lambda d: d["id"])

venda_dao = VendaDAO()

def test_questao_5():

    usuario_id = 3
    data_hora = datetime.now()

    output = [{"usuario_id": 3, 'hora': data_hora.strftime("%H:%M"), 'valor': 1462.78}]

    venda_dao.criar_tabela()

    carrinho_cache = usuario_dao.get_carrinho_cache(usuario_id)

    venda_dao.adicionar(1, data_hora, usuario_id, carrinho_cache)

    vendas = venda_dao.get_vendas(data_hora)

    assert output == sorted(vendas, key=lambda d: d["hora"])



