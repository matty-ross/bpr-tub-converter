# Burnout Paradise: The Ultimate Box to Burnout Paradise Remastered conveter

![](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=FFDD54)

A tool to convert bnd2 PC files from Burnout Paradise: The Ultimate Box to Burnout Paradise Remastered.


## Usage
```
python .\src\main.py
```
You will be prompted to choose bundles which you want to convert.
Then you can choose additional bundles which contain external resources.
These resources will be added to the main bundles.
Finally, the resource IDs will be randomized to avoid ID collisions.

## Supported resource types
- Texture (0)
- Vertex Descriptor (10)
- Renderable (12)
- Texture State (14)
- Material State (15)
