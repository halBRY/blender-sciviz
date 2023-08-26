# ParaView to Blender Headless Example

This guide explains my process for Scientific Visualization in Blender by building and rendering an example scene. 

## Overview

The scientific visualization process begins in ParaView, exports to either PLY or VDB, then imports in Blender. In Blender, I use the GUI to fine tune the visuals of the scene, then recreate the scene in Python to render in parallel using Blender headless and the Python API. I'll go through the process step-by-step, so that I can capture the various considerations I make when transforming and exporting data. 

For this guide, I will be using [this](https://docs.alcf.anl.gov/cooley/software-and-libraries/paraview-tutorial/) dataset. 

## ParaView

Starting in ParaView, import all the data sources from the dataset. It should look something like this. 

![Screenshot of continuum and blood cells imported into ParaView.](https://github.com/halBRY/blender-sciviz/blob/main/images/paraview_1.png?raw=true)

When moving from ParaView to something like Blender, it is important to keep in mind the type of data that is being displayed. The blood cells, rbc and bad_rbc, are Polkygonal Meshes, so it is relatively straight forward to export them to a mesh format that Blender can read. Simply select the rbc and bad_rbc data sources one at a time and click on `File > Save Data`. Save them as PLYs (you could export as other file types, such as OBJ or STL, but I use PLY for the vertex colors option). The continuum, on the other hand, is an Unstructured Mesh. This means we will have to apply some sort of filter to transform the data into a format better suited for Blender. What we choose depends on what is desired for the final visualization. For this guide, I will explain two methods: polygonal surface with a color map, or an OpenVDB volume representation. 

I'll start with the continuum mesh. To save the continuum data source as a polygonal mesh, all you need to do is apply the "Extract Surface" filter in ParaView. You will then be able to `File > Save Data` to export the continuum as a PLY. This will save the mesh with vertex colors matching however it is displayed on screen. You will want to make sure that, in ParaView, you are visualizing the scalar field you want with the most appropriate color map. If you would rather edit the color map in Blender, apply a black and white color scale to the mesh in ParaView—we can create a custom color map later in Blender. 

To save the continuum as a volume in the OpenVDB format, we'll need to convert the Unstructured Grid to a Structured Grid (similar to the voxel format OpenVDB expects). To do this, apply a "Resample to Image" filter. You'll need to set the XYZ sampling dimensions. For this dataset, I have the sample dimensions set to 1024 x 512 x 512. Next, set the visualization mode in ParaView to "Volume". You should see something like the screenshot below. Once you see this, you can `File > Save Data` to export to an OpenVDB file. VDBs are tyically large, so be aware that exporting one or multiple VDBs may take several minutes. 

![Screenshot of continuum represented as a volume.](https://github.com/halBRY/blender-sciviz/blob/main/images/paraview_2.png?raw=true)

If you are using the blood flow dataset, you should now have 10 PLY files for each data source (one file per time step). 


## Blender

Now, we'll set up a simple scene in Blender. This will demonstrate how to access vertex colors, set up a custom color map, add camera animation, and apply modifiers. All of this will be done Blender's GUI. 

To begin, open Blender, delete the default cube. To import the PLY files, you can simply go to `File > Import > Standford (.ply)`. To import an OpenVDB, you can press `Shift + A`, then select `Volume > Import OpenVDB...`. 

Set up lights and camera view

Blender's default scene already has a camera and a light for you. I typically adjust mine so that the light is a Sun Light with a power of 10, and then I lock the camera to my viewport while I adjust to look at the data. 

Set up materials 
    Color attribute
    Color map
    Principled Volume

Camera animation

With the scene set up, you can [insert how to render video out of Blender here].

## GUI to Python Script 

If a dataset is too large to feasibly move to a local machine, or if you'd like to make use of distributed rendering, we will use Blender command line rendering and Blender's Python API. For this tutorial, my use case is converting my scene into a Python script that will be moved to and rendered on a remote Linux computer. 

Blender does support editing a .blend file (the file format of a saved Blender scene) with a Python script from the command line. However, I have had mixed luck with this method, as I have been unable to get the Blender keyframe number to change when it is updated by a Python script. In contrast, creating the entire scene in a Python file functions as expected. 

Unfortunately, I am not sure how to export a Blender scene as a Python script, so I've been creating them by hand. Blender does, however, have a Python terminal that allows the user to quickly query all of the information needed to fill into the script. 

## Headless commands 

## Summary

## Future Improvements 
