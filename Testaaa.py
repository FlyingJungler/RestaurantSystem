import json
import pandas as pd
from openpyxl import Workbook

def load_menu():
    with open('menu.json', 'r') as menu_file:
        menu_data = json.load(menu_file)
        #print("Loaded menu:", menu_data)
        return menu_data




# Initialize order database
order_db = {
    "orders": []
}

def display_menu(menu):
    print("Menu:")
    item_number = 1  # Reset item number for each category
    for category, items in menu.items():
        print(f"\n{category.capitalize()}:")
        for item in items:
            print(f"({item_number}) {item['item']} - £{item['price']:.2f}")
            item_number += 1  # Increment item number for the next item



def process_order(menu):
    order_number = len(order_db["orders"]) + 1
    order = {"order_number": order_number, "items": [], "total_amount": 0}

    while True:
        item_number = input("Enter the item number you want to order (0 to finish): ")

        if item_number == '0':
            break

        item_number = int(item_number)

        found_item = None
        current_index = 0

        for category, items in menu.items():
            category_size = len(items)
            if 1 <= item_number <= category_size + current_index:
                found_item = items[item_number - current_index - 1]
                break

            current_index += category_size

        if found_item:
            order["items"].append(found_item["item"])
            order["total_amount"] += found_item["price"]
        else:
            print("Invalid item number. Please try again.")

    order_db["orders"].append(order)
    print(f"Order #{order['order_number']} processed successfully!")



def display_summary():
    for order in order_db["orders"]:
        print(f"Order #{order['order_number']}:")
        for item in order["items"]:
            print(f"- {item}")
        print(f"Total Amount: £{order['total_amount']:.2f}\n")



def save_to_json():
    with open('order_db.json', 'w') as json_file:
        json.dump(order_db, json_file)

def generate_excel():
    orders_df = pd.DataFrame(order_db["orders"])
    orders_df.to_excel("orders_summary.xlsx", index=False)
    print("Excel file generated successfully!")

if __name__ == "__main__":
    # Load menu from JSON file
    menu_data = load_menu()
    menu = menu_data.get("menu", {})

#   print(menu)  # Print the loaded menu for debugging

    while True:
        display_menu(menu)
        new_order = input("New order? (yes/no): ").lower()

        if new_order == 'yes':
            process_order(menu)
        elif new_order == 'no':
            display_summary()
            save_to_json()
            generate_excel()
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
