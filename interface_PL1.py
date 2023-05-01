from typing import Optional, Tuple, Union
import customtkinter as ctk 
import tkinter as tk
import PL1_Partie_A
import gurobipy as gp
from gurobipy import GRB
import PL1_Partie_B

ctk.set_appearance_mode("light")

ctk.set_default_color_theme("custom.json")

superficie = 0
MainOeuvre=0
eau=0
heuresMachine=0
cultures=0
prixMachine=0
prixEau=0
Rendement=[]
PrixVente=[]
NbreOuvriers=[]
TempsMachine=[]
Eau=[]
SalaireAnnuel=[]
FG=[] 
demandeMin = 0
cultureMin = 0

class InputRow(ctk.CTkFrame):
    def __init__(self, master, name, value):
        super().__init__(master)
        self.grid_columnconfigure((0,2),weight=2)

        self.label = ctk.CTkLabel(self,text=name, fg_color='transparent')
        self.entry = ctk.CTkEntry(self,bg_color='transparent')

        self.label.grid(row=0 , column = 0,sticky="ew")
        self.entry.grid(row = 0 , column = 3,sticky="ew",padx=5)
        self.entry.insert(0, value)
    def getInput(self):
        input = float(self.entry.get())
        return (input)

class InputFrame(ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master)
        self.grid_columnconfigure(0,weight=1)
        self.title=ctk.CTkLabel(self,text="Choose the system's parameters :")
        self.title.grid(row=0, sticky="ew",pady=5)
        self.row1=InputRow(self,"Maximum Area","1000")
        self.row1.grid(row=1,sticky="ew",pady=5)
        self.row2=InputRow(self,"Maximum labor force.","3000")
        self.row2.grid(row=2,sticky="ew",pady=5)
        self.row3=InputRow(self,"Maximum irrigation water","25000000")
        self.row3.grid(row=3,sticky="ew",pady=5)
        self.row4=InputRow(self,"Number of machine hours","24000")
        self.row4.grid(row=4,sticky="ew" ,pady=5)
        self.row5=InputRow(self,"Number of crops","2")
        self.row5.grid(row=5,sticky="ew" ,pady=5)
        self.row6=InputRow(self,"Machine Hour's price :","30")
        self.row6.grid(row=6,sticky="ew" ,pady=5)
        self.row7=InputRow(self,"Water price","0.1")
        self.row7.grid(row=7,sticky="ew" ,pady=5)

    def getInputs(self):
        superficie = int(self.row1.getInput())
        MainOeuvre = int(self.row2.getInput())
        eau = int(self.row3.getInput())
        heuresMachine = int(self.row4.getInput())
        cultures = int(self.row5.getInput())
        prixMachine = int(self.row6.getInput())
        prixEau = float(self.row7.getInput())
        return superficie , MainOeuvre, eau, heuresMachine,cultures,prixMachine,prixEau



class OutputRow(ctk.CTkFrame):
    def __init__(self, master,question, commande):
        super().__init__(master, width=600)
        self.Button=ctk.CTkButton(self,fg_color="#FFCB42",text_color="#000000",command=commande, text=question, width=300)
        self.Button.grid(row=0, sticky="ew", pady=5)
    
    def update(self):
        print(1)


