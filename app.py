from flask import Flask, render_template, request
import numpy as np
import datetime, requests, pandas
from bokeh.plotting import figure, output_file, show

app_arb = Flask(__name__)
app_arb.vars = {}

@app_arb.route("/index_arb",methods=['GET','POST'])
def initialize():
    if request.method == 'GET':
        return render_template("stockquote_main.html")
    else:
        app_arb.vars['ticker_sym'] = request.form['ticker_symbol']

        base_request_str_prefix = "https://www.quandl.com/api/v3/datasets/WIKI/"
        base_request_str_postfix = "/data.json?"
#        dates = get_dates()
        plot_data = '4'       
        request_str = base_request_str_prefix +app_arb.vars['ticker_sym']+base_request_str_postfix
        request_str += 'column_index='+plot_data#+"&start_date="+dates[0]+"&end_date="+dates[1]
        request_str += '&api_key=jmPNze4tXEGFpkhb64Sq'

        data = requests.get(request_str)
        data_frame = pandas.DataFrame(data.json()['dataset_data']['data'],
                                      columns=data.json()['dataset_data']['column_names'])

        data_frame['Date'] = pandas.to_datetime(data_frame['Date'],format="%Y-%m-%d")
        close_price = np.array(data_frame['Close'])
        
        output_file("./templates/stockquote_output.html")
        
        p = figure(title=app_arb.vars['ticker_sym'], x_axis_label="datetime", y_axis_label="price")
        p.line(data_frame['Date'],close_price,legend="test",line_width=2)
        show(p)

        return render_template("stockquote_output.html")
#        return render_template("stockquote_request_str.html",request_str=request_str)


def get_dates():
    now = datetime.datetime.now()
    year = now.year
    year_m_one = year -1
    year = str(year)
    year_m_one = str(year_m_one)
    month = str(now.month)
    day = str(now.day)
    start_date=year_m_one+'-'+month+'-'+day
    end_date=year+'-'+month+'-'+day
    return str(start_date), str(end_date)
    
if __name__ == "__main__":
    app_arb.run(port=33507,debug=True)
