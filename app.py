<div class="card">
                            <div style="display: flex;">
                                <div style="flex: 1;">{image_html}</div>
                                <div style="flex: 3;">
                                    <h4>{row['name']}</h4>
                                    <p><strong>الوصف:</strong> {row['description']}</p>
                                    <p><strong>الكمية:</strong> {row['quantity']}</p>
                                    <p><strong>السعر:</strong> {row['price']} جنيه</p>
                                    <p><strong>الفئة:</strong> {row['category']}</p>
                                    <p><strong>تاريخ الإضافة:</strong> {row['date_added']}</p>
                                    <p><strong>تاريخ الصلاحية:</strong> {row['expiry_date']}</p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.markdown("### جميع المنتجات")
            st.dataframe(st.session_state.products.drop(columns=['image']), use_container_width=True)

# إضافة منتج جديد
if option == "➕ إضافة منتج" and st.session_state.logged_in:
    st.subheader("➕ إضافة منتج جديد")
    with st.form("add_product_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("اسم المنتج (بالعربي):", max_chars=50)
            quantity = st.number_input("الكمية:", min_value=0, step=1)
            category = st.selectbox("الفئة:", ["غذاء", "إلكترونيات", "ملابس", "أخرى"])
        with col2:
            description = st.text_area("الوصف التفصيلي:", height=100)
            price = st.number_input("السعر:", min_value=0.0, step=0.01)
            expiry_date = st.date_input("تاريخ الصلاحية (YYYY-MM-DD):", min_value=date.today())
        image = st.file_uploader("ارفعي صورة المنتج (اختياري):", type=["jpg", "png"])
        
        submitted = st.form_submit_button("إضافة المنتج", use_container_width=True)
    
    if submitted:
        if name:
            image_data = image_to_base64(image) if image else None
            new_product = pd.DataFrame({
                'name': [name],
                'description': [description],
                'quantity': [quantity],
                'price': [price],
                'category': [category],
                'date_added': [datetime.now().strftime("%Y-%m-%d")],
                'expiry_date': [expiry_date.strftime("%Y-%m-%d")],
                'image': [image_data]
            })
            st.session_state.products = pd.concat([st.session_state.products, new_product], ignore_index=True)
            st.success(f"🎉 تم إضافة المنتج '{name}' بنجاح!")
        else:
            st.error("⚠️ الرجاء إدخال اسم المنتج.")

# تعديل منتج
if option == "✏️ تعديل منتج" and st.session_state.logged_in:
    st.subheader("✏️ تعديل منتج")
    if st.session_state.products.empty:
        st.warning("⚠️ لا توجد منتجات للتعديل.")
    else:
        product_names = st.session_state.products['name'].tolist()
        selected_name = st.selectbox("اختر المنتج للتعديل:", product_names)
        if selected_name:
            idx = st.session_state.products[st.session_state.products['name'] == selected_name].index[0]
            with st.form("edit_product_form"):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("اسم المنتج (جديد):", value=st.session_state.products.at[idx, 'name'])
                    quantity = st.number_input("الكمية:", value=int(st.session_state.products.at[idx, 'quantity']), min_value=0)
                    category = st.selectbox("الفئة:", ["غذاء", "إلكترونيات", "ملابس", "أخرى"], 
                                           index=["غذاء", "إلكترونيات", "ملابس", "أخرى"].index(st.session_state.products.at[idx, 'category']))with col2:
                    description = st.text_area("الوصف:", value=st.session_state.products.at[idx, 'description'], height=100)
                    price = st.number_input("السعر:", value=float(st.session_state.products.at[idx, 'price']), min_value=0.0)
                    expiry_date = st.date_input("تاريخ الصلاحية:", value=date.fromisoformat(st.session_state.products.at[idx, 'expiry_date']))
                image = st.file_uploader("ارفعي صورة جديدة (اختياري):", type=["jpg", "png"])
                
                submitted = st.form_submit_button("حفظ التعديلات", use_container_width=True)
            
            if submitted:
                image_data = image_to_base64(image) if image else st.session_state.products.at[idx, 'image']
                st.session_state.products.at[idx, 'name'] = name
                st.session_state.products.at[idx, 'description'] = description
                st.session_state.products.at[idx, 'quantity'] = quantity
                st.session_state.products.at[idx, 'price'] = price
                st.session_state.products.at[idx, 'category'] = category
                st.session_state.products.at[idx, 'expiry_date'] = expiry_date.strftime("%Y-%m-%d")
                st.session_state.products.at[idx, 'image'] = image_data
                st.success(f"🎉 تم تعديل المنتج '{name}' بنجاح!")

# حذف منتج
if option == "🗑️ حذف منتج" and st.session_state.logged_in:
    st.subheader("🗑️ حذف منتج")
    if st.session_state.products.empty:
        st.warning("⚠️ لا توجد منتجات للحذف.")
    else:
        product_names = st.session_state.products['name'].tolist()
        selected_name = st.selectbox("اختر المنتج للحذف:", product_names)
        if st.button("حذف المنتج", type="primary"):
            st.session_state.products = st.session_state.products[st.session_state.products['name'] != selected_name]
            st.success(f"✅ تم حذف المنتج '{selected_name}' بنجاح!")
