# Project 5

## Table of Content
- [Description](#description)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [How it works](#how-it-works)


## Description
This application provides ability to combine multiple mind maps into single mind map, and also
provides convenient way to see all available mind maps. The information about mind maps are stored in
`meta` folder as JSON files. It's presented as the tree with nodes in format `{name, leaves}`. The list of
all available mind maps for combination are stored in `config.json`. When user exports the combined mind map,
it's also stored as `tmp/mind_map.png`.

## Dependencies
There are following dependencies in the project:
- `tkinter` - used for GUI and interaction with user
- `pydot` - used for representing the graphs and exporting as images
- `pillow` - used for working with images
- `pdf2image` - used for transforming PDF files into images
- `json` - built-in package for interacting with JSON files
- `functools` - built-in package for functional programming tools
- `os` - built-in package. Used for working with files and directories.

## Usage
To launch the program, use should first install all dependencies, and then launch `main.py`:
`$ venv/bin/python3 main.py`

## How it works
When user chooses to show combined mind map, the application loads all available mind maps from
`config.json` file, combines the similar paths, constructs _dot_ graph, exports it as *png* image,
and then displays the exported image. The image is saved as `tmp/mind_map.png`.

