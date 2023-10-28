"""."""
from dataclasses import dataclass
import tkinter as tk
import customtkinter as ctk
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, TEXT, REAL


class App(ctk.CTk):
    """Application pour calculs du CNB 2020."""

    def __init__(self):
        super().__init__()

        self.title("CNB 2020")
        app_width, app_height, left_pos, top_pos = self.basic_window_geometry()
        self.geometry(f"{app_width}x{app_height}+{left_pos}+{top_pos}")

        self.loads_frame = ctk.CTkTabview(self, width=600)
        self.loads_frame.pack(side="left", fill="y")

        self.loads_frame.add("Charges permanentes")
        add_element_button = ctk.CTkButton(
            self.loads_frame.tab("Charges permanentes"),
            text="Ajouter élément structural",
            command=self.add_element,
        )
        add_element_button.pack(padx=20, pady=20, side="bottom", fill="x")
        self.elements_id = 0
        self.add_element()

        self.loads_frame.add("Charges d'utilisation")
        self.loads_frame.add("Neige")
        self.loads_frame.add("Vent")
        self.loads_frame.add("Séismes")

    def basic_window_geometry(self):
        """Ajuste les dimensions et position de la fenêtre de l'application."""

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        app_width = int(screen_width * 0.5)
        app_height = int(screen_height * 0.6)

        left_pos = int(screen_width / 2 - app_width / 2 + 300)
        top_pos = int(screen_height / 2 - app_height / 2)

        return app_width, app_height, left_pos, top_pos

    def add_element(self):
        """Créer un nouvel élément structural."""

        self.element_frame = ctk.CTkFrame(self.loads_frame.tab("Charges permanentes"))
        self.element_frame.pack(padx=10, pady=10, fill="x")

        self.elements_id += 1
        element_name = tk.StringVar(value=f"Élément{self.elements_id}")
        element_name_entry = ctk.CTkEntry(
            self.element_frame,
            width=80,
            textvariable=element_name,
        )
        element_name_entry.pack(padx=5, pady=5, side="left", fill="y")

        add_material_button = ctk.CTkButton(
            self.element_frame,
            text="+",
            command=self.add_material,
            width=28,
        )
        add_material_button.pack(padx=5, pady=5, side="bottom", anchor="w")
        self.add_material()

    def add_material(self):
        """Créer un nouveau matériau."""

        self.is_material = False
        self.material_frame = ctk.CTkFrame(self.element_frame)
        self.material_frame.pack(padx=5, pady=5, fill="x")

        @dataclass
        class DeadLoadsTable(declarative_base()):
            __tablename__ = "dead_loads"
            category: str = Column("category", TEXT)
            material: str = Column("material", TEXT, primary_key=True)
            session = sessionmaker(create_engine("sqlite:///loads.db"))()

        category_list = []
        categories = DeadLoadsTable.session.query(DeadLoadsTable.category).all()
        for i in categories:
            for j in i:
                if j not in category_list:
                    category_list.append(j)

        category_combobox = ctk.CTkComboBox(
            self.material_frame,
            values=category_list,
            command=self.select_category,
        )
        category_combobox.pack(padx=5, pady=5, side="left")
        self.select_category(category_combobox.get())

    def select_category(self, category):
        """Affiche les matériaux d'une catégorie.

        Args:
            category (str): Catégorie pour laquelle on souhaite afficher la liste des matériaux.
        """
        if self.is_material:
            self.material_combobox.destroy()
            self.is_material = False

        self.is_material = True

        @dataclass
        class DeadLoadsTable(declarative_base()):
            __tablename__ = "dead_loads"
            category: str = Column("category", TEXT)
            material: str = Column("material", TEXT, primary_key=True)
            session = sessionmaker(create_engine("sqlite:///loads.db"))()

        material_list = []
        materials = (
            DeadLoadsTable.session.query(DeadLoadsTable.material)
            .filter(DeadLoadsTable.category == str(category))
            .all()
        )
        for i in materials:
            for j in i:
                if j not in material_list:
                    material_list.append(j)

        self.material_combobox = ctk.CTkComboBox(
            self.material_frame,
            values=material_list,
        )
        self.material_combobox.pack(padx=5, pady=5, side="left")


if __name__ == "__main__":
    app = App()
    app.mainloop()
