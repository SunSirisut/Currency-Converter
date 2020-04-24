import platform
from tkinter import *
from tkinter import ttk
import requests
import xmltodict
import json
import io
import pandas as pd
from autocomplete import *
from urllib.request import urlopen, Request
from PIL import Image, ImageTk
import os
import numpy as np
import matplotlib.pyplot as plt
from mpldatacursor import datacursor
from datetime import datetime, timedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame
if platform.system() == 'Darwin':
    from tkmacosx import Button


color_bg_1 = '#F4D03F'
color_bg_2 = '#212F3C'
color_graph = '#F1C40F'

root = Tk()

root.title("Currency Exchanger")
root.geometry("1000x400")
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.configure(background = color_bg_1)

# ----------- VARIABLE ZONE --------------- #

exchange_rate_url = "https://currency-converter5.p.rapidapi.com/currency/convert"
headers = {
    'x-rapidapi-host': "currency-converter5.p.rapidapi.com",
    'x-rapidapi-key': "e1f657336amsh2e4f08e77a8c61ep106ccajsn517875c21896"
    }

list_currency = ['AED', 'ALL', 'AMD', 'ANG', 'ARS', 'AUD', 'AZN', 'BDT', 'BGN', 'BHD', 'BND', 'BRL', 'BYN', 'CAD'
                , 'CHF', 'CLP', 'CNY', 'CZK', 'DKK', 'DZD', 'EGP', 'EUR', 'GBP', 'GEL', 'GHS', 'HKD', 'HRK', 'HUF'
                , 'IDR', 'ILS', 'INR', 'IQD', 'IRR', 'ISK', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KRW', 'KWD', 'KZT'
                , 'LAK', 'LBP', 'LKR', 'LYD', 'MAD', 'MDL', 'MKD', 'MMK', 'MXN', 'MYR', 'NOK', 'NPR', 'NZD', 'OMR'
                , 'PHP', 'PKR', 'PLN', 'QAR', 'RON', 'RSD', 'RUB', 'SAR', 'SEK', 'SGD', 'THB', 'TJS', 'TMT', 'TND'
                , 'TRY', 'TWD', 'UAH', 'USD', 'UZS', 'VND', 'ZAR']


df_cache_data = pd.read_csv('cache_data.csv')

# ----------------------------------------- #

# ------------ FUNCTION ZONE ------------ #

