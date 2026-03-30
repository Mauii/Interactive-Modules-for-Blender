Interactive Modules for Blender (Blender Addon)
A modular, interactive training addon for Blender, specifically designed to teach the fundamentals of Blender and later Frankenstein Modding (kitbashing) for the Jedi Knight Academy (JKA) community.

**Overview**
The Training addon transforms Blender into an interactive learning environment. Instead of watching videos, users complete real-time tasks within the 3D Viewport. The addon features a modular lesson system, allowing for easy expansion of the curriculum.

**Key Features:**
Real-time Task Tracking: Visual HUD overlaying the viewport with current goals.
Interactive Logic: Lessons detect user input (hotkeys) and object transformations.
Modular Architecture: Add new lessons by simply dropping lesson_*.py files into the folder. 
Dynamic UI: Automatically scales and updates based on lesson content.

**Installation**
Download this repository as a .zip file.
Open Blender.
Go to Edit > Preferences > Add-ons.
Click Install... and select the downloaded .zip.
Enable JKA Frankenstein Tutor by checking the box.

**How to Use**
Open the Sidebar in the 3D Viewport (Press N).
Look for the JKA tab.
Select a module from the Training Modules dropdown.
Click Start Selected Lesson.
Follow the instructions on the screen. Press ESC at any time to quit a lesson.

**Project Structure**
__init__.py: The core manager. Handles lesson discovery, UI panel, and operator registration.
gui.py: The graphics engine. Handles GPU drawing, font rendering, and dynamic UI scaling.
lesson_*.py: Individual training modules (e.g., Camera Basics, Snapping, 3D Cursor).

**Curriculum (Chapter 1)**
1.0 Camera Basics: Orbit, Pan, and Zoom.
1.1 Standard Views: Numpad navigation.
1.2 Object Selection: Viewport and Outliner selection.
1.3 Focus & Isolation: Framing and Local View.
1.4 Basic Transformations: Move, Rotate, and Scale.
1.5 Snapping Basics: Magnetic alignment.
1.6 Join & Separate: Mesh hierarchy management.
1.7 The 3D Cursor: Precise snapping and pivots.

**Copyright & License**
Copyright © 2024 Maui
This project is licensed under the MIT License.
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

**Contributing**
Contributions are welcome! If you have ideas for new lessons or improvements to the GUI engine, feel free to fork the repo and submit a Pull Request.
Created for the JKA Modding Community.
