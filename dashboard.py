##################################################
#################### DASHBOARD APOSTAS
#################### Guilherme L. Nascimento 
##################################################

from dash import Dash, html, dcc, Input, Output, State, ctx
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from datetime import date, datetime
import time
import math

from funcoes import relatorio_dbVazio, relatorio_db, mensagem
from graficos import graficoBanca, graficoAproveitamentoDiario, graficoAproveitamentoGeral

########### ########### ###########
########### CONFIGURAÇÕES DO APP
########### ########### ###########

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], suppress_callback_exceptions=True)

########### ########### ###########
########### BASE DE DADOS 
########### ########### ###########

df_apostas = pd.read_excel(r"E:\Programação\Python\Projetos\Dashboard Apostas\db_apostas.xlsx")
df_parametros = pd.read_excel(r"E:\Programação\Python\Projetos\Dashboard Apostas\db_parametros.xlsx")

########### ########### ###########
########### VARIÁVEIS GLOBAIS
########### ########### ###########

# Dummy data para declaração de figuras

dummy_data_x = ['01/01/01']
dummy_data_y = ['100']

# Modal

lista_esportes = list(df_parametros["Esporte"].dropna())
lista_tipo = list(df_parametros["Tipo"].dropna())
lista_resultado = list(df_parametros["Resultado"].dropna())
lista_finalizacao = list(df_parametros["Finalizacão"].dropna())

# Cores

cores = {
    'background': 'rgb(6, 6, 6)',
    'background2': 'rgb(40, 40, 40)',
    'text': 'rgb(255, 255, 255)',
    'col_acerto': 'rgb(49, 252, 195)',
    'col_erro': 'rgb(159, 8, 201)',
    'col_retornada': 'rgb(195, 195, 17)',
    'linha_grafico': 'rgb(49, 252, 195)',
    'marker_grafico': 'rgb(159, 8, 201)',
    'grade':'rgb(100, 100, 100)'
}

########### ########### ###########
########### CONFIGURAÇÕES DOS GRÁFICOS
########### ########### ###########

# Banca

fig_banca = graficoBanca(df_apostas, dummy_data_x, dummy_data_y, cores)

# Diario

fig_aproveitamentoDiario = graficoAproveitamentoDiario(df_apostas, cores)

# Geral

fig_aproveitamentoGeral = graficoAproveitamentoGeral(df_apostas, cores)

########### ########### ###########
########### LAYOUT
########### ########### ###########

