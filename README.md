### av_api

Esse pacote usa o API da [Alpha Vantage](https://www.alphavantage.co/documentation/) para fazer o download de dados do mercado financeiro através do python. A Além da API, o pacote também utiliza o `sqlite` para manter as bases localmente.

O pacote é baseado em duas classes:

1. Company: essa classe cria e atualiza dados de uma empresa selecionada.
2. Database: essa classe permite o usuário manipular as databses e tables criadas.

### Exemploo de uso:

No exemplo abaixo instanciamos uma empresa (no caso, a Petrobras que tem ticker=PETR4.SAO) e especificamos que os dados da empresa será salvo em uma `database` chamada `stock_market.db`.

Se a `database` ainda não existe, ela será criada.
```python
from av_api import *

key='sua_chave'

petr=Company(ticker="PETR4.SAO", key=key, database='stock_market.db')
```
Note que `sua_chave` é a chave criada no API (clique [aqui](https://www.alphavantage.co/support/#api-key) para criar sua chave).

Depois de instanciada a empresa, podemos criar uma tabela para receber seus dados:

```python
petr.create_table()
```

Para confirmar que a tabela foi criada, instancie a classe `Database` e liste suas tabelas:

```python
database=Database('stock_market.db')
database.list_tables()
```
Retorna:

```python
['petr4'] #o nomeda tabela é sempre o lowercase do ticker antes do ponto
```

Nesse momento, porém, a tabela `petr4` não tem nenhum dado. Para fazer o download pela primeira vez, use o método `update_table()` com o argumento `full=True` para baixar todos os dados de preços de fechamento disponibilizados pela API:

```python
petr.update_table(full=True)
```

Novamente, para confirmar que o procedimento foi feito, o usuário pode usar a instância `database`:

```python
database.to_dataframe(table_name='petr4').head() #to_dataframe retorna um pandas DataFrame
```
Retorna:

| date         	| ticker    	| close 	|
|--------------	|-----------	|-------	|
| 2021-05-14   	| PETR4.SAO 	| 26.28 	|
| 2021-05-13   	| PETR4.SAO 	| 24.99 	|
| 2021-05-12   	| PETR4.SAO 	| 24.78 	|
| 2021-05-11   	| PETR4.SAO 	| 25.15 	|
| 2021-05-10   	| PETR4.SAO 	| 24.70 	|

O mesmo procedimento pode ser feito para uma outra ação de escolha do usuário. Assim, repetindo o procedimento feito para a petrobras para as ações da B3, temos:

```python
b3=Company(ticker="B3SA3.SAO", key=key, database='stock_market.db')
b3.create_table()
database=Database('stock_market.db')
database.list_tables() #['petr4', 'b3sa3']
b3.update_table(full=True)
database.to_dataframe(table_name='besa3').head() # análogo ao visto acima
```

### Atualizando os dados:

Também é possível usar o método `update_table` para especificar o número de dias a serem atualizados na base local. Por exemplo, para atualizar os dados da última semana para a petrobras, basta fazer:

```python
petr.update_table(full=False, only_days=5)
```



