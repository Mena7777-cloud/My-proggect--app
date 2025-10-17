st.warning("لا توجد منتجات لتعديلها.")
    else:
        # إنشاء قائمة بأسماء المنتجات مع معرفاتها للاختيار منها
        product_ids = list(inventory.keys())
        product_names = [f"{inventory[pid]['name']} (ID: {pid})" for pid in product_ids]
        
        selected_product_display = st.selectbox("اختر المنتج للتعديل:", product_names)
        
        if selected_product_display:
            # استخراج المعرف من النص المختار
            selected_id = selected_product_display.split("ID: ")[1].replace(")", "")
            product_data = inventory[selected_id]

            # نموذج لتعديل بيانات المنتج المختار
            with st.form("edit_product_form"):
                st.write(f"أنت تقوم بتعديل المنتج: {product_data['name']}")
                new_name = st.text_input("اسم المنتج الجديد", value=product_data['name'])
                new_quantity = st.number_input("الكمية الجديدة", min_value=0, step=1, value=product_data['quantity'])
                new_price = st.number_input("السعر الجديد", min_value=0.0, format="%.2f", value=product_data['price'])
                
                update_button = st.form_submit_button("تحديث المنتج")

                if update_button:
                    # تحديث بيانات المنتج في القاموس
                    inventory[selected_id] = {
                        "name": new_name,
                        "quantity": new_quantity,
                        "price": new_price
                    }
                    # حفظ التغييرات
                    save_inventory(inventory)
                    st.success(f"تم تحديث بيانات المنتج '{new_name}' بنجاح!")
                    # إعادة تحميل الصفحة لإظهار التغييرات فورًا
                    st.rerun()

# 4. إذا اختار المستخدم "حذف منتج"
elif action == "حذف منتج":
    st.header("حذف منتج")
    if not inventory:
        st.warning("لا توجد منتجات لحذفها.")
    else:
        # إنشاء قائمة بأسماء المنتجات مع معرفاتها للاختيار منها
        product_ids = list(inventory.keys())
        product_names = [f"{inventory[pid]['name']} (ID: {pid})" for pid in product_ids]
        
        selected_product_to_delete_display = st.selectbox("اختر المنتج للحذف:", product_names, key="delete_select")
        
        if selected_product_to_delete_display:
            # استخراج المعرف من النص المختار
            selected_id_to_delete = selected_product_to_delete_display.split("ID: ")[1].replace(")", "")
            product_name_to_delete = inventory[selected_id_to_delete]['name']

            # زر تأكيد الحذف لتجنب الحذف عن طريق الخطأ
            if st.button(f"تأكيد حذف المنتج '{product_name_to_delete}'"):
                # حذف المنتج من القاموس
                del inventory[selected_id_to_delete]
                # حفظ التغييرات
                save_inventory(inventory)
                st.success(f"تم حذف المنتج '{product_name_to_delete}' بنجاح.")
                # إعادة تحميل الصفحة
                st.rerun()