app.layout = html.Div(
    children=[
        dbc.Row([
            dbc.Col([
                html.H4(
                    'DASHBOARD DE APOSTAS',
                    id = 'id_title_header',
                    className="app-header",
                    style={
                        'textAlign': 'center',
                        "margin-top": "10px",
                        "margin-bottom": "20px"
                    },
                ),
                dbc.Card([
                    dbc.CardHeader(
                        html.H5(
                            'Banca inicial:',
                            className="card-title",
                            style={
                                'textAlign': 'center',
                            },
                        )
                    ),
                    dbc.CardBody([
                        html.H2(
                            '',
                            className="card-text",
                            id = 'id_card_bancaInicial',
                            style={
                                'textAlign': 'center',
                            },
                        )       
                    ]),
                ], 
                style={
                    #'textAlign': 'center',
                    "margin-top": "10px"
                }
                ),
                dbc.Card([
                    dbc.CardHeader(
                        html.H5(
                            'Banca atual:',
                            className="card-title",
                            style={
                                'textAlign': 'center',
                            },
                        ),
                    ),
                    dbc.CardBody([
                        html.H2(
                            '',
                            id='id_card_bancaAtual',
                            className="card-text",
                            style={
                                'textAlign': 'center',
                            },
                        )       
                    ]),
                ], 
                style={
                    #'textAlign': 'center',
                    "margin-top": "10px"
                }
                ),
                dbc.Card([
                    dbc.CardHeader(
                        html.H5(
                            'Saldo:',
                            className="card-title",
                            style={
                                'textAlign': 'center',
                            },
                        ),
                    ),
                    dbc.CardBody([
                        html.H2(
                            '',
                            id='id_card_saldo',
                            className="card-text",
                            style={
                                'textAlign': 'center',
                            },
                        )       
                    ]),
                ], 
                style={
                    #'textAlign': 'center',
                    "margin-top": "10px"
                }
                ),
                dbc.Card([
                    dbc.CardHeader(
                        html.H5(
                            'ROI:',
                            className="card-title",
                            style={
                                'textAlign': 'center',
                            },
                        ),
                    ),
                    dbc.CardBody([
                        html.H2(
                            '',
                            id='id_card_roi',
                            className="card-text",
                            style={
                                'textAlign': 'center',
                            },
                        )       
                    ]),
                ], 
                style={
                    #'textAlign': 'center',
                    "margin-top": "10px"
                }
                ),
                html.Div(  
                    dbc.Button(
                        "Inserir nova aposta", 
                        id="id_botao_novaApostaOpen", 
                        n_clicks=0,
                        size='lg',
                        color="dark", 
                        className="me-1"
                    ),
                    className="d-grid gap-2",
                    style={
                        'textAlign': 'center',
                        "margin-top": "10px"
                    }
                ),
                dbc.Modal([
                        dbc.ModalHeader(
                            dbc.ModalTitle("Adicionar aposta:"),
                            close_button=False
                        ),
                        dbc.ModalBody([
                            html.H6(
                                'Data:',
                                style={
                                    'textAlign': 'left',
                                },
                            ),
                            dcc.DatePickerSingle(
                                id='id_calendario_novaAposta',
                                calendar_orientation='vertical',
                                placeholder='Select a date',
                                display_format='D/M/Y',
                                min_date_allowed=date(2022, 1, 20),
                                max_date_allowed=date.today(),
                                date=date.today(),
                                style={
                                    'color':'black',
                                    'background-color': cores['background'],
                                    "margin-top": "5px",
                                }
                            ),   
                            html.H6(
                                'Esporte:',
                                style={
                                    'textAlign': 'left',
                                    "margin-top": "5px",
                                },
                            ),
                            html.Div([                           
                                dcc.Dropdown(
                                    lista_esportes, 
                                    #value='Todas', 
                                    id='id_dpd_novaApostaEsportes',
                                    placeholder="Selecione um esporte...",
                                    style={
                                        'color':'black',
                                        #'background-color': cores['background'],
                                        "margin-top": "10px"
                                    }
                                ),
                            ],
                            id='id_div_novaApostaEsportes'
                            ),
                            html.H6(
                                'Tipo da aposta:',
                                style={
                                    'textAlign': 'left',
                                    "margin-top": "5px",
                                },
                            ),
                            dcc.Dropdown(
                                lista_tipo, 
                                #value='Todas', 
                                id='id_dpd_novaApostaTipo',
                                placeholder="Selecione o tipo...",
                                style={
                                    'color':'black',
                                    #'background-color': cores['background'],
                                    "margin-top": "10px"
                                }
                            ),
                            html.H6(
                                'Investimento:',
                                style={
                                    'textAlign': 'left',
                                    "margin-top": "5px",
                                },
                            ),
                            dbc.Input(
                                id='id_input_novaApostaInvestimento',
                                type="number",
                                min=0,
                                placeholder="Insira o valor investido...",
                            ),
                            html.H6(
                                'Odd:',
                                style={
                                    'textAlign': 'left',
                                    "margin-top": "5px",
                                },
                            ),
                            dbc.Input(
                                #placeholder="Amount", 
                                id='id_input_novaApostaOdd',
                                type="number",
                                min=0,
                                placeholder="Insira o valor da odd...",
                            ),
                            html.H6(
                                'Resultado:',
                                style={
                                    'textAlign': 'left',
                                    "margin-top": "5px",
                                },
                            ),
                            dcc.Dropdown(
                                lista_resultado, 
                                id='id_dpd_novaApostaResultado',
                                placeholder="Selecione o resultado...",
                                style={
                                    'color':'black',
                                    #'background-color': cores['background'],
                                    "margin-top": "10px"
                                }
                            ),
                            html.H6(
                                'Método de finalização:',
                                style={
                                    'textAlign': 'left',
                                    "margin-top": "5px",
                                },
                            ),
                            dcc.Dropdown(
                                lista_finalizacao, 
                                id='id_dpd_novaApostaFinalizacao',
                                placeholder="Selecione o método...",
                                style={
                                    'color':'black',
                                    #'background-color': cores['background'],
                                    "margin-top": "10px"
                                }
                            ),
                            dbc.Collapse([
                                html.H6(
                                    'Valor retirado:',
                                    style={
                                        'textAlign': 'left',
                                        "margin-top": "5px",
                                    },
                                ),
                                dbc.Input(
                                    id='id_input_novaApostaRetirada',
                                    type="number",
                                    min=0,
                                    placeholder="Insira o valor retirado...",
                                )],
                                id="id_collapse_novaApostaRetirada",
                                is_open=False,
                            ),
                            html.Div([
                                    dbc.Button(
                                        "Inserir aposta", 
                                        id="id_botao_novaApostaInserir", 
                                        className="ms-auto", 
                                        n_clicks=0,
                                        disabled=False,
                                        size='lg',
                                        color="dark", 
                                    ),
                                    dbc.Alert(
                                        "",
                                        id="id_alerta_novaApostaInserir",
                                        dismissable=True,
                                        fade=False,
                                        is_open=True,
                                        duration=2000,
                                        style={
                                            'textAlign': 'center',
                                            "margin-top": "20px",
                                        },
                                        color='success'
                                    ),
                                ],
                                style={
                                    'textAlign': 'center',
                                    "margin-top": "40px",
                                    "margin-bottom": "20px"
                                },
                            ),
                        ]),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Fechar", 
                                id="id_botao_novaApostaClose", 
                                className="ms-auto", 
                                n_clicks=0,
                                color="dark", 
                                # className="me-1"
                            )
                        ),
                    ],
                    id="id_modal_novaAposta",
                    is_open=False,
                    centered=True,
                    size="lg",
                    backdrop="static"
                ),
                html.Div(  
                    dbc.Button(
                        "Configurações  do dashboard", 
                        id="id_botao_configOpen", 
                        n_clicks=0,
                        size='lg',
                        color="dark", 
                        className="me-1"
                    ),
                    className="d-grid gap-2",
                    style={
                        'textAlign': 'center',
                        "margin-top": "10px"
                    }
                ),
                dbc.Modal([
                        dbc.ModalHeader(
                            dbc.ModalTitle("Configurações do dashboard:"),
                            close_button=False
                        ),
                        dbc.ModalBody([
                            html.H6(
                                'Inserir novo esporte:',
                                style={
                                    'textAlign': 'left',
                                },
                            ),
                            dbc.Input(
                                id='id_input_configEsporte',
                                type="text",
                                min=0,
                                placeholder="Insira o nome do esporte...",
                            ),
                            html.Div([
                                dbc.Button(
                                    "Inserir esporte", 
                                    id="id_botao_configInserirEsporte", 
                                    className="ms-auto", 
                                    n_clicks=0,
                                    color="dark", 
                                    # className="me-1"
                                    style={
                                        'textAlign': 'center',
                                        "margin-top": "5px",
                                    },
                                ),
                                dbc.Alert(
                                    "",
                                    id="id_alerta_configEsporte",
                                    dismissable=True,
                                    fade=False,
                                    is_open=False,
                                    duration=2000,
                                    style={
                                        'textAlign': 'center',
                                        "margin-top": "20px",
                                    },
                                    color='success'
                                ),
                            ],
                            style={
                                'textAlign': 'center',
                                "margin-top": "10px",
                                "margin-bottom": "20px"
                            },
                            ),
                            html.H6(
                                'Definir valor para a banca inicial:',
                                style={
                                    'textAlign': 'left',
                                },
                            ),
                            dbc.Input(
                                id='id_input_configBancaInicial',
                                type="number",
                                min=0,
                                placeholder="Insira o valor da banca inicial...",
                            ),
                            html.Div([
                                dbc.Button(
                                    "Inserir banca inicial", 
                                    id="id_botao_configBancaInicial", 
                                    className="ms-auto", 
                                    n_clicks=0,
                                    color="dark", 
                                    # className="me-1"
                                    style={
                                        'textAlign': 'center',
                                        "margin-top": "5px",
                                    },
                                ),
                                dbc.Alert(
                                    "",
                                    id="id_alerta_configBancaInicial",
                                    dismissable=True,
                                    fade=False,
                                    is_open=False,
                                    duration=2000,
                                    style={
                                        'textAlign': 'center',
                                        "margin-top": "20px",
                                    },
                                    color='success'
                                ),
                            ],
                            style={
                                'textAlign': 'center',
                                "margin-top": "10px",
                                "margin-bottom": "20px"
                            },
                            )
                        ]),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Fechar", 
                                id="id_botao_configClose", 
                                className="ms-auto", 
                                n_clicks=0,
                                color="dark", 
                                # className="me-1"
                            )
                        ),
                    ],
                    id="id_modal_config",
                    is_open=False,
                    centered=True,
                    size="lg",
                    backdrop="static"
                ),
            ], md=2),
            dbc.Col([
                dbc.Row([
                    dbc.Card([
                        dbc.CardHeader(
                            html.H5(
                                'Banca',
                                className="card-title",
                                style={
                                    'textAlign': 'center',
                                    "margin-top": "10px"
                                }
                            ),
                        ),
                        dbc.CardBody([
                            dcc.Graph(
                            id='id_graf_banca',
                            figure=fig_banca
                            ),
                        ])
                    ], 
                    style={
                        #'textAlign': 'center',
                        "margin-top": "10px"
                    }
                    ), 
                ]),
                dbc.Row([
                    dbc.Card([
                        dbc.CardHeader([
                            dbc.Tabs([
                                dbc.Tab(
                                    label="Análise diária", 
                                    tab_id="id_tab_abaDiaria",
                                    #active_tab_style={"textTransform": "uppercase"},
                                ),
                                dbc.Tab(
                                    label="Análise geral", 
                                    tab_id="id_tab_abaGeral",
                                    #active_tab_style={"textTransform": "uppercase"},
                                    active_tab_class_name={"backgroundColor": cores['background2']}
                                )
                            ],
                            id="id_tab_abas",
                            active_tab="id_tab_abaDiaria"
                            )  
                        ]),
                        dbc.CardBody([
                            html.Div(
                                children='',
                                id="id_div_abasConteudo", 
                                className="card-text"
                            )
                        ])
                    ], 
                    style={
                        #'textAlign': 'center',
                        "margin-top": "10px"
                    }
                    )
                ])
            ], md=10)
        ])
    ], 
    style={
        "margin": '10px 20px 20px 20px'
    }
)

