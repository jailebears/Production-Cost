import tkinter as tk
from tkinter import messagebox, ttk

#comments are important, it labels the functions :)
class ProductionCostingSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Basic Production Costing System")
        self.root.geometry("500x400")
        
        self.cost_centers = []  
        self.production_orders = []  
        
        self.create_main_interface()
    
    def create_main_interface(self):
#Create the main GUI interface with buttons and labels
        title_label = tk.Label(self.root, text="Production Costing System", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        add_cost_center_btn = tk.Button(button_frame, text="Add Cost Center", 
                                       command=self.add_cost_center_window,
                                       width=20, height=2)
        add_cost_center_btn.pack(pady=5)
        
        create_order_btn = tk.Button(button_frame, text="Create Production Order", 
                                    command=self.create_order_window,
                                    width=20, height=2)
        create_order_btn.pack(pady=5)
        
        enter_costs_btn = tk.Button(button_frame, text="Enter Actual Costs", 
                                   command=self.enter_costs_window,
                                   width=20, height=2)
        enter_costs_btn.pack(pady=5)
        
        show_report_btn = tk.Button(button_frame, text="Show Report", 
                                   command=self.show_report_window,
                                   width=20, height=2)
        show_report_btn.pack(pady=5)
    
    
    def add_cost_center_window(self):
#Open a window to add a new cost center
        window = tk.Toplevel(self.root)
        window.title("Add Cost Center")
        window.geometry("300x150")
        
        tk.Label(window, text="Cost Center ID:").pack(pady=5)
        id_entry = tk.Entry(window, width=30)
        id_entry.pack(pady=5)
        
        tk.Label(window, text="Cost Center Name:").pack(pady=5)
        name_entry = tk.Entry(window, width=30)
        name_entry.pack(pady=5)
        
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
            window.destroy()
        
        save_btn = tk.Button(window, text="Save", command=save_cost_center)
        save_btn.pack(pady=10)
    
    def create_order_window(self):
#Open a window to create a new production order
        window = tk.Toplevel(self.root)
        window.title("Create Production Order")
        window.geometry("300x250")
        
        tk.Label(window, text="Order ID:").pack(pady=5)
        id_entry = tk.Entry(window, width=30)
        id_entry.pack(pady=5)
        
        tk.Label(window, text="Product Name:").pack(pady=5)
        product_entry = tk.Entry(window, width=30)
        product_entry.pack(pady=5)
        
        tk.Label(window, text="Planned Cost:").pack(pady=5)
        cost_entry = tk.Entry(window, width=30)
        cost_entry.pack(pady=5)
        
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
            window.destroy()
        
        save_btn = tk.Button(window, text="Save", command=save_order)
        save_btn.pack(pady=10)
    
    def enter_costs_window(self):
        """Open a window to enter actual costs for a production order"""
        window = tk.Toplevel(self.root)
        window.title("Enter Actual Costs")
        window.geometry("300x200")
        
        tk.Label(window, text="Select Production Order:").pack(pady=5)
        order_var = tk.StringVar()
        order_combo = ttk.Combobox(window, textvariable=order_var, width=27)
        
        order_list = [f"{order['id']} - {order['product_name']}" for order in self.production_orders]
        order_combo['values'] = order_list
        order_combo.pack(pady=5)
        
        tk.Label(window, text="Actual Cost:").pack(pady=5)
        cost_entry = tk.Entry(window, width=30)
        cost_entry.pack(pady=5)
        
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
            window.destroy()
        
        save_btn = tk.Button(window, text="Save", command=save_actual_cost)
        save_btn.pack(pady=10)
    
    def show_report_window(self):
        """Open a window to show the costing report"""
        window = tk.Toplevel(self.root)
        window.title("Production Costing Report")
        window.geometry("600x400")
        
        report_text = tk.Text(window, width=70, height=20)
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
        
        close_btn = tk.Button(window, text="Close", command=window.destroy)
        close_btn.pack(pady=10)
    
    def run(self):
#Start the application
        self.root.mainloop()

if __name__ == "__main__":
    app = ProductionCostingSystem()
    app.run()

