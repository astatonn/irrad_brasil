import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


print("Iniciando....")
# Carregar os dados do arquivo cache.csv
cache_data = pd.read_csv("data/cache.csv")

# Dicionário de regiões e seus respectivos estados
regioes_estados = {
    'Norte': ['RO', 'AC', 'AM', 'RR', 'PA', 'AP', 'TO'],
    'Nordeste': ['MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA'],
    'Sudeste': ['MG', 'ES', 'RJ', 'SP'],
    'Sul': ['PR', 'SC', 'RS'],
    'Centro-Oeste': ['MS', 'MT', 'GO', 'DF']
}

# Carregar o arquivo Shapefile dos estados do Brasil
estados_shapefile = "shapefile/BR_Municipios_2022.shp"
estados_data = gpd.read_file(estados_shapefile)

# Criar a janela e os componentes
window = tk.Tk()
window.title("IR Brasil")

# Exibir o Shapefile completo do Brasil na janela
fig, ax = plt.subplots(figsize=(6, 6))
estados_data.plot(ax=ax)
plt.title("Brasil")
plt.xticks([])
plt.yticks([])
plt.tight_layout()
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.LEFT)

# Opções de origem dos dados
origens = ["Brasil", "Estado", "Região", "Município"]

# Criar a lista suspensa (dropdown) para selecionar a origem dos dados
combo_origem = ttk.Combobox(window, values=origens)
combo_origem.pack(side=tk.TOP)
combo_origem.set("Escolha a origem dos dados")

# Criar a lista suspensa (dropdown) para selecionar o estado
combo_estados = ttk.Combobox(window, values=list(cache_data['State'].unique()))

# Criar a lista suspensa (dropdown) para selecionar a região
combo_regioes = ttk.Combobox(window, values=list(regioes_estados.keys()))

# Criar a lista suspensa (dropdown) para selecionar o município
combo_municipios = ttk.Combobox(window, values=list(cache_data['NM_MUN'].unique()))

# Botão para exibir a origem selecionada
button_exibir = tk.Button(window, text="Exibir")
button_exibir.pack(side=tk.TOP)

# Dados consolidados do estado selecionado
dados_consolidados = None

