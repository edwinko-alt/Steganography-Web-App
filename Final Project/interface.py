from dataclasses import dataclass
from drafter import *
from decoder import *
from encoder import *

@dataclass
class State:
    image: PIL_Image
    display_message: str
    encoded_messages: list[str]

@route
def index(state: State) -> Page:
    return Page(state, ["Please select a 'png' file to get started!.", FileUpload("new_image", accept="image/png"), Button("Display", display_image)])

@route
def display_image(state : State, new_image: bytes) -> Page:

    state.image = PIL_Image.open(io.BytesIO(new_image)).convert('RGB')
    return Page(state, ["Here is your image! Would you like to encode a message, or decode one from the image?", Image(state.image), 
                        Button("Back", index), Button("Decode message", decode), Button("Encode a message", encode)])

@route
def encode(state: State) -> Page:
    return Page(state, [Image(state.image), "Please type the message you would like to encode below. ", TextBox("message", "Start typing to get started!"), 
                Button("Encode", encode_message)])

@route
def encode_message(state: State, message: str):
    state.encoded_messages.append(message)
    return Page(state, ["Would you like to save your file?", Button("Save", save_message), Button("Home Page", index)])

@route
def save_message(state: State):
    img = state.image
    width, length = None
    max_size = width * length

    state.image = encode_message(max_size, img)

@route
def decode(state: State) -> Page:
    display_image = state.image
    green = get_color_values(display_image, 1)

    return Page(state, ["Your file has the message: ", get_encoded_message(green), Button("Return to home page", index)])

hide_debug_information()
start_server(State(None, "Hello, and welcome to my steganography site! Would you like to upload an image?", []))
