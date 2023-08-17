from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

def generate_plot(df, x_column, y_column, title, x_label, y_label, kind='bar'):
    plt.figure(figsize=(12, 8))
    if kind == 'pie':
        plt.pie(df[y_column], labels=df[x_column], autopct='%1.1f%%')
    elif kind == 'line':
        plt.plot(df[x_column], df[y_column], marker='o', linestyle='--')
        plt.xticks(rotation=65)
    else:
        plt.bar(df[x_column], df[y_column])
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return graph_url

@app.route('/', methods=['GET', 'POST'])
def index():
    plot_urls = []

    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            df = pd.read_csv(file)
            df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)

            # Table 1
            types_of_customers = df['Segment'].unique()
            print(types_of_customers)

            # Table 2
            number_of_customers = df['Segment'].value_counts().reset_index()
            number_of_customers = number_of_customers.rename(columns={'index': 'Customer Type', 'Segment': 'Total Customers'})
            print(number_of_customers)

            # Plot 1
            plt.pie(number_of_customers['Total Customers'], labels=number_of_customers['Customer Type'], autopct='%1.1f%%')
            plt.title('Distribution of Customers')
            img = BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_urls.append(base64.b64encode(img.getvalue()).decode())
            plt.close()

            # Table 3
            sales_per_category = df.groupby('Segment')['Sales'].sum().reset_index()
            sales_per_category = sales_per_category.rename(columns={'Segment': 'Customer Type', 'Sales': 'Total Sales'})
            print(sales_per_category)

            # Plot 2
            plt.pie(sales_per_category['Total Sales'], labels=sales_per_category['Customer Type'], autopct='%1.1f%%')
            plt.title('Sales Per Customer Category')
            img = BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_urls.append(base64.b64encode(img.getvalue()).decode())
            plt.close()

            # Bar 1
            plt.bar(sales_per_category['Customer Type'], sales_per_category['Total Sales'])
            plt.title('Sales per Customer Category')
            plt.xlabel('Customer Type')
            plt.ylabel('Total Sales')
            img = BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_urls.append(base64.b64encode(img.getvalue()).decode())
            plt.close()

            # Table 4
            customer_order_freq = df.groupby(['Customer ID', 'Customer Name', 'Segment'])['Order ID'].count().reset_index()
            customer_order_freq.rename(columns={'Order ID': 'Total Orders'}, inplace=True)
            repeat_customers = customer_order_freq[customer_order_freq['Total Orders'] >= 1]
            sorted_repeat_customers = repeat_customers.sort_values(by='Total Orders', ascending=False)
            print(sorted_repeat_customers.head().reset_index(drop=True))
            print()

            # Table 5
            customer_sales = df.groupby(['Customer ID', 'Customer Name', 'Segment'])['Sales'].sum().reset_index()
            top_spenders = customer_sales.sort_values(by='Sales', ascending=False)
            print(top_spenders.head().reset_index(drop=True))

            # Table 6
            type_of_shipping = df['Ship Mode'].unique()
            print(type_of_shipping)

            # Table 7
            shipping_mode = df['Ship Mode'].value_counts().reset_index()
            shipping_mode = shipping_mode.rename(columns={'index': 'Mode of Shipment', 'Ship Mode': 'Use Frequency'})
            print(shipping_mode)

            # Plot 3
            plt.pie(shipping_mode['Use Frequency'], labels=shipping_mode['Mode of Shipment'], autopct='%1.1f%%')
            plt.title('Popular Shipping Method')
            img = BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_urls.append(base64.b64encode(img.getvalue()).decode())
            plt.close()

            # Table 8
            state = df['State'].value_counts().reset_index()
            state = state.rename(columns={'index': 'State', 'State': 'Number of Customers'})
            state_sales = df.groupby(['State'])['Sales'].sum().reset_index()
            top_state_sales = state_sales.sort_values(by='Sales', ascending=False)
            print(top_state_sales.head().reset_index(drop=True))
            print()

            # Table 9
            city = df['City'].value_counts().reset_index()
            city = city.rename(columns={'index': 'City', 'City': 'Number of Customers'})
            city_sales = df.groupby(['City'])['Sales'].sum().reset_index()
            top_city_sales = city_sales.sort_values(by='Sales', ascending=False)
            print(top_city_sales.head().reset_index(drop=True))

            # Table 10
            products_category = df['Category'].unique()
            print(products_category)

            # Table 11
            subcategory_count = df.groupby('Category')['Sub-Category'].nunique().reset_index()
            subcategory_count = subcategory_count.sort_values(by='Sub-Category', ascending=False)
            print(subcategory_count.reset_index(drop=True))
            print()

            # Table 12
            category_sales = df.groupby(['Category'])['Sales'].sum().reset_index()
            category_sales = category_sales.sort_values(by='Sales', ascending=False)
            print(category_sales.reset_index(drop=True))

            # Plot 4
            plt.pie(category_sales['Sales'], labels=category_sales['Category'], autopct='%1.1f%%')
            plt.title('Top Product Category Based on Sales')
            img = BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_urls.append(base64.b64encode(img.getvalue()).decode())
            plt.close()

            # Table 13
            pdt_subcategory = df.groupby(['Sub-Category'])['Sales'].sum().reset_index()
            top_pdt_subcategory = pdt_subcategory.sort_values(by="Sales", ascending=False)
            print(top_pdt_subcategory)

            # Bar 2
            top_pdt_subcategory = top_pdt_subcategory.sort_values(by='Sales', ascending=True)
            plt.barh(top_pdt_subcategory['Sub-Category'], top_pdt_subcategory['Sales'])
            plt.title('Top Product Sub-Categories based on Sales')
            plt.xlabel('Product Sub-Categories')
            plt.ylabel('Total Sales')
            img = BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_urls.append(base64.b64encode(img.getvalue()).decode())
            plt.close()

            # Table 14
            year_sales = df[df['Order Date'].dt.year == 2018]
            monthly_sales = year_sales.resample('M', on='Order Date')['Sales'].sum()
            monthly_sales = monthly_sales.reset_index()
            monthly_sales = monthly_sales.rename(columns={'Order Date': 'Month', 'Sales': 'Total Monthly Sales'})
            print('This are the Monthly sales for 2018')
            print(monthly_sales)

            # Line 2
            plt.plot(monthly_sales['Month'], monthly_sales['Total Monthly Sales'], marker='o', linestyle='--')
            plt.title('Monthly Sales')
            plt.xlabel('Monthly')
            plt.ylabel('Total Sales')
            plt.xticks(rotation=65)
            img = BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_urls.append(base64.b64encode(img.getvalue()).decode())
           

    return render_template('index.html', plot_urls=plot_urls)

if __name__ == '__main__':
    app.run(debug=True)