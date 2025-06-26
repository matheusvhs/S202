### **Baixar e Executar um Container Cassandra**

1. **Baixar a imagem do Cassandra:**

   - No **Prompt de Comando** ou no **PowerShell**, execute:
     ```bash
     docker pull cassandra
     ```

2. **Executar o container Cassandra:**

   - Execute o seguinte comando para iniciar o Cassandra em um container:
     ```bash
     docker run -d --name cassandra-container -p 9042:9042 cassandra
     ```
     - **`-d`**: Executa o container em segundo plano.
     - **`--name cassandra-container`**: Dá o nome "cassandra-container" ao container.
     - **`-p 9042:9042`**: Mapeia a porta 9042 do container para a porta 9042 do host (porta padrão para conexões CQL).

3. **Verificar se o Cassandra está rodando:**
   - Execute:
     ```bash
     docker ps
     ```
   - O Cassandra deve aparecer na lista de containers ativos.

---

### **Acessar o Cassandra com um Script Python**

1. **Instalar a biblioteca `cassandra-driver` no Python:**

   - Certifique-se de que você tem o Python instalado (recomenda-se usar o Python 3).
   - No terminal, execute:
     ```bash
     pip install cassandra-driver
     ```

2. **Criar um script Python para se conectar ao Cassandra:**

   - Crie um arquivo chamado `cassandra_test.py` e insira o seguinte código:

     ```python
     from cassandra.cluster import Cluster

     # Configurar conexão
     cluster = Cluster(['localhost'])  # URL do Cassandra
     session = cluster.connect()

     # Criar um Keyspace e usar
     session.execute("""
     CREATE KEYSPACE IF NOT EXISTS test_keyspace
     WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '1' }
     """)
     session.set_keyspace('test_keyspace')

     # Criar uma tabela
     session.execute("""
     CREATE TABLE IF NOT EXISTS users (
         id UUID PRIMARY KEY,
         name text,
         age int
     )
     """)

     # Inserir dados
     import uuid
     user_id = uuid.uuid4()
     session.execute("""
     INSERT INTO users (id, name, age)
     VALUES (%s, %s, %s)
     """, (user_id, 'Alice', 30))

     # Recuperar dados
     rows = session.execute('SELECT id, name, age FROM users')
     for row in rows:
         print(f"ID: {row.id}, Name: {row.name}, Age: {row.age}")

     # Fechar a conexão
     cluster.shutdown()
     ```

3. **Executar o script:**
   - No terminal, execute:
     ```bash
     python cassandra_test.py
     ```
   - Se tudo estiver configurado corretamente, você verá os dados inseridos e recuperados do Cassandra.
