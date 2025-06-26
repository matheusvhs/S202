# ProjetoS202 - Sistema de Delivery

Este projeto é um sistema de delivery simples com **interface via terminal (CLI)**, backend em **Python/Flask**, e banco de dados **MongoDB**, com cache utilizando **Redis**.


## 📦 Funcionalidades

- Criar pedidos com nome, endereço, telefone e lista de itens
- Atualizar status do pedido (ex: aceito, preparando, etc)
- Buscar pedidos por nome ou telefone do cliente
- Listar todos os pedidos registrados
- Remover pedidos
- Armazenamento persistente com MongoDB
- Cache de status com Redis


## 🚀 Como executar

### Pré-requisitos

- Docker e Docker Compose instalados
- Python

### Inicie os serviços com Docker Compose

```bash
docker compose up --build
```

## 💻 Como usar o CLI

Com os containers rodando, execute:

```bash
python cli_menu.py
```
