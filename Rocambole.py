
import os
import json

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para carregar dados de um arquivo JSON
def carregar_dados(arquivo):
    try:
        with open(arquivo, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Função para salvar dados em um arquivo JSON
def salvar_dados(arquivo, dados):
    with open(arquivo, "w") as f:
        json.dump(dados, f, indent=4)

def registrar_pedido(cliente, pedido, preco):
    pedidos = carregar_dados("pedidos.json")
    if cliente not in pedidos:
        pedidos[cliente] = []
    pedidos[cliente].append({"pedido": pedido, "preco": preco})
    salvar_dados("pedidos.json", pedidos)

def cadastrar_usuario():
    usuarios = carregar_dados("usuarios.json")
    usuario = input("Nome de usuário: ")
    senha = input("Senha: ")
    if usuario in usuarios:
        print("Usuário já existe.")
    else:
        usuarios[usuario] = {"senha": senha, "saldo": 100.00}
        salvar_dados("usuarios.json", usuarios)
        print("Usuário cadastrado com sucesso!")

def autenticar_usuario():
    usuarios = carregar_dados("usuarios.json")
    usuario = input("Usuário: ")
    senha = input("Senha: ")
    if usuario in usuarios and usuarios[usuario]["senha"] == senha:
        return usuario, usuarios[usuario]["saldo"]
    else:
        print("Usuário ou senha inválidos.")
        return None, None

def menu_opcoes(opcoes):
    clear_screen()
    for i, opcao in enumerate(opcoes, 1):
        print(f"{i}. {opcao}")
    return input("Escolha uma opção: ")

def pagar_pedido(usuario, saldo, total_pedido):
    usuarios = carregar_dados("usuarios.json")
    pedidos = carregar_dados("pedidos.json")
    
    if saldo >= total_pedido:
        novo_saldo = saldo - total_pedido
        usuarios[usuario]["saldo"] = novo_saldo
        salvar_dados("usuarios.json", usuarios)

        # Remove os pedidos pagos
        if usuario in pedidos:
            pedidos.pop(usuario)
        salvar_dados("pedidos.json", pedidos)

        print(f"Pagamento de R${total_pedido:.2f} realizado! Saldo: R${novo_saldo:.2f}.")
        return novo_saldo  # Retorna o novo saldo
    else:
        print("Saldo insuficiente.")
        return saldo  # Retorna o saldo original

def main():
    cardapio = {'Broto': 15.00, 'Medina': 25.00, 'Grande': 35.00, 'Big': 60.00}

    while True:
        opcao = menu_opcoes(["Cadastrar Usuário", "Login", "Sair"])
        if opcao == "1":
            cadastrar_usuario()
            input("Usuário cadastrado! Pressione Enter...")
        elif opcao == "2":
            usuario, saldo = autenticar_usuario()
            if usuario:
                pedidos_a_pagar = []
                while True:
                    opcao_usuario = menu_opcoes(["Fazer um pedido", "Ver saldo", "Ver pedidos", "Pagar pedido", "Sair"])
                    if opcao_usuario == "1":
                        clear_screen()
                        print("Cardápio:")
                        for i, (item, preco) in enumerate(cardapio.items(), start=1):
                            print(f"{i}. {item} - R${preco:.2f}")
                        pedido_numero = input("Escolha um item ou 's' para sair: ")
                        if pedido_numero.isdigit() and 1 <= int(pedido_numero) <= len(cardapio):
                            item_escolhido = list(cardapio.keys())[int(pedido_numero) - 1]
                            preco_item = cardapio[item_escolhido]
                            pedidos_a_pagar.append(preco_item)
                            registrar_pedido(usuario, item_escolhido, preco_item)
                        elif pedido_numero in ["s", "sim"]:
                            continue
                        else:
                            print("Opção inválida.")
                    elif opcao_usuario == "2":
                        clear_screen()
                        print(f"Seu saldo é: R${saldo:.2f}")
                        input("Pressione Enter...")
                    elif opcao_usuario == "3":
                        clear_screen()
                        pedidos = carregar_dados("pedidos.json")
                        print("Seus pedidos:")
                        if usuario in pedidos:
                            for pedido in pedidos[usuario]:
                                print(f"{pedido['pedido']} - R${pedido['preco']:.2f}")
                        else:
                            print("Nenhum pedido encontrado.")
                        input("Pressione Enter...")
                    elif opcao_usuario == "4":
                        total_pedido = sum(pedidos_a_pagar)
                        print(f"Total a pagar: R${total_pedido:.2f}")
                        saldo = pagar_pedido(usuario, saldo, total_pedido)  # Atualiza o saldo após pagamento
                        pedidos_a_pagar.clear()
                        input("Pressione Enter...")
                    elif opcao_usuario == "5":
                        break
        elif opcao == "3":
            print("Saindo...")
            break

if __name__ == "__main__":
    main()
