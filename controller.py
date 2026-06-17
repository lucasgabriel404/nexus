from view import Menu
from model import Carrinho,Produto,Pedido,Loja,ClienteCPF,ClienteCNPJ

class Controller():
    def __init__(self):
        self.__menu = Menu()
        self.__carrinho = Carrinho()
        self.__loja = Loja()
    
    def start(self):
        while True:
            self.__menu.limpa_tela()
            self.__menu.exibe_banner()
            self.__menu.exibe_menu_inicial()
            opcao = self.consiste(0,3)
            match opcao:
                case 0:
                    self.tela_sair()
                    break
                case 1:
                    self.tela_cliente()
                case 2:
                    self.tela_vendedor()
                case 3:
                    self.tela_administrador()
                case _:
                    print("Opção inválida")

    def tela_cliente(self):        
        while True:
            self.__menu.limpa_tela()
            self.__menu.exibe_menu_cliente()
            opcao = self.consiste(0,4)
            match opcao:
                case 0:
                    #voltar menu principal
                    self.tela_volta_menu_principal()
                    self.__menu.exibe_pausa()
                    break
                case 1:
                    #ver carrinho
                    self.__menu.limpa_tela()
                    self.tela_cliente_lista_carrinho()
                    self.__menu.exibe_pausa()
                case 2:
                    #adicionar produto no carrinho
                    self.__menu.limpa_tela()
                    self.tela_cliente_adicionar_produto()
                    self.__menu.exibe_pausa()
                case 3:
                    #remover produto do carrinho
                    self.__menu.limpa_tela()
                    self.tela_cliente_remover_produto()
                    self.__menu.exibe_pausa()
                case 4:
                    #finalizar pedido
                    self.__menu.limpa_tela()
                    self.tela_cliente_finalizar_pedido()
                    self.__menu.exibe_pausa()
                case _:
                    print("Opção inválida")

    def tela_vendedor(self):
        while True:
            self.__menu.limpa_tela()
            self.__menu.exibe_menu_vendedor()
            opcao = self.consiste(0,3)
            match opcao:
                case 0:
                    #voltar menu principal
                    self.tela_volta_menu_principal()
                    self.__menu.exibe_pausa()
                    break
                case 1:
                    #listar produtos
                    self.__menu.limpa_tela()
                    self.tela_vendedor_lista_produtos()
                    self.__menu.exibe_pausa()
                case 2:
                    #cadastrar produto
                    self.__menu.limpa_tela()
                    self.tela_vendedor_cadastra_produto()
                    self.__menu.exibe_pausa()
                case 3:
                    #excluir produto
                    self.__menu.limpa_tela()
                    self.tela_vendedor_excluir_produto()
                    self.__menu.exibe_pausa()
                case _:
                    print("Opção inválida")

    #AVALIAR SE FAZ SENTIDO
    def tela_administrador(self):
        while True:
            self.__menu.limpa_tela()
            self.__menu.exibe_menu_administrador()
            opcao = self.consiste(0,2)
            match opcao:
                case 0:
                    #voltar menu principal
                    self.tela_volta_menu_principal()
                    self.__menu.exibe_pausa()
                    break
                case 1:
                    #listar pedidos
                    self.__menu.limpa_tela()
                    self.tela_administrador_lista_pedidos()
                    self.__menu.exibe_pausa()
                case 2:
                    #buscar pedido id
                    self.__menu.limpa_tela()
                    self.tela_administrador_busca_pedido()
                    self.__menu.exibe_pausa()
                case _:
                    print("Opção inválida")

    
    #menu cliente
    def tela_cliente_lista_carrinho(self):
        self.__menu.exibe_mensagem_lista_carrinho()
        self.__carrinho.listar_produtos()
        self.__menu.exibe_valor_total(self.__carrinho.get_valor_total())

    def tela_cliente_adicionar_produto(self):
        self.__menu.exibe_mensagem_lista_produtos()
        self.__loja.listar_produtos()
        id_produto = input("Digite o ID do produto para adicionar ao carrinho: ")
        
        produto = self.__loja.buscar_produto(id_produto)
        
        if not produto:
            self.__menu.exibe_falha()
            return

        if not self.__carrinho.adicionar_produto(produto):
            self.__menu.exibe_falha()
            return        

        self.__menu.exibe_sucesso()
    
    def tela_cliente_remover_produto(self):
        self.__menu.exibe_mensagem_lista_produtos()
        self.__carrinho.listar_produtos()
        id_produto = input("Digite o ID do produto para remover do carrinho: ")

        if not self.__carrinho.remover_produto(id_produto):
            self.__menu.exibe_falha()
            return
        
        self.__menu.exibe_sucesso()        

    
    def tela_cliente_finalizar_pedido(self):
        if self.__carrinho.quantidade_produtos() == 0:
            self.__menu.exibe_mensagem_carrinho_vazio()
            return
    
        self.__menu.exibe_menu_tipo_cliente()
        tipo = self.consiste(1,2)

        match tipo:
                case 0:
                    #voltar
                    self.tela_volta_menu_principal()
                    self.__menu.exibe_pausa()
                case 1:
                    #cpf
                    self.__menu.limpa_tela()
                    self.__menu.exibe_mensagem_cadastro_cpf()
                    nome = input("Nome: ")
                    endereco = input("Endereço: ")
                    cpf = input("CPF: ")
                    cliente = ClienteCPF(nome, endereco, cpf)
                    self.__menu.exibe_pausa()

                case 2:
                    #cnpj
                    self.__menu.limpa_tela()
                    self.__menu.exibe_mensagem_cadastro_cnpj()
                    nome = input("Razão Social: ")
                    endereco = input("Endereço: ")
                    cnpj = input("CNPJ: ")
                    cliente = ClienteCNPJ(nome, endereco, cnpj)
                    self.__menu.exibe_pausa()
        
        self.__menu.limpa_tela()
        pedido = self.__carrinho.finalizar_pedido(cliente)        
        if not self.__loja.adiciona_pedido(pedido):
            self.__menu.exibe_falha()
            return
        
        self.__menu.exibe_sucesso()


    #menu vendedor
    def tela_vendedor_lista_produtos(self):
        self.__menu.exibe_mensagem_lista_produtos()
        self.__loja.listar_produtos()

    def tela_vendedor_cadastra_produto(self):
        self.__menu.exibe_mensagem_cadastro_produto()
        nome_produto = input("Nome do produto: ")
        preco = float(input("Digite o preço do produto: "))
        if not self.__loja.adiciona_produto(nome_produto,preco):
            self.__menu.exibe_falha()
            return
        self.__menu.exibe_sucesso()
    
    def tela_vendedor_excluir_produto(self):
        self.__menu.exibe_mensagem_lista_produtos()
        self.__loja.listar_produtos()
        id_produto = input("Digite o ID do produto para remover da loja: ")

        if not self.__loja.remover_produto(id_produto):
            self.__menu.exibe_falha()
            return
        
        self.__menu.exibe_sucesso()


    #menu administrador    
    def tela_administrador_lista_pedidos(self):
        self.__loja.listar_pedidos()

    def tela_administrador_busca_pedido(self):
        id_pedido = input("Digite o ID do pedido desejado: ")        
        pedido = self.__loja.buscar_pedido(id_pedido)

        if not pedido:
            self.__menu.exibe_falha()
            return
        
        self.__menu.exibe(pedido)


    #menus gerais
    def tela_volta_menu_principal(self):
        self.__menu.exibe_voltando_menu_principal()

    def tela_sair(self):
        self.__menu.exibe_mensagem_sair()


    #utils
    def consiste(self,ini: int, fim: int):
        if ini > fim: ini, fim = fim, ini
        num = fim + 1
        erro = True
        while erro:
            try:
                prompt = f"Número no intervalo [{ini} - {fim}]:"
                num = int(input(prompt))
                if ini <= num <= fim: erro = False
            except ValueError: erro = True
            if erro: print("Número errado! Digite novamente!")
        return num



    