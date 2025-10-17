inventory[selected_id] = {
                        "name": new_name,
                        "quantity": new_quantity,
                        "price": new_price
                    }
                    save_inventory(inventory)
                    st.success(f"تم تحديث بيانات المنتج '{new_name}' بنجاح!")
                    st.rerun() # لإعادة تحميل الصفحة وعرض البيانات المحدثة

# 4. حذف منتج
elif action == "حذف منتج":
    st.header("حذف منتج")
    if not inventory:
        st.warning("لا توجد منتجات لحذفها.")
    else:
        product_ids = list(inventory.keys())
        product_names = [f"{inventory[pid]['name']} (ID: {pid})" for pid in product_ids]
        
        selected_product_name_to_delete = st.selectbox("اختر المنتج للحذف:", product_names, key="delete_select")
        
        if selected_product_name_to_delete:
            selected_id_to_delete = selected_product_name_to_delete.split("ID: ")[1].replace(")", "")
            product_name_to_delete = inventory[selected_id_to_delete]['name']

            if st.button(f"تأكيد حذف المنتج '{product_name_to_delete}'"):
                del inventory[selected_id_to_delete]
                save_inventory(inventory)
                st.success(f"تم حذف المنتج '{product_name_to_delete}' بنجاح.")
                st.rerun() # لإعادة تحميل الصفحة
    
