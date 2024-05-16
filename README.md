# Three Body Sim

This repository contains the necessary files and configurations to build a Python application using Buildozer. The application simulates the gravitational forces between three bodies, addressing the classic Three-body problem in physics.

## Project Structure

- `buildozer.spec`: The Buildozer configuration file.
- `main.py`: The main Python script for the application.

## Getting Started

To get started with this project, follow these steps:

### Prerequisites

Make sure you have the following installed on your machine:

- Python 3.6+
- pip (Python package manager)
- Buildozer
- Android SDK (for building Android applications)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Gummygamer/threebody.git
    cd threebody
    ```

2. **Install dependencies:**

    Ensure you have all necessary dependencies by following the Buildozer documentation. For example, on Ubuntu:

    ```bash
    sudo apt update
    sudo apt install -y python3-pip build-essential git
    pip install --upgrade cython
    pip install buildozer
    ```

3. **Configure Buildozer:**

    The `buildozer.spec` file is already included in this repository. You may need to modify it to suit your specific needs. Open `buildozer.spec` and adjust the configurations if necessary.

### Usage

1. **Building the Application:**

    To build the application, navigate to the project directory and run:

    ```bash
    buildozer -v android debug
    ```

    This command will build the application for Android. You can change the target platform (e.g., `ios`) by modifying the command accordingly.

2. **Running the Application:**

    After building the application, you can run it on an emulator or a connected device. Use the following command to deploy the app:

    ```bash
    buildozer android deploy run
    ```

    Again, modify the platform as needed.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the GPL v3 License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Kivy and Buildozer teams for their awesome tools.

## Contact

For any questions or suggestions, please open an issue or contact the repository owner at [aisushin@gmail.com].