########### ########### ###########
########## CALLBACKS
########### ########### ###########

# Gráfico banca

@app.callback(
    Output("id_graf_banca", "figure"),
    Input("id_botao_novaApostaClose","n_clicks"),
    Input('id_title_header','children')
)
def graf_banca(input_botao_novaApostaClose,input_title_header):
    
    df_apostas = pd.read_excel(r"E:\Programação\Python\Projetos\Dashboard Apostas\db_apostas.xlsx")
    df_parametros = pd.read_excel(r"E:\Programação\Python\Projetos\Dashboard Apostas\db_parametros.xlsx")

    banca_inicial = round(float(df_parametros["Banca Inicial"].dropna()),2)

    vazio = df_apostas.empty

    if vazio is True:

        fig_banca = graficoBanca(df_apostas, [banca_inicial], dummy_data_y, cores)
        
        return fig_banca
    else:

        df_apostas['Datas'] = pd.to_datetime(df_apostas['Data']).dt.date
        lista_datas = df_apostas['Datas'].unique() 
        lista_datas = sorted(lista_datas)

        lista_lucroPorData = list()

        for data in lista_datas:
            lucro_por_data = round(df_apostas.loc[df_apostas['Datas']==data,'Saldo'].sum(),2)
            lista_lucroPorData.append(float(lucro_por_data))

        lista_bancaPorData = list()

        for pos in range(len(lista_lucroPorData)):
            lista_bancaPorData.append(round(sum(lista_lucroPorData[0:pos+1],banca_inicial),2))

        fig_banca = graficoBanca(df_apostas, lista_datas, lista_bancaPorData, cores)

        return fig_banca
        
# Abas (estrutura)

