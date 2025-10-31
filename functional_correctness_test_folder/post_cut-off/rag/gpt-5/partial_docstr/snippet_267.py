
# Initialize the KokoroTTS model
# 🇺🇸 'a' => American English, 🇬🇧 'b' => British English, 🇪🇸 'e' => Spanish, etc.
tts = KokoroTTS(lang_code="a")
# Generate speech from text
text = "The sky above the port was the color of television, tuned to a dead channel."
audios = tts(text=text, voice="af_heart", output_prefix="output")
# To listen in a notebook:
# from IPython.display import Audio, display
# display(Audio(audios[0], rate=24000))
