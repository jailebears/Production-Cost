import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk # how to put images beside the text in the sidebar? + search bar icon in production & actual cost

#comments are important, it labels the functions :) PLEASE study everything
class ProductionCostingSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Basic Production Costing System")
        self.root.geometry("800x500")

        self.cost_centers = []  
        self.production_orders = []

        self.create_main_interface()
    
    def create_main_interface(self):
#Create the main GUI interface with buttons and labels
        # sidebar
        self.sidebar = tk.Frame(self.root, width=220, bg="#374050")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(self.sidebar, text="Product\n Costing\n System", 
                 font=("Arial", 18, "bold"), bg="#374050", fg="white").pack(pady=20)

        # main content area
        self.content_frame = tk.Frame(self.root, bg="white")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # sidebar buttons
        tk.Button(self.sidebar, text="Dashboard", width=20, height=2,
                  command=self.show_dashboard).pack(pady=5)
        tk.Button(self.sidebar, text="Cost Center", width=20, height=2,
                  command=self.show_cost_center).pack(pady=5)
        tk.Button(self.sidebar, text="Production", width=20, height=2,
                  command=self.show_production).pack(pady=5)
        tk.Button(self.sidebar, text="Actual Cost", width=20, height=2,
                  command=self.show_actual_cost).pack(pady=5)
        tk.Button(self.sidebar, text="Reports", width=20, height=2,
                  command=self.show_reports).pack(pady=5)

        # opens dashboard on startup
        self.show_dashboard()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Welcome, User!", 
                 font=("Arial", 20), bg="white").pack(pady=10, anchor="w", padx=20)
        
        # create the cards frame
        cards_frame = tk.Frame(self.content_frame, bg="white")
        cards_frame.pack(pady=10)

        # calculate the values for the cards
        total_orders = len(self.production_orders)
        total_planned = sum(order.get("planned_cost", 0.0) for order in self.production_orders)
        total_actual = sum(order.get("actual_cost", 0.0) for order in self.production_orders)
        variance = total_actual - total_planned

        # shortens process of making cards
        def make_card(parent, title, value, row, col):
            card = tk.Frame(parent, bg="white", bd=1, relief="solid", padx=18, pady=12)
            card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")
            tk.Label(card, text=title, font=("Arial", 14, "bold"), bg="white", fg="#374050", anchor="w").pack(fill="x", expand=True)
            tk.Label(card, text=value, font=("Arial", 14), bg="white", fg="#374050", anchor="w").pack(fill="x", expand=True, pady=(6,0))
            return card
        # tina-try kong i-align sa left yung text sa card, pero di ko magawa (?)

        # arrange in 2x2 grid
        make_card(cards_frame, "Total Orders", str(total_orders), row=0, col=0)
        make_card(cards_frame, "Total Planned Cost", f"₱{total_planned:,.2f}", row=0, col=1)
        make_card(cards_frame, "Total Actual Cost", f"₱{total_actual:,.2f}", row=1, col=0)
        make_card(cards_frame, "Variance", f"₱{variance:,.2f}", row=1, col=1)

        # to even out the cards
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        
    def show_cost_center(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Cost Center", 
                 font=("Arial", 20), bg="white").pack(pady=10, anchor="w", padx=20)
        
        cost_center_container = tk.Frame(self.content_frame, bg="#374050")
        cost_center_container.pack(fill="both", expand=True, padx=20, pady=10)

        add_cost_center_frame = tk.Frame(cost_center_container, bg="white", bd=2, relief="groove", padx=10, pady=10)
        add_cost_center_frame.grid(row=0, column=0, sticky="n", padx=10, pady=10)

        tk.Label(add_cost_center_frame, text="Add Cost Center", 
                font=("Arial", 14, "bold"), bg="white", fg="#374050").pack(pady=(0,10))
        tk.Label(add_cost_center_frame, text="Cost Center ID:", bg="white", fg="#374050", anchor="w").pack(fill="x")
        id_entry = tk.Entry(add_cost_center_frame, width=30)
        id_entry.pack(pady=5, fill="x")

        tk.Label(add_cost_center_frame, text="Name:", bg="white", fg="#374050", anchor="w").pack(fill="x")
        name_entry = tk.Entry(add_cost_center_frame, width=30)
        name_entry.pack(pady=5, fill="x")

        tk.Label(add_cost_center_frame, text="Description (Optional):", bg="white", fg="#374050", anchor="w").pack(fill="x")
        desc_entry = tk.Entry(add_cost_center_frame, width=30)
        desc_entry.pack(pady=5, fill="x")

        def save_cost_center():
