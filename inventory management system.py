import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="Aditya1234",
        database="InventoryManagement",
        auth_plugin="mysql_native_password",
        ssl_disabled=True  # Disable SSL if necessary
    )

# GUI Application
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("1000x700")

        # Tabs
        tab_control = ttk.Notebook(root)
        self.item_tab = ttk.Frame(tab_control)
        self.supplier_tab = ttk.Frame(tab_control)
        self.order_tab = ttk.Frame(tab_control)

        tab_control.add(self.item_tab, text="Items")
        tab_control.add(self.supplier_tab, text="Suppliers")
        tab_control.add(self.order_tab, text="Purchase Orders")
        tab_control.pack(expand=1, fill="both")

        # Setup tabs
        self.setup_items_tab()
        self.setup_suppliers_tab()
        self.setup_orders_tab()

    # Items Tab
    def setup_items_tab(self):
        ttk.Label(self.item_tab, text="Manage Items", font=("Arial", 16)).pack(pady=10)

        # Input fields
        frame = ttk.Frame(self.item_tab)
        frame.pack(pady=10)

        ttk.Label(frame, text="ID").grid(row=0, column=0, padx=5, pady=5)
        self.item_id = ttk.Entry(frame)
        self.item_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Name").grid(row=1, column=0, padx=5, pady=5)
        self.item_name = ttk.Entry(frame)
        self.item_name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Description").grid(row=2, column=0, padx=5, pady=5)
        self.item_description = ttk.Entry(frame)
        self.item_description.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Price").grid(row=3, column=0, padx=5, pady=5)
        self.item_price = ttk.Entry(frame)
        self.item_price.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Stock Quantity").grid(row=4, column=0, padx=5, pady=5)
        self.item_stock = ttk.Entry(frame)
        self.item_stock.grid(row=4, column=1, padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(self.item_tab)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Add Item", command=self.add_item).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Update Item", command=self.update_item).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete Item", command=self.delete_item).grid(row=0, column=2, padx=5)

        # Treeview
        self.item_tree = ttk.Treeview(self.item_tab, columns=("ID", "Name", "Description", "Price", "Stock"), show="headings")
        self.item_tree.heading("ID", text="ID")
        self.item_tree.heading("Name", text="Name")
        self.item_tree.heading("Description", text="Description")
        self.item_tree.heading("Price", text="Price")
        self.item_tree.heading("Stock", text="Stock Quantity")
        self.item_tree.pack(fill="both", expand=True)
        self.item_tree.bind("<Double-1>", self.load_selected_item)

        self.refresh_items()

    def refresh_items(self):
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM items")
        rows = cursor.fetchall()
        connection.close()

        self.item_tree.delete(*self.item_tree.get_children())
        for row in rows:
            self.item_tree.insert("", "end", values=row)

    def add_item(self):
        item_id = self.item_id.get()
        name = self.item_name.get()
        description = self.item_description.get()
        price = self.item_price.get()
        stock = self.item_stock.get()

        if not item_id or not name or not price or not stock:
            messagebox.showerror("Error", "ID, Name, Price, and Stock Quantity are required.")
            return

        try:
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO items (id, name, description, price, stock_quantity) VALUES (%s, %s, %s, %s, %s)",
                           (item_id, name, description, price, stock))
            connection.commit()
            connection.close()
            self.refresh_items()
            messagebox.showinfo("Success", "Item added successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_selected_item(self, event):
        selected_item = self.item_tree.item(self.item_tree.focus())
        values = selected_item["values"]

        self.item_id.delete(0, tk.END)
        self.item_id.insert(0, values[0])
        self.item_name.delete(0, tk.END)
        self.item_name.insert(0, values[1])
        self.item_description.delete(0, tk.END)
        self.item_description.insert(0, values[2])
        self.item_price.delete(0, tk.END)
        self.item_price.insert(0, values[3])
        self.item_stock.delete(0, tk.END)
        self.item_stock.insert(0, values[4])

    def update_item(self):
        item_id = self.item_id.get()
        name = self.item_name.get()
        description = self.item_description.get()
        price = self.item_price.get()
        stock = self.item_stock.get()

        if not item_id or not name or not price or not stock:
            messagebox.showerror("Error", "ID, Name, Price, and Stock Quantity are required.")
            return

        try:
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("UPDATE items SET name=%s, description=%s, price=%s, stock_quantity=%s WHERE id=%s",
                           (name, description, price, stock, item_id))
            connection.commit()
            connection.close()
            self.refresh_items()
            messagebox.showinfo("Success", "Item updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_item(self):
        item_id = self.item_id.get()

        if not item_id:
            messagebox.showerror("Error", "ID is required to delete an item.")
            return

        try:
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM items WHERE id=%s", (item_id,))
            connection.commit()
            connection.close()
            self.refresh_items()
            messagebox.showinfo("Success", "Item deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Suppliers Tab
    def setup_suppliers_tab(self):
        ttk.Label(self.supplier_tab, text="Manage Suppliers", font=("Arial", 16)).pack(pady=10)

        # Input fields
        frame = ttk.Frame(self.supplier_tab)
        frame.pack(pady=10)

        ttk.Label(frame, text="ID").grid(row=0, column=0, padx=5, pady=5)
        self.supplier_id = ttk.Entry(frame)
        self.supplier_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Name").grid(row=1, column=0, padx=5, pady=5)
        self.supplier_name = ttk.Entry(frame)
        self.supplier_name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Contact").grid(row=2, column=0, padx=5, pady=5)
        self.supplier_contact = ttk.Entry(frame)
        self.supplier_contact.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Address").grid(row=3, column=0, padx=5, pady=5)
        self.supplier_address = ttk.Entry(frame)
        self.supplier_address.grid(row=3, column=1, padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(self.supplier_tab)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Add Supplier", command=self.add_supplier).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Update Supplier", command=self.update_supplier).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete Supplier", command=self.delete_supplier).grid(row=0, column=2, padx=5)

        # Treeview
        self.supplier_tree = ttk.Treeview(self.supplier_tab, columns=("ID", "Name", "Contact", "Address"), show="headings")
        self.supplier_tree.heading("ID", text="ID")
        self.supplier_tree.heading("Name", text="Name")
        self.supplier_tree.heading("Contact", text="Contact")
        self.supplier_tree.heading("Address", text="Address")
        self.supplier_tree.pack(fill="both", expand=True)
        self.supplier_tree.bind("<Double-1>", self.load_selected_supplier)

        self.refresh_suppliers()

    def refresh_suppliers(self):
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM suppliers")
        rows = cursor.fetchall()
        connection.close()

        self.supplier_tree.delete(*self.supplier_tree.get_children())
        for row in rows:
            self.supplier_tree.insert("", "end", values=row)

    def add_supplier(self):
        supplier_id = self.supplier_id.get()
        name = self.supplier_name.get()
        contact = self.supplier_contact.get()
        address = self.supplier_address.get()

        if not supplier_id or not name or not contact or not address:
            messagebox.showerror("Error", "ID, Name, Contact, and Address are required.")
            return

        try:
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO suppliers (id, name, contact, address) VALUES (%s, %s, %s, %s)",
                           (supplier_id, name, contact, address))
            connection.commit()
            connection.close()
            self.refresh_suppliers()
            messagebox.showinfo("Success", "Supplier added successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_selected_supplier(self, event):
        selected_supplier = self.supplier_tree.item(self.supplier_tree.focus())
        values = selected_supplier["values"]

        self.supplier_id.delete(0, tk.END)
        self.supplier_id.insert(0, values[0])
        self.supplier_name.delete(0, tk.END)
        self.supplier_name.insert(0, values[1])
        self.supplier_contact.delete(0, tk.END)
        self.supplier_contact.insert(0, values[2])
        self.supplier_address.delete(0, tk.END)
        self.supplier_address.insert(0, values[3])

    def update_supplier(self):
        supplier_id = self.supplier_id.get()
        name = self.supplier_name.get()
        contact = self.supplier_contact.get()
        address = self.supplier_address.get()

        if not supplier_id or not name or not contact or not address:
            messagebox.showerror("Error", "ID, Name, Contact, and Address are required.")
            return

        try:
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("UPDATE suppliers SET name=%s, contact=%s, address=%s WHERE id=%s",
                           (name, contact, address, supplier_id))
            connection.commit()
            connection.close()
            self.refresh_suppliers()
            messagebox.showinfo("Success", "Supplier updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_supplier(self):
        supplier_id = self.supplier_id.get()

        if not supplier_id:
            messagebox.showerror("Error", "ID is required to delete a supplier.")
            return

        try:
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM suppliers WHERE id=%s", (supplier_id,))
            connection.commit()
            connection.close()
            self.refresh_suppliers()
            messagebox.showinfo("Success", "Supplier deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Orders Tab
    def setup_orders_tab(self):
        ttk.Label(self.order_tab, text="Manage Purchase Orders", font=("Arial", 16)).pack(pady=10)

        # Input fields
        frame = ttk.Frame(self.order_tab)
        frame.pack(pady=10)

        ttk.Label(frame, text="ID").grid(row=0, column=0, padx=5, pady=5)
        self.order_id = ttk.Entry(frame)
        self.order_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Date").grid(row=1, column=0, padx=5, pady=5)
        self.order_date = ttk.Entry(frame)
        self.order_date.grid(row=1, column=1, padx=5, pady=5)
        self.order_date.insert(0, date.today())

        ttk.Label(frame, text="Item ID").grid(row=2, column=0, padx=5, pady=5)
        self.order_item_id = ttk.Entry(frame)
        self.order_item_id.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Quantity").grid(row=3, column=0, padx=5, pady=5)
        self.order_quantity = ttk.Entry(frame)
        self.order_quantity.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Supplier ID").grid(row=4, column=0, padx=5, pady=5)
        self.order_supplier_id = ttk.Entry(frame)
        self.order_supplier_id.grid(row=4, column=1, padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(self.order_tab)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Add Order", command=self.add_order).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Update Order", command=self.update_order).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete Order", command=self.delete_order).grid(row=0, column=2, padx=5)

        # Treeview
        self.order_tree = ttk.Treeview(self.order_tab, columns=("ID", "Date", "Item ID", "Quantity", "Supplier ID"), show="headings")
        self.order_tree.heading("ID", text="ID")
        self.order_tree.heading("Date", text="Date")
        self.order_tree.heading("Item ID", text="Item ID")
        self.order_tree.heading("Quantity", text="Quantity")
        self.order_tree.heading("Supplier ID", text="Supplier ID")
        self.order_tree.pack(fill="both", expand=True)
        self.order_tree.bind("<Double-1>", self.load_selected_order)

        self.refresh_orders()

    def refresh_orders(self):
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM purchase_orders")
        rows = cursor.fetchall()
        connection.close()

        self.order_tree.delete(*self.order_tree.get_children())
        for row in rows:
            self.order_tree.insert("", "end", values=row)

    def add_order(self):
        order_id = self.order_id.get()
        order_date = self.order_date.get()
        item_id = self.order_item_id.get()
        quantity = self.order_quantity.get()
        supplier_id = self.order_supplier_id.get()

        if not order_id or not item_id or not quantity or not supplier_id:
            messagebox.showerror("Error", "ID, Item ID, Quantity, and Supplier ID are required.")
            return

        try:
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO purchase_orders (id, order_date, item_id, quantity, supplier_id) VALUES (%s, %s, %s, %s, %s)",
                           (order_id, order_date, item_id, quantity, supplier_id))
            connection.commit()
            connection.close()
            self.refresh_orders()
            messagebox.showinfo("Success", "Order added successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_selected_order(self, event):
        selected_order = self.order_tree.item(self.order_tree.focus())
        values = selected_order["values"]

        self.order_id.delete(0, tk.END)
        self.order_id.insert(0, values[0])
        self.order_date.delete(0, tk.END)
        self.order_date.insert(0, values[1])
        self.order_item_id.delete(0, tk.END)
        self.order_item_id.insert(0, values[2])
        self.order_quantity.delete(0, tk.END)
        self.order_quantity.insert(0, values[3])
        self.order_supplier_id.delete(0, tk.END)
        self.order_supplier_id.insert(0, values[4])

    def update_order(self):
        order_id = self.order_id.get()
        order_date = self.order_date.get()
        item_id = self.order_item_id.get()
        quantity = self.order_quantity.get()
        supplier_id = self.order_supplier_id.get()

        if not order_id or not item_id or not quantity or not supplier_id:
            messagebox.showerror("Error", "ID, Item ID, Quantity, and Supplier ID are required.")
            return

        try:
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("UPDATE purchase_orders SET order_date=%s, item_id=%s, quantity=%s, supplier_id=%s WHERE id=%s",
                           (order_date, item_id, quantity, supplier_id, order_id))
            connection.commit()
            connection.close()
            self.refresh_orders()
            messagebox.showinfo("Success", "Order updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_order(self):
        order_id = self.order_id.get()

        if not order_id:
            messagebox.showerror("Error", "ID is required to delete an order.")
            return

        try:
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM purchase_orders WHERE id=%s", (order_id,))
            connection.commit()
            connection.close()
            self.refresh_orders()
            messagebox.showinfo("Success", "Order deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Create the Tkinter window and run the application
root = tk.Tk()
app = InventoryApp(root)
root.mainloop()