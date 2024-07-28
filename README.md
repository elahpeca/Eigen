This is a simple yet powerful Linux command-line application designed to perform eigendecomposition of square matrices and visualize the results using heatmaps.

Features:

• Interactive Input: Provides an intuitive command-line interface for entering matrix dimensions and elements. • Eigenvalue Calculation: Accurately calculates eigenvalues and eigenvectors for real-valued square matrices. • Matrix Visualization: Generates clear heatmaps using the Seaborn library to represent:

    Matrix of Eigenvectors
    Diagonalized Matrix of Eigenvalues
    Inverse Matrix of Eigenvectors
    Reconstructed Matrix

Linux installation:

The application is currently under development, and system packages are not yet available. Virtual environments are recommended for installation.

    Create the Virtual Environment:

    python3 -m venv venv_name

    Navigate to the Virtual Environment:

    cd venv_name

    Activate the Virtual Environment

    source bin/activate

    Install poetry

    pip install poetry

    Clone the Repository:

    git clone https://github.com/elahpeca/eigendecomposer.git

    Navigate to the Project Directory:

    cd eigendecomposer

    Install the Package:

    poetry install

    Run:

    poetry run eigendecomposer

Usage:

    Launch the App.
    Enter Matrix Size: You'll be prompted to enter the size (number of rows and columns) of your square matrix. Enter an integer value greater than or equal to 1.
    Input Matrix Elements: Enter the elements of your matrix row by row, separated by spaces. The app will guide you through the input process.

The application will generate a window displaying four heatmaps representing the decomposition results.

The code will be further developed to handle complex matrices, perform more advanced analysis, and provide more customization options.

Contributions are welcome! Please open an issue or submit a pull request.

This project is licensed under the GNU General Public License v3.0.
