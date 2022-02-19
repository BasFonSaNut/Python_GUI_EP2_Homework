import tkinter as tk
from tkinter.font import BOLD
from tkinter import messagebox
from db import Database

# Instanciate databse object
db = Database('store.db')

# Main Application/GUI class
class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('Durian Shop')
        # Width height
        master.geometry("700x450")
        # Create widgets/grid
        self.create_widgets()
        # Init selected item var
        self.selected_item = 0
        # Populate initial list
        self.price_list()

    def create_widgets(self):
        # quantity
        self.quantity_text = tk.StringVar()
        self.quantity_label = tk.Label(
            self.master, text='Quantity', font=('Angsana New',25,BOLD), pady=20)
        self.quantity_label.grid(row=0, column=0, sticky=tk.W)
        
        self.quantity_entry = tk.Entry(self.master, textvariable=self.quantity_text)
        self.quantity_entry.grid(row=0, column=1)
        
        # price per kilo
        self.priceperkilo_text = tk.StringVar()
        self.priceperkilo_label = tk.Label(
            self.master, text='Price per kilo', font=('Angsana New',25,BOLD))
        self.priceperkilo_label.grid(row=0, column=2, sticky=tk.W)
        self.priceperkilo_entry = tk.Entry(
            self.master, textvariable=self.priceperkilo_text)
        self.priceperkilo_entry.grid(row=0, column=3)
        
        # Total price 
        self.totalprice_text = tk.StringVar()
        self.totalprice_label = tk.Label(
            self.master, text='Total price', font=('Angsana New',25,BOLD))
        self.totalprice_label.grid(row=1, column=0, sticky=tk.W)
        self.totalprice_entry = tk.Entry(
            self.master, textvariable=self.totalprice_text)
        self.totalprice_entry.grid(row=1, column=1)
        

        # Parts list (listbox)
        self.parts_list = tk.Listbox(self.master, height=8, width=50, border=0)
        self.parts_list.grid(row=3, column=0, columnspan=3,
                             rowspan=6, pady=20, padx=20)
        # Create scrollbar
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(row=3, column=3)
        # Set scrollbar to parts
        self.parts_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.parts_list.yview)

        # Bind select
        self.parts_list.bind('<<ListboxSelect>>', self.select_item)

        # Buttons
        self.calculate_btn = tk.Button(
            self.master, text="Calculate price", width=12, command=self.calculate_item)
        self.calculate_btn.grid(row=2, column=0, pady=20)
        
        self.add_btn = tk.Button(
            self.master, text="Add", width=12, command=self.add_item)
        self.add_btn.grid(row=2, column=1, pady=20)

        self.remove_btn = tk.Button(
            self.master, text="Delete", width=12, command=self.remove_item)
        self.remove_btn.grid(row=2, column=2)

        self.update_btn = tk.Button(
            self.master, text="Edit", width=12, command=self.update_item)
        self.update_btn.grid(row=2, column=3)

        self.exit_btn = tk.Button(
            self.master, text="Clear Data", width=12, command=self.clear_text)
        self.exit_btn.grid(row=2, column=4)

    def price_list(self):
        # Delete items before update. So when you keep pressing it doesnt keep getting (show example by calling this twice)
        self.parts_list.delete(0, tk.END)
        # Loop through records
        for row in db.fetch():
            # Insert into list
            self.parts_list.insert(tk.END, row)

    # Add new item
    def add_item(self):
        if self.quantity_text.get() == '' or self.priceperkilo_text.get() == '' or self.totalprice_text.get() == '':
            messagebox.showerror(
                "Blank not allowed", "Please input all kilo,price per kilo, total : total price could use callculate button to calcalate")
            return
        print(self.quantity_text.get())
        # Insert into DB
        db.insert(self.quantity_text.get(), self.priceperkilo_text.get(),
                  self.totalprice_text.get())
        # Clear list
        self.parts_list.delete(0, tk.END)
        # Insert into list
        self.parts_list.insert(tk.END, (self.quantity_text.get(), self.priceperkilo_text.get(
        ), self.totalprice_text.get()))
        self.clear_text()
        self.price_list()

    # Runs when item is selected
    def select_item(self, event):
        # # Create global selected item to use in other functions
        # global self.selected_item
        try:
            # Get index
            index = self.parts_list.curselection()[0]
            # Get selected item
            self.selected_item = self.parts_list.get(index)
            # print(selected_item) # Print tuple

            # Add text to entries
            self.quantity_entry.delete(0, tk.END)
            self.quantity_entry.insert(tk.END, self.selected_item[1])
            self.priceperkilo_entry.delete(0, tk.END)
            self.priceperkilo_entry.insert(tk.END, self.selected_item[2])
            self.totalprice_entry.delete(0, tk.END)
            self.totalprice_entry.insert(tk.END, self.selected_item[3])
            
        except IndexError:
            pass
        
    # Calculate total price        
    def calculate_item(self):
        if self.quantity_text.get() == '' or self.priceperkilo_text.get() == '':
            messagebox.showerror('Not Allow Blank', 'Please input kilo and price per kilo')
            return
        quantity = self.quantity_text.get()
        priceperkilo = self.priceperkilo_text.get()
        self.totalprice_text.set(float(quantity) * float(priceperkilo))
    
    # Remove item
    def remove_item(self):
        db.remove(self.selected_item[0])
        self.clear_text()
        self.price_list()

    # Update item
    def update_item(self):
        db.update(self.selected_item[0], self.quantity_text.get(
        ), self.priceperkilo_text.get(), self.totalprice_text.get())
        self.price_list()

    # Clear all text fields
    def clear_text(self):
        self.quantity_entry.delete(0, tk.END)
        self.priceperkilo_entry.delete(0, tk.END)
        self.totalprice_entry.delete(0, tk.END)
   
root = tk.Tk()
app = Application(master=root)
app.mainloop()