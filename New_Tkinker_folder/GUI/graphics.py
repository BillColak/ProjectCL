import sqlite3
from tkinter import ttk
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # NavigationToolbar2Tk
from collections import Counter

conn = sqlite3.connect('CListest.sqlite')
cur = conn.cursor()


class Plotter(FigureCanvasTkAgg):

    def __init__(self, master):
        self.figure = Figure()
        super().__init__(self.figure, master=master)
        self.axes = self.figure.add_subplot(111)
        self.get_tk_widget().pack(side=TOP, fill=BOTH, expand=TRUE)

        # TODO turn this into Pandas Dataframe, can I utilized the vin numbers?

        car_db = cur.execute("SELECT * FROM Pages ORDER BY post_id")
        self.condition, self.cylinders, self.drive, self.fuel, self.paint_color, self.title_status, \
        self.transmission, self.map_address = ([] for i in range(8))
        for cars in car_db:

            self.condition.append(cars[3])  #
            self.cylinders.append(cars[4])  #
            self.paint_color.append(cars[8])  #
            self.title_status.append(cars[10])  #
            self.transmission.append(cars[11])  #
            self.map_address.append(str(cars[16]).strip())  #

    def car_color(self):
        list_counter = Counter(self.paint_color)
        paint, popularity = map(list, zip(*list_counter.most_common(len(list_counter))))

        self.axes.clear()
        x_list = paint
        y_list = popularity
        self.axes.bar(x_list, y_list, color='y')
        self.axes.set_title("Paint Color")
        self.draw_idle()

    def car_condition(self):
        list_counter = Counter(self.condition)
        paint, popularity = map(list, zip(*list_counter.most_common(len(list_counter))))

        self.axes.clear()
        x_list = paint
        y_list = popularity
        self.axes.bar(x_list, y_list, color='y')
        self.axes.set_title("Condition")
        self.draw_idle()

    def car_cylinder(self):
        list_counter = Counter(self.cylinders)
        paint, popularity = map(list, zip(*list_counter.most_common(len(list_counter))))

        self.axes.clear()
        x_list = paint
        y_list = popularity
        self.axes.bar(x_list, y_list, color='y')
        self.axes.set_title("Cylinders")
        self.draw_idle()

    def car_title_status(self):
        list_counter = Counter(self.title_status)
        paint, popularity = map(list, zip(*list_counter.most_common(len(list_counter))))

        self.axes.clear()
        x_list = paint
        y_list = popularity
        self.axes.bar(x_list, y_list, color='y')
        self.axes.set_title("Car Status")
        self.draw_idle()

    def car_map_address(self):
        list_counter = Counter(self.map_address)
        paint, popularity = map(list, zip(*list_counter.most_common(10)))

        print(list_counter)

        paint.reverse()
        popularity.reverse()

        self.axes.clear()
        x_list = paint
        y_list = popularity
        self.axes.barh(x_list, y_list, color='y')
        self.axes.set_title("Location")
        self.draw_idle()

    def car_transmission(self):
        list_counter = Counter(self.transmission)
        paint, popularity = map(list, zip(*list_counter.most_common(len(list_counter))))

        self.axes.clear()
        x_list = paint
        y_list = popularity
        self.axes.bar(x_list, y_list, color='y')
        self.axes.set_title("Transmission")
        self.draw_idle()


class Statgraphs(FigureCanvasTkAgg):

    def __init__(self, master):
        self.figure = Figure()
        super().__init__(self.figure, master=master)

        self.axes = self.figure.add_subplot(111)
        self.get_tk_widget().pack(side=TOP, fill=BOTH, expand=TRUE)

        car_db = cur.execute("SELECT * FROM Pages ORDER BY post_id")
        self.condition, self.cylinders, self.drive, self.fuel, self.paint_color, self.title_status, \
        self.transmission, self.map_address, self.price, self.odometer = ([] for i in range(10))
        for cars in car_db:
            # self.vin.append(cars[2])
            self.condition.append(cars[3])  #
            self.cylinders.append(cars[4])  #
            self.drive.append(cars[5])
            self.fuel.append(cars[6])
            self.paint_color.append(cars[8])  #
            # self.car_size.append(cars[9])
            self.title_status.append(cars[10])
            self.transmission.append(cars[11])
            # self.car_type.append(cars[12])
            self.map_address.append(str(cars[16]).strip())  #
            self.price.append(cars[7])
            self.odometer.append(cars[15])

    def prometer(self):
        self.axes.clear()
        x_list = self.price
        y_list = self.odometer

        # TODO to add colorscale or size need to fix the model shit

        self.axes.scatter(x_list, y_list, s=100, c='y', edgecolor='black', alpha=0.75)
        self.axes.set_title("Price vs Odometer")
        self.draw_idle()
