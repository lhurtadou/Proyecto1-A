import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Lee el archivo CSV
file_path = '../Enunciado/DatosPS.csv'
df = pd.read_csv(file_path)

custom_order = ['diciembre', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 
               'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre']
df['Mes'] = pd.Categorical(df['Mes'], categories=custom_order, ordered=True)

# Convertir otras columnas a categóricas para mejor visualización
df['Dia Semana'] = pd.Categorical(df['Dia Semana'], categories=['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'], ordered=True)
df['Momento Dia'] = pd.Categorical(df['Momento Dia'], categories=['Madrugada', 'Mañana', 'Tarde', 'Noche'], ordered=True)

# Agrupar datos por Día de la semana, Mes, y Momento del día
df_grouped = df.groupby(['Dia Semana', 'Mes', 'Momento Dia'], as_index=False).agg({'Rented Bike Count': 'sum'})

# Crear el gráfico de barras apiladas
fig_barras = px.bar(
    df_grouped,
    x="Dia Semana",
    y="Rented Bike Count",
    color="Momento Dia",
    barmode="stack",  
    facet_col="Mes",
    facet_col_wrap=4,  
    title="Número de bicicletas",
    labels={"Rented Bike Count": "Número de bicicletas"}
)


fig_barras.update_layout(
    title={
        'text': "Visualización: Número de bicicletas de acuerdo con momento del día, día de la semana y mes",
        'font': dict(family="Lato", size=24, color='#4682B4', weight="bold"),  # Cambia la fuente, tamaño, color y negrilla
    },
    margin=dict(t=100, b=50, l=100, r=50),  
    xaxis_title="Día de la semana",
    xaxis=dict(tickangle=-45),  
    width=1500,  
    height=710,  
    autosize=False  
)


scatter_variables = {
    'Temperature(C)': 'Temperature(C)',
    'Humidity(%)': 'Humidity(%)',
    'Wind speed (m/s)': 'Wind speed (m/s)',
    'Visibility (10m)': 'Visibility (10m)',
    'Dew point temperature(C)': 'Dew point temperature(C)',
    'Solar Radiation (MJ/m2)': 'Solar Radiation (MJ/m2)',
    'Rainfall(mm)': 'Rainfall(mm)',
    'Snowfall (cm)': 'Snowfall(cm)'
}


external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap'
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Estilos
label_style = {
    'font-weight': 'bold', 
    'color': '#4B0082',  # Morado muy oscuro
    'font-family': 'Lato, sans-serif',
    'font-style': 'italic'  # Letra en cursiva
}


title_style2 = {
    'font-weight': 'bold',
    'text-align': 'center',
    'color': '#4682B4',
    'font-family': 'Lato, sans-serif'
}

title_style = {
    'font-weight': 'bold',
    'text-align': 'left',
    'color': '#4682B4',  
    'font-family': 'Lato, sans-serif',
    'font-size': '24px'  
}

style={
        'display': 'flex',
        'flex-direction': 'column',
        'align-items': 'center',  # Centra el contenedor principal horizontalmente
        'justify-content': 'center',  # Centra el contenedor principal verticalmente si el contenedor tiene altura
        'height': '100vh'  # Opcional: Ajusta la altura del contenedor al 100% de la altura de la ventana
}

output_style = {
    'fontFamily': 'Lato',               # Fuente Lato
    'fontSize': '20px',                 # Tamaño de la letra
    'textAlign': 'center',              # Centrar el texto
    'display': 'flex',                  # Usar flexbox para alinear
    'justifyContent': 'center',         # Centrar horizontalmente
    'alignItems': 'center',             # Centrar verticalmente
    'backgroundColor': '#E6F7FF',       # Fondo verde muy claro
    'border': '5px solid #4682B4',      # Bordes gruesos verdes
    'borderRadius': '10px',             # Bordes ligeramente redondeados
    'width': '250px',                   # Ancho de la caja (rectangular)
    'height': '60px',                  # Altura de la caja (rectangular)
    'margin': 'auto'                    # Centrar horizontalmente en la página
}

