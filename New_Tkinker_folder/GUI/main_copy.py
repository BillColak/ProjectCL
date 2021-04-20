import sqlite3
from tkinter import *
from tkinter import ttk
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from collections import Counter
import collector, DictatorWS, graphics

options = ['saskatoon', 'regina', 'vancouver', 'calgary', 'toronto', 'winnipeg', ]

options_two = ['mitsubishi rvr', 'honda crv']

conn = sqlite3.connect('CListest.sqlite')
cur = conn.cursor()
style.use("ggplot")

# TODO "Code should not just do what it's suppose to do, it should be scalable"

# TODO go over class inheretance and craigsapp how objects communicate wit each other.
# TODO Other websites
# TODO format Database
# TODO geoploting
# TODO make two different versions, lite, and enterprise which doesn't use sqlite.

# single: # 'paint_color''condition''cylinders' 'drive' 'fuel''car_size' 'title_status''transmission''car_type'
# duel: #'odometer''post_time' 'model''price'
# advanced: #'map_address''map_link'

class Main(object):
    def __init__(self, master):
        self.master = master

        def displayposts(self):
            posts = cur.execute("SELECT * FROM Pages").fetchall()

            count = 0
            self.list_books.delete(0, END)
            for post in posts:
                self.list_books.insert(count, str(post[0]) + " - " + str(post[14]))
                count += 1

            def postInfo(evt):
                value = str(self.list_books.get(self.list_books.curselection()))
                id = value.split('-')[0]
                post = cur.execute("SELECT * FROM Pages WHERE post_id=?", (id,))
                post_info = post.fetchall()

                self.list_details.delete(0, 'end')
                self.list_details.insert(0, "Model / Title : " + str(post_info[0][14]))
                self.list_details.insert(1, "Price : $" + str(post_info[0][15]))
                self.list_details.insert(2, "Odometer : " + str(post_info[0][7]))
                self.list_details.insert(3, "Condition : " + str(post_info[0][3]))
                self.list_details.insert(4, "Location : " + str(post_info[0][16]))
                self.list_details.insert(5, "Date Posted : " + str(post_info[0][12]))
                self.list_details.insert(6, "Type : " + str(post_info[0][11]))
                self.list_details.insert(7, "Drive : " + str(post_info[0][5]))
                self.list_details.insert(8, "Link : " + str(post_info[0][1]))

            self.list_books.bind('<<ListboxSelect>>', postInfo)

        # frames
        mainframe = Frame(self.master, bg='#9bc9ff')
        mainframe.pack(fill=BOTH, expand=TRUE)
        # top frames
        topFrame = Frame(mainframe, width=1350, height=70, bg='#9bc9ff', padx=20, relief=SUNKEN, borderwidth=2)
        topFrame.pack(side=TOP, fill=X, expand=TRUE)
        # centre frame
        centreFrame = Frame(mainframe, width=1350, relief=RIDGE, bg='#9bc9ff', height=680)
        centreFrame.pack(side=TOP, fill=BOTH, expand=TRUE)
        # centre left frame
        centreleftFrame = Frame(centreFrame, width=900, height=700, bg='#9bc9ff', borderwidth=2, relief='sunken')
        centreleftFrame.pack(side=LEFT, fill=BOTH, expand=TRUE)

        # centre right frame
        centreRightFrame = Frame(centreFrame, width=450, height=700, bg='#e0f0f0', borderwidth=2, relief='sunken')
        centreRightFrame.pack(fill=BOTH, expand=TRUE)
        # New Centre Right Tabs
        self.rtabs = ttk.Notebook(centreRightFrame, width=440, height=660, )
        self.rtabs.pack(fill=BOTH, expand=TRUE)

        self.rtab1_icon = PhotoImage(file=r'Images\books.png')
        self.rtab2_icon = PhotoImage(file=r'Images\members.png')

        self.rtab1 = ttk.Frame(self.rtabs)
        self.rtab2 = ttk.Frame(self.rtabs)

        self.rtabs.add(self.rtab1, text='Find Car', image=self.rtab2_icon, compound=LEFT)
        self.rtabs.add(self.rtab2, text='Database', image=self.rtab1_icon, compound=LEFT)

        # Search Database Bar
        search_bar = LabelFrame(self.rtab2, width=440, height=250, text='Search Database', bd=2, bg='#9bc9ff')
        search_bar.pack(fill=BOTH, expand=TRUE)

        self.ent_search = Entry(search_bar, width=30, bd=10)
        self.ent_search.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

        self.btn_search = Button(search_bar, text='Search', font='Times 12 bold', bg='#fcc324', fg='black',
                                 command=self.search_db)
        self.btn_search.grid(row=0, column=3, padx=15)

        # DB MAX PRICE
        self.dbl_max = Label(search_bar, text='Max Price:', font='times 12', bg='#9bc9ff', fg='black')
        self.dbl_max.grid(row=3, column=0, pady=5, sticky=W)
        self.dent_max = Entry(search_bar, width=5, )
        self.dent_max.grid(row=3, column=1, padx=1, sticky=W)
        # DB MIN PRICE
        self.dbl_min = Label(search_bar, text='Min Price:', font='times 12', bg='#9bc9ff', fg='black')
        self.dbl_min.grid(row=3, column=2, sticky=W)
        self.dnt_min = Entry(search_bar, width=5, )
        self.dnt_min.grid(row=3, column=3, padx=1, sticky=W)
        # DB  MODEL YEAR
        self.dbl_mod = Label(search_bar, text='Model Year:', font='times 12', bg='#9bc9ff', fg='black')
        self.dbl_mod.grid(row=4, column=0, pady=5, sticky=W)
        self.dnt_mod = Entry(search_bar, width=5, )
        self.dnt_mod.grid(row=4, column=1, padx=1, sticky=W)

        # DB ODOMETER
        self.dbl_odo = Label(search_bar, text='Odometer:', font='times 12', bg='#9bc9ff', fg='black')
        self.dbl_odo.grid(row=4, column=2, padx=1, sticky=W)
        self.dnt_odo = Entry(search_bar, width=5, )
        self.dnt_odo.grid(row=4, column=3, padx=1, sticky=W)

        # Entry Box Bar
        list_bar = LabelFrame(self.rtab1, width=440, height=250, text='Entry Box', bd=2, bg='#9bc9ff')
        list_bar.pack(fill=BOTH, expand=TRUE)

        # COMBO LOCATION AND ITEMS
        self.search_sub = Label(list_bar, text='Look For:', font='times 12', fg='black', bg='#9bc9ff')
        self.search_sub.grid(row=0, column=0, sticky=W)

        self.combo_sub = StringVar()
        self.combosub_ent = ttk.Combobox(list_bar, textvariable=self.combo_sub, width=20, height=40, )
        self.combosub_ent['values'] = options_two
        self.combosub_ent.grid(row=0, column=1, columnspan=3, padx=2, )

        self.search_loco = Label(list_bar, text='Location:', font='times 12', fg='black', bg='#9bc9ff')
        self.search_loco.grid(row=1, column=0, sticky=W)

        self.combo_loco = StringVar()
        self.combo_ent = ttk.Combobox(list_bar, textvariable=self.combo_loco, width=20, height=40, )
        self.combo_ent['values'] = options
        self.combo_ent.grid(row=1, column=1, columnspan=3, padx=2, )

        # BOOST BUTTON
        self.searchBoost = IntVar()
        boost = Radiobutton(list_bar, text='Search Boost:', var=self.searchBoost, value=3, bg='#9bc9ff')
        boost.grid(row=0, rowspan=2, column=5, )  # ADD MESSAGE BOX TO THIS
        # ENTER BUTTON
        self.btn_ent = Button(list_bar, text='Enter', font='Times 12 bold', bg='#fcc324', fg='black',
                              command=self.callback)
        self.btn_ent.grid(row=0, rowspan=2, columnspan=2, column=6, )
        self.btn_ent.config(height=1, width=5)

        # MAX PRICE
        self.lbl_max = Label(list_bar, text='Max Price:', font='times 12', bg='#9bc9ff', fg='black')
        self.lbl_max.grid(row=3, column=0, pady=5, sticky=W)
        self.ent_max = Entry(list_bar, width=5, )
        self.ent_max.grid(row=3, column=1, padx=1, )
        # MIN PRICE
        self.lbl_min = Label(list_bar, text='Min Price:', font='times 12', bg='#9bc9ff', fg='black')
        self.lbl_min.grid(row=3, column=2, sticky=W)
        self.ent_min = Entry(list_bar, width=5, )
        self.ent_min.grid(row=3, column=3, padx=1, )
        # MODEL YEAR
        self.lbl_mod = Label(list_bar, text='Model Year:', font='times 12', bg='#9bc9ff', fg='black')
        self.lbl_mod.grid(row=4, column=0, pady=5, )
        self.ent_mod = Entry(list_bar, width=5, )
        self.ent_mod.grid(row=4, column=1, padx=1, )
        # ODOMETER
        self.lbl_odo = Label(list_bar, text='Odometer:', font='times 12', bg='#9bc9ff', fg='black')
        self.lbl_odo.grid(row=4, column=2, padx=1)
        self.ent_odo = Entry(list_bar, width=5, )
        self.ent_odo.grid(row=4, column=3, padx=1, )

        self.listChoice = IntVar()
        rb1 = Radiobutton(list_bar, text='CraigsList', var=self.listChoice, value=1, bg='#9bc9ff')
        rb2 = Radiobutton(list_bar, text='AutoTrader', var=self.listChoice, value=2, bg='#9bc9ff')
        rb3 = Radiobutton(list_bar, text='Kijiji Auto', var=self.listChoice, value=3, bg='#9bc9ff')
        rb4 = Radiobutton(list_bar, text='Kijiji', var=self.listChoice, value=4, bg='#9bc9ff')
        rb1.grid(row=3, column=5, sticky=W)
        rb2.grid(row=3, column=6, sticky=W)
        rb3.grid(row=4, column=5, sticky=W)
        rb4.grid(row=4, column=6, sticky=W)

        bottom_box = LabelFrame(self.rtab1, width=400, text="Bottom Box", height=450, bd=2, bg='#9bc9ff')
        bottom_box.pack(fill=BOTH, expand=TRUE)

