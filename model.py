from abc import ABC, abstractmethod
import json

class Carrinho():
    def __init__(self):
        self.__lista_produtos = []

    def listar_produtos(self):
        for produto in self.__lista_produtos:
            print(str(produto))

    def adicionar_produto(self,produto):
        self.__lista_produtos.append(produto)
        return True

    def remover_produto(self, id_produto):
        for produto in self.__lista_produtos:
            if str(produto.get_id()) == str(id_produto):

                self.__lista_produtos.remove(produto)
                return True

    def finalizar_pedido(self,cliente:Cliente):
        pedido = Pedido(self.__lista_produtos.copy(),self.get_valor_total(),cliente)
        self.__lista_produtos.clear()
        return pedido

    def quantidade_produtos(self):
        return len(self.__lista_produtos)
    
    def get_valor_total(self):
        total = 0
        for produto in self.__lista_produtos:
            total += produto.get_valor()
        return total


class Produto():
    proximo_id = 1
    def __init__(self,nome,valor):
        self.__id = Produto.proximo_id
        self.__valor = valor
        self.__nome = nome

        Produto.proximo_id += 1

    def __str__(self):
        return f"[ID: {self.__id}] {self.__nome} - R$ {self.__valor:.2f}"
    
    def get_valor(self):
        return self.__valor
    
    def get_id(self):
        return self.__id
    
    def set_id(self,id):
        self.__id = id
    
    def to_dict(self):
        return {
            "id": self.__id,
            "nome": self.__nome,
            "valor": self.__valor
        }
    

class Pedido():
    proximo_id = 1
    
    def __init__(self,lista_produtos, total,cliente:Cliente):
        self.__id = Pedido.proximo_id
        self.__lista_produtos = lista_produtos
        self.__total = total
        self.__cliente = cliente

        Pedido.proximo_id += 1

    def __str__(self):
        texto = f"PEDIDO {self.__id} - {self.__cliente.get_nome()}\n"
        texto += f" Documento: {self.__cliente.get_documento()} - Endereco: {self.__cliente.get_endereco()}\n"
        texto += f" {"-" * 55}\n"

        for produto in self.__lista_produtos:
            texto += f" - {produto}\n"

        texto += f" {"-" * 55} \nTotal: R$ {self.__total:.2f}\n"

        return texto
    
    def get_id(self):
        return self.__id
    
    def set_id(self,id):
        self.__id = id
    
    def to_dict(self):
        return {
            "id": self.__id,
            "total": self.__total,
            "cliente": self.__cliente.to_dict(),
            "produtos": [p.to_dict() for p in self.__lista_produtos]
        }

class Loja():
    def __init__(self):
        self.__lista_pedidos = []
        self.__lista_produtos = []
        self.__carregar_loja()

    def listar_produtos(self):
        for produto in self.__lista_produtos:
            print(produto)
    
    def listar_pedidos(self):
        for pedido in self.__lista_pedidos:
            print(pedido)

    def adiciona_pedido(self,pedido):
        self.__lista_pedidos.append(pedido)
        print(pedido)
        self.__persistir_loja()
        return True

    def adiciona_produto(self,nome,valor):
        produto = Produto(nome,valor)        
        self.__lista_produtos.append(produto)
        self.__persistir_loja()
        return True
    
    def buscar_produto(self, id_produto):
        for produto in self.__lista_produtos:
            if str(produto.get_id()) == str(id_produto):
                return produto
        return None
    
    def buscar_pedido(self, id_pedido):
        for pedido in self.__lista_pedidos:
            if str(pedido.get_id()) == str(id_pedido):
                return pedido
        return None

    def remover_produto(self, id_produto):
        for produto in self.__lista_produtos:
            if str(produto.get_id()) == str(id_produto):

                self.__lista_produtos.remove(produto)
                self.__persistir_loja()
                return True
    
    def __persistir_loja(self):
        dados = {
        "produtos": [p.to_dict() for p in self.__lista_produtos],
        "pedidos": [p.to_dict() for p in self.__lista_pedidos]
        }

        with open("pseudoDB.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def __carregar_loja(self):
        try:
            with open("pseudoDB.json", "r", encoding="utf-8") as f:
                dados = json.load(f)

            #carrega lista produtos
            self.__lista_produtos.clear()
            for produto_json in dados.get("produtos", []):
                produto = Produto(produto_json["nome"],produto_json["valor"])
                produto.set_id(produto_json["id"])
                self.__lista_produtos.append(produto)

            
            #carrega lista pedidos
            self.__lista_pedidos.clear()
            for pedido_json in dados.get("pedidos", []):
                cliente_json = pedido_json["cliente"]

                if cliente_json["tipo"] == "CPF":
                    cliente = ClienteCPF(
                        cliente_json["nome"],
                        cliente_json["endereco"],
                        cliente_json["documento"]
                    )

                if cliente_json["tipo"] == "CNPJ":
                    cliente = ClienteCNPJ(
                        cliente_json["nome"],
                        cliente_json["endereco"],
                        cliente_json["documento"]
                    )

                lista_produtos = []

                for produto_json in pedido_json["produtos"]:
                    produto = Produto(produto_json["nome"],produto_json["valor"])
                    produto.set_id(produto_json["id"])
                    lista_produtos.append(produto)

                pedido = Pedido(
                    lista_produtos=lista_produtos,
                    total=pedido_json["total"],
                    cliente=cliente
                    )
                pedido.set_id(pedido_json["id"])
                self.__lista_pedidos.append(pedido)

            Produto.proximo_id = self.maior_id_produto() + 1
            Pedido.proximo_id = self.maior_id_pedido() + 1

        except FileNotFoundError:
            pass
    
    def maior_id_produto(self):
        if len(self.__lista_produtos) == 0:
            return 0

        maior = 0
        for produto in self.__lista_produtos:
            if produto.get_id() > maior:
                maior = produto.get_id()
        return maior
    
    def maior_id_pedido(self):
        if len(self.__lista_pedidos) == 0:
            return 0

        maior = 0
        for pedido in self.__lista_pedidos:
            if pedido.get_id() > maior:
                maior = pedido.get_id()
        return maior
            
class Cliente(ABC):
    def __init__(self, nome, endereco):
        self.__nome = nome
        self.__endereco = endereco

    def get_nome(self):
        return self.__nome

    def get_endereco(self):
        return self.__endereco

    @abstractmethod
    def get_documento(self):
        pass


class ClienteCPF(Cliente):
    def __init__(self, nome, endereco, cpf):
        super().__init__(nome, endereco)
        self.__cpf = cpf

    def get_documento(self):
        return self.__cpf
    
    def to_dict(self):
        return {
            "tipo": "CPF",
            "nome": self.get_nome(),
            "endereco": self.get_endereco(),
            "documento": self.get_documento()
        }


class ClienteCNPJ(Cliente):
    def __init__(self, nome, endereco, cnpj):
        super().__init__(nome, endereco)
        self.__cnpj = cnpj

    def get_documento(self):
        return self.__cnpj
    
    def to_dict(self):
        return {
            "tipo": "CNPJ",
            "nome": self.get_nome(),
            "endereco": self.get_endereco(),
            "documento": self.get_documento()
        }