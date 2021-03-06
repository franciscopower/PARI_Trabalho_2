# Augmented Reality Paint
This project is based on a powerful library called OpenCV that has tools to help with image processing. It is a mix of two different programs that together will allow the creation of an Augmented Reality Paint! Following, we will give some insight on how they work.

## Color segmenter
The color segmenter is the first requirement to do the setup of the AR Paint. Basically, we have 6 trackbars that we will use to define the max and min of the **BGR**  (blue, green and red) or **HSV** (hue, saturation and value) values in order to segmentate the pixels of the color of the object that we will use as a brush. As soon as we are set with the values, we save this data in a library called *limits* as a *.json* file and then we move on to the next program, AR Paint.

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
  -M, --mirror_image    Mirror image captured by camera
```

The default camera number is 0, as this is the most common one.

If the --augmented_reality argument is used, the program will paint on the live video, as opposed to a white canvas.

The --use_shake_prevention funtionality creates a smoother drawing and allows you to start and stop a brush stroke by hiding your "brush object".

The --mirror_image functionality mirrors the image that the camera captures, making it easier to draw in the air.

### Keyboard shortcuts

- **r** : change brush color to RED ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)
- **g** : change brush color to GREEN ![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+)
- **b** : change brush color to BLUE ![#1589F0](https://via.placeholder.com/15/1589F0/000000?text=+)
- **k** : change brush color to BLACK ![#000000](https://via.placeholder.com/15/000000/000000?text=+) or WHITE ![#FFFFFF](https://via.placeholder.com/15/FFFFFF/000000?text=+) if AR mode is used 
- **\+** : increase brush size
- **\-** : decrease brush size
- **h** : increase drawing opacity (AR Mode only)
- **l** : decrease drawing opacity (AR Mode only)
- **e** : eraser brush
- **c** : clear all drawings
- **t** : show/hide drawing tool marker
- **w**, **s** : write/save drawing to file


## Required libraries

- **OpenCV**
    + `pip install opencv-python`
- **Colorama**
    + `pip install colorama`

***
Trabalho 2 da unidade curricular de Projeto em Automação e Robótica Industrial, Mestrado Integrado em Engenharia Mecânica, Universidade de Aveiro.
Trabalho realizado por:

- Bruno Nunes, 80614
- Diogo Santos, 84861
- Francisco Power, 84706