# Función para calcular el resultado de la simulación de rentabilidad
def calcular_respuesta(hour, temperature, wind_speed, visibility, solar_radiation, rainfall,
                       season, holiday, functioning_day, dia_semana, mes, momento_dia):

    intercept = -1114.2488
    coef_hour = -25.5986
    coef_temperature = 30.6237
    coef_wind_speed = 24.3676
    coef_visibility = 0.1330
    coef_solar_radiation = 28.5253
    coef_rainfall = -7.433e-13

    # Coeficientes de las dummies
    coef_season_spring = -217.5825
    coef_season_summer = -270.4350
    coef_season_winter = -241.3621

    coef_holiday_no = 161.8398
    coef_functioning_day_yes = 983.8418

    # Coeficientes de los días de la semana (domingo como base)
    coef_dia_lunes = 95.7357
    coef_dia_martes = 148.5544
    coef_dia_miercoles = 110.0293
    coef_dia_jueves = 93.5541
    coef_dia_viernes = 158.7148
    coef_dia_sabado = 74.6656

    # Coeficientes de los meses (abril como base)
    coef_mes_enero = -81.7086
    coef_mes_febrero = -118.2155
    coef_mes_marzo = -110.6664
    coef_mes_mayo = 99.1059
    coef_mes_junio = 205.8651
    coef_mes_julio = -174.9433
    coef_mes_agosto = -301.3568
    coef_mes_septiembre = -253.7242
    coef_mes_octubre = -45.3016
    coef_mes_noviembre = -85.8435
    coef_mes_diciembre = -41.4381

    # Coeficientes del momento del día (madrugada como base)
    coef_momento_manana = 479.4287
    coef_momento_tarde = 657.0179
    coef_momento_noche = 1095.5844

    Y = intercept

    # Variables continuas
    Y += coef_hour * hour
    Y += coef_temperature * temperature
    Y += coef_wind_speed * wind_speed
    Y += coef_visibility * visibility
    Y += coef_solar_radiation * solar_radiation
    Y += coef_rainfall * rainfall

    # Variables categóricas: Seasons (base: fall/otoño)
    if season == 'Primavera':
        Y += coef_season_spring
    elif season == 'Verano':
        Y += coef_season_summer
    elif season == 'Invierno':
        Y += coef_season_winter

    # Holiday (base: Holiday_Yes)
    if holiday == 'No Festivo':
        Y += coef_holiday_no

    # Functioning Day (base: Functioning Day_No)
    if functioning_day == 'Sí':
        Y += coef_functioning_day_yes

    # Día de la semana (base: domingo)
    if dia_semana == 'Lunes':
        Y += coef_dia_lunes
    elif dia_semana == 'Martes':
        Y += coef_dia_martes
    elif dia_semana == 'Miercoles':
        Y += coef_dia_miercoles
    elif dia_semana == 'Jueves':
        Y += coef_dia_jueves
    elif dia_semana == 'Viernes':
        Y += coef_dia_viernes
    elif dia_semana == 'Sabado':
        Y += coef_dia_sabado

    # Mes (base: abril)
    if mes == 'Enero':
        Y += coef_mes_enero
    elif mes == 'Febrero':
        Y += coef_mes_febrero
    elif mes == 'Marzo':
        Y += coef_mes_marzo
    elif mes == 'Mayo':
        Y += coef_mes_mayo
    elif mes == 'Junio':
        Y += coef_mes_junio
    elif mes == 'Julio':
        Y += coef_mes_julio
    elif mes == 'Agosto':
        Y += coef_mes_agosto
    elif mes == 'Septiembre':
        Y += coef_mes_septiembre
    elif mes == 'Octubre':
        Y += coef_mes_octubre
    elif mes == 'Noviembre':
        Y += coef_mes_noviembre
    elif mes == 'Diciembre':
        Y += coef_mes_diciembre

    # Momento del día (base: madrugada)
    if momento_dia == 'Mañana':
        Y += coef_momento_manana
    elif momento_dia == 'Tarde':
        Y += coef_momento_tarde
    elif momento_dia == 'Noche':
        Y += coef_momento_noche

    return html.Strong(f"Utilidad: ${round((Y * 7) - (Y * 3.5), 2):.2f} Dólares")