class OutputFrame(ctk.CTkScrollableFrame):
    global superficie , MainOeuvre, eau, heuresMachine,cultures, Rendement,PrixVente,NbreOuvriers,TempsMachine,Eau,SalaireAnnuel,FG,prixMachine,prixEau, demandeMin, cultureMin
    
    def __init__(self, master, width = 600):
        super().__init__(master, width=900, height=300)
        self.grid_columnconfigure(0, weight=2)

        def setLabel(label, texte):
            label.configure(text=texte)


        self.label=ctk.CTkLabel(self,text="",font=("Arial", 18))
             
        def benefice(Rendement,Prix_Vente,nbre_Ovriers,Heures_Machine,Eau,Salaire_ouvrier,gestion,prixEau,prixMachine,label,cultures):
            for param in [Rendement,Prix_Vente,nbre_Ovriers,Heures_Machine,Eau,Salaire_ouvrier,gestion]:
                if len(param) == 0:
                    setLabel(label,"\n One or both tables aren't fully filled ")
                    return
            res = "The profit per hectare is :"
            for i in range(cultures):
                benefice = PL1_Partie_A.calcul_Bénéfice(Rendement[i],Prix_Vente[i],nbre_Ovriers[i],Heures_Machine[i],Eau[i],Salaire_ouvrier[i],gestion[i],prixEau,prixMachine)
                res += "\n" + str(benefice) + "for the crop " + str(i+1) 

            setLabel(label , res)
            return (1)
        
        def résolution(superficie, main_oeuvre, eau_irrigation, heures_machine, nbre_cultures, L_Rendement, L_Prix_Vente, L_nbre_Ovriers, L_Heures_Machine, L_Eau, L_Salaire_ouvrier, L_gestion, prix_eau, prix_machine , label):
            for param in [L_Rendement, L_Prix_Vente, L_nbre_Ovriers, L_Heures_Machine, L_Eau, L_Salaire_ouvrier, L_gestion]:
                if len(param) == 0:
                    setLabel(label,"\n One or both tables aren't fully filled ")
                    return
            benefice_total, recommandation = PL1_Partie_A.Maximiser_Profit(superficie, main_oeuvre,eau_irrigation, heures_machine, nbre_cultures, tuple(L_Rendement), tuple(L_Prix_Vente), tuple(L_nbre_Ovriers), tuple(L_Heures_Machine), tuple(L_Eau), tuple(L_Salaire_ouvrier), tuple(L_gestion), prix_eau, prix_machine)
            text = "The total profil is : " + str(benefice_total) + "\n"
            text += "The best policy is : " + recommandation
            setLabel(label,text)

        def Blé(label):
            global  superficie , MainOeuvre, eau, heuresMachine,cultures, Rendement,PrixVente,NbreOuvriers,TempsMachine,Eau,SalaireAnnuel,FG,prixMachine,prixEau
            DemandeMinimale = InputRow(self,"minimal demand : ", "37500")
            culturesMinimale = InputRow(self,"crop in question : ","1")

            DemandeMinimale.grid(row=5, pady=2)
            culturesMinimale.grid(row=6, pady=2)

            def résolution(superficie, main_oeuvre, eau_irrigation, heures_machine, nbre_cultures, L_Rendement, L_Prix_Vente, L_nbre_Ovriers, L_Heures_Machine, L_Eau, L_Salaire_ouvrier, L_gestion, prix_eau, prix_machine , label, frame1 , frame2):

                global demandeMin, cultureMin
                demandeMin = frame1.getInput()
                cultureMin = int(frame2 . getInput())
                print(demandeMin,cultureMin)

                for param in [L_Rendement, L_Prix_Vente, L_nbre_Ovriers, L_Heures_Machine, L_Eau, L_Salaire_ouvrier, L_gestion]:
                    if len(param) == 0:
                        setLabel(label,"\n One or both tables aren't fully filled ")
                        return
                
                recommandation = PL1_Partie_B.Maximiser_Profit_dem_min(superficie, main_oeuvre,eau_irrigation, heures_machine, nbre_cultures, tuple(L_Rendement), tuple(L_Prix_Vente), tuple(L_nbre_Ovriers), tuple(L_Heures_Machine), tuple(L_Eau), tuple(L_Salaire_ouvrier), tuple(L_gestion), prix_eau, prix_machine, demandeMin,cultureMin)
                setLabel(label,recommandation)

            valider=ctk.CTkButton(self,fg_color="#FFCB42",text_color="#000000",text="validate",command=lambda : résolution(superficie,MainOeuvre,eau,heuresMachine, cultures, Rendement, PrixVente, NbreOuvriers, TempsMachine, Eau, SalaireAnnuel, FG, prixEau, prixMachine ,self.label,DemandeMinimale,culturesMinimale))
            valider.grid(row=7, pady=2)

        def résolution_Embauche(superficie, main_oeuvre, eau_irrigation, heures_machine, nbre_cultures, L_Rendement, L_Prix_Vente, L_nbre_Ovriers, L_Heures_Machine, L_Eau, L_Salaire_ouvrier, L_gestion, prix_eau, prix_machine , label):

                for param in [L_Rendement, L_Prix_Vente, L_nbre_Ovriers, L_Heures_Machine, L_Eau, L_Salaire_ouvrier, L_gestion]:
                    if len(param) == 0:
                        setLabel(label,"\n One or both tables aren't fully filled ")
                        return
                    
                recommandation = PL1_Partie_B.Embauche(superficie, main_oeuvre,eau_irrigation, heures_machine, nbre_cultures, tuple(L_Rendement), tuple(L_Prix_Vente), tuple(L_nbre_Ovriers), tuple(L_Heures_Machine), tuple(L_Eau), tuple(L_Salaire_ouvrier), tuple(L_gestion), prix_eau, prix_machine)
                setLabel(label,recommandation)

        self.Button1=OutputRow(self,f"Determine the profit per hectare for the crops", lambda: benefice(Rendement,PrixVente,NbreOuvriers,TempsMachine,Eau,SalaireAnnuel,FG, prixEau, prixMachine, self.label, cultures))
        
        self.Button2=OutputRow(self,"Resolve to maximize the profit",lambda: résolution(superficie,MainOeuvre,eau,heuresMachine, cultures, Rendement, PrixVente, NbreOuvriers, TempsMachine, Eau, SalaireAnnuel, FG, prixEau, prixMachine ,self.label) )

        self.Button3=OutputRow(self,"Modifications to meet a minimum demand for a specific crop", lambda : Blé(self.label))

        self.Button4=OutputRow(self,"Hire all the labor force", lambda: résolution_Embauche(superficie,MainOeuvre,eau,heuresMachine, cultures, Rendement, PrixVente, NbreOuvriers, TempsMachine, Eau, SalaireAnnuel, FG, prixEau, prixMachine ,self.label) )
        
        self.title=ctk.CTkLabel(self,text="Resolution :")
        self.title.grid(row=0, sticky="ew")

        self.Button1.grid(row=1)
        self.Button2.grid(row=3)
        self.Button3.grid(row=4)
        self.label.grid(row=9, pady = 5)
        self.Button4.grid(row=8)

