import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
from io import BytesIO

st.set_page_config(page_title="WhatsApp Direct AI Translator", page_icon="🎙️")
st.title("🎙️ WhatsApp Direct Voice & Text Translator AI")
st.write("ল্যাপটপে হোয়াটসঅ্যাপ অডিও প্লে করুন -> এআই সরাসরি রেকর্ড করে ট্রান্সফার করে দেবে!")

# ভাষা সিলেক্ট করার মেনু
source_lang = st.selectbox("1. Select WhatsApp Audio Language", ["Bengali", "English", "Hindi", "Spanish"])
target_lang = st.selectbox("2. Select Output Language (Want to transfer into)", ["English", "Spanish", "Hindi", "Bengali", "Korean", "Urdu", "Sanskrit"])

lang_codes = {"Bengali": "bn", "English": "en", "Hindi": "hi", "Spanish": "es", "Korean": "ko", "Urdu": "ur", "Sanskrit": "sa"}

st.subheader("🔴 WhatsApp Audio Recorder:")
audio_bytes = st.audio_input("১. এখানে 'Record' চাপুন -> ২. ল্যাপটপে হোয়াটসঅ্যাপ অডিওটি প্লে করুন:")

if audio_bytes is not None:
    st.audio(audio_bytes, format="audio/wav")
    
    if st.button("Start AI Process ✨"):
        with st.spinner("AI is processing..."):
            try:
                recognizer = sr.Recognizer()
                
                audio_file = BytesIO(audio_bytes.read())
                with sr.AudioFile(audio_file) as source:
                    audio_data = recognizer.record(source)
                    input_text = recognizer.recognize_google(audio_data, language=lang_codes[source_lang])
                
                st.subheader("📝 Text Result:")
                st.success(f"Original Text: {input_text}")
                
                # নতুন শক্তিশালী ডিপ-ট্রান্সলেটর অ্যালগরিদম
                translated_text = GoogleTranslator(source=lang_codes[source_lang], target=lang_codes[target_lang]).translate(input_text)
                
                st.subheader("🔄 Translation Result:")
                st.info(f"Translated Text ({target_lang}): {translated_text}")
                
                # নতুন ভয়েস তৈরি
                tts = gTTS(text=translated_text, lang=lang_codes[target_lang], slow=False)
                tts.save("whatsapp_output.mp3")
                
                st.subheader("🔊 Listen in New Language:")
                st.audio("whatsapp_output.mp3", format="audio/mp3")
                os.remove("whatsapp_output.mp3")
                
            except Exception as e:
                st.error("Sorry! The audio wasn't clear. Please try again.")