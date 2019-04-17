import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np


def brownian(moves):
    particle = [(0, 0)]
    array = np.random.normal(0, 1, (moves, 2))
    for i in range(1, moves):
        particle.append((np.add(particle[i-1][0], array[i][0]),
                         np.add(particle[i-1][1], array[i][1])
                         ))

    #return trace


def sredni_kwadrat(moves):
    array = np.random.normal(0, 1, (moves, 2))
    kwadraty = []
    sumX = 0
    sumY= 0
    X = []
    Y = []
    for i in range(0, moves):
        sumX += array[i][0]
        sumY += array[i][1]
        X.append(sumX)
        Y.append(sumY)
    for i in range(0, moves):
        kwadraty.append((i, X[i]**2 + Y[i]**2))
    return kwadraty


def wykres_sredni(n, moves):
    data = []
    result = []
    for i in range(0, n):
        data.append(sredni_kwadrat(moves))
    for i in range(0, n):
        sum_total = 0
        for j in range(0, moves):
            sum_total += data[j][i][1]
        result.append((i, sum_total/n))

    trace = go.Scatter(
        x=[i[0] for i in result],
        y=[j[1] for j in result]
    )
    data = [trace]
    layout = go.Layout(
        xaxis=dict(title='t'),
        yaxis=dict(title='a^2'),
        showlegend=False
    )
    fig = go.Figure(data=data, layout=layout,)
    py.plot(fig, filename='basic-line',
            auto_open=True)


def multiple(n):
    data = []
    for i in range(0, n):
        data.append(brownian(1000))
    layout = go.Layout(showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    py.plot(data, filename='basic-line',
            auto_open=True,
            layout=layout)
    #pio.write_image(data, "1000.png")


def gestosc(moves):
    particle = [(0, 0)]
    array = np.random.normal(0, 1, (moves, 2))
    for i in range(1, moves):
        particle.append((np.add(particle[i-1][0], array[i][0]),
                         np.add(particle[i-1][1], array[i][1])
                         ))
    return particle


def cala_gestosc(n, moves):
    data = []
    for i in range(0, n):
        data.append(gestosc(moves))
    rozklad = np.zeros((20, 20))
    for i in range(0, n):
        X = int(np.floor(data[i][moves-1][0]/10))
        Y = int(np.floor(data[i][moves-1][1]/10))
        if -10 < X < 10 and -10 < Y < 10:
            rozklad[X+10][Y+10] += 1

    layout = go.Layout(showlegend=False)
    data = go.Histogram2d(
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='surface'
            )

