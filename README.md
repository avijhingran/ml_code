# ml_code
Machine Learning

### To execute any .py file, copy and paste the below commands all together in Google Colab Notebook and run:

```python
# Install scikit-learn (ML library)
!pip install scikit-learn

# Remove the old ml_code folder (ignore errors if it says not found)
!rm -rf ml_code

# Clone your repo into Colab
!git clone https://avijhingran:mytoken@github.com/avijhingran/ml_code.git

# Move into your repo folder
%cd ml_code/my_agent

# Run Main Python Script
!python main.py

# Visualize Output plot
from display_utils import show_plot
show_plot('comparison_plot.png')
```
