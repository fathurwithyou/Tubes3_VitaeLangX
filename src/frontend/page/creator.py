import customtkinter as ctk
from PIL import Image
import os

class CreatorPage(ctk.CTkFrame):
    
    def __init__(self, parent, navigate_callback):
        super().__init__(
            parent,
            fg_color="#1B2B4C",  
            corner_radius=0
        )
        
        self.navigate_callback = navigate_callback
        self.pack(fill="both", expand=True)
        
        self.setup_creator_page()
    
    def setup_creator_page(self):
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(expand=True, fill="both")
        
        center_container = ctk.CTkFrame(main_container, fg_color="transparent")
        center_container.place(relx=0.5, rely=0.5, anchor="center")
        
        self.create_creator_content(center_container)
    
    def create_creator_content(self, parent):
        title_label = ctk.CTkLabel(
            parent,
            text="Meet the Minds Behind the Mission",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#DFCFC2"
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ctk.CTkLabel(
            parent,
            text="This app was crafted by a passionate team of developers with one goal: to make CV matching fast, fun, and reliable.",
            font=ctk.CTkFont(size=14),
            text_color="#FFFFFF",
            wraplength=600
        )
        subtitle_label.pack(pady=(0, 30))
        
        team_container = ctk.CTkFrame(parent, fg_color="transparent")
        team_container.pack()
        
        self.create_team_section(team_container)
    
    def create_team_section(self, parent):
        team_main_container = ctk.CTkFrame(parent, fg_color="transparent")
        team_main_container.pack()
        
        grid_container = ctk.CTkFrame(team_main_container, fg_color="transparent")
        grid_container.pack()

        grid_container.columnconfigure(0, weight=1)
        grid_container.columnconfigure(1, weight=2) 
        grid_container.columnconfigure(2, weight=1)

        soni_container = ctk.CTkFrame(grid_container, fg_color="transparent")
        soni_container.grid(row=0, column=0, padx=20, pady=10, sticky="")
        
        soni_name = ctk.CTkLabel(
            soni_container,
            text="Ahmad Wicaksono",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#DFCFC2"
        )
        soni_name.pack()
        
        soni_nim = ctk.CTkLabel(
            soni_container,
            text="13523121",
            font=ctk.CTkFont(size=14),
            text_color="#FFFFFF"
        )
        soni_nim.pack()

        team_photo = self.create_team_photo(grid_container)
        
        if team_photo:
            team_photo.grid(row=0, column=1, padx=10, pady=10)
        else:
            self.create_photo_placeholder(grid_container)

        fathur_container = ctk.CTkFrame(grid_container, fg_color="transparent")
        fathur_container.grid(row=0, column=2, padx=20, pady=10, sticky="")
        
        fathur_name = ctk.CTkLabel(
            fathur_container,
            text="M. Fathur Rizky",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#DFCFC2"
        )
        fathur_name.pack()
        
        fathur_nim = ctk.CTkLabel(
            fathur_container,
            text="13523100",
            font=ctk.CTkFont(size=14),
            text_color="#FFFFFF"
        )
        fathur_nim.pack()

        dinda_container = ctk.CTkFrame(grid_container, fg_color="transparent")
        dinda_container.grid(row=1, column=1, pady=(5, 0))
        
        dinda_name = ctk.CTkLabel(
            dinda_container,
            text="Adinda Putri",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#DFCFC2"
        )
        dinda_name.pack()
        
        dinda_nim = ctk.CTkLabel(
            dinda_container,
            text="13523071",
            font=ctk.CTkFont(size=14),
            text_color="#FFFFFF"
        )
        dinda_nim.pack()
    
    def create_team_photo(self, parent):
        photo_paths = [
            "assets/trio.png",
            os.path.join(".", "assets", "trio.png"),
            os.path.join("..", "assets", "trio.png"),
            os.path.join("frontend", "assets", "trio.png"),
        ]
        
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            photo_paths.extend([
                os.path.join(current_dir, "assets", "trio.png"),
                os.path.join(current_dir, "..", "assets", "trio.png"),
                os.path.join(current_dir, "..", "..", "assets", "trio.png"),
            ])
        except:
            pass

        for photo_path in photo_paths:
            if os.path.exists(photo_path):
                try:
                    photo_image = Image.open(photo_path)
                    
                    photo_ctk_image = ctk.CTkImage(
                        light_image=photo_image,
                        dark_image=photo_image,
                        size=(400, 300)  
                    )
                    
                    photo_label = ctk.CTkLabel(
                        parent,
                        image=photo_ctk_image,
                        text=""
                    )
                    
                    return photo_label
                except Exception as e:
                    continue
        
        return None