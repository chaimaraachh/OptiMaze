import customtkinter
from PL4 import chaussetous_solver

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, num_months, **kwargs):
        super().__init__(master, **kwargs)

        self.stock = []
        self.demand = []

        for i in range(num_months):
            entry_label = customtkinter.CTkLabel(self, text=f"storage costs {i+1}:")
            entry_label.grid(row=i, column=0, padx=5, pady=5)

            entry = customtkinter.CTkEntry(self)
            entry.grid(row=i, column=1, padx=5, pady=5)
            
            entry_label = customtkinter.CTkLabel(self, text=f"demand {i+1}:")
            entry_label.grid(row=i, column=2, padx=5, pady=5)

            entry2 = customtkinter.CTkEntry(self)
            entry2.grid(row=i, column=3, padx=5, pady=5)

            self.stock.append(entry)
            self.demand.append(entry2)
        entry_label = customtkinter.CTkLabel(self, text="initial stock:")
        entry_label.grid(row=i+1, column=0, padx=5, pady=5)
        self.initial_stock = customtkinter.CTkEntry(self)
        self.initial_stock.grid(row=i+1, column=1, padx=5, pady=5)

        entry_label = customtkinter.CTkLabel(self, text="initial workers:")
        entry_label.grid(row=i+1, column=2, padx=5, pady=5)
        self.initial_workers = customtkinter.CTkEntry(self)
        self.initial_workers.grid(row=i+1, column=3, padx=5, pady=5)

        entry_label = customtkinter.CTkLabel(self, text="worker salary:")
        entry_label.grid(row=i+2, column=0, padx=5, pady=5)
        self.worker_salary = customtkinter.CTkEntry(self)
        self.worker_salary.grid(row=i+2, column=1, padx=5, pady=5)

        entry_label = customtkinter.CTkLabel(self, text="max overtime:")
        entry_label.grid(row=i+2, column=2, padx=5, pady=5)
        self.max_overtime = customtkinter.CTkEntry(self)
        self.max_overtime.grid(row=i+2, column=3, padx=5, pady=5)

        entry_label = customtkinter.CTkLabel(self, text="overtime pay:")
        entry_label.grid(row=i+3, column=0, padx=5, pady=5)
        self.overtime_pay = customtkinter.CTkEntry(self)
        self.overtime_pay.grid(row=i+3, column=1, padx=5, pady=5)

        entry_label = customtkinter.CTkLabel(self, text="hours per shoe:")
        entry_label.grid(row=i+3, column=2, padx=5, pady=5)
        self.hours_per_shoe = customtkinter.CTkEntry(self)
        self.hours_per_shoe.grid(row=i+3, column=3, padx=5, pady=5)

        entry_label = customtkinter.CTkLabel(self, text="material cost:")
        entry_label.grid(row=i+4, column=0, padx=5, pady=5)
        self.material_cost = customtkinter.CTkEntry(self)
        self.material_cost.grid(row=i+4, column=1, padx=5, pady=5)

        entry_label = customtkinter.CTkLabel(self, text="recruitment cost:")
        entry_label.grid(row=i+4, column=2, padx=5, pady=5)
        self.recruitment_cost = customtkinter.CTkEntry(self)
        self.recruitment_cost.grid(row=i+4, column=3, padx=5, pady=5)

        entry_label = customtkinter.CTkLabel(self, text="layoff cost:")
        entry_label.grid(row=i+5, column=0, padx=5, pady=5)
        self.layoff_cost = customtkinter.CTkEntry(self)
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

        self.title = customtkinter.CTkLabel(master=self, text="Production Management", font=('Arial', 30), justify="left")
        self.title.place(x=20, y=20)

        self.descp = customtkinter.CTkLabel(master=self, text="A company must meet varying product demands over several months, with an initial stock and workforce. Workers have a fixed salary, work a certain number of hours, and can work overtime at an additional rate. Producing a product unit requires labor and raw materials, and there are costs for recruitment, layoffs, and storage. The goal is to determine the optimal production plan and worker management policy to minimize costs while meeting monthly demands.", font=('Arial', 14), wraplength=550, justify="left")
        self.descp.place(x=20, y=70)

        self.title2 = customtkinter.CTkLabel(master=self, text="Add your variables and constraints", font=('Arial', 30), justify="left")
        self.title2.place(x=20, y=170)

        self.num_months_label = customtkinter.CTkLabel(master=self, text="Number of months: ", font=('Arial', 16), justify="left")
        self.num_months_label.place(x=20, y=210)

        self.num_months_entry = customtkinter.CTkEntry(master=self, width=40)
        self.num_months_entry.place(x=160, y=210)

        self.continue_button = customtkinter.CTkButton(master=self, text="continue", command=self.create_entries, width=65)
        self.continue_button.place(x=230, y=210)
        
    def button_event(self, my_frame):
        input_array = my_frame.get_input_array()
        result = chaussetous_solver(input_array)
        print(input_array)
        self.result_label.configure(text=f"Optimal production plan: {result[0]}")
        self.result_label1.configure(text=f"Optimal worker management: {result[1]}")
        self.result_label2.configure(text=f"Total cost: {result[2]}")

        
    def create_entries(self):
        try:
            num_months = int(self.num_months_entry.get())
        except ValueError:
            print("Invalid input")
            return

        self.my_frame = MyFrame(self, num_months)
        self.my_frame.place(x=20, y=240)

        self.my_frame.update_idletasks()
        my_frame_y = self.my_frame.winfo_y()

        self.opt_button = customtkinter.CTkButton(master=self, text="optimize", command=lambda: self.button_event(self.my_frame), width=65)
        self.opt_button.place(x=230, y=my_frame_y + self.my_frame.winfo_height() + 15)
        
        self.result_label.place(x=20, y=my_frame_y + self.my_frame.winfo_height() + 50)
        self.result_label1.place(x=20, y=my_frame_y + self.my_frame.winfo_height() + 75)
        self.result_label2.place(x=20, y=my_frame_y + self.my_frame.winfo_height() + 100)




app = App()
app.geometry("600x900")
app.mainloop()
