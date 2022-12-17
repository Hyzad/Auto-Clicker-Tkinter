import tkinter as tk
import threading
import mouse
from tkinter import messagebox
from pynput import keyboard
from tkinter import ttk
from time import sleep
from numpy import random

class Auto(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('700x300')
        self.title("Billio Nar's Mouse Utility Tool")
        self.rng = random.default_rng()

        self.start_off = 'Start'
        self.start_on = 'Stop'
        self.clicking = False
        self.get_pos_button = False

        self.fixed_mouse = False

        self.validate_cmd = (self.register(self.validate_input), '%P')

        self.default_text = 'None'

        self.create_inputs()
        self.keybind_start()

    # function that creates all the inputs 
    def create_inputs(self):
        self.frame = ttk.Frame(self)
        self.frame.pack(padx=10, pady=10, fill='x')

        self.duration_label = ttk.Label(self.frame, text='Run Duration (s):')
        self.duration_label.grid(column=0, row=0, sticky='W')
        self.duration_text = tk.StringVar()
        self.duration_box = ttk.Entry(
            self.frame, textvariable=self.duration_text, validate='all', validatecommand=self.validate_cmd)
        self.duration_box.grid(column=1, row=0, pady=10, padx=10)

        self.min_click_label = ttk.Label(
            self.frame, text='Min Time Between Clicks (ms):')
        self.min_click_label.grid(column=0, row=1, sticky='W')
        self.min_click_text = tk.StringVar()
        self.min_click_box = ttk.Entry(
            self.frame, textvariable=self.min_click_text, validate='all', validatecommand=self.validate_cmd)
        self.min_click_box.grid(column=1, row=1, pady=10, padx=10)

        self.max_click_label = ttk.Label(
            self.frame, text='Max Time Between Clicks (ms):')
        self.max_click_label.grid(column=0, row=2, sticky='W')
        self.max_click_text = tk.StringVar()
        self.max_click_box = ttk.Entry(
            self.frame, textvariable=self.max_click_text, validate='all', validatecommand=self.validate_cmd)
        self.max_click_box.grid(column=1, row=2, pady=10, padx=10)

        self.min_down_label = ttk.Label(
            self.frame, text='Min Time Between Mouse Up/Down (ms):')
        self.min_down_label.grid(column=2, row=0, sticky='W')
        self.min_down_text = tk.StringVar()
        self.min_down_box = ttk.Entry(
            self.frame, textvariable=self.min_down_text, validate='all', validatecommand=self.validate_cmd)
        self.min_down_box.grid(column=3, row=0, pady=10, padx=10)

        self.max_down_label = ttk.Label(
            self.frame, text='Max Time Between Mouse Up/Down (ms):')
        self.max_down_label.grid(column=2, row=1, sticky='W')
        self.max_down_text = tk.StringVar()
        self.max_down_box = ttk.Entry(
            self.frame, textvariable=self.max_down_text, validate='all', validatecommand=self.validate_cmd)
        self.max_down_box.grid(column=3, row=1, pady=10, padx=10)

        # label and button for keybind
        self.keybind_label = ttk.Label(self.frame, text='Choose a Keybind:')
        self.keybind_label.grid(column=2, row=2, sticky='W')
        self.keybind_button = ttk.Button(
            self.frame, text=self.default_text, command=self.keybind_clicked)
        self.keybind_button.grid(column=3, row=2, pady=10, padx=10)
        
        # frame containing position widgets
        self.mouse_frame = ttk.Frame(self.frame)
        self.mouse_frame.grid(column=0, row=3, columnspan=2, sticky='W')

        # label and check box for using mouse pos
        self.mouse_checklabel = ttk.Label(self.mouse_frame, text='Use Coords?')
        self.mouse_checkvar = tk.IntVar()
        self.mouse_checkbutton = tk.Checkbutton(self.mouse_frame, variable=self.mouse_checkvar, command=None, onvalue=1, offvalue=0)

        # widgets for x and y coords
        self.mouse_xlabel = ttk.Label(self.mouse_frame, text='x:')
        self.mouse_xtext = tk.StringVar()
        self.mouse_xcoord = ttk.Entry(
            self.mouse_frame, textvariable=self.mouse_xtext, width=5, validate='all', validatecommand=self.validate_cmd)
        self.mouse_ylabel = ttk.Label(self.mouse_frame, text='y:')
        self.mouse_ytext = tk.StringVar()
        self.mouse_ycoord = ttk.Entry(
            self.mouse_frame, textvariable=self.mouse_ytext, width=5, validate='all', validatecommand=self.validate_cmd)
        # button to set mouse coords
        self.mouse_pos_button = ttk.Button(
            self.mouse_frame, text='Get Coords', command=self.mouse_getpos)

        # puts all 
        self.mouse_checklabel.grid(column=0, row=0)
        self.mouse_checkbutton.grid(column=1, row=0)
        self.mouse_pos_button.grid(column=2, row=0, pady=10, padx=10)
        self.mouse_xlabel.grid(column=3, row=0)
        self.mouse_xcoord.grid(column=4, row=0)
        self.mouse_ylabel.grid(column=5, row=0)
        self.mouse_ycoord.grid(column=6, row=0)
        

        # start button
        self.start_button = ttk.Button(self.frame, text=self.start_off, command=self.start_clicked)
        self.start_button.grid(column=3, row=3, pady=10, padx=10)


    def start_clicked(self):
        #print('this', self.duration_box.get(), "---")
        if not self.duration_box.get():
            self.duration_box.insert(0, 120)
        if not self.max_click_box.get():
            self.max_click_box.insert(0, 350)
        if not self.min_click_box.get():
            self.min_click_box.insert(0, 300)
        if not self.min_down_box.get():
            self.min_down_box.insert(0, 20)
        if not self.max_down_box.get():
            self.max_down_box.insert(0, 35)
        

        if self.mouse_checkvar.get() == 1 and self.mouse_xcoord.get() and self.mouse_ycoord.get() and self.clicking == False:
            x = self.mouse_xcoord.get()
            y = self.mouse_ycoord.get()
            mouse.move(x, y)
        
        
        dur_check = self.duration_box.get().isnumeric()
        max_click_check = self.max_click_box.get().isnumeric()
        min_click_check = self.min_click_box.get().isnumeric()
        max_down_check = self.max_down_box.get().isnumeric()
        min_down_check = self.min_down_box.get().isnumeric()

        if dur_check and max_click_check and min_click_check and max_down_check and min_down_check:
            self.clicking = not self.clicking
            if self.clicking == True:

                self.start_button['text'] = self.start_on
                click = threading.Thread(target=self.clicking_loop)
                click.start()

            elif self.clicking == False:
                self.start_button['text'] = self.start_off
        else:
            messagebox.showerror('ERROR','TIME MUST BE A NUMBER')

    # the clicker 
    def clicking_loop(self):
        click_times = self.random_array(self.min_click_box, self.max_click_box)
        down_times = self.random_array(self.min_down_box, self.max_down_box)
        # add make the time duration actually matter
        while self.clicking == True:
            for i in range(self.array_length):
                if self.clicking == False:
                    break
                print(click_times[i])
                sleep(click_times[i])
                if self.clicking == False:
                    break
                mouse.press(button='left')
                if self.clicking == False:
                    break
                print(down_times[i])
                sleep(down_times[i])
                if self.clicking == False:
                    break
                mouse.release(button='left')
    # starts listening for key clicks when the keybind set button is pressed
    def keybind_clicked(self):
        listener = keyboard.Listener(
            on_press=self.keybind_listener,
            on_release=self.keybind_release)
        listener.start()
    # what happens when a key is pressed while the keybind_clicked listener is started
    def keybind_listener(self, key):
        try:
            self.keybind_button['text'] = key.char
        except AttributeError:
            self.keybind_button['text'] = key
    # what happens when the key bind is released - I dont think this does anything
    def keybind_release(self, key):
        return False
    # listener for when the selected keybind is pressed
    def keybind_start (self):
        listener2 = keyboard.Listener(
            on_press=self.keybind_start_listen)
        listener2.start()
    # starts the auto clicker if the keybind is pressed
    def keybind_start_listen(self, key):
        try:
            if key.char == self.keybind_button['text']:
                self.start_clicked()
        except AttributeError:
            if key == self.keybind_button['text']:
                self.start_clicked()

    # generates a random array for the times given to the function
    def random_array(self, min_time, max_time):
        self.max_time = int(max_time.get())
        self.min_time = int(min_time.get())
        #sets the max time to be 1 higher than the min time if it is lower than the min time
        if self.max_time <= self.min_time:
            max_time.delete(0, tk.END)
            self.max_time = self.min_time + 1
            max_time.insert(0, str(self.max_time))

        min_down_time = int(self.min_down_box.get())/1000
        min_click_time = int(self.min_click_box.get())/1000
        duration = int(self.duration_box.get())

        self.array_length = int(duration/(min_down_time + min_click_time))

        return self.rng.integers(self.min_time, self.max_time, self.array_length)/1000
    
    # only allows numbers to be written in boxes
    def validate_input(self, value):
        if value.isdigit() or value == "":
            return True
        else:
            return False

    # will draw a transparent window on the screen that listens for a mouse click then inserts it into 
    # does it need to be a new window or just a listener? ye draw a window that says to click to set the coordinates
    def mouse_getpos(self):
        self.get_pos_button = not self.get_pos_button
        def click_func():
            mouse_pos = mouse.get_position()
            x = str(mouse_pos[0])
            y = str(mouse_pos[1])
            if self.get_pos_button == True:
                self.mouse_xcoord.insert(0, x)
                self.mouse_ycoord.insert(0, y)
                self.get_pos_button = not self.get_pos_button
        mouse.on_click(click_func)

            


        




# starts the program
if __name__ == "__main__":
    auto = Auto()
    auto.mainloop()