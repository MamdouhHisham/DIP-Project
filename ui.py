import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2
import imutils
import image_processing
import utils
import config

original_image1 = None
original_image2 = None
processed_image = None

def upload_image(image_num, image1_label, image2_label, processed_image_label):
    global original_image1, original_image2, processed_image

    file_path = filedialog.askopenfilename(
        title=f"Select Image {image_num}",
        filetypes=config.IMAGE_FILETYPES
    )
    if file_path:
        try:
            image = cv2.imread(file_path)
            display_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(display_image)
            pil_image.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(pil_image)

            if image_num == 1:
                original_image1 = image
                image1_label.config(image=photo)
                image1_label.image = photo
            else:
                original_image2 = image
                image2_label.config(image=photo)
                image2_label.image = photo

            processed_image_label.config(image='')
            processed_image = None

        except Exception as e:
            messagebox.showerror("Error", f"Could not open image: {str(e)}")

def display_processed_image(processed_img, processed_image_label):
    if len(processed_img.shape) == 2:
        display_processed = cv2.cvtColor(cv2.cvtColor(processed_img, cv2.COLOR_GRAY2BGR), cv2.COLOR_BGR2RGB)
    else:
        display_processed = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)
    
    pil_processed = Image.fromarray(display_processed)
    pil_processed.thumbnail((300, 300))
    processed_photo = ImageTk.PhotoImage(pil_processed)

    processed_image_label.config(image=processed_photo)
    processed_image_label.image = processed_photo

def apply_single_filter(original_image1, filter_name, processed_image_label, master):
    global processed_image
    
    if original_image1 is None:
        messagebox.showwarning("Warning", "Please upload Image 1 first")
        return

    try:
        if filter_name in config.PARAMETER_FILTERS:
            param = utils.create_parameter_dialog(master, f"{filter_name} Parameters", filter_name)
            if param is not None:
                processed_image = image_processing.apply_filter_to_image(original_image1, filter_name, param)
            else:
                return
        else:
            processed_image = image_processing.apply_filter_to_image(original_image1, filter_name)
        
        display_processed_image(processed_image, processed_image_label)
        
    except Exception as e:
        messagebox.showerror("Error", f"Could not apply filter: {str(e)}")

def apply_two_image_operation(original_image1, original_image2, two_image_var, processed_image_label):
    global processed_image
    
    if original_image1 is None or original_image2 is None:
        messagebox.showwarning("Warning", "Please upload both images")
        return

    operation = two_image_var.get()
    
    try:
        img1 = cv2.resize(original_image1, (max(original_image1.shape[1], original_image2.shape[1]), max(original_image1.shape[0], original_image2.shape[0])))
        img2 = cv2.resize(original_image2, (img1.shape[1], img1.shape[0]))
        
        if operation == "Add Images":
            processed_image = cv2.add(img1, img2)
        elif operation == "Subtract Images":
            processed_image = cv2.subtract(img1, img2)
        else:
            messagebox.showwarning("Warning", "Please select an operation")
            return
        
        display_processed_image(processed_image, processed_image_label)
        
    except Exception as e:
        messagebox.showerror("Error", f"Could not perform operation: {str(e)}")

def save_processed_image(processed_img):
    if processed_img is None:
        messagebox.showwarning("Warning", "No processed image to save")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=config.IMAGE_FILETYPES
    )
    if file_path:
        try:
            cv2.imwrite(file_path, processed_img)
            messagebox.showinfo("Success", "Image saved successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save image: {str(e)}")

def main():
    root = tk.Tk()
    root.title("Image Processing Application")
    root.geometry("1200x900")
    root.configure(bg="#f0f0f0")

    main_container = ttk.Frame(root, padding="10")
    main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    upload_frame = ttk.LabelFrame(main_container, text="Image Upload")
    upload_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

    ttk.Button(upload_frame, text="Upload Image 1", command=lambda: upload_image(1, image1_label, image2_label, processed_image_label)).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(upload_frame, text="Upload Image 2", command=lambda: upload_image(2, image1_label, image2_label, processed_image_label)).grid(row=0, column=1, padx=5, pady=5)

    image_frame = ttk.Frame(main_container)
    image_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

    for i, title in enumerate(["Image 1", "Image 2", "Processed Image"]):
        ttk.Label(image_frame, text=title, font=('Arial', 10, 'bold')).grid(row=0, column=i, padx=5)
    
    image1_label, image2_label, processed_image_label = ttk.Label(image_frame), ttk.Label(image_frame), ttk.Label(image_frame)
    image1_label.grid(row=1, column=0, padx=5)
    image2_label.grid(row=1, column=1, padx=5)
    processed_image_label.grid(row=1, column=2, padx=5)

    operation_frame = ttk.LabelFrame(main_container, text="Image Operations")
    operation_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

    ttk.Label(operation_frame, text="Category:").grid(row=0, column=0, sticky=tk.W, pady=5)
    category_var = tk.StringVar(root, value="Select Category")
    category_dropdown = ttk.Combobox(operation_frame, textvariable=category_var, values=list(config.FILTER_CATEGORIES.keys()), state="readonly", width=25)
    category_dropdown.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(operation_frame, text="Method:").grid(row=1, column=0, sticky=tk.W, pady=5)
    method_var = tk.StringVar(root, value="Select Method")
    method_dropdown = ttk.Combobox(operation_frame, textvariable=method_var, state="readonly", width=25)
    method_dropdown.grid(row=1, column=1, padx=5, pady=5)

    def update_method_dropdown(event):
        selected_category = category_var.get()
        methods = []
        if selected_category in config.FILTER_CATEGORIES:
            category_content = config.FILTER_CATEGORIES[selected_category]
            methods = sum(category_content.values(), []) if isinstance(category_content, dict) else category_content
        method_dropdown['values'] = methods
        method_var.set("Select Method")

    category_dropdown.bind('<<ComboboxSelected>>', update_method_dropdown)

    ttk.Label(operation_frame, text="Two Image Operations:").grid(row=2, column=0, sticky=tk.W, pady=5)
    two_image_var = tk.StringVar(root, value="Select Operation")
    two_image_dropdown = ttk.Combobox(operation_frame, textvariable=two_image_var, values=["Add Images", "Subtract Images"], state="readonly", width=25)
    two_image_dropdown.grid(row=2, column=1, padx=5, pady=5)

    ttk.Button(operation_frame, text="Apply Single Image Filter", command=lambda: apply_single_filter(original_image1, method_var.get(), processed_image_label, root)).grid(row=3, column=1, padx=5, pady=5)
    ttk.Button(operation_frame, text="Apply Two Image Operation", command=lambda: apply_two_image_operation(original_image1, original_image2, two_image_var, processed_image_label)).grid(row=4, column=1, padx=5, pady=5)
    ttk.Button(operation_frame, text="Save Processed Image", command=lambda: save_processed_image(processed_image)).grid(row=5, column=1, padx=5, pady=5)

    root.mainloop()
