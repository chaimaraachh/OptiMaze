import subprocess
import tkinter
import matplotlib
import numpy as np


from PL2  import pertrolium_solver
from PL4 import chaussetous_solver
from PL7 import optimize_assignment
from PL9 import optimize_transportation



matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.figure as fig
import customtkinter
import os
from PIL import Image
#from optimazeTools.PL3 import optimize_staffing

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("custom")  # Themes: "blue" (standard), "green", "dark-blue"
class MyFramePL2(customtkinter.CTkFrame):
     def __init__(self, master, n, **kwargs):
        super().__init__(master, **kwargs)
        
        self.quantities=[]
        self.qualities=[]
        self.prices = []
        self.marketing_costs = []
        
        for i in range(n):
                entry_label = customtkinter.CTkLabel(self, text=f"Quantity - type {i+1}: ")
                entry_label.grid(row=i, column=0, padx=2, pady=2)
                

                entry1 = customtkinter.CTkEntry(self,width=40)
                entry1.grid(row=i, column=1, padx=2, pady=2)
                
                
                entry_label = customtkinter.CTkLabel(self, text=f"Quality level - type {i+1}: ")
                entry_label.grid(row=i, column=2, padx=2, pady=2)

                entry2 = customtkinter.CTkEntry(self,width=40)
                entry2.grid(row=i, column=3, padx=2, pady=2)     
                
                
                entry_label = customtkinter.CTkLabel(self, text=f"Baril price {i+1}: ")
                entry_label.grid(row=i, column=4, padx=2, pady=2)

                entry3 = customtkinter.CTkEntry(self,width=40)
                entry3.grid(row=i, column=5, padx=2, pady=2)
                

                entry_label = customtkinter.CTkLabel(self, text=f"Marketing costs - type {i+1}: ")
                entry_label.grid(row=i, column=6, padx=2, pady=2)

                entry4 = customtkinter.CTkEntry(self,width=40)
                entry4.grid(row=i, column=7, padx=2, pady=2)
                
                

                self.quantities.append(entry1)
                self.qualities.append(entry2)
                self.prices.append(entry3)
                self.marketing_costs.append(entry4)

        entry_label = customtkinter.CTkLabel(self, text="Minimal requiered quality:")
        entry_label.grid(row=i+1, column=3, padx=5, pady=5)
        self.Qmin = customtkinter.CTkEntry(self)
        self.Qmin.grid(row=i+1, column=4, padx=5, pady=5)
     def get_inputs(self):
         quantities = [int(x.get()) for x in self.quantities]
         qualities = [int(x.get()) for x in self.qualities]
         prices = [float(x.get()) for x in self.prices]
         marketing_costs = [float(x.get()) for x in self.marketing_costs]
         Qmin = int(self.Qmin.get())
         return quantities, qualities, prices, marketing_costs, Qmin



class MyFramePL4(customtkinter.CTkFrame):
    def __init__(self, master, num_months, **kwargs):
        super().__init__(master, **kwargs)

        self.stock = []
        self.demand = []

        for i in range(num_months):
            entry_label = customtkinter.CTkLabel(self, text=f"storage costs {i+1}:", fg_color= "transparent",bg_color="transparent")
            entry_label.grid(row=i, column=0, padx=5, pady=5)

            entry = customtkinter.CTkEntry(self,fg_color= "transparent",bg_color="transparent")
            entry.grid(row=i, column=1, padx=5, pady=5)
            
            entry_label = customtkinter.CTkLabel(self, text=f"demand {i+1}:",fg_color= "transparent",bg_color="transparent")
            entry_label.grid(row=i, column=2, padx=5, pady=5)

            entry2 = customtkinter.CTkEntry(self,fg_color= "transparent",bg_color="transparent")
            entry2.grid(row=i, column=3, padx=5, pady=5)

            self.stock.append(entry)
            self.demand.append(entry2)
        entry_label = customtkinter.CTkLabel(self, text="initial stock:",fg_color= "transparent",bg_color="transparent")
        entry_label.grid(row=i+1, column=0, padx=5, pady=5)
        self.initial_stock = customtkinter.CTkEntry(self,fg_color= "transparent",bg_color="transparent")
        self.initial_stock.grid(row=i+1, column=1, padx=5, pady=5)

        entry_label = customtkinter.CTkLabel(self, text="initial workers:",fg_color= "transparent",bg_color="transparent")
        entry_label.grid(row=i+1, column=2, padx=5, pady=5)
        self.initial_workers = customtkinter.CTkEntry(self,fg_color= "transparent",bg_color="transparent")
        self.initial_workers.grid(row=i+1, column=3, padx=5, pady=5)

        entry_label = customtkinter.CTkLabel(self, text="worker salary:",fg_color= "transparent",bg_color="transparent")
        entry_label.grid(row=i+2, column=0, padx=5, pady=5)
        self.worker_salary = customtkinter.CTkEntry(self,fg_color= "transparent",bg_color="transparent")
        self.worker_salary.grid(row=i+2, column=1, padx=5, pady=5)

        entry_label = customtkinter.CTkLabel(self, text="max overtime:",fg_color= "transparent",bg_color="transparent")
        entry_label.grid(row=i+2, column=2, padx=5, pady=5)
        self.max_overtime = customtkinter.CTkEntry(self,fg_color= "transparent",bg_color="transparent")
        self.max_overtime.grid(row=i+2, column=3, padx=5, pady=5)

        entry_label = customtkinter.CTkLabel(self, text="overtime pay:",fg_color= "transparent",bg_color="transparent")
        entry_label.grid(row=i+3, column=0, padx=5, pady=5)
        self.overtime_pay = customtkinter.CTkEntry(self,fg_color= "transparent",bg_color="transparent")
        self.overtime_pay.grid(row=i+3, column=1, padx=5, pady=5)

        entry_label = customtkinter.CTkLabel(self, text="hours per shoe:",fg_color= "transparent",bg_color="transparent")
        entry_label.grid(row=i+3, column=2, padx=5, pady=5)
        self.hours_per_shoe = customtkinter.CTkEntry(self,fg_color= "transparent",bg_color="transparent")
        self.hours_per_shoe.grid(row=i+3, column=3, padx=5, pady=5)

        entry_label = customtkinter.CTkLabel(self, text="material cost:",fg_color= "transparent",bg_color="transparent")
        entry_label.grid(row=i+4, column=0, padx=5, pady=5)
        self.material_cost = customtkinter.CTkEntry(self,fg_color= "transparent",bg_color="transparent")
        self.material_cost.grid(row=i+4, column=1, padx=5, pady=5)

        entry_label = customtkinter.CTkLabel(self, text="recruitment cost:",fg_color= "transparent",bg_color="transparent")
        entry_label.grid(row=i+4, column=2, padx=5, pady=5)
        self.recruitment_cost = customtkinter.CTkEntry(self,fg_color= "transparent",bg_color="transparent")
        self.recruitment_cost.grid(row=i+4, column=3, padx=5, pady=5)

        entry_label = customtkinter.CTkLabel(self, text="layoff cost:",fg_color= "transparent",bg_color="transparent")
        entry_label.grid(row=i+5, column=0, padx=5, pady=5)
        self.layoff_cost = customtkinter.CTkEntry(self,fg_color= "transparent",bg_color="transparent")
        self.layoff_cost.grid(row=i+5, column=1, padx=5, pady=5)

    def get_input_array(self):
        demand = [int(x.get()) for x in self.demand]
        initial_stock = int(self.initial_stock.get())
        initial_workers = int(self.initial_workers.get())
        worker_salary = int(self.worker_salary.get())
        max_overtime = int(self.max_overtime.get())
        overtime_pay = int(self.overtime_pay.get())
        hours_per_shoe = int(self.hours_per_shoe.get())
        material_cost = int(self.material_cost.get())
        recruitment_cost = int(self.recruitment_cost.get())
        layoff_cost = int(self.layoff_cost.get())
        storage_costs = [int(x.get()) for x in self.stock]

        return demand, initial_stock, initial_workers, worker_salary, max_overtime, overtime_pay, hours_per_shoe, material_cost, recruitment_cost, layoff_cost, storage_costs

