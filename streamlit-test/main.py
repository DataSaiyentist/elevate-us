import streamlit as st
from back import get_all_zdc, get_list_of_equipements, get_accessibilite
from edit_grievances import add_grievances

import whisper
from add_state_to_equipements import AVAILABLE, UNAVAILABLE

# from st_clickable_images import clickable_images
# import base64


@st.cache_resource
def get_whisper():
    return whisper.load_model("base")


@st.dialog("Quel est le problème avec l'équipement ?")
def grieve(key, supposed_state):
    text = st.text_area("décrivez la situation (optionnel)")
    left, right = st.columns(2)
    if left.button("Problème"):
        add_grievances(key, UNAVAILABLE, text)
    if right.button("En fonctionnement"):
        add_grievances(key, AVAILABLE, text)

    # audio = audiorecorder("Dites vos doléances", key=key+"_audio_input")
    # if audio:
    #     audio.export("audio.wav", format="wav")
    #     transcription = get_whisper().transcribe("audio.wav")
    #     st.write(transcription["text"])
    # audio = st.audio_input("Dites vos doléances", key="audio_input_" + key)
    # result = st.text_area("Ecrivez vos doléances", key="text_area_" + key)
    # # , value=st.session_state.get("text", ""))
    # if audio:
    #     with open("audio.wav", "wb") as f:
    #         f.write(audio.getbuffer())
    #     result = get_whisper().transcribe("audio.wav", language="fr")["text"]
    #     st.write(result)
    # if len(result) > 0:
    #     add_grievances(key, state, result)
    #     # st.write("done")


zdc = st.selectbox("Sélectionner gare", get_all_zdc(), index=None)

if zdc is None:
    st.stop()

# st.write(get_accessibilite(zdc))


# st.markdown(f"![Foo](http://estacions.albertguillaumes.cat/img/paris/{zdc.lower()}.png)")

for key, values in get_list_of_equipements(zdc).items():
    left, middle, little_middle, right = st.columns([0.3, 0.3, 0.05, 0.3])

    status = values.get("state")
    st.write(status)

    # if status == AVAILABLE:
    #     message = "signaler un problème"
    # elif status == UNAVAILABLE:
    #     message = "le problème est toujours là"
    # else:
    #     st.error("erreur")
    #     st.stop()

    left.write(key)
    left.write(values.get("liftsituation", ""))
    middle.image("static/img/ascenseur.png", width=50)

    # left.write(f"info: {message}")

    # if key.startswith("escalier"):
    #     middle.image("static/img/escalator.png", width=100)
    # elif key.startswith("ascenseur"):
    #     middle.image("static/img/ascenseur.png", width=100)
    #     left.write(values["liftsituation"])

    # with open(f"static/img/thumb-{'down' if status == AVAILABLE else 'up'}.png", "rb") as image:
    #     encoded = base64.b64encode(image.read()).decode()
    #     thumb = f"data:image/jpeg;base64,{encoded}"
    # with little_middle:
    #     clicked = clickable_images(
    #         [thumb],
    #         # div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
    #         img_style={"height": "20px"},
    #         key="thumb_" + key,
    #     )
    little_middle.image(
        f"static/img/thumb-{'down' if status == UNAVAILABLE else 'up'}.png"
    )

    if right.button("signaler", key=key):
        grieve(key, None)
