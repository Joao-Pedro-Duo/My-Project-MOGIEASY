# Importar o App, Builder 
# Criar o Aplicativo
# Criar a função build

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty, BooleanProperty, StringProperty
from kivy.lang import Builder
from informacao_onibusV1 import onibus

class TelaHome(Screen):
    # controla se está no modo claro ou escuro
    dark_mode = BooleanProperty(False)

    def toggle_theme(self):
        app = App.get_running_app()
        if app.dark_mode:
            # já esta no modo escuro, muda para o claro
            Window.clearcolor = (1,1,1,1) # Fundo Branco
            app.text_color = (0,0,0,1) # Escrita Preta
            app.dark_mode = False
        else:
            # já está no modo claro, muda para o escuro
            Window.clearcolor = (0,0,0,1) # Fundo preto
            app.text_color = (1,1,1,1) # Escrita branca
            app.dark_mode = True

    

class TelaHorarios(Screen):
    def on_enter(self):
        # Carrega os terminais ao entrar na tela
        terminais = list(onibus.keys())

        # acessando os spinners que estão dentro da SubTelaHorarios
        sub_horarios = self.ids.sub_manager.get_screen("sub_horarios")
        sub_horarios.ids.terminal_spinner.values = terminais

        # Selecionar os botoes Terminal e Linha
        sub_horarios.ids.terminal_spinner.bind(text = self.selecionar_terminal)
        sub_horarios.ids.linha_spinner.bind(text = self.selecionar_linha)

    def selecionar_terminal(self, spinner, terminal_nome):
        sub_horarios = self.ids.sub_manager.get_screen("sub_horarios")
        sub_rotas = self.ids.sub_manager.get_screen("sub_rotas")


        if not terminal_nome or terminal_nome not in onibus:
            sub_horarios.ids.linha_spinner.values = []
            sub_horarios.ids.info_label.text = "Selecione um terminal válido"
            sub_rotas.ids.rota_label.text = ""
            return 
        
        # Preencher linhas do terminal
        linhas = list(onibus[terminal_nome].keys())
        sub_horarios.ids.linha_spinner.values = linhas
        sub_horarios.ids.info_label.text = "Selecione uma linha"
        sub_rotas.ids.rota_label.text = ""

    def selecionar_linha(self, spinner, linha_nome):
        sub_horarios = self.ids.sub_manager.get_screen("sub_horarios")
        sub_rotas = self.ids.sub_manager.get_screen("sub_rotas")


        terminal = sub_horarios.ids.terminal_spinner.text
        if terminal not in onibus or linha_nome not in onibus[terminal]:
            return


        dados_linha = onibus[terminal][linha_nome]


        # Mostrar Horarios (prioriza Segunda e Sexta)
        horarios = []
        if "Horários: Segunda/Sexta" in dados_linha:
            h = dados_linha["Horários: Segunda/Sexta"]
            terminal_h = h.get("terminal", [])
            bairro_h = h.get("bairro/circular", [])
            horarios.append(F"Terminal: {', '.join(terminal_h[:5])} ...") # mostra só os 5 primeiros
            if bairro_h:
                horarios.append(F"Bairro/Circular: {', '.join(bairro_h[:5])} ...")
        else:
            horarios.append("Horários não disponíveis")

        sub_horarios.ids.info_label.text = "\n".join(horarios)


        # Mostrar as Rotas
        rotas = []
        for chave, rota in dados_linha.items():
            if chave.startswith("Rota"):
                rotas.append(F"{chave}: " + " => ".join(rota[:6]) + " ...")
        if rotas:
            sub_rotas.ids.rota_label.text = "\n\n".join(rotas)
        else:
            sub_rotas.ids.rota_label.text = "Rota não disponível"

class SubTelaHorarios(Screen):
    pass

class SubTelaRotas(Screen):
    pass

class TelaMapa(Screen):
    pass


class TelaPagamentos(Screen):
    pass


class Gerenciador(ScreenManager):
    pass


class MOGIEASY(App):
    dark_mode = BooleanProperty(False)  # controla se está em dark mode
    text_color = ListProperty([0, 0, 0, 1])  # cor padrão do texto (preto) 

    def build(self):
        self.title = "MOGIEASY"
        Window.clearcolor = (1, 1, 1, 1)  # começa com fundo branco

        return Builder.load_file("interfaceV1.kv")    
    
    def mudar_tela(self, nome_tela):
        self.root.current = nome_tela



if __name__ == "__main__":
    MOGIEASY().run()
