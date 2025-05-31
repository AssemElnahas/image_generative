import streamlit as st
import openai
from PIL import Image
import io
import requests


def generate_image(prompt, size="1024x1024"):
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": f"Generate an image of: {prompt}"}
    ],
    tools=[{"type": "image_generation", "params": {"model": "dall-e-3"}}]
)

    image_url = response['data'][0]['url']
    return image_url


def main():
    st.title("🖼️ Image Generator with DALL·E")

    st.subheader("🔐 OpenAI API Key")
    st.markdown(
        "Please enter your OpenAI API key below. "
        "You can get one from "
        "[platform.openai.com](https://platform.openai.com/account/api-keys)."
    )
    api_key = st.text_input("API Key", type="password", key="api_key")

    if api_key:
        openai.api_key = api_key
        st.success("API key loaded successfully.")

        prompt = st.text_input("💬 Enter your image prompt", key="prompt")

        if st.button("🎨 Generate Image"):
            if prompt:
                with st.spinner("Generating..."):
                    try:
                        image_url = generate_image(prompt)
                        image = Image.open(requests.get(image_url, stream=True).raw)
                        st.image(image, caption=prompt)
                    except Exception as e:
                        st.error(f"Failed to generate image: {e}")
            else:
                st.warning("Please enter a prompt.")
    else:
        st.info("Enter your OpenAI API key to get started.")


if __name__ == "__main__":
    main()
