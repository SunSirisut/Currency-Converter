import platform
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from autocomplete import *
if platform.system() == 'Darwin':
    from tkmacosx import Button


list_currency = ['AED', 'ALL', 'AMD', 'ANG', 'ARS', 'AUD', 'AZN', 'BDT', 'BGN', 'BHD', 'BND', 'BRL', 'BYN', 'CAD'
                , 'CHF', 'CLP', 'CNY', 'CZK', 'DKK', 'DZD', 'EGP', 'EUR', 'GBP', 'GEL', 'GHS', 'HKD', 'HRK', 'HUF'
                , 'IDR', 'ILS', 'INR', 'IQD', 'IRR', 'ISK', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KRW', 'KWD', 'KZT'
                , 'LAK', 'LBP', 'LKR', 'LYD', 'MAD', 'MDL', 'MKD', 'MMK', 'MXN', 'MYR', 'NOK', 'NPR', 'NZD', 'OMR'
                , 'PHP', 'PKR', 'PLN', 'QAR', 'RON', 'RSD', 'RUB', 'SAR', 'SEK', 'SGD', 'THB', 'TJS', 'TMT', 'TND'
                , 'TRY', 'TWD', 'UAH', 'USD', 'UZS', 'VND', 'ZAR']



root = Tk()

root.title("Currency Exchanger")
root.geometry("500x700")
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

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
dd_from = Combobox_Autocomplete(frame_mid_1, width = 15, justify = 'center', font = ('Helvetica', 16), list_of_items = list_currency)
dd_from.place(x = 100, y = 60, anchor = 'center')
label_flag_from = Label(frame_mid_1, text = '<FLAG>', bg = 'Black', fg = 'white')
label_flag_from.place(x = 100, y = 100, anchor = 'center')

## MID 2
img_swap = ImageTk.PhotoImage(Image.open('swap.png').resize((30, 30), Image.ANTIALIAS))
btn_swap = Button(frame_mid_2, image = img_swap,  width = 40, height = 40)
btn_swap.place(x = 50, y = 60, anchor = 'center')

## MID 3
label_3 = Label(frame_mid_3, text = 'To', font = ('Helvetica', 16))
label_3.place(x = 100, y = 20, anchor = 'center')
dd_to = Combobox_Autocomplete(frame_mid_3, width = 15, justify = 'center', font = ('Helvetica', 16), list_of_items = list_currency)
dd_to.place(x = 100, y = 60, anchor = 'center')
label_flag_to = Label(frame_mid_3, text = '<FLAG>', bg = 'Black', fg = 'white')
label_flag_to.place(x = 100, y = 100, anchor = 'center')


## MID 4
btn_convert = Button(frame_mid_4, text = 'Convert', font = ('Helvetica', 22))
btn_convert.place( x = 250, y = 25, anchor = 'center')


# RESULT
label_result = Label(frame_result, text = '<Result>', font = ('Helvetica', 30))
label_result.place(x = 250, y = 50, anchor = 'center')

root.mainloop()