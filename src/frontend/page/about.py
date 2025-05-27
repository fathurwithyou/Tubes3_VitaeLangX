import customtkinter as ctk
from PIL import Image
import os

class AboutPage(ctk.CTkFrame):
    
    def __init__(self, parent, navigate_callback):
        super().__init__(
            parent,
            fg_color="#1B2B4C", 
            corner_radius=0
        )
        
        self.navigate_callback = navigate_callback
        self.pack(fill="both", expand=True)
        
        self.setup_about_page()
    
    def setup_about_page(self):
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color="#334D7A",
            scrollbar_button_hover_color="#4A5D8A"
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.create_about_content()
    
    def create_about_content(self):
        self.create_how_it_works_section()
        
        ctk.CTkLabel(self.scrollable_frame, text="", height=40).pack()
        
        self.create_bearlock_section()
        
        ctk.CTkLabel(self.scrollable_frame, text="", height=40).pack()
        
        self.create_algorithms_section()
        
        ctk.CTkLabel(self.scrollable_frame, text="", height=40).pack()
    
    def create_how_it_works_section(self):
        title_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="How it Works",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#DFCFC2"
        )
        title_label.pack(pady=(50, 15))
        
        description_text = """At CV Detective, we combine speed and intelligence to match resumes with your target
keywords. Our engine leverages a blend of exact and fuzzy matching algorithms,
so whether it's a perfect hit or a near miss, you'll still get the best candidates."""
        
        description_label = ctk.CTkLabel(
            self.scrollable_frame,
            text=description_text,
            font=ctk.CTkFont(size=14),
            text_color="#FFFFFF",
            wraplength=700,
            justify="center"
        )
        description_label.pack(pady=(0, 20))
    
    def create_bearlock_section(self):
        bearlock_title = ctk.CTkLabel(
            self.scrollable_frame,
            text="Meet Bearlock Holmes",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#DFCFC2"
        )
        bearlock_title.pack(pady=(0, 20))
        
        bearlock_image = self.create_bearlock_image()
        if bearlock_image:
            bearlock_image.pack(pady=(0, 20))
        else:
            placeholder = ctk.CTkFrame(
                self.scrollable_frame,
                width=200,
                height=200,
                fg_color="#2D3E5F",
                corner_radius=15
            )
            placeholder.pack(pady=(0, 20))
            placeholder.pack_propagate(False)
            
            placeholder_label = ctk.CTkLabel(
                placeholder,
                text="Bearlock\nHolmes",
                font=ctk.CTkFont(size=20),
                text_color="#FFFFFF",
                justify="center"
            )
            placeholder_label.pack(expand=True)
        
        bearlock_text = """Say hello to Bearlock Holmes, your loyal search companion!
He's on a mission to help you sniff out the best CVs from a stack of suspects.
Every search you make, he's right there with you, magnifying glass in paw, ready
to highlight the clues you need."""
        
        bearlock_description = ctk.CTkLabel(
            self.scrollable_frame,
            text=bearlock_text,
            font=ctk.CTkFont(size=14),
            text_color="#FFFFFF",
            wraplength=600,
            justify="center"
        )
        bearlock_description.pack(pady=(0, 20))
    
    def create_algorithms_section(self):
        """Create the 'Algorithms We Use' section with cards"""
        algo_title = ctk.CTkLabel(
            self.scrollable_frame,
            text="Algorithms We Use",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#DFCFC2"
        )
        algo_title.pack(pady=(0, 30))
        
        cards_container = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        cards_container.pack(pady=(0, 20))
        
        cards_container.columnconfigure(0, weight=1)
        cards_container.columnconfigure(1, weight=1)
        cards_container.columnconfigure(2, weight=1)
        
        algorithms = [
            {
                "title": "Knuth-Morris-Pratt",
                "description": "Think of it as a detective that remembers where it's been, never checking the same clue twice."
            },
            {
                "title": "Boyer-Moore", 
                "description": "It's like flipping through pages backwards to jump straight to the clue."
            },
            {
                "title": "Levenshtein",
                "description": "Ideal when you're not sure if it was \"ReactJS\" or \"React.js\", we'll still find it."
            }
        ]
        
        for i, algo in enumerate(algorithms):
            self.create_algorithm_card(cards_container, algo, i)
    
    def create_algorithm_card(self, parent, algo_data, column):
        """Create individual algorithm card with fixed dimensions"""
        card = ctk.CTkFrame(
            parent,
            fg_color="#2D3E5F",
            width=200,  
            height=140, 
            corner_radius=15,
            border_width=2,
            border_color="#F9DFDC"
        )
        card.grid(row=0, column=column, padx=20, pady=15, sticky="") 
        card.grid_propagate(False)  
        card.pack_propagate(False) 
        
        title_label = ctk.CTkLabel(
            card,
            text=algo_data["title"],
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#DFCFC2"
        )
        title_label.pack(pady=(15, 10))
        
        desc_label = ctk.CTkLabel(
            card,
            text=algo_data["description"],
            font=ctk.CTkFont(size=13),
            text_color="#FFFFFF",
            wraplength=180,
            justify="center"
        )
        desc_label.pack(pady=(0, 15), padx=10)
    
    def create_bearlock_image(self):
        image_paths = [
            "assets/bearlock.png",
            os.path.join(".", "assets", "bearlock.png"),
            os.path.join("..", "assets", "bearlock.png"),
            os.path.join("frontend", "assets", "bearlock.png"),
        ]
        
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_paths.extend([
                os.path.join(current_dir, "assets", "bearlock.png"),
                os.path.join(current_dir, "..", "assets", "bearlock.png"),
                os.path.join(current_dir, "..", "..", "assets", "bearlock.png"),
            ])
        except:
            pass
        
        for image_path in image_paths:
            if os.path.exists(image_path):
                try:
                    bearlock_image = Image.open(image_path)
                    
                    bearlock_ctk_image = ctk.CTkImage(
                        light_image=bearlock_image,
                        dark_image=bearlock_image,
                        size=(180, 180) 
                    )
                    
                    image_label = ctk.CTkLabel(
                        self.scrollable_frame,
                        image=bearlock_ctk_image,
                        text=""
                    )
                    
                    return image_label
                except Exception as e:
                    continue
        
        return None