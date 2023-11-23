##################################################
#################### DASHBOARD APOSTAS
#################### Guilherme L. Nascimento 
##################################################

from dash import Dash, html, dcc, Input, Output, State, ctx
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table
from datetime import date, datetime
import time
import math
import os

from funcoes import relatorioDBVazio, relatorioDB, mensagem, calcularSaldoNormal, calcularSaldoRetirada, inserirAposta, inserirParametro, leituraDB
from graficos import graficoBanca, graficoAproveitamento

########### ########### ###########
########### CONFIGURAÇÕES DO APP
########### ########### ###########

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], suppress_callback_exceptions=True)

########### ########### ###########
########### BASE DE DADOS 
########### ########### ###########

NOME_ARQUIVO_APOSTAS = 'db_apostas.xlsx'
NOME_ARQUIVO_PARAMETROS = 'db_parametros.xlsx'

dfApostas = leituraDB(NOME_ARQUIVO_APOSTAS)
dfParametros = leituraDB(NOME_ARQUIVO_PARAMETROS)

########### ########### ###########
########### VARIÁVEIS GLOBAIS
########### ########### ###########

# Modal

LISTA_ESPORTES = list(dfParametros["Esporte"].dropna())
LISTA_TIPO = list(dfParametros["Tipo"].dropna())
LISTA_RESULTADO = list(dfParametros["Resultado"].dropna())
LISTA_FINALIZACAO = list(dfParametros["Finalizacão"].dropna())
LISTA_CREDITO_APOSTA = list(dfParametros["Crédito de aposta"].dropna())

# Dummy data para declaração de figuras

DUMMY_DATA_X = ['01/01/01']
DUMMY_DATA_Y = ['100']

# Cores

CORES = {
    'backgroundPreto': 'rgb(6, 6, 6)',
    'backgroundGrafite': 'rgb(40, 40, 40)',
    'texto': 'rgb(255, 255, 255)',
    'colunaAcerto': 'rgb(49, 252, 195)',
    'colunaErro': 'rgb(159, 8, 201)',
    'colunaRetornada': 'rgb(195, 195, 17)',
    'graficoLinha': 'rgb(49, 252, 195)',
    'graficoMarcador': 'rgb(159, 8, 201)',
    'graficoGrade':'rgb(100, 100, 100)'
}

########### ########### ###########
########### CONFIGURAÇÕES DOS GRÁFICOS
########### ########### ###########

# Banca

figuraBanca = graficoBanca(dfApostas, DUMMY_DATA_X, DUMMY_DATA_Y, CORES)

# Diario

figuraAproveitamentoDiario = graficoAproveitamento(dfApostas, CORES)

# Geral

figuraAproveitamentoGeral = graficoAproveitamento(dfApostas, CORES)

########### ########### ###########
########### LAYOUT
########### ########### ###########

