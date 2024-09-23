import os
import time
from tkinter import Tk, Label
from PIL import Image, ImageTk

def get_latest_image(folder='images/'):
    # Get all JPEG files in the directory
    images = [f for f in os.listdir(folder) if f.endswith('.jpg') or f.endswith('.jpeg')]
    
    if not images:
        return None

    # Find the most recent file
    latest_image = max(images, key=lambda x: os.path.getctime(os.path.join(folder, x)))
    return os.path.join(folder, latest_image)

def resize_image(image, target_width, target_height):
    # Calculate the aspect ratio
    original_width, original_height = image.size
    aspect_ratio = original_width / original_height

    # Calculate new dimensions to maintain aspect ratio
    if target_width / aspect_ratio <= target_height:
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    else:
        new_width = int(target_height * aspect_ratio)
        new_height = target_height

    return image.resize((new_width, new_height))

def update_image(label, folder='images/'):
    # Get the latest image
    image_path = get_latest_image(folder)

    if image_path:
        # Open the image and resize it to maintain aspect ratio within the window
        img = Image.open(image_path)
        img = resize_image(img, label.winfo_width(), label.winfo_height())
        img = img.rotate(180)  # Rotate the image by 180 degrees
        
        img = ImageTk.PhotoImage(img)

        # Update the label with the new image
        label.config(image=img)
        label.image = img  # keep a reference to prevent garbage collection

    # Schedule the next check
    label.after(1000, update_image, label, folder)

def start_image_update(label, folder='images/'):
    # Wait until the label is fully rendered before starting the update loop
    label.after(1000, update_image, label, folder)

def main():
    # Create the main window
    root = Tk()
    root.title("Image Viewer")
    root.configure(background="black")

    # Get the screen width and height, and set the window to full screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")
    root.attributes("-fullscreen", True)

    # Create a label to display the image
    image_label = Label(root)
    image_label.configure(background="black")
    image_label.pack(expand=True, fill='both')

    # Start the image update loop after the window is fully rendered
    root.after(1000, start_image_update, image_label)

    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()
