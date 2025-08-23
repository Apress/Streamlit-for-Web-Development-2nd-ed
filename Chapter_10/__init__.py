import os
import streamlit.components.v1 as components
IS_RELEASE = False
if IS_RELEASE:
   absolute_path = os.path.dirname(os.path.abspath(__file__))
   build_path = os.path.join(absolute_path, 'frontend/build')
   _component_func = components.declare_component('rating_stars', path=build_path)
else:
   _component_func = components.declare_component('rating_stars', url='http://localhost:3001')
def rating_stars(stars_count: int):
   stars_selected = _component_func(stars_count=stars_count)
   if stars_selected is None:
     stars_selected = 0
   return stars_selected