class InputFrameDynamic(ctk.CTkScrollableFrame):
    def __init__(self, master, nbreCultures):
        global Rendement,PrixVente,NbreOuvriers,TempsMachine,Eau,SalaireAnnuel,FG ,prixMachine,prixEau

        super().__init__(master, 1200, 200)
        self.Rendement = []
        self.PrixVente = []
        self.NbreOuvriers = []
        self.TempsMachine = []
        self.Eau = []
        self.SalaireAnnuel = []
        self.FG = []
        i = 0

        R_label = ctk.CTkLabel(self, text="Output:")
        R_label.grid(row=0, column=1, padx=5, pady=5)

        Pv_label = ctk.CTkLabel(self, text="Sale Price:")
        Pv_label.grid(row=0, column=2, padx=5, pady=5)
        
        NbreO_label = ctk.CTkLabel(self, text="Worker Number:")
        NbreO_label.grid(row=0, column=3, padx=5, pady=5)

        Tmachine_label = ctk.CTkLabel(self, text="Machine hours:")
        Tmachine_label.grid(row=0, column=4, padx=5, pady=5)

        Eau_label = ctk.CTkLabel(self, text="Used water:")
        Eau_label.grid(row=0, column=5, padx=5, pady=5)

        Salaire_label = ctk.CTkLabel(self, text="Annual worker wage:")
        Salaire_label.grid(row=0, column=6, padx=5, pady=5)

        FG_label = ctk.CTkLabel(self, text="Management fees :")
        FG_label.grid(row=0, column=7, padx=5, pady=5)
        

        for i in range(nbreCultures):
            Culture_label = ctk.CTkLabel(self, text=f"Crop {i+1}:",)
            Culture_label.grid(row=i+1, column=0, padx=5, pady=5)

            entry = ctk.CTkEntry(self)
            entry.grid(row=i+1, column=1, padx=5, pady=5)

            entry2 = ctk.CTkEntry(self)
            entry2.grid(row=i+1, column=2, padx=5, pady=5)

            entry3 = ctk.CTkEntry(self)
            entry3.grid(row=i+1, column=3, padx=5, pady=5)

            entry4 = ctk.CTkEntry(self)
            entry4.grid(row=i+1, column=4, padx=5, pady=5)

            entry5 = ctk.CTkEntry(self)
            entry5.grid(row=i+1, column=5, padx=5, pady=5)

            entry6 = ctk.CTkEntry(self)
            entry6.grid(row=i+1, column=6, padx=5, pady=5)

            entry7 = ctk.CTkEntry(self)
            entry7.grid(row=i+1, column=7, padx=5, pady=5)

            self.Rendement.append(entry)
            self.PrixVente.append(entry2)
            self.NbreOuvriers.append(entry3)
            self.TempsMachine.append(entry4)
            self.Eau.append(entry5)
            self.SalaireAnnuel.append(entry6)
            self.FG.append(entry7)

    def get_input_array(self):
            Rendement = [int(x.get()) for x in self.Rendement]
            PrixVente = [int(x.get()) for x in self.PrixVente]
            NbreOuvriers = [int(x.get()) for x in self.NbreOuvriers]
            TempsMachine = [int(x.get()) for x in self.TempsMachine]
            Eau = [int(x.get()) for x in self.Eau]
            SalaireAnnuel = [int(x.get()) for x in self.SalaireAnnuel]
            FG = [int(x.get()) for x in self.FG]

            print(Rendement)

            return Rendement, PrixVente, NbreOuvriers, TempsMachine, Eau, SalaireAnnuel, FG

