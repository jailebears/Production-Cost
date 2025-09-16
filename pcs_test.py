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

    def show_production(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Production", 
                 font=("Arial", 20), bg="white").pack(pady=10, anchor="w", padx=20)

    def show_actual_cost(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Actual Cost", 
                 font=("Arial", 20), bg="white").pack(pady=10, anchor="w", padx=20)
    
    def show_reports(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Reports", 
                 font=("Arial", 20), bg="white").pack(pady=10, anchor="w", padx=20)

    def run(self):
#Start the application
        self.root.mainloop()

if __name__ == "__main__":
    app = ProductionCostingSystem()
    app.run()

