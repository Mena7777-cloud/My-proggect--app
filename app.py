updated_product = {"name": new_name, "quantity": int(new_quantity), "price": float(new_price)}
                    st.session_state.inventory[original_index] = updated_product
                    save_data(st.session_state.inventory)
                    st.success("تم تحديث بيانات المنتج بنجاح!")
                    st.rerun()

# --- ❌ حذف منتج ---
elif menu_choice == "❌ حذف منتج":
    st.subheader("حذف منتج من المخزون")
    if not st.session_state.inventory:
        st.warning("لا توجد منتجات لحذفها.")
    else:
        product_names = [p['name'] for p in st.session_state.inventory]
        product_to_delete = st.selectbox("اختر المنتج الذي تريد حذفه:", product_names)
        
        if st.button(f"🗑️ حذف المنتج '{product_to_delete}' بشكل نهائي"):
            product_index = next((i for i, p in enumerate(st.session_state.inventory) if p['name'] == product_to_delete), None)
            if product_index is not None:
                st.session_state.inventory.pop(product_index)
                save_data(st.session_state.inventory)
                st.warning(f"تم حذف المنتج '{product_to_delete}' بنجاح.")
                st.rerun()
