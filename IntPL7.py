import customtkinter
import numpy as np
from PL7 import optimize_assignment

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class MyFrame(customtkinter.CTkFrame):
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


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.my_frame = None
        self.result_label = customtkinter.CTkLabel(master=self, text="", font=('Arial', 16), justify="left")
        self.result_label.place(x=20, y=0)

        self.result_label1 = customtkinter.CTkLabel(master=self, text="", font=('Arial', 16), justify="left")
        self.result_label1.place(x=20, y=0)

        self.result_label2 = customtkinter.CTkLabel(master=self, text="", font=('Arial', 16), justify="left")
        self.result_label2.place(x=20, y=0)

        self.title = customtkinter.CTkLabel(master=self, text="Optimal Resource Allocation", font=('Arial', 30), justify="left")
        self.title.place(x=20, y=20)

        self.descp = customtkinter.CTkLabel(master=self, text="A client has issued a call for proposals for a certain number of projects. Multiple companies have submitted bids according to a given table. The goal is to determine the optimal allocation that allows completing all projects at a minimum cost, while considering that:Any company without a bid for a project cannot be selected for that projectExactly one company is selected for each project.A company cannot undertake more than a specified number of projects.",
                                            font=('Arial', 14), wraplength=650, justify="left")
        self.descp.place(x=20, y=70)

        self.title2 = customtkinter.CTkLabel(master=self, text="Add your variables and constraints", font=('Arial', 30), justify="left")
        self.title2.place(x=20, y=150)

        self.num_companies_label = customtkinter.CTkLabel(master=self, text="Number of companies: ", font=('Arial', 16), justify="left")
        self.num_companies_label.place(x=20, y=190)
        
        self.num_projects_label = customtkinter.CTkLabel(master=self, text="Number of projects: ", font=('Arial', 16), justify="left")
        self.num_projects_label.place(x=20, y=230)

        self.num_companies_entry = customtkinter.CTkEntry(master=self, width=40)
        self.num_companies_entry.place(x=180, y=190)

        self.num_projects_entry = customtkinter.CTkEntry(master=self, width=40)
        self.num_projects_entry.place(x=180, y=230)

        self.continue_button = customtkinter.CTkButton(master=self, text="continue", command=lambda: self.create_entries(), width=65)
        self.continue_button.place(x=240, y=210)
        

    def button_event(self, my_frame):
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

        self.result_label.configure(text=result_text)
        self.result_label.place(x=20, y=my_frame.winfo_y() + self.my_frame.winfo_height() + 35)


        
    def create_entries(self):
        try:
            num_companies = int(self.num_companies_entry.get())
            num_projects = int(self.num_projects_entry.get())
        except ValueError:
            print("Invalid input")
            return

        if self.my_frame:
            self.my_frame.destroy()

        self.my_frame = MyFrame(self, num_companies, num_projects)
        self.my_frame.place(x=20, y=260)

        self.my_frame.update_idletasks()
        my_frame_y = self.my_frame.winfo_y()

        self.opt_button = customtkinter.CTkButton(master=self, text="optimize", command=lambda: self.button_event(self.my_frame), width=65)
        self.opt_button.place(x=230, y=my_frame_y + self.my_frame.winfo_height() + 15)



app = App()
app.geometry("700x900")
app.mainloop()
