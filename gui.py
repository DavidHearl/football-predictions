import tkinter as tk
from PIL import Image, ImageTk  # Pillow library is used for image handling

# Create the main window
root = tk.Tk()
root.title("Image in Tkinter")

# Load an image from file
image_path = "team_images/Arsenal.png"  # Replace with the actual path to your image file
original_image = Image.open(image_path)

# Resize the image to 64x64 pixels
resized_image = original_image.resize((64, 64))

# Convert the Image object to a PhotoImage object
tk_image = ImageTk.PhotoImage(original_image)

# Create a label and set the image
image_label = tk.Label(root, image=tk_image, width=64, height=64)
image_label.pack(padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()
