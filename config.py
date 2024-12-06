IMAGE_FILETYPES = [
    ("Image files", "*.jpg *.jpeg *.png"),
    ("All files", "*.*")
]

FILTER_CATEGORIES = {
    "Spatial Domain Methods": {
        "Linear Methods": ["Grayscale", "RGB", "HSV", "Resize", "Rotate", "Weighted Filter"],
        "Nonlinear Methods": ["Binary", "Histogram Equalization"]
    },
    "Smoothing Spatial Filters": ["Average Filter", "Gaussian Filter", "Median Filter", "Minimum Filter", "Maximum Filter"],
    "Sharpening Spatial Filters": ["Laplacian Filter", "LOG Filter", "Sharpening Filter"]
}

PARAMETER_FILTERS = ["Rotate", "Resize"]