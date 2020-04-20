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
if platform.system() == 'Darwin':
    from tkmacosx import Button

root = Tk()

root.title("Currency Exchanger")
root.geometry("500x700")
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

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


url_from = 'https://www.countryflags.io/th/flat/64.png'
req_from = Request(url_from, headers={'User-Agent': 'Mozilla/5.0'})
image_bytes_from = urlopen(req_from).read()
data_stream_from = io.BytesIO(image_bytes_from)
pil_image_from = Image.open(data_stream_from)
tk_image_from = ImageTk.PhotoImage(pil_image_from)

url_to = 'https://www.countryflags.io/th/flat/64.png'
req_to = Request(url_to, headers={'User-Agent': 'Mozilla/5.0'})
image_bytes_to = urlopen(req_to).read()
data_stream_to = io.BytesIO(image_bytes_to)
pil_image_to = Image.open(data_stream_to)
tk_image_to = ImageTk.PhotoImage(pil_image_to)

# ----------------------------------------- #

# ------------ FUNCTION ZONE ------------ #

def get_full_path(file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    full_path = os.path.join(dir_path, file_name)
    return full_path


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


def on_convert_click():
    curr_from = dd_from.get_value()
    curr_to = dd_to.get_value()
    amount = entry_amount.get()
    querystring = {"format":"json","from":curr_from,"to":curr_to,"amount":amount}
    exchange_rate_data = requests.request("GET", exchange_rate_url, headers=headers, params=querystring).json()
    converted_amount = exchange_rate_data['rates'][curr_to]['rate_for_amount']
    label_result.configure(text=converted_amount)


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
frame_top = Frame(root, width = 500, height = 100)
frame_top.grid(row = 0, column = 0, sticky = "NSEW")
frame_top.grid_propagate(0)
frame_mid = Frame(root, width = 500, height = 200)
frame_mid.grid(row = 1, column = 0, sticky = "NSEW")
frame_result = Frame(root, width = 500, height = 100)
frame_result.grid(row = 2, column = 0, sticky = "NSEW")
frame_graph = Frame(root, width = 500, height = 300,background = "Gray")
frame_graph.grid(row = 3, column = 0, sticky = "NSEW")

frame_mid_1 = Frame(frame_mid, width = 200, height=150)
frame_mid_1.grid(row = 0, column = 0, sticky = "NSEW")
frame_mid_2 = Frame(frame_mid, width = 100, height=150)
frame_mid_2.grid(row = 0, column = 1, sticky = "NSEW")
frame_mid_3 = Frame(frame_mid, width = 200, height=150)
frame_mid_3.grid(row = 0, column = 2, sticky = "NSEW")
frame_mid_4 = Frame(frame_mid, width = 200, height=50)
frame_mid_4.grid(row = 2, column = 0, columnspan = 3, sticky = "NSEW")

# FRAME TOP
label_1 = Label(frame_top, text = 'Enter amount', font = ('Helvetica', 16))
label_1.place(x = 250, y = 25, anchor="center")

entry_amount = Entry(frame_top, font = ('Helvetica', 20), justify = 'right')
entry_amount.place(x = 250, y = 60, anchor="center")


# FRAME MID
## MID 1
label_2 = Label(frame_mid_1, text = 'From', font = ('Helvetica', 16))
label_2.place(x = 100, y = 20, anchor = 'center')

code_from = StringVar()
dd_from = Combobox_Autocomplete(frame_mid_1, width = 15, justify = 'center', font = ('Helvetica', 16), list_of_items = list_currency, textvariable = code_from)
dd_from.place(x = 100, y = 60, anchor = 'center')
dd_from.bind('<Return>', (lambda _: update_flag_from(dd_from.get_value())))
dd_from.bind('<Button-1>', (lambda _: update_flag_from(dd_from.get_value())))

label_flag_from = Label(frame_mid_1, image = '', bg = 'White')
label_flag_from.place(x = 100, y = 120, anchor = 'center')

## MID 2

img_swap = ImageTk.PhotoImage(Image.open(get_full_path('swap.png')).resize((30, 30), Image.ANTIALIAS))
btn_swap = Button(frame_mid_2, image = img_swap,  width = 40, height = 40, command = on_swap_click)
btn_swap.place(x = 50, y = 60, anchor = 'center')

## MID 3
label_3 = Label(frame_mid_3, text = 'To', font = ('Helvetica', 16))
label_3.place(x = 100, y = 20, anchor = 'center')

code_to = StringVar()
dd_to = Combobox_Autocomplete(frame_mid_3, width = 15, justify = 'center', font = ('Helvetica', 16), list_of_items = list_currency, textvariable = code_to)
dd_to.place(x = 100, y = 60, anchor = 'center')
dd_to.bind('<Return>', (lambda _: update_flag_to(dd_to.get_value())))
dd_to.bind('<Button-1>', (lambda _: update_flag_to(dd_to.get_value())))

label_flag_to = Label(frame_mid_3, image = '', bg = 'White')
label_flag_to.place(x = 100, y = 120, anchor = 'center')


## MID 4
btn_convert = Button(frame_mid_4, text = 'Convert', font = ('Helvetica', 22), command = on_convert_click)
btn_convert.place( x = 250, y = 25, anchor = 'center')


# RESULT
label_result = Label(frame_result, text = '<Result>', font = ('Helvetica', 30))
label_result.place(x = 250, y = 50, anchor = 'center')

root.mainloop()
