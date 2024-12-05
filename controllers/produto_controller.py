import mysql.connector
from models.produto import Produto

user = "root"
senha = ""
host = "localhost"
banco = "lanchonete_sabrina"

#retorna a conexâo extabelecida ou retorna None quando der errado
def conectar():
    conexao=None
    try:
        conexao =  mysql.connector.connect(
            host=host,
            user=user,
            password=senha,
            database=banco
        )
    except mysql.connector.Error as e:
        print(f"Erro ao conectar com o BD:{e}")

    return conexao

#finalizar a conexão o fim das operações
def fechar_conexao(conexao):
    if conexao.is_connected():
        conexao.close()
        print("Conexão com o BD encerrada!")
    
#C - Criar um novo registro no banco de dados
def inserir(conexao, produto): 
    try:
        cursor = conexao.cursor()
        #usar o %s para evitar o SQL injector
        query = "INSERT INTO produto(descricao, preco, qtd) VALUES(%s, %s, %s)"
        cursor.execute(query, (produto.descricao,produto.preco,produto.qtd))
        conexao.commit()
        print(f"{produto.descricao} Registrado como sucesso!")
        
    except mysql.connector.Error as e:
        print(f"Erro ao inserir produto:{e}")  
    finally:
        cursor.close()
    

#R - Read retona uma lista de objeto produto
def listar(conexao): 
    listaProdutos=[]
    try:
      cursor = conexao.cursor()
      query = "Select * from produto"
      cursor.execute(query)
      registros = cursor.fetchall()
      for registro in registros:
          objeto =  Produto(*registro) #Produto(registro[0],registro[1],..)
          listaProdutos.append(objeto)
      
    except mysql.connector.Error as e:
        print(f"Erro ao listar produtos:{e}")  
    finally:
        cursor.close()
    return listaProdutos

#U - update- atualizar uma informação de uma linha
def update(conexao, idProduto, preco, qtd):
    try:
        cursor =  conexao.cursor()
        query = "UPDATE produto SET preco=%s, qtd=%s WHERE id_codigo_produto=%s"
        cursor.execute(query, (preco, qtd, idProduto))
        conexao.commit()
        print(f"{idProduto} atualizado com sucesso!")
    except mysql.connector.Error as e:
        print(f"Erro ao atualizar produto:{e}")  
    finally:
        cursor.close()

#D deletar uma linha a partir de um ID
def delete(conexao, idProduto):
    try:
        cursor =  conexao.cursor()
        query = "DELETE FROM produto WHERE id_codigo_produto=%s"
        cursor.execute(query,(idProduto,))
        conexao.commit()
        print(F"{idProduto} Excluído!")
        
    except mysql.connector.Error as e:
        print(f"Erro ao excluir produto:{e}")  
    finally:
        cursor.close()
    
#buscar informações de uma linha
def buscar(conexao, busca):
    listaProduto=[]
    try:
        cursor = conexao.cursor()
        query = "Select * from produto where descricao like %s "
        cursor.execute(query, ("%"+busca+"%",))
        registros = cursor.fetchall()
      
        for produto in registros:
            objeto=Produto(*produto)
            listaProduto.append(objeto)   
    except mysql.connector.Error as e:
        print(f"Erro ao buscar produto:{e}")  
    finally:
        cursor.close()
    return listaProduto

#####Main######
conexao = conectar()

if conexao!=None:
    print("Conectado com o banco de dados")
  
    produtos =  buscar(conexao, "dsadsakshd")
    if produtos!=[]:
        for produto in produtos:
            produto.listar()
    else:
        print("Nenhum produto encontrado!")
    
    fechar_conexao(conexao)