@app.callback(
    Output("id_div_abasConteudo", "children"), 
    Input("id_tab_abas", "active_tab")
)
def switch_tab(input_tab_abas):

    df_apostas = pd.read_excel(r"E:\Programação\Python\Projetos\Dashboard Apostas\db_apostas.xlsx")

    lista_esportessUsados = list(df_apostas["Esporte"].unique())
    lista_esportessUsados.sort()

    if input_tab_abas == "id_tab_abaDiaria":

        aba_diaria_conteudo = [
            dbc.Row([
                dbc.Col([
                        dbc.CardBody([
                            html.H6(
                                'Filtros',
                                className="card-title",
                                style={
                                    'textAlign': 'center',
                                    'margin-top': "0px",
                                    #'font-weight': 'bold'
                                },
                            ),
                            html.Hr(
                                style={
                                    "width": "100%", 
                                    "color": "white"
                                }
                            ),
                            dcc.DatePickerSingle(
                                id='id_calendario_abaDiaria',
                                calendar_orientation='vertical',
                                placeholder='Select a date',
                                display_format='D/M/Y',
                                min_date_allowed=date(2022, 1, 20),
                                max_date_allowed=date.today(),
                                date=date.today(),
                                style={
                                    'color':'black',
                                    'background-color': cores['background'],
                                    "margin-top": "10px",
                                },
                            ),
                            dcc.Dropdown(
                                lista_esportessUsados, 
                                #value='Todas', 
                                id='id_dpd_abaDiariaEsporte',
                                placeholder="Selecione um esporte...",
                                style={
                                    'color':'black',
                                    #'background-color': cores['background'],
                                    "margin-top": "10px"
                                }
                            ),
                            dcc.Dropdown(
                                lista_tipo, 
                                #value='Todas', 
                                id='id_dpd_abaDiariaTipo',
                                placeholder="Selecione um tipo de aposta...",
                                style={
                                    'color':'black',
                                    #'background-color': cores['background'],
                                    "margin-top": "10px"
                                }
                            )
                        ]),
                ], md=3),
                dbc.Col([
                        dbc.CardBody([
                            html.H6(
                                'Saldo diário',
                                className="card-title",
                                style={
                                    'textAlign': 'center',
                                    "margin-top": "0px"
                                },
                            ),
                            html.Hr(
                                style={
                                    "width": "100%", 
                                    "color": "white"
                                }
                            ),
                            html.H3(
                                id="id_card_abaDiariaSaldo",
                                children='',
                                className="card-text",
                                style={
                                    'textAlign': 'center'
                                },
                            ),
                            html.H3(
                                id="id_card_abaDiariaSaldoSimbolo",
                                children='',
                                className="card-text",
                                style={
                                    'textAlign': 'center',
                                },
                            )     
                        ]),
                        dbc.CardBody([
                            html.H6(
                                'ROI diário',
                                className="card-title",
                                style={
                                    'textAlign': 'center',
                                    "margin-top": "0px"
                                },
                            ),
                            html.Hr(
                                style={
                                    "width": "100%", 
                                    "color": "white"
                                }
                            ),
                            html.H3(
                                id="id_card_abaDiariaRoi",
                                children='',
                                className="card-text",
                                style={
                                    'textAlign': 'center',
                                },
                            ), 
                            html.H3(
                                id="id_card_abaDiariaRoiSimbolo",
                                children='',
                                className="card-text",
                                style={
                                    'textAlign': 'center'
                                },
                            )
                        ]),
                ], md=2),
                dbc.Col([
                        dbc.CardBody([
                            html.H6(
                                'Número de apostas',
                                className="card-title",
                                style={
                                    'textAlign': 'center',
                                    "margin-top": "0px"
                                },
                            ),
                            html.Hr(
                                style={
                                    "width": "100%", 
                                    "color": "white"
                                }
                            ),
                            html.H3(
                                id="id_card_abaDiariaNumApostas",
                                children='',
                                className="card-text",
                                style={
                                    'textAlign': 'center',
                                },
                            )      
                        ]),
                        dbc.CardBody([
                            html.H6(
                                'Investimento total',
                                className="card-title",
                                style={
                                    'textAlign': 'center',
                                    "margin-top": "0px"
                                },
                            ),
                            html.Hr(
                                style={
                                    "width": "100%", 
                                    "color": "white"
                                }
                            ),
                            html.H3(
                                id="id_card_abaDiariaInvestimento",
                                children='',
                                className="card-text",
                                style={
                                    'textAlign': 'center',
                                },
                            )      
                        ]),
                        dbc.CardBody([
                            html.H6(
                                'Odd média',
                                className="card-title",
                                style={
                                    'textAlign': 'center',
                                    "margin-top": "0px"
                                },
                            ),
                            html.Hr(
                                style={
                                    "width": "100%", 
                                    "color": "white"
                                }
                            ),
                            html.H3(
                                id="id_card_abaDiariaOddMedia",
                                children='',
                                className="card-text",
                                style={
                                    'textAlign': 'center',
                                },
                            )      
                        ])
                ], md=2),
                dbc.Col([
                        dbc.CardBody([
                            html.H6(
                                'Aproveitamento diário',
                                style={
                                    'textAlign': 'center',
                                    "margin-top": "0px"
                                },
                            ),
                            html.Hr(
                                style={
                                    "width": "100%", 
                                    "color": "white"
                                }
                            ),
                            dcc.Graph(
                                id='id_graf_aprovDiario',
                                figure=fig_aproveitamentoDiario
                            )
                        ]) 
                ], md=5)
            ])
        ]

        return aba_diaria_conteudo
    elif input_tab_abas == "id_tab_abaGeral":

        aba_geral_conteudo = [
            dbc.Row([
                dbc.Col([
                        dbc.CardBody([
                            html.H6(
                                'Filtros',
                                style={
                                    'textAlign': 'center',
                                    "margin-top": "0px"
                                },
                            ),
                            html.Hr(
                                style={
                                    "width": "100%", 
                                    "color": "white"
                                }
                            ),
                            dcc.Dropdown(
                                lista_esportessUsados, 
                                #value='Todas', 
                                id='id_dpd_abaGeralEsporte',
                                placeholder="Selecione um esporte...",
                                style={
                                    'color':'black',
                                    #'background-color': cores['background'],
                                    "margin-top": "10px"
                                }
                            ),
                            dcc.Dropdown(
                                lista_tipo, 
                                #value='Todas', 
                                id='id_dpd_abaGeralTipo',
                                placeholder="Selecione um tipo de aposta...",
                                style={
                                    'color':'black',
                                    #'background-color': cores['background'],
                                    "margin-top": "10px"
                                }
                            )
                        ]),
                ], md=3),
                dbc.Col([
                        dbc.CardBody([
                            html.H6(
                                'Saldo',
                                className="card-title",
                                style={
                                    'textAlign': 'center',
                                    "margin-top": "0px"
                                },
                            ),
                            html.Hr(
                                style={
                                    "width": "100%", 
                                    "color": "white"
                                }
                            ),
                            html.H3(
                                id="id_card_abaGeralSaldo",
                                children='',
                                className="card-text",
                                style={
                                    'textAlign': 'center',
                                },
                            ),
                            html.H3(
                                id="id_card_abaGeralSaldoSimbolo",
                                children='',
                                className="card-text",
                                style={
                                    'textAlign': 'center'
                                },
                            )         
                        ]),
                        dbc.CardBody([
                            html.H6(
                                'ROI',
                                className="card-title",
                                style={
                                    'textAlign': 'center',
                                    "margin-top": "0px"
                                },
                            ),
                            html.Hr(
                                style={
                                    "width": "100%", 
                                    "color": "white"
                                }
                            ),
                            html.H3(
                                id="id_card_abaGeralRoi",
                                children='',
                                className="card-text",
                                style={
                                    'textAlign': 'center',
                                },
                            ),
                            html.H3(
                                id="id_card_abaGeralRoiSimbolo",
                                children='',
                                className="card-text",
                                style={
                                    'textAlign': 'center'
                                },
                            )  
                        ])
                ], md=2),
                dbc.Col([
                        dbc.CardBody([
                            html.H6(
                                'Número de apostas',
                                className="card-title",
                                style={
                                    'textAlign': 'center',
                                    "margin-top": "0px"
                                },
                            ),
                            html.Hr(
                                style={
                                    "width": "100%", 
                                    "color": "white"
                                }
                            ),
                            html.H3(
                                id="id_card_abaGeralNumApostas",
                                children='',
                                className="card-text",
                                style={
                                    'textAlign': 'center',
                                },
                            )      
                        ]),
                        dbc.CardBody([
                            html.H6(
                                'Investimento total',
                                className="card-title",
                                style={
                                    'textAlign': 'center',
                                    "margin-top": "0px"
                                },
                            ),
                            html.Hr(
                                style={
                                    "width": "100%", 
                                    "color": "white"
                                }
                            ),
                            html.H3(
                                id="id_card_abaGeralInvestimento",
                                children='',
                                className="card-text",
                                style={
                                    'textAlign': 'center',
                                },
                            )      
                        ]),
                        dbc.CardBody([
                            html.H6(
                                'Odd média',
                                className="card-title",
                                style={
                                    'textAlign': 'center',
                                    "margin-top": "0px"
                                },
                            ),
                            html.Hr(
                                style={
                                    "width": "100%", 
                                    "color": "white"
                                }
                            ),
                            html.H3(
                                id="id_card_abaGeralOddMedia",
                                children='',
                                className="card-text",
                                style={
                                    'textAlign': 'center',
                                },
                            )      
                        ])
                ], md=2),
                dbc.Col([
                        dbc.CardBody([
                            html.H6(
                                'Aproveitamento geral',
                                style={
                                    'textAlign': 'center',
                                    "margin-top": "0px"
                                },
                            ),
                            html.Hr(
                                style={
                                    "width": "100%", 
                                    "color": "white"
                                }
                            ),
                            dcc.Graph(
                                id='id_graf_aprovGeral',
                                figure=fig_aproveitamentoGeral
                            )
                        ]) 
                ], md=5)
            ])
        ]

        return aba_geral_conteudo
    return html.P("Houve um problema...")

# Aba análise diaria (conteúdo e processamento)

