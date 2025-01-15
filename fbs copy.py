"""Copyright Disclaimer:

Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)

Copyright (c) 2025 Dharmin Joshi

You are free to:

- Share: Copy and redistribute the material in any medium, format, or platform.
- Adapt: Remix, transform, and build upon the material.

Under the following terms:

- Attribution: You must give appropriate credit to the original creator (Dharmin Joshi/DevKay), provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the creator endorses you or your use.
- NonCommercial: You may not use the material for commercial purposes.

No additional restrictions: You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, see the full license: https://creativecommons.org/licenses/by-nc/4.0/"""


import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel
from datetime import datetime
import json
import os


class CustomerInfoDialog(tk.Toplevel):
    def __init__(self, parent, title="Enter Customer Information"):
        super().__init__(parent)
        self.title(title)
        self.geometry("300x200")
        self.resizable(False, False)
        
        # Labels and Entry widgets
        self.name_label = tk.Label(self, text="Customer Name:")
        self.name_label.pack(pady=5)
        self.name_entry = tk.Entry(self, width=30)
        self.name_entry.pack(pady=5)
        
        self.phone_label = tk.Label(self, text="Customer Phone:")
        self.phone_label.pack(pady=5)
        self.phone_entry = tk.Entry(self, width=30)
        self.phone_entry.pack(pady=5)
        
        # Submit Button
        self.submit_button = tk.Button(self, text="Submit", command=self.submit)
        self.submit_button.pack(pady=10)
        
        self.customer_data = None
        
    def submit(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()

        if not name or not phone:
            messagebox.showerror("Error", "Both fields are required!")
        else:
            self.customer_data = {'name': name, 'phone': phone}
            self.destroy()

    def get_customer_info(self):
        self.wait_window()  # Wait for the window to be closed
        return self.customer_data


class FastFoodBillingSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FastFood Billing System - Bsc. Chaat-Wala")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#f4f4f4")
        # Menu Items (ID: (Item Name, Price))
        self.menu = {
            1: ('Pani Puri', 30.00),
            2: ('Sev Puri', 35.00),
            3: ('Dahi Puri', 35.00),
            4: ('Bhel Puri', 30.00),
            5: ('Vada Pav', 24.00),
            6: ('Bhaji Pav', 30.00),
            7: ('Samosa Pav', 24.00),
            8: ('Kutchi Dabeli (Double-Roti)', 20.00),
            9: ('Raj Kachori', 60.00),
            10: ('Veg. Sandwich', 35.00),
            11: ('Cheese Chilli Toast Sandwich', 40.00),
            12: ('Bombay Toast Sandwich', 40.00),
            13: ('Bombay Grilled Sandwich', 60.00),
            14: ('Lays Grilled Sandwich', 60.00),
            15: ('Masala Chai', 30.00),
            16: ('Filter Coffee', 30.00),
            17: ('Malaai Lassi', 40.00),
            18: ('Mango Lassi', 40.00),
            19: ('Kokam Sharbat', 20.00),
            20: ('Nimbu Sharbat', 20.00)
        }

        self.order = {}
        self.total = 0.0
        self.discount = 0.0
        self.sgst_rate = 2.5  # 2.5% SGST
        self.cgst_rate = 2.5  # 2.5% CGST
        self.customer_info = {}  # Dictionary to store customer info

        self.create_widgets()

        self.load_order_history()  # Load existing order history

    def create_widgets(self):
        # Header Section
        self.header_frame = tk.Frame(self.root, bg="#2196F3", pady=20)
        self.header_frame.pack(fill=tk.X)

        self.header_label = tk.Label(self.header_frame, text="Bsc. Chaat-Wala - Billing System", font=('Arial', 24, 'bold'), fg="white", bg="#2196F3")
        self.header_label.pack()

        # Main Content Section (Two Columns)
        main_content_frame = tk.Frame(self.root, bg="#f4f4f4", pady=20)
        main_content_frame.pack(fill=tk.BOTH, padx=30)

        # Left Column: Menu Section
        menu_frame = tk.LabelFrame(main_content_frame, text="Menu", font=('Arial', 16, 'bold'), bg="#ffffff", padx=20, pady=20)
        menu_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        self.menu_listbox = tk.Listbox(menu_frame, width=40, height=10, selectmode=tk.SINGLE, font=('Arial', 12))
        self.menu_listbox.grid(row=0, column=0, padx=10, pady=10)

        for item_id, (item, price) in self.menu.items():
            self.menu_listbox.insert(tk.END, f"{item} - Rs. {price:.2f}")

        self.menu_listbox.bind("<Double-1>", self.add_to_order)

        # Right Column: Order Summary Section
        order_frame = tk.LabelFrame(main_content_frame, text="Order Summary", font=('Arial', 16, 'bold'), bg="#ffffff", padx=20, pady=20)
        order_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

        self.order_listbox = tk.Listbox(order_frame, width=40, height=10, font=('Arial', 12))
        self.order_listbox.grid(row=0, column=0, padx=10, pady=10)

        self.calculate_button = tk.Button(order_frame, text="Calculate Total", width=20, height=2, bg="#2196F3", fg="white", font=('Arial', 12), command=self.calculate_total)
        self.calculate_button.grid(row=1, column=0, padx=10, pady=10)

        self.total_label = tk.Label(order_frame, text="Total: Rs. 0.00", font=('Arial', 16, 'bold'), fg="#2196F3")
        self.total_label.grid(row=2, column=0, padx=10, pady=10)

        # Bottom Section: Buttons for actions
        action_button_frame = tk.Frame(self.root, pady=20)
        action_button_frame.pack(fill=tk.X)

        self.add_button = tk.Button(action_button_frame, text="Add Item", width=15, height=2, bg="#4CAF50", fg="white", font=('Arial', 12), command=self.add_to_order)
        self.add_button.pack(side=tk.LEFT, padx=10)

        self.remove_button = tk.Button(action_button_frame, text="Remove Item", width=15, height=2, bg="#f44336", fg="white", font=('Arial', 12), command=self.remove_from_order)
        self.remove_button.pack(side=tk.LEFT, padx=10)

        self.discount_button = tk.Button(action_button_frame, text="Apply Discount", width=15, height=2, bg="#FF9800", fg="white", font=('Arial', 12), command=self.apply_discount)
        self.discount_button.pack(side=tk.LEFT, padx=10)

        self.clear_order_button = tk.Button(action_button_frame, text="Clear Order", width=15, height=2, bg="#607D8B", fg="white", font=('Arial', 12), command=self.clear_order)
        self.clear_order_button.pack(side=tk.LEFT, padx=10)

        self.generate_button = tk.Button(action_button_frame, text="Generate Bill", width=15, height=2, bg="#9C27B0", fg="white", font=('Arial', 12), command=self.generate_bill)
        self.generate_button.pack(side=tk.LEFT, padx=10)

        self.history_button = tk.Button(action_button_frame, text="Order History", width=15, height=2, bg="#00BCD4", fg="white", font=('Arial', 12), command=self.show_order_history)
        self.history_button.pack(side=tk.LEFT, padx=10)

        # Bill Display Text Area
        self.bill_text_area = tk.Text(self.root, width=90, height=15, wrap=tk.WORD, font=('Courier', 12), bg="#f4f4f4", fg="#000000")
        self.bill_text_area.pack(pady=20)
        self.bill_text_area.config(state=tk.DISABLED)

    def add_to_order(self, event=None):
        selected_index = self.menu_listbox.curselection()
        if not selected_index:
            return
        item_text = self.menu_listbox.get(selected_index)
        item_name, price = item_text.split(" - Rs. ")
        item_name = item_name.strip()
        price = float(price)

        quantity = simpledialog.askinteger("Quantity", f"Enter quantity for {item_name}:", minvalue=1)
        if quantity:
            if item_name in self.order:
                self.order[item_name]['quantity'] += quantity
            else:
                self.order[item_name] = {'quantity': quantity, 'price': price}
            self.update_order_listbox()

    def remove_from_order(self):
        selected_index = self.order_listbox.curselection()
        if not selected_index:
            return
        item_text = self.order_listbox.get(selected_index)
        item_name = item_text.split(" - Rs. ")[0].strip()

        del self.order[item_name]
        self.update_order_listbox()

    def update_order_listbox(self):
        self.order_listbox.delete(0, tk.END)
        for item_name, details in self.order.items():
            total_item_price = details['quantity'] * details['price']
            self.order_listbox.insert(tk.END, f"{item_name} - {details['quantity']} x Rs. {details['price']} = Rs. {total_item_price:.2f}")

        self.calculate_total()

    def calculate_total(self):
        self.total = sum(details['quantity'] * details['price'] for details in self.order.values())
        if self.discount:
            self.total -= self.discount

        self.total_label.config(text=f"Total: Rs. {self.total:.2f}")

    def apply_discount(self):
        discount = simpledialog.askfloat("Discount", "Enter discount percentage:", minvalue=0, maxvalue=100)
        if discount is not None:
            self.discount = self.total * discount / 100
            self.calculate_total()

    def clear_order(self):
        self.order.clear()
        self.discount = 0
        self.update_order_listbox()

    def generate_bill(self):
        if not self.order:
            messagebox.showerror("Error", "No items in the order!")
            return

        # Get customer info
        customer_info_dialog = CustomerInfoDialog(self.root)
        self.customer_info = customer_info_dialog.get_customer_info()

        if not self.customer_info:
            messagebox.showerror("Error", "Customer info is required!")
            return

        # Generate Bill Content
        bill_content = f"----- Bsc. Chaat-Wala -----\n"
        bill_content += f"Address: Mulund-Branch\n"
        bill_content += f"Phone: +91-1234567890 | Email: contact@bscchaatwala.com\n"
        bill_content += f"--------------------------------------------\n"
        bill_content += f"Customer: {self.customer_info['name']} |  Phone: {self.customer_info['phone']}\n"
        bill_content += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        bill_content += f"--------------------------------------------\n"
        
        # Header for the items table
        bill_content += f"{'Item':<30} {'Quantity':<10} {'Price':<10} {'Total':<10}\n"
        bill_content += "-" * 60 + "\n"
        
        # Add each item from the order
        for item_name, details in self.order.items():
            total_price = details['price'] * details['quantity']
            bill_content += f"{item_name:<30} {details['quantity']:<10} Rs. {details['price']:<10.2f} Rs. {total_price:<10.2f}\n"
        
        # Add separators
        bill_content += "-" * 60 + "\n"
        
        # If there's a discount, include it
        if self.discount > 0:
            bill_content += f"Discount: Rs. {self.discount:.2f}\n"
        
        # Calculate SGST and CGST
        sgst = self.total * self.sgst_rate / 100
        cgst = self.total * self.cgst_rate / 100
        bill_content += f"SGST (2.5%): Rs. {sgst:.2f}\n"
        bill_content += f"CGST (2.5%): Rs. {cgst:.2f}\n"
        
        # Calculate final total
        final_total = self.total + sgst + cgst
        bill_content += f"Total (after taxes): Rs. {final_total:.2f}\n"
        
        # Add separator and the thank you message
        bill_content += "-" * 60 + "\n"
        bill_content += f"Thank you for visiting Bsc. Chaat-Wala!\n"
        bill_content += f"Visit again at: Bsc. Chaat-Wala Mulund-Branch\n"
        bill_content += f"--------------------------------------------\n"
        bill_content += f"Working Hours: 10:00 AM - 10:00 PM\n"
        bill_content += f"Website: www.bscchaatwala.com\n"
        
        # Display Bill in Text Area
        self.bill_text_area.config(state=tk.NORMAL)
        self.bill_text_area.delete(1.0, tk.END)
        self.bill_text_area.insert(tk.END, bill_content)
        self.bill_text_area.config(state=tk.DISABLED)

        self.save_order_history()  # Save the order to history

    def load_order_history(self):
        if os.path.exists('order_history.json'):
            with open('order_history.json', 'r') as file:
                self.order_history = json.load(file)
        else:
            self.order_history = []

    def save_order_history(self):
        order_data = {
            'customer': self.customer_info,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total': self.total,
            'discount': self.discount,
            'order': self.order
        }
        self.order_history.append(order_data)

        with open('order_history.json', 'w') as file:
            json.dump(self.order_history, file, indent=4)

    def show_order_history(self):
        history_window = Toplevel(self.root)
        history_window.title("Order History")
        history_window.geometry("600x400")
        
        history_listbox = tk.Listbox(history_window, width=80, height=15, font=('Arial', 12))
        history_listbox.pack(pady=20)

        if not self.order_history:
            history_listbox.insert(tk.END, "No orders found.")
        else:
            for idx, order in enumerate(self.order_history):
                customer_info = order['customer']
                order_date = order['timestamp']
                history_listbox.insert(tk.END, f"{customer_info['name']} - {order_date} - Rs. {order['total']:.2f}")

            # Bind double-click event to show full order details
            history_listbox.bind("<Double-1>", lambda event, lb=history_listbox: self.show_full_order_details(event, lb))

    def show_full_order_details(self, event, listbox):
        selected_index = listbox.curselection()
        if selected_index:
            order_index = selected_index[0]
            order = self.order_history[order_index]
            customer_info = order['customer']
            order_date = order['timestamp']
            total = order['total']
            discount = order['discount']
            items = order['order']

            # Create a new window to display full order details
            details_window = Toplevel(self.root)
            details_window.title("Full Order Details")
            details_window.geometry("600x400")
            
            details_text = tk.Text(details_window, width=70, height=15, font=('Courier', 12), wrap=tk.WORD)
            details_text.pack(pady=20)

            # Format the full content of the order
            bill_content = f"----- {customer_info['name']} -----\n"
            bill_content += f"Phone: {customer_info['phone']}\n"
            bill_content += f"Date: {order_date}\n"
            bill_content += f"--------------------------------------------\n"
            bill_content += f"{'Item':<30} {'Quantity':<10} {'Price':<10} {'Total':<10}\n"
            bill_content += "-" * 60 + "\n"

            for item_name, details in items.items():
                total_price = details['price'] * details['quantity']
                bill_content += f"{item_name:<30} {details['quantity']:<10} Rs. {details['price']:<10.2f} Rs. {total_price:<10.2f}\n"

            bill_content += "-" * 60 + "\n"
            
            if discount > 0:
                bill_content += f"Discount: Rs. {discount:.2f}\n"
            
            sgst = total * self.sgst_rate / 100
            cgst = total * self.cgst_rate / 100
            bill_content += f"SGST (2.5%): Rs. {sgst:.2f}\n"
            bill_content += f"CGST (2.5%): Rs. {cgst:.2f}\n"

            final_total = total + sgst + cgst
            bill_content += f"Total (after taxes): Rs. {final_total:.2f}\n"
            bill_content += "-" * 60 + "\n"
            
            bill_content += f"Thank you for visiting Bsc. Chaat-Wala!\n"
            
            # Insert the formatted content into the details window
            details_text.insert(tk.END, bill_content)
            details_text.config(state=tk.DISABLED)



if __name__ == "__main__":
    root = tk.Tk()
    app = FastFoodBillingSystemGUI(root)
    root.mainloop()
