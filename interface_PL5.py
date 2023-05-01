from typing import Literal, Optional, Tuple, Union
from typing_extensions import Literal
import customtkinter as ctk 
import tkinter as tk
from customtkinter.windows.widgets.font import CTkFont
import gurobipy as gp
from gurobipy import GRB
import PL5

nbreVilles = 0
nbreCentrales = 0
Offres=[]
Demandes=[]
Couts=[]
Pénaltie = []


ctk.set_appearance_mode("light")

ctk.set_default_color_theme("blue")

class inputs(ctk.CTkFrame):
    def __init__(self, master: any):
        super().__init__(master, width=300)
        # self.grid_columnconfigure((1,2),weight=1)
        self.configure(width=300)
        self.title = ctk.CTkLabel(self,text="Choose the number of cities and the number of power plants: ", font=('Arial',16))
        self.title.grid(row=1, column = 2,pady=2)

        self.nbreVillesLabel = ctk.CTkLabel(self,text="Nombre de villes", fg_color='transparent')
        self.nbreVillesEntry = ctk.CTkEntry(self,bg_color='transparent')

        self.nbreVillesLabel.grid(row=2 , column = 2,sticky="ew")
        self.nbreVillesEntry.grid(row = 2 , column = 3,sticky="we",padx=5,pady=2)
        self.nbreVillesEntry.insert(0, 4)

        self.nbreCentralesLabel = ctk.CTkLabel(self,text="Nombre de centrales", fg_color='transparent')
        self.nbreCentralesEntry = ctk.CTkEntry(self,bg_color='transparent')

        self.nbreCentralesLabel.grid(row=3 , column = 2,sticky="ew")
        self.nbreCentralesEntry.grid(row = 3 , column = 3,sticky="ew",padx=5, pady=2)
        self.nbreCentralesEntry.insert(0, 3)

class TableauOffres(ctk.CTkScrollableFrame):
    def __init__(self, master,rows):
        super().__init__(master , width = 235)
        self.Offres=[]
        i = 0

        R_label = ctk.CTkLabel(self, text="Offers:")
        R_label.grid(row=0, column=1, padx=5, pady=5)
        

        for i in range(rows):
            Culture_label = ctk.CTkLabel(self, text=f"Power Plant {i+1}:",)
            Culture_label.grid(row=i+1, column=0, padx=5, pady=5)

            entry = ctk.CTkEntry(self)
            entry.grid(row=i+1, column=1, padx=5, pady=5)

            self.Offres.append(entry)

    def get_input_array(self,label):
        global Offres
        Offres = []
        for x in self.Offres:
            if len(x.get()) == 0:
                label.configure("One or more tables is still empty or not fully filled")
            else : 
                Offres = [int(x.get()) for x in self.Offres]

class TableauDemandes(ctk.CTkScrollableFrame):
    def __init__(self, master,rows):
        super().__init__(master, width = 225, height=100)
        self.Demandes=[]
        i = 0

        R_label = ctk.CTkLabel(self, text="Demands:")
        R_label.grid(row=0, column=1, padx=5, pady=5)
        

        for i in range(rows):
            Culture_label = ctk.CTkLabel(self, text=f"City {i+1}:",)
            Culture_label.grid(row=i+1, column=0, padx=5, pady=5)

            entry = ctk.CTkEntry(self)
            entry.grid(row=i+1, column=1, padx=5, pady=5)

            self.Demandes.append(entry)

    def get_input_array(self,label):
        global Demandes
        Demandes = []
        for x in self.Demandes:
            if len(x.get()) == 0:
                label.configure("One or more tables is still empty or not fully filled")
            else: 
                Demandes = [int(x.get()) for x in self.Demandes]
    
class TableauPénaltie(ctk.CTkScrollableFrame):
    def __init__(self, master,rows):
        super().__init__(master, width = 225, height=100)
        self.pénaltie=[]
        i = 0

        R_label = ctk.CTkLabel(self, text="Penalties :")
        R_label.grid(row=0, column=1, padx=5, pady=5)
        

        for i in range(rows):
            Culture_label = ctk.CTkLabel(self, text=f"City {i+1}:",)
            Culture_label.grid(row=i+1, column=0, padx=5, pady=5)

            entry = ctk.CTkEntry(self)
            entry.grid(row=i+1, column=1, padx=5, pady=5)

            self.pénaltie.append(entry)

    def get_input_array(self,label):
        global Pénaltie
        Pénaltie = []
        for x in self.pénaltie:
            if len(x.get()) == 0:
                label.configure("One or more tables is still empty or not fully filled")
            else: 
                Pénaltie = [int(x.get()) for x in self.pénaltie]