@app.callback(
    Output('id_graf_aprovDiario', 'figure'),
    Output('id_card_abaDiariaSaldo', 'children'),
    Output('id_card_abaDiariaRoi', 'children'),
    Output('id_card_abaDiariaNumApostas', 'children'),
    Output('id_card_abaDiariaInvestimento', 'children'),
    Output('id_card_abaDiariaOddMedia', 'children'),
    Output('id_card_abaDiariaSaldoSimbolo','children'),
    Output('id_card_abaDiariaSaldoSimbolo','style'),
    Output('id_card_abaDiariaRoiSimbolo','children'),
    Output('id_card_abaDiariaRoiSimbolo','style'),
    Input('id_calendario_abaDiaria', 'date'),
    Input('id_dpd_abaDiariaEsporte', 'value'),
    Input('id_dpd_abaDiariaTipo', 'value'),
    Input("id_botao_novaApostaClose","n_clicks"),
)
def tab_diario(input_calendario_abaDiaria, input_dpd_abaDiariaEsporte, input_dpd_abaDiariaTipo, input_botao_novaApostaClose):
    
    df_apostas = pd.read_excel(r"E:\Programação\Python\Projetos\Dashboard Apostas\db_apostas.xlsx")

    if df_apostas.empty:

        fig_aproveitamentoDiario = px.pie(
            df_apostas, 
            values='Soma', 
            names='Resultado', 
            title='Resultado diário',
            hole=0.5,
            height=400,
            color='Resultado',
            color_discrete_map = {
                'Acerto': cores['col_acerto'],
                'Erro': cores['col_erro'],
                'Retornada': cores['col_retornada']
            }
        )
        fig_aproveitamentoDiario.update_traces(
            textinfo='percent + value'
        )
        fig_aproveitamentoDiario.update_layout(
            #title='Acertos diários',
            title_x=0.5,
            plot_bgcolor=cores['background2'],
            paper_bgcolor=cores['background2'],
            font_color=cores['text'],
            autosize=True
        )
        
        saldo, roi, numApostas, investimento, oddMedia, bancaAtual, simbolo, style = relatorio_dbVazio()

    else:

        if input_calendario_abaDiaria is not None:

            data_objeto = date.fromisoformat(input_calendario_abaDiaria)
            data_string = data_objeto.strftime('%Y, %m, %d')

            if input_dpd_abaDiariaEsporte is None and input_dpd_abaDiariaTipo is None:

                tabela_filtrada = df_apostas.loc[df_apostas['Data']==data_string]

                fig_aproveitamentoDiario = px.pie(
                    tabela_filtrada, 
                    values='Soma', 
                    names='Resultado', 
                    #title='Aproveitamento',
                    hole=0.5,
                    height=300,
                    color='Resultado',
                    color_discrete_map = {
                        'Acerto': cores['col_acerto'],
                        'Erro': cores['col_erro'],
                        'Retornada': cores['col_retornada']
                    }
                )

                fig_aproveitamentoDiario.update_traces(
                    textinfo='percent + value',
                    insidetextorientation='horizontal'
                )

                fig_aproveitamentoDiario.update_layout(
                    #title='Aproveitamento',
                    title_x=0.5,
                    plot_bgcolor=cores['background2'],
                    paper_bgcolor=cores['background2'],
                    font_color=cores['text'],
                    autosize=True,
                    margin=dict(
                        t=20, b=0, l=0, r=0
                    )
                )

                saldo, roi, numApostas, investimento, oddMedia, bancaInicial, bancaAtual, simbolo, style = relatorio_db(tabela_filtrada, df_parametros, cores)

            if input_dpd_abaDiariaEsporte is not None and input_dpd_abaDiariaTipo is None:

                tabela_filtrada = df_apostas.loc[(df_apostas['Data']==data_string) & (df_apostas['Esporte']==input_dpd_abaDiariaEsporte)]
                
                fig_aproveitamentoDiario = px.pie(
                    tabela_filtrada, 
                    values='Soma', 
                    names='Resultado', 
                    #title='Aproveitamento',
                    hole=0.5,
                    height=300,
                    color='Resultado',
                    color_discrete_map = {
                        'Acerto': cores['col_acerto'],
                        'Erro': cores['col_erro'],
                        'Retornada': cores['col_retornada']
                    }
                )

                fig_aproveitamentoDiario.update_traces(
                    textinfo='percent + value',
                    insidetextorientation='horizontal'
                )

                fig_aproveitamentoDiario.update_layout(
                    #title='Aproveitamento',
                    title_x=0.5,
                    plot_bgcolor=cores['background2'],
                    paper_bgcolor=cores['background2'],
                    font_color=cores['text'],
                    autosize=True,
                    margin=dict(
                        t=20, b=0, l=0, r=0
                    )
                )
            
                saldo, roi, numApostas, investimento, oddMedia, bancaInicial, bancaAtual, simbolo, style = relatorio_db(tabela_filtrada, df_parametros, cores)

            if input_dpd_abaDiariaEsporte is None and input_dpd_abaDiariaTipo is not None:

                tabela_filtrada = df_apostas.loc[(df_apostas['Data']==data_string) & (df_apostas['Tipo']==input_dpd_abaDiariaTipo)]
                
                fig_aproveitamentoDiario = px.pie(
                    tabela_filtrada, 
                    values='Soma', 
                    names='Resultado', 
                    #title='Aproveitamento',
                    hole=0.5,
                    height=300,
                    color='Resultado',
                    color_discrete_map = {
                        'Acerto': cores['col_acerto'],
                        'Erro': cores['col_erro'],
                        'Retornada': cores['col_retornada']
                    }
                )

                fig_aproveitamentoDiario.update_traces(
                    textinfo='percent + value',
                    insidetextorientation='horizontal'
                )

                fig_aproveitamentoDiario.update_layout(
                    #title='Aproveitamento',
                    title_x=0.5,
                    plot_bgcolor=cores['background2'],
                    paper_bgcolor=cores['background2'],
                    font_color=cores['text'],
                    autosize=True,
                    margin=dict(
                        t=20, b=0, l=0, r=0
                    )
                )
            
                saldo, roi, numApostas, investimento, oddMedia, bancaInicial, bancaAtual, simbolo, style = relatorio_db(tabela_filtrada, df_parametros, cores)

            if input_dpd_abaDiariaEsporte is not None and input_dpd_abaDiariaTipo is not None:

                tabela_filtrada = df_apostas.loc[(df_apostas['Data']==data_string) & (df_apostas['Esporte']==input_dpd_abaDiariaEsporte) & (df_apostas['Tipo']==input_dpd_abaDiariaTipo)]
                
                fig_aproveitamentoDiario = px.pie(
                    tabela_filtrada, 
                    values='Soma', 
                    names='Resultado', 
                    #title='Aproveitamento',
                    hole=0.5,
                    height=300,
                    color='Resultado',
                    color_discrete_map = {
                        'Acerto': cores['col_acerto'],
                        'Erro': cores['col_erro'],
                        'Retornada': cores['col_retornada']
                    }
                )

                fig_aproveitamentoDiario.update_traces(
                    textinfo='percent + value',
                    insidetextorientation='horizontal'
                )

                fig_aproveitamentoDiario.update_layout(
                    #title='Aproveitamento',
                    title_x=0.5,
                    plot_bgcolor=cores['background2'],
                    paper_bgcolor=cores['background2'],
                    font_color=cores['text'],
                    autosize=True,
                    margin=dict(
                        t=20, b=0, l=0, r=0
                    )
                )
            
                saldo, roi, numApostas, investimento, oddMedia, bancaInicial, bancaAtual, simbolo, style = relatorio_db(tabela_filtrada, df_parametros, cores)

    return fig_aproveitamentoDiario, saldo, roi, numApostas, investimento, oddMedia, simbolo, style, simbolo, style

