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
        self.title("Tem's Auto Clicker")

        self.rng = random.default_rng()
        #self.frame = ttk.Frame(self)

        self.start_off = 'Start'
        self.start_on = 'Stop'
        self.clicking = False

        self.default_text = 'c'

        self.create_inputs()
        self.keybind_start()

        
    def create_inputs(self):
        self.frame = ttk.Frame(self)
        self.frame.pack(padx=10, pady=10, fill='x')

        self.duration_label = ttk.Label(self.frame, text='Run Duration (s):')
        self.duration_label.grid(column=0, row=0, sticky='W')
        self.duration_text = tk.StringVar()
        self.duration_box = ttk.Entry(self.frame, textvariable=self.duration_text)
        self.duration_box.grid(column=1, row=0, pady=10, padx=10)

        self.min_click_label = ttk.Label(
            self.frame, text='Min Time Between Clicks (ms):')
        self.min_click_label.grid(column=0, row=1, sticky='W')
        self.min_click_text = tk.StringVar()
        self.min_click_box = ttk.Entry(
            self.frame, textvariable=self.min_click_text)
        self.min_click_box.grid(column=1, row=1, pady=10, padx=10)

        self.max_click_label = ttk.Label(
            self.frame, text='Max Time Between Clicks (ms):')
        self.max_click_label.grid(column=0, row=2, sticky='W')
        self.max_click_text = tk.StringVar()
        self.max_click_box = ttk.Entry(
            self.frame, textvariable=self.max_click_text)
        self.max_click_box.grid(column=1, row=2, pady=10, padx=10)

        self.min_down_label = ttk.Label(
            self.frame, text='Min Time Between Mouse Up/Down (ms):')
        self.min_down_label.grid(column=2, row=0, sticky='W')
        self.min_down_text = tk.StringVar()
        self.min_down_box = ttk.Entry(
            self.frame, textvariable=self.min_down_text)
        self.min_down_box.grid(column=3, row=0, pady=10, padx=10)

        self.max_down_label = ttk.Label(
            self.frame, text='Max Time Between Mouse Up/Down (ms):')
        self.max_down_label.grid(column=2, row=1, sticky='W')
        self.max_down_text = tk.StringVar()
        self.max_down_box = ttk.Entry(
            self.frame, textvariable=self.max_down_text)
        self.max_down_box.grid(column=3, row=1, pady=10, padx=10)

        self.keybind_label = ttk.Label(self.frame, text='Choose a Keybind:')
        self.keybind_label.grid(column=2, row=2, sticky='W')
        self.keybind_button = ttk.Button(
            self.frame, text=self.default_text, command=self.keybind_clicked)
        self.keybind_button.grid(column=3, row=2, pady=10, padx=10)

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


    def clicking_loop(self):
        click_times = self.random_array(self.min_click_box, self.max_click_box)
        down_times = self.random_array(self.min_down_box, self.max_down_box)
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

    def keybind_clicked(self):
        listener = keyboard.Listener(
            on_press=self.keybind_listener,
            on_release=self.keybind_release)
        listener.start()

    def keybind_listener(self, key):
        try:
            self.keybind_button['text'] = key.char
        except AttributeError:
            self.keybind_button['text'] = key

    def keybind_release(self, key):
        return False
    
    def keybind_start (self):
        listener2 = keyboard.Listener(
            on_press=self.keybind_start_listen)
        listener2.start()

    def keybind_start_listen(self, key):
        try:
            if key.char == self.keybind_button['text']:
                self.start_clicked()
        except AttributeError:
            if key == self.keybind_button['text']:
                self.start_clicked()

    
    def random_array(self, min_time, max_time):
        self.max_time = int(max_time.get())
        self.min_time = int(min_time.get())
        if self.max_time <= self.min_time:
            max_time.delete(0, tk.END)
            self.max_time = self.min_time + 1
            max_time.insert(0, str(self.max_time))

        min_down_time = int(self.min_down_box.get())/1000
        min_click_time = int(self.min_click_box.get())/1000
        duration = int(self.duration_box.get())

        self.array_length = int(duration/(min_down_time + min_click_time))

        return self.rng.integers(self.min_time, self.max_time, self.array_length)/1000



if __name__ == "__main__":
    auto = Auto()
    auto.mainloop()