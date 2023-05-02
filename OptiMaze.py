import tkinter
import networkx as nx
import pandas as pd
import matplotlib

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.figure as fig
import matplotlib.pyplot as plt
import customtkinter
import os
from PIL import Image

from optimazeTools.PL3 import optimize_staffing
from optimazeTools.PL6 import optimize_distribution
from optimazeTools.PL6_graph import plot_logistic_graph

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("custom")  # Themes: "blue" (standard), "green", "dark-blue"
quantity_matrix = None
"""
class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("700x600")
        global quantity_matrix
        G = create_logistic_graph(quantity_matrix)

        figure = plt.Figure()
        ax = figure.add_subplot(111)
        #canvas = FigureCanvasTkAgg(figure, master=self)
        #canvas.get_tk_widget().grid()
        pos = nx.circular_layout(G)
        # edge_labels = {(i, j): f'{G.edges[i, j]["weight"]}' for i, j in G.edges}
        # Only include non-null edges in the graph
        non_null_edges = [(i, j) for i, j in G.edges if not pd.isnull(G.edges[i, j]['weight'])]

        # Create a dictionary of edge labels for only the non-null edges
        edge_labels = {(i, j): f'{G.edges[i, j]["weight"]}' for i, j in non_null_edges}

        nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=12, ax=ax)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, ax=ax)
        #canvas.draw()
        figure.show()
"""

class ScrollableFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, nbr_clt, nbr_fact, **kwargs):
        super().__init__(master, corner_radius=20, fg_color="#FFFFFF",
                         border_color="#EDEFF8", border_width=4, width=600, height=400, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # add widgets onto the frame...
        self.nbr_clients = nbr_clt
        self.nbr_factories = nbr_fact
        self.client_demands = []
        self.factories_capacity = []
        label_client = customtkinter.CTkLabel(self, text=" Clients Demands :", fg_color="#FFCF55",
                                              corner_radius=30)
        label_client.grid(row=0, columnspan=4, padx=10, pady=10)
        for i in range(self.nbr_clients):
            label1 = customtkinter.CTkLabel(master=self, text=f"Client {i} :")
            label1.grid(row=len(self.client_demands) + 1, column=0, padx=10, pady=10)
            entry1 = customtkinter.CTkEntry(master=self)
            entry1.grid(row=len(self.client_demands) + 1, column=1, padx=10, pady=10)
            self.client_demands.append(entry1)

        label_factories = customtkinter.CTkLabel(self, text="Factories Capacity :", fg_color="#FFCF55",
                                                 corner_radius=30)
        label_factories.grid(row=len(self.client_demands) + 1, columnspan=4, padx=10, pady=10)

        for i in range(self.nbr_factories):
            label1 = customtkinter.CTkLabel(master=self, text=f"Factory {i} :")
            label1.grid(row=len(self.factories_capacity) + 2 + len(self.client_demands), column=0, padx=10, pady=10)
            entry2 = customtkinter.CTkEntry(master=self)
            entry2.grid(row=len(self.factories_capacity) + 2 + len(self.client_demands), column=1, padx=10, pady=10)
            self.factories_capacity.append(entry2)

    def get_items(self):
        return [int(client.get()) for client in self.client_demands], [int(factory.get()) for factory in
                                                                       self.factories_capacity]


class ScrollableFrame_2(customtkinter.CTkScrollableFrame):
    def __init__(self, master, nbr_clt, nbr_fact, nbr_depot, **kwargs):
        super().__init__(master, corner_radius=20, fg_color="#FFFFFF",
                         border_color="#EDEFF8", border_width=4, width=600, height=400, **kwargs)
        self.grid_rowconfigure((1, 2), weight=1)
        self.grid_columnconfigure((1, 2), weight=1)
        # add widgets onto the frame...
        self.nbr_clients = nbr_clt
        self.nbr_factories = nbr_fact
        self.nbr_depot = nbr_depot
        self.client_cost = []
        self.factories_cost = []
        self.depot_cost = []
        client_list = []
        factory_list = []
        depot_list = []
        for i in range(self.nbr_clients):
            client_list.append(f"Client {i}")
        for i in range(self.nbr_factories):
            factory_list.append(f"Factory {i}")
        for i in range(self.nbr_depot):
            depot_list.append(f"Depot {i}")

        factory_headers = factory_list + depot_list + client_list
        depot_headers = depot_list + client_list

        label_client = customtkinter.CTkLabel(self, text="Transhipment Costs :", fg_color="#FFCF55",
                                              corner_radius=30)
        label_client.grid(row=0, columnspan=4, padx=10, pady=10)
        for i in range(self.nbr_clients):
            label_client = customtkinter.CTkLabel(self, text=f" Client {i} :", fg_color="#FFCF55",
                                                  corner_radius=30)
            label_client.grid(row=len(self.client_cost) + 1, column=0, padx=10, pady=10)
            for j, key in enumerate(client_list):
                if i == j:
                    continue
                else:
                    label1 = customtkinter.CTkLabel(master=self, text=f"{key} :")
                    label1.grid(row=len(self.client_cost) + 1, column=1, padx=10, pady=10)
                    entry1 = customtkinter.CTkEntry(master=self)
                    entry1.grid(row=len(self.client_cost) + 1, column=2, padx=10, pady=10)
                    self.client_cost.append(entry1)

        for i in range(self.nbr_factories):
            label_client = customtkinter.CTkLabel(self, text=f" Factory {i}:", fg_color="#FFCF55",
                                                  corner_radius=30)
            label_client.grid(row=len(self.factories_cost) + 2 + len(self.client_cost), column=0, padx=10, pady=10)
            for j, key in enumerate(factory_headers):
                if i == j:
                    continue
                else:
                    label2 = customtkinter.CTkLabel(master=self, text=f"{key} :")
                    label2.grid(row=len(self.factories_cost) + 2 + len(self.client_cost), column=1, padx=10, pady=10)
                    entry2 = customtkinter.CTkEntry(master=self)
                    entry2.grid(row=len(self.factories_cost) + 2 + len(self.client_cost), column=2, padx=10, pady=10)
                    self.factories_cost.append(entry2)

        for i in range(self.nbr_depot):
            label_client = customtkinter.CTkLabel(self, text=f" depot {i}:", fg_color="#FFCF55",
                                                  corner_radius=30)
            label_client.grid(row=len(self.depot_cost) + 2 + len(self.client_cost) + len(self.factories_cost), column=0,
                              padx=10, pady=10)
            for j, key in enumerate(depot_headers):
                if i == j:
                    continue
                else:
                    label3 = customtkinter.CTkLabel(master=self, text=f"{key} :")
                    label3.grid(row=len(self.depot_cost) + 2 + len(self.client_cost) + len(self.factories_cost),
                                column=1, padx=10, pady=10)
                    entry3 = customtkinter.CTkEntry(master=self)
                    entry3.grid(row=len(self.depot_cost) + 2 + len(self.client_cost) + len(self.factories_cost),
                                column=2, padx=10, pady=10)
                    self.factories_cost.append(entry3)

    def get_items(self):
        return [int(factory.get()) for factory in self.factories_cost] + [int(depot.get()) for depot in
                                                                          self.client_cost] + [int(client.get()) for
                                                                                               client in
                                                                                               self.client_cost]


class ScrollableFrameResult(customtkinter.CTkScrollableFrame):
    def __init__(self, master, nbr_clt, nbr_fact, nbr_depot, result, **kwargs):
        super().__init__(master, corner_radius=20, fg_color="#FFFFFF",
                         border_color="#EDEFF8", border_width=4, width=600, height=400, **kwargs)
        self.grid_rowconfigure((1, 2), weight=1)
        self.grid_columnconfigure((1, 2), weight=1)
        # add widgets onto the frame...
        self.nbr_clients = nbr_clt
        self.nbr_factories = nbr_fact
        self.nbr_depot = nbr_depot
        self.client_cost = []
        self.factories_cost = []
        self.depot_cost = []
        self.all_entries = []  # self.factories_cost + self.depot_cost + self.client_cost
        client_list = []
        factory_list = []
        depot_list = []
        for i in range(self.nbr_clients):
            client_list.append(f"Client {i}")
        for i in range(self.nbr_factories):
            factory_list.append(f"Factory {i}")
        for i in range(self.nbr_depot):
            depot_list.append(f"Depot {i}")

        factory_headers = factory_list + depot_list + client_list
        depot_headers = depot_list + client_list
        label_client = customtkinter.CTkLabel(self, text="Optimal Transhipment Quantity :", fg_color="#FFCF55",
                                              corner_radius=30)
        label_client.grid(row=0, columnspan=4, padx=10, pady=10)

        for i in range(self.nbr_factories):
            label_client = customtkinter.CTkLabel(self, text=f" Factory {i}:", fg_color="#FFCF55",
                                                  corner_radius=30)
            label_client.grid(row=len(self.factories_cost) + 1, column=0, padx=10, pady=10)
            for j, key in enumerate(factory_headers):
                if i == j:
                    continue
                else:
                    label2 = customtkinter.CTkLabel(master=self, text=f"{key} :")
                    label2.grid(row=len(self.factories_cost) + 1, column=1, padx=10, pady=10)
                    entry2 = customtkinter.CTkEntry(master=self)
                    entry2.grid(row=len(self.factories_cost) + 1, column=2, padx=10, pady=10)
                    self.factories_cost.append(entry2)
                    self.all_entries.append(entry2)

        for i in range(self.nbr_depot):
            label_client = customtkinter.CTkLabel(self, text=f" depot {i}:", fg_color="#FFCF55",
                                                  corner_radius=30)
            label_client.grid(row=len(self.depot_cost) + 2 + len(self.factories_cost), column=0,
                              padx=10, pady=10)
            for j, key in enumerate(depot_headers):
                if i == j:
                    continue
                else:
                    label3 = customtkinter.CTkLabel(master=self, text=f"{key} :")
                    label3.grid(row=len(self.depot_cost) + 2 + len(self.factories_cost),
                                column=1, padx=10, pady=10)
                    entry3 = customtkinter.CTkEntry(master=self)
                    entry3.grid(row=len(self.depot_cost) + 2 + len(self.factories_cost),
                                column=2, padx=10, pady=10)
                    self.depot_cost.append(entry3)
                    self.all_entries.append(entry3)

        for i in range(self.nbr_clients):
            label_client = customtkinter.CTkLabel(self, text=f" Client {i} :", fg_color="#FFCF55",
                                                  corner_radius=30)
            label_client.grid(row=len(self.client_cost) + len(self.depot_cost) + 2 + len(self.factories_cost), column=0,
                              padx=10, pady=10)
            for j, key in enumerate(client_list):
                if i == j:
                    continue
                else:
                    label1 = customtkinter.CTkLabel(master=self, text=f"{key} :")
                    label1.grid(row=len(self.client_cost) + len(self.depot_cost) + 2 + len(self.factories_cost),
                                column=1, padx=10, pady=10)
                    entry1 = customtkinter.CTkEntry(master=self)
                    entry1.grid(row=len(self.client_cost) + len(self.depot_cost) + 2 + len(self.factories_cost),
                                column=2, padx=10, pady=10)

                    self.client_cost.append(entry1)
                    self.all_entries.append(entry1)

        for i in range(len(self.all_entries)):
            print(self.all_entries[i])
            self.all_entries[i].insert(0, str(result[i]))
            self.all_entries[i].configure(state="disabled")


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


def get_values(self):
    values = []
    for row in self.table:
        row_values = []
        for cell in row:
            if cell.cget("state") == 'disabled':
                continue
            else:
                row_values.append(cell.get())
        values.append(row_values)
    return values


class App(customtkinter.CTk):
    WIDTH = 1300
    HEIGHT = 700
    global quantity_matrix

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

        self.pl3_solve_frame = customtkinter.CTkFrame(master=self, fg_color="#F9FAFF")
        self.pl3_solve_frame.grid(row=0, column=1, sticky="nswe", pady=(0, 10))
        self.pl3_solve_frame.grid_remove()

        self.pl6_solve_frame = customtkinter.CTkFrame(master=self, fg_color="#F9FAFF")
        self.pl6_solve_frame.grid(row=0, column=1, sticky="nswe", pady=(0, 10))
        self.pl6_solve_frame.grid_remove()

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
        self.card2 = Cards(self.frame_cards, 1, 3, None, self.oil_img, "\nPL2: Blending in oil production")
        self.card3 = Cards(self.frame_cards, 1, 5, self.pl3_intro, self.networking_img,
                           "\nPL3: Human resource planning")
        self.card4 = Cards(self.frame_cards, 3, 1, None, self.shoes_img, "\nPL4: Production management")
        self.card5 = Cards(self.frame_cards, 3, 3, None, self.eco_house_img, "\nPL5: Electricity production")
        self.card6 = Cards(self.frame_cards, 3, 5, self.pl6_intro, self.distribution_img,
                           "\n PL6: Product distribution")
        self.card7 = Cards(self.frame_cards, 5, 1, None, self.company_img, "\nPL7: Optimal allocation of resources")
        self.card8 = Cards(self.frame_cards, 5, 3, None, self.road_img, "\nPL8: Equipment replacement")
        self.card9 = Cards(self.frame_cards, 5, 5, None, self.pin_img, "\nPL9: Factories and depots location\n& "
                                                                       "logistics planning")

        # ============ frame_PL_introduction ============
        self.frame_PL_intro.grid_columnconfigure(0, weight=1)
        self.frame_PL_intro.grid_rowconfigure(0, weight=1)
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

        # ========== functions =============

    # =============== PL Introductions =================
    def pl3_intro(self):
        self.hide_all_frames()
        self.frame_PL_intro.grid()
        self.intro_PL3.grid_appear()

    def pl6_intro(self):
        self.hide_all_frames()
        self.frame_PL_intro.grid()
        self.intro_PL6.grid_appear()

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

        radio_var = tkinter.IntVar(0)
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
        self.pl3_reset_button = customtkinter.CTkButton(master=self.tabview_parameter.tab("Parameters"),
                                                        corner_radius=30,
                                                        fg_color="#FFCB42",
                                                        text="Reset",
                                                        text_color="black", hover_color="#FFB200",
                                                        bg_color="transparent",
                                                        command=self.pl3_start)
        self.pl3_reset_button.grid(row=3, column=0, padx=10, pady=10)

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
        self.pl6_solve_frame.grid_columnconfigure((0), weight=1)
        self.pl6_solve_frame.grid_rowconfigure(2, weight=1)
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
        self.frame_generate.grid(row=1, columnspan=4, pady=10, padx=20, sticky="nsew")
        self.frame_generate.grid_columnconfigure((1, 3), weight=1)

        nbr_client_label = customtkinter.CTkLabel(master=self.frame_generate, text="Number Of Clients :")
        nbr_client_label.grid(row=0, column=0, padx=10, pady=10)
        nbr_client_entry = customtkinter.CTkEntry(master=self.frame_generate)
        nbr_client_entry.grid(row=0, column=1, padx=10, pady=10)

        nbr_depot_label = customtkinter.CTkLabel(master=self.frame_generate, text="Number of depots :")
        nbr_depot_label.grid(row=0, column=2, padx=10, pady=10)
        nbr_depot_entry = customtkinter.CTkEntry(master=self.frame_generate)
        nbr_depot_entry.grid(row=0, column=3, padx=10, pady=10)

        nbr_factory_label = customtkinter.CTkLabel(master=self.frame_generate, text="Number Of Factories :")
        nbr_factory_label.grid(row=1, column=0, padx=10, pady=10)
        nbr_factory_entry = customtkinter.CTkEntry(master=self.frame_generate)
        nbr_factory_entry.grid(row=1, column=1, padx=5, pady=10)

        max_transport_label = customtkinter.CTkLabel(master=self.frame_generate, text="Max Transphipment Capacity :",
                                                     justify="center")
        max_transport_label.grid(row=1, column=2, padx=5, pady=10)
        max_transport_entry = customtkinter.CTkEntry(master=self.frame_generate)
        max_transport_entry.grid(row=1, column=3, padx=5, pady=10)

        solve_button = customtkinter.CTkButton(master=self.frame_generate, text="Solve", corner_radius=30,
                                               fg_color="#FFCB42",
                                               text_color="black", hover_color="#FFB200",
                                               bg_color="transparent", state="disabled",
                                               command=None)
        solve_button.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")
        generate_button = customtkinter.CTkButton(master=self.frame_generate, text="Generate", corner_radius=30,
                                                  fg_color="#FFCB42",
                                                  text_color="black", hover_color="#FFB200",
                                                  bg_color="transparent",
                                                  command=lambda: self.generate(nbr_client_entry, nbr_factory_entry,
                                                                                solve_button, nbr_depot_entry,
                                                                                max_transport_entry))

        generate_button.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    def generate(self, client_entry, factory_entry, button, dpt_entry, transp_entry):
        table = ScrollableFrame(self.pl6_solve_frame, int(client_entry.get()), int(factory_entry.get()))
        table.grid(row=2, column=0, padx=10, pady=10)
        table2 = ScrollableFrame_2(self.pl6_solve_frame, int(client_entry.get()), int(factory_entry.get()),
                                   int(dpt_entry.get()))
        table2.grid(row=2, column=1, padx=10, pady=10)
        button.configure(state="normal",
                         command=lambda: self.pl6_solve(client_entry, factory_entry, dpt_entry, transp_entry, table,
                                                        table2))

    def pl6_solve(self, client_entry, factory_entry, dpt_entry, transp_entry, table, table2):
        self.hide_all_frames()
        self.pl6_solve_frame.grid()
        self.pl6_solve_frame.grid_rowconfigure(2, weight=1)
        label = customtkinter.CTkLabel(self.pl6_solve_frame, text=" Solver", fg_color="#FFCF55",
                                       corner_radius=30)
        label.grid(row=0, columnspan=4, padx=10, pady=10)
        client_cap, factory_cap = table.get_items()

        costs = table2.get_items()
        objval, result, quantity = optimize_distribution(costs, factory_cap, client_cap, int(dpt_entry.get()),
                                                                int(transp_entry.get()))
        frame_result = ScrollableFrameResult(self.pl6_solve_frame, len(client_cap), len(factory_cap),
                                             int(dpt_entry.get()), result)
        frame_result.grid(row=0, column=0, padx=10, pady=10)
        reset_button = customtkinter.CTkButton(master=self.pl6_solve_frame, text="Reset", corner_radius=30,
                                               fg_color="#FFCB42",
                                               text_color="black", hover_color="#FFB200",
                                               bg_color="transparent",
                                               command=self.pl6_start)
        reset_button.grid(row=1, column=1, padx=10, pady=10)
        client_list = []
        factory_list = []
        depot_list = []
        headers = []
        for i in range(len(client_cap)):
            client_list.append(f"Client {i}")
        for i in range(len(factory_cap)):
            factory_list.append(f"Factory {i}")
        for i in range(int(dpt_entry.get())):
            depot_list.append(f"Depot {i}")
        headers = factory_list + depot_list +client_list
        quantity_matrix =  pd.DataFrame(quantity,
                                        columns= headers,
                                        index=headers,
                                        )

        graph_button = customtkinter.CTkButton(master=self.pl6_solve_frame, text="Generate Logistics Graph",
                                               corner_radius=30,
                                               fg_color="#FFCB42",
                                               text_color="black", hover_color="#FFB200",
                                               bg_color="transparent",
                                               command=lambda : self.plot())
        graph_button.grid(row=1, column=0, padx=10, pady=10)

    # ================== Loopback functions ===============

    def plot(self):
        plot_logistic_graph()
        """
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self.frame_generate)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it
        """
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
        for widget in self.pl6_solve_frame.winfo_children():
            widget.grid_remove()

        self.frame_right.grid_remove()
        self.frame_PL_intro.grid_remove()
        self.pl3_solve_frame.grid_remove()
        self.pl6_solve_frame.grid_remove()

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