# Aba análise geral (conteúdo e processamento)

@app.callback(
    Output('id_graf_aprovGeral', 'figure'),
    Output('id_card_abaGeralSaldo', 'children'),
    Output('id_card_abaGeralRoi', 'children'),
    Output('id_card_abaGeralNumApostas', 'children'),
    Output('id_card_abaGeralInvestimento', 'children'),
    Output('id_card_abaGeralOddMedia', 'children'),
    Output('id_card_abaGeralSaldoSimbolo', 'children'),
    Output('id_card_abaGeralSaldoSimbolo', 'style'),
    Output('id_card_abaGeralRoiSimbolo', 'children'),
    Output('id_card_abaGeralRoiSimbolo', 'style'),
    Input('id_dpd_abaGeralEsporte', 'value'),
    Input('id_dpd_abaGeralTipo', 'value'),
    Input("id_botao_novaApostaClose","n_clicks"),
)
def tab_geral(input_dpd_abaGeralEsporte, input_dpd_abaGeralTipo, input_botao_novaApostaClose):

    df_apostas = pd.read_excel(r"E:\Programação\Python\Projetos\Dashboard Apostas\db_apostas.xlsx")

    if df_apostas.empty:
        
        fig_aproveitamentoGeral = graficoAproveitamentoGeral(df_apostas, cores)  

        saldo, roi, numApostas, investimento, oddMedia, bancaAtual, simbolo, style = relatorio_dbVazio()
        
    else:

        if input_dpd_abaGeralEsporte is None and input_dpd_abaGeralTipo is None:

            fig_aproveitamentoGeral = graficoAproveitamentoGeral(df_apostas, cores)

            saldo, roi, numApostas, investimento, oddMedia, bancaInicial, bancaAtual, simbolo, style = relatorio_db(df_apostas, df_parametros, cores)

        if input_dpd_abaGeralEsporte is not None and input_dpd_abaGeralTipo is None:

            tabela_filtrada = df_apostas.loc[df_apostas['Esporte']==input_dpd_abaGeralEsporte]
            
            fig_aproveitamentoGeral = graficoAproveitamentoGeral(tabela_filtrada, cores)

            saldo, roi, numApostas, investimento, oddMedia, bancaInicial, bancaAtual, simbolo, style = relatorio_db(tabela_filtrada, df_parametros, cores)

        if input_dpd_abaGeralEsporte is None and input_dpd_abaGeralTipo is not None:

            tabela_filtrada = df_apostas.loc[df_apostas['Tipo']==input_dpd_abaGeralTipo]
            
            fig_aproveitamentoGeral = graficoAproveitamentoGeral(tabela_filtrada, cores)
            
            saldo, roi, numApostas, investimento, oddMedia, bancaInicial, bancaAtual, simbolo, style = relatorio_db(tabela_filtrada, df_parametros, cores)

        if input_dpd_abaGeralEsporte is not None and input_dpd_abaGeralTipo is not None:

            tabela_filtrada = df_apostas.loc[(df_apostas['Esporte']==input_dpd_abaGeralEsporte) & (df_apostas['Tipo']==input_dpd_abaGeralTipo)]
            
            fig_aproveitamentoGeral = graficoAproveitamentoGeral(df_apostas, cores)

            saldo, roi, numApostas, investimento, oddMedia, bancaInicial, bancaAtual, simbolo, style = relatorio_db(tabela_filtrada, df_parametros, cores)

    return fig_aproveitamentoGeral, saldo, roi, numApostas, investimento, oddMedia, simbolo, style, simbolo, style

# Modal de inserir apostas (abertura/fechamento)

@app.callback(
    Output("id_modal_novaAposta", "is_open"),
    Input("id_botao_novaApostaOpen", "n_clicks"), 
    Input("id_botao_novaApostaClose", "n_clicks"),
    Input("id_modal_novaAposta", "is_open"),
)
def modal_apostas_toggle(input_botao_novaApostaOpen, input_botao_novaApostaClose, input_modal_novaAposta):
    if input_botao_novaApostaOpen or input_botao_novaApostaClose:
        return not input_modal_novaAposta
    return input_modal_novaAposta

# Modal de inserir apostas (conteúdo e processamento) 

