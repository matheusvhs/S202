### 1. Acessando o ambiente online do Docker Lab

Acesse o laboratório do [Play With Docker](https://labs.play-with-docker.com/), crie uma conta e faça o login.

Caso o terminal ainda não esteja liberado, clique em `+ ADD NEW INSTANCE` no painel lateral para criar uma instância.

Usando o comando `docker ps` você pode notar que o Docker já está instalado e em execução.

Basta rodar o comando para executar o container de acordo com a atividade.

### 2. Criando os arquivos da atividade

Para adicionar um arquivo na máquina do laboratório pelo terminal use o comando:

```bash
cat > nome.py
```

Esse comando vai bloquear o terminar para edição do conteúdo do arquivo e você já pode digitar o conteúdo.

Porém, para facilitar a edição, você pode usar o comando `Ctrl + C` para sair da edição pelo terminal e em seguida clique no botão `EDITOR` na parte superior do terminal.

Clique em `↻` para recarregar a pasta e mostrar o arquivo criado caso ele não seja mostrado.

Acessando o arquivo pelo editor você pode copiar e colar o código da sua máquina para a máquina do laboratório. Salve o código para efetivar a edição.

Você pode usar o comando `ls` para verificar se o arquivo foi criado com sucesso.

Para renomear o arquivo vc pode user o comando `mv <nome atual do arquivo> <novo nome do arquivo>`.

> Você pode criar um novo arquivo de `requirements.txt` usando o mesmo processo descrito anteriormente, caso deseje.

### 3. Executando os arquivos

A máquina do laboratório já consta com o Python instalado.

Para executar a atividade basta criar um ambiente virtual do Python com o comando:

```bash
python -m venv venv
```

E ativar o ambiente com o comando:

```bash
source venv/bin/activate
```

Em seguida, você pode instalar as dependências da atividade:

```bash
pip install -r requirements.txt
```

E rodar os testes:

```bash
pytest nome.py
```
