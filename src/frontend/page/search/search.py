import customtkinter as ctk
from PIL import Image
import os
from backend import Settings

class SearchPage(ctk.CTkFrame):
    
    def __init__(self, parent, navigate_callback, backend_manager):
        super().__init__(
            parent,
            fg_color="#1B2B4C",
            corner_radius=0
        )
        
        self.navigate_callback = navigate_callback
        self.pack(fill="both", expand=True)
        
        self.selected_algorithm = ctk.StringVar(value="KMP") # Default to KMP to match backend options
        # Top matches entry now uses Settings as default
        self.top_matches_value = ctk.StringVar(value=str(Settings.TOP_N_MATCHES))
        
        self.setup_search_page()
    
    def setup_search_page(self):
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        content_container = ctk.CTkFrame(main_container, fg_color="transparent")
        content_container.place(relx=0.5, rely=0.5, anchor="center")
        
        self.create_back_button_centered(main_container)
        
        self.create_header_section(content_container)
        
        self.create_search_content(content_container)
        
        self.create_search_button(content_container)
    
    def create_back_button_centered(self, parent):
        back_button = ctk.CTkButton(
            parent,
            text="←",
            font=ctk.CTkFont(size=20, weight="bold"),
            width=60,
            height=40,
            corner_radius=8,
            border_width=2,
            border_color="#DFCFC2", 
            fg_color="#334D7A",
            hover_color="#1B2B4C", 
            text_color="#DFCFC2",
            command=lambda: self.navigate_callback("opening")
        )
        back_button.place(x=50, y=30) 
    
    def create_header_section(self, parent):
        header_container = ctk.CTkFrame(parent, fg_color="transparent")
        header_container.pack(pady=(0, 20))
        
        header_content = ctk.CTkFrame(header_container, fg_color="transparent")
        header_content.pack()
        
        left_image = ctk.CTkFrame(header_content, fg_color="transparent")
        left_image.pack(side="left", padx=(0, 20))
        
        self.create_bearlock_sad_image(left_image)
        
        center_text = ctk.CTkFrame(header_content, fg_color="transparent")
        center_text.pack(side="left")
        
        title_label = ctk.CTkLabel(
            center_text,
            text="Search and Match",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#DFCFC2"
        )
        title_label.pack()
        
        description_text = """Input the keywords you're looking for, choose the matching algorithm, and let our
system reveal the most relevant candidates, exact or approximate."""
        
        description_label = ctk.CTkLabel(
            center_text,
            text=description_text,
            font=ctk.CTkFont(size=14),
            text_color="#FFFFFF",
            justify="center"
        )
        description_label.pack(pady=(10, 0))
        
        right_image = ctk.CTkFrame(header_content, fg_color="transparent")
        right_image.pack(side="right", padx=(20, 0))
        
        self.create_asset3_image(right_image)
    
    def create_search_content(self, parent):
        form_frame = ctk.CTkFrame(
            parent,
            fg_color="#DFCFC2",
            corner_radius=20,
            border_width=3,
            border_color="#DFCFC2",
            width=800,
            height=350 
        )
        form_frame.pack(pady=(0, 30)) 
        form_frame.pack_propagate(False)
        
        inner_container = ctk.CTkFrame(form_frame, fg_color="transparent")
        inner_container.pack(expand=True, fill="both", padx=20, pady=30) 
        
        self.create_keywords_section(inner_container)
        
        self.create_algorithm_section(inner_container)
        
        self.create_top_matches_section(inner_container)
    
    def create_keywords_section(self, parent):
        keywords_container = ctk.CTkFrame(parent, fg_color="transparent")
        keywords_container.pack(fill="x", pady=(0, 20)) 
        
        keywords_label = ctk.CTkLabel(
            keywords_container,
            text="Keywords",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1B2B4C"
        )
        keywords_label.pack(anchor="w", pady=(0, 5)) 
        
        self.keywords_entry = ctk.CTkEntry(
            keywords_container,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="#FFFFFF",
            border_color="#FFFFFF",
            border_width=0,
            text_color="#000000",
            placeholder_text="Enter keywords separated by commas...",
            placeholder_text_color="#C3C3C3",
            corner_radius=8
        )
        self.keywords_entry.pack(fill="x")
    
    def create_algorithm_section(self, parent):
        algorithm_container = ctk.CTkFrame(parent, fg_color="transparent")
        algorithm_container.pack(fill="x", pady=(0, 20))
        
        algorithm_label = ctk.CTkLabel(
            algorithm_container,
            text="Search Algorithm",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1B2B4C"
        )
        algorithm_label.pack(anchor="w", pady=(0, 5)) 
        
        self.algorithm_segmented = ctk.CTkSegmentedButton(
            algorithm_container,
            values=["Knuth-Morris-Pratt", "Boyer-Moore"],
            font=ctk.CTkFont(size=14),
            height=40,
            selected_color="#334D7A",
            selected_hover_color="#334D7A",
            unselected_color="#FFFFFF",
            unselected_hover_color="#F0F0F0",
            text_color_disabled="#AC9E92",
            fg_color="#FFFFFF",
            corner_radius=8,
            border_width= 4,
            command=self.select_algorithm_segmented
        )
        self.algorithm_segmented.pack(anchor="w")
        self.algorithm_segmented.set("Knuth-Morris-Pratt")
        
        self.update_algorithm_button_colors()
    
    def create_top_matches_section(self, parent):
        matches_container = ctk.CTkFrame(parent, fg_color="transparent")
        matches_container.pack(fill="x", pady=(0, 20)) 
        
        matches_label = ctk.CTkLabel(
            matches_container,
            text="Top Matches",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1B2B4C"
        )
        matches_label.pack(anchor="w", pady=(0, 5))  
        
        spinbox_container = ctk.CTkFrame(matches_container, fg_color="transparent")
        spinbox_container.pack(anchor="w")
        
        self.top_matches_entry = ctk.CTkEntry(
            spinbox_container,
            width=80,
            height=35,
            font=ctk.CTkFont(size=14),
            fg_color="#FFFFFF",
            border_color="#FFFFFF",
            border_width=0,
            text_color="#000000",
            justify="center",
            corner_radius=8
        )
        self.top_matches_entry.pack(side="left")
        self.top_matches_entry.insert(0, "1")
        
        buttons_container = ctk.CTkFrame(spinbox_container, fg_color="transparent")
        buttons_container.pack(side="left", padx=(5, 0))
        
        up_button = ctk.CTkButton(
            buttons_container,
            text="▲",
            width=30,
            height=17,  
            font=ctk.CTkFont(size=12),
            fg_color="#334D7A",
            hover_color="#1B2B4C",
            text_color="#FFFFFF",
            corner_radius=4,
            command=self.increment_matches
        )
        up_button.pack(pady=(0, 1))
        
        down_button = ctk.CTkButton(
            buttons_container,
            text="▼",
            width=30,
            height=17, 
            font=ctk.CTkFont(size=12),
            fg_color="#334D7A",
            hover_color="#1B2B4C",
            text_color="#FFFFFF",
            corner_radius=4,
            command=self.decrement_matches
        )
        down_button.pack(pady=(0, 0))
    
    def create_search_button(self, parent):
        button_container = ctk.CTkFrame(parent, fg_color="transparent")
        button_container.pack(pady=(0, 0))  
        
        search_button = ctk.CTkButton(
            button_container,
            text="Search Now",
            font=ctk.CTkFont(size=16, weight="normal"),
            width=200,
            height=45,
            corner_radius=8,
            border_width=2,
            border_color="#DFCFC2", 
            fg_color="#334D7A",
            hover_color="#1B2B4C", 
            text_color="#DFCFC2",
            command=self.perform_search
        )
        search_button.pack()
    
    def create_bearlock_sad_image(self, parent):
        try:
            image_path = "./assets/bearlock-sad.png"
            
            if os.path.exists(image_path):
                bearlock_image = Image.open(image_path)
                
                bearlock_ctk_image = ctk.CTkImage(
                    light_image=bearlock_image,
                    dark_image=bearlock_image,
                    size=(120, 120)
                )
                
                image_label = ctk.CTkLabel(
                    parent,
                    image=bearlock_ctk_image,
                    text=""
                )
                image_label.pack()
                
        except Exception as e:
            placeholder = ctk.CTkLabel(
                parent,
                text="Bearlock",
                font=ctk.CTkFont(size=40),
                text_color="#FFFFFF"
            )
            placeholder.pack()
    
    def create_asset3_image(self, parent):
        try:
            image_path = "./assets/asset3.png"
            
            if os.path.exists(image_path):
                asset_image = Image.open(image_path)
                
                asset_ctk_image = ctk.CTkImage(
                    light_image=asset_image,
                    dark_image=asset_image,
                    size=(70, 60)
                )
                
                image_label = ctk.CTkLabel(
                    parent,
                    image=asset_ctk_image,
                    text=""
                )
                image_label.pack()
                
        except Exception as e:
            placeholder = ctk.CTkLabel(
                parent,
                text="Search",
                font=ctk.CTkFont(size=40),
                text_color="#FFFFFF"
            )
            placeholder.pack()
    
    def update_algorithm_button_colors(self):
        self.algorithm_segmented.configure(
            text_color=("#1B2B4C", "#C3C3C3")
        )
    
    def select_algorithm_segmented(self, value):
        self.selected_algorithm.set(value)
        print(f"Algorithm selected: {value}")
        self.algorithm_segmented.after(10, self.update_algorithm_button_colors)
    
    def increment_matches(self):
        try:
            current_value = int(self.top_matches_entry.get())
            new_value = current_value + 1
            self.top_matches_entry.delete(0, "end")
            self.top_matches_entry.insert(0, str(new_value))
        except ValueError:
            self.top_matches_entry.delete(0, "end")
            self.top_matches_entry.insert(0, "1")
    
    def decrement_matches(self):
        try:
            current_value = int(self.top_matches_entry.get())
            new_value = max(1, current_value - 1)
            self.top_matches_entry.delete(0, "end")
            self.top_matches_entry.insert(0, str(new_value))
        except ValueError:
            self.top_matches_entry.delete(0, "end")
            self.top_matches_entry.insert(0, "1")
    
    def perform_search(self):
        keywords = self.keywords_entry.get()
        algorithm = self.selected_algorithm.get()
        top_matches = self.top_matches_entry.get()
        
        print(f"Searching with keywords: {keywords}")
        print(f"Using algorithm: {algorithm}")
        print(f"Top matches: {top_matches}")
        
        self.navigate_callback("result")

    def __init__(self, parent, navigate_callback, backend_manager):
        super().__init__(
            parent,
            fg_color="#1B2B4C",
            corner_radius=0
        )
        
        self.navigate_callback = navigate_callback
        self.backend_manager = backend_manager # Store backend_manager
        self.pack(fill="both", expand=True)
        
        self.selected_algorithm = ctk.StringVar(value="KMP") # Default to KMP to match backend options
        # Top matches entry now uses Settings as default
        self.top_matches_value = ctk.StringVar(value=str(Settings.TOP_N_MATCHES))
        
        self.setup_search_page()

    # ... (create_back_button_centered, create_header_section, etc. remain the same) ...
    
    def create_search_content(self, parent):
        form_frame = ctk.CTkFrame(
            parent,
            fg_color="#DFCFC2",
            corner_radius=20,
            border_width=3,
            border_color="#DFCFC2",
            width=800, # Adjusted for potentially longer algorithm names
            height=350 
        )
        form_frame.pack(pady=(0, 30)) 
        form_frame.pack_propagate(False)
        
        inner_container = ctk.CTkFrame(form_frame, fg_color="transparent")
        inner_container.pack(expand=True, fill="both", padx=30, pady=30) # Increased padding
        
        self.create_keywords_section(inner_container)
        
        self.create_algorithm_section(inner_container)
        
        self.create_top_matches_section(inner_container)

    def create_algorithm_section(self, parent):
        algorithm_container = ctk.CTkFrame(parent, fg_color="transparent")
        algorithm_container.pack(fill="x", pady=(0, 20))
        
        algorithm_label = ctk.CTkLabel(
            algorithm_container,
            text="Search Algorithm",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1B2B4C"
        )
        algorithm_label.pack(anchor="w", pady=(0, 5)) 
        
        # Updated values to match backend_manager expected strings
        self.algorithm_options = ["KMP", "Boyer-Moore", "Aho-Corasick"]
        self.algorithm_segmented = ctk.CTkSegmentedButton(
            algorithm_container,
            values=self.algorithm_options, # Use defined options
            font=ctk.CTkFont(size=14),
            height=40,
            selected_color="#334D7A",
            selected_hover_color="#334D7A",
            unselected_color="#FFFFFF",
            unselected_hover_color="#F0F0F0",
            text_color_disabled="#AC9E92", # Not directly used here, but good to keep
            fg_color="#FFFFFF", # Background for the unselected parts
            text_color="#1B2B4C", # Text color for unselected
            # Text color for selected
            corner_radius=8,
            border_width= 0, # No border for segmented button itself
            command=self.select_algorithm_segmented
        )

        self.algorithm_segmented.pack(fill="x", expand=True) # Fill available width
        self.algorithm_segmented.set("KMP") # Default selection
        # No need for update_algorithm_button_colors if CTk handles text color change on selection

    def select_algorithm_segmented(self, value):
        self.selected_algorithm.set(value)
        print(f"Algorithm selected: {value}")
        # CTk usually handles the color update automatically for SegmentedButton

    def create_top_matches_section(self, parent):
        # ... (implementation is okay, just ensure self.top_matches_entry.insert(0, self.top_matches_value.get()))
        matches_container = ctk.CTkFrame(parent, fg_color="transparent")
        matches_container.pack(fill="x", pady=(0, 20)) 
        
        matches_label = ctk.CTkLabel(
            matches_container,
            text="Top Matches",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1B2B4C"
        )
        matches_label.pack(anchor="w", pady=(0, 5))  
        
        spinbox_container = ctk.CTkFrame(matches_container, fg_color="transparent")
        spinbox_container.pack(anchor="w")
        
        self.top_matches_entry = ctk.CTkEntry(
            spinbox_container,
            width=80,
            height=35,
            font=ctk.CTkFont(size=14),
            fg_color="#FFFFFF",
            border_color="#FFFFFF", # No border for entry
            border_width=0,
            text_color="#000000",
            justify="center",
            corner_radius=8
        )
        self.top_matches_entry.pack(side="left")
        self.top_matches_entry.insert(0, self.top_matches_value.get()) # Use the StringVar's value
        
        buttons_container = ctk.CTkFrame(spinbox_container, fg_color="transparent")
        buttons_container.pack(side="left", padx=(5, 0))
        
        up_button = ctk.CTkButton(
            buttons_container, text="▲", width=30, height=17, font=ctk.CTkFont(size=12),
            fg_color="#334D7A", hover_color="#1B2B4C", text_color="#FFFFFF", corner_radius=4,
            command=self.increment_matches
        )
        up_button.pack(pady=(0, 1))
        
        down_button = ctk.CTkButton(
            buttons_container, text="▼", width=30, height=17, font=ctk.CTkFont(size=12),
            fg_color="#334D7A", hover_color="#1B2B4C", text_color="#FFFFFF", corner_radius=4,
            command=self.decrement_matches
        )
        down_button.pack(pady=(0, 0))

    def perform_search(self):
        keywords_str = self.keywords_entry.get()
        keywords_list = [k.strip() for k in keywords_str.split(',') if k.strip()]
        
        algorithm = self.selected_algorithm.get()
        try:
            top_matches = int(self.top_matches_entry.get())
            if top_matches <= 0:
                top_matches = Settings.TOP_N_MATCHES # Fallback to default if invalid
        except ValueError:
            top_matches = Settings.TOP_N_MATCHES # Fallback if not an integer
        
        print(f"Searching with keywords: {keywords_list}")
        print(f"Using algorithm: {algorithm}")
        print(f"Top matches: {top_matches}")

        if not keywords_list:
            # Optionally, show a message to the user that keywords are required
            print("No keywords entered.")
            # Simple dialog:
            # from tkinter import messagebox
            # messagebox.showwarning("Input Error", "Please enter at least one keyword.")
            return
            
        if self.backend_manager:
            search_results_data = self.backend_manager.search_cvs(
                keywords=keywords_list,
                algorithm=algorithm,
                top_n_matches=top_matches,
                fuzzy_threshold=Settings.FUZZY_THRESHOLD
            )
            print("------ SEARCH RESULTS DATA (from SearchPage) ------")
            import json # For pretty printing
            print(json.dumps(search_results_data, indent=2))
            print("----------------------------------------------------")
            self.navigate_callback("result", search_results=search_results_data)
        else:
            print("Backend manager not available.")
            # Fallback to dummy navigation if needed, or show error
            self.navigate_callback("result", search_results=None) # Indicate no results