##############################################      BUTTON BAR  #################################################

        search_box = LabelFrame(self.rtab2, width=400, text="Search Box", height=450, bd=2, bg='#9bc9ff')
        search_box.pack(fill=BOTH, expand=TRUE)

        btn_one = Button(search_box, text='Transmission', bg='#fcc324', fg='black', font='Times 12', command=lambda: plot.car_transmission())
        btn_one.grid(row=2, column=1, padx=30, pady=10, sticky=W + E)
        btn_two = Button(search_box, text='Color', bg='#fcc324', fg='black', font='Times 12', command=lambda: plot.car_color())
        btn_two.grid(row=2, column=3, padx=30, pady=10, sticky=W + E)
        btn_three = Button(search_box, text='Condition', bg='#fcc324', fg='black', font='Times 12', command=lambda: plot.car_condition())
        btn_three.grid(row=2, column=5, padx=30, pady=10, sticky=W + E)
        btn_four = Button(search_box, text='Cylinders', bg='#fcc324', fg='black', font='Times 12', command=lambda: plot.car_cylinder())
        btn_four.grid(row=3, column=1, padx=30, pady=10, sticky=W + E)
        btn_five = Button(search_box, text='Status', bg='#fcc324', fg='black', font='Times 12', command=lambda: plot.car_title_status())
        btn_five.grid(row=3, column=3, padx=30, pady=10, sticky=W + E)
        btn_six = Button(search_box, text='Location', bg='#fcc324', fg='black', font='Times 12', command=lambda: plot.car_map_address())
        btn_six.grid(row=3, column=5, padx=30, pady=10, sticky=W + E)

        # DB Bar Lower Frame
        image_b = Frame(self.rtab2, width=400, height=350, bg='#9bc9ff')
        image_b.pack(fill=BOTH, expand=TRUE)

        self.combo_graph = StringVar()
        self.combograph_ent = ttk.Combobox(image_b, textvariable=self.combo_graph, width=20, height=40, state="readonly")
        self.combograph_ent['values'] = ["All", "Top 10", "Top 5"]
        self.combograph_ent.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

        btn_four = Button(image_b, text='Button1', bg='#fcc324', fg='black', font='Times 12', command=lambda: stat_graph.prometer())
        btn_four.grid(row=3, column=1, padx=30, pady=10, sticky=W + E)
        btn_five = Button(image_b, text='Button2', bg='#fcc324', fg='black', font='Times 12',)
        btn_five.grid(row=3, column=3, padx=30, pady=10, sticky=W + E)
        btn_six = Button(image_b, text='Button3', bg='#fcc324', fg='black', font='Times 12',)
        btn_six.grid(row=3, column=5, padx=30, pady=10, sticky=W + E)
