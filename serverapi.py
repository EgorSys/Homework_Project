import requests
from flask import Flask, render_template, send_file
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


links = {"Download" : "/download",
         "Plot" : "/plot"}

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html", links=links, image=None)

@app.route('/download', methods=['GET'])
def download_data():
    return send_file("data/covid19-russia-cases.csv", as_attachment=True)

@app.route('/plot', methods=['GET'])
def make_pairplot():
    df = pd.read_csv("data/covid19-russia-cases.csv")
    
    for el in df['Region_ID'].unique():
        df1 = df[df['Region_ID'] == el]
        plt.scatter(df1['Date'], df1['Confirmed']-df1['Recovered'])
    plt.title('Covid Cases by City')
    plt.xlabel('Days')
    plt.ylabel('Covid-19 cases')
    plt.savefig("static/tmp/cities_compare.png")
    return render_template('index.html', links=links, image=('tmp/cities_compare.png', 'lineplot'))


if __name__ == "__main__":
    app.run(host='localhost', port=8888)