from flask import Flask, render_template, request
import pandas as pd
import json

app = Flask(__name__)

@app.route('/')
def home():
    # 1. डेटा पढ़ना
    df = pd.read_csv('sales report.csv', encoding='latin1')
    
    # 2. सर्च बॉक्स से रिक्वेस्ट पकड़ना
    search_query = request.args.get('category', '')
    
    if search_query:
        df = df[df['Category'].str.contains(search_query, case=False, na=False)]
    
    # 3. टोटल Sales और Profit
    total_sales = round(df['Sales'].sum(), 2)
    total_profit = round(df['Profit'].sum(), 2)
    
    # 4. Bar Chart का डेटा (Sub-Category)
    bar_data = df.groupby('Sub-Category')['Sales'].sum().reset_index()
    labels = json.dumps(bar_data['Sub-Category'].tolist())
    values = json.dumps(bar_data['Sales'].tolist())
    
    # 5. Pie Chart का डेटा (Region) - यह हिस्सा शायद पहले छूट गया था
    pie_data = df.groupby('Region')['Sales'].sum().reset_index()
    pie_labels = json.dumps(pie_data['Region'].tolist())
    pie_values = json.dumps(pie_data['Sales'].tolist())
    
    # 6. टेबल बनाना
    table_html = df.head(20).to_html(classes='table table-bordered table-striped', index=False)
    
    # 7. HTML फ़ाइल को कॉल करना और सभी वेरिएबल्स (Pie Chart सहित) भेजना
    return render_template('index.html', 
                           search_query=search_query, 
                           total_sales=total_sales, 
                           total_profit=total_profit, 
                           table_html=table_html, 
                           labels=labels, 
                           values=values,
                           pie_labels=pie_labels, 
                           pie_values=pie_values)

if __name__ == '__main__':
    app.run(debug=True)