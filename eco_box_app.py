import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import json
import os

# File paths
DATA_FILE = 'data.json'
LOGO_FILE = 'light_logo.jpg'  # Updated logo file

# Load data from file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    else:
        # Initialize with default data if file does not exist
        default_data = {
            'users': {
                'admin1': 'pass1',
                'admin2': 'pass2',
                'admin3': 'pass3'
            },
            'inventory': [],
            'orders': [],
            'logistics': [],
            'payments': [],
            'profile': {'username': 'admin1', 'email': 'admin1@example.com'}
        }
        save_data(default_data)  # Save the default data to file
        return default_data

# Save data to file
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Load initial data
data = load_data()
users = data['users']
inventory = data['inventory']
orders = data['orders']
logistics = data['logistics']
payments = data['payments']
profile = data['profile']

# Color scheme
bg_color = "#000000"  # Updated to black
fg_color = "#ffffff"
button_color = "#4CAF50"
button_hover_color = "#45a049"
entry_bg_color = "#3c3c3c"
entry_fg_color = "#ffffff"
font = ("Helvetica", 16)
button_font = ("Helvetica", 16)

class HoverButton(tk.Button):
    def __init__(self, master, **kwargs):
        tk.Button.__init__(self, master, **kwargs)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = button_hover_color

    def on_leave(self, e):
        self['background'] = self.defaultBackground

