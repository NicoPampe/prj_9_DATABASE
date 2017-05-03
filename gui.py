#!/usr/bin/python3

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import font
import pg8000

#TODO: Can this be populated with a query instead? There's more items since I got 0.15 working.
factorio_item_array = ['piercing-bullet-magazine','rocket','explosive-rocket','shotgun-shell','piercing-shotgun-shell','railgun-dart','poison-capsule','slowdown-capsule','basic-grenade','defender-capsule','distractor-capsule','destroyer-capsule','basic-electric-discharge-defense-remote','copper-plate','iron-plate','stone-brick','wood','wooden-chest','iron-stick','iron-axe','stone-furnace','boiler','steam-engine','iron-gear-wheel','electronic-circuit','basic-transport-belt','basic-mining-drill','burner-mining-drill','basic-inserter','burner-inserter','pipe','offshore-pump','copper-cable','small-electric-pole','pistol','submachine-gun','basic-bullet-magazine','basic-armor','radar','small-lamp','pipe-to-ground','assembling-machine-1','repair-pack','gun-turret','night-vision-equipment','energy-shield-equipment','energy-shield-mk2-equipment','battery-equipment','battery-mk2-equipment','solar-panel-equipment','fusion-reactor-equipment','basic-laser-defense-equipment','basic-electric-discharge-defense-equipment','basic-exoskeleton-equipment','basic-oil-processing','advanced-oil-processing','heavy-oil-cracking','light-oil-cracking','sulfuric-acid','plastic-bar','solid-fuel-from-light-oil','solid-fuel-from-petroleum-gas','solid-fuel-from-heavy-oil','sulfur','lubricant','empty-barrel','fill-crude-oil-barrel','empty-crude-oil-barrel','flame-thrower-ammo','steel-plate','long-handed-inserter','fast-inserter','smart-inserter','speed-module','speed-module-2','speed-module-3','productivity-module','productivity-module-2','productivity-module-3','effectivity-module','effectivity-module-2','effectivity-module-3','player-port','fast-transport-belt','express-transport-belt','solar-panel','assembling-machine-2','assembling-machine-3','car','straight-rail','curved-rail','diesel-locomotive','cargo-wagon','train-stop','rail-signal','heavy-armor','basic-modular-armor','power-armor','power-armor-mk2','iron-chest','steel-chest','smart-chest','wall','flame-thrower','land-mine','rocket-launcher','shotgun','combat-shotgun','railgun','science-pack-1','science-pack-2','science-pack-3','alien-science-pack','lab','red-wire','green-wire','basic-transport-belt-to-ground','fast-transport-belt-to-ground','express-transport-belt-to-ground','basic-splitter','fast-splitter','express-splitter','advanced-circuit','processing-unit','logistic-robot','construction-robot','logistic-chest-passive-provider','logistic-chest-active-provider','logistic-chest-storage','logistic-chest-requester','rocket-defense','roboport','steel-axe','big-electric-pole','substation','medium-electric-pole','basic-accumulator','steel-furnace','electric-furnace','basic-beacon','blueprint','deconstruction-planner','pumpjack','oil-refinery','engine-unit','electric-engine-unit','flying-robot-frame','explosives','battery','storage-tank','small-pump','chemical-plant','small-plane','laser-turret']

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
        # TODO: uncomment
        # self.database_setup()
        
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
            if row==50:
                row = 0
                column += 1
                pass
            pass

        self.search_button = Checkbutton(self.search_frame, text="Rocket",  variable = self.factorio_item_input['rocket'], command = self.search_action).grid(row=1, column = 0, sticky=W)

    def search_action(self):
        self.current_search_results = []
        for item, var in self.factorio_item_input.items():
            if var.get():
                print('The item to look up: ' + str(item))
                self.current_search_results.extend(self.search_by_item(str(item)))

        self.item_recusion(self.current_search_results)

        print('\nfinished tree\n\n')


    def item_recusion(self, items):
        for item in items:
            print(item)
            if item[0] == 'copper-ore' or item[0] == 'iron-ore' or item[0] == 'coal' or item[0] == 'stone' or item[0] == 'raw-wood' or item[0] == 'water' or item[0] == 'crude-oil' or item[0] == 'alien-artifact':
                print()
            else:
                additional_itesm = self.search_by_item(item[0])
                self.item_recusion(additional_itesm)


###################
# EDIT BELOW HERE #
###################
    def database_setup(self):
        # query = """SELECT ar.name 
        #            FROM artist AS ar"""

        print('set up')

        query1 = """DROP TABLE IF EXISTS factorio_recipe cascade"""
        query2 = """CREATE TABLE factorio_recipe(
                       id serial, 
                       recipe TEXT, 
                       resources TEXT, 
                       amount TEXT)""" 
        query3 = """(%s)copy factorio_recipe(recipe, resources, amount) FROM   'factorio_015_items.csv' WITH (DELIMITER ',')"""

        # query = """DROP TABLE IF EXISTS factorio_recipe cascade;
        #            CREATE TABLE factorio_recipe(
        #                id serial, 
        #                recipe TEXT, 
        #                resources TEXT, 
        #                amount TEXT); 
        #            \copy factorio_recipe(recipe, resources, amount) FROM 'factorio_recipe.csv' WITH (DELIMITER ',');"""

        try:
            self.cursor.execute(query1, ( ))
            self.cursor.execute(query2, ( ))
            self.cursor.execute(query3, (r"\\", ))
            self.db.commit()

            # resultset = self.cursor.fetchall()
            # return resultset

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


