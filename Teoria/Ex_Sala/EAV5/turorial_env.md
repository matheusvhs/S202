Siga as instruções dos arquivos de tutorial para rodar os SGBDs localmente via Docker.

Crie um ambiente virtual e instale o Python 3.8.

Recomendo a utilização do miniconda para o ambiente virtual:

        conda create -n nome_ambiente -y
        conda activate nome_ambiente
        conda install python==3.8 -y

Instale as dependências do arquivo "requirements.txt" (em anexo):

        pip install -r requirements.txt

Modifique as credenciais de acesso aos bancos de dados (caso esteja usando a nuvem). 
Acesse o arquivo "np3_enunciado.md" e faça a implementação das funções pedidas no arquito "base.py".
Execute o arquivo abaixo usando o Pytest:

        pytest base.py

Dica: Comente as funções que ainda não tiver implementado para não gerar erro nos testes.
(Se preferir, pode remover o "assert" da função de teste e exibir as resposta com "print" para fazer um teste manual)