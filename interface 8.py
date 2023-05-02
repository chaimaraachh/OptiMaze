import customtkinter
import numpy as np
import tkinter
from PL8 import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTk



customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, n, **kwargs):
        super().__init__(master, **kwargs)
        
        self.entries = []
        # Update entries list when user changes an entry
        def update_entry(row, col):
            val = self.entries[row][col].get()
            self.entries[row][col].delete(0, 'end')
            self.entries[row][col].insert(0, val)
            self.entries[col][row].delete(0, 'end')
            self.entries[col][row].insert(0, val)
        # Add column headers
        for j in range(n):
            header = customtkinter.CTkLabel(self, text=f"{j+1}")
            header.grid(row=0, column=j+1, padx=5, pady=5)

        # Add row headers and entries
        for i in range(n):
            header = customtkinter.CTkLabel(self, text=f" {i+1}")
            header.grid(row=i+1, column=0, padx=5, pady=5)
            row_entries=[]
            for j in range(n):
                entry = customtkinter.CTkEntry(self, width=50)
                
                entry.insert(0, '0')  # Set default value to 0
                entry.grid(row=i+1, column=j+1, padx=3, pady=5)
                #entry.bind('<FocusOut>', lambda event, i=i, j=j: update_entry(i, j)) #symmetry
                row_entries.append(entry)
            self.entries.append(row_entries)
       
               
        #add start and end cities 
        entry_label = customtkinter.CTkLabel(self, text="Enter start city :")
        entry_label.grid(row=i+2, column=0, padx=5, pady=5)

        self.start_city = customtkinter.CTkEntry(self)
        self.start_city.grid(row=i+2, column=1, padx=7, pady=5)

        entry_label = customtkinter.CTkLabel(self, text="Enter end city :")
        entry_label.grid(row=i+2, column=2, padx=7, pady=5)

        self.end_city = customtkinter.CTkEntry(self)
        self.end_city.grid(row=i+2, column=3, padx=5, pady=5)





   

        

    def get_inputs(self):
        
            distances = []
            for i in range(len(self.entries)):
                row_distances= []
                for j in range(len(self.entries[i])):
                    try:
                        value = int(self.entries[i][j].get())
                    except ValueError:
                        value = np.nan
                    row_distances.append(value)
                distances.append(row_distances)
            start_city = int(self.start_city.get())
            end_city = int(self.end_city.get())
            return distances,start_city,end_city
                
        


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.my_frame = None

        self.title = customtkinter.CTkLabel(master=self, text="Finding the shortest path between two cities ", font=('Arial', 30), justify="center")
        self.title.place(x=20, y=20)

        self.descp = customtkinter.CTkLabel(master=self, text="Welcome to the shortest path problem solver! Given a set of cities and the distances between them, the goal of this problem is to find the shortest path that starts from a specific city and ends at another.Our solver uses the Gurobi optimization library to find the shortest path, ensuring that the solution is both efficient and accurate. Enter your city distances, start city, and end city to find the shortest path!", font=('Arial', 16), wraplength=1400, justify="left")
        self.descp.place(x=70, y=80)

        self.title2 = customtkinter.CTkLabel(master=self, text="Add the number of cities : ", font=('Arial', 20), justify="left")
        self.title2.place(x=20, y=150)

        self.n_label = customtkinter.CTkLabel(master=self, text="Number of cities: ", font=('Arial', 16), justify="center")
        self.n_label.place(x=100, y=200)
        self.n_entry = customtkinter.CTkEntry(master=self, width=50)
        self.n_entry.place(x=250, y=200)

        self.continue_button = customtkinter.CTkButton(master=self, text="continue", command=lambda: self.create_entries(), width=65, fg_color="#FFCB42")
        self.continue_button.place(x=320, y=200)
    def plot_event(self, fig):
        """
        # create tkinter window
        root_tk = tkinter.Tk()
        root_tk.geometry("500x400")
        root_tk.title("circulation network between cities")
        # Create a frame to hold the plot
        frame = tkinter.Frame(root_tk)
        frame.pack()
        # Add the plot to the frame
        canvas = FigureCanvasTk(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Run the window
        root_tk.mainloop()
        """
        fig.show()

    



    def button_event(self, my_frame,n):
        
        input_array = my_frame.get_inputs()
            
        inputs = tuple(input_array) + (n,)
        print(inputs)
        result = shortest_path(inputs)
        print(result)
        fig=plot_shortest_path(inputs)

      
        

        self.result_label = customtkinter.CTkLabel(master=self, text=result, font=('Arial', 16), justify="left")
        self.result_label.place(x=650, y=200)
        self.plot_button = customtkinter.CTkButton(master=self, text="plot circulation network", command=lambda: self.plot_event(fig), width=80,fg_color="#FFCB42")
        self.plot_button.place(x=1300, y=200)

        
        


        



        

    def create_entries(self):
        try:
            n = int(self.n_entry.get())
        except ValueError:
            print("Invalid input")
            return

        if self.my_frame:
            self.my_frame.destroy()

        self.my_frame = MyFrame(self, n)
        self.my_frame.place(x=20, y=260)

        self.my_frame.update_idletasks()
        my_frame_y = self.my_frame.winfo_y()

        self.opt_button = customtkinter.CTkButton(master=self, text="find shortest path", command=lambda: self.button_event(self.my_frame,n), width=80,fg_color="#FFCB42")
        self.opt_button.place(x=500, y=200)

app = App()
app.geometry("1700x1400")
app.mainloop()
