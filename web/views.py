from django.shortcuts import render
import pandas as pd
from web import connection
import json
import plotly.offline as opy
import plotly.express as px
import numpy as np

# Create your views here.
def home(request):

    conn = connection.conn()

    best_emp = pd.read_sql("select * from order_emp_best", conn)
    best_emp['total_sale'] = round(best_emp['total_sale']/1000,2)

    # best_emp_fig = px.bar(best_emp, x="fullname", y="total_sale")
    # best_emp_fig_div = opy.plot(best_emp_fig, auto_open=False, output_type='div')

    best_emp_json_records = best_emp.reset_index().to_json(orient ='records')
    best_emp = json.loads(best_emp_json_records)

    

    df_scatter_sales = pd.read_sql("select * from scatter_sales", conn).sort_values(by=['total_sale'], ascending=False)
    df_scatter_sales['total_sale'] = round(df_scatter_sales['total_sale']/1000,2)
    config = {'displaylogo': False}
    scatter_sales_fig = px.scatter_geo(df_scatter_sales, lat='lat', lon='lon',
                        color="country", # which column to use to set the color of markers
                        size=round(df_scatter_sales['total_sale']**2,1),
                        projection="natural earth",
                        custom_data=['total_sale', 'id_and_name', 'country'],
                        hover_data={'lon':False, 
                        'lat':False, 'total_sale':True},
                        template="plotly_dark",
                        )

    scatter_sales_fig.update_layout(
                            margin=dict(l=0, r=0, t=26, b=0),
                            autosize=False,
                            width=590,
                            height=290,
                            font_family='Avenir Next',
                            title={
                                'text': "<b>Sales by Country</b>",
                                'y':1,
                                'x':0.5},
                            legend_font_size=10,
                            showlegend=False)
    scatter_sales_fig.update_traces(
        hovertemplate="<br>".join([
            "Country: %{customdata[2]}",
            "Customer ID, Name: %{customdata[1]}",
            "Total of Sales: $%{customdata[0]}k",
        ])
    )
    scatter_sales_div = opy.plot(scatter_sales_fig, auto_open=False, output_type='div')

    
    best_cust_json_records = df_scatter_sales.reset_index().to_json(orient ='records')
    best_cust = json.loads(best_cust_json_records)

    df_customers = pd.read_sql("select * from \"customers\"", conn)
    df_customers['age'] = round((np.datetime64('today') - df_customers['date_of_birth']) / np.timedelta64(1, 'Y'), 1)

    cust_age_pie = df_customers.groupby(pd.cut(df_customers["age"], np.arange(0, 125, 20))).size().reset_index(name='size')
    cust_age_pie['age'] = cust_age_pie['age'].astype('str')
    cust_age_pie['age'] = cust_age_pie['age'].replace({'(0, 20]': '0 - 20', '(20, 40]': '20 - 40', '(40, 60]': '40 - 60', '(60, 80]': '60 - 80', '(80, 100]': '80 - 100', '(100, 120]': '> 100'})
    pie_cust_fig = px.pie(cust_age_pie, values='size', names='age', 
                        template="plotly_dark")
    pie_cust_fig.update_layout(
                            margin=dict(l=0, r=0, t=26, b=0),
                            autosize=False,
                            width=365,
                            height=210,
                            font_family='Avenir Next',
                            title={
                                'text': "<b>Customer's Age Distribution</b>",
                                'y':1,
                                'x':0.5})
    pie_cust_fig_div = opy.plot(
                    pie_cust_fig, 
                    # include_plotlyjs=False,
                    auto_open=False, 
                    output_type='div',
                    config=config,
                    )
    pie_cust_fig_small = pie_cust_fig
    pie_cust_fig_small.update_layout(
                            margin=dict(l=0, r=0, t=26, b=0),
                            autosize=False,
                            width=300,
                            height=180,
                            font_family='Avenir Next',
                            title={
                                'text': "<b>Customer's Age Distribution</b>",
                                'y':1,
                                'x':0.5})
    pie_cust_fig_small_div = opy.plot(
                    pie_cust_fig_small, 
                    # include_plotlyjs=False,
                    auto_open=False, 
                    output_type='div',
                    config=config,
                    )
    # fig_div = plotly.offline.plot(
    #                 pie_cust_fig,
    #                 image_width='60%',
    #                 image_height='60%',
    #                 include_plotlyjs=False,
    #                 output_type='div',
    #                 auto_open=False,)

    df_products = pd.read_sql("select * from \"products\"", conn)
    prod_stock_fig = px.bar(df_products.sort_values(by=['stock'], ascending=False), x='stock', y='productname', orientation='h', template="plotly_dark")
    prod_stock_fig.update_layout(
                            margin=dict(l=0, r=0, t=10, b=0),
                            autosize=False,
                            # yaxis_visible=False,
                            yaxis_title=None,
                            xaxis_title=None,
                            # xaxis_visible=False,
                            width=590,
                            height=290,
                            font_family='Avenir Next',
                            title={
                                'text': "<b>Stock Status</b>",
                                'y':1,
                                'x':0.55},
                            yaxis = dict(
                            tickfont = dict(size=10)))
    prod_stock_fig_div = opy.plot(prod_stock_fig, auto_open=False, output_type='div')

    prod_type = df_products.groupby(['type']).size().reset_index(name='size')
    total_n_prods = prod_type['size'].sum()
    prod_type['pct'] = prod_type['size']/total_n_prods*100
    prod_type['pct_str'] = prod_type['pct'].astype(str) + '%'
    prod_type_fig = px.bar(prod_type.sort_values(by=['type']), 
                            x='type', y='size', 
                            text = 'pct_str', orientation='v', 
                            template="plotly_dark")
    prod_type_fig.update_layout(
                            margin=dict(l=0, r=0, t=26, b=0),
                            autosize=False,
                            yaxis_visible=False,
                            xaxis_visible=False,
                            width=590,
                            height=290,
                            font_family='Avenir Next',
                            title={
                                'text': "<b>Products' Type</b>",
                                'y':1,
                                'x':0.5})
    prod_type_fig_div = opy.plot(prod_type_fig, auto_open=False, output_type='div')

    df_prod_order_cust_emp = pd.read_sql("select * from \"prod_order_cust_emp\"", conn)
    df_prod_order_cust_emp['orderdate'] = df_prod_order_cust_emp['orderdate'].astype(str)
    df_prod_order_cust_emp_json_records = df_prod_order_cust_emp.reset_index().to_json(orient ='records')
    prod_order_cust_emp = json.loads(df_prod_order_cust_emp_json_records)

    df_orders = pd.read_sql("select * from \"orders\"", conn)
    order_total = df_orders.copy()
    order_total['total_sale'] = round(order_total['quantity'] * order_total['unitprice']/1000000,3)


    order_total.index = pd.to_datetime(order_total['orderdate'],format='%m/%d/%y %I:%M%p')

    order_total_y_m = order_total.groupby(by=[order_total.index.year, order_total.index.month])[['total_sale']].apply(sum)
    order_total_y_m.index.names =(['year', 'month'])
    order_total_y_m_json_records = order_total_y_m.reset_index().to_json(orient ='records')
    order_total_y_m = json.loads(order_total_y_m_json_records)

    order_totals_year = order_total.groupby(by=[order_total.index.year])[['total_sale']].apply(sum)
    order_totals_year.index.names =(['year'])

    total_sales = order_totals_year[['total_sale']].apply(sum)[0]

    order_totals_year['change_pct'] = round((order_totals_year['total_sale'] - order_totals_year['total_sale'].shift(1))/order_totals_year['total_sale'].shift(1)*100,2)
    order_totals_year['change_pct'] = order_totals_year['change_pct'].astype(str) + '%'
    order_totals_year_fig = px.line(order_totals_year.reset_index(), x='year', y='total_sale', text='change_pct', orientation='v', template="plotly_dark",
                                    labels={
                                            "total_sale": "$ billion",
                                            },)
    order_totals_year_fig.update_layout(
                            margin=dict(l=0, r=0, t=26, b=0),
                            autosize=False,
                            yaxis_visible=False,
                            xaxis_title=None,
                            width=365,
                            height=210,
                            font_family='Avenir Next',
                            title={
                                'text': "<b>Revenue Yearly Change</b>",
                                'y':1,
                                'x':0.5})
    order_totals_year_fig_div = opy.plot(
                                        order_totals_year_fig, 
                                        config=config,
                                        # include_plotlyjs=False,
                                        auto_open=False, 
                                        output_type='div',
                                        )
    order_totals_year_fig_small = order_totals_year_fig    
    order_totals_year_fig_small.update_layout(
                            margin=dict(l=0, r=0, t=26, b=0),
                            autosize=False,
                            yaxis_visible=False,
                            xaxis_title=None,
                            width=300,
                            height=180,
                            font_family='Avenir Next',
                            title={
                                'text': "<b>Revenue Yearly Change</b>",
                                'y':1,
                                'x':0.5})
    
    order_totals_year_fig_small_div = opy.plot(
                                        order_totals_year_fig_small, 
                                        config=config,
                                        # include_plotlyjs=False,
                                        auto_open=False, 
                                        output_type='div',
                                        )

    order_totals_year_json_records = order_totals_year.reset_index().to_json(orient ='records')
    order_totals_year = json.loads(order_totals_year_json_records)

    prod_type['pct'] = prod_type['size']/total_n_prods*100
    prod_type['pct_str'] = prod_type['pct'].astype(str) + '%'
    prod_type_fig = px.bar(prod_type.sort_values(by=['type']), x='type', y='size', text = 'pct_str', orientation='v', template="plotly_dark")

    
    

    
    # # total_sales1 = order_totals_year[['total_sale']].apply(sum)
    # total_sales_json_records = total_sales.reset_index().to_json(orient ='records')
    # total_sales = json.loads(total_sales_json_records)
    

    return render(request, 'home.html',
    {
            "best_emp": best_emp,
            "scatter_sales_div" : scatter_sales_div,
            "best_cust": best_cust,
            "pie_cust_fig_div": pie_cust_fig_div,
            "prod_stock_fig_div": prod_stock_fig_div,
            "prod_type_fig_div": prod_type_fig_div,
            "prod_order_cust_emp": prod_order_cust_emp,
            "order_total_y_m": order_total_y_m,
            "order_totals_year": order_totals_year,
            "total_sales": total_sales,
            "order_totals_year_fig_div": order_totals_year_fig_div,
            "order_totals_year_fig_small_div": order_totals_year_fig_small_div,
            "pie_cust_fig_small_div": pie_cust_fig_small_div
        },
    )

