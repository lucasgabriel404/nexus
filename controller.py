from view import View
from model import *

class Controller():
    def __init__(self):
        self.__view = View()
        self.__login = Login()
        self.__carrinho = Carrinho()        
        self.__lojasmanager = LojasManager()
        self.__repopedidos = RepositorioPedidos()

        self.__loja_cliente = None
    
    def start(self):
        while True:
            self.__view.limpa_tela()
            self.__view.exibe_banner()
            self.__view.exibe_menu_inicial()
            opcao = self.consiste(0,3)
            match opcao:
                case 0:
                    self.tela_sair()
                    break
                case 1:
                    self.tela_cliente_login()
                case 2:
                    self.tela_loja_escolhe()
                case 3:
                    self.tela_administrador()
                case _:
                    print("Opção inválida")

    def tela_cliente_login(self):
        while not self.__login.get_usuario_logado():
            self.__view.limpa_tela()
            self.__view.exibe_login_cliente()
            user = str(input("Digite o usuario, ou digite 1 para primeiro acesso: "))
            if user == str(1):
                self.__view.limpa_tela()
                self.tela_cadastro_cliente()
                self.__view.exibe_pausa()
                return
            
            senha = str(input("Digite a senha: "))
            if self.__login.logar_usuario(user,senha):
                self.__view.exibe_sucesso()
                self.__view.exibe_pausa()
                self.tela_cliente_menu()
                self.__view.exibe_pausa()
                self.__login.deslogar_usuario()
                break
            self.__view.exibe_login_falhou()
            self.__view.exibe_pausa()
            break

    def tela_cadastro_cliente(self):
        self.__view.exibe_cadastro_cliente()
        self.__view.exibe_menu_tipo_cliente()
        tipo = self.consiste(0,2)

        match tipo:
                case 0:
                    #voltar
                    self.__view.exibe_voltando_menu_principal()
                    return
                case 1:
                    #cpf
                    self.__view.limpa_tela()
                    self.__view.exibe_mensagem_cadastro_cpf()
                    user = input("Usuário: ")
                    senha = str(input("Senha: "))
                    nome = input("Nome: ")
                    endereco = input("Endereço: ")
                    cpf = input("CPF: ")
                    cliente = ClienteCPF(nome, endereco, cpf, user, senha)

                case 2:
                    #cnpj
                    self.__view.limpa_tela()
                    self.__view.exibe_mensagem_cadastro_cnpj()
                    user = input("Usuário: ")
                    senha = str(input("Senha: "))
                    nome = input("Razão Social: ")
                    endereco = input("Endereço: ")
                    cnpj = input("CNPJ: ")
                    cliente = ClienteCNPJ(nome, endereco, cnpj, user, senha)
                
        if self.__login.adiciona_usuario(cliente):
            self.__view.exibe_sucesso_cadastro()
            return

        self.__view.exibe_falha_cadastro()
        return
    
    def tela_cliente_menu(self):        
        while True:
            self.__view.limpa_tela()
            self.__view.exibe_menu_cliente(self.__loja_cliente,self.__login.get_usuario_logado())
            opcao = self.consiste(0,6)
            match opcao:
                case 0:
                    #voltar menu principal
                    self.__carrinho.limpar_carrinho()
                    self.__loja_cliente = None
                    self.tela_volta_menu_principal()
                    break
                case 1:
                    #trocar loja
                    self.__view.limpa_tela()
                    self.tela_cliente_selecionar_loja()
                    self.__view.exibe_pausa()
                case 2:
                    #ver carrinho
                    self.__view.limpa_tela()
                    self.tela_cliente_lista_carrinho()
                    self.__view.exibe_pausa()
                case 3:
                    #adicionar produto no carrinho
                    self.__view.limpa_tela()
                    self.tela_cliente_adicionar_produto()
                    self.__view.exibe_pausa()
                case 4:
                    #remover produto do carrinho
                    self.__view.limpa_tela()
                    self.tela_cliente_remover_produto()
                    self.__view.exibe_pausa()
                case 5:
                    #finalizar pedido
                    self.__view.limpa_tela()
                    self.tela_cliente_finalizar_pedido()
                    self.__view.exibe_pausa()
                case 6:
                    self.__view.limpa_tela()
                    self.tela_cliente_pedidos()
                    self.__view.exibe_pausa()
                case _:
                    print("Opção inválida")

    def tela_loja_escolhe(self):
        self.__view.limpa_tela()
        self.__view.exibe_mensagem_lista_lojas()
        self.__lojasmanager.listar_lojas()
        id_loja = input("Digite o ID da loja que deseja entrar: ")
        if not self.__lojasmanager.logar_loja(id_loja):
            self.__view.exibe_falha()
            return        
        self.__view.exibe_sucesso()
        self.__view.exibe_pausa()
        self.tela_loja_menu()

    def tela_loja_menu(self):
        while True:
            self.__view.limpa_tela()
            self.__view.exibe_menu_vendedor(self.__lojasmanager.get_loja_logada())
            opcao = self.consiste(0,4)
            match opcao:
                case 0:
                    #voltar menu principal
                    self.__lojasmanager.deslogar_loja()
                    self.tela_volta_menu_principal()
                    self.__view.exibe_pausa()
                    break
                case 1:
                    #listar produtos
                    self.__view.limpa_tela()
                    self.tela_loja_lista_produtos()
                    self.__view.exibe_pausa()
                case 2:
                    #cadastrar produto
                    self.__view.limpa_tela()
                    self.tela_loja_cadastra_produto()
                    self.__view.exibe_pausa()
                case 3:
                    #excluir produto
                    self.__view.limpa_tela()
                    self.tela_loja_excluir_produto()
                    self.__view.exibe_pausa()
                case 4:
                    #listar pedidos
                    self.__view.limpa_tela()
                    self.tela_loja_listar_pedidos()
                    self.__view.exibe_pausa()
                case _:
                    print("Opção inválida")

    #AVALIAR SE FAZ SENTIDO
    def tela_administrador(self):
        while True:
            self.__view.limpa_tela()
            self.__view.exibe_menu_administrador()
            opcao = self.consiste(0,6)
            match opcao:
                case 0:
                    #voltar menu principal
                    self.tela_volta_menu_principal()
                    self.__view.exibe_pausa()
                    break
                case 1:
                    #listar lojas
                    self.__view.limpa_tela()
                    self.tela_administrador_listar_lojas()
                    self.__view.exibe_pausa()
                case 2:
                    #adicionar loja
                    self.__view.limpa_tela()
                    self.tela_administrador_cadastra_loja()
                    self.__view.exibe_pausa()
                case 3:
                    #remover loja
                    self.__view.limpa_tela()
                    self.tela_administrador_remove_loja()
                    self.__view.exibe_pausa()
                case 4:
                    #listar usuarios
                    self.__view.limpa_tela()
                    self.tela_administrador_lista_usuarios()
                    self.__view.exibe_pausa()
                case 5:
                    #remover usuario
                    self.__view.limpa_tela()
                    self.tela_administrador_remove_usuario()
                    self.__view.exibe_pausa()
                case 6:
                    #listar todos pedidos
                    self.__view.limpa_tela()
                    self.tela_administrador_lista_pedidos()
                    self.__view.exibe_pausa()
                
                case _:
                    print("Opção inválida")

    
    #menu cliente
    def tela_cliente_selecionar_loja(self):
        if self.__carrinho.quantidade_produtos() > 0:
            self.tela_cliente_aviso_carrinho()
            simnao = self.consiste(0,1)
            if simnao == 0:
                self.__view.exibe("Operação Cancelada!")
                self.__view.exibe_pausa()
                return
        
        self.__carrinho.limpar_carrinho()
        self.__view.limpa_tela()
        self.__view.exibe_mensagem_lista_lojas()
        self.__lojasmanager.listar_lojas()
        id_loja = input("Digite o ID da loja que deseja selecionar: ")
        
        self.__loja_cliente = self.__lojasmanager.buscar_loja(id_loja)

        if not self.__loja_cliente:
            self.__view.exibe_falha()
            return
        
        self.__view.exibe_sucesso()

    def tela_cliente_aviso_carrinho(self):
        self.__view.exibe_mensagem_aviso_itens_carrinho()        

    def tela_cliente_lista_carrinho(self):
        if not self.is_loja_selecionada():
            return
        
        self.__view.exibe_mensagem_lista_carrinho()
        self.__carrinho.listar_produtos()
        self.__view.exibe_valor_total(self.__carrinho.get_valor_total())

    def tela_cliente_adicionar_produto(self):
        if not self.is_loja_selecionada():
            return

        self.__view.exibe_mensagem_lista_produtos()
        self.__loja_cliente.listar_produtos()
        id_produto = input("Digite o ID do produto para adicionar ao carrinho: ")
        
        produto = self.__loja_cliente.buscar_produto(id_produto)
        
        if not produto:
            self.__view.exibe_falha()
            return

        if not self.__carrinho.adicionar_produto(produto):
            self.__view.exibe_falha()
            return        

        self.__view.exibe_sucesso()
    
    def tela_cliente_remover_produto(self):
        if not self.is_loja_selecionada():
            return

        self.__view.exibe_mensagem_lista_produtos()
        self.__carrinho.listar_produtos()
        id_produto = input("Digite o ID do produto para remover do carrinho: ")

        if not self.__carrinho.remover_produto(id_produto):
            self.__view.exibe_falha()
            return
        
        self.__view.exibe_sucesso()        
    
    def tela_cliente_finalizar_pedido(self):
        if not self.is_loja_selecionada():
            return

        if self.__carrinho.quantidade_produtos() == 0:
            self.__view.exibe_mensagem_carrinho_vazio()
            return  
        
        self.__view.limpa_tela()
        pedido = self.__carrinho.finalizar_pedido(self.__login.get_usuario_logado(),self.__loja_cliente)        
        if not self.__repopedidos.adiciona_pedido(pedido):
            self.__view.exibe_falha()
            return
        
        self.__view.exibe_sucesso()
    
    def tela_cliente_pedidos(self):
        self.__view.exibe_mensagem_lista_pedidos()

        pedidos = self.__repopedidos.pedidos_do_cliente(
            self.__login.get_usuario_logado()
        )

        if len(pedidos) == 0:
            self.__view.exibe("Nenhum pedido encontrado.")
            return

        for pedido in pedidos:
            print(pedido)

    def is_loja_selecionada(self):
        if not self.__loja_cliente:
            self.__view.exibe("Selecione uma loja primeiro.")
            return False
        return True


    #menu loja
    def tela_loja_lista_produtos(self):
        self.__view.exibe_mensagem_lista_produtos()
        self.__lojasmanager.get_loja_logada().listar_produtos()

    def tela_loja_cadastra_produto(self):
        self.__view.exibe_mensagem_cadastro_produto()
        nome_produto = input("Nome do produto: ")
        preco = input("Digite o preço do produto: ")
        if not self.__lojasmanager.get_loja_logada().adiciona_produto(nome_produto,preco):
            self.__view.exibe_falha()
            return
        self.__lojasmanager.salvardb()
        self.__view.exibe_sucesso()
    
    def tela_loja_excluir_produto(self):
        self.__view.exibe_mensagem_lista_produtos()
        self.__lojasmanager.get_loja_logada().listar_produtos()
        id_produto = input("Digite o ID do produto para remover da loja: ")
        if not self.__lojasmanager.get_loja_logada().remover_produto(id_produto):
            self.__view.exibe_falha()
            return
        self.__lojasmanager.salvardb()
        self.__view.exibe_sucesso()

    def tela_loja_listar_pedidos(self):
        self.__view.exibe_mensagem_loja_lista_pedidos()

        pedidos = self.__repopedidos.pedidos_da_loja(
            self.__lojasmanager.get_loja_logada()
        )

        if not pedidos:
            self.__view.exibe("Nenhum pedido encontrado.")
            return

        for pedido in pedidos:
            self.__view.exibe(pedido)


    #menu administrador    
    def tela_administrador_listar_lojas(self):
        self.__view.exibe_mensagem_lista_lojas()
        self.__lojasmanager.listar_lojas()

    def tela_administrador_cadastra_loja(self):
        self.__view.exibe_mensagem_cadastrar_loja()
        nome_loja = input("Nome da loja: ")
        if not self.__lojasmanager.adiciona_loja(Loja(nome_loja)):
            self.__view.exibe_falha()
            return
        self.__view.exibe_sucesso()

    def tela_administrador_remove_loja(self):
        self.__view.exibe_mensagem_lista_lojas()
        self.__lojasmanager.listar_lojas()
        id_produto = input("Digite o ID da loja que deseja remover: ")
        if not self.__lojasmanager.remover_loja(id_produto):
            self.__view.exibe_falha()
            return        
        self.__view.exibe_sucesso()   

    def tela_administrador_lista_usuarios(self):
        self.__view.exibe_mensagem_lista_usuarios()
        self.__login.listar_usuarios()

    def tela_administrador_remove_usuario(self):
        self.__view.exibe_mensagem_lista_usuarios()
        self.__login.listar_usuarios()
        nome_user = input("Digite o nome do usuário que deseja remover: ")
        if not self.__login.remover_usuario(nome_user):
            self.__view.exibe_falha()
            return        
        self.__view.exibe_sucesso()

    def tela_administrador_lista_pedidos(self):
        self.__view.exibe_mensagem_lista_pedidos()

        pedidos = self.__repopedidos.get_lista_pedidos()

        if not pedidos:
            self.__view.exibe("Nenhum pedido encontrado.")
            return

        for pedido in pedidos:
            self.__view.exibe(pedido)
            self.__view.exibe("=" * 55)


    #menus gerais
    def tela_volta_menu_principal(self):
        self.__view.exibe_voltando_menu_principal()

    def tela_sair(self):
        self.__view.exibe_mensagem_sair()


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



    