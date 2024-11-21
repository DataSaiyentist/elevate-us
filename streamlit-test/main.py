import streamlit as st
from back import get_all_zdc, get_list_of_equipements
import whisper
from audiorecorder import audiorecorder
import io

@st.cache_resource
def get_whisper():
    return whisper.load_model("base")


zdc = st.selectbox("Sélectionner gare", get_all_zdc(), index=None)

if zdc is None:
    st.stop()

for key, values in get_list_of_equipements(zdc).items():
    left, middle, right = st.columns(3)
    left.write(key)
    if key.startswith("escalier"):
        middle.image("static/img/escalator.png", width=100)
    elif key.startswith("ascenseur"):
        middle.image("static/img/ascenseur.png", width=100)
        left.write(values["liftsituation"])

    if right.toggle("Grieve", key=key):
        audio = audiorecorder("Dites vos doléances", key=key+"_audio_input")

        if audio:
            # with open('myfile.wav', mode='bx') as f:
            #     f.write(audio)

            # audio.seek(0)


            # rate, audio = read(io.BytesIO(audio))
            audio.export("audio.wav", format="wav")
            transcription = get_whisper().transcribe("audio.wav")
            st.write(transcription["text"])
            print(transcription)
