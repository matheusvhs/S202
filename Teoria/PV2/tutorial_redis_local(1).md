### **Baixar e Executar um Container Redis**

1. **Baixar a imagem do Redis:**

   - No **Prompt de Comando** ou no **PowerShell**, execute:
     ```bash
     docker pull redis
     ```

2. **Executar o container Redis:**

   - Execute o seguinte comando para iniciar o Redis em um container:
     ```bash
     docker run -d --name redis-container -p 6379:6379 redis
     ```
     - **`-d`**: Executa o container em segundo plano.
     - **`--name redis-container`**: Dá o nome "redis-container" ao container.
     - **`-p 6379:6379`**: Mapeia a porta 6379 do container para a porta 6379 do host.

3. **Verificar se o Redis está rodando:**
   - Execute:
     ```bash
     docker ps
     ```
   - O Redis deve aparecer na lista de containers ativos.

---

### **Acessar o Redis com um Script Python**

1. **Instalar a biblioteca `redis` no Python:**

   - Certifique-se de que você tem o Python instalado (recomenda-se usar o Python 3).
   - No terminal, execute:
     ```bash
     pip install redis
     ```

2. **Criar um script Python para se conectar ao Redis:**

   - Crie um arquivo chamado `redis_test.py` e insira o seguinte código:

     ```python
     import redis

     # Conectar ao Redis
     client = redis.Redis(host='localhost', port=6379, decode_responses=True)

     # Testar conexão
     try:
         client.ping()
         print("Conexão com o Redis bem-sucedida!")
     except redis.ConnectionError:
         print("Falha ao conectar ao Redis.")

     # Inserir e recuperar dados
     client.set('chave', 'valor')
     print("Valor armazenado:", client.get('chave'))
     ```

3. **Executar o script:**
   - No terminal, execute:
     ```bash
     python redis_test.py
     ```
   - Se tudo estiver configurado corretamente, você verá a mensagem de conexão bem-sucedida e o valor armazenado no Redis.
