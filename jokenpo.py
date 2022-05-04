import random

#Definindo a função que fará o jogo
def pedra_papel_tesoura(escolha):
    opcoes = ['pedra', 'papel', 'tesoura']
    #Escolha do computador - dentre um dos índices da lista de opções
    escolha_computador = opcoes[random.randint(0,2)]
    
    #Definindo o ganhador do jogo
    
    if escolha_computador == "pedra":
        if escolha == "pedra":
            return print("Vocês empataram")
        elif escolha == "tesoura":
             return print(f"Você perdeu, {escolha_computador} vence {escolha}")
        else:
            return print(f"Você ganhou, {escolha} vence {escolha_computador}")
    elif escolha_computador == "papel":
        if escolha == "papel":
            return print("Vocês empataram")
        elif escolha == "tesoura":
             return print(f"Você ganhou, {escolha} vence {escolha_computador}")
        else:
            return print(f"Você perdeu, {escolha_computador} vence {escolha}")
    elif escolha_computador == "tesoura":
        if escolha == "tesoura":
            return print("Vocês empataram")
        elif escolha == "pedra":
             return print(f"Você ganhou, {escolha} vence {escolha_computador}")
        else:
            return print(f"Você perdeu, {escolha_computador} vence {escolha}")


opcoes = ['pedra', 'papel', 'tesoura']       
escolha = input("Digite sua escolha (pedra,papel,tesoura): ").lower()

#Validação do usuário
while escolha not in opcoes:
    escolha = input("Digite sua escolha novamente (pedra,papel,tesoura): ")

#Chama a função para o computador fazer uma escolha
pedra_papel_tesoura(escolha)

#Interação com o usuário
validacao = input("Gostaria de jogar novamente? (S/N)").upper()
while validacao == "S":
    escolha = input("Digite sua escolha (pedra,papel,tesoura): ").lower()
    pedra_papel_tesoura(escolha)
    validacao = input("Gostaria de jogar novamente? (S/N)").upper()
    
print("Fim de jogo")