class InputOutput(ctk.CTkFrame):
        global superficie , MainOeuvre, eau, heuresMachine,cultures,prixMachine,prixEau

        def __init__(self, master):
            super().__init__(master)
            self.grid_columnconfigure((1, 2), weight=1)

            self.inputFrame=InputFrame(self)
            self.inputFrame.grid(row=1, column=0)

            self.outputFrame=OutputFrame(self)
            self.outputFrame.grid(column=2 , row=1)
        def getInputs(self):
            superficie , MainOeuvre, eau, heuresMachine,cultures,prixMachine,prixEau = self.inputFrame.getInputs()
            return superficie , MainOeuvre, eau, heuresMachine,cultures,prixMachine,prixEau

class App(ctk.CTk):
    def __init__(self):
        global superficie , MainOeuvre, eau, heuresMachine,cultures, Rendement,PrixVente,NbreOuvriers,TempsMachine,Eau,SalaireAnnuel,FG , prixMachine,prixEau
        super().__init__()

        self.title("PL1")
        self.geometry("1200x650")
        self.grid_columnconfigure((3,0), weight = 1)

        self.InputOutput=InputOutput(self)
        self.InputOutput.grid(row=0, sticky = "ew")

        def validerInput1(frame):
            global superficie , MainOeuvre, eau, heuresMachine,cultures,prixMachine,prixEau
            superficie , MainOeuvre, eau, heuresMachine,cultures,prixMachine,prixEau = frame.getInputs()
            print(superficie , MainOeuvre, eau, heuresMachine,cultures,prixMachine,prixEau)
            dynamicInput = InputFrameDynamic(self, cultures)
            dynamicInput.grid(row=2 , pady = 10)
            def actionButton(frame):
                global Rendement,PrixVente,NbreOuvriers,TempsMachine,Eau,SalaireAnnuel,FG
                Rendement,PrixVente,NbreOuvriers,TempsMachine,Eau,SalaireAnnuel,FG = frame.get_input_array()
                print(Rendement,PrixVente,NbreOuvriers,TempsMachine,Eau,SalaireAnnuel,FG)

            inputButton2=ctk.CTkButton(self,fg_color="#FFCB42",text_color="#000000", text="Validate the table", command=lambda: actionButton(dynamicInput))
            inputButton2.grid(row=3, pady=2)
            return (superficie , MainOeuvre, eau, heuresMachine,cultures,prixMachine,prixEau)

        
        self.inputButton=ctk.CTkButton(self, fg_color="#FFCB42",text_color="#000000",text="Validate the area, workforce, water, machine hours, and number of crops.", command=lambda: validerInput1(self.InputOutput))
        self.inputButton.grid(row=1, column=0, pady=10)

        


app = App()
app.mainloop()

app.mainloop()