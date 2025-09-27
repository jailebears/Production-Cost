import tkinter as tk
from tkinter import messagebox, ttk
# I removed PIL na since there are no images naman 

class ProductionCostingSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Basic Production Costing System")
        self.root.geometry("1000x620")

        self.colors = {
            "bg_dark": "#1f2733",
            "bg_sidebar": "#2b3442",
            "bg_card": "#ffffff",
            "text_primary": "#0f172a",
            "text_secondary": "#374050",
            "accent": "#3b82f6",
            "accent_muted": "#eff6ff",
            "white": "#ffffff"
        }
        self.root.configure(bg=self.colors["bg_dark"])

        self.cost_centers = []  
        self.production_orders = []
        self.activity_links = []  
        self.planned_details = {}  
        self.actual_details = {}   
        self.activity_types = []  
        self.sales_data = {}       
        
        self.tutorial_shown = {
            "cost_center": False,
            "activity_types": False,
            "planned_cost": False,
            "actual_cost": False,
            "sales_data": False,
            "profitability": False,
            "reports": False
        }

        self.active_page = None
        self.sidebar_buttons = {}

        self._init_styles()

        self.create_main_interface()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def create_main_interface(self):
        self.sidebar = tk.Frame(self.root, width=220, bg=self.colors["bg_sidebar"])
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(self.sidebar, text="Product\n Costing\n System", 
                 font=("Arial", 18, "bold"), bg=self.colors["bg_sidebar"], fg="white", justify="left").pack(pady=20, padx=16, anchor="w")

        self.content_frame = tk.Frame(self.root, bg=self.colors["white"])
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        def add_side_button(key, label, command, icon=""):
            btn = tk.Button(
                self.sidebar,
                text=(f"{icon}  {label}" if icon else label),
                width=20,
                height=2,
                relief=tk.FLAT,
                bg=self.colors["bg_sidebar"],
                fg="#d1d5db",
                activebackground=self.colors["bg_sidebar"],
                activeforeground="#ffffff",
                command=lambda k=key, cmd=command: (cmd(), self._highlight_sidebar(k))
            )
            btn.pack(pady=4, padx=8)
            self.sidebar_buttons[key] = btn

        add_side_button("dashboard", "Dashboard", self.show_dashboard, icon="🏠")
        add_side_button("cost_center", "Cost Center", self.show_cost_center, icon="🏷️")
        add_side_button("activity_types", "Activity Type", self.show_activity_types, icon="🧰")
        add_side_button("planned_cost", "Planned Cost", self.show_planned_cost, icon="🧮")
        add_side_button("production", "Production", self.show_production, icon="🏭")
        add_side_button("actual_cost", "Actual Cost", self.show_actual_cost, icon="💰")
        add_side_button("sales_data", "Sales Data", self.show_sales_data, icon="📈")
        add_side_button("reports", "Reports", self.show_reports, icon="📊")
        add_side_button("profitability", "Profitability", self.show_profitability, icon="💡")

        # footer actions
        tk.Frame(self.sidebar, height=8, bg=self.colors["bg_sidebar"]).pack(fill=tk.X)
        reset_btn = tk.Button(
            self.sidebar,
            text="Reset Data",
            width=20,
            height=2,
            relief=tk.FLAT,
            bg=self.colors["bg_sidebar"],
            fg="#fca5a5",
            activebackground=self.colors["bg_sidebar"],
            activeforeground="#fecaca",
            command=self.reset_data
        )
        reset_btn.pack(side=tk.BOTTOM, pady=8, padx=8)

        self.show_dashboard()
        self._highlight_sidebar("dashboard")

    def _highlight_sidebar(self, key):
        for k, btn in self.sidebar_buttons.items():
            if k == key:
                btn.configure(bg=self.colors["accent"], fg=self.colors["white"]) 
            else:
                btn.configure(bg=self.colors["bg_sidebar"], fg="#d1d5db")
        self.active_page = key

    def _init_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure(
            "Custom.Treeview",
            rowheight=26,
            borderwidth=0,
            relief="flat"
        )
        style.configure(
            "Custom.Treeview.Heading",
            font=("Arial", 10, "bold"),
            padding=(6, 6)
        )
        style.map("Custom.Treeview", background=[("selected", "#e0e7ff")])
        style.configure("Custom.TCombobox", padding=4)

    def reset_data(self):
        if not messagebox.askyesno("Confirm Reset", "This will clear all Cost Centers and Production Orders. Continue?"):
            return
        self.cost_centers = []
        self.production_orders = []
        self.activity_types = []
        self.sales_data = {}
        self.planned_details = {}
        self.actual_details = {}
        self.activity_links = []
        if hasattr(self, "cc_tree") and isinstance(self.cc_tree, ttk.Treeview):
            try:
                # widget may be destroyed when switching tabs; guard calls
                if str(self.cc_tree) in self.root.children or True:
                    for item in self.cc_tree.get_children():
                        self.cc_tree.delete(item)
            except Exception:
                pass
        self.show_dashboard()

    def show_tutorial(self, tab_name, steps):
        if self.tutorial_shown.get(tab_name, False):
            return

        self.tutorial_shown[tab_name] = True
            
        tutorial_window = tk.Toplevel(self.root)
        tutorial_window.title(f"{tab_name.replace('_', ' ').title()} - Tutorial")
        tutorial_window.geometry("500x400")
        tutorial_window.configure(bg=self.colors["white"])
        tutorial_window.transient(self.root)
        tutorial_window.grab_set()
        
        tutorial_window.geometry("+{}+{}".format(
            self.root.winfo_rootx() + 50,
            self.root.winfo_rooty() + 50
        ))
        
        current_step = [0] 
        
        def show_step(step_index):
            for widget in content_frame.winfo_children():
                widget.destroy()
                
            if step_index < len(steps):
                step = steps[step_index]

                tk.Label(content_frame, text=f"Step {step_index + 1} of {len(steps)}", 
                        font=("Arial", 12, "bold"), bg=self.colors["white"], 
                        fg=self.colors["accent"]).pack(pady=(10,5))

                tk.Label(content_frame, text=step["title"], 
                        font=("Arial", 14, "bold"), bg=self.colors["white"], 
                        fg=self.colors["text_primary"]).pack(pady=5)

                desc_label = tk.Label(content_frame, text=step["description"], 
                                    font=("Arial", 11), bg=self.colors["white"], 
                                    fg=self.colors["text_secondary"], wraplength=450, justify="left")
                desc_label.pack(pady=10, padx=20)

                btn_frame = tk.Frame(content_frame, bg=self.colors["white"])
                btn_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)
                
                if step_index > 0:
                    tk.Button(btn_frame, text="← Previous", 
                            command=lambda: (current_step.__setitem__(0, step_index-1), show_step(current_step[0])),
                            bg=self.colors["bg_sidebar"], fg="white", relief=tk.FLAT).pack(side=tk.LEFT)
                
                if step_index < len(steps) - 1:
                    tk.Button(btn_frame, text="Next →", 
                            command=lambda: (current_step.__setitem__(0, step_index+1), show_step(current_step[0])),
                            bg=self.colors["accent"], fg="white", relief=tk.FLAT).pack(side=tk.RIGHT)
                else:
                    tk.Button(btn_frame, text="Start Using!", 
                            command=tutorial_window.destroy,
                            bg=self.colors["accent"], fg="white", relief=tk.FLAT).pack(side=tk.RIGHT)

                tk.Button(btn_frame, text="Skip Tutorial", 
                        command=tutorial_window.destroy,
                        bg=self.colors["white"], fg=self.colors["text_secondary"], relief=tk.FLAT).pack()

        content_frame = tk.Frame(tutorial_window, bg=self.colors["white"])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        show_step(0)
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Welcome, User!", 
                 font=("Arial", 20, "bold"), bg=self.colors["white"], fg=self.colors["text_primary"]).pack(pady=16, anchor="w", padx=20)

        dash_panel = tk.Frame(self.content_frame, bg=self.colors["bg_sidebar"], bd=0)
        dash_panel.pack(fill=tk.X, padx=20, pady=8)
        cards_holder = tk.Frame(dash_panel, bg=self.colors["white"], bd=1, relief="ridge")
        cards_holder.pack(fill=tk.X, padx=12, pady=12)

        cards_frame = tk.Frame(cards_holder, bg=self.colors["white"])
        cards_frame.pack(pady=4, padx=6, fill=tk.X)

        total_orders = len(self.production_orders)
        total_planned = sum(order.get("planned_cost", 0.0) for order in self.production_orders)
        total_actual = sum(order.get("actual_cost", 0.0) for order in self.production_orders)
        variance = total_actual - total_planned

        total_profit = 0.0
        for order in self.production_orders:
            order_id = order.get("id")
            sales_info = self.sales_data.get(order_id, {})
            selling_price = sales_info.get("selling_price", 0.0)
            quantity_sold = sales_info.get("quantity_sold", 0.0)
            revenue = selling_price * quantity_sold
            actual_cost = order.get("actual_cost", 0.0)
            total_profit += (revenue - actual_cost)

        def make_card(parent, title, value, row, col):
            card = tk.Frame(parent, bg=self.colors["bg_card"], bd=1, relief="ridge", padx=18, pady=12, highlightbackground="#e5e7eb", highlightthickness=1)
            card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")
            tk.Label(card, text=title, font=("Arial", 11, "bold"), bg=self.colors["bg_card"], fg=self.colors["text_secondary"], anchor="w").pack(fill="x", expand=True)
            tk.Label(card, text=value, font=("Arial", 16, "bold"), bg=self.colors["bg_card"], fg=self.colors["text_primary"], anchor="w").pack(fill="x", expand=True, pady=(6,2))
            return card

        make_card(cards_frame, "Total Orders", str(total_orders), row=0, col=0)
        make_card(cards_frame, "Total Planned Cost", f"₱{total_planned:,.2f}", row=0, col=1)
        make_card(cards_frame, "Total Actual Cost", f"₱{total_actual:,.2f}", row=1, col=0)
        make_card(cards_frame, "Cost Variance", f"₱{variance:,.2f}", row=1, col=1)
        make_card(cards_frame, "Total Profit", f"₱{total_profit:,.2f}", row=2, col=0)

        profit_status = "Profitable" if total_profit > 0 else "Loss" if total_profit < 0 else "Break-even"
        make_card(cards_frame, "Status", profit_status, row=2, col=1)

        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        self._unsaved_production = False
        
    def show_cost_center(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Cost Center", 
                 font=("Arial", 20, "bold"), bg=self.colors["white"], fg=self.colors["text_primary"]).pack(pady=10, anchor="w", padx=20)

        cc_panel = tk.Frame(self.content_frame, bg=self.colors["bg_sidebar"], bd=0, relief="flat")
        cc_panel.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        form_card = tk.Frame(cc_panel, bg=self.colors["white"], bd=1, relief="ridge")
        form_card.pack(side=tk.LEFT, padx=12, pady=12, anchor="n")
        form = tk.Frame(form_card, bg=self.colors["white"]) 
        form.pack(padx=12, pady=12)

        tk.Label(form, text="Cost Center ID:", bg=self.colors["white"], fg=self.colors["text_secondary"], font=("Arial", 12)).grid(row=0, column=0, pady=5, sticky="w")
        id_entry = ttk.Entry(form, width=32)
        id_entry.grid(row=0, column=1, pady=5, padx=(10,0))

        tk.Label(form, text="Cost Center Name:", bg=self.colors["white"], fg=self.colors["text_secondary"], font=("Arial", 12)).grid(row=1, column=0, pady=5, sticky="w")
        name_entry = ttk.Entry(form, width=32)
        name_entry.grid(row=1, column=1, pady=5, padx=(10,0))

        tk.Label(form, text="Description (Optional):", bg=self.colors["white"], fg=self.colors["text_secondary"], font=("Arial", 12)).grid(row=2, column=0, pady=5, sticky="w")
        desc_entry = ttk.Entry(form, width=32)
        desc_entry.grid(row=2, column=1, pady=5, padx=(10,0))

        def save_cost_center():
            cost_center_id = id_entry.get().strip()
            cost_center_name = name_entry.get().strip()
            if not cost_center_id or not cost_center_name:
                messagebox.showerror("Error", "Please fill in all fields!")
                return
            self.cost_centers.append({
                "id": cost_center_id,
                "name": cost_center_name,
                "description": desc_entry.get().strip()
            })
            messagebox.showinfo("Success", "Cost Center added successfully!")
            id_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
            desc_entry.delete(0, tk.END)
            refresh_cc_table()

        save_btn = tk.Button(form, text="Save", command=save_cost_center, width=10, bg=self.colors["accent"], fg=self.colors["white"], relief=tk.FLAT)
        save_btn.grid(row=3, column=1, pady=10, sticky="e")

        table_card = tk.Frame(cc_panel, bg=self.colors["white"], bd=1, relief="ridge")
        table_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=12, pady=12)
        table_frame = tk.Frame(table_card, bg=self.colors["white"]) 
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("id", "name", "description")
        self.cc_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10, style="Custom.Treeview")
        self.cc_tree.heading("id", text="ID")
        self.cc_tree.heading("name", text="Name")
        self.cc_tree.heading("description", text="Description")
        self.cc_tree.column("id", width=120, anchor="w")
        self.cc_tree.column("name", width=220, anchor="w")
        self.cc_tree.column("description", width=360, anchor="w")
        self.cc_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.cc_tree.yview)
        self.cc_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def refresh_cc_table():
            for item in self.cc_tree.get_children():
                self.cc_tree.delete(item)
            for cc in self.cost_centers:
                self.cc_tree.insert("", tk.END, values=(cc.get("id"), cc.get("name"), cc.get("description", "")))

        refresh_cc_table()

    def show_activity_types(self):
        tutorial_steps = [
            {
                "title": "Welcome to Activity Types!",
                "description": "Activity Types describe what kind of work happens at each cost center. Examples: 'Machining Hours', 'Manual Assembly Time', 'Quality Inspection Hours'."
            },
            {
                "title": "Step 1: Create Activity Types",
                "description": "First, create your custom activity types using the form on the left. Enter a name like 'Custom Machining Hours' and description. This builds your library of activities."
            },
            {
                "title": "Step 2: Assign to Work Centers",
                "description": "Next, link your activity types to specific cost centers with hourly rates. This tells the system how much each type of work costs per hour."
            },
            {
                "title": "Why This Matters",
                "description": "These rates will be used when calculating planned costs for production orders. Make sure your rates reflect actual labor and machine costs!"
            }
        ]
        self.show_tutorial("activity_types", tutorial_steps)
        self.clear_content()
        tk.Label(self.content_frame, text="Activity Type", 
                 font=("Arial", 20, "bold"), bg=self.colors["white"], fg=self.colors["text_primary"]).pack(pady=10, anchor="w", padx=20)

        info_panel = tk.Frame(self.content_frame, bg=self.colors["bg_sidebar"], bd=0)
        info_panel.pack(fill=tk.X, padx=20, pady=(0,10))
        info_card = tk.Frame(info_panel, bg=self.colors["white"], bd=1, relief="ridge")
        info_card.pack(fill=tk.X, padx=12, pady=12)
        info = tk.Label(info_card, justify="left", bg=self.colors["white"], fg=self.colors["text_secondary"],
                        text=("Step 1: First, create custom activity types below.\n"
                              "Step 2: Then assign them to work centers with rates.\n\n"
                              "Activity types describe cost drivers like machine hours, labor hours.\n"
                              "Examples: 'Machinery', 'Labor', 'Quality Control'"))
        info.pack(padx=12, pady=10, anchor="w")

        panel = tk.Frame(self.content_frame, bg=self.colors["bg_sidebar"], bd=0)
        panel.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        left_card = tk.Frame(panel, bg=self.colors["white"], bd=1, relief="ridge")
        left_card.pack(side=tk.LEFT, padx=12, pady=12, anchor="n")

        type_form = tk.Frame(left_card, bg=self.colors["white"]) 
        type_form.pack(padx=12, pady=12)
        
        tk.Label(type_form, text="Create Activity Type", bg=self.colors["white"], fg=self.colors["text_primary"], font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0,10), sticky="w")
        
        tk.Label(type_form, text="Activity Type Name:", bg=self.colors["white"], fg=self.colors["text_secondary"], font=("Arial", 12)).grid(row=1, column=0, pady=5, sticky="w")
        activity_name_entry = ttk.Entry(type_form, width=30)
        activity_name_entry.grid(row=1, column=1, pady=5, padx=(10,0))

        tk.Label(type_form, text="Description:", bg=self.colors["white"], fg=self.colors["text_secondary"], font=("Arial", 12)).grid(row=2, column=0, pady=5, sticky="w")
        activity_desc_entry = ttk.Entry(type_form, width=30)
        activity_desc_entry.grid(row=2, column=1, pady=5, padx=(10,0))

        def save_activity_type():
            name = activity_name_entry.get().strip()
            desc = activity_desc_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter activity type name!")
                return

            for activity in self.activity_types:
                if activity["name"].lower() == name.lower():
                    messagebox.showerror("Error", "Activity type already exists!")
                    return
                    
            self.activity_types.append({"name": name, "description": desc})
            messagebox.showinfo("Success", "Activity type added successfully!")
            activity_name_entry.delete(0, tk.END)
            activity_desc_entry.delete(0, tk.END)
            refresh_activity_types_table()
            refresh_assignment_combo()

        tk.Button(type_form, text="Add Activity Type", command=save_activity_type, width=15, bg=self.colors["accent"], fg=self.colors["white"], relief=tk.FLAT).grid(row=3, column=1, pady=10, sticky="e")

        types_table_frame = tk.Frame(left_card, bg=self.colors["white"])
        types_table_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0,12))
        
        tk.Label(types_table_frame, text="Available Activity Types", bg=self.colors["white"], fg=self.colors["text_primary"], font=("Arial", 12, "bold")).pack(anchor="w", pady=(0,5))
        
        types_columns = ("name", "description")
        self.activity_types_tree = ttk.Treeview(types_table_frame, columns=types_columns, show="headings", height=8, style="Custom.Treeview")
        self.activity_types_tree.heading("name", text="Activity Type")
        self.activity_types_tree.heading("description", text="Description")
        self.activity_types_tree.column("name", width=150, anchor="w")
        self.activity_types_tree.column("description", width=200, anchor="w")
        self.activity_types_tree.pack(fill=tk.BOTH, expand=True)

        separator = tk.Frame(left_card, bg=self.colors["bg_sidebar"], height=2)
        separator.pack(fill=tk.X, padx=12, pady=10)
        
        assign_form = tk.Frame(left_card, bg=self.colors["white"]) 
        assign_form.pack(padx=12, pady=12)

        tk.Label(assign_form, text="Assign to Work Center", bg=self.colors["white"], fg=self.colors["text_primary"], font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0,10), sticky="w")
        
        tk.Label(assign_form, text="Work Center (Cost Center):", bg=self.colors["white"], fg=self.colors["text_secondary"], font=("Arial", 12)).grid(row=1, column=0, pady=5, sticky="w")
        wc_var = tk.StringVar()
        wc_values = [cc.get("id", "") for cc in self.cost_centers]
        wc_combo = ttk.Combobox(assign_form, textvariable=wc_var, width=27, values=wc_values, state="readonly")
        wc_combo.grid(row=1, column=1, pady=5, padx=(10,0))

        tk.Label(assign_form, text="Activity Type:", bg=self.colors["white"], fg=self.colors["text_secondary"], font=("Arial", 12)).grid(row=2, column=0, pady=5, sticky="w")
        atype_var = tk.StringVar()
        atype_combo = ttk.Combobox(assign_form, textvariable=atype_var, width=27, state="readonly")
        atype_combo.grid(row=2, column=1, pady=5, padx=(10,0))

        tk.Label(assign_form, text="Rate (Planned Cost) per hour:", bg=self.colors["white"], fg=self.colors["text_secondary"], font=("Arial", 12)).grid(row=3, column=0, pady=5, sticky="w")
        rate_entry = ttk.Entry(assign_form, width=30)
        rate_entry.grid(row=3, column=1, pady=5, padx=(10,0))

        def refresh_assignment_combo():
            activity_names = [activity["name"] for activity in self.activity_types]
            atype_combo['values'] = activity_names

        def save_link():
            wc = wc_var.get().strip()
            atype = atype_var.get().strip()
            rate = rate_entry.get().strip()
            if not wc or not atype or not rate:
                messagebox.showerror("Error", "Please fill in all fields!")
                return
            ids = {cc.get("id") for cc in self.cost_centers}
            if wc not in ids:
                messagebox.showerror("Error", f"Work Center '{wc}' doesn't exist. Add it in Cost Center.")
                return
            try:
                rate_val = float(rate)
            except ValueError:
                messagebox.showerror("Error", "Rate must be a number!")
                return
            self.activity_links.append({"work_center_id": wc, "activity_type": atype, "rate": rate_val})
            wc_var.set("")
            atype_var.set("")
            rate_entry.delete(0, tk.END)
            refresh_activity_table()

        tk.Button(assign_form, text="Assign", command=save_link, width=10, bg=self.colors["accent"], fg=self.colors["white"], relief=tk.FLAT).grid(row=4, column=1, pady=10, sticky="e")

        right_card = tk.Frame(panel, bg=self.colors["white"], bd=1, relief="ridge")
        right_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=12, pady=12)
        table_frame = tk.Frame(right_card, bg=self.colors["white"]) 
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(table_frame, text="Work Center Assignments", bg=self.colors["white"], fg=self.colors["text_primary"], font=("Arial", 12, "bold")).pack(anchor="w", pady=(0,10))

        columns = ("work_center", "activity_type", "rate")
        self.activity_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15, style="Custom.Treeview")
        self.activity_tree.heading("work_center", text="Work Center")
        self.activity_tree.heading("activity_type", text="Activity Type")
        self.activity_tree.heading("rate", text="Rate (Planned Cost)")
        self.activity_tree.column("work_center", width=180, anchor="w")
        self.activity_tree.column("activity_type", width=180, anchor="w")
        self.activity_tree.column("rate", width=160, anchor="w")
        self.activity_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        sb = ttk.Scrollbar(table_frame, orient="vertical", command=self.activity_tree.yview)
        self.activity_tree.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        def refresh_activity_types_table():
            for item in self.activity_types_tree.get_children():
                self.activity_types_tree.delete(item)
            for activity in self.activity_types:
                self.activity_types_tree.insert("", tk.END, values=(activity.get("name"), activity.get("description", "")))

        def refresh_activity_table():
            for item in self.activity_tree.get_children():
                self.activity_tree.delete(item)
            for link in self.activity_links:
                self.activity_tree.insert("", tk.END, values=(link.get("work_center_id"), link.get("activity_type"), f"₱{link.get('rate', 0):,.2f} per hour"))

        refresh_activity_types_table()
        refresh_activity_table()
        refresh_assignment_combo()

    def show_sales_data(self):
        tutorial_steps = [
            {
                "title": "Welcome to Sales Data!",
                "description": "Enter selling prices and quantities sold for your production orders. This data is used to calculate revenue and profitability."
            },
            {
                "title": "Adding Sales Information",
                "description": "Select a production order, enter the selling price per unit, and quantity sold. The system calculates total revenue automatically."
            },
            {
                "title": "Revenue Calculation",
                "description": "Revenue = Selling Price × Quantity Sold. This revenue is then compared with actual costs to determine profit margins."
            }
        ]
        self.show_tutorial("sales_data", tutorial_steps)
        self.clear_content()
        tk.Label(self.content_frame, text="Sales Data", 
                 font=("Arial", 20, "bold"), bg=self.colors["white"], fg=self.colors["text_primary"]).pack(pady=10, anchor="w", padx=20)

        info_panel = tk.Frame(self.content_frame, bg=self.colors["bg_sidebar"], bd=0)
        info_panel.pack(fill=tk.X, padx=20, pady=(0,10))
        info_card = tk.Frame(info_panel, bg=self.colors["white"], bd=1, relief="ridge")
        info_card.pack(fill=tk.X, padx=12, pady=12)
        info = tk.Label(info_card, justify="left", bg=self.colors["white"], fg=self.colors["text_secondary"],
                        text=("Enter selling price and quantity sold for each production order.\n"
                              "This data is used for profitability analysis."))
        info.pack(padx=12, pady=10, anchor="w")

        panel = tk.Frame(self.content_frame, bg=self.colors["bg_sidebar"], bd=0)
        panel.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        form_card = tk.Frame(panel, bg=self.colors["white"], bd=1, relief="ridge")
        form_card.pack(side=tk.LEFT, padx=12, pady=12, anchor="n")
        form = tk.Frame(form_card, bg=self.colors["white"]) 
        form.pack(padx=12, pady=12)

        tk.Label(form, text="Production Order:", bg=self.colors["white"], fg=self.colors["text_secondary"], font=("Arial", 12)).grid(row=0, column=0, pady=5, sticky="w")
        order_var = tk.StringVar()
        order_combo = ttk.Combobox(form, textvariable=order_var, width=30, state="readonly")
        order_list = [f"{order['id']} - {order['product_name']}" for order in self.production_orders]
        order_combo['values'] = order_list
        order_combo.grid(row=0, column=1, pady=5, padx=(10,0))

        tk.Label(form, text="Selling Price per Unit:", bg=self.colors["white"], fg=self.colors["text_secondary"], font=("Arial", 12)).grid(row=1, column=0, pady=5, sticky="w")
        price_entry = ttk.Entry(form, width=32)
        price_entry.grid(row=1, column=1, pady=5, padx=(10,0))

        tk.Label(form, text="Quantity Sold:", bg=self.colors["white"], fg=self.colors["text_secondary"], font=("Arial", 12)).grid(row=2, column=0, pady=5, sticky="w")
        qty_entry = ttk.Entry(form, width=32)
        qty_entry.grid(row=2, column=1, pady=5, padx=(10,0))

        def save_sales_data():
            selection = order_var.get().strip()
            price = price_entry.get().strip()
            qty = qty_entry.get().strip()
            
            if not selection or not price or not qty:
                messagebox.showerror("Error", "Please fill in all fields!")
                return
                
            try:
                price_val = float(price)
                qty_val = float(qty)
            except ValueError:
                messagebox.showerror("Error", "Price and quantity must be numbers!")
                return
                
            order_id = selection.split(" - ")[0]
            self.sales_data[order_id] = {
                "selling_price": price_val,
                "quantity_sold": qty_val
            }
            
            messagebox.showinfo("Success", "Sales data saved successfully!")
            order_var.set("")
            price_entry.delete(0, tk.END)
            qty_entry.delete(0, tk.END)
            refresh_sales_table()
        
        tutorial_steps = [
            {
                "title": "Welcome to Sales Data!",
                "description": "Enter selling prices and quantities sold for your production orders. This data is used to calculate revenue and profitability."
            },
            {
                "title": "Adding Sales Information",
                "description": "Select a production order, enter the selling price per unit, and quantity sold. The system calculates total revenue automatically."
            },
            {
                "title": "Revenue Calculation",
                "description": "Revenue = Selling Price × Quantity Sold. This revenue is then compared with actual costs to determine profit margins."
            }
        ]
        self.root.after(100, lambda: self.show_tutorial("sales_data", tutorial_steps))

        save_btn = tk.Button(form, text="Save", command=save_sales_data, width=10, bg=self.colors["accent"], fg=self.colors["white"], relief=tk.FLAT)
        save_btn.grid(row=3, column=1, pady=10, sticky="e")

        table_card = tk.Frame(panel, bg=self.colors["white"], bd=1, relief="ridge")
        table_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=12, pady=12)
        table_frame = tk.Frame(table_card, bg=self.colors["white"]) 
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("order_id", "product_name", "selling_price", "quantity_sold", "revenue")
        sales_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12, style="Custom.Treeview")
        sales_tree.heading("order_id", text="Order ID")
        sales_tree.heading("product_name", text="Product Name")
        sales_tree.heading("selling_price", text="Selling Price")
        sales_tree.heading("quantity_sold", text="Quantity Sold")
        sales_tree.heading("revenue", text="Total Revenue")
        
        sales_tree.column("order_id", width=100, anchor="w")
        sales_tree.column("product_name", width=150, anchor="w")
        sales_tree.column("selling_price", width=120, anchor="e")
        sales_tree.column("quantity_sold", width=120, anchor="e")
        sales_tree.column("revenue", width=120, anchor="e")
        
        sales_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=sales_tree.yview)
        sales_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def refresh_sales_table():
            for item in sales_tree.get_children():
                sales_tree.delete(item)
            
            for order in self.production_orders:
                order_id = order.get("id")
                product_name = order.get("product_name", "")
                sales_info = self.sales_data.get(order_id, {})
                selling_price = sales_info.get("selling_price", 0.0)
                quantity_sold = sales_info.get("quantity_sold", 0.0)
                revenue = selling_price * quantity_sold
                
                sales_tree.insert("", tk.END, values=(
                    order_id,
                    product_name,
                    f"₱{selling_price:,.2f}",
                    f"{quantity_sold:,.0f}",
                    f"₱{revenue:,.2f}"
                ))

        refresh_sales_table()

    def show_profitability(self):
        tutorial_steps = [
            {
                "title": "Welcome to Profitability Analysis!",
                "description": "This is where you see the big picture - which orders made money and which ones lost money, and why."
            },
            {
                "title": "Summary Dashboard",
                "description": "The top cards show overall business performance: total revenue, costs, profit, and number of profitable vs loss-making orders."
            },
            {
                "title": "Detailed Analysis",
                "description": "The table below shows each order's profitability with profit margins. Use the filter to focus on profitable or loss-making orders."
            },
            {
                "title": "Key Insights",
                "description": "The insights box analyzes your data and highlights the most and least profitable orders, helping you make better business decisions."
            }
        ]
        self.show_tutorial("profitability", tutorial_steps)
        self.clear_content()
        tk.Label(self.content_frame, text="Profitability Analysis", 
                 font=("Arial", 20, "bold"), bg=self.colors["white"], fg=self.colors["text_primary"]).pack(pady=10, anchor="w", padx=20)

        summary_panel = tk.Frame(self.content_frame, bg=self.colors["bg_sidebar"], bd=0)
        summary_panel.pack(fill=tk.X, padx=20, pady=(0,10))
        summary_card = tk.Frame(summary_panel, bg=self.colors["white"], bd=1, relief="ridge")
        summary_card.pack(fill=tk.X, padx=12, pady=12)
        
        total_revenue = 0.0
        total_cost = 0.0
        total_profit = 0.0
        profitable_orders = 0
        loss_orders = 0
        
        for order in self.production_orders:
            order_id = order.get("id")
            sales_info = self.sales_data.get(order_id, {})
            selling_price = sales_info.get("selling_price", 0.0)
            quantity_sold = sales_info.get("quantity_sold", 0.0)
            revenue = selling_price * quantity_sold
            actual_cost = order.get("actual_cost", 0.0)
            profit = revenue - actual_cost
            
            total_revenue += revenue
            total_cost += actual_cost
            total_profit += profit
            
            if profit > 0:
                profitable_orders += 1
            elif profit < 0:
                loss_orders += 1

        summary_frame = tk.Frame(summary_card, bg=self.colors["white"])
        summary_frame.pack(padx=12, pady=12, fill=tk.X)
        
        def make_summary_card(parent, title, value, color="#000000"):
            card_frame = tk.Frame(parent, bg=self.colors["bg_card"], bd=1, relief="ridge", padx=12, pady=8)
            card_frame.pack(side=tk.LEFT, padx=8, pady=4, fill=tk.BOTH, expand=True)
            tk.Label(card_frame, text=title, font=("Arial", 10, "bold"), bg=self.colors["bg_card"], fg=self.colors["text_secondary"]).pack()
            tk.Label(card_frame, text=value, font=("Arial", 14, "bold"), bg=self.colors["bg_card"], fg=color).pack(pady=(4,0))

        make_summary_card(summary_frame, "Total Revenue", f"₱{total_revenue:,.2f}", "#059669")
        make_summary_card(summary_frame, "Total Cost", f"₱{total_cost:,.2f}", "#dc2626")
        make_summary_card(summary_frame, "Net Profit", f"₱{total_profit:,.2f}", "#059669" if total_profit >= 0 else "#dc2626")
        make_summary_card(summary_frame, "Profitable Orders", f"{profitable_orders}", "#059669")
        make_summary_card(summary_frame, "Loss Orders", f"{loss_orders}", "#dc2626")

        detail_panel = tk.Frame(self.content_frame, bg=self.colors["bg_sidebar"], bd=0)
        detail_panel.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        detail_card = tk.Frame(detail_panel, bg=self.colors["white"], bd=1, relief="ridge")
        detail_card.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        filter_frame = tk.Frame(detail_card, bg=self.colors["white"])
        filter_frame.pack(padx=12, pady=12, anchor="w")
        
        tk.Label(filter_frame, text="Detailed Profitability by Order", font=("Arial", 12, "bold"), bg=self.colors["white"], fg=self.colors["text_primary"]).pack(anchor="w", pady=(0,10))
        
        filter_row = tk.Frame(filter_frame, bg=self.colors["white"])
        filter_row.pack(anchor="w")
        
        tk.Label(filter_row, text="Filter:", bg=self.colors["white"], fg=self.colors["text_secondary"]).pack(side=tk.LEFT)
        
        filter_var = tk.StringVar(value="All Orders")
        filter_combo = ttk.Combobox(filter_row, textvariable=filter_var, width=20, values=["All Orders", "Profitable Only", "Loss Only", "Break-even"], state="readonly")
        filter_combo.pack(side=tk.LEFT, padx=(8,0))

        table_container = tk.Frame(detail_card, bg=self.colors["white"])
        table_container.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0,12))

        columns = ("order_id", "product_name", "revenue", "actual_cost", "profit", "margin", "status")
        profit_tree = ttk.Treeview(table_container, columns=columns, show="headings", height=12, style="Custom.Treeview")
        
        profit_tree.heading("order_id", text="Order ID")
        profit_tree.heading("product_name", text="Product")
        profit_tree.heading("revenue", text="Revenue")
        profit_tree.heading("actual_cost", text="Actual Cost")
        profit_tree.heading("profit", text="Profit")
        profit_tree.heading("margin", text="Margin %")
        profit_tree.heading("status", text="Status")
        
        profit_tree.column("order_id", width=80, anchor="w")
        profit_tree.column("product_name", width=120, anchor="w")
        profit_tree.column("revenue", width=100, anchor="e")
        profit_tree.column("actual_cost", width=100, anchor="e")
        profit_tree.column("profit", width=100, anchor="e")
        profit_tree.column("margin", width=80, anchor="e")
        profit_tree.column("status", width=80, anchor="w")
        
        profit_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        profit_scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=profit_tree.yview)
        profit_tree.configure(yscrollcommand=profit_scrollbar.set)
        profit_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def refresh_profitability_table():
            for item in profit_tree.get_children():
                profit_tree.delete(item)
            
            filter_selection = filter_var.get()
            
            for order in self.production_orders:
                order_id = order.get("id")
                product_name = order.get("product_name", "")
                sales_info = self.sales_data.get(order_id, {})
                selling_price = sales_info.get("selling_price", 0.0)
                quantity_sold = sales_info.get("quantity_sold", 0.0)
                revenue = selling_price * quantity_sold
                actual_cost = order.get("actual_cost", 0.0)
                profit = revenue - actual_cost
                
                margin = (profit / revenue * 100) if revenue > 0 else 0
                
                if profit > 0:
                    status = "Profitable"
                elif profit < 0:
                    status = "Loss"
                else:
                    status = "Break-even"
                
                if filter_selection == "Profitable Only" and profit <= 0:
                    continue
                elif filter_selection == "Loss Only" and profit >= 0:
                    continue
                elif filter_selection == "Break-even" and profit != 0:
                    continue
                
                profit_tree.insert("", tk.END, values=(
                    order_id,
                    product_name,
                    f"₱{revenue:,.2f}",
                    f"₱{actual_cost:,.2f}",
                    f"₱{profit:,.2f}",
                    f"{margin:.1f}%",
                    status
                ))

        filter_combo.bind("<<ComboboxSelected>>", lambda e: refresh_profitability_table())
        refresh_profitability_table()

        insights_frame = tk.Frame(detail_card, bg=self.colors["white"])
        insights_frame.pack(fill=tk.X, padx=12, pady=(0,12))
        
        tk.Label(insights_frame, text="Key Insights", font=("Arial", 12, "bold"), bg=self.colors["white"], fg=self.colors["text_primary"]).pack(anchor="w", pady=(0,5))
        
        insights_text = tk.Text(insights_frame, height=4, bg=self.colors["accent_muted"], fg=self.colors["text_secondary"], wrap=tk.WORD, relief=tk.FLAT)
        insights_text.pack(fill=tk.X)
        
        insights = []
        if total_profit > 0:
            insights.append(f"✓ Overall business is profitable with net profit of ₱{total_profit:,.2f}")
        else:
            insights.append(f"⚠ Business is operating at a loss of ₱{abs(total_profit):,.2f}")
        
        if profitable_orders > 0 and loss_orders > 0:
            insights.append(f"• Mixed performance: {profitable_orders} profitable orders, {loss_orders} loss-making orders")
        elif profitable_orders > 0:
            insights.append(f"• All {profitable_orders} orders are profitable")
        elif loss_orders > 0:
            insights.append(f"• All {loss_orders} orders are making losses - review pricing and costs")
            
        order_profits = []
        for order in self.production_orders:
            order_id = order.get("id")
            sales_info = self.sales_data.get(order_id, {})
            selling_price = sales_info.get("selling_price", 0.0)
            quantity_sold = sales_info.get("quantity_sold", 0.0)
            revenue = selling_price * quantity_sold
            actual_cost = order.get("actual_cost", 0.0)
            profit = revenue - actual_cost
            order_profits.append((order_id, order.get("product_name", ""), profit))
        
        if order_profits:
            order_profits.sort(key=lambda x: x[2], reverse=True)
            best_order = order_profits[0]
            worst_order = order_profits[-1]
            
            if best_order[2] > 0:
                insights.append(f"• Most profitable: {best_order[0]} ({best_order[1]}) with ₱{best_order[2]:,.2f} profit")
            if worst_order[2] < 0:
                insights.append(f"• Biggest loss: {worst_order[0]} ({worst_order[1]}) with ₱{worst_order[2]:,.2f} loss")
        
        insights_text.insert(tk.END, "\n".join(insights))
        insights_text.config(state=tk.DISABLED)
        
        tutorial_steps = [
            {
                "title": "Welcome to Profitability Analysis!",
                "description": "This is where you see the big picture - which orders made money and which ones lost money, and why."
            },
            {
                "title": "Summary Dashboard",
                "description": "The top cards show overall business performance: total revenue, costs, profit, and number of profitable vs loss-making orders."
            },
            {
                "title": "Detailed Analysis",
                "description": "The table below shows each order's profitability with profit margins. Use the filter to focus on profitable or loss-making orders."
            },
            {
                "title": "Key Insights",
                "description": "The insights box analyzes your data and highlights the most and least profitable orders, helping you make better business decisions."
            }
        ]
        self.root.after(100, lambda: self.show_tutorial("profitability", tutorial_steps))

    def show_production(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Production", 
                 font=("Arial", 20, "bold"), bg=self.colors["white"], fg=self.colors["text_primary"]).pack(pady=10, anchor="w", padx=20)

        select_panel = tk.Frame(self.content_frame, bg=self.colors["bg_sidebar"], bd=0)
        select_panel.pack(fill=tk.X, padx=20, pady=10)
        select_card = tk.Frame(select_panel, bg=self.colors["white"], bd=1, relief="ridge")
        select_card.pack(fill=tk.X, padx=12, pady=12)
        srow = tk.Frame(select_card, bg=self.colors["white"]) ; srow.pack(anchor="w")
        tk.Label(srow, text="Select Order:", bg=self.colors["white"], fg=self.colors["text_secondary"]).pack(side=tk.LEFT)
        s_var = tk.StringVar()
        s_combo = ttk.Combobox(srow, textvariable=s_var, width=35, state="readonly",
                               values=[f"{o['id']} - {o['product_name']}" for o in self.production_orders])
        s_combo.pack(side=tk.LEFT, padx=(8,0))

        panel = tk.Frame(self.content_frame, bg=self.colors["bg_sidebar"], bd=0)
        panel.pack(fill=tk.X, padx=20, pady=(0,10))
        card = tk.Frame(panel, bg=self.colors["white"], bd=1, relief="ridge")
        card.pack(fill=tk.X, padx=12, pady=12)
        tk.Label(card, text="Planned Cost (read-only)", bg=self.colors["white"], fg=self.colors["text_primary"], font=("Arial", 12, "bold")).pack(anchor="w")

        cols = ("element","qty","rate","planned")
        p_table = ttk.Treeview(card, columns=cols, show="headings", height=10, style="Custom.Treeview")
        for col, txt, w, anchor in [("element","Cost Element",220,"w"),("qty","Planned Qty",100,"e"),("rate","Rate",140,"e"),("planned","Planned Cost",140,"e")]:
            p_table.heading(col, text=txt); p_table.column(col, width=w, anchor=anchor)
        p_table.pack(fill=tk.X)
        p_total = tk.Label(card, text="Total Planned: ₱0.00", bg=self.colors["white"], fg=self.colors["text_primary"], font=("Arial", 10, "bold"))
        p_total.pack(anchor="e", pady=(4,0))

        def refresh():
            for t in p_table.get_children(): p_table.delete(t)
            sel = s_var.get().strip()
            if not sel:
                p_total.config(text="Total Planned: ₱0.00"); return
            oid = sel.split(" - ")[0]
            rows = self.planned_details.get(oid, [])
            total = 0.0
            for r in rows:
                qty = r.get("qty", 0.0); rate = r.get("rate", 0.0)
                planned = r.get("planned", r.get("planned_cost", 0.0))
                total += planned
                p_table.insert("", tk.END, values=(r.get("element"), f"{qty}", f"₱{rate:,.2f}", f"₱{planned:,.2f}"))
            p_total.config(text=f"Total Planned: ₱{total:,.2f}")

        s_combo.bind("<<ComboboxSelected>>", lambda e: refresh())
        refresh()
        
        a_panel = tk.Frame(self.content_frame, bg=self.colors["bg_sidebar"], bd=0)
        a_panel.pack(fill=tk.X, padx=20, pady=(0,10))
        a_card = tk.Frame(a_panel, bg=self.colors["white"], bd=1, relief="ridge")
        a_card.pack(fill=tk.X, padx=12, pady=12)
        tk.Label(a_card, text="Actual Cost (read-only)", bg=self.colors["white"], fg=self.colors["text_primary"], font=("Arial", 12, "bold")).pack(anchor="w")
        a_cols = ("element","actual")
        a_table = ttk.Treeview(a_card, columns=a_cols, show="headings", height=8, style="Custom.Treeview")
        a_table.heading("element", text="Cost Element"); a_table.column("element", width=240, anchor="w")
        a_table.heading("actual", text="Actual"); a_table.column("actual", width=160, anchor="e")
        a_table.pack(fill=tk.X)
        a_total = tk.Label(a_card, text="Total Actual: ₱0.00", bg=self.colors["white"], fg=self.colors["text_primary"], font=("Arial", 10, "bold"))
        a_total.pack(anchor="e", pady=(4,0))

        def refresh_actual_view():
            for t in a_table.get_children(): a_table.delete(t)
            sel = s_var.get().strip()
            if not sel: a_total.config(text="Total Actual: ₱0.00"); return
            oid = sel.split(" - ")[0]
            rows = self.actual_details.get(oid, [])
            total = 0.0
            for r in rows:
                total += r.get('actual', 0.0)
                a_table.insert("", tk.END, values=(r.get('element'), f"₱{r.get('actual',0.0):,.2f}"))
            a_total.config(text=f"Total Actual: ₱{total:,.2f}")

        s_combo.bind("<<ComboboxSelected>>", lambda e: (refresh(), refresh_actual_view()))
        refresh_actual_view()

    def show_actual_cost(self):
        tutorial_steps = [
            {
                "title": "Welcome to Actual Costs!",
                "description": "After production is complete, record the real costs that were incurred. This lets you compare actual vs planned costs."
            },
            {
                "title": "Recording Actual Costs",
                "description": "Select a production order, choose the cost element, and enter the actual amount spent. You can add multiple entries for the same element."
            },
            {
                "title": "Removing Mistakes",
                "description": "Made an error? Select a row in the table and click 'Remove Selected' to delete it. The total will update automatically."
            },
            {
                "title": "Variance Analysis",
                "description": "The system compares your actual costs with planned costs to show variances - helping you understand where you went over or under budget."
            }
        ]
        self.show_tutorial("actual_cost", tutorial_steps)
        self.clear_content()
        tk.Label(self.content_frame, text="Actual Cost", 
                 font=("Arial", 20, "bold"), bg=self.colors["white"], fg=self.colors["text_primary"]).pack(pady=10, anchor="w", padx=20)

        panel = tk.Frame(self.content_frame, bg=self.colors["bg_sidebar"], bd=0)
        panel.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        card = tk.Frame(panel, bg=self.colors["white"], bd=1, relief="ridge")
        card.pack(fill=tk.X, padx=12, pady=12)

        form = tk.Frame(card, bg=self.colors["white"]) 
        form.pack(padx=12, pady=12, anchor="w")

        tk.Label(form, text="Select Production Order:", bg=self.colors["white"], fg=self.colors["text_secondary"], font=("Arial", 12)).grid(row=0, column=0, pady=5, sticky="w")
        order_var = tk.StringVar()
        order_combo = ttk.Combobox(form, textvariable=order_var, width=27, state="readonly")
        order_list = [f"{order['id']} - {order['product_name']}" for order in self.production_orders]
        order_combo['values'] = order_list
        order_combo.grid(row=0, column=1, pady=5, padx=(10,0))

        tk.Label(form, text="Cost Element:", bg=self.colors["white"], fg=self.colors["text_secondary"], font=("Arial", 12)).grid(row=1, column=0, pady=5, sticky="w")
        elem_var = tk.StringVar(); elem_combo = ttk.Combobox(form, textvariable=elem_var, width=27, state="readonly")
        elem_combo.grid(row=1, column=1, pady=5, padx=(10,0))
        tk.Label(form, text="Actual Cost:", bg=self.colors["white"], fg=self.colors["text_secondary"], font=("Arial", 12)).grid(row=2, column=0, pady=5, sticky="w")
        cost_entry = ttk.Entry(form, width=30)
        cost_entry.grid(row=2, column=1, pady=5, padx=(10,0))

        a_cols = ("element","actual")
        a_table = ttk.Treeview(card, columns=a_cols, show="headings", height=10, style="Custom.Treeview")
        a_table.heading("element", text="Cost Element"); a_table.column("element", width=220, anchor="w")
        a_table.heading("actual", text="Actual Cost"); a_table.column("actual", width=140, anchor="e")
        a_table.pack(fill=tk.X, padx=12, pady=(6,0))
        a_total = tk.Label(card, text="Total Actual: ₱0.00", bg=self.colors["white"], fg=self.colors["text_primary"], font=("Arial", 10, "bold"))
        a_total.pack(anchor="e", padx=12, pady=(4,0))
        
        def remove_selected_actual():
            selected = a_table.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a row to remove.")
                return
            
            sel = order_var.get().strip()
            if not sel:
                return
            oid = sel.split(" - ")[0]
            
            item_values = a_table.item(selected[0])['values']
            element_to_remove = item_values[0]
            actual_to_remove = float(item_values[1].replace('₱', '').replace(',', ''))
            
            if oid in self.actual_details:
                for i, item in enumerate(self.actual_details[oid]):
                    if item['element'] == element_to_remove and item['actual'] == actual_to_remove:
                        self.actual_details[oid].pop(i)
                        break
                
                total = sum(item['actual'] for item in self.actual_details[oid])
                for o in self.production_orders:
                    if o.get('id') == oid:
                        o['actual_cost'] = total
                        break
                
                a_table.delete(selected[0])
                a_total.config(text=f"Total Actual: ₱{total:,.2f}")

        remove_actual_btn = tk.Button(card, text="Remove Selected Entry", command=remove_selected_actual, 
                                    bg="#dc2626", fg="white", relief=tk.FLAT)
        remove_actual_btn.pack(anchor="e", padx=12, pady=4)

        def refresh_elements():
            sel = order_var.get().strip()
            if not sel:
                elem_combo['values'] = []
                for item in a_table.get_children():
                    a_table.delete(item)
                a_total.config(text="Total Actual: ₱0.00")
                return
            oid = sel.split(" - ")[0]
            elems = [r.get('element') for r in self.planned_details.get(oid, [])]
            elem_combo['values'] = elems
            
            for item in a_table.get_children():
                a_table.delete(item)
            
            existing_actuals = self.actual_details.get(oid, [])
            total = 0.0
            for actual_entry in existing_actuals:
                total += actual_entry.get('actual', 0.0)
                a_table.insert("", tk.END, values=(actual_entry.get('element'), f"₱{actual_entry.get('actual', 0.0):,.2f}"))
            a_total.config(text=f"Total Actual: ₱{total:,.2f}")

        def add_actual():
            sel = order_var.get().strip()
            if not sel:
                messagebox.showerror("Error", "Select an order first.")
                return
            oid = sel.split(" - ")[0]
            el = elem_var.get().strip(); val = cost_entry.get().strip()
            if not el or not val:
                messagebox.showerror("Error", "Select element and enter actual cost.")
                return
            try:
                v = float(val)
            except ValueError:
                messagebox.showerror("Error", "Actual cost must be a number.")
                return
            self.actual_details.setdefault(oid, [])
            self.actual_details[oid].append({"element": el, "actual": v})
            total = sum(item['actual'] for item in self.actual_details[oid])
            for o in self.production_orders:
                if o.get('id') == oid:
                    o['actual_cost'] = total
                    break
            a_table.insert("", tk.END, values=(el, f"₱{v:,.2f}"))
            a_total.config(text=f"Total Actual: ₱{total:,.2f}")
            cost_entry.delete(0, tk.END)

        order_combo.bind("<<ComboboxSelected>>", lambda e: refresh_elements())
        tk.Button(form, text="Add Actual", command=add_actual, width=12, bg=self.colors["accent"], fg=self.colors["white"], relief=tk.FLAT).grid(row=3, column=1, pady=10, sticky="e")
        
        refresh_elements()
        
        if not self.tutorial_shown.get("actual_cost", False):
            tutorial_steps = [
                {
                    "title": "Welcome to Actual Costs!",
                    "description": "After production is complete, record the real costs that were incurred. This lets you compare actual vs planned costs."
                },
                {
                    "title": "Recording Actual Costs",
                    "description": "Select a production order, choose the cost element, and enter the actual amount spent. You can add multiple entries for the same element."
                },
                {
                    "title": "Removing Mistakes",
                    "description": "Made an error? Select a row in the table and click 'Remove Selected' to delete it. The total will update automatically."
                },
                {
                    "title": "Variance Analysis",
                    "description": "The system compares your actual costs with planned costs to show variances - helping you understand where you went over or under budget."
                }
            ]
            self.root.after(100, lambda: self.show_tutorial("actual_cost", tutorial_steps))
    
    def show_reports(self):
        tutorial_steps = [
            {
                "title": "Welcome to Reports!",
                "description": "Compare planned vs actual costs for each production order. This helps you understand where you went over or under budget."
            },
            {
                "title": "Variance Analysis",
                "description": "Select an order to see detailed variance analysis by cost element. Positive variance means you spent more than planned; negative means you saved money."
            },
            {
                "title": "Using the Data",
                "description": "Use these reports to improve future planning. If you consistently go over budget on certain elements, adjust your planned rates accordingly."
            }
        ]
        self.show_tutorial("reports", tutorial_steps)
        self.clear_content()
        tk.Label(self.content_frame, text="Reports", 
                 font=("Arial", 20, "bold"), bg=self.colors["white"], fg=self.colors["text_primary"]).pack(pady=10, anchor="w", padx=20)

        panel = tk.Frame(self.content_frame, bg=self.colors["bg_sidebar"], bd=0, relief="flat")
        panel.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        card = tk.Frame(panel, bg=self.colors["white"], bd=1, relief="ridge")
        card.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        filter_frame = tk.Frame(card, bg=self.colors["white"]) 
        filter_frame.pack(padx=14, pady=14, anchor="w")

        tk.Label(filter_frame, text="Costing Report", font=("Arial", 10, "bold"), bg=self.colors["white"], fg=self.colors["text_secondary"]).grid(row=0, column=0, sticky="w")
        tk.Label(filter_frame, text="Select Production Order", font=("Arial", 9), bg=self.colors["white"], fg=self.colors["text_secondary"]).grid(row=1, column=0, sticky="w")
        report_order_var = tk.StringVar()
        order_values = [f"{o['id']} - {o['product_name']}" for o in self.production_orders]
        order_combo = ttk.Combobox(filter_frame, textvariable=report_order_var, width=35, values=order_values, state="readonly", style="Custom.TCombobox")
        order_combo.grid(row=1, column=1, padx=(8,0))

        table_container = tk.Frame(card, bg=self.colors["white"], bd=0)
        table_container.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0,14))

        columns = ("element", "planned", "actual", "variance")
        report_tree = ttk.Treeview(table_container, columns=columns, show="headings", height=10, style="Custom.Treeview")
        report_tree.heading("element", text="Cost Element")
        report_tree.heading("planned", text="Planned")
        report_tree.heading("actual", text="Actual")
        report_tree.heading("variance", text="Variance")
        report_tree.column("element", width=240, anchor="w")
        report_tree.column("planned", width=120, anchor="e")
        report_tree.column("actual", width=120, anchor="e")
        report_tree.column("variance", width=120, anchor="e")
        report_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        sb = ttk.Scrollbar(table_container, orient="vertical", command=report_tree.yview)
        report_tree.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        total_row = tk.Frame(card, bg=self.colors["white"]) 
        total_row.pack(fill=tk.X, padx=14, pady=(4,14))
        total_label = tk.Label(total_row, text="TOTAL:", bg=self.colors["white"], fg=self.colors["text_secondary"], font=("Arial", 10, "bold"))
        total_label.pack(side=tk.LEFT)
        total_planned_lbl = tk.Label(total_row, text="₱0", bg=self.colors["white"], fg=self.colors["text_secondary"], width=14, anchor="e")
        total_actual_lbl = tk.Label(total_row, text="₱0", bg=self.colors["white"], fg=self.colors["text_secondary"], width=14, anchor="e")
        total_var_lbl = tk.Label(total_row, text="₱0", bg=self.colors["white"], fg=self.colors["text_secondary"], width=14, anchor="e")
        total_var_lbl.pack(side=tk.RIGHT)
        total_actual_lbl.pack(side=tk.RIGHT)
        total_planned_lbl.pack(side=tk.RIGHT)

        def refresh_table():
            for item in report_tree.get_children():
                report_tree.delete(item)
            total_planned = 0.0
            total_actual = 0.0
            selection = report_order_var.get().strip()
            if not selection:
                return
            oid = selection.split(" - ")[0]
            planned_rows = self.planned_details.get(oid, [])
            actual_rows = self.actual_details.get(oid, [])
            element_to_actual = {}
            for a in actual_rows:
                element_to_actual[a.get('element')] = element_to_actual.get(a.get('element'), 0.0) + float(a.get('actual', 0.0))
            for r in planned_rows:
                elem = r.get('element')
                planned = float(r.get('planned', r.get('planned_cost', 0.0)))
                actual = float(element_to_actual.get(elem, 0.0))
                variance = actual - planned
                report_tree.insert("", tk.END, values=(elem, f"₱{planned:,.2f}", f"₱{actual:,.2f}", f"₱{variance:,.2f}"))
                total_planned += planned
                total_actual += actual
            total_var = total_actual - total_planned
            total_planned_lbl.config(text=f"₱{total_planned:,.2f}")
            total_actual_lbl.config(text=f"₱{total_actual:,.2f}")
            total_var_lbl.config(text=f"₱{total_var:,.2f}")

        order_combo.bind("<<ComboboxSelected>>", lambda e: refresh_table())
        refresh_table()
        
        tutorial_steps = [
            {
                "title": "Welcome to Reports!",
                "description": "Compare planned vs actual costs for each production order. This helps you understand where you went over or under budget."
            },
            {
                "title": "Variance Analysis",
                "description": "Select an order to see detailed variance analysis by cost element. Positive variance means you spent more than planned; negative means you saved money."
            },
            {
                "title": "Using the Data",
                "description": "Use these reports to improve future planning. If you consistently go over budget on certain elements, adjust your planned rates accordingly."
            }
        ]
        self.root.after(100, lambda: self.show_tutorial("reports", tutorial_steps))

    def show_planned_cost(self):
        tutorial_steps = [
            {
                "title": "Welcome to Planned Costs!",
                "description": "Here you create production orders and estimate how much they should cost. This becomes your budget for each order."
            },
            {
                "title": "Creating an Order",
                "description": "Enter an Order ID (like 'ID-2025-001') and Product Name. These identify your production order."
            },
            {
                "title": "Adding Cost Elements",
                "description": "For each order, add cost elements like 'Machining', 'Raw Materials', etc. Enter planned quantity and rate per unit/hour."
            },
            {
                "title": "Planning Tips",
                "description": "Be realistic with quantities and rates. Use your activity type rates from the previous tab. You can add/remove rows before saving."
            },
            {
                "title": "Saving & Clearing",
                "description": "Click 'Save Planned Total' to save the order. The form will clear automatically so you can create the next order."
            }
        ]
        self.show_tutorial("planned_cost", tutorial_steps)
        self.clear_content()
        tk.Label(self.content_frame, text="Planned Cost", 
                 font=("Arial", 20, "bold"), bg=self.colors["white"], fg=self.colors["text_primary"]).pack(pady=10, anchor="w", padx=20)

        panel = tk.Frame(self.content_frame, bg=self.colors["bg_sidebar"], bd=0)
        panel.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        card = tk.Frame(panel, bg=self.colors["white"], bd=1, relief="ridge")
        card.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        header = tk.Frame(card, bg=self.colors["white"]) ; header.pack(padx=12, pady=8, anchor="w")
        tk.Label(header, text="Order ID:", bg=self.colors["white"], fg=self.colors["text_secondary"]).grid(row=0, column=0)
        order_id_var = tk.StringVar(); ttk.Entry(header, textvariable=order_id_var, width=18).grid(row=0, column=1, padx=(6,16))
        tk.Label(header, text="Product Name:", bg=self.colors["white"], fg=self.colors["text_secondary"]).grid(row=0, column=2)
        product_var = tk.StringVar(); ttk.Entry(header, textvariable=product_var, width=22).grid(row=0, column=3, padx=(6,16))

        p_form = tk.Frame(card, bg=self.colors["white"]) ; p_form.pack(padx=12, pady=6, anchor="w")
        tk.Label(p_form, text="Cost Element:", bg=self.colors["white"], fg=self.colors["text_secondary"]).grid(row=0, column=0)
        elem_var = tk.StringVar(); ttk.Entry(p_form, textvariable=elem_var, width=22).grid(row=0, column=1, padx=(6,12))
        tk.Label(p_form, text="Planned Qty:", bg=self.colors["white"], fg=self.colors["text_secondary"]).grid(row=0, column=2)
        qty_var = tk.StringVar(); ttk.Entry(p_form, textvariable=qty_var, width=10).grid(row=0, column=3, padx=(6,12))
        tk.Label(p_form, text="Rate (per unit/hr):", bg=self.colors["white"], fg=self.colors["text_secondary"]).grid(row=0, column=4)
        rate_var = tk.StringVar(); ttk.Entry(p_form, textvariable=rate_var, width=12).grid(row=0, column=5, padx=(6,12))
        add_btn = tk.Button(p_form, text="Add") ; add_btn.grid(row=0, column=6)

        columns = ("element","qty","rate","planned")
        table = ttk.Treeview(card, columns=columns, show="headings", height=10, style="Custom.Treeview")
        for col, txt, w, anchor in [("element","Cost Element",220,"w"),("qty","Planned Qty",100,"e"),("rate","Rate",140,"e"),("planned","Planned Cost",140,"e")]:
            table.heading(col, text=txt); table.column(col, width=w, anchor=anchor)
        table.pack(fill=tk.BOTH, expand=True, padx=12)

        total_lbl = tk.Label(card, text="Total Planned: ₱0.00", bg=self.colors["white"], fg=self.colors["text_primary"], font=("Arial", 10, "bold"))
        total_lbl.pack(anchor="e", padx=12, pady=(4,0))

        rows = []

        def add_row():
            e = elem_var.get().strip(); q = qty_var.get().strip(); r = rate_var.get().strip()
            if not e or not q or not r:
                messagebox.showerror("Error", "Enter element, qty and rate.")
                return
            try:
                qf = float(q); rf = float(r)
            except ValueError:
                messagebox.showerror("Error", "Qty and rate must be numbers.")
                return
            planned = qf * rf
            rows.append({"element": e, "qty": qf, "rate": rf, "planned": planned})
            table.insert("", tk.END, values=(e, f"{qf}", f"₱{rf:,.2f}", f"₱{planned:,.2f}"))
            elem_var.set(""); qty_var.set(""); rate_var.set("")
            total = sum(rw["planned"] for rw in rows)
            total_lbl.config(text=f"Total Planned: ₱{total:,.2f}")

        def remove_selected_row():
            selected = table.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a row to remove.")
                return
            
            item_values = table.item(selected[0])['values']
            element_to_remove = item_values[0]
            
            table.delete(selected[0])
            
            for i, row in enumerate(rows):
                if row['element'] == element_to_remove:
                    rows.pop(i)
                    break
            
            total = sum(rw["planned"] for rw in rows)
            total_lbl.config(text=f"Total Planned: ₱{total:,.2f}")

        add_btn.configure(command=add_row)
        
        remove_btn = tk.Button(p_form, text="Remove Selected", bg="#dc2626", fg="white", relief=tk.FLAT)
        remove_btn.grid(row=0, column=7, padx=(5,0))
        remove_btn.configure(command=remove_selected_row)

        def save_planned():
            oid = order_id_var.get().strip(); pname = product_var.get().strip()
            if not oid or not pname:
                messagebox.showerror("Error", "Enter Order ID and Product Name.")
                return
            if not rows:
                messagebox.showerror("Error", "Add at least one cost element before saving.")
                return
            total = sum(rw["planned"] for rw in rows)
            self.planned_details[oid] = list(rows)
            for o in self.production_orders:
                if o.get("id") == oid:
                    o["product_name"] = pname
                    o["planned_cost"] = total
                    break
            else:
                self.production_orders.append({"id": oid, "product_name": pname, "cost_center_id": "", "planned_cost": total, "actual_cost": 0.0})
            messagebox.showinfo("Saved", f"Planned total saved for order {oid}: ₱{total:,.2f}")
            
            order_id_var.set("")
            product_var.set("")
            rows.clear()
            for item in table.get_children():
                table.delete(item)
            total_lbl.config(text="Total Planned: ₱0.00")

        action_row = tk.Frame(card, bg=self.colors["white"]) ; action_row.pack(fill=tk.X, padx=12, pady=(8,4))
        tk.Button(action_row, text="Save Planned Total", command=save_planned, bg=self.colors["accent"], fg=self.colors["white"], relief=tk.FLAT).pack(anchor="e")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ProductionCostingSystem()
    app.run()