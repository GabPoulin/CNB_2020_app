import customtkinter as ctk
from dataclasses import dataclass
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, TEXT, REAL


class App(ctk.CTk):
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
        add_element_button.pack(padx=20, pady=20, fill="x")
        self.add_element()

        self.loads_frame.add("Charges d'utilisation")
        self.loads_frame.add("Neige")
        self.loads_frame.add("Vent")
        self.loads_frame.add("Séismes")

    def basic_window_geometry(self):
        """Ajuster les dimensions et position de la fenêtre."""

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        app_width = int(screen_width * 0.5)
        app_height = int(screen_height * 0.6)

        left_pos = int(screen_width / 2 - app_width / 2 + 300)
        top_pos = int(screen_height / 2 - app_height / 2)

        return app_width, app_height, left_pos, top_pos

    def add_element(self):
        """Créer un nouvel élément structural."""

        element_frame = ctk.CTkFrame(self.loads_frame.tab("Charges permanentes"))
        element_frame.pack(padx=10, pady=10, fill="x")

        element_name = ctk.CTkEntry(
            element_frame,
            width=80,
            placeholder_text="Élément",
        )
        element_name.pack(padx=5, pady=5, side="left", fill="y")

        def add_material():
            """Créer un nouveau matériau."""

            @dataclass
            class DeadLoadsTable(declarative_base()):
                """Se connecte à la table dead_loads de loads.db."""

                __tablename__ = "dead_loads"
                category: str = Column("category", TEXT)
                material: str = Column("material", TEXT, primary_key=True)
                load: str = Column("load", REAL)
                unit: str = Column("unit", TEXT)
                session = sessionmaker(create_engine("sqlite:///loads.db"))()

            category_list = []
            categ = DeadLoadsTable.session.query(DeadLoadsTable.category).all()
            for i in categ:
                for j in i:
                    if j not in category_list:
                        category_list.append(j)

            material_frame = ctk.CTkFrame(element_frame)
            material_frame.pack(padx=5, pady=5, fill="x")
            material_category = ctk.CTkComboBox(material_frame, values=category_list)
            material_category.pack(padx=5, pady=5, side="left")

            material_list = []
            mat = (
                DeadLoadsTable.session.query(DeadLoadsTable.material)
                .filter(DeadLoadsTable.category == str(material_category.get()))
                .all()
            )
            for i in mat:
                for j in i:
                    if j not in material_list:
                        material_list.append(j)

            material_material = ctk.CTkComboBox(material_frame, values=material_list)
            material_material.pack(padx=5, pady=5, side="left")

        add_material_button = ctk.CTkButton(
            element_frame,
            text="Ajouter matériau",
            command=add_material,
        )
        add_material_button.pack(padx=5, pady=5, side="bottom", fill="x")
        add_material()


if __name__ == "__main__":
    app = App()
    app.mainloop()
