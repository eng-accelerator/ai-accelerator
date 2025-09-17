# Getting Started with Gradio

Gradio is an open-source Python library that makes it easy to build and share beautiful, customizable web demos of your machine learning models, APIs, and data science workflows. It's perfect for quickly showcasing your work without needing to know HTML, CSS, or JavaScript.

This document will cover the essential building blocks of Gradio and provide code examples to get you started.

## Installation

First, you need to install the Gradio library. You can do this using pip for local machines:

%pip install gradio

## The Core Concept: `gradio.Interface`

The central class in Gradio is `gradio.Interface`. It takes a Python function, and automatically generates a user interface around it.

You need to specify three main things when creating an `Interface`:

1.  **`fn`**: The Python function that takes inputs and returns outputs.
2.  **`inputs`**: The Gradio component(s) that define the input type(s) for your function.
3.  **`outputs`**: The Gradio component(s) that define the output type(s) of your function.

Let's start with a simple example: a function that takes a name as input and returns a greeting.

import gradio as gr

def greet(name):
    return "Hello, " + name + "!"

# Create the interface
# inputs='text' specifies a textbox input
# outputs='text' specifies a textbox output
demo = gr.Interface(fn=greet, inputs="text", outputs="text")

# Launch the interface
# The launch() method starts a local server
# You can access the interface at the displayed URL
demo.launch()

import gradio as gr

def greet_with_age(name, age):
    return f"Hello, {name}! You are {age} years old."

# Inputs as a list: [textbox for name, number input for age]
demo = gr.Interface(fn=greet_with_age, inputs=["text", "number"], outputs="text")

demo.launch()

import gradio as gr

def analyze_text(text):
    word_count = len(text.split())
    char_count = len(text)
    return f"Word Count: {word_count}", f"Character Count: {char_count}"

# Outputs as a list: [textbox for word count, textbox for character count]
demo = gr.Interface(fn=analyze_text, inputs="text", outputs=["text", "text"])

demo.launch()

**Note:** We've commented out `demo.launch()` in the code cell above so that the notebook doesn't automatically start a Gradio app when you run the cell. When you are ready to test your Gradio app locally, uncomment that line and run the cell.

## Input and Output Components

Gradio provides a wide variety of components for both inputs and outputs. Here are some common ones:

### Text

*   **`gr.Textbox()`**: For single or multi-line text input/output.
*   **`gr.Label()`**: For displaying a classification label and confidence scores.

### Numbers

*   **`gr.Number()`**: For numerical input.
*   **`gr.Slider()`**: For numerical input within a specified range.

### Media

*   **`gr.Image()`**: For image input/output (upload, webcam, or gallery).
*   **`gr.Audio()`**: For audio input/output (microphone or file upload).
*   **`gr.Video()`**: For video input/output.

### Data Structures

*   **`gr.DataFrame()`**: For displaying tabular data.
*   **`gr.JSON()`**: For displaying JSON data.

### Other

*   **`gr.Dropdown()`**: For selecting an option from a list.
*   **`gr.Checkbox()`**: For boolean input.
*   **`gr.Radio()`**: For selecting one option from a set.
*   **`gr.File()`**: For file uploads.

You can pass instances of these components to the `inputs` and `outputs` parameters. If you have multiple inputs or outputs, pass them as a list.

Let's look at an example with multiple inputs:

Let's understand some of the Gradio components piece by piece.

### Textbox Input and Output

import gradio as gr

def echo_text(text):
    return text

demo_textbox = gr.Interface(
    fn=echo_text,
    inputs=gr.Textbox(label="Enter some text"),
    outputs=gr.Textbox(label="Echoed text"),
    title="Textbox Example"
)

demo_textbox.launch()

### Number Input and Output

import gradio as gr

def double_number(number):
    return number * 2

demo_number = gr.Interface(
    fn=double_number,
    inputs=gr.Number(label="Enter a number"),
    outputs=gr.Number(label="Doubled number"),
    title="Number Example"
)

# demo_number.launch()

### Slider Input and Number Output

import gradio as gr

def add_ten(value):
    return value + 10

demo_slider = gr.Interface(
    fn=add_ten,
    inputs=gr.Slider(minimum=0, maximum=100, label="Select a value"),
    outputs=gr.Number(label="Value + 10"),
    title="Slider Example"
)

demo_slider.launch()

### Checkbox Input and Text Output

import gradio as gr

def check_status(is_checked):
    return f"Checkbox is {'checked' if is_checked else 'unchecked'}"

demo_checkbox = gr.Interface(
    fn=check_status,
    inputs=gr.Checkbox(label="Check this box"),
    outputs=gr.Textbox(label="Status"),
    title="Checkbox Example"
)

demo_checkbox.launch()

### Dropdown Input and Text Output

import gradio as gr

def show_choice(choice):
    return f"You selected: {choice}"

demo_dropdown = gr.Interface(
    fn=show_choice,
    inputs=gr.Dropdown(["Option A", "Option B", "Option C"], label="Choose an option"),
    outputs=gr.Textbox(label="Your choice"),
    title="Dropdown Example"
)

demo_dropdown.launch()

### Image Input and Output

import gradio as gr

def process_image(image):
    # In a real application, you would process the image here
    # For this example, we just return the image
    return image

demo_image = gr.Interface(
    fn=process_image,
    inputs=gr.Image(label="Upload an image"),
    outputs=gr.Image(label="Processed image"),
    title="Image Example"
)

demo_image.launch()

And an example with multiple outputs:

## Customizing Components

Gradio components can be customized using various parameters during initialization. For example, you can set labels, default values, and appearance.

import gradio as gr

def greet_custom(name):
    return "Hello, " + name + "!"

demo = gr.Interface(
    fn=greet_custom,
    inputs=gr.Textbox(label="Enter Your Name", placeholder="Type here...", lines=2),
    outputs=gr.Textbox(label="Greeting Output"),
    title="Customized Greeting App"
)

# demo.launch()

## Sharing Your Gradio App

Gradio makes it easy to share your demos. When you use `launch()`, you get a local URL. You can also set `share=True` to create a public, shareable link that is valid for 72 hours.

import gradio as gr

def greet(name):
    return "Hello, " + name + "!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")

# To create a shareable link (valid for 72 hours)
# demo.launch(share=True)