@app.callback(
    Output("id_alerta_novaApostaInserir", "is_open"),
    Output("id_alerta_novaApostaInserir", "children"),
    Output("id_alerta_novaApostaInserir", "color"),
    Input("id_botao_novaApostaInserir","n_clicks"),
    State("id_calendario_novaAposta", "date"), 
    State("id_dpd_novaApostaEsportes", "value"),
    State("id_dpd_novaApostaTipo", "value"),
    State("id_input_novaApostaInvestimento", "value"),
    State("id_input_novaApostaOdd", "value"),
    State("id_dpd_novaApostaResultado", "value"),
    State("id_dpd_novaApostaFinalizacao", "value"),
    State("id_input_novaApostaRetirada", "value"), 
)
def modal_apostas_conteudo(input_botao_novaApostaInserir, state_calendario_novaAposta, state_dpd_novaApostaEsportes, state_dpd_novaApostaTipo, state_input_novaApostaInvestimento, state_input_novaApostaOdd, state_dpd_novaApostaResultado, state_dpd_novaApostaFinalizacao, state_input_novaApostaRetirada):

    if 'id_botao_novaApostaInserir' == ctx.triggered_id:
        if state_calendario_novaAposta and state_dpd_novaApostaEsportes and state_dpd_novaApostaTipo and state_input_novaApostaInvestimento and state_input_novaApostaOdd and state_dpd_novaApostaResultado and state_dpd_novaApostaFinalizacao is not None:
            
            aposta_data = datetime.strptime(state_calendario_novaAposta, '%Y-%m-%d')
            aposta_esporte = state_dpd_novaApostaEsportes
            aposta_tipo = state_dpd_novaApostaTipo
            aposta_investimento = float(state_input_novaApostaInvestimento)
            aposta_odd = float(state_input_novaApostaOdd)
            aposta_resultado = state_dpd_novaApostaResultado
            aposta_finalizacao = state_dpd_novaApostaFinalizacao
            aposta_retirada = state_input_novaApostaRetirada
            soma = 1

            if state_dpd_novaApostaFinalizacao == 'Normal': 
                if aposta_resultado == 'Acerto':
                    aposta_saldo = round((aposta_investimento * aposta_odd)-aposta_investimento,2)
                elif aposta_resultado == 'Erro':
                    aposta_saldo = round(-1*aposta_investimento,2)
                elif aposta_resultado == 'Retornada':
                    aposta_saldo = 0
                    
                df_apostas = pd.read_excel(r"E:\Programação\Python\Projetos\Dashboard Apostas\db_apostas.xlsx")

                nova_aposta = [aposta_data, aposta_esporte, aposta_tipo, aposta_odd, aposta_investimento, aposta_finalizacao, aposta_resultado, aposta_saldo, soma]
                df_nova_aposta = pd.DataFrame([nova_aposta], columns=list(['Data', 'Esporte', 'Tipo', 'Odd', 'Investimento', 'Finalização', 'Resultado', 'Saldo', 'Soma']))
                df_concat = pd.concat([df_apostas,df_nova_aposta], ignore_index=True)
                
                with pd.ExcelWriter(
                    r"E:\Programação\Python\Projetos\Dashboard Apostas\db_apostas.xlsx", 
                    mode="a", 
                    engine="openpyxl", 
                    if_sheet_exists="overlay",
                    date_format="YYYY-MM-DD",
                    datetime_format="YYYY-MM-DD HH:MM:SS"
                ) as writer:
                    df_concat.to_excel(writer, sheet_name="Plan1", index=False)  
                
                time.sleep(0.1)

                mensagemAlerta, corAlerta, stateAlerta = mensagem('Sucesso','Aposta')

                return stateAlerta, mensagemAlerta, corAlerta
            else: 
                if state_input_novaApostaRetirada is not None:

                    if aposta_resultado == 'Acerto':
                        aposta_saldo = round(aposta_retirada-aposta_investimento,2)
                    elif aposta_resultado == 'Erro':
                        aposta_saldo = round(aposta_retirada-aposta_investimento,2)
                    elif aposta_resultado == 'Retornada':
                        aposta_saldo = 0
                        
                    df_apostas = pd.read_excel(r"E:\Programação\Python\Projetos\Dashboard Apostas\db_apostas.xlsx")

                    nova_aposta = [aposta_data, aposta_esporte, aposta_tipo, aposta_odd, aposta_investimento, aposta_finalizacao, aposta_resultado, aposta_saldo, soma]
                    df_nova_aposta = pd.DataFrame([nova_aposta], columns=list(['Data', 'Esporte', 'Tipo', 'Odd', 'Investimento', 'Finalização', 'Resultado', 'Saldo', 'Soma']))
                    df_concat = pd.concat([df_apostas,df_nova_aposta], ignore_index=True)
                    
                    with pd.ExcelWriter(
                        r"E:\Programação\Python\Projetos\Dashboard Apostas\db_apostas.xlsx", 
                        mode="a", 
                        engine="openpyxl", 
                        if_sheet_exists="overlay",
                        date_format="YYYY-MM-DD",
                        datetime_format="YYYY-MM-DD HH:MM:SS"
                    ) as writer:
                        df_concat.to_excel(writer, sheet_name="Plan1", index=False)  
                    
                    time.sleep(0.1)

                    mensagemAlerta, corAlerta, stateAlerta = mensagem('Sucesso','Aposta')

                    return stateAlerta, mensagemAlerta, corAlerta
                else: 

                    time.sleep(0.1)
                    mensagemAlerta, corAlerta, stateAlerta = mensagem('Erro','Aposta')
 
                    return stateAlerta, mensagemAlerta, corAlerta
        else:
            
            time.sleep(0.1)

            mensagemAlerta, corAlerta, stateAlerta = mensagem('Erro','Aposta')

            return stateAlerta, mensagemAlerta, corAlerta
    else:  

        mensagemAlerta, corAlerta, stateAlerta = mensagem('Nulo','Nulo')

        return stateAlerta, mensagemAlerta, corAlerta

# Modal de inserir apostas (colapse para apostas retiradas) 

@app.callback(
    Output("id_collapse_novaApostaRetirada", "is_open"),
    Input("id_dpd_novaApostaFinalizacao", "value"), 
)
def modal_apostas_colapseRetirada(input_dpd_novaApostaFinalizacao):
    if input_dpd_novaApostaFinalizacao == 'Retirada':
        status_colapse = True
        return status_colapse
    else: 
        status_colapse = False
        return status_colapse

# Modal de inserir apostas (limpeza dos dados)

@app.callback(
    Output("id_dpd_novaApostaEsportes", "value"),
    Output("id_dpd_novaApostaTipo", "value"),
    Output("id_input_novaApostaInvestimento", "value"),
    Output("id_input_novaApostaOdd", "value"),
    Output("id_dpd_novaApostaResultado", "value"),
    Output("id_dpd_novaApostaFinalizacao", "value"),
    Output("id_input_novaApostaRetirada", "value"), 
    Input("id_botao_novaApostaInserir","n_clicks"), 
    Input("id_botao_novaApostaClose","n_clicks"),
    Input("id_dpd_novaApostaEsportes", "value"),
    Input("id_dpd_novaApostaTipo", "value"),
    Input("id_input_novaApostaInvestimento", "value"),
    Input("id_input_novaApostaOdd", "value"),
    Input("id_dpd_novaApostaResultado", "value"),
    Input("id_dpd_novaApostaFinalizacao", "value"),
    Input("id_input_novaApostaRetirada", "value"), 
)
def modal_aposta_limpeza(input_botao_novaApostaInserir, input_botao_novaApostaClose, input_dpd_novaApostaEsportes, input_dpd_novaApostaTipo, input_input_novaApostaInvestimento, input_input_novaApostaOdd, input_dpd_novaApostaResultado, input_dpd_novaApostaFinalizacao, input_input_novaApostaRetirada):
    if 'id_botao_novaApostaInserir' == ctx.triggered_id:
        if input_dpd_novaApostaEsportes and input_dpd_novaApostaTipo and input_input_novaApostaInvestimento and input_input_novaApostaOdd and input_dpd_novaApostaResultado and input_dpd_novaApostaFinalizacao is not None:
            if input_dpd_novaApostaFinalizacao == 'Normal':
                return input_dpd_novaApostaEsportes, input_dpd_novaApostaTipo, input_input_novaApostaInvestimento, None, None, input_dpd_novaApostaFinalizacao, None
            else:
                if input_input_novaApostaRetirada is not None:
                    return input_dpd_novaApostaEsportes, input_dpd_novaApostaTipo, input_input_novaApostaInvestimento, None, None, None, None
                else:
                    return input_dpd_novaApostaEsportes, input_dpd_novaApostaTipo, input_input_novaApostaInvestimento, input_input_novaApostaOdd, input_dpd_novaApostaResultado, input_dpd_novaApostaFinalizacao, input_input_novaApostaRetirada
        else:
            return input_dpd_novaApostaEsportes, input_dpd_novaApostaTipo, input_input_novaApostaInvestimento, input_input_novaApostaOdd, input_dpd_novaApostaResultado, input_dpd_novaApostaFinalizacao, input_input_novaApostaRetirada
    elif 'id_botao_novaApostaClose' == ctx.triggered_id:
        return None, None, None, None, None, None, None
    else: 
        return input_dpd_novaApostaEsportes, input_dpd_novaApostaTipo, input_input_novaApostaInvestimento, input_input_novaApostaOdd, input_dpd_novaApostaResultado, input_dpd_novaApostaFinalizacao, input_input_novaApostaRetirada