def exibir_origem():
    global dados_consolidados
    
    origem_escolhida = combo_origem.get()

    if origem_escolhida == "Brasil":
        # Exibir o Shapefile completo do Brasil
        ax.clear()
        estados_data.plot(ax=ax)
        plt.title("Brasil")
        canvas.draw()
        return

    estado_escolhido = combo_estados.get()
    if estado_escolhido != "":
        # Retornar se o estado escolhido for o mesmo estado já processado anteriormente
        print(dados_consolidados)
        if dados_consolidados is not None and estado_escolhido == dados_consolidados['State'].iloc[0]:
            return
        
        # Filtrar os dados para exibir apenas o estado escolhido
        estado_data = cache_data[cache_data['State'] == estado_escolhido]

        if not estado_data.empty:
            print("Carregando dados do estado escolhido")
            # Selecionar apenas as colunas numéricas
            colunas_numericas = ['H(h)_m', 'H(i_opt)_m', 'Hb(n)_m', 'T2m']
            dados_consolidados = estado_data.groupby(['year', 'month', 'State'])[colunas_numericas].mean().round(3)
            dados_consolidados = dados_consolidados.reset_index()
            dados_consolidados['State'] = estado_escolhido

            # Converter os nomes dos meses em valores numéricos
            meses_numericos = {
                'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
            }
            dados_consolidados['month'] = dados_consolidados['month'].map(meses_numericos)
            dados_consolidados = dados_consolidados.sort_values(['year', 'month'])

            # Converter o índice em um formato numérico
            dados_consolidados['data'] = pd.to_datetime(dados_consolidados[['year', 'month']].assign(day=1))
            dados_consolidados.set_index('data', inplace=True)

            # Criar uma nova figura e eixo para o gráfico
            ax.clear()
            ax.set_xlabel('Data (ano, mês)')
            ax.set_ylabel('Valores médios')
            ax.set_title(f"Dados Consolidados do Estado: {estado_escolhido}")
            
            # Exibir os dados consolidados em um gráfico
            for coluna in colunas_numericas:
                ax.plot(dados_consolidados.index, dados_consolidados[coluna], label=coluna)
            ax.legend('teste')
            canvas.draw()

            # Remover o conteúdo existente da tabela
            for item in table.get_children():
                table.delete(item)
            colunas_numericas.insert(0, 'year')
            colunas_numericas.insert(1, 'month')
            # Exibir tabela com informações consolidadas
            for i, row in dados_consolidados.iterrows():
                table.insert('', tk.END, values=tuple(row[col] for col in colunas_numericas))

        else:
            messagebox.showwarning("Aviso", f"Não há dados disponíveis para o estado {estado_escolhido}.")
    
    elif origem_escolhida == "Região":
        # Exibir a lista suspensa (dropdown) para selecionar a região
        combo_regioes.pack(side=tk.TOP)
        exibir_regiao()

    elif origem_escolhida == "Município":
        print("Carregando dados do Município escolhido")
        # Exibir a lista suspensa (dropdown) para selecionar o município
        combo_municipios.pack(side=tk.TOP)

        municipio_escolhido = combo_municipios.get()
        
        if municipio_escolhido != "":
            # Retornar se o município escolhido for o mesmo município já processado anteriormente
            if dados_consolidados is not None and municipio_escolhido == dados_consolidados['NM_MUN'].iloc[0]:
                return
            
            # Filtrar os dados para exibir apenas o município escolhido
            municipio_data = cache_data[cache_data['NM_MUN'] == municipio_escolhido]

            if not municipio_data.empty:
                # Selecionar apenas as colunas numéricas
                colunas_numericas = ['H(h)_m', 'H(i_opt)_m', 'Hb(n)_m', 'T2m']
                dados_consolidados_municipio = municipio_data.groupby(['year', 'month', 'NM_MUN'])[colunas_numericas].mean().round(3)
                dados_consolidados_municipio = dados_consolidados_municipio.reset_index()
                dados_consolidados_municipio['NM_MUN'] = municipio_escolhido

                # Converter os nomes dos meses em valores numéricos
                meses_numericos = {
                    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                    'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
                }
                dados_consolidados_municipio['month'] = dados_consolidados_municipio['month'].map(meses_numericos)
                dados_consolidados_municipio = dados_consolidados_municipio.sort_values(['year', 'month'])

                # Converter o índice em um formato numérico
                dados_consolidados_municipio['data'] = pd.to_datetime(dados_consolidados_municipio[['year', 'month']].assign(day=1))
                dados_consolidados_municipio.set_index('data', inplace=True)

                # Criar uma nova figura e eixo para o gráfico
                print(dados_consolidados_municipio)
                ax.clear()
                ax.set_xlabel('Data (ano, mês)')
                ax.set_ylabel('Valores médios')
                ax.set_title(f"Dados Consolidados do Município: {municipio_escolhido}")
                
                # Exibir os dados consolidados em um gráfico
                for coluna in colunas_numericas:
                    ax.plot(dados_consolidados_municipio.index, dados_consolidados_municipio[coluna], label=coluna)

                ax.legend()
                canvas.draw()

                # Remover o conteúdo existente da tabela
                for item in table.get_children():
                    table.delete(item)
                
                colunas_numericas.insert(0, 'year')
                colunas_numericas.insert(1, 'month')

                # Exibir tabela com informações consolidadas
                for i, row in dados_consolidados_municipio.iterrows():
                    table.insert('', tk.END, values=tuple(row[col] for col in colunas_numericas))

            else:
                messagebox.showwarning("Aviso", f"Não há dados disponíveis para o município {municipio_escolhido}.")
    
    else:
        messagebox.showwarning("Aviso", "Escolha uma origem válida.")


def exibir_regiao():
    regiao_escolhida = combo_regioes.get()
    if regiao_escolhida != "":
        # Filtrar os estados da região escolhida
        estados_regiao = regioes_estados[regiao_escolhida]

        # Filtrar os dados para exibir apenas os estados da região escolhida
        regiao_data = cache_data[cache_data['State'].isin(estados_regiao)]

        if not regiao_data.empty:
            # Selecionar apenas as colunas numéricas
            colunas_numericas = ['H(h)_m', 'H(i_opt)_m', 'Hb(n)_m', 'T2m']

            # Consolidar os dados por ano, mês e região
            dados_consolidados_regiao = regiao_data.groupby(['year', 'month', 'Region'])[colunas_numericas].mean().round(3)
            dados_consolidados_regiao = dados_consolidados_regiao.reset_index()

            # Converter os nomes dos meses em valores numéricos
            meses_numericos = {
                'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
            }
            dados_consolidados_regiao['month'] = dados_consolidados_regiao['month'].map(meses_numericos)
            dados_consolidados_regiao = dados_consolidados_regiao.sort_values(['year', 'month'])

            # Converter o índice em um formato numérico
            dados_consolidados_regiao['data'] = pd.to_datetime(dados_consolidados_regiao[['year', 'month']].assign(day=1))
            dados_consolidados_regiao.set_index('data', inplace=True)

            # Criar uma nova figura e eixo para o gráfico
            ax.clear()
            ax.set_xlabel('Data (ano, mês)')
            ax.set_ylabel('Valores médios')
            ax.set_title(f"Dados Consolidados da Região: {regiao_escolhida}")

            # Exibir os dados consolidados em um gráfico
            for coluna in colunas_numericas:
                ax.plot(dados_consolidados_regiao.index, dados_consolidados_regiao[coluna], label=coluna)

            ax.legend()
            canvas.draw()

            # Remover o conteúdo existente da tabela
            for item in table.get_children():
                table.delete(item)

            colunas_numericas.insert(0, 'year')
            colunas_numericas.insert(1, 'month')

            # Exibir tabela com informações consolidadas
            for i, row in dados_consolidados_regiao.iterrows():
                table.insert('', tk.END, values=tuple(row[col] for col in colunas_numericas))

        else:
            messagebox.showwarning("Aviso", f"Não há dados disponíveis para a região {regiao_escolhida}.")

