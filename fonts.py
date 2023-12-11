from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

app = QApplication([])  # Create a minimal application object

# Get the list of available font families
font_families = QFontDatabase().families()

# Print the list of font families
for font_family in font_families:
    print(font_family)

# You can also print more details about each font
for font_family in font_families:
    print(f"Font Family: {font_family}")
    for style in QFontDatabase().styles(font_family):
        print(f"  Style: {style}")
        # for size in QFontDatabase().smoothSizes(font_family, style):
        #     print(f"    Size: {size}")

app.exit()  # Exit the application to prevent GUI event loop from blocking