app.layout = html.Div(
    children=[
        dbc.Row([
            dbc.Col([
                html.H4(
                    'DASHBOARD DE APOSTAS',
                    id = 'colunaHeader',
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
                            id = 'colunaBancaInicial',
                            style={
                                'textAlign': 'center',
                            },
                        )       
                    ]),
                ], 
                style={
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
                            id='colunaBancaAtual',
                            className="card-text",
                            style={
                                'textAlign': 'center',
                            },
                        )       
                    ]),
                ], 
                style={
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
                            id='colunaSaldo',
                            className="card-text",
                            style={
                                'textAlign': 'center',
                            },
                        )       
                    ]),
                ], 
                style={
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
                            id='colunaRoi',
                            className="card-text",
                            style={
                                'textAlign': 'center',
                            },
                        )       
                    ]),
                ], 
                style={
                    "margin-top": "10px"
                }
                ),
                html.Div(  
                    dbc.Button(
                        "Inserir nova aposta", 
                        id="modalNovaApostaBotaoAbrir", 
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
                                id='modalNovaApostaCalendario',
                                calendar_orientation='vertical',
                                placeholder='Select a date',
                                display_format='D/M/Y',
                                min_date_allowed=date(2022, 1, 20),
                                max_date_allowed=date.today(),
                                date=date.today(),
                                style={
                                    'color':'black',
                                    'background-color': CORES['backgroundPreto'],
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
                                    LISTA_ESPORTES, 
                                    #value='Todas', 
                                    id='modalNovaApostaEsporte',
                                    placeholder="Selecione um esporte...",
                                    style={
                                        'color':'black',
                                        "margin-top": "10px"
                                    }
                                ),
                            ],
                            id='modalNovaApostaDivEsporte'
                            ),
                            html.H6(
                                'Tipo da aposta:',
                                style={
                                    'textAlign': 'left',
                                    "margin-top": "5px",
                                },
                            ),
                            dcc.Dropdown(
                                LISTA_TIPO, 
                                #value='Todas', 
                                id='modalNovaApostaTipo',
                                placeholder="Selecione o tipo...",
                                style={
                                    'color':'black',
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
                                id='modalNovaApostaInvestimento',
                                type="number",
                                min=0,
                                placeholder="Insira o valor investido...",
                            ),
                            dbc.Switch(
                                label='Crédito de aposta',
                                value=False,
                                id="modalNovaApostaSwitchCredito",
                                style={
                                    "margin-top": "10px"
                                }
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
                                id='modalNovaApostaOdd',
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
                                LISTA_RESULTADO, 
                                id='modalNovaApostaResultado',
                                placeholder="Selecione o resultado...",
                                style={
                                    'color':'black',
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
                                LISTA_FINALIZACAO, 
                                id='modalNovaApostaFinalizacao',
                                placeholder="Selecione o método...",
                                style={
                                    'color':'black',
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
                                    id='modalNovaApostaRetirada',
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
                                        id="modalNovaApostaBotaoInserir", 
                                        className="ms-auto", 
                                        n_clicks=0,
                                        disabled=False,
                                        size='lg',
                                        color="dark", 
                                    ),
                                    dbc.Alert(
                                        "",
                                        id="modalNovaApostaAlertaInserir",
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
                                id="modalNovaApostaBotaoFechar", 
                                className="ms-auto", 
                                n_clicks=0,
                                color="dark", 
                                # className="me-1"
                            )
                        ),
                    ],
                    id="modalNovaAposta",
                    is_open=False,
                    centered=True,
                    size="lg",
                    backdrop="static"
                ),
                html.Div(  
                    dbc.Button(
                        "Configurações  do dashboard", 
                        id="modalConfiguracoesBotaoAbrir", 
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
                                id='modalConfiguracoesEsporte',
                                type="text",
                                min=0,
                                placeholder="Insira o nome do esporte...",
                            ),
                            html.Div([
                                dbc.Button(
                                    "Inserir esporte", 
                                    id="modalConfiguracoesBotaoInserirEsporte", 
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
                                    id="modalConfiguracoesAlertaEsporte",
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
                                id='modalConfiguracoesBancaInicial',
                                type="number",
                                min=0,
                                placeholder="Insira o valor da banca inicial...",
                            ),
                            html.Div([
                                dbc.Button(
                                    "Inserir banca inicial", 
                                    id="modalConfiguracoesBotaoInserirBancaInicial", 
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
                                    id="modalConfiguracoesAlertaBancaInicial",
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
                                id="modalConfiguracoesBotaoFechar", 
                                className="ms-auto", 
                                n_clicks=0,
                                color="dark", 
                                # className="me-1"
                            )
                        ),
                    ],
                    id="modalConfiguracoes",
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
                            id='graficoBanca',
                            figure=figuraBanca
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
                                    tab_id="abaDiaria",
                                ),
                                dbc.Tab(
                                    label="Análise geral", 
                                    tab_id="abaGeral",
                                    active_tab_class_name={"backgroundColor": CORES['backgroundGrafite']}
                                )
                            ],
                            id="abas",
                            active_tab="abaDiaria"
                            )  
                        ]),
                        dbc.CardBody([
                            html.Div(
                                children='',
                                id="abasConteudo", 
                                className="card-text"
                            )
                        ])
                    ], 
                    style={
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
    Output("graficoBanca", "figure"),
    Input("modalNovaApostaBotaoFechar","n_clicks"),
    Input('colunaHeader','children')
)
def graf_banca(input_modalNovaApostaBotaoFechar,input_colunaHeader):
    
    dfApostas = leituraDB(NOME_ARQUIVO_APOSTAS)
    dfParametros = leituraDB(NOME_ARQUIVO_PARAMETROS)

    bancaInicial = round(float(dfParametros["Banca Inicial"].dropna()),2)

    if dfApostas.empty:

        figuraBanca = graficoBanca(dfApostas, [date.today()], [bancaInicial], CORES)
        
        return figuraBanca
    else:

        dfApostas['Datas'] = pd.to_datetime(dfApostas['Data']).dt.date
        listaDatas = dfApostas['Datas'].unique() 
        listaDatas = sorted(listaDatas)

        listaLucroPorData = list()

        for data in listaDatas:
            lucroPorData = round(dfApostas.loc[dfApostas['Datas']==data,'Saldo'].sum(),2)
            listaLucroPorData.append(float(lucroPorData))

        listaBancaPorData = list()

        for pos in range(len(listaLucroPorData)):
            listaBancaPorData.append(round(sum(listaLucroPorData[0:pos+1],bancaInicial),2))

        figuraBanca = graficoBanca(dfApostas, listaDatas, listaBancaPorData, CORES)

        return figuraBanca
        