def get_full_path(file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    full_path = os.path.join(dir_path, file_name)
    return full_path


def check_in_cache(d, f, t):
    global df_cache_data
    result = ''
    for i in range(len(df_cache_data)):
        if df_cache_data.loc[i]['date'] == d and df_cache_data.loc[i]['from'] == f and df_cache_data.loc[i]['to'] == t:
            result = df_cache_data.loc[i]['rate']
            return result
    return result


def get_currency_by_range(f, t, r):
    l_date = []
    l_cur = []
    
    for i in range(r, 0, -1):
        d = datetime.today() - timedelta(days = i)
        l_date.append(d.strftime('%Y-%m-%d'))
        
    querystring = {"format" : "json", "to" : t, "from" : f}
    
    for d in l_date:
        print(d)
        tmp = str(check_in_cache(d, f, t))
        if len(tmp) != 0:
            l_cur.append(tmp)
        else:
            url = "https://currency-converter5.p.rapidapi.com/currency/historical/" + d
            response = requests.request("GET", url, headers=headers, params=querystring)
            res = response.json()
            l_cur.append(res['rates'][t]['rate'])
            new_row = [d, f, t, res['rates'][t]['rate']]
            df_cache_data.loc[len(df_cache_data)] = new_row
        
    return l_date, l_cur


df_code_mapping = pd.read_csv(get_full_path('country_currency_mapping.csv'))

def update_flag_from(cur_from):
    global url_from, req_from, image_bytes_from, data_stream_from, pil_image_from, tk_image_from
    global df_code_mapping
    if cur_from != '':
        code_from = df_code_mapping[df_code_mapping['Code'] == cur_from].iloc[0, 1]
        url_from = 'https://www.countryflags.io/' + code_from +'/flat/64.png'
        req_from = Request(url_from, headers={'User-Agent': 'Mozilla/5.0'})
        image_bytes_from = urlopen(req_from).read()
        data_stream_from = io.BytesIO(image_bytes_from)
        pil_image_from = Image.open(data_stream_from)
        tk_image_from = ImageTk.PhotoImage(pil_image_from)

        label_flag_from.configure(image = tk_image_from)
    else:
        label_flag_from.configure(image = '')


def update_flag_to(cur_to):
    global url_to, req_to, image_bytes_to, data_stream_to, pil_image_to, tk_image_to
    global df_code_mapping

    if cur_to != '':
        code_to = df_code_mapping[df_code_mapping['Code'] == cur_to].iloc[0, 1]

        url_to = 'https://www.countryflags.io/' + code_to + '/flat/64.png'
        req_to = Request(url_to, headers={'User-Agent': 'Mozilla/5.0'})
        image_bytes_to = urlopen(req_to).read()
        data_stream_to = io.BytesIO(image_bytes_to)
        pil_image_to = Image.open(data_stream_to)
        tk_image_to = ImageTk.PhotoImage(pil_image_to)

        label_flag_to.configure(image = tk_image_to)
    else:
        label_flag_to.configure(image = '')


def show_graph(period):
    curr_from = dd_from.get_value()
    curr_to = dd_to.get_value()
    print(curr_from)
    print(curr_to)
    
    if curr_from != '' and curr_to != '':
        for widget in frame_graph_2.winfo_children():
            widget.destroy()

        l_date, l_cur = get_currency_by_range(curr_from, curr_to, period)
        y = [float(i) for i in l_cur]
        # tmp_date = [int(d.split('-')[-1]) for d in l_date]
        # x = range(min(tmp_date), max(tmp_date) + 1)
        tmp_date = [d.split('-')[-2] + '/' + d.split('-')[-1] for d in l_date]
        x = tmp_date
        x_tmp = range(0, len(x))
        print(x)
        print(y)

        fig = plt.Figure(dpi = 100)
        fig, ax = plt.subplots()
        fig.set_figheight(3.5)
        fig.set_figwidth(5)
        line = FigureCanvasTkAgg(fig, frame_graph_2)
        line.get_tk_widget().pack()
        ax.plot(x, y, color = color_graph, linewidth = 2.0, marker = 'o', markersize = 8)
        ax.set_xticks(x)
        ax.tick_params(axis = "x", labelsize = 8)
        ax.tick_params(axis = "y", labelsize = 8)
        ax.set_title('Exchange rate 1 ' + curr_from + ' to ' + curr_to)
        ax.set_ylim(bottom = min(y) - (0.001 * min(y)), top = max(y) + (0.001 * max(y)))


    def formatter(**kwargs):
        dist = abs(np.array(x_tmp) - kwargs['x'])
        # print(dist)
        i = dist.argmin()
        tmp = 'Date:' + str(l_date[i]) + '\n 1 ' + curr_from + ' = ' + str(str(y[i]) + ' ' + curr_to)
        return tmp

    datacursor(hover = True, formatter = formatter)


def on_convert_click():
    curr_from = dd_from.get_value()
    curr_to = dd_to.get_value()
    amount = entry_amount.get()
    querystring = {"format":"json","from":curr_from,"to":curr_to,"amount":amount}
    exchange_rate_data = requests.request("GET", exchange_rate_url, headers=headers, params=querystring).json()
    converted_amount = exchange_rate_data['rates'][curr_to]['rate_for_amount']
    label_result.configure(text=converted_amount)
        
    show_graph(3)

def on_swap_click():
    tmp_from = dd_from.get_value()
    tmp_to = dd_to.get_value()
    dd_from.delete(0, END)
    dd_from.insert(0, tmp_to)
    dd_to.delete(0, END)
    dd_to.insert(0, tmp_from)
    dd_from.unpost_listbox()
    dd_from.event_generate('<Button-1>')
    dd_to.unpost_listbox()
    dd_to.event_generate('<Button-1>')

# --------------------------------------- #

# ----- FRAME ----- #
frame_top = Frame(root, width = 500, height = 100, background = color_bg_1)
frame_top.grid(row = 0, column = 0, sticky = "NSEW")
frame_top.grid_propagate(0)

frame_mid = Frame(root, width = 500, height = 200)
frame_mid.grid(row = 1, column = 0, sticky = "NSEW")
frame_mid_1 = Frame(frame_mid, width = 200, height=150, background = color_bg_1)
frame_mid_1.grid(row = 0, column = 0, sticky = "NSEW")
frame_mid_2 = Frame(frame_mid, width = 100, height=150, background = color_bg_1)
frame_mid_2.grid(row = 0, column = 1, sticky = "NSEW")
frame_mid_3 = Frame(frame_mid, width = 200, height=150, background = color_bg_1)
frame_mid_3.grid(row = 0, column = 2, sticky = "NSEW")
frame_mid_4 = Frame(frame_mid, width = 200, height=50, background = color_bg_1)
frame_mid_4.grid(row = 2, column = 0, columnspan = 3, sticky = "NSEW")

frame_result = Frame(root, width = 500, height = 100, background = color_bg_2)
frame_result.grid(row = 2, column = 0, padx = 10, pady = 5, sticky = "NSEW")

frame_graph = Frame(root, width = 500, height = 400)
frame_graph.grid(row = 0, column = 1, rowspan = 3, padx = 5, pady = 5, sticky = "NSEW")
frame_graph_1 = Frame(frame_graph, width = 500, height = 50)
frame_graph_1.grid(row = 0, column = 0, sticky = "NSEW")
frame_graph_2 = Frame(frame_graph, width = 500, height = 350)
frame_graph_2.grid(row = 1, column = 0, sticky = "NSEW")


# FRAME TOP
label_1 = Label(frame_top, text = 'Enter amount', font = ('Helvetica', 18), bg = color_bg_1)
label_1.place(x = 250, y = 30, anchor="center")

entry_amount = Entry(frame_top, font = ('Helvetica', 20), justify = 'center')
entry_amount.place(x = 250, y = 70, width = 450, height = 40, anchor="center")


# FRAME MID
## MID 1
label_2 = Label(frame_mid_1, text = 'From', font = ('Helvetica', 18), bg = color_bg_1)
label_2.place(x = 100, y = 20, anchor = 'center')

code_from = StringVar()
dd_from = Combobox_Autocomplete(frame_mid_1, justify = 'center', font = ('Helvetica', 16), list_of_items = list_currency, textvariable = code_from)
dd_from.place(x = 100, y = 60, width = 150, height = 40, anchor = 'center')
dd_from.bind('<Return>', (lambda _: update_flag_from(dd_from.get_value())))
dd_from.bind('<Button-1>', (lambda _: update_flag_from(dd_from.get_value())))

label_flag_from = Label(frame_mid_1, image = '', bg = color_bg_1)
label_flag_from.place(x = 100, y = 120, anchor = 'center')

## MID 2

img_swap = ImageTk.PhotoImage(Image.open(get_full_path('swap.png')).resize((30, 30), Image.ANTIALIAS))
btn_swap = Button(frame_mid_2, image = img_swap,  width = 50, height = 40, command = on_swap_click, bg = color_bg_2)
btn_swap.place(x = 50, y = 60, anchor = 'center')

## MID 3
label_3 = Label(frame_mid_3, text = 'To', font = ('Helvetica', 18), bg = color_bg_1)
label_3.place(x = 100, y = 20, anchor = 'center')

code_to = StringVar()
dd_to = Combobox_Autocomplete(frame_mid_3, justify = 'center', font = ('Helvetica', 16), list_of_items = list_currency, textvariable = code_to)
dd_to.place(x = 100, y = 60, width = 150, height = 40, anchor = 'center')
dd_to.bind('<Return>', (lambda _: update_flag_to(dd_to.get_value())))
dd_to.bind('<Button-1>', (lambda _: update_flag_to(dd_to.get_value())))

label_flag_to = Label(frame_mid_3, image = '', bg = color_bg_1)
label_flag_to.place(x = 100, y = 120, anchor = 'center')


## MID 4
btn_convert = Button(frame_mid_4, text = 'Convert', font = ('Helvetica', 22), bg = color_bg_2, fg = 'White', command = on_convert_click)
btn_convert.place( x = 250, y = 15, anchor = 'center')


# RESULT
label_result = Label(frame_result, text = '', font = ('Helvetica', 36), bg = color_bg_2, fg = '#FFCC00')
label_result.place(x = 250, y = 50, anchor = 'center')


## GRAPH
# BUTTONS
btn_3days = Button(frame_graph_1, text = '3 days', font = ('Helvetica', 12), bg = color_bg_2, fg = 'White',  borderwidth=0, command = lambda: show_graph(3))
btn_3days.place( x = 80, y = 25, anchor = 'center')

btn_1week = Button(frame_graph_1, text = '1 week', font = ('Helvetica', 12), bg = color_bg_2, fg = 'White', command = lambda: show_graph(7))
btn_1week.place( x = 250, y = 25, anchor = 'center')

btn_1month = Button(frame_graph_1, text = '1 month', font = ('Helvetica', 12), bg = color_bg_2, fg = 'White', command = lambda: show_graph(30))
btn_1month.place( x = 420, y = 25, anchor = 'center')

# GRAPH
x = []
y = []
fig = plt.Figure(dpi = 100)
fig, ax = plt.subplots()
fig.set_figheight(3.5)
fig.set_figwidth(5)
line = FigureCanvasTkAgg(fig, frame_graph_2)
line.get_tk_widget().pack()
ax.plot(x, y, color = 'blue', linewidth = 2.0, marker = 'o', markersize = 8)
ax.set_xticks(x)
ax.tick_params(axis = "x", labelsize = 8)
ax.tick_params(axis = "y", labelsize = 8)


df_cache_data.to_csv('cache_data.csv', index=False)
root.mainloop()
