from abc import ABC, abstractmethod
import json

class PseudoDB():
    ARQUIVO = "pseudoDB.json"

    @staticmethod
    def carregar_dados():
        try:
            with open(PseudoDB.ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "usuarios": [],
                "lojas": [],
                "pedidos": []
            }

    @staticmethod
    def salvar_dados(dados):
        with open(PseudoDB.ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

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

    def finalizar_pedido(self, cliente, loja):
        pedido = Pedido(
            self.__lista_produtos.copy(),
            self.get_valor_total(),
            cliente,
            loja
        )

        self.limpar_carrinho()

        return pedido

    def quantidade_produtos(self):
        return len(self.__lista_produtos)
    
    def get_valor_total(self):
        total = 0
        for produto in self.__lista_produtos:
            total += produto.get_valor()
        return total

    def limpar_carrinho(self):
        self.__lista_produtos.clear()

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

    @staticmethod
    def from_dict(dados_produto):
        produto = Produto(
            dados_produto["nome"],
            dados_produto["valor"]
        )

        produto.set_id(dados_produto["id"])

        return produto

    
class RepositorioPedidos():
    def __init__(self):
        self.__lista_pedidos = []
        self.__carregar_pedidos()

    def __persistir_pedidos(self):
        dados = PseudoDB.carregar_dados()

        dados["pedidos"] = [
            pedido.to_dict() for pedido in self.__lista_pedidos
        ]

        PseudoDB.salvar_dados(dados)

    def __carregar_pedidos(self):
        dados = PseudoDB.carregar_dados()

        self.__lista_pedidos.clear()

        for pedido_dados in dados.get("pedidos", []):

            pedido = Pedido.from_dict(pedido_dados)

            self.__lista_pedidos.append(pedido)
        
        Pedido.proximo_id = self.maior_id_pedido() + 1

    def pedidos_do_cliente(self, cliente):
        pedidos_cliente = []

        for pedido in self.__lista_pedidos:
            if str(pedido.get_cliente().get_usuario()) == str(cliente.get_usuario()):
                pedidos_cliente.append(pedido)

        return pedidos_cliente
    
    def pedidos_da_loja(self, loja):
        pedidos_loja = []

        for pedido in self.__lista_pedidos:
            if str(pedido.get_loja().get_id()) == str(loja.get_id()):
                pedidos_loja.append(pedido)

        return pedidos_loja
    
    def listar_pedidos(self):
        for pedido in self.__lista_pedidos:
            print(pedido)

    def adiciona_pedido(self,pedido):
        self.__lista_pedidos.append(pedido)
        print(pedido)
        self.__persistir_pedidos()
        return True

    def buscar_pedido(self, id_pedido):
        for pedido in self.__lista_pedidos:
            if str(pedido.get_id()) == str(id_pedido):
                return pedido
        return None
    
    def get_lista_pedidos(self):
        return self.__lista_pedidos

    def maior_id_pedido(self):
        if len(self.__lista_pedidos) == 0:
            return 0

        maior = 0
        for pedido in self.__lista_pedidos:
            if pedido.get_id() > maior:
                maior = pedido.get_id()
        return maior
    
class Pedido():
    proximo_id = 1
    
    def __init__(self,lista_produtos, total,cliente,loja):
        self.__id = Pedido.proximo_id
        self.__lista_produtos = lista_produtos
        self.__total = total
        self.__cliente = cliente
        self.__loja = loja

        Pedido.proximo_id += 1

    def __str__(self):
        texto = f"LOJA: {self.__loja.get_nome()}\n"
        texto += f"PEDIDO {self.__id} - {self.__cliente.get_nome()}\n"
        texto += f" Documento: {self.__cliente.get_documento()} - Endereco: {self.__cliente.get_endereco()}\n"
        texto += f" {"-" * 55}\n"

        for produto in self.__lista_produtos:
            texto += f" - {produto}\n"

        texto += f" {"-" * 55} \nTotal: R$ {self.__total:.2f}\n"

        return texto
    
    @staticmethod
    def from_dict(dadosdb):
        cliente = Cliente.from_dict(dadosdb["cliente"])

        loja = Loja(dadosdb["loja"]["nome"])

        loja.set_id(dadosdb["loja"]["id"])

        lista_produtos = [
            Produto.from_dict(produto)
            for produto in dadosdb["produtos"]
        ]

        pedido = Pedido(
            lista_produtos=lista_produtos,
            total=dadosdb["total"],
            cliente=cliente,
            loja=loja
        )

        pedido.set_id(dadosdb["id"])

        return pedido
    
    def to_dict(self):
        return {
            "id": self.__id,
            "total": self.__total,
            "cliente": self.__cliente.to_dict(),
            "loja": {
                "id": self.__loja.get_id(),
                "nome": self.__loja.get_nome()
            },
            "produtos": [p.to_dict() for p in self.__lista_produtos]
        }
    
    def get_loja(self):
        return self.__loja
    
    def get_cliente(self):
        return self.__cliente
    
    def get_id(self):
        return self.__id
    
    def set_id(self,id):
        self.__id = id
    

    




class LojasManager():
    def __init__(self):
        self.__lista_lojas = []
        self.__loja_logada = None
        self.__carregar_lojas()

    def __persistir_lojas(self):
        dados = PseudoDB.carregar_dados()

        dados["lojas"] = [
            loja.to_dict() for loja in self.__lista_lojas
        ]

        PseudoDB.salvar_dados(dados)

    def __carregar_lojas(self):
        dados = PseudoDB.carregar_dados()

        self.__lista_lojas.clear()

        for loja_json in dados.get("lojas", []):
            loja = Loja.from_dict(loja_json)
            self.__lista_lojas.append(loja)

        Loja.proximo_id = self.maior_id_loja() + 1
        Produto.proximo_id = self.maior_id_produto() + 1

    def salvardb(self):
        self.__persistir_lojas()

    def adiciona_loja(self, loja):
        self.__lista_lojas.append(loja)
        self.__persistir_lojas()
        return True

    def listar_lojas(self):
        for loja in self.__lista_lojas:
            print(loja)

    def buscar_loja(self, id):
        for loja in self.__lista_lojas:
            if str(loja.get_id()) == str(id):
                return loja

        return None

    def remover_loja(self, id):
        loja = self.buscar_loja(id)
        if loja:
            self.__lista_lojas.remove(loja)
            self.__persistir_lojas()
            return True
        return False

    def logar_loja(self,id):
        for loja in self.__lista_lojas:
            if str(loja.get_id()) == str(id):
                self.__loja_logada = loja
                return True
        return False

    def deslogar_loja(self):
        self.__loja_logada = None

    def get_loja_logada(self):
        return self.__loja_logada
    
    def maior_id_produto(self):
        maior = 0

        for loja in self.__lista_lojas:
            for produto in loja.get_lista_produtos():
                if produto.get_id() > maior:
                    maior = produto.get_id()

        return maior
    
    def maior_id_loja(self):
        if len(self.__lista_lojas) == 0:
            return 0

        maior = 0

        for loja in self.__lista_lojas:
            if loja.get_id() > maior:
                maior = loja.get_id()

        return maior
    
class Loja():
    proximo_id = 1
    def __init__(self,nome):
        self.__id = Loja.proximo_id
        self.__lista_produtos = []
        self.__nome = nome    

        Loja.proximo_id += 1

    def __str__(self):
        return f"[ID: {self.__id:<3}] {self.__nome}"

    def to_dict(self):
        return {
            "id": self.__id,
            "nome": self.__nome,
            "produtos": [p.to_dict() for p in self.__lista_produtos]
        }

    @staticmethod
    def from_dict(data):
        loja = Loja(data["nome"])

        loja.set_id(data["id"])

        for produto_json in data.get("produtos", []):
            loja.__lista_produtos.append(
                Produto.from_dict(produto_json)
            )

        return loja

    def listar_produtos(self):
        for produto in self.__lista_produtos:
            print(produto)

    def adiciona_produto(self,nome,valor):
        try:
            valor = float(valor)
        except Exception:
            return False
        
        produto = Produto(nome,valor)        
        self.__lista_produtos.append(produto)
        return True
    
    def buscar_produto(self, id_produto):
        for produto in self.__lista_produtos:
            if str(produto.get_id()) == str(id_produto):
                return produto
        return None
    
    def remover_produto(self, id_produto):
        try:
            for produto in self.__lista_produtos:
                if str(produto.get_id()) == str(id_produto):

                    self.__lista_produtos.remove(produto)
                    return True
        except Exception:
            return False
            
    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id
    
    def get_nome(self):
        return self.__nome

    def get_lista_produtos(self):
        return self.__lista_produtos  





    
class Login():
    def __init__(self):
        self.__lista_usuarios = []
        self.__usuario_logado = None
        self.__carregar_usuarios()

    def __carregar_usuarios(self):
        dados = PseudoDB.carregar_dados()

        self.__lista_usuarios.clear()

        for usuario_json in dados.get("usuarios", []):

            cliente = Cliente.from_dict(usuario_json)

            self.__lista_usuarios.append(cliente)
        
    def __persistir_usuarios(self):
        dados = PseudoDB.carregar_dados()

        dados["usuarios"] = [
            usuario.to_dict() for usuario in self.__lista_usuarios
        ]

        PseudoDB.salvar_dados(dados)

    def adiciona_usuario(self,cliente):
        for usuario in self.__lista_usuarios:
            if str(usuario.get_usuario()) == (cliente.get_usuario()):
                return False

        self.__lista_usuarios.append(cliente)
        self.__persistir_usuarios()
        return True

    def logar_usuario(self,usuario,senha):
        for cliente in self.__lista_usuarios:
            if str(cliente.get_usuario()) == str(usuario) and str(cliente.get_senha()) == str(senha):
                self.__usuario_logado = cliente
                return True
        return False
    
    def remover_usuario(self, usuario_remover):
        for usuario in self.__lista_usuarios:
            if str(usuario.get_usuario()) == str(usuario_remover):
                self.__lista_usuarios.remove(usuario)
                self.__persistir_usuarios()
                return True

        return False

    def listar_usuarios(self):
        for usuario in self.__lista_usuarios:
            print(usuario)
    
    def deslogar_usuario(self):
        self.__usuario_logado = None

    def get_usuario_logado(self):
        return self.__usuario_logado
    
class Cliente(ABC):
    def __init__(self, nome, endereco,usuario,senha):
        self.__usuario = usuario
        self.__senha = senha
        self.__nome = nome
        self.__endereco = endereco

    @staticmethod
    def from_dict(cliente):
        if cliente["tipo"] == "CPF":
            return ClienteCPF(
                cliente["nome"],
                cliente["endereco"],
                cliente["documento"],
                cliente["usuario"],
                cliente["senha"]
            )

        if cliente["tipo"] == "CNPJ":
            return ClienteCNPJ(
                cliente["nome"],
                cliente["endereco"],
                cliente["documento"],
                cliente["usuario"],
                cliente["senha"]
            )

    def __str__(self):
        return (f"Usuário: {self.get_usuario():<20}| Nome: {self.get_nome():<25}| Documento: {self.get_documento()}"        )

    def get_usuario(self):
        return self.__usuario

    def get_senha(self):
        return self.__senha

    def get_nome(self):
        return self.__nome

    def get_endereco(self):
        return self.__endereco

    @abstractmethod
    def get_documento(self):
        pass


class ClienteCPF(Cliente):
    def __init__(self, nome, endereco, cpf,usuario,senha):
        super().__init__(nome, endereco,usuario,senha)
        self.__cpf = cpf

    def get_documento(self):
        return self.__cpf
    
    def to_dict(self):
        return {
            "usuario":self.get_usuario(),
            "senha":self.get_senha(),
            "tipo": "CPF",
            "nome": self.get_nome(),
            "endereco": self.get_endereco(),
            "documento": self.get_documento()
        }

class ClienteCNPJ(Cliente):
    def __init__(self, nome, endereco, cnpj,usuario,senha):
        super().__init__(nome, endereco,usuario,senha)
        self.__cnpj = cnpj

    def get_documento(self):
        return self.__cnpj
    
    def to_dict(self):
        return {
            "usuario":self.get_usuario(),
            "senha":self.get_senha(),
            "tipo": "CNPJ",
            "nome": self.get_nome(),
            "endereco": self.get_endereco(),
            "documento": self.get_documento()
        }