# Abas (estrutura)

@app.callback(
    Output("abasConteudo", "children"), 
    Input("abas", "active_tab")
)
def switch_tab(input_abas):

    dfApostas = leituraDB(NOME_ARQUIVO_APOSTAS)

    listaEsportesUsados = list(dfApostas["Esporte"].unique())
    listaEsportesUsados.sort()

    if input_abas == "abaDiaria":

        abaDiariaConteudo = [
            dbc.Row([
                dbc.Col([
                        dbc.CardBody([
                            html.H6(
                                'Filtros',
                                className="card-title",
                                style={
                                    'textAlign': 'center',
                                    'margin-top': "0px",
                                },
                            ),
                            html.Hr(
                                style={
                                    "width": "100%", 
                                    "color": "white"
                                }
                            ),
                            dcc.DatePickerSingle(
                                id='abaDiariaCalendario',
                                calendar_orientation='vertical',
                                placeholder='Select a date',
                                display_format='D/M/Y',
                                min_date_allowed=date(2022, 1, 20),
                                max_date_allowed=date.today(),
                                date=date.today(),
                                style={
                                    'color':'black',
                                    'background-color': CORES['backgroundPreto'],
                                    "margin-top": "10px",
                                },
                            ),
                            dcc.Dropdown(
                                listaEsportesUsados, 
                                id='abaDiariaEsporte',
                                placeholder="Esporte",
                                style={
                                    'color':'black',
                                    "margin-top": "10px"
                                }
                            ),
                            dcc.Dropdown(
                                LISTA_TIPO, 
                                id='abaDiariaTipo',
                                placeholder="Tipo de aposta",
                                style={
                                    'color':'black',
                                    "margin-top": "10px"
                                }
                            ),
                            dcc.Dropdown(
                                LISTA_CREDITO_APOSTA, 
                                id='abaDiariaCredito',
                                placeholder="Crédito de aposta",
                                style={
                                    'color':'black',
                                    "margin-top": "10px"
                                }
                            ),
                            dcc.Dropdown(
                                LISTA_FINALIZACAO,  
                                id='abaDiariaFinalizacao',
                                placeholder="Tipo de finalização",
                                style={
                                    'color':'black',
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
                                id="abaDiariaSaldo",
                                children='',
                                className="card-text",
                                style={
                                    'textAlign': 'center'
                                },
                            ),
                            html.H3(
                                id="abaDiariaSaldoSimbolo",
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
                                id="abaDiariaRoi",
                                children='',
                                className="card-text",
                                style={
                                    'textAlign': 'center',
                                },
                            ), 
                            html.H3(
                                id="abaDiariaRoiSimbolo",
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
                                'Quantidade de apostas',
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
                                id="abaDiariaQuantidadeApostas",
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
                                id="abaDiariaInvestimento",
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
                                id="abaDiariaOddMedia",
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
                                id='graficoAproveitamentoDiario',
                                figure=figuraAproveitamentoDiario
                            )
                        ]) 
                ], md=5)
            ]),
            dbc.Row([
                dash_table.DataTable(
                    id="tabelaApostas",
                    data=dfApostas.to_dict('records'))
                    #, [{"name": i, "id": i} for i in dfApostas.columns]
            ])

        ]

        return abaDiariaConteudo
    
    elif input_abas == "abaGeral":

        abaGeralConteudo = [
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
                                listaEsportesUsados, 
                                #value='Todas', 
                                id='abaGeralEsporte',
                                placeholder="Esporte",
                                style={
                                    'color':'black',
                                    "margin-top": "10px"
                                }
                            ),
                            dcc.Dropdown(
                                LISTA_TIPO, 
                                #value='Todas', 
                                id='abaGeralTipo',
                                placeholder="Tipo de aposta",
                                style={
                                    'color':'black',
                                    "margin-top": "10px"
                                }
                            ),
                            dcc.Dropdown(
                                LISTA_CREDITO_APOSTA, 
                                #value='Todas', 
                                id='abaGeralCredito',
                                placeholder="Crédito de aposta",
                                style={
                                    'color':'black',
                                    "margin-top": "10px"
                                }
                            ),
                            dcc.Dropdown(
                                LISTA_FINALIZACAO,  
                                id='abaGeralFinalizacao',
                                placeholder="Tipo de finalização",
                                style={
                                    'color':'black',
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
                                id="abaGeralSaldo",
                                children='',
                                className="card-text",
                                style={
                                    'textAlign': 'center',
                                },
                            ),
                            html.H3(
                                id="abaGeralSaldoSimbolo",
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
                                id="abaGeralRoi",
                                children='',
                                className="card-text",
                                style={
                                    'textAlign': 'center',
                                },
                            ),
                            html.H3(
                                id="abaGeralRoiSimbolo",
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
                                'Quantidade de apostas',
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
                                id="abaGeralQuantidadeApostas",
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
                                id="abaGeralInvestimento",
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
                                id="abaGeralOddMedia",
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
                                id='graficoAproveitamentoGeral',
                                figure=figuraAproveitamentoGeral
                            )
                        ]) 
                ], md=5)
            ])
        ]

        return abaGeralConteudo
    return html.P("Houve um problema...")

