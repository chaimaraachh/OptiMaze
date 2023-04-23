import tkinter as tk
from tkinter import ttk
import os

# Function to open new widget (replace with desired functionality)
def open_widget():
    new_window = tk.Toplevel()
    new_window.title("New Widget")
    new_window.geometry("300x200")
    tk.Label(new_window, text="New widget content").pack(pady=20)

# Main application
class OptiMazeApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("OptiMaze")
        self.configure(bg="#277BC0")

        # Title
        title = tk.Label(self, text="OptiMaze", bg="#277BC0", fg="white", font=("Arial", 30))
        title.pack(pady=20)

        # Card frame
        card_frame = tk.Frame(self, bg="#277BC0")
        card_frame.pack()

        # Card creation function
        def create_card(parent, icon_path, text):
            card = ttk.Frame(parent, padding=30, relief="groove", style="Card.TFrame")
            card.grid(column=0, row=0, padx=5, pady=0)

            icon = tk.PhotoImage(master=self, file=icon_path)
            icon_label = tk.Label(card, image=icon, bg="#FFEBEB")
            icon_label.image = icon
            icon_label.pack(pady=1)

            label = tk.Label(card, text=text, bg="#FFEBEB", fg="#277BC0", font=("Arial", 10), wraplength=180)
            label.pack()

            button = tk.Button(card, text="Essayer", command=open_widget, bg="#FFCB42", fg="white", font=("Arial", 9))
            button.pack(pady=5)

            return card

        # Create cards
        assets_folder = "assets"
        icon_paths = [
            os.path.join(assets_folder, 'agriculture.png'),
            os.path.join(assets_folder, 'oil.png'),
            os.path.join(assets_folder, 'networking.png'),
            os.path.join(assets_folder, '3d-shoes.png'),
            os.path.join(assets_folder, 'eco-house.png'),
            os.path.join(assets_folder, 'distribution.png'),
            os.path.join(assets_folder, 'company.png'),
            os.path.join(assets_folder, 'road.png'),
            os.path.join(assets_folder, 'pin.png')
        ]

        texts = ["PL1 : Gestion optimale d’une zone agricole  ",
                 "PL2 : Mixage en production pétrolière",
                 "PL3 : Planification des besoins en ressources humaines",
                 "PL4 :  Gestion de la production",
                 "PL5: La production d’électricité",
                 "PL6 :   Distribution de produit",
                 "PL7 : Affectation optimale de ressources",
                 "    PL8    :    Remplacement d’équipement    ",
                 "PL9 : Localisation d’usine et de dépôts et planification logistique"]


        for i in range(3):
            for j in range(3):
                index = i * 3 + j
                icon_path = icon_paths[index]
                text = texts[index]
                card = create_card(card_frame, icon_path, text)
                card.grid(row=i, column=j, padx=10, pady=5)



# Custom card style
style = ttk.Style()
style.configure("Card.TFrame", background="#FFEBEB")

app = OptiMazeApp()
app.geometry("800x700")
app.mainloop()
