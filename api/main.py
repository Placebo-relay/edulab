import streamlit as st
import json
from googletrans import Translator

# Function to translate the values of a JSON with a cache for translated values
def translate_json_values_with_cache(json_data, translation_cache, source_lang, target_lang, max_entries=300):
    translator = Translator()
    translated_json = {}
    entry_count = 0
    for key, value in json_data.items():
        if entry_count >= max_entries:
            translated_json[key] = value
            continue
        if isinstance(value, str):
            if (value, source_lang, target_lang) in translation_cache:
                translated_json[key] = translation_cache[(value, source_lang, target_lang)]
            else:
                try:
                    translated_value = translator.translate(value, src=source_lang, dest=target_lang).text
                    translated_json[key] = translated_value
                    translation_cache[(value, source_lang, target_lang)] = translated_value
                except Exception as e:
                    translated_json[key] = value
            entry_count += 1
        else:
            translated_json[key] = value
    return translated_json, translation_cache

# Streamlit app
def main():
    st.title('JSON Translator App')

    # File upload
    uploaded_file = st.file_uploader("Upload JSON file", type=["json"])

    if uploaded_file is not None:
        data = json.load(uploaded_file)

        st.write(f"Original data: {data}")

        # Language selection
        source_lang = st.selectbox("Select source language", options=['auto', 'en', 'es', 'fr', 'de', 'it', 'ja', 'ko', 'zh-CN'])
        target_lang = st.selectbox("Select target language", options=['en', 'es', 'fr', 'de', 'it', 'ja', 'ko', 'zh-CN'])

        # Load or initialize the translation cache
        if 'translation_cache' not in st.session_state:
            st.session_state.translation_cache = {}

        # Translate the values
        translated_data, st.session_state.translation_cache = translate_json_values_with_cache(data, st.session_state.translation_cache, source_lang, target_lang)
        st.write("Partly translated data:")
        st.write(translated_data)

if __name__ == "__main__":
    main()
