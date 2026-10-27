import random

import FreeSimpleGUI as sg


LINHAS = 6
COLUNAS = 7

COR_TABULEIRO = "#176B87"
COR_VAZIA = "#DCE7EB"
COR_JOGADOR = "#E34B4B"
COR_COMPUTADOR = "#F4C542"


def criar_tabuleiro():
    return [[None for _ in range(COLUNAS)] for _ in range(LINHAS)]


def inserir_ficha(tabuleiro, coluna, jogador):
    if not 0 <= coluna < COLUNAS:
        return None

    for linha in range(LINHAS - 1, -1, -1):
        if tabuleiro[linha][coluna] is None:
            tabuleiro[linha][coluna] = jogador
            return linha

    return None


def verificar_vitoria(tabuleiro, jogador):
    direcoes = ((0, 1), (1, 0), (1, 1), (1, -1))

    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            if tabuleiro[linha][coluna] != jogador:
                continue

            for delta_linha, delta_coluna in direcoes:
                final_linha = linha + 3 * delta_linha
                final_coluna = coluna + 3 * delta_coluna
                if not (0 <= final_linha < LINHAS and 0 <= final_coluna < COLUNAS):
                    continue

                if all(
                    tabuleiro[linha + passo * delta_linha][coluna + passo * delta_coluna]
                    == jogador
                    for passo in range(1, 4)
                ):
                    return True

    return False


def tabuleiro_cheio(tabuleiro):
    return all(tabuleiro[0][coluna] is not None for coluna in range(COLUNAS))


def desenhar_tabuleiro(window, tabuleiro):
    cores = {
        None: COR_VAZIA,
        1: COR_JOGADOR,
        2: COR_COMPUTADOR,
    }

    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            window[f"-CELL-{linha}-{coluna}-"].update(
                text_color=cores[tabuleiro[linha][coluna]]
            )


def criar_layout():
    seletores = [
        sg.Button(
            str(coluna + 1),
            key=f"-COL-{coluna}-",
            size=(4, 1),
            pad=(3, 4),
        )
        for coluna in range(COLUNAS)
    ]
    linhas_tabuleiro = [
        [
            sg.Text(
                "●",
                key=f"-CELL-{linha}-{coluna}-",
                size=(3, 1),
                font=("Arial", 24),
                justification="center",
                text_color=COR_VAZIA,
                background_color=COR_TABULEIRO,
                pad=(2, 1),
            )
            for coluna in range(COLUNAS)
        ]
        for linha in range(LINHAS)
    ]

    return [
        [
            sg.Text(
                "CONNECT FOUR",
                font=("Arial", 22, "bold"),
                text_color="#F5F7F8",
            )
        ],
        [sg.Text("Sua vez", key="-STATUS-", size=(30, 1), font=("Arial", 12))],
        [sg.Column([seletores, *linhas_tabuleiro], element_justification="center")],
        [
            sg.Button("Novo jogo", key="-RESET-"),
            sg.Button("Sair", key="-EXIT-"),
        ],
    ]


def main():
    sg.theme("DarkBlue3")
    window = sg.Window(
        "Connect Four",
        criar_layout(),
        element_justification="center",
        finalize=True,
    )
    tabuleiro = criar_tabuleiro()
    jogo_encerrado = False
    desenhar_tabuleiro(window, tabuleiro)

    while True:
        evento, _ = window.read()

        if evento in (sg.WIN_CLOSED, "-EXIT-"):
            break

        if evento == "-RESET-":
            tabuleiro = criar_tabuleiro()
            jogo_encerrado = False
            window["-STATUS-"].update("Sua vez")
            desenhar_tabuleiro(window, tabuleiro)
            continue

        if jogo_encerrado or not isinstance(evento, str) or not evento.startswith("-COL-"):
            continue

        coluna = int(evento[5:-1])
        if inserir_ficha(tabuleiro, coluna, 1) is None:
            window["-STATUS-"].update("Coluna cheia. Escolha outra.")
            continue

        desenhar_tabuleiro(window, tabuleiro)
        if verificar_vitoria(tabuleiro, 1):
            window["-STATUS-"].update("Você venceu!")
            jogo_encerrado = True
            continue

        if tabuleiro_cheio(tabuleiro):
            window["-STATUS-"].update("Empate!")
            jogo_encerrado = True
            continue

        colunas_disponiveis = [
            coluna for coluna in range(COLUNAS) if tabuleiro[0][coluna] is None
        ]
        coluna_computador = random.choice(colunas_disponiveis)
        inserir_ficha(tabuleiro, coluna_computador, 2)
        desenhar_tabuleiro(window, tabuleiro)

        if verificar_vitoria(tabuleiro, 2):
            window["-STATUS-"].update("O computador venceu.")
            jogo_encerrado = True
        elif tabuleiro_cheio(tabuleiro):
            window["-STATUS-"].update("Empate!")
            jogo_encerrado = True
        else:
            window["-STATUS-"].update("Sua vez")

    window.close()


if __name__ == "__main__":
    main()