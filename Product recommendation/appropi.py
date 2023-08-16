import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from flask import Flask, request, render_template_string
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = Flask(__name__)

# HTML template
template = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Association Rule Mining</title>
    <link rel="icon" href="../Images/favicon.png" />
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
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

      #form label {
        font-size: 1.5vw;
        font-weight: 600;
        display: flex;
        flex-wrap: wrap;
        font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS",
          sans-serif;
      }

      #Submit-Button {
        margin-top: 2vh;
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
    <h3 id="header3">Association Rule Mining</h3>
    <h2 id="header2">Upload Dataset</h2>
    <br />
    <div id="form">
      <form method="POST" enctype="multipart/form-data">
        <label for="file"> Select CSV file:</label>
        <input type="file" name="file" accept=".csv" /><br />
        <label for="min_lift"> Minimum Lift:</label>
        <input
          style="border-bottom: 2px solid rgb(165, 165, 165)"
          type="text"
          name="min_lift"
        /><br />
        <label for="min_confidence"> Minimum Confidence:</label>
        <input
          style="border-bottom: 2px solid rgb(165, 165, 165)"
          type="text"
          name="min_confidence"
        /><br />
        <button
          id="Submit-Button"
          type="submit"
          class="btn btn-primary"
          name="Submit"
          value="Upload CSV"
        >
          Submit
        </button>
      </form>
    </div>

    <hr id="ruler" />
    <div id="result">
      <div>
        {% if preview_table %}
        <h2 id="header2">Dataset Preview</h2>
        <div id="centre">
          {{ preview_table|safe }} {% endif %} {% if result_table %}
        </div>
        <h2 id="header2">Association Rule Results</h2>
        <div id="centre">
          {{ result_table|safe }} {% endif %} {% if graph %}
        </div>
        <h2 id="header2">Association Rule Visualization</h2>
        <div id="centre">{{ graph|safe }} {% endif %}</div>
      </div>
    </div>
  </body>
</html>


"""


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        min_lift = float(request.form.get('min_lift'))
        min_confidence = float(request.form.get('min_confidence'))

        # Load CSV file
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        data = pd.read_csv(file)

        # Data preprocessing
        data['Description'] = data['Description'].str.strip()
        data.dropna(axis=0, subset=['InvoiceNo'], inplace=True)
        data['InvoiceNo'] = data['InvoiceNo'].astype('str')
        data = data[~data['InvoiceNo'].str.contains('C')]

        basket = (data[data['Country'] == "Germany"]
                  .groupby(['InvoiceNo', 'Description'])['Quantity']
                  .sum().unstack().reset_index().fillna(0).set_index('InvoiceNo'))

        def encode_units(x):
            return 1 if x >= 1 else 0

        basket_sets = basket.applymap(encode_units)
        basket_sets.drop('POSTAGE', inplace=True, axis=1)

        frequent_itemsets = apriori(
            basket_sets, min_support=0.07, use_colnames=True)
        rules = association_rules(
            frequent_itemsets, metric="lift", min_threshold=1)

        selected_rules = rules[(rules['lift'] >= min_lift) & (
            rules['confidence'] >= min_confidence)]

        # Visualization
        plt.figure(figsize=(10, 6))
        plt.scatter(selected_rules['confidence'],
                    selected_rules['lift'], alpha=0.5)
        plt.xlabel('Confidence')
        plt.ylabel('Lift')
        plt.title('Association Rule Visualization')

        img_stream = BytesIO()
        plt.savefig(img_stream, format='png')
        img_stream.seek(0)
        img_data = base64.b64encode(img_stream.read()).decode('utf-8')

        plt.close()

        # Prepare HTML content
        preview_table = data.head().to_html()
        result_table = selected_rules.to_html()
        graph = f'<img src="data:image/png;base64,{img_data}" alt="Association Rule Visualization">'

        return render_template_string(template, preview_table=preview_table, result_table=result_table, graph=graph)

    return render_template_string(template, preview_table="", result_table="", graph="")


if __name__ == '__main__':
    app.run(debug=True)
