import streamlit as st
import json
import os

# --- Initial Setup ---
FILE_PATH = 'inventory.json'

# --- Data Loading and Saving Functions ---
def load_data():
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'w') as f:
            json.dump([], f)
        return []
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_data(data):
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- Load data at the start of the app ---
if 'inventory' not in st.session_state:
    st.session_state.inventory = load_data()

# --- App Interface Design ---
st.set_page_config(layout="wide", page_title="Inventory Management System")
st.title("Inventory Management System")
st.write("Developed by: Hanan")
st.write("---")

# --- Sidebar Menu ---
menu_choice = st.sidebar.radio(
    "Main Menu",
    ["📊 View Inventory", "➕ Add Product", "✏️ Edit Product", "❌ Delete Product"],
    captions=["Overview", "Data Entry", "Update Data", "Remove Data"]
)

# --- 📊 View Inventory ---
if menu_choice == "📊 View Inventory":
    st.subheader("All Products in Inventory")
    if st.session_state.inventory:
        display_list = []
        for item in st.session_state.inventory:
            formatted_item = {
                "Product Name": item["name"],
                "Quantity": item["quantity"],
                "Price": f"{item['price']:.2f} EGP"
            }
            display_list.append(formatted_item)
        st.dataframe(display_list, use_container_width=True)
    else:
        st.info("Inventory is currently empty. You can add products from the 'Add Product' menu.")

# --- ➕ Add Product ---
elif menu_choice == "➕ Add Product":
    st.subheader("Add a New Product to Inventory")
    with st.form(key="add_form", clear_on_submit=True):
        name = st.text_input("Product Name")
        quantity = st.number_input("Quantity", min_value=0, step=1)
        price = st.number_input("Price", min_value=0.0, format="%.2f")
        
        if st.form_submit_button("✅ Add Product"):
            if name:
                new_product = {"name": name, "quantity": int(quantity), "price": float(price)}
                st.session_state.inventory.append(new_product)
                save_data(st.session_state.inventory)
                st.success(f"Product '{name}' added successfully!")
            else:
                st.error("Error: Please enter a product name.")

# --- ✏️ Edit Product ---
elif menu_choice == "✏️ Edit Product":
    st.subheader("Edit an Existing Product")
    if not st.session_state.inventory:
        st.warning("No products to edit. Please add products first.")
    else:
        product_names = [p['name'] for p in st.session_state.inventory]
        selected_product_name = st.selectbox("Select the product to edit:", product_names)
        
        if selected_product_name:
            product_to_edit = next((p for p in st.session_state.inventory if p['name'] == selected_product_name), None)
            original_index = st.session_state.inventory.index(product_to_edit)

            with st.form(key=f"edit_{selected_product_name}"):
                st.write(f"You are editing: {product_to_edit['name']}")
                new_name = st.text_input("New Name", value=product_to_edit['name'])
                new_quantity = st.number_input("New Quantity", value=product_to_edit['quantity'], min_value=0, step=1)
                new_price = st.number_input("New Price", value=product_to_edit['price'], min_value=0.0, format="%.2f")
                
                if st.form_submit_button("💾 Save Changes"):
                    updated_product = {"name": new_name, "quantity": int(new_quantity), "price": float(new_price)}
                    st.session_state.inventory[original_index] = updated_product
                    save_data(st.session_state.inventory)
                    st.success("Product updated successfully!")
                    st.rerun()
