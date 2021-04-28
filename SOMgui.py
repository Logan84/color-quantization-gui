#!/usr/bin/env python
# Import Libraries
import PySimpleGUI as sg
import os
from PIL import Image, ImageTk
import io
import numpy as np
from minisom import MiniSom

# To use JPEGs or resize
def convert_to_bytes(file_or_bytes, resize=None):
    if isinstance(file_or_bytes, str):
        img = Image.open(file_or_bytes)
    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

def resize_recreated(image_data):
    cur_width, cur_height = image_data.size
    new_width = 400
    new_height = 300
    scale = min(new_height/cur_height, new_width/cur_width)
    img = image_data.resize((int(cur_width*scale), int(cur_height*scale)), Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

sg.theme('DarkAmber')

# Define Gui Elements
file_column = [[sg.Text("Image Folder"),
                sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
                sg.FolderBrowse()],
                [sg.Listbox(values=[], enable_events=True, size=(40, 20), key="-FILE LIST-")]
]
image_preview_column = [[sg.Text("Choose an image from list on left:")],
                        [sg.Text(size=(40, 1), key="-TOUT-")],
                        [sg.Image(key="-IMAGE-")]
]
SOM_inputs_column = [[sg.Text("Enter your desired inputs for the following paramters:")],
                    [sg.Text("Width: (This will create a NxN SOM"), sg.Input(key="-DIMENSION-")],
                    [sg.Text("Learning Rate: "), sg.Input(key="-LEARNING-")],
                    [sg.Text("Neighborhood Radius: "), sg.Input(key="-NEIGHBORHOOD-")],
                    [sg.Text("Number of Epoch: "), sg.Input(key="-EPOCH-")],
                    [sg.Submit(key="-RUN SOM-")]
]
SOM_outputs_column = [[sg.Text("The Recreated Image:")],
                    [sg.Image(key="-RECREATED-")]
]

#Define Layout
layout = [
    [sg.Column(file_column, size=(600,400)),
    sg.VSeparator(),
    sg.Column(image_preview_column, size=(600,400))],
    [sg.Column(SOM_inputs_column, size=(600,400)),
    sg.VSeparator(),
    sg.Column(SOM_outputs_column, size=(600,400))]
]

# Create the window
window = sg.Window("SOM Color Quantization", layout)

# Create an event loop
while True:

    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "OK" or event == sg.WIN_CLOSED:
        break
    if event == '-FOLDER-':
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []
        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":
        try:
            filename = os.path.join(
                values['-FOLDER-'], values['-FILE LIST-'][0]
            )
            window['-TOUT-'].update(filename)
            window['-IMAGE-'].update(data=convert_to_bytes(filename, resize=(400, 300)))
            print(window['-IMAGE-'].get_size())

        except Exception as E:
            print(f'** Error {E} **')
            pass

    elif event == "-RUN SOM-":
        try:
            dim = int(values['-DIMENSION-'])
            lr = float(values['-LEARNING-'])
            neigh = float(values['-NEIGHBORHOOD-'])
            epoch = int(values['-EPOCH-'])
            print('{}, {}, {}, {}, {}'.format(dim, lr, neigh, epoch, filename))

            data = Image.open(filename)
            #print(data.format)
            #print(data.mode)
            data = np.asarray(data)
            #print(data.shape)
            #print(data[0])
            training_data = np.reshape(data, (data.shape[0] * data.shape[1], data.shape[2])) / 255

            
            som = MiniSom(dim, dim, data.shape[2], sigma=neigh, learning_rate = lr)
            som.random_weights_init(training_data)
            print(som.get_weights())
            som.train(training_data, epoch, verbose=False)

            qnt = som.quantization(training_data)

            new_image = np.zeros(data.shape)
            
            for i, q in enumerate(qnt):
                new_image[np.unravel_index(i, (data.shape[0], data.shape[1]))] = q
            
            #print(new_image.shape)
            pilImage = Image.fromarray(np.uint8(new_image * 255)).convert('RGB')
            #print(pilImage.mode)
            window['-RECREATED-'].update(data=resize_recreated(pilImage))

        except Exception as E:
            print(f'** Error {E} **')
            sg.popup_error('Enter Valid Values or Select Image')
            pass

window.close()