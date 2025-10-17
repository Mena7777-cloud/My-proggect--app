import streamlit as st
import json
import os

# --- الإعدادات الأساسية ---
FILE_NAME = 'inventory.json'

# --- وظائف مساعدة ---

# وظيفة لتحميل بيانات التخزين من ملف JSON
def load_inventory():
    if not os.path.exists(FILE_NAME):
        return {}
    try:
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content:
                return {}
            return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

# وظيفة لحفظ بيانات التخزين في ملف JSON
def save_inventory(inventory_data):
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(inventory_data, f, indent=4, ensure_ascii=False)

# --- واجهة التطبيق الرئيسية ---

st.set_page_config(page_title="نظام إدارة التخزين", page_icon="📦", layout="wide")

st.title("📦 نظام إدارة التخزين")
st.write("Storage Management System") 
st.write("نظام ادارة التخزين")

# تحميل البيانات
inventory = load_inventory()

# --- القائمة الجانبية للتنقل ---
st.sidebar.title("خيارات التشغيل")
action = st.sidebar.radio(
    "اختر الإجراء المطلوب:",
    ["عرض المنتجات والبحث", "إضافة منتج جديد", "تعديل منتج", "حذف منتج"]
)

# --- تنفيذ الإجراءات ---

# 1. عرض المنتجات والبحث
if action == "عرض المنتجات والبحث":
    st.header("عرض المنتجات والبحث")
    
    search_query = st.text_input("ابحث عن منتج بالاسم:")

    if not inventory:
        st.info("لا توجد منتجات مخزنة حاليًا. يمكنك إضافة منتجات جديدة من القائمة الجانبية.")
    else:
        product_list = []
        filtered_inventory = {pid: data for pid, data in inventory.items() if search_query.lower() in data['name'].lower()}

        if not filtered_inventory:
            st.warning(f"لم يتم العثور على منتجات تطابق البحث: '{search_query}'")
        else:
            for product_id, details in filtered_inventory.items():
                product_list.append({
                    'معرف المنتج': product_id,
                    'اسم المنتج': details['name'],
                    'الكمية': details['quantity'],
                    'السعر': int(details.get('price', 0)) # تحويل السعر لعدد صحيح عند العرض
                })
            st.table(product_list)

# 2. إضافة منتج جديد
elif action == "إضافة منتج جديد":
    st.header("إضافة منتج جديد")
    with st.form("new_product_form", clear_on_submit=True):
        product_name = st.text_input("اسم المنتج")
        product_quantity = st.number_input("الكمية", min_value=0, step=1)
        product_price = st.number_input("السعر", min_value=0, step=1) 
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
            st.rerun()
        elif submitted:
            st.error("الرجاء إدخال اسم المنتج.")

# 3. تعديل منتج (تم الإصلاح)
elif action == "تعديل منتج":
    st.header("تعديل بيانات منتج")
    if not inventory:
        st.warning("لا توجد منتجات لتعديلها.")
    else:
        product_items = [f"{details['name']} (ID: {pid})" for pid, details in inventory.items()]
        selected_item = st.selectbox("اختر المنتج للتعديل:", product_items, key="edit_select")

        if selected_item:
            selected_id = selected_item.split("ID: ")[1][:-1]
            product_data = inventory[selected_id]

            with st.form("edit_form"):
                st.write(f"تقوم بتعديل: {product_data['name']}")
                new_name = st.text_input("اسم المنتج", value=product_data['name'])
