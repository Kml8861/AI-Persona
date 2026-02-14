import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel
import os
print("CWD:", os.getcwd())

#
# model = Qwen3TTSModel.from_pretrained(
#     "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
#     device_map="cuda:0",
#     dtype=torch.bfloat16,
#     attn_implementation="eager",
# )
#
# # single inference
# wavs, sr = model.generate_custom_voice(
#     text="Hello. How are you? Everything is okay? What would you like to do next? I'm here to help you.",
#     language="English", # Pass `Auto` (or omit) for auto language adaptive; if the target language is known, set it explicitly.
#     speaker="Vivian",
#     instruct="talk with sincerity and peace", # Omit if not needed.
# )
# sf.write("output_custom_voice.wav", wavs[0], sr)

# # batch inference
# wavs, sr = model.generate_custom_voice(
#     text=[
#         "其实我真的有发现，我是一个特别善于观察别人情绪的人。",
#         "She said she would be here by noon."
#     ],
#     language=["Chinese", "English"],
#     speaker=["Vivian", "Ryan"],
#     instruct=["", "Very happy."]
# )
# sf.write("output_custom_voice_1.wav", wavs[0], sr)
# sf.write("output_custom_voice_2.wav", wavs[1], sr)










#tts.speak(text, expression_state) zrobić nawet jak expression_state = None