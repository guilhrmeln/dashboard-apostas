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
            color=cores['graficoLinha']
        ),
        marker=dict(
            size=12,
            color=cores['graficoMarcador'],
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
        plot_bgcolor=cores['backgroundGrafite'],
        paper_bgcolor=cores['backgroundGrafite'],
        font_color=cores['texto'],
        autosize=True,
        margin=dict(
            t=20, b=0, l=0, r=0
        )
    )

    grafico.update_xaxes(
        showgrid=True,
        gridcolor=cores['graficoGrade']
    )

    grafico.update_yaxes(
        showgrid=True,
        gridcolor=cores['graficoGrade']
    )

    return grafico

def graficoAproveitamento(dataframe, cores):

    grafico = px.pie(
        dataframe, 
        values='Soma', 
        names='Resultado', 
        hole=0.5,
        height=300,
        color='Resultado',
        color_discrete_map = {
            'Acerto': cores['colunaAcerto'],
            'Erro': cores['colunaErro'],
            'Retornada': cores['colunaRetornada']
        }
    )

    grafico.update_traces(
        textinfo='percent + value'
    )

    grafico.update_layout(
        title_x=0.5,
        plot_bgcolor=cores['backgroundGrafite'],
        paper_bgcolor=cores['backgroundGrafite'],
        font_color=cores['texto'],
        autosize=True,
        margin=dict(
            t=20, b=0, l=0, r=0
        )
    )

    return grafico