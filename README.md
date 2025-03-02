# ComfyUI OOP Nodes
This project contains a set of **ComfyUI OOP Nodes** that allow users to build detailed, object-oriented prompts with customizable visual attributes for characters, environments, and scenes. These nodes are designed to provide an intuitive way to generate and control different elements such as person attributes, hairstyles, eyes, locations, and poses. The **randomize** function allows for dynamic generation, enabling users to randomize different visual elements such as eye color, hairstyle, body shape, and more, providing endless possibilities for character creation and scene design.

## Features
Available Nodes

![Demo Workflow](https://github.com/0xRavenBlack/ComfyUI-OOP/blob/main/screenshot/workflow.png?raw=true)

### OOP Hair Node 🦰
Allows customization of hair color, style, and optional secondary color.

### OOP Eyes Node 👀
Customizes eye shape and color with an option to randomize attributes.

### OOP Location Node 🌍
Generates scenes with customizable locations and objects, with randomization options.

### OOP Mouth Node 👄
Customizes mouth shape, size, and openness with randomization features.

### OOP Person Node 👤
Generates detailed person descriptions based on gender, age, body shape, ethnicity, hair, eyes, mouth, clothing, and poses.

###  OOP Pose Node 🧍
Customizes poses with configurable body, hand, and leg poses, with randomization support.

###  OOP Style Node 🎨
Combines visual styles like "Abstract", "Vintage", "Cyberpunk", "Watercolor", and more to create diverse art styles.

### OOP View Node 📐
Configures camera angles, shot types, and background blur effects for image generation.

### Requirements
Python 3.x
ComfyUI (This set of nodes is designed to be used in the ComfyUI environment)
#### Installation

    cd custom_nodes

Clone the repository:

    git clone https://github.com/0xRavenBlack/ComfyUI-OOP

Restart ComfyUI to load the new nodes.

#### Example
For example, consider the following prompt using the new OOP syntax:
```
    Style: PhotoRAW, Cyberpunk
    Perspective: shot:FullBody, angle:Dutch Angle, background:NoBlur
    Person:
    *  BodyShape: Athletic
    *  Gender: Female
    *  Age: 30-39Years
    *  Ethnicity: Latino
    *  Hair: color:OliveBeige, style:Ponytail
    *  Eyes: shape:Round, color:Hazel
    *  Mouth: shape:Full, size:Medium, opened:Slightly
    *  Clothes: Top::Garment:Sweater, color:Red, Bottom::Garment:Sweatpants, color:Gray
    *  Poses: body:Stand, hands:HandToMouth, legs:LegLift
    Animal: type:Wolf, color: Purple, action:Playing
    Location: location:Beach, object:Toy
    Environment: time:Night, mood:FullMoon
```
![](https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/224701fb-4c3f-47d2-a90b-6d3ac8cd58cf/width=525/224701fb-4c3f-47d2-a90b-6d3ac8cd58cf.jpeg)Link to Image: [https://civitai.com/images/61040035](https://civitai.com/images/61040035)

#### License
This project is licensed under the MIT License - see the LICENSE file for details.

#### Contributing
If you wish to contribute to this project, feel free to fork the repository and submit a pull request with your improvements!
