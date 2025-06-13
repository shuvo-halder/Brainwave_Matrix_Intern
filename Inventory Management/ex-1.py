import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("800x600")

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.db_conn = sqlite3.connect('inventory.db')
        self.create_tables()

        self.logged_in_user = None
        self.create_login_screen()

    def create_tables(self):
        cursor = self.db_conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL
            )
        ''')
        self.db_conn.commit()

    def create_login_screen(self):
        self.clear_frame()

        login_frame = ttk.Frame(self.root, padding="20")
        login_frame.pack(expand=True)

        ttk.Label(login_frame, text="Username:", font=("Helvetica", 12)).grid(row=0, column=0, pady=5, sticky="w")
        self.username_entry = ttk.Entry(login_frame, width=30)
        self.username_entry.grid(row=0, column=1, pady=5)

        ttk.Label(login_frame, text="Password:", font=("Helvetica", 12)).grid(row=1, column=0, pady=5, sticky="w")
        self.password_entry = ttk.Entry(login_frame, show="*", width=30)
        self.password_entry.grid(row=1, column=1, pady=5)

        ttk.Button(login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(login_frame, text="Register", command=self.create_register_screen).grid(row=3, column=0, columnspan=2)

    def create_register_screen(self):
        self.clear_frame()

        register_frame = ttk.Frame(self.root, padding="20")
        register_frame.pack(expand=True)

        ttk.Label(register_frame, text="New Username:", font=("Helvetica", 12)).grid(row=0, column=0, pady=5, sticky="w")
        self.new_username_entry = ttk.Entry(register_frame, width=30)
        self.new_username_entry.grid(row=0, column=1, pady=5)

        ttk.Label(register_frame, text="New Password:", font=("Helvetica", 12)).grid(row=1, column=0, pady=5, sticky="w")
        self.new_password_entry = ttk.Entry(register_frame, show="*", width=30)
        self.new_password_entry.grid(row=1, column=1, pady=5)

        ttk.Button(register_frame, text="Register", command=self.register).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(register_frame, text="Back to Login", command=self.create_login_screen).grid(row=3, column=0, columnspan=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            self.logged_in_user = username
            self.create_main_screen()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def register(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            cursor = self.db_conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.db_conn.commit()
            messagebox.showinfo("Success", "Registration successful. Please login.")
            self.create_login_screen()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")

    def create_main_screen(self):
        self.clear_frame()

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Product Entry Form
        form_frame = ttk.LabelFrame(main_frame, text="Product Information", padding="10")
        form_frame.pack(fill="x", pady=10)

        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Quantity:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.quantity_entry = ttk.Entry(form_frame)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Price:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.price_entry = ttk.Entry(form_frame)
        self.price_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        form_frame.columnconfigure(1, weight=1)

        # Action Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=5)

        ttk.Button(button_frame, text="Add Product", command=self.add_product).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Update Product", command=self.update_product).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Product", command=self.delete_product).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear Fields", command=self.clear_fields).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Logout", command=self.logout).pack(side="right", padx=5)

        # Product List
        list_frame = ttk.LabelFrame(main_frame, text="Product List", padding="10")
        list_frame.pack(fill="both", expand=True, pady=10)

        self.tree = ttk.Treeview(list_frame, columns=("ID", "Name", "Quantity", "Price"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")
        
        self.tree.column("ID", width=50)
        self.tree.column("Name", width=200)
        self.tree.column("Quantity", width=100)
        self.tree.column("Price", width=100)
        
        self.tree.pack(fill="both", expand=True, side="left")
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self.on_item_select)
        
        # Reports
        report_frame = ttk.LabelFrame(main_frame, text="Reports", padding="10")
        report_frame.pack(fill="x", pady=10)
        
        ttk.Button(report_frame, text="Low Stock Alert (<=10)", command=self.low_stock_report).pack(side="left", padx=5)

        self.load_products()

    def on_item_select(self, event):
        selected_items = self.tree.selection()
        if not selected_items:
            return
            
        selected_item = selected_items[0]
        item = self.tree.item(selected_item)
        record = item['values']
        
        self.clear_fields()
        self.name_entry.insert(0, record[1])
        self.quantity_entry.insert(0, record[2])
        self.price_entry.insert(0, record[3])

    def add_product(self):
        name = self.name_entry.get()
        quantity_str = self.quantity_entry.get()
        price_str = self.price_entry.get()
        
        if not all([name, quantity_str, price_str]):
            messagebox.showerror("Error", "All fields are required.")
            return
            
        try:
            quantity = int(quantity_str)
            price = float(price_str)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer and Price must be a number.")
            return

        cursor = self.db_conn.cursor()
        cursor.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
        self.db_conn.commit()
        
        self.load_products()
        self.clear_fields()
        messagebox.showinfo("Success", "Product added successfully.")
        
    def update_product(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select a product to update.")
            return
            
        selected_item = selected_items[0]
        product_id = self.tree.item(selected_item)['values'][0]

        name = self.name_entry.get()
        quantity_str = self.quantity_entry.get()
        price_str = self.price_entry.get()

        if not all([name, quantity_str, price_str]):
            messagebox.showerror("Error", "All fields are required.")
            return
            
        try:
            quantity = int(quantity_str)
            price = float(price_str)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer and Price must be a number.")
            return

        cursor = self.db_conn.cursor()
        cursor.execute("UPDATE products SET name = ?, quantity = ?, price = ? WHERE id = ?", (name, quantity, price, product_id))
        self.db_conn.commit()
        
        self.load_products()
        self.clear_fields()
        messagebox.showinfo("Success", "Product updated successfully.")

    def delete_product(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select a product to delete.")
            return

        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?"):
            return
            
        selected_item = selected_items[0]
        product_id = self.tree.item(selected_item)['values'][0]

        cursor = self.db_conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        self.db_conn.commit()
        
        self.load_products()
        self.clear_fields()
        messagebox.showinfo("Success", "Product deleted successfully.")
        
    def low_stock_report(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT name, quantity FROM products WHERE quantity <= 10")
        low_stock_products = cursor.fetchall()
        
        if not low_stock_products:
            messagebox.showinfo("Low Stock Report", "No products with low stock.")
            return
            
        report_text = "Low Stock Products (Quantity <= 10):\n\n"
        for name, quantity in low_stock_products:
            report_text += f"{name}: {quantity}\n"
            
        messagebox.showinfo("Low Stock Report", report_text)
        
    def load_products(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM products")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection())

    def logout(self):
        self.logged_in_user = None
        self.create_login_screen()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
