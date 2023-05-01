import customtkinter
import numpy as np
from PL9 import optimize_transportation

customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, num_factories, num_depots, num_clients, **kwargs):
        super().__init__(master, **kwargs)
        self.offers = []
        self.entries = []
        self.row_entries =[]

        # Add row header
        header = customtkinter.CTkLabel(self, text="Offers")
        header.grid(row=1, column=0, padx=5, pady=5)

        # Add column headers
        for j in range(num_factories):
            header = customtkinter.CTkLabel(self, text=f"Factory {j + 1}")
            header.grid(row=0, column=j + 1, padx=5, pady=5)

        entries = []

        # Create table entries
        for j in range(num_factories):
            entry = customtkinter.CTkEntry(self, width=50)
            entry.grid(row=1, column=j + 1, padx=5, pady=5)
            entries.append(entry)
        self.entries.append(entries)
        
        # Add row header
        header = customtkinter.CTkLabel(self, text="from/to")
        header.grid(row=2, column=0, padx=5, pady=5)

        # Add column headers
        for j in range(num_depots):
            header = customtkinter.CTkLabel(self, text=f"Depot {j + 1}")
            header.grid(row=2, column=j + 1, padx=5, pady=5)

        # Add row headers and create table entries
        for i in range(num_factories):
            header = customtkinter.CTkLabel(self, text=f"Factory {i + 1}")
            header.grid(row=i + 3, column=0, padx=5, pady=5)

            entries = []
            for j in range(num_depots):
                entry = customtkinter.CTkEntry(self, width=50)
                entry.grid(row=i + 3, column=j + 1, padx=5, pady=5)
                entries.append(entry)
            self.entries.append(entries)

        # Add row header
        header = customtkinter.CTkLabel(self, text="from/to")
        header.grid(row=num_factories + 3, column=0, padx=5, pady=5)

        # Add column headers
        for j in range(num_clients):
            header = customtkinter.CTkLabel(self, text=f"Client {j + 1}")
            header.grid(row=num_factories + 3, column=j + 1, padx=5, pady=5)

        # Add row headers and create table entries
        for i in range(num_depots):
            header = customtkinter.CTkLabel(self, text=f"Depot {i + 1}")
            header.grid(row=i + num_factories+ 4, column=0, padx=5, pady=5)

            row_entries = []
            for j in range(num_clients):
                entry = customtkinter.CTkEntry(self, width=50)
                entry.grid(row=i + num_factories + 4, column=j + 1, padx=5, pady=5)
                row_entries.append(entry)
            self.entries.append(row_entries)
        # Add row header
        header = customtkinter.CTkLabel(self, text="Quantity required")
        header.grid(row=num_depots + num_factories + 5, column=0, padx=5, pady=5)

        # Add column headers
        for j in range(num_clients):
            header = customtkinter.CTkLabel(self, text=f"Client {j + 1}")
            header.grid(row=num_depots + num_factories + 4, column=j + 1, padx=5, pady=5)

        # Create table entries
        row_entries = []
        for j in range(num_clients):
            entry = customtkinter.CTkEntry(self, width=50)
            entry.grid(row=num_depots + num_factories + 5, column=j + 1, padx=5, pady=5)
            row_entries.append(entry)
        self.entries.append(row_entries)

        # Add row header
        header = customtkinter.CTkLabel(self, text="Fixed cost")
        header.grid(row=num_depots + num_factories + 7, column=0, padx=5, pady=5)

        # Add column headers for factories
        for j in range(num_factories):
            header = customtkinter.CTkLabel(self, text=f"Factory {j + 1}")
            header.grid(row=6+num_depots + num_factories, column=j + 1, padx=5, pady=5)

        # Add column headers for depots
        for j in range(num_depots):
            header = customtkinter.CTkLabel(self, text=f"Depot {j + 1}")
            header.grid(row=6+num_depots + num_factories, column=num_factories + j + 1, padx=5, pady=5)

        # Create table entries
        row_entries = []
        for j in range(num_factories + num_depots):
            entry = customtkinter.CTkEntry(self, width=50)
            entry.grid(row=num_depots + num_factories+7, column=j + 1, padx=5, pady=5)
            row_entries.append(entry)
        self.entries.append(row_entries)




