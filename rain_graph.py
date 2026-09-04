import requests
import re
import random

# 1. Fetch a static SVG of your GitHub contributions
username = "ShivangKaushal"
url = f"https://ghchart.rshah.org/{username}"
response = requests.get(url)
svg_data = response.text

# 2. Define the CSS animation for the falling blocks
css_animation = """
<style>
  rect {
    animation: dropIn 1.5s cubic-bezier(0.25, 1, 0.5, 1) forwards;
    opacity: 0;
    transform: translateY(-100px);
  }
  @keyframes dropIn {
    0% { transform: translateY(-150px); opacity: 0; }
    50% { opacity: 1; }
    100% { transform: translateY(0); opacity: 1; }
  }
</style>
"""

# 3. Inject random animation delays so the blocks fall at different times
def inject_delay(match):
    delay = round(random.uniform(0.0, 2.5), 2)
    original_rect = match.group(0)
    # Safely insert the style attribute into the rect tag
    return original_rect.replace('<rect ', f'<rect style="animation-delay: {delay}s;" ')

# Find all SVG rectangles (the contribution blocks) and add the delay
animated_svg = re.sub(r'<rect[^>]*>', inject_delay, svg_data)

# Safely insert the CSS inside the SVG body (right before it closes)
animated_svg = animated_svg.replace('</svg>', f'{css_animation}</svg>')

# 4. Save the new animated file
with open('raining-blocks.svg', 'w') as file:
    file.write(animated_svg)
    
print("Raining blocks SVG successfully generated!")
