from tkinter import *
from PIL import ImageTk, Image
import json
import os


# main window
root = Tk()
root.title('price comparison')
root.geometry('530x170')

bg_color = '#68d3ed'
root.configure(background=bg_color)

# create resized logo OBI
image_obi = Image.open('images/Obi.png')
resize_image_obi = image_obi.resize((250, 65,))
logo_img_obi = ImageTk.PhotoImage(resize_image_obi)
logo_label_obi = Label(image=logo_img_obi, background=bg_color)
logo_label_obi.grid(row=1, column=0, columnspan=2)

# create resized logo Leroy_Merlin
image_lm = Image.open('images/Leroy_Merlin.png')
resize_image_lm = image_lm.resize((220, 124,))
logo_img_lm = ImageTk.PhotoImage(resize_image_lm)
logo_label_lm = Label(image=logo_img_lm, background=bg_color)
logo_label_lm.grid(row=1, column=3, columnspan=2)

# vs text
vs = Label(root, text='vs', background=bg_color, font=('Helvetica', 30))
vs.grid(row=1, column=2)

# create info label and entry area
info_label = Label(root, text='Enter the name of the item you are looking for:', background=bg_color)
info_label.grid(row=0, column=0, columnspan=2)
search_e = Entry(root, width=30)
search_e.insert(0, 'OSB') # default text
search_e.grid(row=0, column=2, columnspan=2, pady=5)


def search():

    # resule window
    global top
    top = Toplevel()
    top.title('Your items')
    top.geometry('820x400')
    top.configure(background=bg_color)

    logo_label_obi = Label(top, image=logo_img_obi, background=bg_color)
    logo_label_obi.grid(row=0, column=0, columnspan=3)

    logo_label_lm = Label(top, image=logo_img_lm, background=bg_color)
    logo_label_lm.grid(row=0, column=4, columnspan=3)

    vs = Label(top, text='vs', background=bg_color, font=('Helvetica', 30))
    vs.grid(row=0, column=3)

    try:
        os.remove('lm.json')
        os.remove('obi.json')
    except:
        pass

    search_name = search_e.get()
    global obi_search, lm_search
    obi_search = search_name.replace(' ', '%20')
    lm_search = search_name.replace(' ', '+')
    with open('search_phrase.txt', 'w', encoding='utf8') as f:
        f.write(obi_search + '\n')
        f.write(lm_search)

    os.system('python my_spiders.py')

    show_results()

    close_button = Button(top, text='Exit', command=top.destroy, padx=5, pady=5, width = 10, fg='yellow', bg='green')
    close_button.grid(column=3, sticky=S)


# create search button
search_button = Button(root, text='search', command=search, width = 10, fg='yellow', bg='green')
search_button.grid(row=0, column=4, pady=5)


def show_results(): # from obi and lm json file
    try:
        with open('obi.json', 'r') as f:
            obi = json.loads(f.read())
            counter = 10
            for k, v in obi[0].items():
                item = Label(top, text=f'{k} -> {v}', background=bg_color).grid(row=counter, column=0, columnspan=3)
                counter += 1
    except:
        error = Label(top, text='Occured error', background=bg_color).grid(row=10, column=1, columnspan=3, pady=10)

    try:
        with open('lm.json', 'r') as f:
            obi = json.loads(f.read())
            counter = 10
            for k, v in obi[0].items():
                item = Label(top, text=f'{k} -> {v}', background=bg_color).grid(row=counter, column=4, columnspan=3)
                counter += 1
    except:
        error = Label(top, text='Occured error', background=bg_color).grid(row=10, column=6, columnspan=3, pady=10)




root.mainloop()



