# src/frontend/page/result/result.py
import customtkinter as ctk
from PIL import Image
import os

class ResultPage(ctk.CTkFrame):
    
    def __init__(self, parent, navigate_callback, backend_manager, search_results=None, **kwargs): # Added **kwargs
        super().__init__(
            parent,
            fg_color="#1B2B4C", # Matches screenshot background
            corner_radius=0,
            **kwargs 
        )
        
        self.navigate_callback = navigate_callback
        self.backend_manager = backend_manager 
        self.search_results_data = search_results if search_results else {"results": []} 
        self.pack(fill="both", expand=True)
        
        self.setup_result_page()
    
    def setup_result_page(self):
        page_main_container = ctk.CTkFrame(self, fg_color="transparent")
        page_main_container.pack(fill="both", expand=True, padx=30, pady=20)
        
        back_button_frame = ctk.CTkFrame(page_main_container, fg_color="transparent")
        back_button_frame.pack(fill="x", pady=(0, 10)) 
        self.create_back_button(back_button_frame)

        self.header_display_frame = ctk.CTkFrame(page_main_container, fg_color="transparent")
        self.header_display_frame.pack(fill="x", pady=(0, 25)) # Increased bottom padding for header
        self.create_header_section(self.header_display_frame) 

        self.scrollable_results_area = ctk.CTkScrollableFrame(
            page_main_container, 
            fg_color="transparent", 
            scrollbar_button_color="#334D7A", 
            scrollbar_button_hover_color="#4A5D8A"
        )
        self.scrollable_results_area.pack(fill="both", expand=True)
        
        self.create_results_grid(self.scrollable_results_area)
    
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
            command=lambda: self.navigate_callback("search")
        )
        back_button.pack(anchor="nw")
    
    def create_header_section(self, parent): 
        header_content = ctk.CTkFrame(parent, fg_color="transparent") 
        header_content.pack(pady=10) # Added padding around header content
        
        # Omitting side images (hat and book) for a cleaner look if not strictly needed
        # or to give more space to title/subtitle if they were present in screenshot.
        # If they are desired, uncomment their creation and packing.
        # left_image = ctk.CTkFrame(header_content, fg_color="transparent")
        # left_image.pack(side="left", padx=(0, 20))
        # self.create_hat_image(left_image) #
        
        center_content = ctk.CTkFrame(header_content, fg_color="transparent")
        center_content.pack(side="left", expand=True) # Allow center content to expand
        
        title_label = ctk.CTkLabel(
            center_content,
            text="Results", # Matches screenshot
            font=ctk.CTkFont(size=36, weight="bold"), # Slightly larger title
            text_color="#DFCFC2"
        )
        title_label.pack(pady=(0, 8)) # Padding below title
        
        # Subtitle text from the screenshot
        description_text = """The search is complete! Bearlock Holmes has scanned 100 CVs in just 100 ms and uncovered
candidates that match your clues. Whether it's an exact keyword hit or a fuzzy match, the most
promising profiles are now on your desk.""" # Matches screenshot

        description_label = ctk.CTkLabel(
            center_content,
            text=description_text,
            font=ctk.CTkFont(size=14), 
            text_color="#FFFFFF",      
            justify="center",
            wraplength=700 # Adjust wraplength as needed
        )
        description_label.pack(pady=(5, 0))
        
        # right_image = ctk.CTkFrame(header_content, fg_color="transparent")
        # right_image.pack(side="right", padx=(20, 0))
        # self.create_book_image(right_image) #

    def create_results_grid(self, parent_scrollable_frame): 
        results_organizer = ctk.CTkFrame(parent_scrollable_frame, fg_color="transparent")
        results_organizer.pack(fill="x", expand=True, padx=10, pady=5) # Allow organizer to expand

        actual_results = self.search_results_data.get("results", [])

        if not actual_results:
            no_results_label = ctk.CTkLabel(
                results_organizer, 
                text="No matching CVs found.",
                font=ctk.CTkFont(size=18),
                text_color="#FFFFFF"
            )
            no_results_label.pack(pady=50, expand=True) 
            return
        
        max_cols = 3 # As per screenshot
        
        cards_grid_container = ctk.CTkFrame(results_organizer, fg_color="transparent")
        # Center the grid container if it doesn't fill the width
        cards_grid_container.pack(anchor="n", expand=True if len(actual_results) < max_cols else False)


        for i, result_item in enumerate(actual_results):
            if i % max_cols == 0:
                row_frame = ctk.CTkFrame(cards_grid_container, fg_color="transparent")
                row_frame.pack(fill="x", pady=10, anchor="n") # Increased pady for rows
                # Configure columns for equal spacing within the row
                for col_idx in range(max_cols):
                    row_frame.grid_columnconfigure(col_idx, weight=1)
            
            # Card Frame
            card_frame = ctk.CTkFrame(
                row_frame, 
                fg_color="#DFCFC2", # Matches screenshot card background
                corner_radius=15,  # Matches screenshot
                width=300,         # Adjusted width
                height=220         # Adjusted height to fit content better
            )
            # Place card in the grid
            card_frame.grid(row=0, column=(i % max_cols), padx=15, pady=10, sticky="n") # Added more padx/pady
            card_frame.grid_propagate(False) 
            card_frame.pack_propagate(False) 
            
            self.create_result_card(card_frame, result_item)
    
    def create_result_card(self, parent, result):
        # Main content area within the card
        content_frame = ctk.CTkFrame(parent, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=15) # Increased padx
        
        # Header: Name and Match Count
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        name_label = ctk.CTkLabel(
            header_frame,
            text=result.get("name", "N/A"),
            font=ctk.CTkFont(size=18, weight="bold"), # Larger name font
            text_color="#1B2B4C" # Dark text
        )
        name_label.pack(side="left", anchor="w")
        
        # Matches text as per screenshot "X matches"
        matches_text = f"{result.get('total_occurrences', 0)} matches"
        matches_label = ctk.CTkLabel(
            header_frame,
            text=matches_text,
            font=ctk.CTkFont(size=14), # Adjusted size
            text_color="#334D7A" 
        )
        matches_label.pack(side="right", anchor="e")

        # Matched Keywords Section
        keywords_section_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        keywords_section_frame.pack(fill="x", pady=(5, 10)) # expand=True, 

        matched_keywords_title_label = ctk.CTkLabel(
            keywords_section_frame,
            text="Matched keywords:",
            font=ctk.CTkFont(size=13, weight="normal"), # Normal weight as per screenshot
            text_color="#1B2B4C"
        )
        matched_keywords_title_label.pack(anchor="w")

        exact_keywords_data = result.get("matched_keywords", {})
        if exact_keywords_data:
            for i, (keyword, count) in enumerate(list(exact_keywords_data.items())[:3]): # Display up to 3 to match screenshot
                occurrence_text = f"{count} occurrence{'s' if count > 1 else ''}"
                keyword_item_label = ctk.CTkLabel(
                    keywords_section_frame,
                    text=f"{i+1}. {keyword.capitalize()}: {occurrence_text}",
                    font=ctk.CTkFont(size=12),
                    text_color="#1B2B4C"
                )
                keyword_item_label.pack(anchor="w", padx=15) # Indent list items
        else:
            no_exact_keywords_label = ctk.CTkLabel(
                keywords_section_frame,
                text="No exact keywords matched.",
                font=ctk.CTkFont(size=12),
                text_color="#4B4B4B" # Dimmer text
            )
            no_exact_keywords_label.pack(anchor="w", padx=15)
        
        # Buttons Frame (ensure it's at the bottom)
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", side="bottom", pady=(15,0)) # Push to bottom, add padding above
                
        summary_button = ctk.CTkButton(
            buttons_frame, text="Summary", font=ctk.CTkFont(size=13, weight="normal"), # Slightly larger button font
            width=100, height=32, corner_radius=6, # Adjusted button size
            fg_color="#334D7A", hover_color="#273A5C", text_color="#DFCFC2", # Match screenshot style
            command=lambda app_id=result.get("applicant_id"): self.show_summary(app_id)
        )
        summary_button.pack(side="left", expand=True, padx=(0,5))
                
        view_cv_button = ctk.CTkButton(
            buttons_frame, text="View CV", font=ctk.CTkFont(size=13, weight="normal"),
            width=100, height=32, corner_radius=6,
            fg_color="#334D7A", hover_color="#273A5C", text_color="#DFCFC2",
            command=lambda app_id=result.get("applicant_id"): self.view_cv(app_id, path)
        )
        view_cv_button.pack(side="right", expand=True, padx=(5,0))

    def show_summary(self, applicant_id):
        if applicant_id is None:
            print("Error: Applicant ID is None for summary.")
            return
        print(f"Showing summary for Applicant ID: {applicant_id}")
        self.navigate_callback("summary", applicant_id=applicant_id)
            
    def view_cv(self, applicant_id):
        if applicant_id is None:
            print("Error: Applicant ID is None for CV view.")
            return
        print(f"Viewing CV for Applicant ID: {applicant_id}")
        self.navigate_callback("cv", applicant_id=applicant_id)

    def create_hat_image(self, parent):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "..", "..", "assets", "asset2.png")
            if not os.path.exists(image_path): image_path = "./assets/asset2.png" 
            if os.path.exists(image_path):
                hat_image = Image.open(image_path)
                hat_ctk_image = ctk.CTkImage(light_image=hat_image, dark_image=hat_image, size=(100, 95))
                image_label = ctk.CTkLabel(parent, image=hat_ctk_image, text="")
                image_label.pack()
            else: raise FileNotFoundError("Hat image not found")
        except Exception as e:
            print(f"Error loading asset2.png (hat): {e}")
            ctk.CTkLabel(parent, text="🎩", font=ctk.CTkFont(size=40), text_color="#DFCFC2").pack()
    
    def create_book_image(self, parent):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "..", "..", "assets", "asset4.png")
            if not os.path.exists(image_path): image_path = "./assets/asset4.png"
            if os.path.exists(image_path):
                book_image = Image.open(image_path)
                book_ctk_image = ctk.CTkImage(light_image=book_image, dark_image=book_image, size=(90, 100))
                image_label = ctk.CTkLabel(parent, image=book_ctk_image, text="")
                image_label.pack()
            else: raise FileNotFoundError("Book image not found")
        except Exception as e:
            print(f"Error loading asset4.png (book): {e}")
            ctk.CTkLabel(parent, text="📖", font=ctk.CTkFont(size=50), text_color="#DFCFC2").pack()