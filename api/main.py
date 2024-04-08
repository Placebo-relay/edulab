import streamlit as st
import pandas as pd
from googletrans import Translator

# Function to chunk the JSON data
def chunk_json_data(data, chunk_size=300):
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    return chunks

# Function to translate a chunk of data
def translate_chunk(chunk):
    translator = Translator()
    translated_chunk = []
    for index, row in chunk.iterrows():
        translated_text = translator.translate(row['text'], dest='en').text
        translated_chunk.append({'original_text': row['text'], 'translated_text': translated_text})
    return pd.DataFrame(translated_chunk)

# Streamlit app
def main():
    st.title('JSON Translator App')

    # File upload
    uploaded_file = st.file_uploader("Upload JSON file", type=["json"])

    if uploaded_file is not None:
        data = pd.read_json(uploaded_file)

        st.write(f"Original data: {data}")

        # Chunk the data
        data_chunks = chunk_json_data(data, chunk_size=300)

        # Translate and display each chunk
        for i, chunk in enumerate(data_chunks):
            st.write(f"Translated chunk {i+1}:")
            translated_chunk = translate_chunk(chunk)
            st.write(translated_chunk)

if __name__ == "__main__":
    main()
