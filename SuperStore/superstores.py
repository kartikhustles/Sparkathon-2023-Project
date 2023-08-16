import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import io
import base64

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded.csv')
            file.save(filename)
            return redirect(url_for('result', filename='uploaded.csv'))
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/result/<filename>')
def result(filename):
    csv_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(csv_path)

    # Data analysis and visualization
    null_count = df['Postal Code'].isnull().sum()
    df["Postal Code"].fillna(0, inplace=True)
    df['Postal Code'] = df['Postal Code'].astype(int)
    
    # ... (perform the rest of your data analysis and visualization)
    
    # Save plots as images
    types_of_customers = df['Segment'].unique()
    
    number_of_customers = df['Segment'].value_counts().reset_index()
    number_of_customers = number_of_customers.rename(columns={'index': 'Customer Type', 'Segment': 'Total Customers'})
    
    pie_chart1_path = plot_pie_chart(number_of_customers, 'Customer Type', 'Total Customers', 'Distribution of Customers')
    
    sales_per_category=df.groupby('Segment')['Sales'].sum().reset_index()
    sales_per_category=sales_per_category.rename(columns={'Segment': 'Customer Type', 'Sales': 'Total Sales'})

    pie_chart2_path = plot_pie_chart(sales_per_category, 'Customer Type', 'Total Sales', 'Sales Per Customer Category')
    bar_chart1_path = plot_bar_chart(sales_per_category, 'Customer Type', 'Total Sales', 'Sales per Customer Category', 'Customer Type', 'Total Sales')
    
    customer_order_freq=df.groupby(['Customer ID', 'Customer Name', 'Segment'])['Order ID'].count().reset_index() 
    customer_order_freq.rename(columns={'Order ID': 'Total Orders'}, inplace=True)
    repeat_customers = customer_order_freq[customer_order_freq[ 'Total Orders']>= 1]
    sorted_repeat_customers=repeat_customers.sort_values (by='Total Orders', ascending=False)

    customer_sales = df.groupby(['Customer ID', 'Customer Name', 'Segment'])['Sales'].sum().reset_index()
    top_spenders = customer_sales.sort_values(by='Sales', ascending=False)

    type_of_shipping=df['Ship Mode'].unique()
    '''pie_chart2_path = os.path.join(app.config['UPLOAD_FOLDER'], 'static', 'pie_chart2.png')
    plt.pie(sales_per_category['Total Sales'], labels=sales_per_category['Customer Type'], autopct='%1.1f%%')
    plt.title('Sales Per Customer Category')
    plt.savefig(pie_chart2_path)
    plt.close()
    
    bar_chart1_path = os.path.join(app.config['UPLOAD_FOLDER'], 'static', 'bar_chart1.png')
    plt.bar(sales_per_category['Customer Type'], sales_per_category['Total Sales'])
    plt.title('Sales Per Customer Category')
    plt.savefig(bar_chart1_path)
    plt.close()'''
    
    
    
    
    # ... (repeat the process for other plots)
    
    # Render the results using the result.html template
    return render_template( 'result.html', 
                           types_of_customers=types_of_customers, 
                           number_of_customers=number_of_customers, 
                           pie_chart1=pie_chart1_path, 
                           sales_per_category=sales_per_category, 
                           pie_chart2=pie_chart2_path, 
                           bar_chart1=bar_chart1_path,
                           sorted_repeat_customers=sorted_repeat_customers,
                           top_spenders=top_spenders,
                           type_of_shipping=type_of_shipping)
                        #    shipping_mode=shipping_mode,
                        #    state_sales=top_state_sales,
                        #    city_sales=top_city_sales,
                        #    products_category=products_category,
                        #    subcategory_count=subcategory_count,
                        #    category_sales=category_sales,
                        #    pdt_subcategory=top_pdt_subcategory,
                        #    yearly_sales=yearly_sales,
                        #    monthly_sales=monthly_sales)

def plot_pie_chart(data, labels_col, values_col, title):
    plt.figure()
    plt.pie(data[values_col], labels=data[labels_col], autopct='%1.1f%%')
    plt.title(title)
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url

def plot_bar_chart(data, x_col, y_col, title, x_label, y_label):
    plt.figure()
    plt.bar(data[x_col], data[y_col])
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=45)
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url

if __name__ == '__main__':
    app.run(debug=True)