class MyFramePL7(customtkinter.CTkFrame):
    def __init__(self, master, num_companies, num_projects, **kwargs):
        super().__init__(master, **kwargs)
        self.entries = []

        # Add column headers
        for j in range(num_projects):
            header = customtkinter.CTkLabel(self, text=f"Proj{j+1}")
            header.grid(row=0, column=j+1, padx=5, pady=5)

        # Add row headers
        for i in range(num_companies):
            header = customtkinter.CTkLabel(self, text=f"Company {i+1}")
            header.grid(row=i+1, column=0, padx=5, pady=5)

        # Create table entries
        for i in range(num_companies):
            row_entries = []
            for j in range(num_projects):
                entry = customtkinter.CTkEntry(self, width=50)
                entry.grid(row=i+1, column=j+1, padx=5, pady=5)
                row_entries.append(entry)
            self.entries.append(row_entries)
    def get_costs_array(self):
        costs = []
        for i in range(len(self.entries)):
            row_costs = []
            for j in range(len(self.entries[i])):
                try:
                    value = int(self.entries[i][j].get())
                except ValueError:
                    value = np.nan
                row_costs.append(value)
            costs.append(row_costs)
        return np.array(costs)

class MyFramePL9(customtkinter.CTkFrame):
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


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("700x600")

        figure = fig.Figure()
        ax1 = figure.add_subplot(111)
        canvas = FigureCanvasTkAgg(figure, master=self)
        canvas.get_tk_widget().grid()
        canvas.draw()


def command(check_var, entry):
    if check_var == 1:
        entry.configure(state="normal")
        print("normal")
    else:
        entry.configure(state="disabled")
        print("disabled")


class CheckBoxFrame(customtkinter.CTkFrame):
    def __init__(self, master, item_list, **kwargs):
        super().__init__(master, **kwargs, fg_color="transparent")

        self.checkbox_list = []
        self.entry_list = []
        self.daily_req = []
        for i, item in enumerate(item_list):
            self.add_item(item)

        self.label = customtkinter.CTkLabel(master=self,
                                            text="Number of consecutive work days", fg_color="#FFCF55",
                                            corner_radius=30)
        self.label.grid(row=0, column=0, columnspan=2, pady=10, ipadx=10, ipady=5)
        self.nbr_work_entry = customtkinter.CTkEntry(master=self)
        self.nbr_work_entry.grid(row=0, column=2, pady=10)

    def add_item(self, item):
        checkbox = customtkinter.CTkCheckBox(self, text=item)
        checkbox.grid(row=len(self.checkbox_list) + 1, column=0, pady=5, padx=20)
        self.checkbox_list.append(checkbox)
        label = customtkinter.CTkLabel(self, text="Min Daily Number Of Employees")
        label.grid(row=len(self.checkbox_list), column=1, padx=5, pady=5)
        entry = customtkinter.CTkEntry(self, state="disabled", fg_color="#EDEFF8")
        entry.grid(row=len(self.checkbox_list), column=2, padx=5, pady=5)
        self.entry_list.append(entry)
        checkbox.configure(command=lambda: self.command(checkbox))
        if entry.get().isnumeric():
            self.daily_req.append(int(entry.get()))

    def command(self, checkbox):
        index = self.checkbox_list.index(checkbox)
        if checkbox.get() == 1:
            self.entry_list[index].configure(state="normal", fg_color="#FFFFFF")
            print("normal")
        else:
            self.entry_list[index].configure(state="disabled", fg_color="#EDEFF8")
            print("disabled")

    def remove_item(self, item):
        for checkbox in self.checkbox_list:
            if item == checkbox.cget("text"):
                checkbox.destroy()
                self.checkbox_list.remove(checkbox)
                return

    def get_checked_items(self):
        return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1], [int(entry.get()) for
                                                                                                   entry in
                                                                                                   self.entry_list if
                                                                                                   entry.get() != "" and entry.get().isnumeric()], int(
            self.nbr_work_entry.get())


