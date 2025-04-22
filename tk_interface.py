import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image,ImageTk
import numpy as np


# Tk window
original_img = None
transformed_img = None
# custom methods for loading images

def load_image():
    global original_img, transformed_img
    file_path = filedialog.askopenfilename()
    if file_path:
        original_img = cv2.imread(file_path)
        original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
        image=cv2.resize(original_img,(550,350),interpolation=cv2.INTER_AREA)
        original_img = image
        transformed_img=image.copy()
        display_images()


def display_images():
    global transformed_img
    max_width, max_height = 850, 700  # You can adjust this to your screen size
    image=cv2.copyMakeBorder(transformed_img,borderType=cv2.BORDER_CONSTANT,top=200, bottom=200, left=200, right=200, value=(225,3,221))
    h, w = transformed_img.shape[:2]    
    # Scale down if too big
    if w > max_width or h > max_height:
        scale_w = max_width / w
        scale_h = max_height / h
        scale = min(scale_w, scale_h)
        new_w = int(w * scale)
        new_h = int(h * scale)
    else:
        new_w, new_h = w, h

    resized_image = cv2.resize(transformed_img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    display_image = Image.fromarray(resized_image)
    img2 = ImageTk.PhotoImage(display_image)
    transformed_label.config(image=img2)
    transformed_label.image = img2


def reset_image():
    global transformed_img,original_img
    transformed_img=original_img 
    display_images()

def grayscale():
    global transformed_img
    transformed_img=cv2.cvtColor(transformed_img,cv2.COLOR_RGB2GRAY)
    display_images()
    
def rotate_image():
    global original_img, transformed_img
    angle = float(rotation_angle.get())
    image = original_img
    h, w = image.shape[:2]
    center = (w / 2, h / 2)

    # Get rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # Compute new bounding dimensions
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # Adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - center[0]
    M[1, 2] += (nH / 2) - center[1]

    # Perform the rotation
    transformed_img = cv2.warpAffine(image, M, (nW, nH))
    display_images()


def h_shear_image():
    global transformed_img
    shear = float(h_shear_factor.get())
    rows, cols = transformed_img.shape[:2]
    M = np.float32([[1, shear, 0], [0, 1, 0]])
    transformed_img = cv2.warpAffine(transformed_img, M, (int(cols + shear*rows), rows))
    display_images()

def v_shear_image():
    global transformed_img
    shear = float(v_shear_factor.get())
    rows, cols = transformed_img.shape[:2]
    M = np.float32([[1, 0, 0], [shear, 1, 0]])
    transformed_img = cv2.warpAffine(transformed_img, M, (int(rows + shear*cols), cols))
    display_images()

def translate_image():
    global original_img,transformed_img
    image=original_img
    h,w=image.shape[:2]
    x=float(translate_x.get())
    y=float(translate_y.get())
    t_matrix=np.float32([[1,0,x],[0,1,y]])
    transformed_img=cv2.warpAffine(image,t_matrix,(w,h))
    display_images()

def scale_image():
    global original_img,transformed_img
    scale=float(scale_factor.get())
    height, width = original_img.shape[:2]
    new_width = int(width * scale)
    new_height = int(height * scale)
    transformed_img = cv2.resize(original_img, (new_width, new_height))
    display_images()

def reflect_x_func():
    global transformed_img
    h = transformed_img.shape[0]
    M = np.float32([[1, 0, 0], [0, -1, h]])
    transformed_img = cv2.warpAffine(transformed_img, M, (transformed_img.shape[1], h))
    display_images()


def reflect_y_func():
    global transformed_img
    w = transformed_img.shape[1]
    M = np.float32([[-1, 0, w], [0, 1, 0]])
    transformed_img = cv2.warpAffine(transformed_img, M, (w, transformed_img.shape[0]))
    display_images()


root = tk.Tk()
root.title("IMAGE TRANSFORMATION APP") 
root.configure(bg="#1e1e1e",padx=10,pady=10)
root.geometry("1400x700")
control_panel = tk.Frame(root, bg="#252526", padx=25 ,pady=25)
control_panel.pack(side=tk.LEFT, fill=tk.Y)


display_panel = tk.Frame(root, bg="#2e2e2e",padx=3)
display_panel.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
image_frame = tk.Frame(display_panel, bg="gray",width=700,height=600,padx=30,pady=30,border=3)
image_frame.pack()
transformed_label = tk.Label(image_frame, bg="#2e2e2e")
transformed_label.pack(side=tk.RIGHT, padx=20)


# Control Widgets
tk.Button(control_panel, text="Upload Image", command=load_image, bg="dodger blue", fg="white").pack(pady=5, fill='x')
translate_x = tk.Entry(control_panel)
translate_x.place(width=200, height=25)
translate_y = tk.Entry(control_panel)
tk.Label(control_panel, text="Translate X:", fg="white", bg="#2e2e2e").pack()
translate_x.pack()
tk.Label(control_panel, text="Translate Y:", fg="white", bg="#2e2e2e").pack()
translate_y.pack()
tk.Button(control_panel, text="Translate", command=translate_image, bg="RoyalBlue2", fg="white").pack(pady=5, fill='x')

scale_factor = tk.Entry(control_panel)
tk.Label(control_panel, text="Scale Factor:", fg="white", bg="#2e2e2e").pack()
scale_factor.pack()
tk.Button(control_panel, text="Scale",command=scale_image, bg="RoyalBlue2", fg="white").pack(pady=5, fill='x')

rotation_angle = tk.Entry(control_panel)
tk.Label(control_panel, text="Rotation Angle:", fg="white", bg="#2e2e2e").pack()
rotation_angle.pack()
tk.Button(control_panel, text="Rotate",command=rotate_image, bg="RoyalBlue2", fg="white").pack(pady=5, fill='x')
#Shearing
h_shear_factor = tk.Entry(control_panel)
tk.Label(control_panel, text="Horizontal Shear Factor:", fg="white", bg="#2e2e2e").pack()
h_shear_factor.pack()
tk.Button(control_panel, text="Shear", command=h_shear_image, bg="RoyalBlue2", fg="white").pack(pady=5, fill='x')
#vertical 
v_shear_factor = tk.Entry(control_panel)
tk.Label(control_panel, text="Vertical Shear Factor:", fg="white", bg="#2e2e2e").pack()
v_shear_factor.pack()
tk.Button(control_panel, text="Shear",command=v_shear_image,  bg="RoyalBlue2", fg="white").pack(pady=5, fill='x')

tk.Button(control_panel, text="Reflect_X",command=reflect_x_func,  bg="RoyalBlue2", fg="white").pack(pady=5, fill='x')
tk.Button(control_panel, text="Reflect_Y", command=reflect_y_func, bg="RoyalBlue2", fg="white").pack(pady=5, fill='x')

tk.Button(control_panel, text="Grayscale",command=grayscale,  bg="RoyalBlue2", fg="white").pack(pady=5, fill='x')
tk.Button(control_panel, text="Reset", command=reset_image, bg="RoyalBlue2", fg="white").pack(pady=5, fill='x')

root.mainloop()