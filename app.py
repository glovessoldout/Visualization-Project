# to run this app use this command in 
# git-bash, anaconda prompt, or terminal : python -m flask run
from flask import Flask, render_template, Response, send_file, jsonify
from flask_socketio import SocketIO
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import io
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
 
app = Flask(__name__)

@app.route('/')
def home():
    print("vanilla")
    return render_template("index.html")

@app.route('/home')
def homie():
    print("home screen")
    return("included urls:<br/>"
        "<br/>"
        "/home: guide to the api<br/>"
        "/dashboard: dashboard<br/>"
        "/api/fighters: the test api from Drew<br/>"
        "/api/arxiv/: the meat<br/>"
        "/arxiv_topics: full list<br/>"
        "/arxiv_topic_count: list and number of papers per topic <br/>"
        "/api/arxiv/<category>/<start_date>/<end_date>, min start_date = 2007-05-23, max end_date = 2020-09-14<br/>"
        "/api/arxiv/<category>/<start_date>/<end_date>/wordcloud.png<br/>"
        )

@app.route('/arxiv_topics')
def topics():
    file1 = pd.read_fwf("./data/Topic_List.txt")
    #topics = file1.readlines() 
    return file1.to_json()

@app.route("/arxiv_topic_count")
def topic_count():
    df2 = pd.read_csv('./data/topics_count_list.csv')
    return df2.to_json()

@app.route("/dashboard")
def dashboard():
    #df = pd.read_csv('./data/arxiv_condensed_data_again.csv')
    df = pd.read_csv('./data/test.csv')
    print("DF with stats")
    print(df.to_json())
    return render_template("dashboard.html", json_data=df.to_json())

@app.route("/api/fighters")
def api_fighters():
    df = pd.read_csv("./data/test.csv")
    return df.to_json()

@app.route("/api/arxiv/")
def api_arxiv():
    df_arxiv = pd.read_csv("./data/arxiv_condensed_data_again.csv")
    print("this is huge")
    return df_arxiv.to_json()


@app.route('/api/arxiv/<category>/<start_date>/<end_date>')
def api_arxiv_filters_json(category,start_date,end_date):
    apc = api_arxiv_filters(category,start_date,end_date)
    return apc.to_json()

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

def generate_wordcloud(word_list):
    wordcloud = WordCloud(width=960, height=960,max_font_size=1000, min_font_size=0, max_words=40, background_color="gray").generate(word_list)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.margins(x=0, y=0)
    return(plt.savefig("testing"))
    #plt.show()

def api_arxiv_filters(category,start_date,end_date):
    arxiv_pc = pd.read_csv("./data/arxiv_condensed_data_again.csv")
    apc2 = arxiv_pc.loc[arxiv_pc['update_date'] >= start_date,:]
    apc2 = apc2.loc[apc2['update_date'] <= end_date,:]
    apc = apc2[apc2["categories"].str.contains(category)].sort_values("update_date")
    return apc

@app.route('/api/arxiv/<category>/<start_date>/<end_date>/wordcloud.png')
def arxiv_wordcloud(category,start_date,end_date):
    apc = api_arxiv_filters(category,start_date,end_date)
    array = []
    text2 = ""
    space = " "
    for paper in apc["title"]:
        ph = paper.split()
        for word in ph:
            text2 = text2 + word + space
    # wc = generate_wordcloud(text2)
    # output = io.BytesIO()
    # FigureCanvas(wc).print_png(output)
    # return Response(output.getvalue(), mimetype='image/png')
    generate_wordcloud(text2)
    testing = 'testing.png'
    return send_file(testing, mimetype='image/png')
#I'm high
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig

if __name__ == "__main__":
    socketio.run(app, debug=True)