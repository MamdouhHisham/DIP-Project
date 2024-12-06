import tkinter as tk
from tkinter import messagebox

def create_parameter_dialog(parent, title, operation):
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.geometry("300x150")
    dialog.resizable(False, False)
    dialog.grab_set()

    result = tk.StringVar()

    if operation == "Rotate":
        label = tk.Label(dialog, text="Enter Rotation Angle:\n(-360 to 360)")
    elif operation == "Resize":
        label = tk.Label(dialog, text="Enter Resize Factor:\n(0.1 to 10.0)")
    label.pack(pady=(20, 10))

    entry = tk.Entry(dialog, textvariable=result, justify='center')
    entry.pack(pady=10)

    if operation == "Rotate":
        result.set("45")
    elif operation == "Resize":
        result.set("0.5")

    def validate_and_close():
        try:
            value = float(result.get())
            
            if operation == "Rotate":
                if -360 <= value <= 360:
                    dialog.result = value
                    dialog.destroy()
                else:
                    messagebox.showerror("Invalid Input", "Rotation angle must be between -360 and 360 degrees")
            elif operation == "Resize":
                if 0.1 <= value <= 10.0:
                    dialog.result = value
                    dialog.destroy()
                else:
                    messagebox.showerror("Invalid Input", "Resize factor must be between 0.1 and 10.0")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number")

    button_frame = tk.Frame(dialog)
    button_frame.pack(pady=10)

    ok_button = tk.Button(button_frame, text="OK", command=validate_and_close)
    ok_button.pack(side=tk.LEFT, padx=10)

    cancel_button = tk.Button(button_frame, text="Cancel", command=dialog.destroy)
    cancel_button.pack(side=tk.LEFT)

    dialog.wait_window(dialog)

    return getattr(dialog, 'result', None)