class Cards(customtkinter.CTkFrame):
    def __init__(self, master, row, column, command, icon, text, **kwargs):
        super().__init__(master, corner_radius=20, fg_color="#FFFFFF",
                         border_color="#EDEFF8", border_width=4, **kwargs)
        self.grid(row=row, column=column, sticky="nsew", ipadx=5, ipady=5)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((1, 3), weight=1)
        self.grid_rowconfigure(4, minsize=10)
        self.grid_rowconfigure(0, minsize=10)
        self.grid_rowconfigure(2, minsize=10)

        self.label = customtkinter.CTkLabel(master=self, text=text,
                                            image=icon, compound='top', fg_color="transparent", bg_color="transparent",
                                            corner_radius=20, anchor="center",
                                            font=("Roboto Medium", -14))
        self.label.grid(row=1, column=1, sticky="nsew", padx=7)
        self.button = customtkinter.CTkButton(master=self, corner_radius=30, fg_color="#FFCB42",
                                              text="Solve",
                                              text_color="black", hover_color="#FFB200",
                                              bg_color="transparent",
                                              command=command)
        self.button.grid(row=3, column=1, padx=10)

        # self.bind("<Button-1>", self.on_hover)

    # def on_hover(self):
    #    self.configure(border_color="#FFB200")


