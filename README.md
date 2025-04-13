<span style="font-family:'consolas';">

# Anti-Gravity
Anti-Gravity is an open-source puzzle game (inspired from *Tomb of the Mask*) built with the PyGame python library for a Computer Science ATAR PyGame Project. 

It comprises 2000 lines of code spread across 30 different python files and over 100 self-made pixelart textures.

This project was made with the goal of improving my programming skills and has therefore 0% AI usage.

Game progression: [Documentation (Google Docs)](https://docs.google.com/document/d/1YgxO29jv7kmoHWKECIMXgPgSoPKQm0y9mQzlj-sPr10/edit?usp=sharing)

> **NOTE**: To see all commit history view the main-history branch.

## Installing Dependencies
> Required libraries: pygame

Install all the required python libraries.\
For example by using PIP (windows)
```
C:\Users\user> pip install library
```

## Installing anti-gravity

### Using git (Windows)
```
C:\Users\user> cd ./*folder you want to download into*
C:\Users\user\*folder*> git clone https://github.com/enenflash/anti-gravity anti-gravity
```

### Manually
Alternatively you can use https://download-directory.github.io/ to download the entire repository.

## Running the game

### Run using run.bat
Double click run.bat in File Explorer

### Using CMD (Windows)
```
C:\Users\user> cd ./*game folder*
C:\Users\user> python main.py
```

### Run using VSCode
Open the folder in VSCode and run main.py

# Modifying the game
You can edit and create levels, textures and even menus.

## Levels
Run level_designer.py to design your own levels.

It will require a path to a json file which represents a map in anti-gravity.

To edit a level enter an already existing map path such as 
```
Map Path: data/maps/level0.json
```

To create a new level, create a json file and copy and paste these lines
```
{
    "map": [

    ]
}
```
Then enter the path of that map when you run level_designer.py

* Use WASD to move around the map (if you created a new map, it will be empty).
* Use the arrow keys to change the tile and r to rotate the tile
* Press enter to place a tile, c to clear the tile, and v to stack another tile on top of the tile already in that position

> PRESS M TO SAVE THE MAP. IT WILL NOT AUTOMATICALLY SAVE.

Note that you will need to specify the player-start position of the map if not the game will crash.
```
{
    "map": [
        *map data here*
    ],
    "player-start": [*start_x*, *start_y*]
}
```

By placing the electricity nodes such that they face each other, the game will automatically spawn in the eletricity upon loading the map (which it will also do for all tiles that have the 'spawner' property) However, movables, portals and other non-static tiles have to be added manually.
```
{
    "maps": [
        *map data here*
    ],
    "player-start": [*start_x* *start_y*]
    "movables": [
        { "id": "3.0.00", "pos": [7, 3] }
    ]
    "portals": [
        { "id": "4.0.00", "pos": [1, 5], "link": [7, 9] },
        { "id": "4.0.00", "pos": [7, 9], "link": [1, 5] }
    ]
}
```
In this example, a green movable was added with an initial position of [7, 3] and two portals that link to each other were added.

Note that portals of the same colour are not automatically linked. The position which the player teleports to has to be specified with the "link" attribute.

## Textures
You can replace the current textures of the game by replacing them with an image of the same name.

You can also add additional images with different names but you will have to specify the image path in the json files.

For example, to add a new tile, copy and paste the image into resources/tiles/ and open data/textures/tile_textures.json

Add a new tile by giving it a unique ID. For example:

```
"3.0.05": {
    "name": "new_block",
    "texture": "resources/tiles/new_block.png",
    "type": "image"
},
```

The name attribute isn't used, it's just for convenience.
The type attribute specifies if the texture is a static image or an animation. Look at some of the sprite sheets in the json file for reference.


</span>