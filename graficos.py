import plotly.express as px

def graficoBanca(dataframe, dadosX, dadosY, cores):
    
    grafico = px.line(dataframe, 
        x=dadosX, 
        y=dadosY, 
        markers= True,
        height=350
    )

    grafico.update_traces(
        line=dict(
            width=2,
            color=cores['linha_grafico']
        ),
        marker=dict(
            size=12,
            color=cores['marker_grafico'],
            opacity=0.8
        )
    )

    grafico.update_layout(
        #title='Banca',
        title_x=0.5,
        xaxis = dict( 
            title = 'Período',
            showgrid = True,
            zeroline = True,
            showline = False,
            showticklabels = True,
            gridwidth = 1,
            #tickformat= ',d'
            dtick='M1',
            tickmode = 'linear'
        ),
        yaxis = dict( 
            title = 'R$',
            showgrid = True,
            zeroline = True,
            showline = False,
            showticklabels = True,
            gridwidth = 1,
        ),
        plot_bgcolor=cores['background2'],
        paper_bgcolor=cores['background2'],
        font_color=cores['text'],
        autosize=True,
        margin=dict(
            t=20, b=0, l=0, r=0
        )
    )

    grafico.update_xaxes(
        showgrid=True,
        gridcolor=cores['grade']
    )

    grafico.update_yaxes(
        showgrid=True,
        gridcolor=cores['grade']
    )

    return grafico

def graficoAproveitamentoDiario(dataframe, cores):

    grafico = px.pie(
        dataframe, 
        values='Soma', 
        names='Resultado', 
        hole=0.5,
        height=400,
        color='Resultado',
        color_discrete_map = {
            'Acerto': cores['col_acerto'],
            'Erro': cores['col_erro'],
            'Retornada': cores['col_retornada']
        }
    )

    grafico.update_traces(
        textinfo='percent + value'
    )

    grafico.update_layout(
        title_x=0.5,
        plot_bgcolor=cores['background2'],
        paper_bgcolor=cores['background2'],
        font_color=cores['text'],
        autosize=True
    )

    return grafico

def graficoAproveitamentoGeral(dataframe, cores):

    grafico = px.pie(
        dataframe, 
        values='Soma', 
        names='Resultado', 
        hole=0.5,
        height=300,
        color='Resultado',
        color_discrete_map = {
            'Acerto': cores['col_acerto'],
            'Erro': cores['col_erro'],
            'Retornada': cores['col_retornada']
        }
    )

    grafico.update_traces(
        textinfo='percent + value'
    )

    grafico.update_layout(
        title_x=0.5,
        plot_bgcolor=cores['background2'],
        paper_bgcolor=cores['background2'],
        font_color=cores['text'],
        autosize=True,
        margin=dict(
            t=20, b=0, l=0, r=0
        )
    )

    return grafico