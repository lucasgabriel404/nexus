import os

class Menu():
    def exibe_banner(self):
        NEXUS_LOGO = r"""
     _   _ _______  ___   _ ____
    | \ | | ____\ \/ / | | / ___|
    |  \| |  _|  \  /| | | \___ \
    | |\  | |___ /  \| |_| |___) |
    |_| \_|_____/_/\_\___/|____/
    """
        print(NEXUS_LOGO)
        print("   Materiais de Construção  -  Orçamento Inteligente")
        print("   Equipe: Thais  -  Lucas M.  -  Yahgo  -  Lucas G.")
        print("-" * 55)

    def exibe_menu_inicial(self):
        print("1 - Entrar como cliente")
        print("2 - Entrar como vendedor")
        print("3 - Entrar como administrador")
        print("0 - Sair")

    def exibe_menu_cliente(self):
        print("\n   Menu Cliente")
        print("-" * 55)
        print("1 - Ver Carrinho")
        print("2 - Adcionar Produto no Carrinho")
        print("3 - Remover Produto do Carrinho")
        print("4 - Finalizar Pedido")
        print("0 - Voltar ao Menu Inicial")

    def exibe_menu_tipo_cliente(self):
        print("Tipo de cliente:")
        print("1 - Pessoa Física")
        print("2 - Pessoa Jurídica")

    def exibe_mensagem_cadastro_cpf(self):
        print("\n   Cadastro Cliente Pessoa Física")
        print("-" * 55)

    def exibe_mensagem_cadastro_cnpj(self):
        print("\n   Cadastro Cliente Pessoa Jurídica")
        print("-" * 55)

    def exibe_mensagem_lista_carrinho(self):
        print("\n   Lista Produtos no Carrinho")
        print("-" * 55)

    def exibe_mensagem_remover_produto(self):
        print("\n   Lista Produtos no Carrinho")
        print("-" * 55)

    def exibe_mensagem_carrinho_vazio(self):
        print("O carrinho está vazio! Não foi possível fechar o pedido.")

    def exibe_mensagem_pedido_concluido(self):
        print("Pedido concluído com sucesso!")

    def exibe_menu_vendedor(self):
        print("\n   Menu Vendedor")
        print("-" * 55)
        print("1 - Listar Produtos")
        print("2 - Cadastrar Produto")
        print("3 - Excluir Produto")
        print("0 - Sair")

    def exibe_mensagem_cadastro_produto(self):
        print("\n   Cadastro Produto")
        print("-" * 55)

    def exibe_mensagem_lista_produtos(self):
        print("\n   Lista de Produtos")
        print("-" * 55)

    def exibe_menu_administrador(self):
        print("\n   Menu Administrador")
        print("-" * 55)
        print("1 - Listar Pedidos")
        print("2 - Consultar Pedidos por ID")
        print("0 - Sair")

    def exibe_mensagem_sair(self):
        print("Até Logo.")

    def exibe_voltando_menu_principal(self):
        print("Voltando ao menu anterior...")

    def exibe_sucesso(self):
        print("Operação realizada com sucesso!")
    
    def exibe_falha(self):
        print("A operação falhou!")

    def exibe_valor_total(self,valor):
        print("-" * 55)
        print(f"VALOR TOTAL:    R${valor:.2f}")
    
    def exibe_pausa(self):
        input("\nPressione ENTER para continuar...")
    
    def limpa_tela(self):
        os.system("clear") 

    def exibe(self, objeto):
        print(objeto)