# Aba análise diaria (conteúdo e processamento)

@app.callback(
    Output('graficoAproveitamentoDiario', 'figure'),
    Output('abaDiariaSaldo', 'children'),
    Output('abaDiariaRoi', 'children'),
    Output('abaDiariaQuantidadeApostas', 'children'),
    Output('abaDiariaInvestimento', 'children'),
    Output('abaDiariaOddMedia', 'children'),
    Output('abaDiariaSaldoSimbolo','children'),
    Output('abaDiariaSaldoSimbolo','style'),
    Output('abaDiariaRoiSimbolo','children'),
    Output('abaDiariaRoiSimbolo','style'),
    Output('tabelaApostas','data'),
    Input('abaDiariaCalendario', 'date'),
    Input('abaDiariaEsporte', 'value'),
    Input('abaDiariaTipo', 'value'),
    Input('abaDiariaCredito', 'value'),
    Input('abaDiariaFinalizacao', 'value'),
    Input("modalNovaApostaBotaoFechar","n_clicks"),
)
def tab_diario(input_calendario_abaDiaria, input_dpd_abaDiariaEsporte, input_dpd_abaDiariaTipo, input_dpd_abaDiariaCreditoDeAposta, input_dpd_abaDiariaFinalizacao, input_botao_novaApostaClose):
    
    dfApostas = leituraDB(NOME_ARQUIVO_APOSTAS)

    if dfApostas.empty:

        figuraAproveitamentoDiario = graficoAproveitamento(dfApostas, CORES)
        
        saldo, roi, numApostas, investimento, oddMedia, simbolo, style = relatorioDBVazio()

    else:

        data_objeto = date.fromisoformat(input_calendario_abaDiaria)
        data_string = data_objeto.strftime('%Y, %m, %d')

        tabela_filtrada = dfApostas.loc[
            ((dfApostas['Data']==data_string) if data_string is not None else (dfApostas['Data']!=None))
            & ((dfApostas['Esporte']==input_dpd_abaDiariaEsporte) if input_dpd_abaDiariaEsporte is not None else (dfApostas['Esporte']!=None)) 
            & ((dfApostas['Tipo']==input_dpd_abaDiariaTipo) if input_dpd_abaDiariaTipo is not None else (dfApostas['Tipo']!=None))
            & ((dfApostas['Crédito de aposta']==input_dpd_abaDiariaCreditoDeAposta) if input_dpd_abaDiariaCreditoDeAposta is not None else (dfApostas['Crédito de aposta']!=None))
            & ((dfApostas['Finalização']==input_dpd_abaDiariaFinalizacao) if input_dpd_abaDiariaFinalizacao is not None else (dfApostas['Finalização']!=None))
        ]

        figuraAproveitamentoDiario = graficoAproveitamento(tabela_filtrada, CORES)
    
        saldo, roi, numApostas, investimento, oddMedia, bancaInicial, bancaAtual, simbolo, style = relatorioDB(tabela_filtrada, dfParametros, CORES)

        tabela = tabela_filtrada.to_dict('records')

    return figuraAproveitamentoDiario, saldo, roi, numApostas, investimento, oddMedia, simbolo, style, simbolo, style, tabela

