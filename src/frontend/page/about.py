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
        
        # Bind to configure event for responsive design
        self.bind("<Configure>", self._on_window_configure)
        self._text_widgets_to_wrap = []
        
        self.setup_about_page()
    
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
    
    def setup_about_page(self):
        """Setup the main about page with enhanced scrollable frame"""
        # Clear existing widgets and reset tracking
        for widget in self.winfo_children():
            widget.destroy()
        self._text_widgets_to_wrap = []
        
        # Enhanced scrollable container
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=15,
            scrollbar_button_color="#334D7A",
            scrollbar_button_hover_color="#4A5D8A"
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=30, pady=25)
        
        self.create_about_content()
    
    def create_about_content(self):
        """Create all content sections with enhanced spacing"""
        # Enhanced back button
        # self.create_back_button()
        
        # Spacer
        ctk.CTkFrame(self.scrollable_frame, fg_color="transparent", height=20).pack()
        
        # Main sections
        self.create_how_it_works_section()
        self.create_section_spacer()
        
        self.create_bearlock_section()
        self.create_section_spacer()
        
        self.create_algorithms_section()
        self.create_section_spacer()
        
        self.create_features_section()
        
        # Bottom spacer
        ctk.CTkFrame(self.scrollable_frame, fg_color="transparent", height=50).pack()
    
    def create_back_button(self):
        """Create enhanced back button"""
        back_button = ctk.CTkButton(
            self.scrollable_frame,
            text="← Back to Home",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=150,
            height=45,
            corner_radius=12,
            border_width=2,
            border_color="#DFCFC2",
            fg_color="#334D7A",
            hover_color="#273A5C",
            text_color="#DFCFC2",
            command=lambda: self.navigate_callback("opening")
        )
        back_button.pack(anchor="w", pady=(10, 0))
    
    def create_section_spacer(self):
        """Create consistent section spacing"""
        spacer = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent", height=60)
        spacer.pack()
    
    def create_how_it_works_section(self):
        """Create enhanced 'How it Works' section"""
        # Section container with subtle background
        section_container = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="#273A5C",
            corner_radius=20,
            border_width=2,
            border_color="#334D7A"
        )
        section_container.pack(fill="x", pady=20, padx=10)
        
        # Title with icon
        title_label = ctk.CTkLabel(
            section_container,
            text="🔍 How it Works",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#DFCFC2"
        )
        title_label.pack(pady=(30, 20))
        
        # Enhanced description
        description_text = """At CV Detective, we combine speed and intelligence to match resumes with your target
keywords. Our engine leverages a blend of exact and fuzzy matching algorithms,
so whether it's a perfect hit or a near miss, you'll still get the best candidates.
        
Our system processes CVs in milliseconds, providing both precise keyword matches
and intelligent approximate matching for maximum coverage."""
        
        description_label = ctk.CTkLabel(
            section_container,
            text=description_text,
            font=ctk.CTkFont(size=15),
            text_color="#FFFFFF",
            wraplength=750,
            justify="center"
        )
        description_label.pack(pady=(0, 30), padx=30)
        
        # Track description for responsive wrapping
        self._text_widgets_to_wrap.append({
            'widget': description_label,
            'padding': 120
        })
    
    def create_bearlock_section(self):
        """Create enhanced Bearlock Holmes section"""
        # Section container
        section_container = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="#2D3E5F",
            corner_radius=20,
            border_width=2,
            border_color="#B8A398"
        )
        section_container.pack(fill="x", pady=20, padx=10)
        
        # Title
        bearlock_title = ctk.CTkLabel(
            section_container,
            text="🐻 Meet Bearlock Holmes",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#DFCFC2"
        )
        bearlock_title.pack(pady=(30, 25))
        
        # Content container for image and text
        content_container = ctk.CTkFrame(section_container, fg_color="transparent")
        content_container.pack(pady=(0, 30), padx=30)
        
        # Image section
        image_container = ctk.CTkFrame(content_container, fg_color="transparent")
        image_container.pack(pady=(0, 25))
        
        bearlock_image = self.create_bearlock_image(image_container)
        if not bearlock_image:
            # Enhanced placeholder
            placeholder = ctk.CTkFrame(
                image_container,
                width=220,
                height=220,
                fg_color="#1B2B4C",
                corner_radius=20,
                border_width=3,
                border_color="#DFCFC2"
            )
            placeholder.pack()
            placeholder.pack_propagate(False)
            
            placeholder_label = ctk.CTkLabel(
                placeholder,
                text="🐻🔍\nBearlock\nHolmes",
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color="#DFCFC2",
                justify="center"
            )
            placeholder_label.pack(expand=True)
        
        # Enhanced description
        bearlock_text = """Say hello to Bearlock Holmes, your loyal search companion and master detective!
He's on a mission to help you sniff out the best CVs from a stack of suspects.
Every search you make, he's right there with you, magnifying glass in paw, ready
to highlight the clues you need.

With his keen eye for detail and lightning-fast algorithms, Bearlock ensures
no great candidate goes unnoticed in your talent search."""
        
        bearlock_description = ctk.CTkLabel(
            content_container,
            text=bearlock_text,
            font=ctk.CTkFont(size=15),
            text_color="#FFFFFF",
            wraplength=650,
            justify="center"
        )
        bearlock_description.pack()
        
        # Track description for responsive wrapping
        self._text_widgets_to_wrap.append({
            'widget': bearlock_description,
            'padding': 120
        })
    
    def create_algorithms_section(self):
        """Create enhanced 'Algorithms We Use' section with Aho-Corasick"""
        # Section container
        section_container = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="#273A5C",
            corner_radius=20,
            border_width=2,
            border_color="#334D7A"
        )
        section_container.pack(fill="x", pady=20, padx=10)
        
        # Title
        algo_title = ctk.CTkLabel(
            section_container,
            text="⚡ Algorithms We Use",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#DFCFC2"
        )
        algo_title.pack(pady=(30, 35))
        
        # Cards container with responsive grid
        cards_container = ctk.CTkFrame(section_container, fg_color="transparent")
        cards_container.pack(pady=(0, 30), padx=20)
        
        # Configure grid columns
        for i in range(3):
            cards_container.columnconfigure(i, weight=1, minsize=250)
        
        # Enhanced algorithm data with Aho-Corasick
        algorithms = [
            {
                "title": "Knuth-Morris-Pratt",
                "icon": "🔄",
                "description": "Think of it as a detective that remembers where it's been, never checking the same clue twice. Perfect for efficient single keyword searches.",
                "color": "#4A90E2"
            },
            {
                "title": "Boyer-Moore", 
                "icon": "⚡",
                "description": "It's like flipping through pages backwards to jump straight to the clue. Optimized for fast text scanning and pattern matching.",
                "color": "#7B68EE"
            },
            {
                "title": "Aho-Corasick",
                "icon": "🎯",
                "description": "The ultimate multi-keyword hunter! Searches for multiple patterns simultaneously in a single pass through the text.",
                "color": "#50C878"
            }
        ]
        
        for i, algo in enumerate(algorithms):
            self.create_algorithm_card(cards_container, algo, i)
    
    def create_algorithm_card(self, parent, algo_data, column):
        """Create enhanced algorithm card with better styling"""
        card = ctk.CTkFrame(
            parent,
            fg_color="#1B2B4C",
            width=240,
            height=180,
            corner_radius=18,
            border_width=3,
            border_color=algo_data["color"]
        )
        card.grid(row=0, column=column, padx=15, pady=15, sticky="ew")
        card.grid_propagate(False)
        card.pack_propagate(False)
        
        # Icon and title container
        header_container = ctk.CTkFrame(card, fg_color="transparent")
        header_container.pack(pady=(20, 10))
        
        # Algorithm icon
        icon_label = ctk.CTkLabel(
            header_container,
            text=algo_data["icon"],
            font=ctk.CTkFont(size=28)
        )
        icon_label.pack()
        
        # Algorithm title
        title_label = ctk.CTkLabel(
            header_container,
            text=algo_data["title"],
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#DFCFC2"
        )
        title_label.pack(pady=(5, 0))
        
        # Description
        desc_label = ctk.CTkLabel(
            card,
            text=algo_data["description"],
            font=ctk.CTkFont(size=13),
            text_color="#FFFFFF",
            wraplength=200,
            justify="center"
        )
        desc_label.pack(pady=(0, 20), padx=15)
        
        # Track description for responsive wrapping
        self._text_widgets_to_wrap.append({
            'widget': desc_label,
            'padding': 80
        })
    
    def create_features_section(self):
        """Create additional features section"""
        # Section container
        section_container = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="#2D3E5F",
            corner_radius=20,
            border_width=2,
            border_color="#B8A398"
        )
        section_container.pack(fill="x", pady=20, padx=10)
        
        # Title
        features_title = ctk.CTkLabel(
            section_container,
            text="✨ Key Features",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#DFCFC2"
        )
        features_title.pack(pady=(30, 25))
        
        # Features grid
        features_container = ctk.CTkFrame(section_container, fg_color="transparent")
        features_container.pack(pady=(0, 30), padx=30)
        
        # Configure grid
        for i in range(2):
            features_container.columnconfigure(i, weight=1)
        
        features = [
            {
                "icon": "🚀",
                "title": "Lightning Fast",
                "description": "Process hundreds of CVs in milliseconds with optimized algorithms"
            },
            {
                "icon": "🎯",
                "title": "Smart Matching",
                "description": "Combines exact and fuzzy matching for comprehensive results"
            },
            {
                "icon": "📊",
                "title": "Detailed Analytics",
                "description": "Get insights on match quality and keyword frequency"
            },
            {
                "icon": "🔍",
                "title": "Multi-Algorithm",
                "description": "Choose from KMP, Boyer-Moore, or Aho-Corasick algorithms"
            }
        ]
        
        for i, feature in enumerate(features):
            row = i // 2
            col = i % 2
            self.create_feature_item(features_container, feature, row, col)
    
    def create_feature_item(self, parent, feature_data, row, col):
        """Create individual feature item"""
        feature_frame = ctk.CTkFrame(
            parent,
            fg_color="#1B2B4C",
            corner_radius=15,
            border_width=2,
            border_color="#334D7A"
        )
        feature_frame.grid(row=row, column=col, padx=15, pady=10, sticky="ew")
        
        # Content container
        content_frame = ctk.CTkFrame(feature_frame, fg_color="transparent")
        content_frame.pack(pady=20, padx=20)
        
        # Icon and title
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack()
        
        icon_label = ctk.CTkLabel(
            header_frame,
            text=feature_data["icon"],
            font=ctk.CTkFont(size=24)
        )
        icon_label.pack(side="left", padx=(0, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=feature_data["title"],
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#DFCFC2"
        )
        title_label.pack(side="left")
        
        # Description
        desc_label = ctk.CTkLabel(
            content_frame,
            text=feature_data["description"],
            font=ctk.CTkFont(size=13),
            text_color="#FFFFFF",
            wraplength=250,
            justify="left"
        )
        desc_label.pack(pady=(10, 0), anchor="w")
        
        # Track description for responsive wrapping
        self._text_widgets_to_wrap.append({
            'widget': desc_label,
            'padding': 100
        })
    
    def create_bearlock_image(self, parent):
        """Create Bearlock image with enhanced fallback paths"""
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
                        size=(200, 200)
                    )
                    
                    image_label = ctk.CTkLabel(
                        parent,
                        image=bearlock_ctk_image,
                        text=""
                    )
                    image_label.pack()
                    
                    return image_label
                except Exception as e:
                    print(f"Error loading image from {image_path}: {e}")
                    continue
        
        return None