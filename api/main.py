import streamlit as st
from google.cloud import translate_v2 as translate
import pandas as pd
import json
import io

# Create a Streamlit app
st.title('JSON Translator')

# Ask the user to upload a JSON file
uploaded_file = st.file_uploader("Upload a JSON file", type="json")

if uploaded_file is not None:
    # Read the uploaded JSON file
    json_data = json.load(uploaded_file)

    # Ask the user to select the language for translation
    target_language = st.selectbox('Select the target language', ['Spanish', 'French', 'German'])

    # Ask the user for the number of entries and the starting entry
    num_entries = st.number_input('Enter the number of entries to process', min_value=1, max_value=len(json_data))
    start_entry = st.number_input('Enter the starting entry', min_value=1, max_value=len(json_data))

    # Extract the specified number of entries starting from the specified entry
    extracted_data = json_data[start_entry-1:start_entry+num_entries-1]

    # Translate the values of the extracted entries to the selected language
    translator = translate.Client()
    translated_data = []
    for entry in extracted_data:
        translated_entry = {}
        for key, value in entry.items():
            translated_text = translator.translate(value, target_language=target_language)
            translated_entry[key] = translated_text['translatedText']
        translated_data.append(translated_entry)

    # Create a DataFrame from the translated data
    translated_df = pd.DataFrame(translated_data)

    # Allow the user to download the modified JSON file
    st.write(translated_df)
    csv = translated_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="translated_data.csv">Download translated data</a>'
    st.markdown(href, unsafe_allow_html=True)

    # Allow the user to download the original JSON file
    st.write(json_data)
    original_json = json.dumps(json_data, indent=4)
    b64_original = base64.b64encode(original_json.encode()).decode()
    href_original = f'<a href="data:file/json;base64,{b64_original}" download="original_data.json">Download original data</a>'
    st.markdown(href_original, unsafe_allow_html=True)
