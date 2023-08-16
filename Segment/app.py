import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from flask import Flask, request, render_template_string
from io import BytesIO
import base64


app = Flask(__name__)

template = '''
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>KMeans Clustering</title>
    <link rel="icon" href="../../Images/favicon.png" />
    <style>
    #choose-file {
        font-weight: 400;
        font-size: 0.5vw;
        text-align: center;
        font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS",
          sans-serif;
        padding: 0.5rem 1.5rem;
      }

      #centre {
        display: flex;
        justify-content: center;
      }

      #ruler {
        margin-top: 5vh;
        color: grey;
      }

      #header3 {
        font-size: 3vw;
        text-align: center;
        font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS",
          sans-serif;
        padding-top: 10px;
      }

      #header2 {
        font-size: 2vw;
        text-align: center;
        font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS",
          sans-serif;
        padding-top: 10px;
      }

      #form {
        display: flex;
        justify-content: center;
      }

      #result {
        display: flex;
        justify-content: center;
      }

      #form p {
        font-size: 1.5vw;
        font-weight: 600;
        display: flex;
        flex-wrap: wrap;
        font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS",
          sans-serif;
      }

      #Submit-Button {
        margin-left: 35%;
        font-weight: 600;
        font-size: 1.1vw;
        text-align: center;
        font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS",
          sans-serif;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        background: #fbc43c;
      }

      #form input,
      textarea {
        max-width: 90%;
        margin: 15px;
        padding: 4px 10px;
        border: 0px solid transparent;
        color: #000000;
        background: transparent;
        width: 90%;
        line-height: 1.6;
        font-size: 1.05rem;
      }

      #prediction-result {
        font-size: 1.5vw;
        font-weight: 600;
        font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS",
          sans-serif;
        display: flex;
        justify-content: center;
        margin-top: 2vw;
      }
    </style>
  </head>
  <body>
    <h3 id="header3">KMeans Clustering</h3>
    <div id="form">
      <form method="POST" enctype="multipart/form-data">
        <input id="choose-file" type="file" name="file" accept=".csv" />
        <button
          id="Submit-Button"
          type="submit"
          class="btn btn-primary"
          name="submit"
          value="Upload CSV"
        >
          Submit
        </button>
        <!-- <input id="Submit-Button" type="submit" value="Upload CSV" /> -->
      </form>
    </div>

    <hr id="ruler" />
    <div id="result">
      <div>
        {% if dataset_preview %}
        <h2 id="header2">Dataset Preview</h2>
        <div id="centre">
          {{ dataset_preview|safe }} {% endif %} {% if result_image %}
        </div>
        <h2 id="header2">Clustered Data</h2>
        <div id="centre">
          <img
            src="data:image/png;base64,{{ result_image }}"
            alt="Clustered Data"
          />
          {% endif %}
        </div>
      </div>
    </div>
  </body>
</html>





'''

def plot_clusters(X, Y, kmeans):
    plt.figure(figsize=(8, 8))
    plt.scatter(X[Y == 0, 0], X[Y == 0, 1], s=50, c='green', label='Cluster 1')
    plt.scatter(X[Y==1,0], X[Y==1,1], s=50, c='red', label='Cluster 2')
    plt.scatter(X[Y==2,0], X[Y==2,1], s=50, c='yellow', label='Cluster 3')
    plt.scatter(X[Y==3,0], X[Y==3,1], s=50, c='violet', label='Cluster 4')
    plt.scatter(X[Y==4,0], X[Y==4,1], s=50, c='blue', label='Cluster 5')
    plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=100, c='black', label='Centroids')
    plt.title('Customer Groups')
    plt.xlabel('Annual Income')
    plt.ylabel('Spending Score')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode()
    buffer.close()

    return plot_data

@app.route('/', methods=['GET', 'POST'])
def index():
    dataset_preview = None
    result_image = None

    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            customer_data = pd.read_csv(file)
            X = customer_data.iloc[:, [3, 4]].values
            wcss = []

            for i in range(1, 11):
                kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
                kmeans.fit(X)
                wcss.append(kmeans.inertia_)

            kmeans = KMeans(n_clusters=5, init='k-means++', random_state=0)
            Y = kmeans.fit_predict(X)

            result_image = plot_clusters(X, Y, kmeans)

            dataset_preview = customer_data.head().to_html(index=False)

    return render_template_string(template, dataset_preview=dataset_preview, result_image=result_image)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)