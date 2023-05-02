import customtkinter 
from PL2  import pertrolium_solver

customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
class PL2Frame(customtkinter.CTkFrame):
     def __init__(self, master, n, **kwargs):
        super().__init__(master, **kwargs)
        
        self.quantities=[]
        self.qualities=[]
        self.prices = []
        self.marketing_costs = []
        
        for i in range(n):
                entry_label = customtkinter.CTkLabel(self, text=f"Entrer la quantité disponible pour le type {i+1}: ")
                entry_label.grid(row=i, column=0, padx=5, pady=5)
                

                entry1 = customtkinter.CTkEntry(self,width=80)
                entry1.grid(row=i, column=1, padx=5, pady=5)
                
                
                entry_label = customtkinter.CTkLabel(self, text=f"Entrer le niveau de qualité pour le type {i+1}: ")
                entry_label.grid(row=i, column=2, padx=5, pady=5)

                entry2 = customtkinter.CTkEntry(self,width=80)
                entry2.grid(row=i, column=3, padx=5, pady=5)     
                
                
                entry_label = customtkinter.CTkLabel(self, text=f"Entrez le prix par baril pour le type {i+1}: ")
                entry_label.grid(row=i, column=4, padx=5, pady=5)

                entry3 = customtkinter.CTkEntry(self,width=80)
                entry3.grid(row=i, column=5, padx=5, pady=5)
                

                entry_label = customtkinter.CTkLabel(self, text=f"Entrez les frais de marketing pour le type {i+1}: ")
                entry_label.grid(row=i, column=6, padx=5, pady=5)

                entry4 = customtkinter.CTkEntry(self,width=80)
                entry4.grid(row=i, column=7, padx=5, pady=5)
                
                

                self.quantities.append(entry1)
                self.qualities.append(entry2)
                self.prices.append(entry3)
                self.marketing_costs.append(entry4)

        entry_label = customtkinter.CTkLabel(self, text="Entrez la qualité minimale requise :")
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

           
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.my_frame = None
        self.result_label = customtkinter.CTkLabel(master=self, text="", font=('Arial', 16), justify="left")
        self.result_label.place(x=40, y=0)

        self.result_label1 = customtkinter.CTkLabel(master=self, text="", font=('Arial', 16), justify="left")
        self.result_label1.place(x=40, y=0)


        self.title = customtkinter.CTkLabel(master=self, text="Optimizing Oil Blend Composition", font=('Arial', 30), justify="left")
        self.title.place(x=40, y=20)
        self.descp = customtkinter.CTkLabel(master=self, text="Welcome to the Oil Blending Tool! This tool was designed to assist oil companies in optimizing their oil production by selecting the types of oil to blend in order to maximize their revenue. With this interface, you can select the number of oil types you want to include in your mix, specify the quantity, quality, and price of each type. Our mathematical model using Gurobi Python will find the optimal blend to maximize your revenue while meeting the minimum quality specifications for each oil type. This tool will help you improve your efficiency and increase your profitability.", font=('Arial', 14), wraplength=1400, justify="left")
        self.descp.place(x=80, y=70)

        self.title2 = customtkinter.CTkLabel(master=self, text="Customize Your Oil Blend", font=('Arial', 30), justify="left")
        self.title2.place(x=40, y=130)

        self.n_label = customtkinter.CTkLabel(master=self, text="the number of oil types: ", font=('Arial', 16), justify="left")
        self.n_label.place(x=400, y=180)

        self.n_entry = customtkinter.CTkEntry(master=self, width=60)
        self.n_entry.place(x=600, y=180)

        self.continue_button = customtkinter.CTkButton(master=self, text="continue", command=self.create_entries, width=65,fg_color="#FFCB42")
        self.continue_button.place(x=800, y=180)
    def button_event(self, my_frame,n):
        input_array=my_frame.get_inputs() 
        input_array2 = tuple(input_array)+(n,)

        result = pertrolium_solver(input_array2)
        if result == 0:
            self.result_label.configure(text="No solution available")
        else:
            self.result_label.configure(text="your optimal solution:")
            self.result_label1.configure(text=result)
            
                
            
    def create_entries(self):
        try:
            n = int(self.n_entry.get())
        except ValueError:
            print("invalid input")
            return
        self.my_frame = PL2Frame(self, n)
        self.my_frame.place(x=40, y=240)

        self.my_frame.update_idletasks()
        my_frame_y = self.my_frame.winfo_y()

        self.opt_button = customtkinter.CTkButton(master=self, text="mix", command=lambda: self.button_event(self.my_frame,n), width=65,fg_color="#FFCB42")
        self.opt_button.place(x=800, y=my_frame_y + self.my_frame.winfo_height() + 5)
        
        self.result_label.place(x=400, y=my_frame_y + self.my_frame.winfo_height() + 50)
        self.result_label1.place(x=400, y=my_frame_y + self.my_frame.winfo_height() + 100)
        
            
app = App()
app.geometry("1700x1000")
app.mainloop()
