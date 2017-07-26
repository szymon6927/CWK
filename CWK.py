# -*- coding: utf-8 -*-
from tkinter import *
import tkinter.ttk as ttk
import time
import datetime
import os

FONT_14 = ("Consolas", 14)
FONT_11 = ("Consolas", 11)
FONT_16 = ('Consolas', 16)
FONT_18 = ('Consolas', 18)
FONT_24 = ('Consolas', 24)
FONT_32 = ('Consolas', 32)
FONT_36 = ('Consolas', 36)
# flat, groove, raised, ridge, solid, or sunken


class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.stop_clock = False
        self.stop_function = False
        self.grid()
        self.build_menu()
        self.welcome()
        self.current_time()
        self.check_option()
        self.input_time()
        self.execute()
        self.add_logo()
        self.show_current_time()
        self.remaining = 0

    def build_menu(self):
        self.menu_bar = Menu(self)
        self.first = Menu(self.menu_bar, tearoff=0)
        self.first.add_command(label="O programie", command=self.about_program)
        self.first.add_separator()
        self.first.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="Menu", menu=self.first)
        root.config(menu=self.menu_bar)

    def about_program(self):
        about_info = Toplevel(root)
        about_info.geometry("200x200")
        info_label = Label(about_info, font=("Consolas", 10), text="Czasowy wyłącznik komputera \n"
                           "autor: Szymon Miks \n wersja: 1.0.0")
        info_label.pack(expand=1)

    def welcome(self):
        Label(self, text="Witaj w programie CWK!", font=FONT_16, bg="#2C3E50",
              fg="white").grid(row=0, column=0, columnspan=1, sticky=N, pady=(30, 5))
        Label(self, text="wybierz czas za jaki twój", font=FONT_16, bg="#2C3E50",
              fg="white").grid(row=1, column=0, columnspan=1, sticky=N)
        Label(self, text="komputer ma zostać wyłączony", font=FONT_16, bg="#2C3E50",
              fg="white").grid(row=2, column=0, columnspan=1, sticky=N, pady=(5, 30))

    def add_logo(self):
        photo = PhotoImage(file='img/logo5.png')
        label = Label(self, image=photo, background="#2C3E50")
        label.image = photo
        label.grid(row=0, rowspan=3, column=1)

    def current_time(self):
        Label(self, text="Obecna godzina to: ", font=FONT_14, bg="#2C3E50", fg="white").grid(row=3, column=0, sticky=W)
        self.hour_lbl = Label(self, text="", font=FONT_14, bg="#2C3E50", fg="white")
        self.hour_lbl.grid(row=3, column=1, sticky=W)

    def show_current_time(self):
        if not self.stop_clock:
            now = time.strftime("%H:%M:%S")
            self.hour_lbl.configure(text=now)
            self.after(1000, self.show_current_time)

    def check_option(self):
        self.option = IntVar()
        s = ttk.Style()  # Creating style element
        s.configure('Wild.TRadiobutton',    # First argument is the name of style. Needs to end with: .TRadiobutton
                    background="#2C3E50",   # Setting background to our specified color above
                    foreground="white",
                    font=FONT_11)     # You can define colors like this also
        self.first_option = ttk.Radiobutton(self, text="Wyłącz po określonym czasie",
                    variable=self.option, command=self.selection, value=1, style='Wild.TRadiobutton')
        self.first_option.grid(row=4, column=0, sticky=W)

        self.second_option = ttk.Radiobutton(self, text="Wyłącz o określonej godzinie", variable=self.option,
                                             command=self.selection, value=2, style='Wild.TRadiobutton')
        self.second_option.grid(row=5, column=0, sticky=W)

    def input_time(self):
        Label(self, text="Podaj czas za jaki twój komputer ma się wyłączyć", font=FONT_11, bg="#2C3E50",
              fg="white").grid(row=6, column=0, sticky=W)
        self.input_time = Entry(self, bd=2, bg="#2C3E50", fg="white", highlightbackground="white",
                                highlightcolor="white", highlightthickness=1)
        self.input_time.grid(row=6, column=1, padx=(2, 5), sticky=W)
        self.input_time.insert(0, 'Czas')
        self.input_time.bind('<FocusIn>', self.on_entry_click)
        self.input_time.bind('<FocusOut>', self.on_focusout)
        # self.input_time.configure(state="readonly", )

    def execute(self):
        self.stop_execute = Button(text="STOP", height=2, width=20, state=DISABLED,
                                   font=FONT_16, activebackground='#91999C', activeforeground='white',
                                   relief='solid', bd=3, background="#E74C3C", fg="white", command=self.enable_widgets)
        self.stop_execute.grid(row=9, column=0, sticky=W, pady=(15, 5), padx=(2, 5))

        self.execute = Button(text="Wykonaj", state=DISABLED, height=2, background="#ECF0F1",
                              activebackground='#91999C', activeforeground='white', width=20, font=FONT_16,
                              relief='solid', bd=3, command=self.turn_off)
        self.execute.grid(row=9, column=0, sticky=E, pady=(15, 5), padx=(2, 5))

    def disable_widgets(self):
        self.execute.configure(state=DISABLED)
        self.input_time.configure(state=DISABLED)
        self.first_option.configure(state=DISABLED)
        self.second_option.configure(state=DISABLED)

    def enable_widgets(self):
        if self.counter:
            self.stop_function = True
            self.execute.configure(state="normal")
            self.input_time.configure(state="normal")
            self.first_option.configure(state="normal")
            self.second_option.configure(state="normal")
            self.counter.configure(text="00:00:00")

    def count_down(self, remaining=None):
        self.stop = True
        if not self.stop_function:
            self.disable_widgets()
            self.info_text = Label(self, text="Do wyłączenia pozostało: ", font=FONT_16, bg="#2C3E50", fg="white")
            self.info_text.grid(row=7, rowspan=2, column=0, sticky=W)
            self.counter = Label(self, text="", font=FONT_24, width=10, bg="#E74C3C", fg='#FFF', relief='solid', bd=3)
            self.counter.grid(row=7, rowspan=2, column=1, sticky=E, pady=(5, 5), padx=(2, 5))
            if remaining is not None:
                self.remaining = remaining

            if self.remaining <= 0:
                self.counter.configure(text="time's up!")
                os.system("shutdown -s")
            else:
                data = str(datetime.timedelta(seconds=self.remaining))
                self.counter.configure(text="%s" % data)
                self.remaining = self.remaining - 1
                self.after(1000, self.count_down)

    def on_entry_click(self, event):
        input_content = self.input_time.get()
        if input_content == "Tylko minuty" or input_content == "Format godz:min":
            self.input_time.delete(0, "end")  # delete all the text in the entry
            self.input_time.insert(0, '')  # Insert blank for user input
            self.execute.config(state="normal", bg="#2980B9", fg="white")

    def on_focusout(self, event):
        if self.input_time.get() == "":
            self.input_time.insert(0, "Czas")

    def selection(self):
        choise = self.option.get()
        if choise == 1:
            print("wybor 1")
            self.input_time.configure(state="normal")
            self.input_time.delete(0, "end")
            self.input_time.insert(0, "Tylko minuty")
        elif choise == 2:
            print("wybor 2")
            self.input_time.configure(state="normal")
            self.input_time.delete(0, "end")
            self.input_time.insert(0, "Format godz:min")
        return choise

    def turn_off(self):
        choice = self.option.get()
        if choice == 1:
            minutes = self.input_time.get()
            shutdown = int(minutes) * 60
            print(shutdown)
            print("shutdown -s -t ", shutdown)
            self.stop_function = False
            self.stop_execute.configure(state="normal")
            self.count_down(shutdown)
        elif choice == 2:
            input_time = self.input_time.get()
            now = time.strftime("%H:%M")
            start_dt = datetime.datetime.strptime(now, '%H:%M')
            end_dt = datetime.datetime.strptime(input_time, '%H:%M')
            diff = (end_dt - start_dt)
            shutdown = diff.seconds
            int_shutdown = int(shutdown)
            self.stop_function = False
            self.stop_execute.configure(state="normal")
            self.count_down(int_shutdown)


if __name__ == '__main__':
    root = Tk()
    root.title("Czasowy wyłącznik komputera")
    root.iconbitmap(default='img/time4.ico')
    root.config(bg="#2C3E50")
    # root.geometry("650x400")
    app = Application(root)
    app.configure(background='#2C3E50')
    root.mainloop()
