from IPython.display import Image, display

def show_plot(image_path='comparison_plot.png'):
    """Display a saved plot image."""
    display(Image(filename=image_path))