class IntroFrame(customtkinter.CTkFrame):
    def __init__(self, master, row, column, title, icon, text, command, **kwargs):
        super().__init__(master, corner_radius=20, fg_color="#FFFFFF",
                         border_color="#EDEFF8", border_width=4, **kwargs)
        self.grid_rowconfigure((1), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid(row=row, column=column, ipady=10, padx=30, pady=10, ipadx=10)

        self.title = customtkinter.CTkLabel(master=self, corner_radius=20,
                                            fg_color="transparent",
                                            text=title,
                                            font=customtkinter.CTkFont(size=20, weight="bold"),
                                            image=icon,
                                            compound="left"
                                            )
        self.title.grid(row=1, column=0, pady=20, sticky="nsew", padx=20)

        self.discription = customtkinter.CTkLabel(master=self, corner_radius=20,
                                                  fg_color="transparent", bg_color="transparent",
                                                  text=text,
                                                  font=("Roboto Medium", -20),
                                                  )
        self.discription.grid(row=2, column=0, padx=10, pady=10, sticky="nsew", ipadx=10, ipady=10)
        self.button = customtkinter.CTkButton(master=self, corner_radius=30, fg_color="#FFCB42",
                                              text="Start",
                                              text_color="black", hover_color="#FFB200",
                                              bg_color="transparent",
                                              command=command)
        self.button.grid(row=3, column=0, padx=10, pady=20)

    def grid_remove(self):
        super().grid_remove()

    def grid_appear(self):
        super().grid()


class App(customtkinter.CTk):
    WIDTH = 1300
    HEIGHT = 700

    def __init__(self):
        super().__init__()
        self.switch_var = customtkinter.StringVar()

        self.title("OptiMaze Solver")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
        self.iconbitmap(os.path.join(image_path, "optimization.ico"))

        # ============ Load images =============

        self.shoes_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, "3d-shoes.png")), size=(54, 54))
        self.agriculture_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, "agriculture.png")),
                                                      size=(54, 54))
        self.company_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, "company.png")), size=(54, 54))
        self.distribution_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, "distribution.png")),
                                                       size=(54, 54))
        self.eco_house_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, "eco-house.png")),
                                                    size=(54, 54))
        self.networking_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, "networking.png")),
                                                     size=(54, 54))
        self.oil_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, "oil.png")), size=(54, 54))
        self.pin_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, "pin.png")), size=(54, 54))
        self.road_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, "road.png")), size=(54, 54))

        # ======================== TopLevel window ================

        self.toplevel_window = None
        self.my_framePL2 = None
        self.my_framePL4 = None
        self.my_framePL7 = None
        self.my_framePL9 = None
        # ============ create main frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0,
                                                 fg_color="#EDEFF8")
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self, fg_color="#F9FAFF")
        self.frame_right.grid(row=0, column=1, sticky="nswe")

        self.frame_PL_intro = customtkinter.CTkFrame(master=self, fg_color="#F9FAFF")
        self.frame_PL_intro.grid(row=0, column=1, sticky="nswe")
        self.frame_PL_intro.grid_remove()

        self.pl2_solve_frame = customtkinter.CTkFrame(master=self, fg_color="#F9FAFF")
        self.pl2_solve_frame.grid(row=0, column=1, sticky="nswe", pady=(0, 10))
        self.pl2_solve_frame.grid_remove()


        self.pl3_solve_frame = customtkinter.CTkFrame(master=self, fg_color="#F9FAFF")
        self.pl3_solve_frame.grid(row=0, column=1, sticky="nswe", pady=(0, 10))
        self.pl3_solve_frame.grid_remove()

        self.pl4_solve_frame = customtkinter.CTkFrame(master=self, fg_color="#F9FAFF")
        self.pl4_solve_frame.grid(row=0, column=1, sticky="nswe", pady=(0, 10))
        self.pl4_solve_frame.grid_remove()

        self.pl6_solve_frame = customtkinter.CTkFrame(master=self, fg_color="#F9FAFF")
        self.pl6_solve_frame.grid(row=0, column=1, sticky="nswe", pady=(0, 10))
        self.pl6_solve_frame.grid_remove()

        self.pl7_solve_frame = customtkinter.CTkFrame(master=self, fg_color="#F9FAFF")
        self.pl7_solve_frame.grid(row=0, column=1, sticky="nswe", pady=(0, 10))
        self.pl7_solve_frame.grid_remove()

        self.pl9_solve_frame = customtkinter.CTkFrame(master=self, fg_color="#F9FAFF")
        self.pl9_solve_frame.grid(row=0, column=1, sticky="nswe", pady=(0, 10))
        self.pl9_solve_frame.grid_remove()

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label = customtkinter.CTkLabel(master=self.frame_left, text="OptiMaze Solver",
                                            fg_color="transparent", bg_color="transparent",
                                            font=("Roboto Medium", -17)
                                            )
        self.label.grid(row=1, column=0)

        self.home_button = customtkinter.CTkButton(master=self.frame_left,
                                                   text="Home",
                                                   font=("Roboto Medium", -14),
                                                   corner_radius=40,
                                                   fg_color="#3E89C7",
                                                   command=self.go_to_home)
        self.home_button.grid(row=2, column=0, pady=10, padx=20)

        self.about_button = customtkinter.CTkButton(master=self.frame_left,
                                                    text="About",
                                                    font=("Roboto Medium", -14),
                                                    corner_radius=40
                                                    )
        self.about_button.grid(row=3, column=0, pady=10, padx=20)

        self.help_button = customtkinter.CTkButton(master=self.frame_left,
                                                   text="Help",
                                                   font=("Roboto Medium", -14),
                                                   corner_radius=40
                                                   )
        self.help_button.grid(row=4, column=0, pady=10, padx=20)

        # ============ frame_right ============

        # configure grid layout (1x2)
        self.frame_right.rowconfigure(2, weight=1)
        self.frame_right.columnconfigure(0, weight=1)
        self.frame_right.grid_rowconfigure(0, minsize=10)

        self.home_label = customtkinter.CTkLabel(master=self.frame_right, corner_radius=20,
                                                 fg_color="transparent",
                                                 text="Choose A Linear Programming Challenge And Get Started ",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))

        self.home_label.grid(row=1, column=0, pady=20, padx=40, sticky="nsew")

        self.frame_cards = customtkinter.CTkFrame(master=self.frame_right, fg_color="transparent")

        self.frame_cards.grid(row=2, column=0, pady=20, padx=20, sticky="nsew")
        self.frame_cards.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
        self.frame_cards.grid_rowconfigure(2, minsize=10)  # empty row as spacing
        self.frame_cards.grid_rowconfigure(4, minsize=10)  # empty row as spacing
        self.frame_cards.grid_rowconfigure(6, minsize=10)  # empty row as spacing

        self.frame_cards.grid_columnconfigure(0, minsize=10)  # empty row with minsize as spacing
        self.frame_cards.grid_columnconfigure(2, minsize=10)  # empty row as spacing
        self.frame_cards.grid_columnconfigure(4, minsize=10)  # empty row as spacing
        self.frame_cards.grid_columnconfigure(6, minsize=10)  # empty row as spacing

        # ============ frame_cards ============

        # configure grid layout
        self.frame_cards.rowconfigure((1, 3, 5), weight=1)
        self.frame_cards.columnconfigure((1, 3, 5), weight=1)

        self.card1 = Cards(self.frame_cards, 1, 1, None, self.agriculture_img,
                           "\nPL1: Agricultural Zone Management")
        self.card2 = Cards(self.frame_cards, 1, 3, self.pl2_intro, self.oil_img, "\nPL2: Blending in oil production")
        self.card3 = Cards(self.frame_cards, 1, 5, self.pl3_intro, self.networking_img,
                           "\nPL3: Human resource planning")
        self.card4 = Cards(self.frame_cards, 3, 1, self.pl4_intro, self.shoes_img, "\nPL4: Production management")
        self.card5 = Cards(self.frame_cards, 3, 3, None, self.eco_house_img, "\nPL5: Electricity production")
        self.card6 = Cards(self.frame_cards, 3, 5, self.pl6_intro, self.distribution_img,
                           "\n PL6: Product distribution")
        self.card7 = Cards(self.frame_cards, 5, 1, self.pl7_intro, self.company_img, "\nPL7: Optimal allocation of resources")
        self.card8 = Cards(self.frame_cards, 5, 3, None, self.road_img, "\nPL8: Equipment replacement")
        self.card9 = Cards(self.frame_cards, 5, 5, self.pl9_intro, self.pin_img, "\nPL9: Factories and depots location\n& "
                                                                       "logistics planning")

        # ============ frame_PL_introduction ============
        self.frame_PL_intro.grid_columnconfigure(0, weight=1)
        self.frame_PL_intro.grid_rowconfigure(0, weight=1)

        self.intro_PL2 = IntroFrame(self.frame_PL_intro, 0, 0, "  PL2: Optimizing Oil Blend Composition", self.oil_img,
                                    "Welcome to the Oil Blending Tool! This tool was  "
                                    "designed to assist oil \n companies in optimizing their "
                                    " oil production by selecting the types of oil to \n  "
                                    "blend in order to maximize their revenue. With this "
                                    " interface, \n you can select the number of oil types you want to include in your mix,  "
                                    "specify the quantity, quality, \n and price of each type. ", self.pl2_start)


        self.intro_PL3 = IntroFrame(self.frame_PL_intro, 0, 0, "  PL3: Human resource planning", self.networking_img,
                                    "Welcome To Human Resource Planning.\n\n A post office needs staff for a number of "
                                    "days a week based on the minimun daily requirement.\nWe will attempt to "
                                    "determine the planning to "
                                    "meet the needs of the office using the minimum \nnumber of employees knowing that "
                                    "each employee must work for a defined number of consecutive\n days before taking a "
                                    "leave off.", self.pl3_start)

        self.intro_PL6 = IntroFrame(self.frame_PL_intro, 0, 0, "  PL6: Product distribution", self.distribution_img,
                                    "A company produces canned tomatoes in several "
                                    "factories with an annual production capacity. \nIt has "
                                    "a number of clients with annual demands. The "
                                    "company also has a number of depots\n through which "
                                    "goods can pass. Production costs are the same for all "
                                    "factories. The possibility of\n transport from one "
                                    "place to another varies depending on the location. We "
                                    "will attempt to map out the\n company's logistics model "
                                    "as well as determine the optimal transportation and "
                                    "transhipment policy. ", self.pl6_start)

        self.intro_PL4 = IntroFrame(self.frame_PL_intro, 0, 0, "  PL4: Production Management", self.shoes_img,
                                    "A company must meet varying product demands over  "
                                    "several months, with an initial stock \n and workforce. "
                                    " Workers have a fixed salary, work a certain number "
                                    " of hours, and can work overtime at \n an additional "
                                    "rate. Producing a product unit requires labor and  "
                                    "raw materials, and there are  \n costs for recruitment, "
                                    "layoffs, and storage. The goal is to determine the  "
                                    "optimal production plan and \n worker management policy "
                                    "as well as determine the \n optimal transportation and "
                                    " to minimize costs while meeting monthly demands.", self.pl4_start)

        self.intro_PL7 = IntroFrame(self.frame_PL_intro, 0, 0, "  PL7: Optimal Resource Allocation", self.company_img,
                                    "A client has issued a call for proposals for a   "
                                    "certain number of projects.  \n   Multiple companies have"
                                    " submitted bids according to a given table.\n "
                                    " The goal is to determine the optimal allocation that allows"
                                    " completing all projects at \n a minimum cost, while   "
                                    "considering that: \n  Any company without  a bid for a  "
                                    "project cannot be selected for that project Exactly  "
                                    " \n one company is selected for each project.\n A company  "
                                    "cannot undertake more than a specified number of projects."
                                   , self.pl7_start)

        self.intro_PL9 = IntroFrame(self.frame_PL_intro, 0, 0, "  PL9: Factory, Warehouse Location and Logistics Planning", self.pin_img,
                                    "A canned goods producer aims to optimize their "
                                    "supply chain by determining ideal \n factory and "
                                    "warehouse locations. To make the best decision, \n they "
                                    "  should develop a system that considers production"
                                    " capacities,\n  transportation costs, customer  "
                                    "requirements, and fixed annual costs, ultimately \n  "
                                    "improving efficiency and reducing overall expenses.  "

                                   , self.pl9_start)

        # ========== functions =============

    # =============== PL Introductions =================

    def pl2_intro(self):
        self.hide_all_frames()
        self.frame_PL_intro.grid()
        self.intro_PL2.grid_appear()


    def pl3_intro(self):
        self.hide_all_frames()
        self.frame_PL_intro.grid()
        self.intro_PL3.grid_appear()

    def pl4_intro(self):
        self.hide_all_frames()
        self.frame_PL_intro.grid()
        self.intro_PL4.grid_appear()

        
    def pl6_intro(self):
        self.hide_all_frames()
        self.frame_PL_intro.grid()
        self.intro_PL6.grid_appear()

        
    def pl7_intro(self):
        self.hide_all_frames()
        self.frame_PL_intro.grid()
        self.intro_PL7.grid_appear()

    def pl9_intro(self):
        self.hide_all_frames()
        self.frame_PL_intro.grid()
        self.intro_PL9.grid_appear()

    # ==============   Pl Solvers ===================

    def pl3_start(self):
        self.hide_all_frames()
        self.pl3_solve_frame.grid()
        self.pl3_solve_frame.grid_rowconfigure((1), weight=1)
        self.pl3_solve_frame.grid_rowconfigure(2, minsize=10)
        self.pl3_solve_frame.grid_columnconfigure(1, minsize=5)
        self.pl3_solve_frame.grid_columnconfigure((0, 3), weight=1)

        self.title = customtkinter.CTkLabel(master=self.pl3_solve_frame, corner_radius=20,
                                            fg_color="transparent",
                                            text="  PL3: Human resource planning",
                                            font=customtkinter.CTkFont(size=20, weight="bold"),
                                            image=self.networking_img,
                                            compound="left"
                                            )
        self.title.grid(row=0, columnspan=4, pady=20, sticky="nsew", padx=20)

        self.tabview_parameter = customtkinter.CTkTabview(master=self.pl3_solve_frame, corner_radius=20,
                                                          fg_color="#FFFFFF",
                                                          border_color="#EDEFF8", border_width=4)
        self.tabview_parameter.grid(row=1, column=0)
        self.tabview_parameter.add("Parameters")

        self.label_type = customtkinter.CTkLabel(master=self.tabview_parameter.tab("Parameters"),
                                                 text="Decision Variable's Type", justify="left", fg_color="#FFCF55",
                                                 corner_radius=30)
        self.label_type.grid(row=1, column=0, padx=20, pady=10, ipadx=5, ipady=3, stick="nsw")

        radio_var = tkinter.IntVar(self)
        self.radio_button1 = customtkinter.CTkRadioButton(self.tabview_parameter.tab("Parameters"), text="INTEGER",
                                                          variable=radio_var, value=1, fg_color="#FFB200")
        self.radio_button1.grid(row=1, column=1, pady=10)
        self.radio_button1.select()
        self.radio_button2 = customtkinter.CTkRadioButton(self.tabview_parameter.tab("Parameters"), text="CONTINOUS",
                                                          variable=radio_var,
                                                          value=2, fg_color="#FFB200")
        self.radio_button2.grid(row=1, column=2, pady=10)

        self.checkbox_frame = CheckBoxFrame(master=self.tabview_parameter.tab("Parameters"),
                                            item_list=["Monday", "Tuesday", "Wednesday",
                                                       "Thursday", "Friday", "Saturday",
                                                       "Sunday"])
        self.checkbox_frame.grid(row=2, padx=30, columnspan=4, ipadx=10, pady=5, sticky="nsew")

        self.pl3_solve_button = customtkinter.CTkButton(master=self.tabview_parameter.tab("Parameters"),
                                                        corner_radius=30,
                                                        fg_color="#FFCB42",
                                                        text="Solve",
                                                        text_color="black", hover_color="#FFB200",
                                                        bg_color="transparent",
                                                        command=lambda: self.pl3_solve(radio_var))
        self.pl3_solve_button.grid(row=3, column=1, padx=10, pady=10)

        self.tabview_solver = customtkinter.CTkTabview(master=self.pl3_solve_frame, corner_radius=20,
                                                       fg_color="#FFFFFF",
                                                       border_color="#EDEFF8", border_width=4, )
        self.tabview_solver.grid(row=1, column=2, ipadx=20)
        self.tabview_solver.add("Solver")
        self.result_label1 = customtkinter.CTkLabel(master=self.tabview_solver.tab("Solver"),
                                                    font=("Roboto Medium", -17), text='')
        self.result_label1.grid(row=0, sticky="nsew", padx=5)
        self.result_label2 = customtkinter.CTkLabel(master=self.tabview_solver.tab("Solver"),
                                                    font=("Roboto Medium", -17), text='')
        self.result_label2.grid(row=1, sticky="nsew", padx=5)

    def pl3_solve(self, radio_var=None):
        if radio_var.get() == 1:
            type = "INTEGER"
        else:
            type = "CONTINOUS"

        list1, list2, nbr_work_day = self.checkbox_frame.get_checked_items()
        result, objval = optimize_staffing(type, len(list1), list2, nbr_work_day)
        dict = {}
        for i in range(len(result)):
            dict[list1[i]] = result[i]
        self.result_label1.configure(text=f"optimal number of employees is : {objval}")
        result_list = [f"{key} : {value}" for key, value in dict.items()]
        result_str = "\n".join(result_list)
        self.result_label2.configure(text=result_str)






    # ================ PL 6 =======================
    def pl6_start(self):
        self.hide_all_frames()
        self.pl6_solve_frame.grid()
        self.pl6_solve_frame.grid_columnconfigure((0), weight = 1)
        self.title = customtkinter.CTkLabel(master=self.pl6_solve_frame, corner_radius=20,
                                            fg_color="transparent",
                                            text="  PL6: Product distribution",
                                            font=customtkinter.CTkFont(size=20, weight="bold"),
                                            image=self.distribution_img,
                                            compound="left"
                                            )
        self.title.grid(row=0, columnspan=4, pady=20, sticky="nsew", padx=20)

        self.frame_generate = customtkinter.CTkFrame(master=self.pl6_solve_frame, corner_radius=20,
                                                     fg_color="#FFFFFF",
                                                     border_color="#EDEFF8", border_width=4)
        self.frame_generate.grid(row=1,columnspan=4, pady=10, padx=20, sticky="nsew")
        self.frame_generate.grid_columnconfigure((1,3), weight= 1)
        nbr_client_label = customtkinter.CTkLabel(master=self.frame_generate, text = "Number Of Clients :")
        nbr_client_label.grid(row = 0 , column = 0 , padx=10, pady=10)
        nbr_client_entry = customtkinter.CTkEntry(master=self.frame_generate)
        nbr_client_entry.grid(row= 0 , column = 1, padx=10, pady =10)

        nbr_depot_label = customtkinter.CTkLabel(master=self.frame_generate, text ="Number of depots :")
        nbr_depot_label.grid(row=0, column=2, padx=10, pady=10)
        nbr_depot_entry = customtkinter.CTkEntry(master=self.frame_generate)
        nbr_depot_entry.grid(row=0, column=3, padx=10, pady=10)

        nbr_factory_label = customtkinter.CTkLabel(master=self.frame_generate, text ="Number Of Factories :")
        nbr_factory_label.grid(row=1, column=0, padx=10, pady=10)
        nbr_factory_entry = customtkinter.CTkEntry(master=self.frame_generate)
        nbr_factory_entry.grid(row=1, column=1, padx=5, pady=10)

        max_transport_label = customtkinter.CTkLabel(master=self.frame_generate , text="Max Transphipment Capacity :", justify="center")
        max_transport_label.grid(row=1, column=2, padx=5, pady=10)
        max_transport_entry = customtkinter.CTkEntry(master=self.frame_generate)
        max_transport_entry.grid(row=1, column=3, padx=5, pady=10)

        generate_button = customtkinter.CTkButton(master=self.frame_generate, text="Generate",corner_radius=30,
                                                        fg_color="#FFCB42",
                                                        text_color="black", hover_color="#FFB200",
                                                        bg_color="transparent")
        generate_button.grid(row = 2 , column = 4 , padx =10, pady=10, sticky="nsew")




