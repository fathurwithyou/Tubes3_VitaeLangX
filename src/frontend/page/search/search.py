import customtkinter as ctk
from PIL import Image
import os
import re
from backend import Settings

class SearchPage(ctk.CTkFrame):
    
    def __init__(self, parent, navigate_callback, backend_manager):
        super().__init__(
            parent,
            fg_color="#1B2B4C",
            corner_radius=0
        )
        
        self.navigate_callback = navigate_callback
        self.backend_manager = backend_manager
        self.pack(fill="both", expand=True)
        
        # Initialize variables
        self.selected_algorithm = ctk.StringVar(value="KMP")
        self.top_matches_value = ctk.StringVar(value=str(Settings.TOP_N_MATCHES))
        self.algorithm_options = ["KMP", "Boyer-Moore", "Aho-Corasick"]
        
        # Bind to configure event for responsive design
        self.bind("<Configure>", self._on_window_configure)
        self._text_widgets_to_wrap = []
        
        self.setup_search_page()
    
    def _on_window_configure(self, event):
        """Handle window resize events to update text wrapping"""
        if event.widget == self:
            self.after_idle(self._update_text_wrapping)
    
    def _update_text_wrapping(self):
        """Update text wrapping for all text widgets based on current window size"""
        try:
            current_width = self.winfo_width()
            if current_width > 1:
                for widget_info in self._text_widgets_to_wrap:
                    widget = widget_info['widget']
                    padding = widget_info.get('padding', 100)
                    if widget.winfo_exists():
                        new_wrap_length = max(300, current_width - padding)
                        widget.configure(wraplength=new_wrap_length)
        except Exception as e:
            print(f"Error updating text wrapping: {e}")

    def setup_search_page(self):
        """Setup the main search page layout"""
        # Clear existing widgets and reset tracking
        for widget in self.winfo_children():
            widget.destroy()
        self._text_widgets_to_wrap = []
        
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(expand=True, fill="both", padx=50, pady=30)
        
        # Content container - centered
        content_container = ctk.CTkFrame(main_container, fg_color="transparent")
        content_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Create sections
        self.create_back_button(main_container)
        self.create_header_section(content_container)
        self.create_search_content(content_container)
        self.create_search_button(content_container)
    
    def create_back_button(self, parent):
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
        back_button.pack(anchor="nw", pady=(0, 0)) 
    
    def create_header_section(self, parent):
        """Create enhanced header with responsive layout"""
        header_container = ctk.CTkFrame(parent, fg_color="transparent")
        header_container.pack(pady=(0, 30))
        
        # Header content with images and text
        header_content = ctk.CTkFrame(header_container, fg_color="transparent")
        header_content.pack()
        
        # Left image
        left_image = ctk.CTkFrame(header_content, fg_color="transparent")
        left_image.pack(side="left", padx=(0, 25))
        self.create_bearlock_sad_image(left_image)
        
        # Center text content
        center_text = ctk.CTkFrame(header_content, fg_color="transparent")
        center_text.pack(side="left")
        
        # Main title
        title_label = ctk.CTkLabel(
            center_text,
            text="Search and Match",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#DFCFC2"
        )
        title_label.pack()
        
        # Description with responsive wrapping
        description_text = """Input the keywords you're looking for, choose the matching algorithm, and let our
system reveal the most relevant candidates, exact or approximate."""
        
        description_label = ctk.CTkLabel(
            center_text,
            text=description_text,
            font=ctk.CTkFont(size=14),
            text_color="#FFFFFF",
            justify="center",
            wraplength=500
        )
        description_label.pack(pady=(12, 0))
        
        # Track description for responsive wrapping
        self._text_widgets_to_wrap.append({
            'widget': description_label,
            'padding': 150
        })
        
        # Right image
        right_image = ctk.CTkFrame(header_content, fg_color="transparent")
        right_image.pack(side="right", padx=(25, 0))
        self.create_asset3_image(right_image)
    
    def create_search_content(self, parent):
        """Create enhanced search form with better styling"""
        form_frame = ctk.CTkFrame(
            parent,
            fg_color="#DFCFC2",
            corner_radius=25,
            border_width=0,
            width=850,
            height=380
        )
        form_frame.pack(pady=(0, 30))
        form_frame.pack_propagate(False)
        
        # Inner container with enhanced padding
        inner_container = ctk.CTkFrame(form_frame, fg_color="transparent")
        inner_container.pack(expand=True, fill="both", padx=40, pady=35)
        
        # Create form sections
        self.create_keywords_section(inner_container)
        self.create_algorithm_section(inner_container)
        self.create_top_matches_section(inner_container)
    
    def create_keywords_section(self, parent):
        """Create enhanced keywords input section"""
        keywords_container = ctk.CTkFrame(parent, fg_color="transparent")
        keywords_container.pack(fill="x", pady=(0, 25))
        
        # Section label
        keywords_label = ctk.CTkLabel(
            keywords_container,
            text="Keywords",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1B2B4C"
        )
        keywords_label.pack(anchor="w", pady=(0, 8))
        
        # Enhanced input field
        self.keywords_entry = ctk.CTkEntry(
            keywords_container,
            height=45,
            font=ctk.CTkFont(size=14),
            fg_color="#FFFFFF",
            border_color="#334D7A",
            border_width=2,
            text_color="#000000",
            placeholder_text="Enter keywords separated by commas (e.g., python, java, react)...",
            placeholder_text_color="#999999",
            corner_radius=12
        )
        self.keywords_entry.pack(fill="x")
    
    def create_algorithm_section(self, parent):
        """Create enhanced algorithm selection section"""
        algorithm_container = ctk.CTkFrame(parent, fg_color="transparent")
        algorithm_container.pack(fill="x", pady=(0, 25))
        
        # Section label
        algorithm_label = ctk.CTkLabel(
            algorithm_container,
            text="Search Algorithm",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1B2B4C"
        )
        algorithm_label.pack(anchor="w", pady=(0, 8))
        
        # Enhanced segmented button
        self.algorithm_segmented = ctk.CTkSegmentedButton(
            algorithm_container,
            values=self.algorithm_options,
            font=ctk.CTkFont(size=14, weight="normal"),
            height=45,
            selected_color="#DFCFC2",
            selected_hover_color="#DEC5B1",
            unselected_color="#FFFFFF",
            unselected_hover_color="#F5F5F5",
            text_color="#1B2B4C",
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=2,
            command=self.select_algorithm_segmented
        )
        self.algorithm_segmented.pack(fill="x")
        self.algorithm_segmented.set("KMP")
    
    def create_top_matches_section(self, parent):
        """Create enhanced top matches section with spinbox"""
        matches_container = ctk.CTkFrame(parent, fg_color="transparent")
        matches_container.pack(fill="x", pady=(0, 25))
        
        # Section label
        matches_label = ctk.CTkLabel(
            matches_container,
            text="Top Matches",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1B2B4C"
        )
        matches_label.pack(anchor="w", pady=(0, 8))
        
        # Spinbox container
        spinbox_container = ctk.CTkFrame(matches_container, fg_color="transparent")
        spinbox_container.pack(anchor="w")
        
        # Enhanced number input
        self.top_matches_entry = ctk.CTkEntry(
            spinbox_container,
            width=100,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#FFFFFF",
            border_color="#334D7A",
            border_width=2,
            text_color="#1B2B4C",
            justify="center",
            corner_radius=10
        )
        self.top_matches_entry.pack(side="left")
        self.top_matches_entry.insert(0, self.top_matches_value.get())
        
        # Enhanced spinbox buttons
        buttons_container = ctk.CTkFrame(spinbox_container, fg_color="transparent")
        buttons_container.pack(side="left", padx=(8, 0))
        
        up_button = ctk.CTkButton(
            buttons_container,
            text="▲",
            width=35,
            height=19,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#334D7A",
            hover_color="#273A5C",
            text_color="#FFFFFF",
            corner_radius=6,
            command=self.increment_matches
        )
        up_button.pack(pady=(0, 2))
        
        down_button = ctk.CTkButton(
            buttons_container,
            text="▼",
            width=35,
            height=19,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#334D7A",
            hover_color="#273A5C",
            text_color="#FFFFFF",
            corner_radius=6,
            command=self.decrement_matches
        )
        down_button.pack()
        
        # Helper text
        helper_label = ctk.CTkLabel(
            matches_container,
            text="Number of best matching candidates to display",
            font=ctk.CTkFont(size=12),
            text_color="#666666"
        )
        helper_label.pack(anchor="w", pady=(5, 0))
    
    def create_search_button(self, parent):
        """Create enhanced search button with better styling"""
        button_container = ctk.CTkFrame(parent, fg_color="transparent")
        button_container.pack()
        
        search_button = ctk.CTkButton(
            button_container,
            text="🔍 Search Now",
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
        """Create Bearlock sad image with fallback"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "..", "..", "assets", "bearlock-sad.png")
            if not os.path.exists(image_path):
                image_path = "./assets/bearlock-sad.png"
            
            if os.path.exists(image_path):
                bearlock_image = Image.open(image_path)
                bearlock_ctk_image = ctk.CTkImage(
                    light_image=bearlock_image,
                    dark_image=bearlock_image,
                    size=(130, 130)
                )
                image_label = ctk.CTkLabel(parent, image=bearlock_ctk_image, text="")
                image_label.pack()
            else:
                raise FileNotFoundError("Bearlock sad image not found")
                
        except Exception as e:
            print(f"Error loading bearlock-sad.png: {e}")
            placeholder = ctk.CTkLabel(
                parent,
                text="🐻😔",
                font=ctk.CTkFont(size=50),
                text_color="#DFCFC2"
            )
            placeholder.pack()
    
    def create_asset3_image(self, parent):
        """Create asset3 image with fallback"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "..", "..", "assets", "asset3.png")
            if not os.path.exists(image_path):
                image_path = "./assets/asset3.png"
            
            if os.path.exists(image_path):
                asset_image = Image.open(image_path)
                asset_ctk_image = ctk.CTkImage(
                    light_image=asset_image,
                    dark_image=asset_image,
                    size=(80, 70)
                )
                image_label = ctk.CTkLabel(parent, image=asset_ctk_image, text="")
                image_label.pack()
            else:
                raise FileNotFoundError("Asset3 image not found")
                
        except Exception as e:
            print(f"Error loading asset3.png: {e}")
            placeholder = ctk.CTkLabel(
                parent,
                text="🔍",
                font=ctk.CTkFont(size=50),
                text_color="#DFCFC2"
            )
            placeholder.pack()
    
    def select_algorithm_segmented(self, value):
        """Handle algorithm selection"""
        self.selected_algorithm.set(value)
        print(f"Algorithm selected: {value}")
    
    def increment_matches(self):
        """Increment the top matches value"""
        try:
            current_value = int(self.top_matches_entry.get())
            new_value = min(50, current_value + 1)  # Cap at 50
            self.top_matches_entry.delete(0, "end")
            self.top_matches_entry.insert(0, str(new_value))
        except ValueError:
            self.top_matches_entry.delete(0, "end")
            self.top_matches_entry.insert(0, "1")
    
    def decrement_matches(self):
        """Decrement the top matches value"""
        try:
            current_value = int(self.top_matches_entry.get())
            new_value = max(1, current_value - 1)  # Minimum 1
            self.top_matches_entry.delete(0, "end")
            self.top_matches_entry.insert(0, str(new_value))
        except ValueError:
            self.top_matches_entry.delete(0, "end")
            self.top_matches_entry.insert(0, "1")
    
    def perform_search(self):
        """Perform the search with validation and backend integration"""
        # Get and validate input
        keywords_str = self.keywords_entry.get().strip()
        if not keywords_str:
            print("No keywords entered.")
            # Could add a visual feedback here
            return
        
        keywords_list = [k.strip() for k in re.split(r',[\s]+', keywords_str) if k.strip()]
        if not keywords_list:
            print("No valid keywords found.")
            return
        
        # Get algorithm
        algorithm = self.selected_algorithm.get()
        
        # Get and validate top matches
        try:
            top_matches = int(self.top_matches_entry.get())
            if top_matches <= 0:
                top_matches = Settings.TOP_N_MATCHES
        except ValueError:
            top_matches = Settings.TOP_N_MATCHES
        
        # Debug output
        print(f"Searching with keywords: {keywords_list}")
        print(f"Using algorithm: {algorithm}")
        print(f"Top matches: {top_matches}")
        
        # Perform search using backend
        if self.backend_manager:
            try:
                search_results_data = self.backend_manager.search_cvs(
                    keywords=keywords_list,
                    algorithm=algorithm,
                    top_n_matches=top_matches,
                    fuzzy_threshold=Settings.FUZZY_THRESHOLD
                )
                
                print("------ SEARCH RESULTS DATA (from SearchPage) ------")
                import json
                print(json.dumps(search_results_data, indent=2))
                print("----------------------------------------------------")
                
                # Navigate to results with data
                self.navigate_callback("result", search_results=search_results_data)
                
            except Exception as e:
                print(f"Search error: {e}")
                # Could add error handling UI here
                self.navigate_callback("result", search_results=None)
        else:
            print("Backend manager not available.")
            self.navigate_callback("result", search_results=None)