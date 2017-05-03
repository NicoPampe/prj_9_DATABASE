#!/usr/bin/python3

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import font
import pg8000
import math

#TODO: Can this be populated with a query instead? There's more items since I got 0.15 working.
factorio_item_array = []

# implements a simple login window
class LoginWindow:
    def __init__(self, window):
        self.window = window

        self.window.title('Login')
        self.window.grid()

        # styling
        self.font = font.Font(family = 'Arial', size = 12)
        Style().configure('TButton', font = self.font)
        Style().configure('TLabel', font = self.font)

	# setup widgets
        self.user_label = Label(window, text='Username: ')
        self.user_label.grid(column = 0, row = 0)
        self.user_input = Entry(window, width = 20, font = self.font)
        self.user_input.grid(column = 1, row = 0)

        self.pw_label = Label(window, text='Password: ')
        self.pw_label.grid(column = 0, row = 1)
        self.pw_input = Entry(window, width = 20, show='*', font = self.font)
        self.pw_input.grid(column = 1, row = 1)

        self.button_frame = Frame(window)
        self.button_frame.grid(column = 0, columnspan = 2, row = 2)

        self.ok_button = Button(self.button_frame, text='OK', command=self.ok_action)
        self.ok_button.grid(column = 0, row = 0)

        self.cancel_button = Button(self.button_frame, text='Cancel', command=quit)
        self.cancel_button.grid(column = 1, row=0)

        self.window.bind('<Return>', self.enter_action)
        self.user_input.focus_set()

    def enter_action(self, event):
        self.ok_action()

    def ok_action(self):
        try:        
            credentials = {'user'     : self.user_input.get(),
                           'password' : self.pw_input.get(),
                           'database' : 'csci403',
                           'host'     : 'flowers.mines.edu' }
            self.db = pg8000.connect(**credentials)
            self.window.destroy()
        except pg8000.Error as e:
            messagebox.showerror('Login Failed', e.args[2])
# end LoginWindow


class Application:
    def __init__(self, window, db):
        self.window = window
        self.window.title('Factorio Look Up Table')
        self.window.grid()

        self.db = db
        self.cursor = db.cursor()
        
        # Run to set up the factorio database
        self.database_setup()
        
        # styling
        self.font = font.Font(family = 'Arial', size = 12)
        Style().configure('TButton', font = self.font)
        Style().configure('TLabel', font = self.font)

        # search portion of GUI
        self.search_frame = Frame(window);
        self.search_frame.grid(row = 0, column = 0)
        self.search_sb = Scrollbar(self.search_frame)
        # self.search_sb.pack(side = RIGHT, fill = Y)
        # self.search_lb = Listbox(self.search_frame, height = 10, width = 80, font = self.font, exportselection = 0)
        # self.search_lb.pack()
        # self.search_lb.config(yscrollcommand = self.search_sb.set)
        # self.search_sb.config(command = self.search_lb.yview)


        self.current_search_results = []
        self.factorio_item_input = {}
        for item in factorio_item_array:
            self.factorio_item_input[item] = IntVar()
            pass
        
        row = 0
        column = 0
        for item in factorio_item_array:
            self.search_button = Checkbutton(self.search_frame, text=item,  variable = self.factorio_item_input[item], command = self.search_action).grid(row=row, column=column, sticky=W)
            row += 1
            if row==30:
                row = 0
                column += 1
                pass
            pass

        self.search_button = Checkbutton(self.search_frame, text="Rocket",  variable = self.factorio_item_input['rocket'], command = self.search_action).grid(row=1, column = 0, sticky=W)

    def search_action(self):
        self.mult = 1
        self.current_search_results = []
        for item, var in self.factorio_item_input.items():
            if var.get():
                print('The item to look up: ' + str(item))
                self.current_search_results.extend(self.search_by_item(str(item)))

        self.tottal_items = {}
        if len(self.current_search_results) != 0:
            self.item_recusion(self.current_search_results)
            print('\n..........\nfinished tree\n..........')
            print('total raw items needed:')
            print(self.tottal_items)
            pass



    def item_recusion(self, items):
        for item in items:
            print(item)
            if item[0] in self.tottal_items.keys():
                self.tottal_items[item[0]] += float(item[1])
            else:
                self.tottal_items[item[0]] = float(item[1])
            if item[0] == 'copper-ore' or item[0] == 'iron-ore' or item[0] == 'coal' or item[0] == 'stone' or item[0] == 'raw-wood' or item[0] == 'water' or item[0] == 'crude-oil' or item[0] == 'alien-artifact':
                print()
            else:
                self.mult = float(item[1])
                additional_itesm = self.search_by_item(item[0])
                for x in range(0,len(additional_itesm)):
                    tmp = additional_itesm[x][1] 
                    additional_itesm[x][1] = float(item[1]) * float(tmp)
                    pass
                self.item_recusion(additional_itesm)


###################
# EDIT BELOW HERE #
###################
    def database_setup(self):
        query1 = """DROP TABLE IF EXISTS factorio_recipe cascade"""
        query2 = """CREATE TABLE factorio_recipe(
                       id serial, 
                       recipe TEXT, 
                       resources TEXT, 
                       amount TEXT)""" 
        query3 = """(%s)copy factorio_recipe(recipe, resources, amount) FROM   'factorio_015_items.csv' WITH (DELIMITER ',')"""

        query_get_names = """SELECT DISTINCT recipe FROM factorio_recipe"""

        # query = """DROP TABLE IF EXISTS factorio_recipe cascade;
        #            CREATE TABLE factorio_recipe(
        #                id serial, 
        #                recipe TEXT, 
        #                resources TEXT, 
        #                amount TEXT); 
        #            \copy factorio_recipe(recipe, resources, amount) FROM 'factorio_recipe.csv' WITH (DELIMITER ',');"""

        try:
            # self.cursor.execute(query1, ( ))
            # self.cursor.execute(query2, ( ))
            # self.cursor.execute(query3, (r"\\", ))
            self.cursor.execute(query_get_names, ( ))

            resultset = self.cursor.fetchall()
            for item in resultset:
                factorio_item_array.extend(item)
            return resultset

        except pg8000.Error as e:
            messagebox.showerror('Database error', e.args[2])
            return None

    def search_by_item(self, search_string):
        query = """SELECT resources, amount FROM factorio_recipe 
                    WHERE recipe = (%s)"""

        try:
            self.cursor.execute(query, (search_string, ))

            resultset = self.cursor.fetchall()
            return resultset

        except pg8000.Error as e:
            messagebox.showerror('Database error', e.args[2])
            return None

# end of Application


############################
# application startup code #
############################

lw = Tk()
lwapp = LoginWindow(lw)
lw.mainloop()

window = Tk()
app = Application(window, lwapp.db)
window.mainloop()