# Modal de configurações (abertura/fechamento)

@app.callback(
    Output("id_modal_config", "is_open"),
    Input("id_botao_configOpen", "n_clicks"), 
    Input("id_botao_configClose", "n_clicks"),
    Input("id_modal_config", "is_open"),
)
def modal_config_toggle(input_botao_configOpen, input_botao_configClose, input_modal_config):
    if input_botao_configOpen or input_botao_configClose:
        return not input_modal_config
    return input_modal_config

# Modal de configurações (conteúdo e processamento)

@app.callback(
    Output("id_alerta_configEsporte", "is_open"),
    Output("id_alerta_configEsporte", "children"),
    Output("id_alerta_configEsporte", "color"),   
    Output("id_alerta_configBancaInicial", "is_open"),
    Output("id_alerta_configBancaInicial", "children"),
    Output("id_alerta_configBancaInicial", "color"),   
    Input("id_botao_configInserirEsporte", "n_clicks"),
    Input("id_botao_configBancaInicial", "n_clicks"),
    State("id_input_configEsporte", "value"), 
    State("id_input_configBancaInicial", "value"), 
)
def modal_config_conteudo(input_botao_configInserirEsporte, input_botao_configBancaInicial, state_input_configEsporte, state_input_configBancaInicial):
    if 'id_botao_configInserirEsporte' == ctx.triggered_id:
        if state_input_configEsporte is not None: 
            
            df_parametros = pd.read_excel(r"E:\Programação\Python\Projetos\Dashboard Apostas\db_parametros.xlsx")
            novo_esporte = state_input_configEsporte
            df_parametros_novo = pd.DataFrame([novo_esporte], columns=list(['Esporte']))
            df_concat = pd.concat([df_parametros,df_parametros_novo], ignore_index=True)
            
            with pd.ExcelWriter(
                r"E:\Programação\Python\Projetos\Dashboard Apostas\db_parametros.xlsx", 
                mode="a", 
                engine="openpyxl", 
                if_sheet_exists="overlay",
                date_format="DD-MM-YYYY",
                datetime_format="DD-MM-YYYY"
            ) as writer:
                df_concat.to_excel(writer, sheet_name="Plan1", index=False)      

                time.sleep(0.1)

                mensagemAlerta, corAlerta, stateAlerta = mensagem('Sucesso','Esporte')

                return stateAlerta, mensagemAlerta, corAlerta, False, '', 'danger'
        else:
            
            time.sleep(0.1)
            
            mensagemAlerta, corAlerta, stateAlerta = mensagem('Erro','Esporte')

            return stateAlerta, mensagemAlerta, corAlerta, False, '', 'danger'
    elif 'id_botao_configBancaInicial' == ctx.triggered_id:
        if state_input_configBancaInicial is not None: 
            
            df_parametros = pd.read_excel(r"E:\Programação\Python\Projetos\Dashboard Apostas\db_parametros.xlsx")
            
            df_nova_banca = df_parametros
            lista_banca_inicial = list(df_parametros['Banca Inicial'])
            nova_banca = state_input_configBancaInicial
            lista_banca_inicial[0] = nova_banca
            df_nova_banca['Banca Inicial'] = lista_banca_inicial

            with pd.ExcelWriter(
                r"E:\Programação\Python\Projetos\Dashboard Apostas\db_parametros.xlsx", 
                mode="a", 
                engine="openpyxl", 
                if_sheet_exists="overlay",
                date_format="DD-MM-YYYY",
                datetime_format="DD-MM-YYYY"
            ) as writer:
                df_nova_banca.to_excel(writer, sheet_name="Plan1", index=False)      

                time.sleep(0.1)
                mensagemAlerta, corAlerta, stateAlerta = mensagem('Sucesso','Banca')

                return False, '', 'danger', stateAlerta, mensagemAlerta, corAlerta
        else:
            
            time.sleep(0.1)

            mensagemAlerta, corAlerta, stateAlerta = mensagem('Erro','Banca')

            return False, '', 'danger', stateAlerta, mensagemAlerta, corAlerta
    else:
        mensagemAlerta, corAlerta, stateAlerta = mensagem('Nulo','Nulo')

        return stateAlerta, mensagemAlerta, corAlerta, stateAlerta, mensagemAlerta, corAlerta
           
# Modal de configurações (limpeza dos dados) e Modal de configurações (atualização do DPD dos esportes no modal de inserir apostas)

@app.callback(
    Output("id_input_configEsporte", "value"),
    Output("id_div_novaApostaEsportes", "children"),
    Output("id_input_configBancaInicial", "value"),
    Input("id_botao_configInserirEsporte", "n_clicks"),
    Input("id_botao_configBancaInicial", "n_clicks"),
    Input("id_botao_configClose", "n_clicks"),
    Input("id_input_configEsporte", "value"),
    Input("id_input_configBancaInicial", "value"),
)
def modal_config_limpeza(input_botao_configInserirEsporte, input_botao_configBancaInicial, input_botao_configClose, input_input_configEsporte, input_input_configBancaInicial):
    
    df_parametros = pd.read_excel(r"E:\Programação\Python\Projetos\Dashboard Apostas\db_parametros.xlsx")
    lista_esportes = list(df_parametros["Esporte"].dropna())

    dropdown = [
        dcc.Dropdown(
            lista_esportes, 
            #value='Todas', 
            id='id_dpd_novaApostaEsportes',
            placeholder="Selecione um esporte...",
            style={
                'color':'black',
                #'background-color': cores['background'],
                "margin-top": "10px"
            }
        ),
    ]

    if 'id_botao_configInserirEsporte' == ctx.triggered_id or 'id_botao_configClose' == ctx.triggered_id or 'id_botao_configBancaInicial' == ctx.triggered_id:
        return None, dropdown, None
    else:
        return input_input_configEsporte, dropdown, input_input_configBancaInicial

# Cards

@app.callback(
    Output("id_card_bancaInicial", "children"),
    Output("id_card_bancaAtual", "children"),
    Output("id_card_saldo", "children"),
    Output("id_card_roi", "children"),
    Input("id_botao_novaApostaClose","n_clicks"),
    Input('id_title_header','children')
)
def cards(input_botao_novaApostaClose, input_title_header):

    df_apostas = pd.read_excel(r"E:\Programação\Python\Projetos\Dashboard Apostas\db_apostas.xlsx")
    df_parametros = pd.read_excel(r"E:\Programação\Python\Projetos\Dashboard Apostas\db_parametros.xlsx")

    saldo, roi, numApostas, investimento, oddMedia, bancaInicial, bancaAtual, simbolo, style = relatorio_db(df_apostas, df_parametros, cores)

    return bancaInicial, bancaAtual, saldo, roi

########### ########### ###########
########### LOCAL HOST
########### ########### ###########

if __name__ == '__main__':
    app.run_server(debug=True)
    