####################################################Tool Bar######################################################

        # UTILITY ONE
        self.iconbook = PhotoImage(file=r'Images\add_book.png')
        self.btnbook = Button(topFrame, text="Kijiji", image=self.iconbook, compound=LEFT, font='Times 12 bold',
                              justify=LEFT)
        self.btnbook.pack(side=LEFT, )

        # UTILITY TWO
        self.iconmember = PhotoImage(file=r'Images\users.png')
        self.btnmember = Button(topFrame, text='AutoTrader', font='Times 12 bold')
        self.btnmember.configure(image=self.iconmember, compound=LEFT)
        self.btnmember.pack(side=LEFT, )

        # UTILITY THREE
        self.icongive = PhotoImage(file=r'Images\givebook.png')
        self.btngive = Button(topFrame, text='MarketPlace', font='Times 12 bold', image=self.icongive, compound=LEFT)
        self.btngive.pack(side=LEFT, )

        ################################################Tabs############################################################

        self.tabs = ttk.Notebook(centreleftFrame, width=900, height=660, )
        self.tabs.pack(fill=BOTH, expand=TRUE)

        self.tab1_icon = PhotoImage(file=r'Images\books.png')
        self.tab2_icon = PhotoImage(file=r'Images\members.png')

        self.tab1 = ttk.Frame(self.tabs)
        self.tab2 = ttk.Frame(self.tabs)
        self.tab3 = ttk.Frame(self.tabs)
        self.tab4 = ttk.Frame(self.tabs)
        self.tab5 = ttk.Frame(self.tabs)

        # RESIZING WEIGHTS
        self.tab1.columnconfigure(0, weight=2)
        self.tab1.columnconfigure(1, weight=2)
        self.tab1.rowconfigure(0, weight=2)

        self.tabs.add(self.tab1, text='Post Listing', image=self.tab1_icon, compound=LEFT)
        self.tabs.add(self.tab2, text='Statistics', image=self.tab2_icon, compound=LEFT)
        self.tabs.add(self.tab3, text='TAB3', image=self.tab2_icon, compound=LEFT)
        # self.tabs.add(self.tab4, text='TAB4', image=self.tab2_icon, compound=LEFT)
        # self.tabs.add(self.tab5, text='TAB5', image=self.tab2_icon, compound=LEFT)

        # list books
        self.list_books = Listbox(self.tab1, width=40, height=30, font='times 12 bold')
        self.sbv = ttk.Scrollbar(self.tab1, orient=VERTICAL)
        self.sbh = ttk.Scrollbar(self.tab1, orient=HORIZONTAL)
        self.list_books.grid(row=0, column=0, padx=(10, 0), pady=10, sticky=N + S + E + W)

        self.list_books.config(yscrollcommand=self.sbv.set, xscrollcommand=self.sbh.set)
        self.sbv.config(command=self.list_books.yview)
        self.sbv.grid(row=0, column=0, sticky=N + S + E)

        self.sbh.config(command=self.list_books.xview)
        self.sbh.grid(row=1, column=0, sticky=W + E + S)

        # list details   ########## DO NOT DELETE THIS ################
        self.list_details = Listbox(self.tab1, width=75, height=30, font='times 12 bold')
        self.sbdy = ttk.Scrollbar(self.tab1, orient=VERTICAL)
        self.sbdh = ttk.Scrollbar(self.tab1, orient=HORIZONTAL)
        self.list_details.grid(row=0, column=1, padx=(10, 0), pady=10, sticky=N + S + E + W)

        self.list_details.config(yscrollcommand=self.sbdy.set, xscrollcommand=self.sbdh.set)
        self.sbdy.config(command=self.list_details.yview)
        self.sbdy.grid(row=0, column=1, sticky=N + S + E)

        self.sbdh.config(command=self.list_details.xview)
        self.sbdh.grid(row=1, column=1, sticky=W + E + S)

        ################################tab2############################################
        # self.goptions = Label(self.tab2, text='OK.. ', font='Times 14 bold', fg='black', bd=1, relief=SUNKEN, anchor=W)
        # self.goptions.pack(side=TOP, fill=X)

