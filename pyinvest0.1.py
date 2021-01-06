import streamlit as st
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import os
import plotly.express as px
import time
from functools import reduce
import gc
from datetime import datetime, timedelta

sns.set()
print('GC: ', gc.collect())

# FOLDER = './data/'
FOLDER = './stocks/'

stocks = os.listdir(FOLDER)
# print(stocks)

def percentChange(startPoint, currentPoint):
    try:
        x = ((float(currentPoint) - startPoint) / abs(startPoint)) * 100.00
        if x == 0.0:
            return 0.000000001
        else:
            return x
    except:
        return 0.0001


class Singleton(object):
    ''' Classe que instância um único objeto para toda a sessão
    '''

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(
                                      cls, *args, **kwargs)
        return cls._instance

    def set_dataframe(self, stock):
        self.df = pd.read_csv(FOLDER + stock, parse_dates=True, usecols=['Date', 'Adj_Close'])
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.stock = stock.rstrip('.csv')

    def plot_chart(self):
        fig = px.line(self.df, x="Date", y="Adj_Close", title=self.stock)
        st.plotly_chart(fig)

    def __len__(self):
        return self.df.shape[0]

    def start(self, pct):
        index = int(pct*len(self))
        it = 0
        self.accuracyArray = []
        lastLen = 0
        with st.spinner('Aguarde...'):
            start_time = time.time()
            while index < len(self):
                avgLine = self.df['Adj_Close'][:index]
                dates = self.df['Date'][:index]

                patternAr, performanceAr = self.pattern_storage(avgLine)
                dates, patForRec = self.current_pattern(avgLine, dates)
                patFound, plotPatAr = self.pattern_recognition(patternAr, patForRec)
                if patFound:    
                    self.plot(self.df['Adj_Close'], index, dates, performanceAr, plotPatAr, patternAr, patForRec)

                end_time = time.time() - start_time
                st.text(f'Processamento levou {int(end_time)} segundos para {it} amostras.')
                it += 1
                index += 1
                if self.accuracyArray:
                    tam = len(self.accuracyArray)
                    accuracyAverage = sum(self.accuracyArray)/tam
                    if lastLen < tam:
                        st.text(f'Acurácia é de {int(accuracyAverage)}% depois de {tam} predições.')
                        lastLen = tam

    def plot(self, data, index, dates, performanceAr, plotPatAr, patternAr, patForRec):
        predArray = []

        plt.figure(figsize=(10, 6))

        lines = []
        color = []

        predictedOutcomesAr = []

        max_date = max(dates)

        for eachPatt in plotPatAr:
            futurePoints = patternAr.index(eachPatt)

            if performanceAr[futurePoints] > patForRec[29]:
                pcolor = '#24bc00'
                predArray.append(1.000)
            else:
                pcolor = '#d40000'
                predArray.append(-1.000)

            plt.plot(dates, eachPatt)
            lines.append(eachPatt)
            predictedOutcomesAr.append(performanceAr[futurePoints])
            
            color.append(pcolor)

            plt.scatter(max_date+timedelta(days=5), performanceAr[futurePoints], c=pcolor, alpha=.3)

        realOutcomeRange = data[index+20:index+30]
        realAvgOutcome = reduce(lambda x, y: x+y, realOutcomeRange)/len(realOutcomeRange)
        realMovement = percentChange(data[index], realAvgOutcome)
        predictedAvgOutcome = reduce(lambda x, y: x+y, predictedOutcomesAr)/len(predictedOutcomesAr)

        predictionAverage = reduce(lambda x, y: x+y, predArray)/len(predArray)

        print(predictionAverage)
        if predictionAverage < 0:
            st.text("Previsão de baixa")
            print('drop prediction')
            print(patForRec[29])
            print(realMovement)
            if realMovement < patForRec[29]:
                self.accuracyArray.append(100)
            else:
                self.accuracyArray.append(0)

        if predictionAverage > 0:
            st.text("Previsão de alta")
            print('rise prediction')
            print(patForRec[29])
            print(realMovement)
            if realMovement > patForRec[29]:
                self.accuracyArray.append(100)
            else:
                self.accuracyArray.append(0)
    
        plt.scatter(max_date+timedelta(days=10), realMovement, c='#54fff7', s=25)
        plt.scatter(max_date+timedelta(days=10), predictedAvgOutcome, c='b', s=25)

        plt.plot(dates, patForRec, '#54fff7', linewidth=3)

        plt.grid(True)
        plt.xticks(rotation=45)
        plt.subplots_adjust(bottom=0.23)
        plt.title(f'Reconhecimento de padrões - {self.stock}')
        plt.show()
        st.pyplot()

    def pattern_storage(self, avgLine):
        patternAr = []
        performanceAr = []

        x = len(avgLine)-60

        y = 31
        while y < x:
            pattern = []

            for i in range(29, -1, -1):
                pattern.append(percentChange(avgLine[y - 30], avgLine[y - i]))

            outcomeRange = avgLine[y+20:y+30]
            currentPoint = avgLine[y]
            try:
                avgOutcome = reduce(lambda x, y: x+y, outcomeRange)/len(outcomeRange)
            except Exception as e:
                print(str(e))
                avgOutcome = 0

            futureOutcome = percentChange(currentPoint, avgOutcome)
    
            patternAr.append(pattern)
            performanceAr.append(futureOutcome)

            y += 1

        return patternAr, performanceAr

    def current_pattern(self, avgLine, dates):
        patForRec = avgLine.iloc[-30:].apply(lambda x: percentChange(avgLine.iloc[-31], x)).values
        return dates.iloc[-30:], patForRec

    def pattern_recognition(self, patternAr, patForRec):
        plotPatAr = []
        patFound = False

        for eachPattern in patternAr[:-5]:
            l = []
            for i in range(0,30):
                sim = 100.00 - abs(percentChange(eachPattern[i], patForRec[i]))

                if i < 15 and sim <= 50:
                    break

                l.append(sim)
    
            howSim = sum(l)/30.0

            if howSim > 70:
                patFound = True
                plotPatAr.append(eachPattern)

        return patFound, plotPatAr


def main():
    # st.image('images/logo.png', width=400)
    st.title('PyInvest v0.1 - Pattern Recognition')
    #https://github.com/MatheusMullerGit

    stock = st.selectbox('Qual ação?: ', stocks)

    c = Singleton()
    c.set_dataframe(stock)    

    c.plot_chart()

    st.text(f'O tamanho do dataframe é {len(c)}')

    st.header("Efetuar reconhecimento de padrões")
    pct = st.slider('Qual a porcentagem dos dados? ', 0.0, 1.0, 0.6, 0.1)

    if st.button('Iniciar'):
        c.start(pct)
        print('GC: ', gc.collect())


if __name__ == '__main__':
    main()
