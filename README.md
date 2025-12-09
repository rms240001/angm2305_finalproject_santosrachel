# Pixel Art Grid Editor

Commentary Demonstration Video: (https://youtu.be/WwsAnfaxZnI)

GitHub Repository Link: (https://github.com/rms240001/angm2305_finalproject_santosrachel)

## Project Description

This is a grid editor where users can select from various canvas sizes to draw sprites for their games/art. Firstly, you can select from various canvas sizes. Next it allows people the ability to draw on the canvas with different colors and to erase OR clear the entire canvas in case you want to start over. After you are done, you can even save the canvas you worked on as an PNG in your files.

## Project Structure

```
|   requirements.txt
|
\---src
        project.py
```

### src/project.py

This .py file contains all the logic for my project, from the main logic loop to functions that help with the different features included in my project.

draw_welcome_screen() - this is the screen the user is first presented with

draw_canvas_size_selector_screen() - this function helps present the user with 3 different canvas sizes to choose from (waits on user input to move on)

draw_grid_editor() - most critical function; holds the logic for the user being able to select various colors/tools to use on the canvas, being able to draw on the canvas, and other quality of life functionality (clearing canvas and saving the canvas as PNG file)

enter_filename() - allows the user to name the file however they want (saves to Downloads folder)

get_downloads_folder() - helps figure out where the Downloads folder is 

### requirements.txt

This is where all my 3rd party libraries are listed (pygame)

## Design Considerations

I wanted my project to flow as if it were a real application (something like the Paint application on Windows), so I decided that instead of having everything take place in 1 screen, to have different "views" for the user to interact with. For example, being able to select the canvas size, drawing on my canvas, and saving the file all live within their own views.

I wanted to provide the user with different "tools", this would give the user different options when designing sprites... I was only able to finish an "editor" and "eraser", but the idea was to also include things like a "sprayer", etc. I included different colors for users to choose so it gives them more creative freedom, rather than just using black for their drawings. 

Included quality of life features, like being able to clear the canvas so the user did not have to delete 1 pixel at a time if they wanted to start over.

## Future Areas of Improvement

- Fixing the way text is aligned on my views, sometimes they look misaligned
- Add more tools, like a "sprayer", or a "roller"
- You can only follow one main flow, as in, when you select a canvas size, you are stuck with it and can't go back unless you restart the application, like having "Back" buttons
- Allowing users to add custom colors based on a HEX code, right now the user is limited to the palette I provide them