def required(request):

    conn = connection.conn()

    best_emp = pd.read_sql("select * from order_emp_best", conn)
    best_emp['total_sale'] = round(best_emp['total_sale']/1000,2)

    best_emp_fig = px.bar(best_emp, x="fullname", y="total_sale", template="plotly_dark", title="Sales by Employee")
    best_emp_fig_div = opy.plot(best_emp_fig, auto_open=False, output_type='div')
    df_customers = pd.read_sql("select * from \"customers\"", conn)
    df_orders = pd.read_sql("select * from \"orders\"", conn)
    df_products = pd.read_sql("select * from \"products\"", conn)
    df_prod_order = pd.merge(df_orders, df_products[['product_id', 'productname', 'type']], on='product_id')
    df_prod_order_cust = pd.merge(df_prod_order, df_customers[['customer_id', 'first_name', 'last_name', 'country']], on='customer_id')

    df_prod_order_cust['sale'] = df_prod_order_cust['unitprice'] * df_prod_order_cust['quantity']

    df_prod_order_cust['id_and_name'] = df_prod_order_cust['customer_id'].astype(str) + " - " + df_prod_order_cust['first_name'] + " " + df_prod_order_cust['last_name']

    prod_order = df_prod_order_cust.groupby(by=['product_id', 'productname'])[['type', 'sale']].apply(sum)[['sale']].reset_index().sort_values(by=['sale'], ascending=False)

    prod_order_fig = px.bar(prod_order, x='sale', y='productname', template="plotly_dark", title="Top Selling Products")

    prod_order_fig_div = opy.plot(prod_order_fig, auto_open=False, output_type='div')



    return render(request, 'required.html',
{
        "best_emp_fig_div": best_emp_fig_div,
        "prod_order_fig_div": prod_order_fig_div
    },
)