def exibir_municipio():
    municipio_escolhido = combo_municipios.get()
    global dados_consolidados
    if municipio_escolhido != "":
        # Filtrar os dados para exibir apenas o município escolhido
        municipio_data = cache_data[cache_data['NM_MUN'] == municipio_escolhido]

        if not municipio_data.empty:
            # Selecionar apenas as colunas numéricas
            colunas_numericas = ['H(h)_m', 'H(i_opt)_m', 'Hb(n)_m', 'T2m']

            # Criar uma nova figura e eixo para o gráfico
            ax.clear()
            ax.set_xlabel('Data (ano, mês)')
            ax.set_ylabel('Valores médios')
            ax.set_title(f"Dados do Município: {municipio_escolhido}")

            # Exibir os dados do município em um gráfico
            for coluna in colunas_numericas:
                ax.plot(municipio_data['year'], municipio_data[coluna], label=coluna)

            ax.legend()
            canvas.draw()

            # Remover o conteúdo existente da tabela
            for item in table.get_children():
                table.delete(item)

            # Exibir tabela com informações do município
            for i, row in municipio_data.iterrows():
                table.insert('', tk.END, values=tuple(row[col] for col in colunas_numericas))

        else:
            messagebox.showwarning("Aviso", f"Não há dados disponíveis para o município {municipio_escolhido}.")


def exibir():
    exibir_origem()

button_exibir.config(command=exibir)
# Criar a lista suspensa (dropdown) para selecionar o estado
combo_estados = ttk.Combobox(window, values=list(cache_data['State'].unique()))

# Criar a lista suspensa (dropdown) para selecionar a região
combo_regioes = ttk.Combobox(window, values=list(regioes_estados.keys()))

# Criar a lista suspensa (dropdown) para selecionar o município
combo_municipios = ttk.Combobox(window, values=list(cache_data['NM_MUN'].unique()))

# Botão para exibir a origem selecionada
# button_exibir = tk.Button(window, text="Exibir", command=exibir_origem)
button_exibir.pack(side=tk.TOP)

def on_origem_selected(event):
    origem_escolhida = combo_origem.get()

    if origem_escolhida == "Brasil":
        combo_estados.pack_forget()
        combo_regioes.pack_forget()
        combo_municipios.pack_forget()
    elif origem_escolhida == "Estado":
        combo_estados.pack(side=tk.TOP)
        combo_regioes.pack_forget()
        combo_municipios.pack_forget()
    elif origem_escolhida == "Região":
        combo_estados.pack_forget()
        combo_regioes.pack(side=tk.TOP)
        combo_municipios.pack_forget()
    elif origem_escolhida == "Município":
        combo_estados.pack_forget()
        combo_regioes.pack_forget()
        combo_municipios.pack(side=tk.TOP)

combo_origem.bind("<<ComboboxSelected>>", on_origem_selected)


# Criar a tabela para exibir os dados
colunas_tabela = ['Ano','Mês', 'H(h)_m', 'H(i_opt)_m', 'Hb(n)_m', 'T2m']
table = ttk.Treeview(window, columns=colunas_tabela, show='headings')
style = ttk.Style()
style.configure("Treeview", rowheight=40)

# Configurar as colunas da tabela
for coluna in colunas_tabela:
    table.heading(coluna, text=coluna)
    table.column(coluna, width=70)

table.pack(side=tk.TOP)

texto = tk.Label(window, text='H(h)_m => Irradiation on horizontal plane (kWh/m2/mo) \n H(i_opt)_m => Irradiation on optimally inclined plane (kWh/m2/mo) \n Hb(n)_m => Monthly beam (direct) irradiation on a plane always normal to sun rays (kWh/m2/mo) \n T2m => Average of temperature (degree Celsius)')
texto.pack(side=tk.BOTTOM)

# Iniciar o loop da janela
window.mainloop()