# Aba análise geral (conteúdo e processamento)

@app.callback(
    Output('graficoAproveitamentoGeral', 'figure'),
    Output('abaGeralSaldo', 'children'),
    Output('abaGeralRoi', 'children'),
    Output('abaGeralQuantidadeApostas', 'children'),
    Output('abaGeralInvestimento', 'children'),
    Output('abaGeralOddMedia', 'children'),
    Output('abaGeralSaldoSimbolo', 'children'),
    Output('abaGeralSaldoSimbolo', 'style'),
    Output('abaGeralRoiSimbolo', 'children'),
    Output('abaGeralRoiSimbolo', 'style'),
    Input('abaGeralEsporte', 'value'),
    Input('abaGeralTipo', 'value'),
    Input('abaGeralCredito', 'value'),
    Input('abaGeralFinalizacao', 'value'),
    Input("modalNovaApostaBotaoFechar","n_clicks"),
)
def tab_geral(input_dpd_abaGeralEsporte, input_dpd_abaGeralTipo, input_dpd_abaGeralCreditoDeAposta, input_dpd_abaGeralFinalizacao, input_botao_novaApostaClose):

    dfApostas = leituraDB(NOME_ARQUIVO_APOSTAS)

    if dfApostas.empty:
        
        figuraAproveitamentoGeral = graficoAproveitamento(dfApostas, CORES) 

        saldo, roi, numApostas, investimento, oddMedia, simbolo, style = relatorioDBVazio()
        
    else:

        tabela_filtrada = dfApostas.loc[
            ((dfApostas['Esporte']==input_dpd_abaGeralEsporte) if input_dpd_abaGeralEsporte is not None else (dfApostas['Esporte']!=None)) 
            & ((dfApostas['Tipo']==input_dpd_abaGeralTipo) if input_dpd_abaGeralTipo is not None else (dfApostas['Tipo']!=None))
            & ((dfApostas['Crédito de aposta']==input_dpd_abaGeralCreditoDeAposta) if input_dpd_abaGeralCreditoDeAposta is not None else (dfApostas['Crédito de aposta']!=None))
            & ((dfApostas['Finalização']==input_dpd_abaGeralFinalizacao) if input_dpd_abaGeralFinalizacao is not None else (dfApostas['Finalização']!=None))
        ]

        figuraAproveitamentoGeral = graficoAproveitamento(tabela_filtrada, CORES) 

        saldo, roi, numApostas, investimento, oddMedia, bancaInicial, bancaAtual, simbolo, style = relatorioDB(tabela_filtrada, dfParametros, CORES)

    return figuraAproveitamentoGeral, saldo, roi, numApostas, investimento, oddMedia, simbolo, style, simbolo, style

# Modal de inserir apostas (abertura/fechamento)

