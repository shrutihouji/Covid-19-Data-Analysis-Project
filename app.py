from flask import Flask, render_template, send_file, make_response
from corona import table, plot1,top10,pie1,scatter1,total,datewise,agewise

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import folium
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)
@app.route('/')

def show_tables():
    tableDisplay = table()
    figureDisplay1 = plot1()
    top10fig = top10()
    figureDisplay2=pie1()
    figureDisplay3=scatter1()
    totals=total()
    dateWise = datewise()
    ageWise=agewise()
    return render_template('index.html',  returnList = tableDisplay, figure1=figureDisplay1,top10list=top10fig,  figure2=figureDisplay2, figure3=figureDisplay3,total_data=totals,dateWiseData=dateWise,ageWiseDetails=ageWise)
   


if __name__ == "__main__":
    app.jinja_v.cache = {}
    app.run(debug=True)