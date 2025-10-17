import streamlit as st
import json
import os

# --- الإعدادات الأساسية ---
FILE_NAME = 'inventory.json'

# --- وظائف مساعدة ---

# وظيفة لتحميل بيانات المخزون من ملف JSON
def load_inventory():
    if not os.path.exists(FILE_NAME):
        return {}
    try:
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

# وظيفة لحفظ بيانات المخزون في ملف JSON
def save_inventory(inventory_data):
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(inventory_data, f, indent=4, ensure_ascii=False)

# --- واجهة التطبيق الرئيسية ---

st.set_page_config(page_title="نظام إدارة المخزون", page_icon="📦", layout="wide")

st.title("📦 نظام إدارة المخزون")
st.write("واجهة بسيطة لإدارة مخزون المنتجات بشكل احترافي (Professional).")

# تحميل البيانات
inventory = load_inventory()

# --- القائمة الجانبية للتنقل ---
st.sidebar.title("خيارات التشغيل")
action = st.sidebar.radio(
    "اختر الإجراء المطلوب:",
    ["عرض المخزون", "إضافة منتج جديد", "تعديل منتج", "حذف منتج"]
)

# --- تنفيذ الإجراءات ---

if action == "عرض المخزون":
    st.header("عرض المخزون الحالي")
    if not inventory:
        st.info("المخزون فارغ حاليًا. يمكنك إضافة منتجات جديدة من القائمة الجانبية.")
    else:
        product_list = []
        for product_id, details in inventory.items():
            product_list.append({
                'معرف المنتج': product_id,
                'اسم المنتج': details['name'],
                'الكمية': details['quantity'],
                'السعر (للقطعة)': f"{details.get('price', 0):.2f}"
            })
        st.table(product_list)

elif action == "إضافة منتج جديد":
    st.header("إضافة منتج جديد")
    with st.form("new_product_form", clear_on_submit=True):
        product_name = st.text_input("اسم المنتج")
        product_quantity = st.number_input("الكمية", min_value=0, step=1)
        product_price = st.number_input("السعر (للقطعة)", min_value=0.0, format="%.2f")
        submitted = st.form_submit_button("إضافة المنتج")

        if submitted and product_name:
            if not inventory:
                new_id = "1"
            else:
                new_id = str(max([int(k) for k in inventory.keys() if k.isdigit()] + [0]) + 1)
            
            inventory[new_id] = {
                "name": product_name,
                "quantity": product_quantity,
                "price": product_price
            }
            save_inventory(inventory)
            st.success(f"تمت إضافة المنتج '{product_name}' بنجاح!")
        elif submitted:
            st.error("الرجاء إدخال اسم المنتج.")

elif action == "تعديل منتج":
    st.header("تعديل بيانات منتج")
    if not inventory:
        st.warning("لا توجد منتجات لتعديلها.")
    else:
        product_items = [f"{details['name']} (ID: {pid})" for pid, details in inventory.items()]
        selected_item = st.selectbox("اختر المنتج للتعديل:", product_items)

        if selected_item:
            selected_id = selected_item.split("ID: ")[1][:-1]
            product_data = inventory[selected_id]

            with st.form("edit_form"):
                new_name = st.text_input("اسم المنتج", value=product_data['name'])
                new_quantity = st.number_input("الكمية", min_value=0, step=1, value=product_data['quantity'])
                new_price = st.number_input("السعر", min_value=0.0, format="%.2f", value=product_data.get('price', 0.0))
                
                if st.form_submit_button("تحديث المنتج"):
                    inventory[selected_id] = {
                        "name": new_name,
                        "quantity": new_quantity,
                        "price": new_price
                    }
                    save_inventory(inventory)
                    st.success("تم تحديث المنتج بنجاح!")
                    st.rerun()