@app.callback(
    Output("modalNovaAposta", "is_open"),
    Input("modalNovaApostaBotaoAbrir", "n_clicks"), 
    Input("modalNovaApostaBotaoFechar", "n_clicks"),
    Input("modalNovaAposta", "is_open"),
)
def modal_apostas_toggle(input_botao_novaApostaOpen, input_botao_novaApostaClose, input_modal_novaAposta):
    if input_botao_novaApostaOpen or input_botao_novaApostaClose:
        return not input_modal_novaAposta
    return input_modal_novaAposta

# Modal de inserir apostas (conteúdo e processamento) 

@app.callback(
    Output("modalNovaApostaAlertaInserir", "is_open"),
    Output("modalNovaApostaAlertaInserir", "children"),
    Output("modalNovaApostaAlertaInserir", "color"),
    Input("modalNovaApostaBotaoInserir","n_clicks"),
    State("modalNovaApostaCalendario", "date"), 
    State("modalNovaApostaEsporte", "value"),
    State("modalNovaApostaTipo", "value"),
    State("modalNovaApostaInvestimento", "value"),
    State("modalNovaApostaSwitchCredito", "value"),
    State("modalNovaApostaOdd", "value"),
    State("modalNovaApostaResultado", "value"),
    State("modalNovaApostaFinalizacao", "value"),
    State("modalNovaApostaRetirada", "value"), 
)
def modal_apostas_conteudo(input_botao_novaApostaInserir, state_calendario_novaAposta, state_dpd_novaApostaEsportes, state_dpd_novaApostaTipo, state_input_novaApostaInvestimento, state_switch_creditoDeAposta, state_input_novaApostaOdd, state_dpd_novaApostaResultado, state_dpd_novaApostaFinalizacao, state_input_novaApostaRetirada):

    if 'modalNovaApostaBotaoInserir' == ctx.triggered_id:
        if state_calendario_novaAposta and state_dpd_novaApostaEsportes and state_dpd_novaApostaTipo and state_input_novaApostaInvestimento and state_input_novaApostaOdd and state_dpd_novaApostaResultado and state_dpd_novaApostaFinalizacao is not None:
            
            apostaData = datetime.strptime(state_calendario_novaAposta, '%Y-%m-%d')
            apostaEsporte = state_dpd_novaApostaEsportes
            apostaTipo = state_dpd_novaApostaTipo
            apostaInvestimento = float(state_input_novaApostaInvestimento)
            apostaCreditoDeAposta = state_switch_creditoDeAposta
            apostaOdd = float(state_input_novaApostaOdd)
            apostaResultado = state_dpd_novaApostaResultado
            apostaFinalizacao = state_dpd_novaApostaFinalizacao
            apostaRetirada = state_input_novaApostaRetirada
            soma = 1

            if state_dpd_novaApostaFinalizacao == 'Normal': 

                apostaSaldo = calcularSaldoNormal(apostaResultado, apostaInvestimento, apostaCreditoDeAposta, apostaOdd)
                    
                dfApostas = leituraDB(NOME_ARQUIVO_APOSTAS)
                
                inserirAposta(dfApostas, apostaData, apostaEsporte, apostaTipo, apostaOdd, apostaInvestimento, apostaCreditoDeAposta, apostaFinalizacao, apostaResultado, apostaSaldo, soma, NOME_ARQUIVO_APOSTAS)
                
                time.sleep(0.1)

                mensagemAlerta, corAlerta, stateAlerta = mensagem('Sucesso','Aposta')

                return stateAlerta, mensagemAlerta, corAlerta
            else: 
                if state_input_novaApostaRetirada is not None:

                    apostaSaldo = calcularSaldoRetirada(apostaResultado, apostaInvestimento, apostaCreditoDeAposta, apostaRetirada)

                    dfApostas = leituraDB(NOME_ARQUIVO_APOSTAS)

                    inserirAposta(dfApostas, apostaData, apostaEsporte, apostaTipo, apostaOdd, apostaInvestimento, apostaCreditoDeAposta, apostaFinalizacao, apostaResultado, apostaSaldo, soma, NOME_ARQUIVO_APOSTAS)
     
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
    Input("modalNovaApostaFinalizacao", "value"), 
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
    Output("modalNovaApostaEsporte", "value"),
    Output("modalNovaApostaTipo", "value"),
    Output("modalNovaApostaInvestimento", "value"),
    Output("modalNovaApostaSwitchCredito", "value"),
    Output("modalNovaApostaOdd", "value"),
    Output("modalNovaApostaResultado", "value"),
    Output("modalNovaApostaFinalizacao", "value"),
    Output("modalNovaApostaRetirada", "value"), 
    Input("modalNovaApostaBotaoInserir","n_clicks"), 
    Input("modalNovaApostaBotaoFechar","n_clicks"),
    Input("modalNovaApostaEsporte", "value"),
    Input("modalNovaApostaTipo", "value"),
    Input("modalNovaApostaInvestimento", "value"),
    Input("modalNovaApostaSwitchCredito", "value"),
    Input("modalNovaApostaOdd", "value"),
    Input("modalNovaApostaResultado", "value"),
    Input("modalNovaApostaFinalizacao", "value"),
    Input("modalNovaApostaRetirada", "value"), 
)
def modal_aposta_limpeza(input_botao_novaApostaInserir, input_botao_novaApostaClose, input_dpd_novaApostaEsportes, input_dpd_novaApostaTipo, input_input_novaApostaInvestimento, input_switch_novaApostaCreditoDeAposta, input_input_novaApostaOdd, input_dpd_novaApostaResultado, input_dpd_novaApostaFinalizacao, input_input_novaApostaRetirada):
    if 'modalNovaApostaBotaoInserir' == ctx.triggered_id:
        if input_dpd_novaApostaEsportes and input_dpd_novaApostaTipo and input_input_novaApostaInvestimento and input_input_novaApostaOdd and input_dpd_novaApostaResultado and input_dpd_novaApostaFinalizacao is not None:
            if input_dpd_novaApostaFinalizacao == 'Normal':
                return input_dpd_novaApostaEsportes, input_dpd_novaApostaTipo, input_input_novaApostaInvestimento, False, None, None, input_dpd_novaApostaFinalizacao, None
            else:
                if input_input_novaApostaRetirada is not None:
                    return input_dpd_novaApostaEsportes, input_dpd_novaApostaTipo, input_input_novaApostaInvestimento, False, None, None, None, None
                else:
                    return input_dpd_novaApostaEsportes, input_dpd_novaApostaTipo, input_input_novaApostaInvestimento, False, input_input_novaApostaOdd, input_dpd_novaApostaResultado, input_dpd_novaApostaFinalizacao, input_input_novaApostaRetirada
        else:
            return input_dpd_novaApostaEsportes, input_dpd_novaApostaTipo, input_input_novaApostaInvestimento, False, input_input_novaApostaOdd, input_dpd_novaApostaResultado, input_dpd_novaApostaFinalizacao, input_input_novaApostaRetirada
    elif 'modalNovaApostaBotaoFechar' == ctx.triggered_id:
        return None, None, None, False, None, None, None, None
    else: 
        return input_dpd_novaApostaEsportes, input_dpd_novaApostaTipo, input_input_novaApostaInvestimento, input_switch_novaApostaCreditoDeAposta, input_input_novaApostaOdd, input_dpd_novaApostaResultado, input_dpd_novaApostaFinalizacao, input_input_novaApostaRetirada