############# PL4 ################
    def pl2_start(self):
        self.hide_all_frames()
        self.pl2_solve_frame.grid()
        self.pl2_solve_frame.grid_columnconfigure((0), weight = 1)
        self.title = customtkinter.CTkLabel(master=self.pl2_solve_frame, corner_radius=20,
                                            fg_color="transparent",
                                            text="  PL2: Optimizing Oil Blend Composition",
                                            font=customtkinter.CTkFont(size=20, weight="bold"),
                                            image=self.oil_img,
                                            compound="left"
                                            )
        self.title.grid(row=0, columnspan=4, pady=20, sticky="nsew", padx=20)

        self.frame_generate = customtkinter.CTkFrame(master=self.pl2_solve_frame, corner_radius=20,
                                                     fg_color="#FFFFFF",
                                                     border_color="#EDEFF8", border_width=4)
        self.frame_generate.grid(row=1,columnspan=4, pady=10, padx=20, sticky="nsew")
        self.frame_generate.grid_columnconfigure((1,3), weight= 1)
        nbr_types_label = customtkinter.CTkLabel(master=self.frame_generate, text = "Number of oil types :")
        nbr_types_label.grid(row = 0 , column = 0 , padx=10, pady=10)
        self.nbr_types_entry = customtkinter.CTkEntry(master=self.frame_generate)
        self.nbr_types_entry.grid(row= 0 , column = 1, padx=10, pady =10)
        self.continue_button = customtkinter.CTkButton(master=self.frame_generate, text="continue", command=lambda: self.create_entriesPL2(int(self.nbr_types_entry.get())), width=65)
        self.continue_button.grid(row= 0 , column = 2, padx=10, pady =10)


    def pl2_solve(self):
        print("ok")

    def pl4_start(self):
        self.hide_all_frames()
        self.pl4_solve_frame.grid()
        self.pl4_solve_frame.grid_columnconfigure((0), weight = 1)
        self.title = customtkinter.CTkLabel(master=self.pl4_solve_frame, corner_radius=20,
                                            fg_color="transparent",
                                            text="  PL4: Production Management",
                                            font=customtkinter.CTkFont(size=20, weight="bold"),
                                            image=self.distribution_img,
                                            compound="left"
                                            )
        self.title.grid(row=0, columnspan=4, pady=20, sticky="nsew", padx=20)

        self.frame_generate = customtkinter.CTkFrame(master=self.pl4_solve_frame, corner_radius=20,
                                                     fg_color="#FFFFFF",
                                                     border_color="#EDEFF8", border_width=4)
        self.frame_generate.grid(row=1,columnspan=4, pady=10, padx=20, sticky="nsew")
        self.frame_generate.grid_columnconfigure((1,3), weight= 1)
        nbr_months_label = customtkinter.CTkLabel(master=self.frame_generate, text = "Number Of Months :")
        nbr_months_label.grid(row = 0 , column = 0 , padx=10, pady=10)
        self.nbr_months_entry = customtkinter.CTkEntry(master=self.frame_generate)
        self.nbr_months_entry.grid(row= 0 , column = 1, padx=10, pady =10)
        self.continue_button = customtkinter.CTkButton(master=self.frame_generate, text="continue", command=lambda: self.create_entries(int(self.nbr_months_entry.get())), width=65)
        self.continue_button.grid(row= 0 , column = 2, padx=10, pady =10)


    def pl4_solve(self):
        print("ok")


