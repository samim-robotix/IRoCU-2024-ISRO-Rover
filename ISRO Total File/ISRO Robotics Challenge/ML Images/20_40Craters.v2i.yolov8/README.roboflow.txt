
20_40Craters - v2 2024-04-15 10:08am
==============================

This dataset was exported via roboflow.com on April 15, 2024 at 4:39 AM GMT

Roboflow is an end-to-end computer vision platform that helps you
* collaborate with your team on computer vision projects
* collect & organize images
* understand and search unstructured image data
* annotate, and create datasets
* export, train, and deploy computer vision models
* use active learning to improve your dataset over time

For state of the art Computer Vision training notebooks you can use with this dataset,
visit https://github.com/roboflow/notebooks

To find over 100k other datasets and pre-trained models, visit https://universe.roboflow.com

The dataset includes 1259 images.
Craters are annotated in YOLOv8 format.

The following pre-processing was applied to each image:
* Auto-orientation of pixel data (with EXIF-orientation stripping)
* Resize to 640x640 (Stretch)

The following augmentation was applied to create 3 versions of each source image:
* 50% probability of horizontal flip
* 50% probability of vertical flip
* Equal probability of one of the following 90-degree rotations: none, clockwise, counter-clockwise, upside-down
* Random rotation of between -45 and +45 degrees
* Random brigthness adjustment of between -15 and +15 percent
* Random exposure adjustment of between -17 and +17 percent
* Random Gaussian blur of between 0 and 2 pixels

The following transformations were applied to the bounding boxes of each image:
* Random shear of between -11° to +11° horizontally and -11° to +11° vertically