# Create the main application class
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Eco Box")  # Updated app name
        self.state('zoomed')  # Default to full screen
        self.configure(bg=bg_color)
        
        # Load and resize the logo image using Pillow
        # Load and resize the logo image using Pillow
        self.logo_image = Image.open('dark_logo.jpg')  # Updated to dark_logo.jpg
        self.logo_image = self.logo_image.resize((150, 50))  # Resize logo to 150x50 pixels
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        
        self.create_login_screen()

    def create_login_screen(self):
        # Clear the current frame
        for widget in self.winfo_children():
            widget.destroy()

        # Add the logo to the center
        logo_label = tk.Label(self, image=self.logo_photo, bg=bg_color)
        logo_label.pack(pady=20)
        
        # Create login screen
        tk.Label(self, text="Login", font=("Helvetica", 24), fg=fg_color, bg=bg_color).pack(pady=20)

        self.username = tk.Entry(self, width=30, bg=entry_bg_color, fg=entry_fg_color, font=font, insertbackground=entry_fg_color)
        self.username.pack(pady=10)
        self.username.insert(0, "Username")
        self.username.bind("<FocusIn>", self.clear_username)
        
        self.password = tk.Entry(self, width=30, show='*', bg=entry_bg_color, fg=entry_fg_color, font=font, insertbackground=entry_fg_color)
        self.password.pack(pady=10)
        self.password.insert(0, "Password")
        self.password.bind("<FocusIn>", self.clear_password)
        
        self.bind("<Return>", lambda event: self.login())

        HoverButton(self, text="Login", command=self.login, bg=button_color, fg=fg_color, font=button_font, width=20, height=2).pack(pady=20)

    def clear_username(self, event):
        if self.username.get() == "Username":
            self.username.delete(0, tk.END)

    def clear_password(self, event):
        if self.password.get() == "Password":
            self.password.delete(0, tk.END)

    def login(self):
        # Login validation
        username = self.username.get()
        password = self.password.get()

        if username in users and users[username] == password:
            self.create_main_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def create_main_screen(self):
        # Clear the current frame
        for widget in self.winfo_children():
            widget.destroy()

        # Add the logo to the center
        logo_label = tk.Label(self, image=self.logo_photo, bg=bg_color)
        logo_label.pack(pady=20)
        
        # Create main screen
        tk.Label(self, text="Welcome to Eco Box", font=("Helvetica", 18), fg=fg_color, bg=bg_color).pack(pady=20)

        HoverButton(self, text="Inventory", command=self.inventory_screen, bg=button_color, fg=fg_color, font=button_font, width=20, height=2).pack(pady=10)
        HoverButton(self, text="Orders", command=self.orders_screen, bg=button_color, fg=fg_color, font=button_font, width=20, height=2).pack(pady=10)
        HoverButton(self, text="Logistics", command=self.logistics_screen, bg=button_color, fg=fg_color, font=button_font, width=20, height=2).pack(pady=10)
        HoverButton(self, text="Payments", command=self.payments_screen, bg=button_color, fg=fg_color, font=button_font, width=20, height=2).pack(pady=10)
        HoverButton(self, text="Profile", command=self.profile_screen, bg=button_color, fg=fg_color, font=button_font, width=20, height=2).pack(pady=10)

    # Inventory Section
    def inventory_screen(self):
        self.show_screen("Inventory", ["Add Item", "View Inventory", "Edit Item"], self.handle_inventory_action)

    def handle_inventory_action(self, action):
        if action == "Add Item":
            item = simpledialog.askstring("Add Item", "Enter item details:")
            if item:
                inventory.append(item)
                save_data(data)  # Save data after modification
                messagebox.showinfo("Inventory", "Item added successfully!")
        elif action == "View Inventory":
            self.show_list_screen("Inventory List", inventory)
        elif action == "Edit Item":
            item = simpledialog.askstring("Edit Item", "Enter item to edit:")
            if item in inventory:
                new_details = simpledialog.askstring("Edit Item", "Enter new details:")
                inventory[inventory.index(item)] = new_details
                save_data(data)  # Save data after modification
                messagebox.showinfo("Inventory", "Item updated successfully!")
            else:
                messagebox.showerror("Inventory", "Item not found!")

    # Orders Section
    def orders_screen(self):
        self.show_screen("Orders", ["Create Order", "View Orders", "Edit Order"], self.handle_orders_action)

    def handle_orders_action(self, action):
        if action == "Create Order":
            order = simpledialog.askstring("Create Order", "Enter order details:")
            if order:
                orders.append(order)
                save_data(data)  # Save data after modification
                messagebox.showinfo("Orders", "Order created successfully!")
        elif action == "View Orders":
            self.show_list_screen("Order List", orders)
        elif action == "Edit Order":
            order = simpledialog.askstring("Edit Order", "Enter order to edit:")
            if order in orders:
                new_details = simpledialog.askstring("Edit Order", "Enter new details:")
                orders[orders.index(order)] = new_details
                save_data(data)  # Save data after modification
                messagebox.showinfo("Orders", "Order updated successfully!")
            else:
                messagebox.showerror("Orders", "Order not found!")

    # Logistics Section
    def logistics_screen(self):
        self.show_screen("Logistics", ["Track Shipment", "Schedule Delivery", "Logistics Status"], self.handle_logistics_action)

    def handle_logistics_action(self, action):
        if action == "Track Shipment":
            tracking_info = simpledialog.askstring("Track Shipment", "Enter tracking details:")
            logistics.append(tracking_info)
            save_data(data)  # Save data after modification
            messagebox.showinfo("Logistics", "Tracking info added!")
        elif action == "Schedule Delivery":
            delivery_info = simpledialog.askstring("Schedule Delivery", "Enter delivery schedule:")
            logistics.append(delivery_info)
            save_data(data)  # Save data after modification
            messagebox.showinfo("Logistics", "Delivery scheduled!")
        elif action == "Logistics Status":
            self.show_list_screen("Logistics Status", logistics)

    # Payments Section
    def payments_screen(self):
        self.show_screen("Payments", ["Generate Invoice", "View Payments", "Payment Status"], self.handle_payments_action)

    def handle_payments_action(self, action):
        if action == "Generate Invoice":
            invoice = simpledialog.askstring("Generate Invoice", "Enter invoice details:")
            payments.append(invoice)
            save_data(data)  # Save data after modification
            messagebox.showinfo("Payments", "Invoice generated successfully!")
        elif action == "View Payments":
            self.show_list_screen("Payment List", payments)
        elif action == "Payment Status":
            status_info = simpledialog.askstring("Payment Status", "Enter payment status details:")
            payments.append(status_info)
            save_data(data)  # Save data after modification
            messagebox.showinfo("Payments", "Payment status updated!")

    # Profile Section
    def profile_screen(self):
        self.show_screen("Profile", ["View Profile", "Edit Profile", "Logout"], self.handle_profile_action, is_profile=True)

    def handle_profile_action(self, action):
        if action == "View Profile":
            profile_info = f"Username: {profile['username']}\nEmail: {profile['email']}"
            messagebox.showinfo("Profile", profile_info)
        elif action == "Edit Profile":
            new_username = simpledialog.askstring("Edit Profile", "Enter new username:")
            new_email = simpledialog.askstring("Edit Profile", "Enter new email:")
            if new_username:
                profile['username'] = new_username
            if new_email:
                profile['email'] = new_email
            save_data(data)  # Save data after modification
            messagebox.showinfo("Profile", "Profile updated successfully!")
        elif action == "Logout":
            self.create_login_screen()

    def show_screen(self, screen_name, actions, handler, is_profile=False):
        # Clear the current frame
        for widget in self.winfo_children():
            widget.destroy()

        # Add the logo to the center
        logo_label = tk.Label(self, image=self.logo_photo, bg=bg_color)
        logo_label.pack(pady=20)
        
        # Display the selected screen
        tk.Label(self, text=f"{screen_name} Screen", font=("Helvetica", 18), fg=fg_color, bg=bg_color).pack(pady=20)

        for action in actions:
            HoverButton(self, text=action, command=lambda a=action: handler(a), bg=button_color, fg=fg_color, font=button_font, width=20, height=2).pack(pady=10)
        
        if is_profile:
            HoverButton(self, text="Logout", command=self.create_login_screen, bg=button_color, fg=fg_color, font=button_font, width=20, height=2).pack(pady=10)
        
        # Add the "Back to Menu" button
        HoverButton(self, text="Back to Menu", command=self.create_main_screen, bg=button_color, fg=fg_color, font=button_font, width=20, height=2).pack(pady=20)

    def show_list_screen(self, title, items):
        # Clear the current frame
        for widget in self.winfo_children():
            widget.destroy()

        # Add the logo to the center
        logo_label = tk.Label(self, image=self.logo_photo, bg=bg_color)
        logo_label.pack(pady=20)
        
        # Display the list
        tk.Label(self, text=title, font=("Helvetica", 18), fg=fg_color, bg=bg_color).pack(pady=20)

        for item in items:
            tk.Label(self, text=item, font=font, fg=fg_color, bg=bg_color).pack(pady=5)

        # Add the "Back to Menu" button
        HoverButton(self, text="Back to Menu", command=self.create_main_screen, bg=button_color, fg=fg_color, font=button_font, width=20, height=2).pack(pady=20)

if __name__ == "__main__":
    app = App()
    app.mainloop()