########## PL7 ####################
    def pl7_start(self):
        self.hide_all_frames()
        self.pl7_solve_frame.grid()
        self.pl7_solve_frame.grid_columnconfigure((0), weight = 1)
        self.title = customtkinter.CTkLabel(master=self.pl7_solve_frame, corner_radius=20,
                                            fg_color="transparent",
                                            text="  PL7: Optimal allocation of resources",
                                            font=customtkinter.CTkFont(size=20, weight="bold"),
                                            image=self.company_img,
                                            compound="left"
                                            )
        self.title.grid(row=0, columnspan=4, pady=20, sticky="nsew", padx=20)

        self.frame_generate = customtkinter.CTkFrame(master=self.pl7_solve_frame, corner_radius=20,
                                                     fg_color="#FFFFFF",
                                                     border_color="#EDEFF8", border_width=4)
        self.frame_generate.grid(row=1,columnspan=4, pady=10, padx=20, sticky="nsew")
        self.frame_generate.grid_columnconfigure((1,3), weight= 1)
        self.frame_generate.grid(row=1,columnspan=4, pady=10, padx=20, sticky="nsew")
        self.frame_generate.grid_columnconfigure((1,3), weight= 1)

        nbr_companies_label = customtkinter.CTkLabel(master=self.frame_generate, text = "Number Of Companies :")
        nbr_companies_label.grid(row = 0 , column = 0 , padx=10, pady=10)
        self.nbr_companies_entry = customtkinter.CTkEntry(master=self.frame_generate)
        self.nbr_companies_entry.grid(row= 0 , column = 1, padx=10, pady =10)

        nbr_projects_label = customtkinter.CTkLabel(master=self.frame_generate, text = "Number Of Projects :")
        nbr_projects_label.grid(row = 0 , column = 2 , padx=10, pady=10)
        self.nbr_projects_entry = customtkinter.CTkEntry(master=self.frame_generate)
        self.nbr_projects_entry.grid(row= 0 , column = 3, padx=10, pady =10)

        
        self.continue_button = customtkinter.CTkButton(master=self.frame_generate, text="continue", command=lambda: self.create_entriesPL7(int(self.nbr_companies_entry.get()),int(self.nbr_projects_entry.get())), width=65)
        self.continue_button.grid(row= 0 , column = 4, padx=10, pady =10)


    def pl7_solve(self):
        print("ok")

    ############## PL9 ##################


    def pl9_start(self):
        self.hide_all_frames()
        self.pl9_solve_frame.grid()
        self.pl9_solve_frame.grid_columnconfigure((0), weight = 1)
        self.title = customtkinter.CTkLabel(master=self.pl9_solve_frame, corner_radius=20,
                                            fg_color="transparent",
                                            text="  PL9: Factory, Warehouse Location and Logistics Planning",
                                            font=customtkinter.CTkFont(size=20, weight="bold"),
                                            image=self.pin_img,
                                            compound="left"
                                            )
        self.title.grid(row=0, columnspan=4, pady=20, sticky="nsew", padx=20)

        self.frame_generate = customtkinter.CTkFrame(master=self.pl9_solve_frame, corner_radius=20,
                                                     fg_color="#FFFFFF",
                                                     border_color="#EDEFF8", border_width=4)
        self.frame_generate.grid(row=1,columnspan=4, pady=10, padx=20, sticky="nsew")
        self.frame_generate.grid_columnconfigure((1,3), weight= 1)
        self.frame_generate.grid(row=1,columnspan=4, pady=10, padx=20, sticky="nsew")
        self.frame_generate.grid_columnconfigure((1,3), weight= 1)

        num_factories_label = customtkinter.CTkLabel(master=self.frame_generate, text = "Number Of Factories :")
        num_factories_label.grid(row = 0 , column = 0 , padx=10, pady=10)
        self.num_factories = customtkinter.CTkEntry(master=self.frame_generate)
        self.num_factories.grid(row= 0 , column = 1, padx=10, pady =10)

        num_depots_label = customtkinter.CTkLabel(master=self.frame_generate, text = "Number Of Depots :")
        num_depots_label.grid(row = 0 , column = 2 , padx=10, pady=10)
        self.num_depots = customtkinter.CTkEntry(master=self.frame_generate)
        self.num_depots.grid(row= 0 , column = 3, padx=10, pady =10)

        num_clients_label = customtkinter.CTkLabel(master=self.frame_generate, text = "Number Of Clients :")
        num_clients_label.grid(row = 0 , column = 4 , padx=10, pady=10)
        self.num_clients = customtkinter.CTkEntry(master=self.frame_generate)
        self.num_clients.grid(row= 0 , column = 5, padx=10, pady =10)


        
        self.continue_button = customtkinter.CTkButton(master=self.frame_generate, text="continue", command=lambda: self.create_entriesPL9(int(self.num_factories.get()),int(self.num_depots.get()),int(self.num_clients.get())), width=65)
        self.continue_button.grid(row= 1 , column = 2, padx=10, pady =10)

    def pl9_solve(self):
        print("ok")

    # ================== Loopback functions ===============

    def go_to_home(self):
        self.hide_all_frames()
        self.frame_right.grid()

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def hide_all_frames(self):
        for widget in self.frame_PL_intro.winfo_children():
            widget.grid_remove()
        for widget in self.pl3_solve_frame.winfo_children():
            widget.grid_remove()

        self.frame_right.grid_remove()
        self.frame_PL_intro.grid_remove()
        self.pl2_solve_frame.grid_remove()

        self.pl3_solve_frame.grid_remove()
        self.pl6_solve_frame.grid_remove()
        self.pl4_solve_frame.grid_remove()
        self.pl7_solve_frame.grid_remove()
        self.pl9_solve_frame.grid_remove()
    def on_closing(self, event=0):
        self.destroy()