# Matplotlib Graphs
        displayposts(self)
        plot = graphics.Plotter(self.tab3)
        plotbar = NavigationToolbar2Tk(plot, self.tab3)
        plotbar.update()

        stat_graph = graphics.Statgraphs(self.tab2)
        toolbar = NavigationToolbar2Tk(stat_graph, self.tab2)
        toolbar.update()  # figure adjustment button gives and error

        # bar1 = FigureCanvasTkAgg(, self.tab4)
        # bar1.get_tk_widget().pack(side=TOP, fill=BOTH, expand=TRUE)
        # toolbar1 = NavigationToolbar2Tk(bar1, self.tab4)
        # toolbar1.update()


    def callback(self):
        location = str(self.combo_ent.get()).strip()
        min_price = ["min_price=", str(self.ent_min.get()).strip().replace(" ", "")]
        max_price = ["max_price=", str(self.ent_max.get()).strip().replace(" ", "")]
        look_for_craig = ["auto_make_model=", str(self.combosub_ent.get()).strip().replace(" ", "+")]
        model_year = ["min_auto_year=", str(self.ent_mod.get()).strip().replace(" ", "")]
        odometer = ["max_auto_miles=", str(self.ent_odo.get()).strip().replace(" ", "")]

        cquery = []
        qlist = [min_price, max_price, look_for_craig, model_year, odometer]
        for q in qlist:
            if q[1] != "":
                cquery.append(q[0] + q[1])
        url = f"https://{location}.craigslist.org/search/cta?" + ("&".join(cquery[0:]))
        print(url)

        open_collect = collector.Collector(url)
        count_car = open_collect.totalcount_factor()
        run_scraper = open_collect.collect()
        print(count_car)
        print(run_scraper)
        hugo = DictatorWS.Dictator(run_scraper)

    def search_db(self):
        value = self.ent_search.get()
        if len(value) > 0:
            search = cur.execute("SELECT * FROM Pages WHERE model LIKE ?", ('%' + value + '%',)).fetchall()
            self.list_books.delete(0, END)
            count = 0
            for post in search:
                self.list_books.insert(count, str(post[0]) + "-" + post[14])
                count += 1

        else:
            search = cur.execute("SELECT * FROM Pages").fetchall()
            self.list_books.delete(0, END)
            count = 0
            for post in search:
                self.list_books.insert(count, str(post[0]) + "-" + post[14])
                count += 1

def main():
    root = Tk()
    app = Main(root)
    root.title("AutoStop Software")
    root.configure(background='grey')
    root.geometry("1370x700+50+50")
    root.iconbitmap(r'Images\icon.ico')
    root.mainloop()


if __name__ == "__main__":
    main()
