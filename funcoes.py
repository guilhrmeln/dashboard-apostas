import math
import pandas as pd

#Função que retorna os parâmetros de análise de um DB vazio

def relatorio_dbVazio():
    saldo = 'Sem dados'
    roi = 'Sem dados'
    numApostas = 'Sem dados'
    investimento = 'Sem dados'
    oddMedia = 'Sem dados'
    simbolo = ''
    style = {
        'textAlign': 'center',
        'color':'white'
    }
    
    return saldo, roi, numApostas, investimento, oddMedia, simbolo, style

#Função que retorna os parâmetros de análise do DB, seja ele completo ou filtrado

def relatorio_db(dataframe, parametros, colors):

    saldo = float(round(dataframe['Saldo'].sum(),2))

    if saldo > 0:
        simbolo = '▲'
        style = {
            'textAlign': 'center',
            'color': colors['col_acerto']
        }
    elif saldo < 0: 
        simbolo = '▼'
        style = {
            'textAlign': 'center',
            'color': colors['col_erro']
        }
    else:
        simbolo = ''
        style = {
            'textAlign': 'center',
            'color':'white'
        }

    roi = round(saldo*100/dataframe["Investimento"].sum(),2)
    oddMedia = dataframe["Odd"].mean()
    
    if math.isnan(roi and oddMedia) == True:
        roi = '0 %'
        oddMedia = '0.00'
    else:
        roi = str(roi) + ' %'
        oddMedia = str(round(oddMedia,2))

    bancaInicial = round(float(parametros["Banca Inicial"].dropna()),2)
    bancaAtual = 'R$' + " " + str(bancaInicial + saldo)
    saldo = 'R$' + " " + str(saldo)
    numApostas = str(dataframe['Saldo'].count())
    investimento = 'R$' + " " + str(round(dataframe['Investimento'].sum(),2))

    return saldo, roi, numApostas, investimento, oddMedia, bancaInicial, bancaAtual, simbolo, style

#Função para mensagens de alerta

def mensagem(resultado,tipo):

    if resultado == 'Sucesso':
        if tipo == 'Aposta':
            corAlerta = 'success'
            mensagemAlerta = 'Aposta adicionada com sucesso!'
            stateAlerta = True
        elif tipo == 'Esporte':
            corAlerta = 'success'
            mensagemAlerta = 'Esporte adicionado com sucesso!'
            stateAlerta = True
        elif tipo == 'Banca':
            corAlerta = 'success'
            mensagemAlerta = 'Banca inicial definida com sucesso! Atualize a página para o novo valor entrar em vigor.'
            stateAlerta = True
    elif resultado == 'Erro':
        if tipo == 'Aposta':
            corAlerta = 'danger'
            mensagemAlerta = 'ERRO: informe todos os dados da aposta antes de adicioná-la.'
            stateAlerta = True
        elif tipo == 'Esporte':
            corAlerta = 'danger'
            mensagemAlerta = 'ERRO: informe um novo esporte antes de adicioná-lo.'
            stateAlerta = True
        elif tipo == 'Banca':
            corAlerta = 'danger'
            mensagemAlerta = 'ERRO: informe um valor para banca inicial antes de adicioná-la.'
            stateAlerta = True
    else:
        mensagemAlerta = '...'
        corAlerta = 'success'
        stateAlerta = False    

    return mensagemAlerta, corAlerta, stateAlerta

#Função para definir o saldo da aposta por finalização normal

def calcularSaldoNormal(resultado, investimento, odd):
    if resultado == 'Acerto':
        saldo = round((investimento * odd)-investimento,2)
    elif resultado == 'Erro':
        saldo = round(-1*investimento,2)
    elif resultado == 'Retornada':
        saldo = 0
    return saldo

#Função para definir o saldo da aposta por finalização retirada

def calcularSaldoRetirada(resultado, investimento, valorRetirado):
    if resultado == 'Acerto':
        saldo = round(valorRetirado-investimento,2)
    elif resultado == 'Erro':
        saldo = round(valorRetirado-investimento,2)
    elif resultado == 'Retornada':
        saldo = 0
    return saldo

#Função para inserir aposta no DB

def inserirAposta(dataframe, apostaData, apostaEsporte, apostaTipo, apostaOdd, apostaInvestimento, apostaFinalizacao, apostaResultado, apostaSaldo, soma):
    
    novaAposta = [apostaData, apostaEsporte, apostaTipo, apostaOdd, apostaInvestimento, apostaFinalizacao, apostaResultado, apostaSaldo, soma]
    df_novaAposta = pd.DataFrame([novaAposta], columns=list(['Data', 'Esporte', 'Tipo', 'Odd', 'Investimento', 'Finalização', 'Resultado', 'Saldo', 'Soma']))
    df_concat = pd.concat([dataframe,df_novaAposta], ignore_index=True)
    
    with pd.ExcelWriter(
        r"E:\Programação\Python\Projetos\Dashboard Apostas\db_apostas.xlsx", 
        mode="a", 
        engine="openpyxl", 
        if_sheet_exists="overlay",
        date_format="YYYY-MM-DD",
        datetime_format="YYYY-MM-DD HH:MM:SS"
    ) as writer:
        df_concat.to_excel(writer, sheet_name="Plan1", index=False)  

    return