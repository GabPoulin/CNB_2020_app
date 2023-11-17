"""."""
from dataclasses import dataclass
import tkinter as tk
import customtkinter as ctk
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, TEXT, REAL


class App(ctk.CTk):
    """CNB 2020."""

    def __init__(self):
        super().__init__()

        ctk.set_default_color_theme("app_color_theme.json")
        self.title("CNB 2020")
        self.set_window_geometry()

        self.loads_tabview = ctk.CTkTabview(self)
        self.loads_tabview.pack(padx=5, pady=5, fill="both")

        self.loads_tabview.add("D")
        self.deadload_tab()
        self.loads_tabview.add("L")
        self.loads_tabview.add("S")
        self.loads_tabview.add("W")
        self.loads_tabview.add("E")

    def set_window_geometry(self):
        """Ajuste les dimensions et position de la fenêtre de l'application."""

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        app_width = int(screen_width * 0.4)
        app_height = int(screen_height * 0.6)

        left_pos = int(screen_width / 2 - app_width / 2)
        top_pos = int(screen_height / 3 - app_height / 3)

        self.geometry(f"{app_width}x{app_height}+{left_pos}+{top_pos}")

    def deadload_tab(self):
        self.input_frame = ctk.CTkFrame(self.loads_tabview.tab("D"))
        self.input_frame.pack(padx=5, pady=30, side="left", fill="y")

        self.output_frame = ctk.CTkFrame(self.loads_tabview.tab("D"))
        self.output_frame.pack(padx=5, pady=5, side="left", fill="both")
        vertical_line = ctk.CTkFrame(self.output_frame, width=5, height=600)
        vertical_line.pack(padx=5, pady=5, fill="y")

        add_element_button = ctk.CTkButton(
            self.input_frame,
            text="Nouvel élément structural",
            command=self.add_element,
        )
        add_element_button.pack(padx=5, pady=5, ipady=30, fill="x")

        add_material_button = ctk.CTkButton(
            self.input_frame,
            text="Ajouter matériau",
            command=self.add_material,
        )
        add_material_button.pack(padx=5, pady=5, ipady=30, fill="x")

        horizontal_line = ctk.CTkFrame(self.input_frame, width=300, height=5)
        horizontal_line.pack(padx=5, pady=5)

        element_name = tk.StringVar(value=f"Nom de l'élément structural")
        element_name_entry = ctk.CTkEntry(
            self.input_frame,
            textvariable=element_name,
            width=200,
        )
        element_name_entry.pack(padx=5, pady=5, anchor="w")

        self.select_category()

    def select_category(self):
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
            self.input_frame,
            values=category_list,
            command=self.select_material,
        )
        category_combobox.pack(padx=5, pady=5, fill="x")

        self.is_material = False
        self.select_material(category_combobox.get())

    def select_material(self, category):
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

        self.material_combobox = ctk.CTkComboBox(self.input_frame, values=material_list)
        self.material_combobox.pack(padx=5, pady=5, fill="x")

    def add_element(self):
        """Créer un nouvel élément structural."""

        pass

    def add_material(self):
        """Créer un nouvel élément structural."""

        pass


if __name__ == "__main__":
    app = App()
    app.mainloop()
