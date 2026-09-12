import streamlit as st
import google.genai as genai

# إعداد الشاشة
st.set_page_config(page_title="المساعد الطبي للدراسة", page_icon="🩺")
st.title("🩺 المساعد الطبي للدراسة")

# إدخال مفتاح API
api_key = st.sidebar.text_input("أدخل مفتاح Gemini API الخاص بك:", type="password")

if api_key:
    client = genai.Client(api_key=api_key)

    # تهيئة سجل المحادثة
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض المحادثات السابقة
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # استقبال سؤال المستخدم
    if prompt := st.chat_input("اطرح سؤالك الطبي هنا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # توليد الإجابة
        with st.chat_message("assistant"):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
else:
    st.info("يرجى إدخال مفتاح API في القائمة الجانبية للبدء.")
