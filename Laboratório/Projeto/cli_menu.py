import requests
import sys

BASE_URL = "http://localhost:5000"  # ajuste se necessário

def menu():
    print("\n=== MENU DO SISTEMA DE DELIVERY ===")
    print("1. Criar novo pedido")
    print("2. Listar todos os pedidos")
    print("3. Atualizar status do pedido")
    print("4. Ver pedidos de um cliente")
    print("5. Deletar pedido")
    print("6. Sair")

def criar_pedido():
    nome = input("Nome do cliente: ")
    endereco = input("Endereço do cliente: ")
    telefone = input("Telefone do cliente: ")
    itens = input("Itens do pedido (ex: pizza, refrigerante): ").split(',')
    payload = {
        "cliente": {
            "nome": nome,
            "endereco": endereco,
            "telefone": telefone
        },
        "itens": [i.strip() for i in itens]
    }
    try:
        r = requests.post(f"{BASE_URL}/pedido", json=payload)
        print(r.json())
    except Exception as e:
        print("Erro ao criar pedido:", e)

def listar_pedidos():
    try:
        r = requests.get(f"{BASE_URL}/pedidos")
        pedidos = r.json()
        for pedido in pedidos:
            cliente = pedido.get("cliente", {})
            if isinstance(cliente, dict):
                nome = cliente.get("nome", "")
                endereco = cliente.get("endereco", "")
                telefone = cliente.get("telefone", "")
            else:
                nome = str(cliente)
                endereco = ""
                telefone = ""
            print(f"ID: {pedido['_id']}")
            print(f"Cliente: {nome} - {endereco} - {telefone}")
            print(f"Itens: {pedido['itens']}")
            print(f"Status: {pedido['status']}\n")
    except Exception as e:
        print("Erro ao listar pedidos:", e)

def atualizar_status():
    pedido_id = input("ID do pedido: ")
    status_permitidos = ['aceito', 'cancelado', 'preparando', 'saiu para entrega', 'entregue']

    print("\nEscolha o novo status:")
    print("1. aceito")
    print("2. cancelado")
    print("3. preparando")
    print("4. saiu para entrega")
    print("5. entregue")

    try:
        opcao = int(input("Digite o número correspondente: "))
        if 1 <= opcao <= 5:
            status = status_permitidos[opcao - 1]
            r = requests.put(f"{BASE_URL}/pedido/{pedido_id}", json={"status": status})
            if r.status_code == 200:
                print("✅ Status atualizado com sucesso!")
                print(r.json())
            else:
                print(f"❌ Erro ao atualizar: {r.status_code} - {r.text}")
        else:
            print("❌ Opção inválida. Escolha um número entre 1 e 5.")
    except ValueError:
        print("❌ Entrada inválida. Digite um número válido.")
    except Exception as e:
        print("❌ Erro ao atualizar status:", e)

def ver_pedidos_cliente():
    nome = input("Nome ou telefone do cliente: ")
    try:
        r = requests.get(f"{BASE_URL}/cliente/{nome}")
        pedidos = r.json()
        for pedido in pedidos:
            print(f"ID: {pedido['_id']}, Itens: {pedido['itens']}, Status: {pedido['status']}")
    except Exception as e:
        print("Erro ao buscar pedidos:", e)

def deletar_pedido():
    pedido_id = input("ID do pedido: ")
    try:
        r = requests.delete(f"{BASE_URL}/pedido/{pedido_id}")
        print(r.json())
    except Exception as e:
        print("Erro ao deletar pedido:", e)

if __name__ == "__main__":
    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            criar_pedido()
        elif opcao == '2':
            listar_pedidos()
        elif opcao == '3':
            atualizar_status()
        elif opcao == '4':
            ver_pedidos_cliente()
        elif opcao == '5':
            deletar_pedido()
        elif opcao == '6':
            print("Saindo...")
            sys.exit()
        else:
            print("Opção inválida. Tente novamente.")