################# ###########

    def create_entries(self,nbr_months_entry):

        self.my_framePL4 = MyFramePL4(self.frame_generate, nbr_months_entry)
        self.my_framePL4.grid(row= 1 , column = 1, padx=10, pady =10)

        self.opt_button = customtkinter.CTkButton(master=self.frame_generate, text="optimize", command=lambda: self.button_event(self.my_framePL4), width=65,fg_color="#FFCB42")
        self.opt_button.grid(row= 2 , column = 1, padx=10, pady =10)

        self.result_labelPL4 = customtkinter.CTkLabel(master=self.frame_generate, text="", font=('Arial', 16), justify="left")
        self.result_label1PL4 = customtkinter.CTkLabel(master=self.frame_generate, text="", font=('Arial', 16), justify="left")
        self.result_label2PL4 = customtkinter.CTkLabel(master=self.frame_generate, text="", font=('Arial', 16), justify="left")
        self.result_labelPL4.grid(row= 3 , column = 1, padx=10, pady =10)
        self.result_label1PL4.grid(row= 4 , column = 1, padx=10, pady =10)
        self.result_label2PL4.grid(row= 5 , column = 1, padx=10, pady =10)

    def create_entriesPL2(self,n):
        self.my_frame = MyFramePL2(self.frame_generate, n)
        self.my_frame.grid(row= 1 , column = 1, padx=10, pady =10)
        self.result_label = customtkinter.CTkLabel(master=self.frame_generate, text="", font=('Arial', 16), justify="left")
        self.result_label1 = customtkinter.CTkLabel(master=self.frame_generate, text="", font=('Arial', 16), justify="left")

        self.opt_button = customtkinter.CTkButton(master=self.frame_generate, text="mix", command=lambda: self.button_eventPL2(self.my_frame,n), width=65,fg_color="#FFCB42")
        self.opt_button.grid(row= 2 , column = 1, padx=10, pady =10)
        
        self.result_label.grid(row= 3 , column = 1, padx=10, pady =10)
        self.result_label1.grid(row= 4 , column = 1, padx=10, pady =10)
        

    def create_entriesPL7(self,num_companies,num_projects):

        self.my_framePL7 = MyFramePL7(self.frame_generate, num_companies, num_projects)
        self.my_framePL7.grid(row= 1 , column = 1, padx=10, pady =10)

        self.opt_button = customtkinter.CTkButton(master=self.frame_generate, text="optimize", command=lambda: self.button_eventPL7(self.my_framePL7), width=65)
        self.opt_button.grid(row= 2 , column = 1, padx=10, pady =10)
        self.result_label2PL7 = customtkinter.CTkLabel(master=self.frame_generate, text="", font=('Arial', 16), justify="left")
        self.result_label2PL7.grid(row=3 , column = 1, padx=10, pady =10)




    def button_event(self, my_frame):
        input_array = my_frame.get_input_array()
        result = chaussetous_solver(input_array)
        self.result_labelPL4.configure(text=f"Optimal production plan: {result[0]}")
        self.result_label1PL4.configure(text=f"Optimal worker management: {result[1]}")
        self.result_label2PL4.configure(text=f"Total cost: {result[2]}")


    def button_eventPL7(self, my_frame):
        costs = my_frame.get_costs_array()
        assignment, obj_val = optimize_assignment(costs)
        result_text = ""

        if assignment:
            result_text += "Optimal solution found:\n"
            for i, j in assignment:
                result_text += f"Assign project {j} to company {i}\n"
            result_text += f"Objective value: {obj_val}"
        else:
            result_text = "No optimal solution found."

        self.result_label2PL7.configure(text=result_text)

    def button_eventPL2(self, my_frame,n):
        input_array=my_frame.get_inputs() 
        input_array2 = tuple(input_array)+(n,)

        result = pertrolium_solver(input_array2)
        if result == 0:
            self.result_label.configure(text="No solution available")
        else:
            self.result_label.configure(text="your optimal solution:")
            self.result_label1.configure(text=result)
      

    def button_eventPL9(self, my_frame):
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
        

        
        self.scrollable_frame2 = customtkinter.CTkScrollableFrame(self.frame_generate, width=655, height=10)
        self.scrollable_frame2.grid(row= 5 , column = 2, padx=10, pady =10)

        self.result_labelPL9 = customtkinter.CTkLabel(master=self.scrollable_frame2, text=result, font=('Arial', 16), justify="left",wraplength=650)
        self.result_labelPL9.pack(padx=10, pady=10)



    def create_entriesPL9(self,num_factories,num_depots,num_clients):


        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.frame_generate, width=655, height=150)
        self.scrollable_frame.grid(row= 3 , column = 2, padx=10, pady =10)

        self.my_framePL9 = MyFramePL9(self.scrollable_frame, num_factories, num_depots, num_clients)
        self.my_framePL9.pack()

        self.scrollable_frame.update_idletasks()
        my_frame_y = self.scrollable_frame.winfo_y()

        self.opt_button = customtkinter.CTkButton(self.frame_generate, text="optimize", command=lambda: self.button_eventPL9(self.my_framePL9), width=65,fg_color="#FFCB42")
        self.opt_button.grid(row= 4 , column = 2, padx=10, pady =10)

if __name__ == "__main__":
    app = App()
    app.mainloop()