#Save the new cost center
            cost_center_id = id_entry.get().strip()
            cost_center_name = name_entry.get().strip()
            
            if not cost_center_id or not cost_center_name:
                messagebox.showerror("Error", "Please fill in all fields!")
                return
            
            self.cost_centers.append({
                "id": cost_center_id,
                "name": cost_center_name
            })
            
            messagebox.showinfo("Success", "Cost Center added successfully!")

        tk.Button(add_cost_center_frame, text="Save", bg="#374050", fg="white", command=save_cost_center).pack(pady=10)

        list_frame = tk.Frame(cost_center_container, bg="white", bd=2, relief="groove", padx=10, pady=10)
        list_frame.grid(row=0, column=1, sticky="n", padx=10, pady=10)

        tk.Label(list_frame, text="ID   Name   Description", 
                font=("Arial", 12, "bold"), bg="white", fg="#374050").pack(anchor="w")

    def show_production(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Production", 
                 font=("Arial", 20), bg="white").pack(pady=10, anchor="w", padx=20)
        
        production_container = tk.Frame(self.content_frame, bg="#374050")
        production_container.pack(fill="both", expand=True, padx=20, pady=10)

        production_frame = tk.Frame(production_container, bg="white", bd=2, relief="groove", padx=10, pady=10)
        production_frame.grid(row=0, column=0, sticky="n", padx=10, pady=10)

        tk.Label(production_frame, text="Create Production Order", 
                font=("Arial", 14, "bold"), bg="white", fg="#374050").pack(pady=(0,10))
        tk.Label(production_frame, text="Cost Center ID:", bg="white", fg="#374050", anchor="w").pack(fill="x")
        id_entry = tk.Entry(production_frame, width=30)
        id_entry.pack(pady=5, fill="x")

        tk.Label(production_frame, text="Product Name:", bg="white", fg="#374050", anchor="w").pack(fill="x")
        product_entry = tk.Entry(production_frame, width=30)
        product_entry.pack(pady=5, fill="x")

        tk.Label(production_frame, text="Planned Cost:", bg="white", fg="#374050", anchor="w").pack(fill="x")
        cost_entry = tk.Entry(production_frame, width=30)
        cost_entry.pack(pady=5, fill="x")

        def save_order():
#Save the new production order
            order_id = id_entry.get().strip()
            product_name = product_entry.get().strip()
            planned_cost = cost_entry.get().strip()
            

            print(f"Debug - Order ID: '{order_id}', Product: '{product_name}', Cost: '{planned_cost}'")
            
            if not order_id or not product_name or not planned_cost:
                messagebox.showerror("Error", f"Please fill in all fields!\nOrder ID: '{order_id}'\nProduct: '{product_name}'\nCost: '{planned_cost}'")
                return
            
            try:
                planned_cost_float = float(planned_cost)
            except ValueError:
                messagebox.showerror("Error", "Planned cost must be a number!")
                return
            
            self.production_orders.append({
                "id": order_id,
                "product_name": product_name,
                "planned_cost": planned_cost_float,
                "actual_cost": 0.0
            })
            
            messagebox.showinfo("Success", "Production Order created successfully!")

        tk.Button(production_frame, text="Save", bg="#374050", fg="white", command=save_order).pack(pady=10)

        search_frame = tk.Frame(production_container, bg="white", bd=2, relief="groove", padx=10, pady=10)
        search_frame.grid(row=0, column=1, sticky="n", padx=10, pady=10)
        tk.Label(search_frame, text="Search",
                 font=("Arial", 12, "bold"), bg="white", fg="#374050").pack(pady=(0,10))

        list_frame = tk.Frame(production_container, bg="white", bd=2, relief="groove", padx=10, pady=10)
        list_frame.grid(row=1, column=1, sticky="n", padx=10, pady=10)

        tk.Label(list_frame, text="ID   Name   Description", 
                font=("Arial", 12, "bold"), bg="white", fg="#374050").pack(anchor="w")

    def show_actual_cost(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Actual Cost", 
                 font=("Arial", 20), bg="white").pack(pady=10, anchor="w", padx=20)
        
        actual_cost_container = tk.Frame(self.content_frame, bg="#374050")
        actual_cost_container.pack(fill="both", expand=True, padx=20, pady=10)

        actual_cost_frame = tk.Frame(actual_cost_container, bg="white", bd=2, relief="groove", padx=10, pady=10)
        actual_cost_frame.grid(row=0, column=0, sticky="n", padx=10, pady=10)

        tk.Label(actual_cost_frame, text="Select Production Order", 
                font=("Arial", 14, "bold"), bg="white", fg="#374050").pack(pady=(0,10))
        tk.Label(actual_cost_frame, text="Production Order", bg="white", fg="#374050", anchor="w").pack(fill="x")
        order_var = tk.StringVar()
        order_combo = ttk.Combobox(actual_cost_frame, textvariable=order_var, width=27)

        order_list = [f"{order['id']} - {order['product_name']}" for order in self.production_orders]
        order_combo['values'] = order_list
        order_combo.pack(pady=5, fill="x")

        tk.Label(actual_cost_frame, text="Actual Cost", bg="white", fg="#374050", anchor="w").pack(fill="x")
        cost_entry = tk.Entry(actual_cost_frame, width=30)
        cost_entry.pack(pady=5, fill="x")

        def save_actual_cost():
