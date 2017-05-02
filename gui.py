#!/usr/bin/python3

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import font
import pg8000

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
            # credentials = {'user'     : self.user_input.get(),
            #                'password' : self.pw_input.get(),
            #                'database' : 'csci403',
            #                'host'     : 'flowers.mines.edu' }
            credentials = {'user'     : 'npampe',
                           'password' : 'Magicle101',
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

        # search results
        # self.results_frame = Frame(window)
        # self.results_frame.grid(row = 1, column = 0)
        # self.results_sb = Scrollbar(self.results_frame)
        # self.results_sb.pack(side = RIGHT, fill = Y)
        # self.results_lb = Listbox(self.results_frame, height = 10, width = 80, font = self.font, exportselection = 0)
        # self.results_lb.pack()
        # self.results_lb.config(yscrollcommand = self.results_sb.set)
        # self.results_sb.config(command = self.results_lb.yview)

        # search results listbox callbacks
        # self.results_lb.bind('<<ListboxSelect>>', self.album_select)

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



    def album_select(self, event):
        if len(self.results_lb.curselection()):
            self.edit_album_button.config(state = NORMAL)
            self.delete_album_button.config(state = NORMAL)
        else:
            self.edit_album_button.config(state = DISABLED)
            self.delete_album_button.config(state = DISABLED)

    def recreate_edit_frame(self):
        self.edit_frame.destroy()
        self.edit_frame = Frame(window)
        self.edit_frame.grid(row = 2, column = 0, padx = 10, pady = 10)

    def show_add_artist(self):
        self.recreate_edit_frame()
        add_artist_label = Label(self.edit_frame, text = 'Add Artist')
        add_artist_label.grid(row = 0, columnspan = 3, column = 0)
        artist_entry_label = Label(self.edit_frame, text = 'New artist name: ')
        artist_entry_label.grid(row = 1, column = 0)
        self.add_artist_entry = Entry(self.edit_frame, width = 40, font = self.font)
        self.add_artist_entry.grid(row = 1, column = 1)
        save = Button(self.edit_frame, text = 'Save', command = self.save_new_artist)
        save.grid(row = 1, column = 2)

    def save_new_artist(self):
        if len(self.add_artist_entry.get()) == 0:
            messagebox.showerror('Error Saving Artist', 'Please enter an artist name.')
        else:
            self.insert_artist(self.add_artist_entry.get())
            self.recreate_edit_frame()

    def show_add_album(self):
        self.recreate_edit_frame()
        artist_list = self.get_artists()
        add_album_label = Label(self.edit_frame, text = 'Add Album')
        add_album_label.grid(row = 0, column = 0, columnspan = 2)
        artist_choose_label = Label(self.edit_frame, text = 'Choose artist: ')
        artist_choose_label.grid(row = 1, column = 0)
        self.artist_cb = Combobox(self.edit_frame, values = artist_list, font = self.font)
        self.artist_cb.grid(row = 1, column = 1)
        album_entry_label = Label(self.edit_frame, text = 'Enter album title: ')
        album_entry_label.grid(row = 2, column = 0)
        self.album_entry = Entry(self.edit_frame, width = 40, font = self.font)
        self.album_entry.grid(row = 2, column = 1)
        year_entry_label = Label(self.edit_frame, text = 'Enter album year: ')
        year_entry_label.grid(row = 3, column = 0)
        self.year_entry = Entry(self.edit_frame, width = 40, font = self.font)
        self.year_entry.grid(row = 3, column = 1)
        save = Button(self.edit_frame, text = 'Save', command = self.save_new_album)
        save.grid(row = 4, column = 0, columnspan = 2)

    def save_new_album(self):
        if len(self.artist_cb.get()) == 0:
            messagebox.showerror('Error Saving Album', 'Please select an artist.')
        elif len(self.album_entry.get()) == 0:
            messagebox.showerror('Error Saving Album', 'Please enter an album title.')
        else:
            self.insert_album(self.artist_cb.get(), self.album_entry.get(), self.year_entry.get())
            self.recreate_edit_frame()

    def show_edit_album(self):
        self.recreate_edit_frame()
        rows = self.results_lb.curselection()
        artist, album_title, year, album_id = self.current_search_results[rows[0]]
        edit_album_label = Label(self.edit_frame, text = 'Edit Album')
        edit_album_label.grid(row = 0, column = 0, columnspan = 2)
        artist_label = Label(self.edit_frame, text = 'Artist:')
        artist_label.grid(row = 1, column = 0)
        artist_entry = Entry(self.edit_frame, width = 40, font = self.font)
        artist_entry.insert(0, artist)
        artist_entry.config(state = DISABLED)
        artist_entry.grid(row = 1, column = 1)
        album_entry_label = Label(self.edit_frame, text = 'Album title: ')
        album_entry_label.grid(row = 2, column = 0)
        self.album_entry = Entry(self.edit_frame, width = 40, font = self.font)
        self.album_entry.insert(0, album_title)
        self.album_entry.grid(row = 2, column = 1)
        year_entry_label = Label(self.edit_frame, text = 'Album year: ')
        year_entry_label.grid(row = 3, column = 0)
        self.year_entry = Entry(self.edit_frame, width = 40, font = self.font)
        self.year_entry.insert(0, str(year))
        self.year_entry.grid(row = 3, column = 1)
        save = Button(self.edit_frame, text = 'Save', command = self.save_edited_album)
        save.grid(row = 4, column = 0, columnspan = 2)

    def save_edited_album(self):
        if len(self.album_entry.get()) == 0:
            messagebox.showerror('Error Saving Album', 'Please enter an album title.')
        else:
            rows = self.results_lb.curselection()
            artist, album_title, year, album_id = self.current_search_results[rows[0]]
            self.current_search_results[rows[0]][1] = self.album_entry.get()
            self.current_search_results[rows[0]][2] = self.year_entry.get()
            self.update_album(album_id, self.album_entry.get(), self.year_entry.get())
            self.results_lb.delete(rows[0], rows[0])
            s = artist + ' - ' + self.album_entry.get() + ' (' + str(self.year_entry.get()) + ')'
            self.results_lb.insert(rows[0], s)
            self.recreate_edit_frame()

    def remove_album(self):
        self.recreate_edit_frame()
        if messagebox.askyesno('Delete Confirmation', 'Are you sure?'):
            rows = self.results_lb.curselection()
            artist, album_title, year, album_id = self.current_search_results[rows[0]]
            self.delete_album(album_id)
            self.results_lb.delete(ANCHOR)
        

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
        query3 = """(%s)copy factorio_recipe(recipe, resources, amount) FROM   'factorio_recipe.csv' WITH (DELIMITER ',')"""

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

    def search_by_artist(self, search_string):
        query = """SELECT ar.name, al.title, al.year, al.id 
                   FROM artist AS ar, album AS al
                   WHERE lower(ar.name) LIKE lower(%s)
                   AND ar.id = al.artist_id
                   ORDER BY ar.name, al.year, al.title"""

        search_string = '%' + search_string + '%'
        try:
            self.cursor.execute(query, (search_string, ))

            resultset = self.cursor.fetchall()
            return resultset

        except pg8000.Error as e:
            messagebox.showerror('Database error', e.args[2])
            return None

    def search_by_album(self, search_string):
        query = """SELECT ar.name, al.title, al.year, al.id 
                   FROM artist AS ar, album AS al
                   WHERE lower(al.title) LIKE lower(%s)
                   AND ar.id = al.artist_id
                   ORDER BY al.year, al.title"""
        search_string = '%' + search_string + '%'
        try:
            self.cursor.execute(query, (search_string, ))

            resultset = self.cursor.fetchall()
            return resultset

        except pg8000.Error as e:
            messagebox.showerror('Database error', e.args[2])
            return None

    def insert_artist(self, artist_name):
        query =  """INSERT INTO artist (name) 
                    VALUES (%s)"""
        try:
            self.cursor.execute(query, (artist_name, ))
            self.db.commit()
            print('Saved new artist: ' + artist_name)

        except pg8000.Error as e:
            messagebox.showerror('Database error', e.args[2])
            return None


    def get_artists(self):
        query = """SELECT ar.name 
                   FROM artist AS ar"""
        try:
            self.cursor.execute(query, ( ))
            resultset = self.cursor.fetchall()
            result_string = []
            for name in resultset:
                result_string.append(name[0])
            return result_string

        except pg8000.Error as e:
            messagebox.showerror('Database error', e.args[2])
            return None

    def insert_album(self, artist_name, album_name, year):
        query =  """INSERT INTO album (artist_id, title, year) 
                    VALUES (
                        (SELECT id FROM artist WHERE name=%s),
                        %s, %s
                    )"""
        try:
            self.cursor.execute(query, (artist_name, album_name, year, ))
            self.db.commit()
            print('Save new album: ' + artist_name + ' - ' + album_name + ' (' + year + ')')

        except pg8000.Error as e:
            messagebox.showerror('Database error', e.args[2])
            return None

    def update_album(self, album_id, album_name, year):
        query =  """UPDATE album
                    SET title = %s, year = %s
                    WHERE id = %s"""
        try:
            self.cursor.execute(query, (album_name, year, album_id, ))
            self.db.commit()
            print('Update album: ' + str(album_id) + ': ' + album_name + ' (' + year + ')' + ' (Not yet implemented)')

        except pg8000.Error as e:
            messagebox.showerror('Database error', e.args[2])
            return None

    def delete_album(self, album_id):
        query =  """DELETE FROM album 
                    WHERE album.id = %s"""
        try:
            self.cursor.execute(query, (album_id, ))
            self.db.commit()
            print('Delete album: ' + str(album_id))

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


