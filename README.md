
<div align='center'>
<img src='img/header.jpg' alt='Apoie este trabalho' style='width:100%' >
</div>

# **Irradiação Solar Brasileira**
<div align='center'>
<img src='img/logo.png' alt='Logo Irrad Brasil' style='width:30%;'>
</div>

## Resumo
Este estudo tem como finalidade apresentar o método de obtenção de dados de irradiação solar no Brasil entre os anos de 2017 a 2020 e apresentar o programa _Irrad Brasil_. Criado para incentivar o uso de energias limpas e o apriomotamento das tecnologias.

## Fonte dos Dados

### Irradiação Solar
Os dados de Irradiação Solar foram obtidos da Comissão Europeia por meio da ferramenta PHOTOVOLTAIC GEOGRAPHICAL INFORMATION SYSTEM (PVGIS), utilizando como base as bases de dados PVGIS-ERA5 e PVGIS-SARAH2.

### Shapefiles
Os dados sobre os limites territoriais do Brasil e da região nordeste do Brasil foram obtidos da base de dados do Instituto Brasileiro de Geografia e Estatística (IBGE).

## Processamento dos Dados

### Da obtenção

Os dados foram obtidos por meio da linguagem de programação Python, utilizando requisições HTTP com uma progressão de latitude e longitude de 0.05 para ambos os parâmetros (aproximadamente 550m). Foram obtidos os dados mensais de 2017 a 2020 para a coordenada analisada, incluindo as seguintes informações:

- Irradiation on horizontal plane (kWh/m2/mo)
- Irradiation on optimally inclined plane (kWh/m2/mo)
- Monthly beam (direct) irradiation on a plane always normal to sun rays (kWh/m2/mo)
- 24 hour average of temperature (degree Celsius)

Os arquivos resultantes das requisições foram salvos com a extensão .csv, seguindo o formato dados_{latitude}_{longitude}.csv. Em seguida, um novo script em Python foi criado para, a partir do Shapefile do Brasil fornecido pelo IBGE, excluir os arquivos que não estavam dentro dos limites geográficos do país. Esse script também adicionou duas novas colunas aos dados obtidos: Região e Estado.

Posteriormente, os dados foram consolidados em um único arquivo .csv para serem comparados com os limites municipais usando o shapefile dos municípios do Brasil. Nesse processo, foi adicionada ao dataframe uma nova coluna com o nome da cidade representada pela coordenada analisada.

## Usando o software

### Requisitos 
- Python 3.x

### Instalação
- Baixe os arquivos de .csv <a href='https://drive.google.com/drive/folders/1krlZj5JAbxSn427i0npcilFOY2KtF8Ym?usp=drive_link'>aqui</a> e salve na pasta **data**.
- Baixe os shapefiles do IBGE <a href='https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2022/Brasil/BR/BR_Municipios_2022.zip'>aqui</a> e extraia todos os arquivos salve na pasta **shapefile**.

Clone o código: ```git clone https://github.com/astatonn/irrad_brasil```

Instale as dependências: ```pip install -r requirements.txt```

Execute o arquivo irrad_brasil.py: ```python3 irrad_brasil.py```

### Uso
Você pode visualizar os dados filtrando por região, estado ou município.
<br />
<br />
<img src='img/IR%20Brasil.png' style='width:49%'>
<img src='img/IR%20Brasil%202.png' style='width:49%'>
<img src='img/IR%20Brasil%203.png' style='width:49%'>
<img src='img/IR%20Brasil%204.png' style='width:49%'>

## Melhorias / Bugs
- [ ] Exportar gráficos
- [ ] Shapefile não carrega junto com o gráfico 
- [ ] Inserir pesquisa assistida
- [ ] Programa não finaliza corretamente  

Para atualizar essa lista, crie um novo tópico de discussão.

## Referências

> EUROPEAN COMMSION. Photovoltaic Geographical Information System, 2023. Disponível em: https://re.jrc.ec.europa.eu/pvg_tools/en/. Acesso em: 09 de junho de 2023.
> INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA. Malhas Territoriais, 2022. Disponível em: https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/15774-malhas.html. Acesso em: 09 de junho de 2023.

## Contato 
<p align="left">
  <a href="mailto:lucas.lima.rk@gmail.com" alt="Gmail">
  <img src="https://img.shields.io/badge/-Gmail-FF0000?style=flat-square&labelColor=FF0000&logo=gmail&logoColor=white&link=LINK-DO-SEU-EMAIL" /></a><a href="https://www.linkedin.com/in/lucas-lima-477377a5/" alt="Linkedin">
  <img src="https://img.shields.io/badge/-Linkedin-0e76a8?style=flat-square&logo=Linkedin&logoColor=white&link=LINK-DO-SEU-LINKEDIN" /></a>
</p>  

<div align="center">
  <br/>
    <div>
        <sub>Este projeto utilizou Git Flow como modelo de trabalho</sub> <br />
      <sub>Copyright © 2023 - <a href="https://github.com/astatonn">astatonn</sub></a>
    </div>
    <br/>
    
</div>