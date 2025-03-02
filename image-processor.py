import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk

def open_image():
    global original_image, img_display
    file_path = filedialog.askopenfilename()
    if file_path:
        image = cv2.imread(file_path)
        original_image = image
        img_display = image.copy()
        update_image()

def save_image():
    if img_display is None:
        return
    save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"),
                                                        ("JPEG files", "*.jpg"),
                                                        ("All Files", "*.*")])
    if save_path:
        cv2.imwrite(save_path, img_display)
        print(f"Image saved at {save_path}")

def apply_filter(image, blur_value, edge_thresh1, edge_thresh2):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(image, (blur_value, blur_value), 0) if blur_value > 0 else image
    edges = cv2.Canny(image, edge_thresh1, edge_thresh2)
    return gray, blurred, edges

def update_image():
    global img_display
    if original_image is None:
        return
    blur_value = blur_slider.get() if blur_slider.get() % 2 == 1 else blur_slider.get() + 1
    edge_thresh1 = edge1_slider.get()
    edge_thresh2 = edge2_slider.get()
    
    gray, blurred, edges = apply_filter(original_image, blur_value, edge_thresh1, edge_thresh2)
    
    if filter_var.get() == "Grayscale":
        img_display = gray
        img = Image.fromarray(img_display)
    elif filter_var.get() == "Blur":
        img_display = blurred
        img = Image.fromarray(cv2.cvtColor(img_display, cv2.COLOR_BGR2RGB))
    elif filter_var.get() == "Edges":
        img_display = edges
        img = Image.fromarray(img_display)
    else:
        img_display = original_image.copy()
        img = Image.fromarray(cv2.cvtColor(img_display, cv2.COLOR_BGR2RGB))
    
    img = ImageTk.PhotoImage(img)
    img_label.config(image=img)
    img_label.image = img

def main():
    global original_image, img_display, img_label, blur_slider, edge1_slider, edge2_slider, filter_var
    
    root = tk.Tk()
    root.title("Image Processing")
    
    original_image = None
    img_display = None
    
    img_label = tk.Label(root, text="Open an image to start.", width=50, height=20, bg="gray")
    img_label.pack()
    
    control_frame = tk.Frame(root)
    control_frame.pack()
    
    open_button = tk.Button(control_frame, text="Open Image", command=open_image)
    open_button.pack()
    
    filter_var = tk.StringVar(value="Grayscale")
    filters = ["Grayscale", "Blur", "Edges"]
    ttk.Combobox(control_frame, textvariable=filter_var, values=filters, state="readonly").pack()
    
    blur_slider = tk.Scale(control_frame, from_=1, to=25, orient="horizontal", label="Blur Strength")
    blur_slider.pack()
    
    edge1_slider = tk.Scale(control_frame, from_=0, to=255, orient="horizontal", label="Edge Threshold 1")
    edge1_slider.pack()
    
    edge2_slider = tk.Scale(control_frame, from_=0, to=255, orient="horizontal", label="Edge Threshold 2")
    edge2_slider.pack()
    
    apply_button = tk.Button(control_frame, text="Apply Filter", command=update_image)
    apply_button.pack()
    
    save_button = tk.Button(control_frame, text="Save Image", command=save_image)
    save_button.pack()
    
    root.mainloop()

if __name__ == "__main__":
    main()
