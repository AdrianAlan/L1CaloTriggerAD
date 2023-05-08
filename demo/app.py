import gradio as gr
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from huggingface_hub import from_pretrained_keras
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Flatten
from qkeras import *


def load_keras_model(model_path: str):
    org_model = from_pretrained_keras(model_path)
    input_ = Input(shape=(18, 14), name="inputs_")
    x = Flatten()(input_)
    for layer in org_model.layers[1:]:
        x = layer(x)
    output = Activation("linear", name="outputs")(x)
    return Model(input_, output, name="cicada")


def parse_input(et):
    if not et:
        raise gr.Error("Provide the input")

    et = [e.split(",") for e in et.split("\n")]
    et = np.array(et)
    et = et.astype(np.float32)

    if et.shape != (18, 14):
        raise gr.Error("The input shape has to be 18 rows and 14 columns")
    if np.any(et < 0) or np.any(et > 1023):
        raise gr.Error("The input has to be in a range (0, 1023)!")

    return et.reshape(1, 18, 14)


def inference(input_):
    input_ = parse_input(input_)
    return model.predict(input_)[0][0]


def saliency(input_):
    input_ = parse_input(input_)
    x = tf.constant(input_)
    with tf.GradientTape() as tape:
        tape.watch(x)
        predictions = model(x)
    gradient = tape.gradient(predictions, x)
    gradient = gradient.numpy()
    min_val, max_val = np.min(gradient), np.max(gradient)
    gradient = (gradient - min_val) / (max_val - min_val + tf.keras.backend.epsilon())

    fig_i = plt.figure()
    plt.imshow(input_.reshape(18, 14), cmap="Reds")
    plt.colorbar()
    plt.axis("off")
    plt.tight_layout()

    fig_s = plt.figure()
    plt.imshow(gradient.reshape(18, 14), cmap="Greys")
    plt.colorbar()
    plt.axis("off")
    plt.tight_layout()

    return fig_i, fig_s


model = load_keras_model("cicada-project/cicada-v1.1")

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            input_ = gr.Textbox(
                label="Calo Deposits",
                lines=18,
                placeholder="\n".join([",".join(["0"] * 14)] * 18),
            )
            with gr.Row():
                classify = gr.Button("Get Anomaly Score")
                interpret = gr.Button("Visualize")
        with gr.Column():
            label = gr.Number(label="CICADA Anomaly Score")
        with gr.Column():
            with gr.Tabs():
                with gr.TabItem("Display Calorimeter Input"):
                    input_plot = gr.Plot()
                with gr.TabItem("Display Saliency Map"):
                    interpretation_plot = gr.Plot()

    classify.click(inference, input_, label)
    interpret.click(saliency, input_, [input_plot, interpretation_plot])

demo.launch()
