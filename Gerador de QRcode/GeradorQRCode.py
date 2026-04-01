import flet as ft
import qrcode
import os
import sys # Necessário para achar os arquivos no .exe

# FUNÇÃO GPS: Faz o executável encontrar a imagem dentro dele mesmo
def resource_path(relative_path):
    try:
        # Pasta temporária do PyInstaller
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main(page: ft.Page):
    # configuracao da janela
    page.title = "Gerador de QR Code"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 800
    page.window_height = 500 # Aumentei um pouco para caber tudo elegante
    page.window_resizable = False
    page.window_maximizable = False

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # logo no topo (USANDO O GPS)
    logo_topo = ft.Image(
        src=resource_path("LogoSorriso.png"),
        width=140,
        height=140
    )

    # alternar tema
    def alternar_tema(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        page.update()

    botao_tema = ft.IconButton(
        icon=ft.Icons.BRIGHTNESS_6,
        on_click=alternar_tema
    )

    # inputs
    link_input = ft.TextField(label="Link", width=300)
    nome_input = ft.TextField(label="Nome do arquivo", width=300)
    resultado_texto = ft.Text(value="", text_align=ft.TextAlign.CENTER)

    # gerar qr code
    def gerar_qrcode(e):
        link = link_input.value.strip()
        nome = nome_input.value.strip()

        if not link or not nome:
            resultado_texto.value = "⚠️ Preencha os campos!"
            page.update()
            return

        try:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(link)
            qr.make(fit=True)

            img = qr.make_image(fill_color="green", back_color="black")

            # Salva na pasta onde o usuário abrir o .exe
            caminho = os.path.join(os.getcwd(), f"{nome}.png")
            img.save(caminho)

            resultado_texto.value = f"✅ Salvo em: {nome}.png"

        except Exception as ex:
            resultado_texto.value = f"❌ Erro: {str(ex)}"

        page.update()

    botao_gerar = ft.ElevatedButton(
        "Gerar QR Code",
        on_click=gerar_qrcode
    )

    # qr fixo github (gerado na hora)
    github_qr = qrcode.make("https://github.com/jonathanmalaquias/Portifolio.git")
    github_qr.save("github.png")

    qr_img = ft.Image(
        src="github.png", # Esse não precisa de resource_path pq é gerado na hora fora do exe
        width=90,
        height=90
    )

    # layout
    page.add(
        ft.Column(
            [
                logo_topo,
                botao_tema,
                link_input,
                nome_input,
                botao_gerar,
                resultado_texto,
                ft.Text("Meu Portfólio:", size=10),
                qr_img
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

if __name__ == "__main__":
    ft.app(target=main)