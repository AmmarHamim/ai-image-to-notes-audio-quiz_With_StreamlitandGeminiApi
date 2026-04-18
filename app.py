import streamlit as st
from api_call import note_generator,audio_transcription,quiz_generator
from PIL import Image
import re

st.title("Note summary and Quiz Generator")
st.markdown("Upload upto 3 images")
st.divider()

with st.sidebar:
    st.header("Controls")
    #images
    images=st.file_uploader("Upload the photos",type=["jpg","jpeg","png"],accept_multiple_files=True)

    pil_images=[]
    for img in images:
        pil_img=Image.open(img)
        pil_images.append(pil_img)

    if images:
        if len(images)>3:
            st.error("upload upto 3 images")
        else:
            col=st.columns(len(images))

            for i,img in enumerate(images):
                with col[i]:
                    st.image(img)

    
    #dificulty
    selected_opt=st.selectbox("Select a difficulty for your quiz",["Easy","Medium","Hard"],index=None)
    

    pressed=st.button("Click here to generate",type="primary")


if pressed:
    if not images:
        st.error("You must upload a image")
    if not selected_opt:
        st.error("You must select a difficulty")

    if images and selected_opt:

        #note container

        with st.container(border=True):
            st.subheader("Your note")

            with st.spinner("generating...."):
                generated_notes=note_generator(pil_images)
                st.markdown(generated_notes)

        #audio transcript
        with st.container(border=True):
            st.subheader("Audio Transcription")

            # generated_notes=generated_notes.replace("#","")
            # generated_notes=generated_notes.replace("*","")
            # generated_notes=generated_notes.replace("-","")            
            # generated_notes=generated_notes.replace("]","")            
            # generated_notes=generated_notes.replace("[","")            
            # generated_notes=generated_notes.replace(":","")  

            generated_notes = re.sub(r'[#*\[\]`]', '', generated_notes)   # remove symbols
            generated_notes = re.sub(r'-\s+', '. ', generated_notes)     # list → pause
            generated_notes = re.sub(r'\s+', ' ', generated_notes).strip()          

            with st.spinner("generating audio..."):
                audio_transcript=audio_transcription(generated_notes)
                st.audio(audio_transcript)

        #quiz
        with st.container(border=True):
            st.subheader(f"Your quiz difficulty is {selected_opt}")
            with st.spinner("Generating quiz..."):
                generated_quiz=quiz_generator(pil_images,selected_opt)
                st.markdown(generated_quiz)
