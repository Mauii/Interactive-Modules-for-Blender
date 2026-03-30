Interactive Modules for Blender (Blender 5.x Add-on)
An interactive, task-based training add-on for Blender. It transforms the 3D viewport into a real-time learning environment, specifically designed to teach Blender fundamentals and advanced Frankenstein Modding (kitbashing) for the Jedi Knight Academy (JKA) community.

**Overview**:
Forget long video tutorials. This add-on provides a HUD-driven experience where you learn by doing. The system detects your keystrokes, tool selections, and object manipulations in real-time, guiding you through a comprehensive curriculum directly inside the 3D Viewport.
Key Features
Real-time Task Tracking: A dynamic HUD overlays the viewport, showing current goals and progress.
Interactive Logic: Lessons sense hotkeys, tool changes (like the Ruler or Selection boxes), and 3D transformations.
Modular Architecture: Simply drop a new lesson_*.py file into the folder to expand the curriculum.
Dynamic UI: The interface automatically scales and adjusts based on lesson text and task complexity.
Blender 5.1 Ready: Fully updated to support the latest API changes in Blender 5.x.

**Installation**
Download this repository as a .zip file.
Open Blender.
Go to Edit > Preferences > Add-ons.
Click Install... and select the downloaded .zip.
Search for JKA Frankenstein Tutor and enable it by checking the box.

**How to Use**:
Open the Sidebar in the 3D Viewport (Press N).
Select the JKA tab.
Choose a module from the Training Modules dropdown.
Click Start Selected Lesson.
Follow the HUD instructions. Press ESC at any time to cancel a lesson.

**Curriculum (Chapter 1: Fundamentals)**:
The first chapter covers everything needed to master Object Mode before moving to advanced mesh editing.
1.0 Camera Basics: Master Orbit, Pan, and Zoom.
1.1 Standard Views: Numpad navigation and orthographic views.
1.2 Object Selection: Viewport and Outliner selection techniques.
1.3 Focus & Isolation: Framing objects and using Local View.
1.4 Basic Transformations: The "Big Three": Grab, Rotate, and Scale.
1.5 Snapping Basics: Using the Magnet tool and Vertex snapping.
1.6 Join & Separate: Managing mesh hierarchy and merging objects.
1.7 The 3D Cursor: Precise snapping and using the cursor as a pivot.
1.8 Duplicate & Instance: Difference between Shift+D and Alt+D.
1.9 Adding & Organizing: Creating primitives and using Collections.
1.10 Origin Points: Managing object pivots for proper rotation.
1.11 Hiding & Unhiding: Managing viewport clutter with H and Alt+H.
1.12 Hierarchy & Parenting: Creating logical links between objects.
1.13 Selection Tools: Mastering Box, Circle, and Lasso select.
1.14 Applying Transforms: Keeping mesh data "clean" with Ctrl+A.
1.15 Viewport Shading: Switching between Wireframe, Solid, and X-Ray.
1.16 Global vs Local: Understanding coordinate systems for tilted parts.
1.17 Undo & History: Managing mistakes and the undo stack.
1.18 Visual Aids: Using the Measure tool and Annotations.

**Project Structure**:
__init__.py: Core manager. Handles natural sorting of lessons, UI, and registration.
gui.py: Graphics engine. Handles dynamic GPU drawing and HUD rendering.
lesson_*.py: Individual modular lesson files.

**Copyright & License**:
Copyright © 2024 Maui
This project is licensed under the MIT License.
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

**Contributing**:
Contributions are welcome! Fork the repo and submit a Pull Request if you have ideas for new lessons (Chapter 2 & 3) or HUD improvements.
Created for the JKA Modding Community.