# Layout de la aplicación
app.layout = html.Div(children=[
    html.H1(children='Sistema de Bicicletas Compartidas: Visualización y Simulación', style=title_style2),

    # Primera visualización: gráfico de barras
    dcc.Graph(figure=fig_barras, style=style ),

    # Segunda visualización: gráficos de dispersión
    html.Div([
        html.H2('Visualización: Bicicletas Alquiladas con respecto a Factores Ambientales y Climáticos', style=title_style),
        dcc.Dropdown(
            id='scatter-variable',
            options=[{'label': var, 'value': var} for var in scatter_variables.keys()],
            value='Temperature(C)'
        ),
        dcc.Graph(id='scatter-graph')
    ], style={'padding': '20px'}),

    # Tercera visualización: simulación de rentabilidad
# Tercera visualización: simulación de rentabilidad
html.Div(
    [
        html.H2("Simulación: Utilidad Bicicletas Compartidas", style=title_style),
        html.H6("Modifique el valor de cada una de las variables para ver el resultado de Utilidad", style={'text-align': 'left'}),
        html.Div([
            html.Div([
                html.Label("Temperatura (°C)", style=label_style),
                dcc.Slider(-17.8, 39.4, 5.5, value=-3, id='temperatura'),
                html.Br(),
                html.Label("Hora del día", style=label_style),
                dcc.Slider(0, 23, 1, value=12, id='hour'),
                html.Br(),
                html.Label("Velocidad del viento (m/s)", style=label_style),
                dcc.Slider(
                    min=0,
                    max=10,
                    step=1,
                    value=12,
                    id='wind_speed',
                ),
                html.Br(),
                html.Label("Visibilidad (metros)", style=label_style),
                dcc.Slider(
                min=0,
                max=2000,
                step=100,
                value=100,
                marks={i: f'{i}' for i in range(0, 2001, 100)},  
                id='visibility'
                ),
                html.Br(),
                html.Label("Festivo", style=label_style),
                dcc.Dropdown(id='holiday', options=[
                    {'label': 'No Festivo', 'value': 'No Festivo'},
                    {'label': 'Festivo', 'value': 'Festivo'},
                ], value='Festivo'),
                html.Br(),
                html.Label("Día de Funcionamiento", style=label_style),
                dcc.Dropdown(id='dia_laboral', options=[
                    {'label': 'Sí', 'value': 'Sí'},
                    {'label': 'No', 'value': 'No'},
                ], value='Sí'),
                html.Br(),
                html.Label("Momento del Día", style=label_style),
                dcc.Dropdown(id='momento_dia', options=[
                    {'label': 'Mañana', 'value': 'Mañana'},
                    {'label': 'Madrugada', 'value': 'Madrugada'},
                    {'label': 'Tarde', 'value': 'Tarde'},
                    {'label': 'Noche', 'value': 'Noche'},
                ], value='Mañana'),
                html.Br(),
            ], style={'width': '45%', 'display': 'inline-block', 'vertical-align': 'top'}),
            html.Div([
                html.Label("Radiación Solar (MJ/m²)", style=label_style),
                dcc.Input(id='solar_radiation', type='number', value=0.5),
                html.Br(),
                html.Label("Precipitación (mm)", style=label_style),
                dcc.Input(id='rainfall', type='number', value=0),
                html.Br(),
                html.Label("Estación del año", style=label_style),
                dcc.Dropdown(id='seasons', options=[
                    {'label': 'Primavera', 'value': 'Primavera'},
                    {'label': 'Verano', 'value': 'Verano'},
                    {'label': 'Otoño', 'value': 'Otoño'},
                    {'label': 'Invierno', 'value': 'Invierno'},
                ], value='Verano'),
                html.Br(),
                html.Label("Día de la Semana", style=label_style),
                dcc.Dropdown(id='dia_semana', options=[
                    {'label': 'Lunes', 'value': 'Lunes'},
                    {'label': 'Martes', 'value': 'Martes'},
                    {'label': 'Miercoles', 'value': 'Miercoles'},
                    {'label': 'Jueves', 'value': 'Jueves'},
                    {'label': 'Viernes', 'value': 'Viernes'},
                    {'label': 'Sabado', 'value': 'Sabado'},
                    {'label': 'Domingo', 'value': 'Domingo'},
                ], value='Lunes'),
                html.Br(),
                html.Label("Mes", style=label_style),
                dcc.Dropdown(id='mes', options=[
                    {'label': 'Enero', 'value': 'Enero'},
                    {'label': 'Febrero', 'value': 'Febrero'},
                    {'label': 'Marzo', 'value': 'Marzo'},
                    {'label': 'Abril', 'value': 'Abril'},
                    {'label': 'Mayo', 'value': 'Mayo'},
                    {'label': 'Junio', 'value': 'Junio'},
                    {'label': 'Julio', 'value': 'Julio'},
                    {'label': 'Agosto', 'value': 'Agosto'},
                    {'label': 'Septiembre', 'value': 'Septiembre'},
                    {'label': 'Octubre', 'value': 'Octubre'},
                    {'label': 'Noviembre', 'value': 'Noviembre'},
                    {'label': 'Diciembre', 'value': 'Diciembre'},
                ], value='Enero'),
                html.Br(),
            ], style={'width': '45%', 'display': 'inline-block'}),
        ], style={'display': 'flex', 'justify-content': 'center'}),
        html.Div(id='output-container', style=output_style, children="Resultado: 0")
    ], style={'padding': '20px'})
])

# Callbacks para actualizar el gráfico de dispersión y la simulación de rentabilidad
@app.callback(
    Output('scatter-graph', 'figure'),
    [Input('scatter-variable', 'value')]
)
def update_scatter(selected_variable):
    fig = px.scatter(
        df, 
        x=selected_variable, 
        y='Rented Bike Count', 
        trendline='ols', 
        title=f'Relación entre {selected_variable} y Número de bicicletas alquiladas',
        labels={selected_variable: selected_variable, 'Rented Bike Count': 'Número de bicicletas alquiladas'}
    )
    fig.update_layout(title_x=0.5) 
    return fig

@app.callback(
    Output('output-container', 'children'),
    [Input('temperatura', 'value'),
     Input('hour', 'value'),
     Input('wind_speed', 'value'),
     Input('visibility', 'value'),
     Input('solar_radiation', 'value'),
     Input('rainfall', 'value'),
     Input('seasons', 'value'),
     Input('dia_semana', 'value'),
     Input('mes', 'value'),
     Input('holiday', 'value'),
     Input('dia_laboral', 'value'),
     Input('momento_dia', 'value')]
)
def update_output(temperatura, hour, wind_speed, visibility, solar_radiation, rainfall,
                   seasons, dia_semana, mes, holiday, dia_laboral, momento_dia):
    resultado = calcular_respuesta(hour, temperatura, wind_speed, visibility, solar_radiation, rainfall,
                                   seasons, holiday, dia_laboral, dia_semana, mes, momento_dia)
    return resultado

# Corre la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