class TableauCout(ctk.CTkScrollableFrame):
    entries = []
    def __init__(self,master, width =600):
        global nbreVilles, nbreCentrales, Couts
        
        super().__init__(master, width = 620, height = 100)
        # create table of entries
        self.configure(label_text = "The cost of transporting a Kwh from a given power plant to a given city:", label_fg_color = "transparent")
        for i in range(nbreCentrales):
                row = []
                label_centrale = ctk.CTkLabel(self, text=f"centrale {i+1}")
                label_centrale.grid(row=i+1, column=0)
                for j in range(nbreVilles):
                    label_ville = ctk.CTkLabel(self, text=f"ville {j+1}")
                    label_ville.grid(row=0, column=j+1)
                    entry = ctk.CTkEntry(self)
                    entry.grid(row=i+1, column=j+1)
                    row.append(entry)
                self.entries.append(row)

    def get_cell_values(self,label):
        global Couts
        SCouts = []
        for row in self.entries:
            row_values = []
            for entry in row:
                value = entry.get()
                if value == '': 
                    label.configure("One or more tables is still empty or not fully filled")
                    return
                row_values.append(entry.get())
            SCouts.append(row_values)
        strings = SCouts[-nbreCentrales:]
        Couts = [[int(x) for x in row] for row in strings]
        SCouts = []

class Result(ctk.CTkScrollableFrame):
    def __init__(self,master):
        super().__init__(master, width = 600, height = 50)
        self.text = ctk.CTkLabel(self,text="")
        self.text.grid()
    def configure(self,x):
        self.text.configure(text=x)

class App(ctk.CTk):
    def __init__(self):
        
        super().__init__()

        self.title("PL5")
        self.geometry("1200x650")

        self.Inputs = inputs(self)
        self.Inputs.grid(row= 0, sticky = "ew",padx=5,pady=5)
        self.Inputs.place(relx=0.5,rely=0.1,anchor="center")

        def getInput(centrales , villes):
            global nbreVilles, nbreCentrales, Couts, Offres , Demandes 
            nbreCentrales = int(centrales.get())
            nbreVilles = int(villes.get())

            OffresCentrales = TableauOffres(self,nbreCentrales)
            DemandesVilles = TableauDemandes(self,nbreVilles)
            CoutsVillesCentrales=TableauCout(self)

            OffresCentrales.grid(row=8,pady=2)
            OffresCentrales.place(relx=0.11,rely=0.42,anchor="center")

            DemandesVilles.grid(row=10,pady=2)
            DemandesVilles.place(relx=0.89,rely=0.42,anchor="center")

            CoutsVillesCentrales.grid(row=9,pady=10)
            CoutsVillesCentrales.place(relx=0.5,rely=0.42,anchor="center")

            res = Result(self)
            res.place(relx=0.5,rely=0.83,anchor="center")

            def getValues(DemandesVilles,OffresCentrales,CoutsVillesCentrales,label):
                global nbreVilles, nbreCentrales, Couts, Offres , Demandes 
                
                DemandesVilles.get_input_array(label)
                OffresCentrales.get_input_array(label)
                CoutsVillesCentrales.get_cell_values(label)

                if len(Couts) == 0 or len(Offres) == 0 or len(Demandes) == 0:
                    print("One or more lists are empty")
                    label.configure(text="One or more lists are empty")
                    return
                x = PL5.Politique(Offres,Demandes,Couts)
                label.configure(str(x))
            
            def Pénaltie(label):
                global nbreVilles, nbreCentrales, Couts, Offres , Demandes, Pénaltie
                PenaltieVilles=TableauPénaltie(self,nbreVilles)
                PenaltieVilles.place(relx=0.89,rely=0.76,anchor="center")

                def ButtonAction(label):
                    global nbreVilles, nbreCentrales, Couts, Offres , Demandes, Pénaltie
                    PenaltieVilles.get_input_array(label)
                    if len(Pénaltie)==0 : 
                        return
                    else :
                        x = PL5.Politique_avec_penaltie(Pénaltie,Offres,Demandes,Couts)
                        label.configure(str(x))

                button = ctk.CTkButton(self, fg_color="#FFCB42", text="Valider Pénalties", command=lambda : ButtonAction(label),text_color="#000000")
                button.place(relx=0.71,rely=0.64,anchor="center")
                

            button = ctk.CTkButton(self, fg_color="#FFCB42",text_color="#000000", text=f"Find the best policy to meet the demands of {nbreVilles} city/cities.", command=lambda : getValues(DemandesVilles,OffresCentrales,CoutsVillesCentrales,res))
            button.place(relx=0.3,rely=0.64,anchor="center")

            button2 = ctk.CTkButton(self, text=f"Find the best policy in case of penalty", command=lambda : Pénaltie(res),fg_color="#FFCB42",text_color="#000000")
            button2.place(relx=0.55,rely=0.64,anchor="center")




        self.Valider = ctk.CTkButton(self,text="validate",command=lambda:getInput(self.Inputs.nbreCentralesEntry,self.Inputs.nbreVillesEntry),fg_color="#FFCB42",text_color="#000000")
        self.Valider.grid(row=7,column=3,pady=5)
        self.Valider.place(relx=0.5,rely=0.2,anchor="center")




app = App()
app.mainloop()