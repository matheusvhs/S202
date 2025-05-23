## [S202] EAV4

Um fabricante de automóveis contratou você para desenvolver um sistema de banco de dados distribuído usando o Cassandra para as linhas de montagem de toda a corporação, onde cada máquina pudesse acessar a base de dados e buscar as peças de maneira correta para ser montada nos respectivos modelos de veículos. Para isso, você deverá criar a tabela estoque para registrar o id, o nome, o modelo do carro, a estante, o nível e a quantidade de cada peça no estoque.

### Configuração

Coloque todos os arquivos em uma mesma pasta.

Crie um ambiente virtual (python 3.11) se achar necessário e execute o seguinte comando para instalar as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

Para executar os testes use o comando:

```bash
pytest s202_eav4_base.py
```

**Questão 1**

(5 pontos) Crie a tabela para armazenar as pecas com as informações de acordo com o enunciado.

**Questão 2**

(5 pontos) Desenvola a função add_part para inserir as informações das pecas no Cassandra.

**Questão 3**

(5 pontos) Desenvolva a função get_shelf_parts para buscar o nome, o carro e a quantidade das partes de uma determinada estante.

**Questão 4 (extra)**

(5 pontos) Desenvolva a função get_car_parts para buscar o nome, a estante, o nivel e a quantidade das partes de um determinado carro.

**Questão 5 (extra)**

(5 pontos) Desenvolva a função get_shelves_stats para buscar a quantidade de peças mínima, máxima e média (arrendaonda para baixo) em cada estante.


def create_table(self):
        #---------------------------------------------------------------------Questão 1
        query = """
        CREATE TABLE IF NOT EXISTS car_parts (
            id INT,
            name TEXT,
            car_model TEXT,
            shelf INT,
            level INT,
            amount INT,
            PRIMARY KEY ((shelf), id)
        )
        """
        self.cassandra_session.execute(query)
        
        # Criando índice secundário para busca por car_model
        index_query = """
        CREATE INDEX IF NOT EXISTS car_model_idx ON car_parts (car_model)
        """
        self.cassandra_session.execute(index_query)
        

    def add_part(self, part : CarPart):
        query = """
        INSERT INTO car_parts (id, name, car_model, shelf, level, amount)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
        self.cassandra_session.execute(query, (part.id, part.name, part.car_model, part.shelf, part.level, part.amount))
        

    def get_shelf_parts(self, shelf):
        #---------------------------------------------------------------------Questão 3
        query = """
            SELECT name, car_model, amount FROM car_parts
            WHERE shelf = %s
        """
        rows = self.cassandra_session.execute(query, (shelf,))
        return [row for row in rows]