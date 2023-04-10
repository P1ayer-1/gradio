import gradio as gr
from PIL import Image, ImageOps
import os

def add_content(history, file, text):
    if not text and file is None:
        return history, "", None
    
    if file is not None and text is not None:
        history = history + [((file.name, "any", text), None)]
        return history, "", None
    elif file is not None:
        history = history + [((file.name, "any"), None)]
        return history, "", None
    else:
        history = history + [(text, None)]
        return history, "", None

def generate_from_model_text(message):
    return message + " from text"

def add_file( file):
    return file.name

def generate_from_model_media(file, alt_text):
    img = Image.open(file)
    img_gray = ImageOps.grayscale(img)
    
    file_dir = os.path.dirname(file)
    new_file_name = 'processed_' + os.path.basename(file)
    new_file_path = os.path.join(file_dir, new_file_name)
    
    input_format = img.format.lower()

    # rotation seems to be messed up at times
    # img_gray = img_gray.transpose(Image.ROTATE_270)
    img_gray.save(new_file_path, format=input_format)

    new_alt_text = 'Processed image (grayscale): ' + alt_text
    return new_file_path, new_alt_text

def bot(history):

    if len(history[-1][0]) == 3 and history[-1][0][-1] == "":
        file_name = history[-1][0][0]
        if history[-1][0][1] is not None:
            alt_text = history[-1][0][1]
        else:
            alt_text = "None"
        new_file_name, new_alt_text = generate_from_model_media(file_name, alt_text)
        history[-1][1] = (new_file_name, new_alt_text)
        return history
    elif len(history[-1][0]) == 3:
        file_name = history[-1][0][0]
        alt_text = history[-1][0][1]
        user_text = history[-1][0][2]
        response = generate_from_model_text(user_text)
        new_file_name, new_alt_text = generate_from_model_media(file_name, alt_text)
        history[-1][1] = (new_file_name, new_alt_text, response)
        return history
    else:
        user_text = history[-1][0]
        response = generate_from_model_text(user_text)
        history[-1][1] = response
        return history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot([], elem_id="chatbot").style(height=750)
    with gr.Row():
        file_output = gr.File(visible=False)
        with gr.Column(scale=0.85):
            txt = gr.Textbox(
                show_label=False,
                placeholder="Enter text and press enter, or upload an image",
            ).style(container=False)
        with gr.Column(scale=0.15, min_width=0):
            btn = gr.UploadButton("Upload File", file_types=["image", "video", "audio"])
            submit_btn = gr.Button("Submit")



    submit_btn.click(fn=add_content, inputs=[chatbot, btn, txt], outputs=[chatbot, txt, btn], queue=False).then(
        bot, chatbot, chatbot
    )
    

    btn.upload(add_file, [btn], [file_output])


demo.launch()
