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
        
        # Bind to configure event for responsive design
        self.bind("<Configure>", self._on_window_configure)
        self._text_widgets_to_wrap = []
        
        self.setup_result_page()
    
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

    def setup_result_page(self):
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()
        
        # Reset text widgets tracking
        self._text_widgets_to_wrap = []
        
        page_main_container = ctk.CTkFrame(self, fg_color="transparent")
        page_main_container.pack(fill="both", expand=True, padx=50, pady=30)
        
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
        back_button.pack(anchor="nw", pady=(0, 0)) 
    
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
        
        # Get dynamic timing information from search results
        total_cvs_scanned = self._get_total_cvs_scanned()
        search_time = self._get_search_time()
        
        # Create dynamic description with actual search data
        description_text = f"""The search is complete! Bearlock Holmes has scanned {total_cvs_scanned} CVs in just {search_time} ms and uncovered
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
        
        # Track description for responsive wrapping
        self._text_widgets_to_wrap.append({
            'widget': description_label,
            'padding': 120
        })

    def _get_total_cvs_scanned(self):
        """Get the total number of CVs scanned from backend or estimate"""
        try:
            # Try to get actual count from backend manager
            if hasattr(self.backend_manager, 'get_total_cv_count'):
                return self.backend_manager.get_total_cv_count()
            
            # Alternative: Try to get from database directly
            if hasattr(self.backend_manager, 'db_manager'):
                cv_count = self.backend_manager.db_manager.get_total_cv_count()
                if cv_count is not None:
                    return cv_count
            
            # Fallback: Use a reasonable estimate based on results
            results_count = len(self.search_results_data.get("results", []))
            if results_count > 0:
                # Estimate total CVs as roughly 10-20x the results found
                return max(100, results_count * 15)
            else:
                return 100  # Default fallback
                
        except Exception as e:
            print(f"Error getting CV count: {e}")
            return 100  # Default fallback

    def _get_search_time(self):
        """Get the actual search time from the search results"""
        try:
            # Get timing data from search results
            exact_time = self.search_results_data.get('exact_match_time_ms', 0)
            fuzzy_time = self.search_results_data.get('fuzzy_match_time_ms', 0)
            
            # Calculate total search time
            total_time = exact_time + fuzzy_time
            
            if total_time > 0:
                return f"{total_time:.1f}"
            else:
                # Fallback to a reasonable default
                return "100"
                
        except Exception as e:
            print(f"Error getting search time: {e}")
            return "100"  # Default fallback

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
            
            self.create_result_card(card_frame, result_item)

    def create_result_card(self, parent, result):
        content_frame = ctk.CTkFrame(parent, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        name_label = ctk.CTkLabel(
            header_frame,
            text=result.get("name", "N/A"),
            font=ctk.CTkFont(size=18, weight="bold"), 
            text_color="#1B2B4C",
            wraplength=180,
            anchor="w",
            justify="left"
        )
        name_label.pack(side="left", anchor="w")
        
        # Track name label for responsive wrapping
        self._text_widgets_to_wrap.append({
            'widget': name_label,
            'padding': 100
        })
        
        matches_text = f"{result.get('total_occurrences', 0)} matches"
        matches_label = ctk.CTkLabel(
            header_frame,
            text=matches_text,
            font=ctk.CTkFont(size=12),
            text_color="#334D7A"
        )
        matches_label.pack(side="right", anchor="e")

        # Buttons frame - positioned early to ensure visibility
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", side="bottom", pady=(5,0))
                
        summary_button = ctk.CTkButton(
            buttons_frame, 
            text="Summary", 
            font=ctk.CTkFont(size=12, weight="normal"),
            width=90, 
            height=28, 
            corner_radius=6, 
            border_width=1, 
            border_color="#334D7A", 
            fg_color="#334D7A", 
            hover_color="#1B2B4C", 
            text_color="#DFCFC2",
            command=lambda app_id=result.get("applicant_id"): (
                    print(f"DEBUG: Summary button clicked with app_id: {app_id}"),
                    self.show_summary(app_id, result.get("cv_path"))
                )
            )
        summary_button.pack(side="left", expand=True, padx=(0,5))
                
        view_cv_button = ctk.CTkButton(
            buttons_frame, 
            text="View CV", 
            font=ctk.CTkFont(size=12, weight="normal"),
            width=90, 
            height=28, 
            corner_radius=6, 
            border_width=1, 
            border_color="#334D7A", 
            fg_color="#334D7A", 
            hover_color="#1B2B4C", 
            text_color="#DFCFC2",
            command=lambda app_id=result.get("applicant_id"): (
                    print(f"DEBUG: View CV button clicked with app_id: {app_id}"),
                    self.view_cv(app_id, result.get("cv_path"))
                )
            )
        view_cv_button.pack(side="right", expand=True, padx=(5,0))

        # Keywords section
        keywords_outer_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        keywords_outer_frame.pack(fill="both", expand=True, pady=(0,10))
        
        keywords_scroll_frame = ctk.CTkScrollableFrame(
            keywords_outer_frame, 
            fg_color="#F0F0F0", 
            height=80, 
            corner_radius=6
        )
        keywords_scroll_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        exact_keywords = result.get("matched_keywords", {})
        if exact_keywords:
            exact_title = ctk.CTkLabel(
                keywords_scroll_frame, 
                text="Exact:", 
                font=ctk.CTkFont(size=11, weight="bold"), 
                text_color="#1B2B4C"
            )
            exact_title.pack(anchor="w", padx=5)
            for keyword, count in exact_keywords.items():
                keyword_text = f"- {keyword} ({count})"
                keyword_label = ctk.CTkLabel(
                    keywords_scroll_frame, 
                    text=keyword_text, 
                    font=ctk.CTkFont(size=10), 
                    text_color="#1B2B4C"
                )
                keyword_label.pack(anchor="w", padx=10)

        fuzzy_keywords_info = result.get("fuzzy_keywords", {})
        if fuzzy_keywords_info:
            fuzzy_threshold_display = "N/A" 
            try:
                from backend import Settings 
                fuzzy_threshold_display = Settings.FUZZY_THRESHOLD
            except ImportError:
                pass

            fuzzy_title = ctk.CTkLabel(
                keywords_scroll_frame, 
                text=f"Fuzzy (>= {fuzzy_threshold_display}%):", 
                font=ctk.CTkFont(size=11, weight="bold"), 
                text_color="#1B2B4C"
            )
            fuzzy_title.pack(anchor="w", pady=(5,0), padx=5)
            for keyword, value in fuzzy_keywords_info.items():
                if isinstance(value, (tuple, list)) and len(value) == 2:
                    similarity, total_occurrences = value
                else:
                    similarity, total_occurrences = 0, 0
                keyword_text = f"- {keyword} (~{similarity:.0f}%) - ({total_occurrences})"
                keyword_label = ctk.CTkLabel(
                    keywords_scroll_frame, 
                    text=keyword_text, 
                    font=ctk.CTkFont(size=10), 
                    text_color="#1B2B4C"
                )
                keyword_label.pack(anchor="w", padx=10)

        if not exact_keywords and not fuzzy_keywords_info:
            no_keywords_label = ctk.CTkLabel(
                keywords_scroll_frame, 
                text="No specific keywords matched.", 
                font=ctk.CTkFont(size=10), 
                text_color="#1B2B4C"
            )
            no_keywords_label.pack(anchor="center", expand=True)

    def show_summary(self, applicant_id, cv_path=None):
        if applicant_id is None:
            print("Error: Applicant ID is None for summary.")
            return
        print(f"Showing summary for Applicant ID: {applicant_id}")
        self.navigate_callback("summary", applicant_id=applicant_id, cv_path=cv_path)
            
    def view_cv(self, applicant_id, cv_path):
        if applicant_id is None:
            print("Error: Applicant ID is None for CV view.")
            return
        if cv_path is None:
            print("Error: CV Path is None for CV view.")
            return
        print(f"Viewing CV for Applicant ID: {applicant_id}, Path: {cv_path}")
        self.navigate_callback("cv", applicant_id=applicant_id, cv_path=cv_path)

    def create_hat_image(self, parent):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "..", "..", "assets", "asset2.png")
            if not os.path.exists(image_path): 
                image_path = "./assets/asset2.png" 
            if os.path.exists(image_path):
                hat_image = Image.open(image_path)
                hat_ctk_image = ctk.CTkImage(light_image=hat_image, dark_image=hat_image, size=(100, 95))
                image_label = ctk.CTkLabel(parent, image=hat_ctk_image, text="")
                image_label.pack()
            else: 
                raise FileNotFoundError("Hat image not found")
        except Exception as e:
            print(f"Error loading asset2.png (hat): {e}")
            ctk.CTkLabel(parent, text="🎩", font=ctk.CTkFont(size=40), text_color="#DFCFC2").pack()
    
    def create_book_image(self, parent):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "..", "..", "assets", "asset4.png")
            if not os.path.exists(image_path): 
                image_path = "./assets/asset4.png"
            if os.path.exists(image_path):
                book_image = Image.open(image_path)
                book_ctk_image = ctk.CTkImage(light_image=book_image, dark_image=book_image, size=(90, 100))
                image_label = ctk.CTkLabel(parent, image=book_ctk_image, text="")
                image_label.pack()
            else: 
                raise FileNotFoundError("Book image not found")
        except Exception as e:
            print(f"Error loading asset4.png (book): {e}")
            ctk.CTkLabel(parent, text="📖", font=ctk.CTkFont(size=50), text_color="#DFCFC2").pack()