#Save the actual cost for the selected order
            selected_order = order_var.get()
            actual_cost = cost_entry.get().strip()
            
            if not selected_order or not actual_cost:
                messagebox.showerror("Error", "Please select an order and enter actual cost!")
                return
            
            try:
                actual_cost_float = float(actual_cost)
            except ValueError:
                messagebox.showerror("Error", "Actual cost must be a number!")
                return
            
            order_id = selected_order.split(" - ")[0]  
            for order in self.production_orders:
                if order["id"] == order_id:
                    order["actual_cost"] = actual_cost_float
                    break
            
            messagebox.showinfo("Success", "Actual cost updated successfully!")

        tk.Button(actual_cost_frame, text="Save", bg="#374050", fg="white", command=save_actual_cost).pack(pady=10)

        search_frame = tk.Frame(actual_cost_container, bg="white", bd=2, relief="groove", padx=10, pady=10)
        search_frame.grid(row=0, column=1, sticky="n", padx=10, pady=10)
        tk.Label(search_frame, text="Search",
                 font=("Arial", 12, "bold"), bg="white", fg="#374050").pack(pady=(0,10))

        list_frame = tk.Frame(actual_cost_container, bg="white", bd=2, relief="groove", padx=10, pady=10)
        list_frame.grid(row=1, column=1, sticky="n", padx=10, pady=10)

        tk.Label(list_frame, text="Production Order    Actual Cost", 
                font=("Arial", 12, "bold"), bg="white", fg="#374050").pack(anchor="w")
    
    def show_reports(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Reports", 
                 font=("Arial", 20), bg="white").pack(pady=10, anchor="w", padx=20)
        
        report_container = tk.Frame(self.content_frame, bg="#374050")
        report_container.pack(fill="both", expand=True, padx=20, pady=10)

        report_frame = tk.Frame(report_container, bg="white", bd=2, relief="groove", padx=10, pady=10)
        report_frame.grid(row=0, column=0, sticky="n", padx=10, pady=10)

        tk.Label(report_frame, text="Costing Report", 
                font=("Arial", 14, "bold"), bg="white", fg="#374050").pack(pady=(0,10))
        tk.Label(report_frame, text="Production Order", bg="white", fg="#374050", anchor="w").pack(fill="x")
        order_var = tk.StringVar()
        order_combo = ttk.Combobox(report_frame, textvariable=order_var, width=27)

        order_list = [f"{order['id']} - {order['product_name']}" for order in self.production_orders]
        order_combo['values'] = order_list
        order_combo.pack(pady=5, fill="x")

        list_frame = tk.Frame(report_container, bg="white", bd=2, relief="groove", padx=10, pady=10)
        list_frame.grid(row=1, column=0, sticky="n", padx=10, pady=10)

        tk.Label(list_frame, text="Production Order    Planned Cost     Actual Cost     Variation", 
                font=("Arial", 12, "bold"), bg="white", fg="#374050").pack(anchor="w")

        report_text = tk.Text(report_frame, width=70, height=20)
        report_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        report_content = "PRODUCTION COSTING REPORT\n"
        report_content += "=" * 50 + "\n\n"
        
        report_content += "COST CENTERS:\n"
        report_content += "-" * 20 + "\n"
        if self.cost_centers:
            for cc in self.cost_centers:
                report_content += f"ID: {cc['id']}, Name: {cc['name']}\n"
        else:
            report_content += "No cost centers added yet.\n"
        
        report_content += "\n"
        
        report_content += "PRODUCTION ORDERS:\n"
        report_content += "-" * 20 + "\n"
        if self.production_orders:
            report_content += f"{'Order ID':<10} {'Product':<15} {'Planned':<10} {'Actual':<10} {'Variance':<10}\n"
            report_content += "-" * 65 + "\n"
        
        if self.production_orders:
            total_planned = 0
            total_actual = 0
            
            for order in self.production_orders:
                planned = order['planned_cost']
                actual = order['actual_cost']
                variance = actual - planned 
                
                total_planned += planned
                total_actual += actual
                
                report_content += f"{order['id']:<10} {order['product_name']:<15} ${planned:<9.2f} ${actual:<9.2f} ${variance:<9.2f}\n"
            
            report_content += "-" * 65 + "\n"
            total_variance = total_actual - total_planned
            report_content += f"{'TOTAL':<10} {'':<15} ${total_planned:<9.2f} ${total_actual:<9.2f} ${total_variance:<9.2f}\n"
        else:
            report_content += "No production orders created yet.\n"
        
        report_text.insert(tk.END, report_content)
        report_text.config(state=tk.DISABLED)

    def run(self):
#Start the application
        self.root.mainloop()

if __name__ == "__main__":
    app = ProductionCostingSystem()
    app.run()

