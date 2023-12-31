import math
import pandas as pd
import os

#Função para ler o DB

def leituraDB(nomeArquivo):

    dir = os.getcwd()
    filePath = dir + '\\' + nomeArquivo
    dataframe = pd.read_excel(filePath)

    return dataframe

#Função que retorna os parâmetros de análise de um DB vazio

def relatorioDBVazio():
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

def relatorioDB(dataframe, parametros, cores):

    saldo = float(round(dataframe['Saldo'].sum(),2))

    if saldo > 0:
        simbolo = '▲'
        style = {
            'textAlign': 'center',
            'color': cores['colunaAcerto']
        }
    elif saldo < 0: 
        simbolo = '▼'
        style = {
            'textAlign': 'center',
            'color': cores['colunaErro']
        }
    else:
        simbolo = ''
        style = {
            'textAlign': 'center',
            'color':'white'
        }

    if dataframe["Investimento"].sum() == 0:
        roi = '0 %'
    else:
        roi = str(round(saldo*100/dataframe["Investimento"].sum(),2)) + ' %'

    if math.isnan(dataframe["Odd"].mean()) == True:
        oddMedia = '0.00'  
    else:
        oddMedia = str(round(dataframe["Odd"].mean(),2))

    bancaInicial = round(float(parametros["Banca Inicial"].dropna()),2)
    bancaAtual = 'R$ ' + str(round(bancaInicial + saldo,2))
    saldo = 'R$ ' + str(saldo)
    numApostas = str(dataframe['Saldo'].count())
    investimento = 'R$ ' + str(round(dataframe['Investimento'].sum(),2))

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

def calcularSaldoNormal(resultado, investimento, creditoDeAposta, odd):

    if creditoDeAposta == True:
        if resultado == 'Acerto':
            saldo = round((investimento * odd)-investimento,2)
        elif resultado == 'Erro':
            saldo = 0
        elif resultado == 'Retornada':
            saldo = 0
        return saldo
    else: 
        if resultado == 'Acerto':
            saldo = round((investimento * odd)-investimento,2)
        elif resultado == 'Erro':
            saldo = round(-1*investimento,2)
        elif resultado == 'Retornada':
            saldo = 0
        return saldo
#Função para definir o saldo da aposta por finalização retirada

def calcularSaldoRetirada(resultado, investimento, creditoDeAposta, valorRetirado):
        
    if creditoDeAposta == True:
        if resultado == 'Acerto':
            saldo = round(valorRetirado-investimento,2)
        elif resultado == 'Erro':
            saldo = round(valorRetirado-investimento,2)
        elif resultado == 'Retornada':
            saldo = 0
        return saldo
    else:
        if resultado == 'Acerto':
            saldo = round(valorRetirado-investimento,2)
        elif resultado == 'Erro':
            saldo = round(valorRetirado-investimento,2)
        elif resultado == 'Retornada':
            saldo = 0
        return saldo

#Função para inserir aposta no DB

def inserirAposta(dataframe, apostaData, apostaEsporte, apostaTipo, apostaOdd, apostaInvestimento, apostaCreditoDeAposta, apostaFinalizacao, apostaResultado, apostaSaldo, soma, nomeArquivo):
    
    if apostaCreditoDeAposta == True:
        apostaCreditoDeAposta = 'Sim'
    else:
        apostaCreditoDeAposta = 'Não'

    novaAposta = [apostaData, apostaEsporte, apostaTipo, apostaOdd, apostaInvestimento, apostaCreditoDeAposta, apostaFinalizacao, apostaResultado, apostaSaldo, soma]
    df_novaAposta = pd.DataFrame([novaAposta], columns=list(['Data', 'Esporte', 'Tipo', 'Odd', 'Investimento', 'Crédito de aposta', 'Finalização', 'Resultado', 'Saldo', 'Soma']))
    dataframe = pd.concat([dataframe,df_novaAposta], ignore_index=True)
    
    dir = os.getcwd()
    filePath = dir + '\\' + nomeArquivo

    with pd.ExcelWriter(
        filePath, 
        mode="a", 
        engine="openpyxl", 
        if_sheet_exists="overlay",
        date_format="YYYY-MM-DD",
        datetime_format="YYYY-MM-DD HH:MM:SS"
    ) as writer:
        dataframe.to_excel(writer, sheet_name="Plan1", index=False)  

#Função para inserir parâmetro no DB

def inserirParametro(dataframe, tipo, novoParametro, nomeArquivo):

    if tipo == 'Esporte':

        df_novoParametro = pd.DataFrame([novoParametro], columns=list([tipo]))
        dataframe = pd.concat([dataframe,df_novoParametro], ignore_index=True)   
    
    elif tipo == 'Banca Inicial': 

        dataframe['Banca Inicial'][0] = novoParametro

    dir = os.getcwd()
    filePath = dir + '\\' + nomeArquivo

    with pd.ExcelWriter(
        filePath, 
        mode="a", 
        engine="openpyxl", 
        if_sheet_exists="overlay",
        date_format="DD-MM-YYYY",
        datetime_format="DD-MM-YYYY"
    ) as writer:
        dataframe.to_excel(writer, sheet_name="Plan1", index=False) 
            