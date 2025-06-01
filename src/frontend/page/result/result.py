# src/frontend/page/result/result.py
import customtkinter as ctk
from PIL import Image
import os

class ResultPage(ctk.CTkFrame):
    
    def __init__(self, parent, navigate_callback, backend_manager, search_results=None, **kwargs):
        super().__init__(
            parent,
            fg_color="#1B2B4C", 
            corner_radius=0,
            **kwargs 
        )
        
        self.navigate_callback = navigate_callback
        self.backend_manager = backend_manager 
        self.search_results_data = search_results if search_results else {"results": []} 
        self.pack(fill="both", expand=True)
        
        self.setup_result_page()
    
    # ... (setup_result_page, create_back_button, create_header_section, create_results_grid remain the same as your provided code) ...
    def setup_result_page(self):
        page_main_container = ctk.CTkFrame(self, fg_color="transparent")
        page_main_container.pack(fill="both", expand=True, padx=30, pady=20)
        
        back_button_frame = ctk.CTkFrame(page_main_container, fg_color="transparent")
        back_button_frame.pack(fill="x", pady=(0, 10)) 
        self.create_back_button(back_button_frame)

        self.header_display_frame = ctk.CTkFrame(page_main_container, fg_color="transparent")
        self.header_display_frame.pack(fill="x", pady=(0, 25)) 
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
        header_content.pack(pady=10)
        
        center_content = ctk.CTkFrame(header_content, fg_color="transparent")
        center_content.pack(side="left", expand=True)
        
        title_label = ctk.CTkLabel(
            center_content,
            text="Results", 
            font=ctk.CTkFont(size=36, weight="bold"), 
            text_color="#DFCFC2"
        )
        title_label.pack(pady=(0, 8)) 
        
        description_text = """The search is complete! Bearlock Holmes has scanned 100 CVs in just 100 ms and uncovered
candidates that match your clues. Whether it's an exact keyword hit or a fuzzy match, the most
promising profiles are now on your desk."""

        description_label = ctk.CTkLabel(
            center_content,
            text=description_text,
            font=ctk.CTkFont(size=14), 
            text_color="#FFFFFF",      
            justify="center",
            wraplength=700 
        )
        description_label.pack(pady=(5, 0))

    def create_results_grid(self, parent_scrollable_frame): 
        results_organizer = ctk.CTkFrame(parent_scrollable_frame, fg_color="transparent")
        results_organizer.pack(fill="x", expand=True, padx=10, pady=5)

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
        
        max_cols = 3
        
        cards_grid_container = ctk.CTkFrame(results_organizer, fg_color="transparent")
        cards_grid_container.pack(anchor="n", expand=True if len(actual_results) < max_cols else False)

        for i, result_item in enumerate(actual_results):
            if i % max_cols == 0:
                row_frame = ctk.CTkFrame(cards_grid_container, fg_color="transparent")
                row_frame.pack(fill="x", pady=10, anchor="n") 
                for col_idx in range(max_cols):
                    row_frame.grid_columnconfigure(col_idx, weight=1)
            
            card_frame = ctk.CTkFrame(
                row_frame, 
                fg_color="#DFCFC2", 
                corner_radius=15,  
                width=300,         
                height=220         
            )
            card_frame.grid(row=0, column=(i % max_cols), padx=15, pady=10, sticky="n")
            card_frame.grid_propagate(False) 
            card_frame.pack_propagate(False) 
            
            self.create_result_card(card_frame, result_item) # Call with result_item

    def create_result_card(self, parent, result): # 'result' here is result_item
        content_frame = ctk.CTkFrame(parent, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        name_label = ctk.CTkLabel(
            header_frame,
            text=result.get("name", "N/A"),
            font=ctk.CTkFont(size=18, weight="bold"), 
            text_color="#1B2B4C" 
        )
        name_label.pack(side="left", anchor="w")
        
        matches_text = f"{result.get('total_occurrences', 0)} matches"
        matches_label = ctk.CTkLabel(
            header_frame,
            text=matches_text,
            font=ctk.CTkFont(size=14), 
            text_color="#334D7A" 
        )
        matches_label.pack(side="right", anchor="e")

        keywords_section_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        keywords_section_frame.pack(fill="x", pady=(5, 10))

        matched_keywords_title_label = ctk.CTkLabel(
            keywords_section_frame,
            text="Matched keywords:",
            font=ctk.CTkFont(size=13, weight="normal"), 
            text_color="#1B2B4C"
        )
        matched_keywords_title_label.pack(anchor="w")

        exact_keywords_data = result.get("matched_keywords", {})
        if exact_keywords_data:
            for i, (keyword, count) in enumerate(list(exact_keywords_data.items())[:3]): 
                occurrence_text = f"{count} occurrence{'s' if count > 1 else ''}"
                keyword_item_label = ctk.CTkLabel(
                    keywords_section_frame,
                    text=f"{i+1}. {keyword.capitalize()}: {occurrence_text}",
                    font=ctk.CTkFont(size=12),
                    text_color="#1B2B4C"
                )
                keyword_item_label.pack(anchor="w", padx=15)
        else:
            no_exact_keywords_label = ctk.CTkLabel(
                keywords_section_frame,
                text="No exact keywords matched.",
                font=ctk.CTkFont(size=12),
                text_color="#4B4B4B" 
            )
            no_exact_keywords_label.pack(anchor="w", padx=15)
        
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", side="bottom", pady=(15,0))
                
        summary_button = ctk.CTkButton(
            buttons_frame, text="Summary", font=ctk.CTkFont(size=13, weight="normal"), 
            width=100, height=32, corner_radius=6, 
            fg_color="#334D7A", hover_color="#273A5C", text_color="#DFCFC2", 
            # Pass specific cv_path for summary if its content depends on specific CV
            command=lambda app_id=result.get("applicant_id"), cv_specific_path=result.get("cv_path"): self.show_summary(app_id, cv_specific_path)
        )
        summary_button.pack(side="left", expand=True, padx=(0,5))
                
        view_cv_button = ctk.CTkButton(
            buttons_frame, text="View CV", font=ctk.CTkFont(size=13, weight="normal"),
            width=100, height=32, corner_radius=6,
            fg_color="#334D7A", hover_color="#273A5C", text_color="#DFCFC2",
            # Correctly capture and pass applicant_id AND the specific cv_path for this card
            command=lambda app_id=result.get("applicant_id"), cv_specific_path=result.get("cv_path"): self.view_cv(app_id, cv_specific_path)
        )
        view_cv_button.pack(side="right", expand=True, padx=(5,0))

    # Modified show_summary to accept cv_path
    def show_summary(self, applicant_id, cv_path=None): # Added cv_path, default to None
        if applicant_id is None:
            print("Error: Applicant ID is None for summary.")
            return
        # cv_path might be None if not all summaries are tied to a specific CV version
        print(f"Showing summary for Applicant ID: {applicant_id}, Specific CV path: {cv_path}")
        self.navigate_callback("summary", applicant_id=applicant_id, cv_path=cv_path)
            
    # Modified view_cv to accept cv_path
    def view_cv(self, applicant_id, cv_path): # Added cv_path parameter
        if applicant_id is None:
            print("Error: Applicant ID is None for CV view.")
            return
        if cv_path is None: # Add a check for cv_path
            print("Error: CV Path is None for CV view.")
            # Optionally, try to fall back to applicant_id based lookup if that's desired
            # For now, require cv_path if this method is called with it.
            return
        print(f"Viewing CV for Applicant ID: {applicant_id}, Path: {cv_path}")
        # Pass cv_path to the navigation callback
        self.navigate_callback("cv", applicant_id=applicant_id, cv_path=cv_path)

    # ... (create_hat_image, create_book_image remain the same) ...
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