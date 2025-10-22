import streamlit as st
import pandas as pd
from datetime import datetime, date

# عنوان التطبيق
st.title("إدارة التخزين - Storage Management System")
st.header("نظام إدارة التخزين")

# إعداد الجلسة للبيانات والتسجيل
if 'products' not in st.session_state:
    st.session_state.products = pd.DataFrame(columns=[
        'name', 'description', 'quantity', 'price', 'category', 'date_added', 'expiry_date'
    ])

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# نظام الصلاحيات: تسجيل دخول
if not st.session_state.logged_in:
    st.subheader("تسجيل الدخول للتحكم الكامل")
    password = st.text_input("كلمة المرور:", type="password")
    if st.button("تسجيل دخول"):
        if password == "secret":  # غيري "secret" لكلمة مرور خاصة بيكِ
            st.session_state.logged_in = True
            st.success("تم تسجيل الدخول بنجاح! الآن تقدري تضيفي/تعدلي/تحذفي.")
            st.rerun()  # إعادة تحميل الصفحة
        else:
            st.error("كلمة المرور خاطئة. جربي تاني.")
    st.info("بدون تسجيل، تقدري بس تشوفي العرض والبحث.")
    is_admin = False
else:
    st.success("أنتِ مسجلة الدخول كمديرة. تقدري تتحكمي في كل حاجة.")
    if st.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()
    is_admin = True

# خيارات التشغيل في الـ sidebar
options = ["عرض المنتجات والبحث"]
if is_admin:
    options += ["إضافة منتج جديد", "تعديل منتج", "حذف منتج"]

option = st.sidebar.selectbox("اختر الإجراء المطلوب:", options)

# عرض المنتجات والبحث (متاح للجميع)
if option == "عرض المنتجات والبحث":
    st.subheader("عرض المنتجات والبحث")
    search_term = st.text_input("ابحث عن منتج بالاسم (بالعربي):")
    
    if st.session_state.products.empty:
        st.warning("لا توجد منتجات مخزنة حاليًا. يمكنك إضافة منتجات جديدة إذا كنتِ مسجلة الدخول.")
    else:
        # بحث غير حساس لحالة الحروف، بالعربي
        if search_term:
            filtered = st.session_state.products[
                st.session_state.products['name'].str.contains(search_term, case=False, na=False)
            ]
            if filtered.empty:
                st.info("لم يتم العثور على منتجات تطابق البحث.")
            else:
                st.dataframe(filtered, use_container_width=True)
        else:
            st.dataframe(st.session_state.products, use_container_width=True)

# إضافة منتج جديد (للمدير فقط)
elif option == "إضافة منتج جديد" and is_admin:
    st.subheader("إضافة منتج جديد")
    with st.form("add_product_form"):
        name = st.text_input("اسم المنتج (بالعربي):", max_chars=50)
        description = st.text_area("الوصف التفصيلي:")
        quantity = st.number_input("الكمية:", min_value=0, step=1)
        price = st.number_input("السعر:", min_value=0.0, step=0.01)
        category = st.selectbox("الفئة:", ["غذاء", "إلكترونيات", "ملابس", "أخرى"])
        expiry_date = st.date_input("تاريخ الصلاحية (YYYY-MM-DD):", min_value=date.today())
        
        submitted = st.form_submit_button("إضافة المنتج")
    
    if submitted:
        if name:
            new_product = pd.DataFrame({
                'name': [name],
                'description': [description],
                'quantity': [quantity],
                'price': [price],
                'category': [category],
                'date_added': [datetime.now().strftime("%Y-%m-%d")],  # تاريخ غربي تلقائي
                'expiry_date': [expiry_date.strftime("%Y-%m-%d")]
            })
            st.session_state.products = pd.concat([st.session_state.products, new_product], ignore_index=True)
            st.success(f"تم إضافة المنتج '{name}' بنجاح!")
        else:
            st.error("الرجاء إدخال اسم المنتج.")

# تعديل منتج (للمدير فقط)
elif option == "تعديل منتج" and is_admin:
    st.subheader("تعديل منتج")
    if st.session_state.products.empty:
        st.warning("لا توجد منتجات للتعديل.")else:
        product_names = st.session_state.products['name'].tolist()
        selected_name = st.selectbox("اختر المنتج للتعديل:", product_names)
        if selected_name:
            idx = st.session_state.products[st.session_state.products['name'] == selected_name].index[0]
            with st.form("edit_product_form"):
                name = st.text_input("اسم المنتج (جديد):", value=st.session_state.products.at[idx, 'name'])
                description = st.text_area("الوصف:", value=st.session_state.products.at[idx, 'description'])
                quantity = st.number_input("الكمية:", value=st.session_state.products.at[idx, 'quantity'], min_value=0)
                price = st.number_input("السعر:", value=st.session_state.products.at[idx, 'price'], min_value=0.0)
                category = st.selectbox("الفئة:", ["غذاء", "إلكترونيات", "ملابس", "أخرى"], index=["غذاء", "إلكترونيات", "ملابس", "أخرى"].index(st.session_state.products.at[idx, 'category']))
                expiry_date = st.date_input("تاريخ الصلاحية:", value=date.fromisoformat(st.session_state.products.at[idx, 'expiry_date']))
                
                submitted = st.form_submit_button("حفظ التعديلات")
            
            if submitted:
                st.session_state.products.at[idx, 'name'] = name
                st.session_state.products.at[idx, 'description'] = description
                st.session_state.products.at[idx, 'quantity'] = quantity
                st.session_state.products.at[idx, 'price'] = price
                st.session_state.products.at[idx, 'category'] = category
                st.session_state.products.at[idx, 'expiry_date'] = expiry_date.strftime("%Y-%m-%d")
                st.success(f"تم تعديل المنتج '{name}' بنجاح!")

# حذف منتج (للمدير فقط)
elif option == "حذف منتج" and is_admin:
    st.subheader("حذف منتج")
    if st.session_state.products.empty:
        st.warning("لا توجد منتجات للحذف.")
    else:
        product_names = st.session_state.products['name'].tolist()
        selected_name = st.selectbox("اختر المنتج للحذف:", product_names)
        if st.button("حذف المنتج"):
            st.session_state.products = st.session_state.products[st.session_state.products['name'] != selected_name
