import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image

# load all environment variables
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content([input_prompt, image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # read file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]

        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
# streamlit app -> Frontend Setup
st.set_page_config(page_title="Calorie Advisor")

st.header("Built using Gemini")
uploaded_file = st.file_uploader("Choose an Image...", type=["jpg", "png", "jpeg"])
image = "" 
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=None)

submit = st.button("Tell me about the total calories")

input_prompt = """
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
        Finally you can also mention the food is healthy or not and also tell the percentage of healthy food items in the image and percentage split of fats, proteins, carbohydrates, sugar & other important things essential for diet


"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data)
    st.header("The Response is: ")
    st.write(response)