class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.my_frame = None

        self.title = customtkinter.CTkLabel(master=self, text="Factory, Warehouse Location and Logistics Planning", font=('Arial', 25), justify="left")
        self.title.place(x=20, y=20)

        self.descp = customtkinter.CTkLabel(master=self, text="A canned goods producer aims to optimize their supply chain by determining ideal factory and warehouse locations. To make the best decision, they should develop a system that considers production capacities, transportation costs, customer requirements, and fixed annual costs, ultimately improving efficiency and reducing overall expenses.",
                                            font=('Arial', 14), wraplength=650, justify="left")
        self.descp.place(x=20, y=70)

        self.title2 = customtkinter.CTkLabel(master=self, text="Add your variables and constraints", font=('Arial', 30), justify="left")
        self.title2.place(x=20, y=150)

        self.num_factories_label = customtkinter.CTkLabel(master=self, text="Number of factories: ", font=('Arial', 16), justify="left")
        self.num_factories_label.place(x=20, y=190)

        self.num_depots_label = customtkinter.CTkLabel(master=self, text="Number of depots: ", font=('Arial', 16), justify="left")
        self.num_depots_label.place(x=20, y=230)

        self.num_clients_label = customtkinter.CTkLabel(master=self, text="Number of clients: ", font=('Arial', 16), justify="left")
        self.num_clients_label.place(x=20, y=270)

        self.num_factories = customtkinter.CTkEntry(master=self, width=40)
        self.num_factories.place(x=180, y=190)

        self.num_depots= customtkinter.CTkEntry(master=self, width=40)
        self.num_depots.place(x=180, y=230)

        self.num_clients = customtkinter.CTkEntry(master=self, width=40)
        self.num_clients.place(x=180, y=270)

        self.continue_button = customtkinter.CTkButton(master=self, text="continue", command=lambda: self.create_entries(), width=65,fg_color="#FFCB42")
        self.continue_button.place(x=250, y=230)


    def button_event(self, my_frame):
        offers = []
        production_transport_costs = []
        transport_client_costs = []
        quantity_required = []
        fixed_costs = []

        # Get offers
        for entry in my_frame.entries[0]:
            offers.append(int(entry.get()))

        # Get production_transport_costs
        for row_entries in my_frame.entries[1:1 + int(self.num_factories.get())]:
            row_costs = []
            for entry in row_entries:
                row_costs.append(int(entry.get()))
            production_transport_costs.append(row_costs)
        production_transport_costs=production_transport_costs[0:int(self.num_factories.get())]

        # Get transport_client_costs
        for row_entries in my_frame.entries[1 + int(self.num_factories.get()):1 + int(self.num_factories.get()) + int(self.num_depots.get())]:
            row_costs = []
            for entry in row_entries:
                row_costs.append(int(entry.get()))
            transport_client_costs.append(row_costs)
        transport_client_costs=transport_client_costs[0:int(self.num_depots.get())]

        # Get quantity_required
        for entry in my_frame.entries[-2]:
            quantity_required.append(int(entry.get()))

        # Get fixed_costs
        for entry in my_frame.entries[-1]:
            fixed_costs.append(int(entry.get()))
        result=optimize_transportation(offers, production_transport_costs, transport_client_costs, quantity_required, fixed_costs)
        

        print(result)
        
        self.scrollable_frame2 = customtkinter.CTkScrollableFrame(self, width=655, height=10)
        self.scrollable_frame2.place(x=20, y=510)

        self.result_label = customtkinter.CTkLabel(master=self.scrollable_frame2, text=result, font=('Arial', 16), justify="left",wraplength=650)
        self.result_label.pack(padx=10, pady=10)



    def create_entries(self):
        try:
            num_factories = int(self.num_factories.get())
            num_depots = int(self.num_depots.get())
            num_clients = int(self.num_clients.get())

        except ValueError:
            print("Invalid input")
            return

        if self.my_frame:
            self.my_frame.destroy()

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, width=655, height=150)
        self.scrollable_frame.place(x=20, y=310)

        self.my_frame = MyFrame(self.scrollable_frame, num_factories, num_depots, num_clients)
        self.my_frame.pack()

        self.scrollable_frame.update_idletasks()
        my_frame_y = self.scrollable_frame.winfo_y()

        self.opt_button = customtkinter.CTkButton(master=self, text="optimize", command=lambda: self.button_event(self.my_frame), width=65,fg_color="#FFCB42")
        self.opt_button.place(x=250, y=480 + 70)



app = App()
app.geometry("700x750")
app.mainloop()
