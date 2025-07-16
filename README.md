# Used Car Value Estimator

[Launch the App on Render](https://carapp-l2d7.onrender.com)

This Streamlit web app predicts the market value of used cars based on user input. It allows interactive exploration of the `vehicles_us` dataset through dropdown filters, histograms, and scatterplots.

The project uses:
- Streamlit for the user interface
- Plotly for interactive visualizations
- A trained regression model to estimate price based on mileage, year, and other features

---

## Getting Started Locally

To run this app on your machine, you’ll need:

### Requirements
- Python 3.11.9 (recommended via [pyenv](https://github.com/pyenv/pyenv))
- [Pipenv](https://github.com/pypa/pipenv)

### Setup Instructions

```bash
# Create a virtual environment
pipenv --python 3.11.9

# Install project dependencies
pipenv install

# Launch the app
pipenv run streamlit run app.py
