import math

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


