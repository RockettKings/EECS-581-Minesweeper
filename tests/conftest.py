"""
Prologue Comment
File: conftest.py
Description: Shared pytest setup for frontend tests. Forces pygame to use
             headless dummy drivers so tests can create a display without
             opening a real window.
Inputs: None
Outputs: Environment configuration applied before test collection
External sources: None
Author: Jon Kazmaier
Created: [Sept 19 2026]
"""

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