def test(request):

    conn = connection.conn()

    best_emp = pd.read_sql("select * from order_emp_best", conn)
    best_emp['total_sale'] = round(best_emp['total_sale']/1000,2)

    # best_emp_fig = px.bar(best_emp, x="fullname", y="total_sale")
    # best_emp_fig_div = opy.plot(best_emp_fig, auto_open=False, output_type='div')

    best_emp_json_records = best_emp.reset_index().to_json(orient ='records')
    best_emp = json.loads(best_emp_json_records)

    df_scatter_sales = pd.read_sql("select * from scatter_sales", conn)
    

    df_scatter_sales = pd.read_sql("select * from scatter_sales", conn).sort_values(by=['total_sale'], ascending=False)

    
    df_scatter_sales['total_sale'] = round(df_scatter_sales['total_sale']/1000,2)


    config = {'displaylogo': False}
    scatter_sales_fig = px.scatter_geo(df_scatter_sales, lat='lat', lon='lon',
                        color="country", # which column to use to set the color of markers
                        size=round(df_scatter_sales['total_sale']**2,1),
                        projection="natural earth",
                        custom_data=['total_sale', 'id_and_name', 'country'],
                        hover_data={'lon':False, 
                        'lat':False, 'total_sale':True},
                        template="plotly_dark",
                        )

    scatter_sales_fig.update_layout(
                            margin=dict(l=0, r=0, t=26, b=0),
                            autosize=False,
                            width=590,
                            height=290,
                            font_family='Avenir Next',
                            title={
                                'text': "<b>Sales by Country</b>",
                                'y':1,
                                'x':0.5},
                            legend_font_size=10,
                            showlegend=False)
    scatter_sales_fig.update_traces(
        hovertemplate="<br>".join([
            "Country: %{customdata[2]}",
            "Customer ID, Name: %{customdata[1]}",
            "Total of Sales: $%{customdata[0]}k",
        ])
    )
    scatter_sales_div = opy.plot(scatter_sales_fig, auto_open=False, output_type='div')

    
    best_cust_json_records = df_scatter_sales.reset_index().to_json(orient ='records')
    best_cust = json.loads(best_cust_json_records)

    df_customers = pd.read_sql("select * from \"customers\"", conn)
    df_customers['age'] = round((np.datetime64('today') - df_customers['date_of_birth']) / np.timedelta64(1, 'Y'), 1)

    cust_age_pie = df_customers.groupby(pd.cut(df_customers["age"], np.arange(0, 125, 20))).size().reset_index(name='size')
    cust_age_pie['age'] = cust_age_pie['age'].astype('str')
    cust_age_pie['age'] = cust_age_pie['age'].replace({'(0, 20]': '0 - 20', '(20, 40]': '20 - 40', '(40, 60]': '40 - 60', '(60, 80]': '60 - 80', '(80, 100]': '80 - 100', '(100, 120]': '> 100'})
    pie_cust_fig = px.pie(cust_age_pie, values='size', names='age', 
                        template="plotly_dark")
    pie_cust_fig.update_layout(
                            margin=dict(l=0, r=0, t=26, b=0),
                            autosize=False,
                            width=365,
                            height=210,
                            font_family='Avenir Next',
                            title={
                                'text': "<b>Customer's Age Distribution</b>",
                                'y':1,
                                'x':0.5})
    pie_cust_fig_div = opy.plot(
                    pie_cust_fig, 
                    # include_plotlyjs=False,
                    auto_open=False, 
                    output_type='div',
                    config=config,
                    )
    pie_cust_fig_small = pie_cust_fig
    pie_cust_fig_small.update_layout(
                            margin=dict(l=0, r=0, t=26, b=0),
                            autosize=False,
                            width=300,
                            height=180,
                            font_family='Avenir Next',
                            title={
                                'text': "<b>Customer's Age Distribution</b>",
                                'y':1,
                                'x':0.5})
    pie_cust_fig_small_div = opy.plot(
                    pie_cust_fig_small, 
                    # include_plotlyjs=False,
                    auto_open=False, 
                    output_type='div',
                    config=config,
                    )
    # fig_div = plotly.offline.plot(
    #                 pie_cust_fig,
    #                 image_width='60%',
    #                 image_height='60%',
    #                 include_plotlyjs=False,
    #                 output_type='div',
    #                 auto_open=False,)

    df_products = pd.read_sql("select * from \"products\"", conn)
    prod_stock_fig = px.bar(df_products.sort_values(by=['stock'], ascending=False), x='stock', y='productname', orientation='h', template="plotly_dark")
    prod_stock_fig.update_layout(
                            margin=dict(l=0, r=0, t=10, b=0),
                            autosize=False,
                            # yaxis_visible=False,
                            yaxis_title=None,
                            xaxis_title=None,
                            # xaxis_visible=False,
                            width=590,
                            height=290,
                            font_family='Avenir Next',
                            title={
                                'text': "<b>Stock Status</b>",
                                'y':1,
                                'x':0.55},
                            yaxis = dict(
                            tickfont = dict(size=10)))
    prod_stock_fig_div = opy.plot(prod_stock_fig, auto_open=False, output_type='div')

    prod_type = df_products.groupby(['type']).size().reset_index(name='size')
    total_n_prods = prod_type['size'].sum()
    prod_type['pct'] = prod_type['size']/total_n_prods*100
    prod_type['pct_str'] = prod_type['pct'].astype(str) + '%'
    prod_type_fig = px.bar(prod_type.sort_values(by=['type']), 
                            x='type', y='size', 
                            text = 'pct_str', orientation='v', 
                            template="plotly_dark")
    prod_type_fig.update_layout(
                            margin=dict(l=0, r=0, t=26, b=0),
                            autosize=False,
                            yaxis_visible=False,
                            xaxis_visible=False,
                            width=590,
                            height=290,
                            font_family='Avenir Next',
                            title={
                                'text': "<b>Products' Type</b>",
                                'y':1,
                                'x':0.5})
    prod_type_fig_div = opy.plot(prod_type_fig, auto_open=False, output_type='div')

    df_prod_order_cust_emp = pd.read_sql("select * from \"prod_order_cust_emp\"", conn)
    df_prod_order_cust_emp['orderdate'] = df_prod_order_cust_emp['orderdate'].astype(str)
    df_prod_order_cust_emp_json_records = df_prod_order_cust_emp.reset_index().to_json(orient ='records')
    prod_order_cust_emp = json.loads(df_prod_order_cust_emp_json_records)

    df_orders = pd.read_sql("select * from \"orders\"", conn)
    order_total = df_orders.copy()
    order_total['total_sale'] = round(order_total['quantity'] * order_total['unitprice']/1000000,3)


    order_total.index = pd.to_datetime(order_total['orderdate'],format='%m/%d/%y %I:%M%p')

    order_total_y_m = order_total.groupby(by=[order_total.index.year, order_total.index.month])[['total_sale']].apply(sum)
    order_total_y_m.index.names =(['year', 'month'])
    order_total_y_m_json_records = order_total_y_m.reset_index().to_json(orient ='records')
    order_total_y_m = json.loads(order_total_y_m_json_records)

    order_totals_year = order_total.groupby(by=[order_total.index.year])[['total_sale']].apply(sum)
    order_totals_year.index.names =(['year'])

    total_sales = order_totals_year[['total_sale']].apply(sum)[0]

    order_totals_year['change_pct'] = round((order_totals_year['total_sale'] - order_totals_year['total_sale'].shift(1))/order_totals_year['total_sale'].shift(1)*100,2)
    order_totals_year['change_pct'] = order_totals_year['change_pct'].astype(str) + '%'
    order_totals_year_fig = px.line(order_totals_year.reset_index(), x='year', y='total_sale', text='change_pct', orientation='v', template="plotly_dark",
                                    labels={
                                            "total_sale": "$ billion",
                                            },)
    order_totals_year_fig.update_layout(
                            margin=dict(l=0, r=0, t=26, b=0),
                            autosize=False,
                            yaxis_visible=False,
                            xaxis_title=None,
                            width=365,
                            height=210,
                            font_family='Avenir Next',
                            title={
                                'text': "<b>Revenue Yearly Change</b>",
                                'y':1,
                                'x':0.5})
    order_totals_year_fig_div = opy.plot(
                                        order_totals_year_fig, 
                                        config=config,
                                        # include_plotlyjs=False,
                                        auto_open=False, 
                                        output_type='div',
                                        )
    order_totals_year_fig_small = order_totals_year_fig    
    order_totals_year_fig_small.update_layout(
                            margin=dict(l=0, r=0, t=26, b=0),
                            autosize=False,
                            yaxis_visible=False,
                            xaxis_title=None,
                            width=300,
                            height=180,
                            font_family='Avenir Next',
                            title={
                                'text': "<b>Revenue Yearly Change</b>",
                                'y':1,
                                'x':0.5})
    
    order_totals_year_fig_small_div = opy.plot(
                                        order_totals_year_fig_small, 
                                        config=config,
                                        # include_plotlyjs=False,
                                        auto_open=False, 
                                        output_type='div',
                                        )

    order_totals_year_json_records = order_totals_year.reset_index().to_json(orient ='records')
    order_totals_year = json.loads(order_totals_year_json_records)

    prod_type['pct'] = prod_type['size']/total_n_prods*100
    prod_type['pct_str'] = prod_type['pct'].astype(str) + '%'
    prod_type_fig = px.bar(prod_type.sort_values(by=['type']), x='type', y='size', text = 'pct_str', orientation='v', template="plotly_dark")

    
    

    
    # # total_sales1 = order_totals_year[['total_sale']].apply(sum)
    # total_sales_json_records = total_sales.reset_index().to_json(orient ='records')
    # total_sales = json.loads(total_sales_json_records)
    

    return render(request, 'home.html',
    {
            "best_emp": best_emp,
            "scatter_sales_div" : scatter_sales_div,
            "best_cust": best_cust,
            "pie_cust_fig_div": pie_cust_fig_div,
            "prod_stock_fig_div": prod_stock_fig_div,
            "prod_type_fig_div": prod_type_fig_div,
            "prod_order_cust_emp": prod_order_cust_emp,
            "order_total_y_m": order_total_y_m,
            "order_totals_year": order_totals_year,
            "total_sales": total_sales,
            "order_totals_year_fig_div": order_totals_year_fig_div,
            "order_totals_year_fig_small_div": order_totals_year_fig_small_div,
            "pie_cust_fig_small_div": pie_cust_fig_small_div
        },
    )