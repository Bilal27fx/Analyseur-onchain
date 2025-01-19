import tkinter as tk
from tkinter import messagebox
import webbrowser
from dexscrener_connection import get_specific_data_from_api

def open_link(url):
    """Ouvre un lien dans le navigateur."""
    webbrowser.open(url)

def show_token_data():
    """Affiche les données du token dans la même fenêtre, sous forme de tableau."""
    token_address = entry.get()  # Récupérer l'adresse du token depuis l'input
    if token_address:
        result = get_specific_data_from_api(token_address)  # Appel de l'API pour récupérer les données
        if isinstance(result, tuple):  # Si les données sont bien récupérées sous forme de tuple
            # Afficher les résultats sous forme de tableau
            for widget in result_frame.winfo_children():  # Efface les widgets précédents
                widget.destroy()

            headers = ["Token Name", "Chain", "Price in USD", "Market Cap", "Website", "Twitter", "24H Change"]
            data = [result[0], result[1], result[2], result[3], result[4], result[5], f"{result[6]} %"]

            # Affichage des en-têtes de tableau
            for col, header in enumerate(headers):
                header_label = tk.Label(result_frame, text=header, font=("Arial", 12, "bold"), bg="#555555", fg="yellow", padx=10, pady=5)
                header_label.grid(row=0, column=col, sticky="nsew")

            # Affichage des données dans le tableau
            for col, value in enumerate(data):
                if col == 4 or col == 5:  # Pour le Website et Twitter, rendre le texte cliquable
                    value_label = tk.Label(result_frame, text=value, font=("Arial", 12), bg="#333333", fg="white", padx=10, pady=5, cursor="hand2")
                    value_label.grid(row=1, column=col, sticky="nsew")
                    # Ajouter un lien cliquable
                    value_label.bind("<Button-1>", lambda e, url=value: open_link(url))
                else:
                    value_label = tk.Label(result_frame, text=value, font=("Arial", 12), bg="#333333", fg="white", padx=10, pady=5)
                    value_label.grid(row=1, column=col, sticky="nsew")

            # Rendre les colonnes ajustables
            for col in range(len(headers)):
                result_frame.grid_columnconfigure(col, weight=1)

            show_page(result_frame)  # Affiche la page des résultats
        else:
            messagebox.showerror("Erreur", result)  # Afficher une erreur si on ne récupère pas de données valides
    else:
        messagebox.showwarning("Entrée invalide", "Veuillez saisir une adresse de token.")  # Avertir l'utilisateur si l'adresse est vide

def show_page(page):
    """Affiche la page donnée (frame) et cache les autres pages."""
    page.tkraise()

def clear_input():
    """Réinitialise les champs de saisie et d'affichage."""
    entry.delete(0, tk.END)  # Efface l'entrée de l'adresse du token
    for widget in result_frame.winfo_children():  # Efface les widgets des résultats
        widget.destroy()
    show_page(start_frame)  # Retour à la première page (saisie du token)

# Créer la fenêtre principale de Tkinter
root = tk.Tk()

root.title("Analysateur de token Onchain")
root.geometry("600x400")  # Définir la taille de la fenêtre

# Définir la couleur de fond et le texte
root.config(bg="#333333")  # Fond gris foncé

# Créer un widget Frame pour chaque "page" ou "onglet"

# Première page : Saisie du token
start_frame = tk.Frame(root, bg="#333333")
start_frame.pack(fill="both", expand=True)

#header_label = tk.Label(start_frame, text="Analysateur de Token Onchain", font=("Arial", 18, "bold"), bg="#333333", fg="yellow")
#header_label.pack(pady=20)

entry = tk.Entry(start_frame, width=50, font=("Arial", 12), fg="yellow", bg="#555555", insertbackground="yellow")
entry.pack(pady=10)

button = tk.Button(start_frame, text="Obtenir les données", command=show_token_data, bg="#000000", fg="black", font=("Arial", 12, "bold"))
button.pack(pady=10)

clear_button = tk.Button(start_frame, text="Réinitialiser", command=clear_input, bg="#d9534f", fg="white", font=("Arial", 12, "bold"))
clear_button.pack(pady=10)

# Deuxième page : Affichage des résultats du token
result_frame = tk.Frame(root, bg="#333333")
result_frame.pack(fill="both", expand=True)

# Lancer la première page
show_page(start_frame)

# Lancer la boucle principale de Tkinter
root.mainloop()
