import streamlit as st
import requests


def load_image():
    uploaded_file = st.file_uploader(label='Загрузите изображение')
    if uploaded_file is not None:
        image_data = uploaded_file.getvalue()
        st.image(image_data)
        return image_data
    else:
        return None


st.title('Object Detection')
img = load_image()
result = st.button('Детектировать изображение')

if result:
    result = requests.post(url='http://127.0.0.1:8000/detect-image',
                           files={'image_file': img})

    st.image(result.content)
    btn_for_dwnld = st.download_button(
        label="Download Image",
        data=result.content,
        mime="image/jpeg",
    )
