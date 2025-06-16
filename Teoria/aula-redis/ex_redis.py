import redis
import time
import json

# Conectando ao Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Função para adicionar usuário (com TTL de 60 segundos)
def add_user(user_id, name, email):
    user_data = {'id': user_id, 'name': name, 'email': email}
    r.setex(f'user:{user_id}', 60, json.dumps(user_data))
    print(f"[INFO] Usuário {name} adicionado (expira em 60s)")

# Função para adicionar mensagem (com TTL de 5 segundos)
def add_message(msg_id, content, sender_id, receiver_id):
    msg_data = {
        'id': msg_id,
        'content': content,
        'sender': sender_id,
        'receiver': receiver_id,
        'timestamp': time.time()
    }
    r.setex(f'message:{msg_id}', 5, json.dumps(msg_data))
    print(f"[INFO] Mensagem {msg_id} adicionada (expira em 5s)")

# Função para exibir usuários ativos
def show_users():
    print("\n[USUÁRIOS ATIVOS]")
    for key in r.scan_iter("user:*"):
        user = json.loads(r.get(key))
        print(f"ID: {user['id']} | Nome: {user['name']} | Email: {user['email']}")

# Função para exibir mensagens ativas
def show_messages():
    print("\n[MENSAGENS ATIVAS]")
    for key in r.scan_iter("message:*"):
        msg = json.loads(r.get(key))
        print(f"ID: {msg['id']} | De: {msg['sender']} | Para: {msg['receiver']} | Conteúdo: {msg['content']}")

# Demonstração: conversa entre dois usuários
if __name__ == "__main__":
    # Limpar Redis antes
    r.flushdb()

    add_user(1, "Alice", "alice@example.com")
    add_user(2, "Bob", "bob@example.com")

    add_message(101, "Oi Bob!", 1, 2)
    
    add_message(102, "Oi Alice! Tudo bem?", 2, 1)

    time.sleep(2)
    show_users()
    show_messages()

    time.sleep(4)
    print("\n[Aguardando 4 segundos…]")
    show_users()
    show_messages()

    time.sleep(60)
    print("\n[Aguardando 60 segundos…]")
    show_users()
    show_messages()