# Modal de configurações (abertura/fechamento)

@app.callback(
    Output("modalConfiguracoes", "is_open"),
    Input("modalConfiguracoesBotaoAbrir", "n_clicks"), 
    Input("modalConfiguracoesBotaoFechar", "n_clicks"),
    Input("modalConfiguracoes", "is_open"),
)
def modal_config_toggle(input_botao_configOpen, input_botao_configClose, input_modal_config):
    if input_botao_configOpen or input_botao_configClose:
        return not input_modal_config
    return input_modal_config

# Modal de configurações (conteúdo e processamento)

@app.callback(
    Output("modalConfiguracoesAlertaEsporte", "is_open"),
    Output("modalConfiguracoesAlertaEsporte", "children"),
    Output("modalConfiguracoesAlertaEsporte", "color"),   
    Output("modalConfiguracoesAlertaBancaInicial", "is_open"),
    Output("modalConfiguracoesAlertaBancaInicial", "children"),
    Output("modalConfiguracoesAlertaBancaInicial", "color"),   
    Input("modalConfiguracoesBotaoInserirEsporte", "n_clicks"),
    Input("modalConfiguracoesBotaoInserirBancaInicial", "n_clicks"),
    State("modalConfiguracoesEsporte", "value"), 
    State("modalConfiguracoesBancaInicial", "value"), 
)
def modal_config_conteudo(input_botao_configInserirEsporte, input_botao_configBancaInicial, state_input_configEsporte, state_input_configBancaInicial):
    if 'modalConfiguracoesBotaoInserirEsporte' == ctx.triggered_id:
        if state_input_configEsporte is not None: 
            
            dfParametros = leituraDB(NOME_ARQUIVO_PARAMETROS)

            inserirParametro(dfParametros, 'Esporte', state_input_configEsporte, NOME_ARQUIVO_PARAMETROS)  

            time.sleep(0.1)

            mensagemAlerta, corAlerta, stateAlerta = mensagem('Sucesso','Esporte')

            return stateAlerta, mensagemAlerta, corAlerta, False, '', 'danger'
        else:
            
            time.sleep(0.1)
            
            mensagemAlerta, corAlerta, stateAlerta = mensagem('Erro','Esporte')

            return stateAlerta, mensagemAlerta, corAlerta, False, '', 'danger'
        
    elif 'modalConfiguracoesBotaoInserirBancaInicial' == ctx.triggered_id:
        if state_input_configBancaInicial is not None: 
            
            dfParametros = leituraDB(NOME_ARQUIVO_PARAMETROS)
            
            inserirParametro(dfParametros, 'Banca Inicial', state_input_configBancaInicial, NOME_ARQUIVO_PARAMETROS) 

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
    Output("modalConfiguracoesEsporte", "value"),
    Output("modalNovaApostaDivEsporte", "children"),
    Output("modalConfiguracoesBancaInicial", "value"),
    Input("modalConfiguracoesBotaoInserirEsporte", "n_clicks"),
    Input("modalConfiguracoesBotaoInserirBancaInicial", "n_clicks"),
    Input("modalConfiguracoesBotaoFechar", "n_clicks"),
    Input("modalConfiguracoesEsporte", "value"),
    Input("modalConfiguracoesBancaInicial", "value"),
)
def modal_config_limpeza(input_botao_configInserirEsporte, input_botao_configBancaInicial, input_botao_configClose, input_input_configEsporte, input_input_configBancaInicial):
    
    dfParametros = leituraDB(NOME_ARQUIVO_PARAMETROS)
    lista_esportes = list(dfParametros["Esporte"].dropna())

    dropdown = [
        dcc.Dropdown(
            lista_esportes, 
            #value='Todas', 
            id='modalNovaApostaEsporte',
            placeholder="Selecione um esporte...",
            style={
                'color':'black',
                "margin-top": "10px"
            }
        ),
    ]

    if 'modalConfiguracoesBotaoInserirEsporte' == ctx.triggered_id or 'modalConfiguracoesBotaoFechar' == ctx.triggered_id or 'modalConfiguracoesBotaoInserirBancaInicial' == ctx.triggered_id:
        return None, dropdown, None
    else:
        return input_input_configEsporte, dropdown, input_input_configBancaInicial

# Cards

@app.callback(
    Output("colunaBancaInicial", "children"),
    Output("colunaBancaAtual", "children"),
    Output("colunaSaldo", "children"),
    Output("colunaRoi", "children"),
    Input("modalNovaApostaBotaoFechar","n_clicks"),
    Input('colunaHeader','children')
)
def cards(input_botao_novaApostaClose, input_title_header):

    dfApostas = leituraDB(NOME_ARQUIVO_APOSTAS)
    dfParametros = leituraDB(NOME_ARQUIVO_PARAMETROS)

    saldo, roi, numApostas, investimento, oddMedia, bancaInicial, bancaAtual, simbolo, style = relatorioDB(dfApostas, dfParametros, CORES)

    return bancaInicial, bancaAtual, saldo, roi

########### ########### ###########
########### LOCAL HOST
########### ########### ###########

if __name__ == '__main__':
    app.run_server(debug=True)
    