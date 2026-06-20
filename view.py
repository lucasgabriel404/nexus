import os

class View():
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
        print("2 - Entrar como lojista")
        print("3 - Entrar como administrador do sistema")
        print("0 - Sair")

    def exibe_login_cliente(self):
        print("\n   Login Cliente")
        print("-" * 55)

    def exibe_login_falhou(self):
        print("\nLogin falhou, usuario ou senha estão incorretos.")

    def exibe_cadastro_cliente(self):
        print("\n   Cadastro Cliente")
        print("-" * 55)

    def exibe_sucesso_cadastro(self):
        print("\nCadastro realizado com sucesso! Faça Login novamente com seus dados novos.")

    def exibe_falha_cadastro(self):
        print("\nCadastro falhou, usuario já existe.")

    def exibe_menu_cliente(self,loja,usuario):
        print(f"\n   {loja.get_nome() if loja else "Selecione uma Loja"} - {usuario.get_nome() if usuario else "Quebrou o Programa Somehow"} ")
        print(f"   Menu Cliente")
        print("-" * 55)
        print("1 - Trocar Loja")
        print("2 - Ver Carrinho")
        print("3 - Adcionar Produto no Carrinho")
        print("4 - Remover Produto do Carrinho")
        print("5 - Finalizar Pedido")
        print("6 - Meus Pedidos")
        print("0 - Voltar ao Menu Inicial")

    def exibe_menu_tipo_cliente(self):
        print("Tipo de cliente:")
        print("1 - Pessoa Física")
        print("2 - Pessoa Jurídica")
        print("0 - Voltar ao Menu Inicial")

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

    def exibe_menu_vendedor(self,loja):
        print(f"   {loja.get_nome() if loja else "Parabéns você quebrou o pograma :("}")
        print("   Menu Lojista")
        print("-" * 55)
        print("1 - Listar Produtos")
        print("2 - Cadastrar Produto")
        print("3 - Excluir Produto")
        print("4 - Listar Pedidos")
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
        print("1 - Listar Lojas")
        print("2 - Cadastrar Lojas")
        print("3 - Remover Lojas")
        print("4 - Listar Clientes")
        print("5 - Remover Cliente")
        print("6 - Listar Todos os Pedidos")
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

    def exibe_mensagem_cadastrar_loja(self):
        print("\n   Cadastrar Loja")
        print("-" * 55)

    def exibe_mensagem_lista_lojas(self):
        print("\n   Lista de Lojas")
        print("-" * 55)
    
    def exibe_mensagem_lista_usuarios(self):
        print("\n   Lista de Clientes")
        print("-" * 55)

    def exibe_mensagem_lista_pedidos(self):
        print("\n   Meus Pedidos")
        print("-" * 55)

    def exibe_mensagem_loja_lista_pedidos(self):
        print("\n   Lista de Pedidos")
        print("-" * 55)

    def exibe_mensagem_aviso_itens_carrinho(self):
        print("\n /!\  AVISO  /!\ ")
        print("-" * 55)
        print("Você tem itens adicionados no carrinho!")
        print("Trocar a loja vai esvaziar os seus itens salvos.\n")
        print("Deseja Continuar?")
        print("1 - Sim")
        print("0 - Não")
        
