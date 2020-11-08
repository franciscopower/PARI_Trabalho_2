# Augmented Reality Paint
This project is based on a powerful library called OpenCV that has tools to help with image processing. It is a mix of two different programs that together will allow the creation of an Augmented Reality Paint! Following, we will give some inside on how they work.

## Color segmenter
The color segmenter is the first requirement to do the setup so we can work with the AR Paint. Basically, we have 6 trackbars that we will use to define the max and min of the BGR colors (blue, green and red) or also in our programar the HSV (hue, saturation and value) in order to segment the pixels of the color of the object that we will use as a marker. As soon as we are set with the values, we save this data on a library called Limits as a json file and then we move on to the next project (AR Paint)!

### How to use 

```text
optional arguments:
  -h, --help            show this help message and exit
  -hsv, --segmentate_in_hsv
                        If selected, segmentation will be in hsv
  -cn CAMERA_NUMBER, --camera_number CAMERA_NUMBER
                        Number of camera to use
```
The default camera number is 0, as this is the most common one.

***

## AR Paint

Use a colored object to paint the world around you!

This program allows you to use an object of your choice as a brush and paint on a white canvas by moving the object in the air as it is being recorded by a webcam. You may choose to use the augmented reality mode, which lets you paint on the live video of your camera, as opposed to a white canvas. Your world becomes your canvas.

**NOTE**: *To use this program, you need to create a limits.json file using the previous program, Color Segmenter.*

### How to use 

To run the code, you need to pass in the required argument --json_file. You may also pass in some additional arguments, as follows.

```text
optional arguments:
  -h, --help            show this help message and exit
  -jf JSON_FILE, --json_file JSON_FILE
                        json file with this limits defined in color
                        segmenter
  -cn CAMERA_NUMBER, --camera_number CAMERA_NUMBER
                        Number of  camera to use
  -AR, --augmented_reality
                        Definition of paint type display
  -USP, --use_shake_prevention
                        Add function - shake prevention
```

The default camera number is 0, as this is the most common one.

If the --augmented_reality argument is used, the program will paint on the live video, as opposed to a white canvas.

The --use_shake_prevention funtionality creates a smoother drawing and allows you to start and stop a brush stroke by hiding your "brush object".

### Keyboard shortcuts

- **r** : change brush color to <span style="color: green"> Some green text </span> RED
- **g** : change brush color to GREEN
- **b** : change brush color to BLUE
- **p**, **k** : change brush color to BLACkK
- **\+** : increase brush size
- **\-** : decrease brush size
- **h** : increase brush opacity
- **l** : decrease brush opacity
- **e** : eraser brush
- **c** : clear all drawings
- **w**, **s** : write/save drawing to file


## Required libraries

### OpenCV
`pip install opencv-python`
### Colorama
`pip install colorama`

***
Trabalho 2 da unidade curricular de Projeto em Automação e Robótica Industrial, Mestrado Integrado em Engenharia Mecânica, Universidade de Aveiro.
Trabalho realizado por:

- Bruno Nunes, 80614
- Diogo Santos, 84861
- Francisco Power, 84706
