# Wildlife Detection System Setup Instructions

## Prerequisites

Before setting up the Wildlife Detection System, ensure you have the following installed on your machine:

- Python 3.10 or higher
- pip (Python package installer)
- Git (optional, for cloning the repository)

## Installation Steps

1. **Clone the Repository**

   Open your terminal and clone the repository using the following command:

   ```
   git clone https://github.com/yourusername/wildlife-detection-system.git
   ```

   Navigate into the project directory:

   ```
   cd wildlife-detection-system
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   It is recommended to create a virtual environment to manage dependencies:

   ```
   python -m venv venv
   ```

   Activate the virtual environment:

   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

3. **Install Dependencies**

   Install the required packages using pip:

   ```
   pip install -r requirements.txt
   ```

4. **Configure Settings**

   Open the `src/config/settings.py` file to configure detection parameters and feature toggles according to your preferences.

5. **Run the Application**

   To start the wildlife detection system, run the following command:

   ```
   python src/main.py
   ```

6. **Access the Dashboard**

   Open your web browser and navigate to `http://127.0.0.1:5000` to access the dashboard. You will see the real-time video feed and event logs.

## Additional Notes

- Ensure your camera is connected and accessible for real-time detection.
- You can customize detection parameters and enable/disable features in the settings file.
- For speech interaction, ensure you have the necessary audio input devices configured.

## Troubleshooting

- If you encounter any issues, check the console output for error messages.
- Ensure all dependencies are correctly installed and compatible with your operating system.

## Conclusion

You are now set up to use the Wildlife Detection System. Enjoy exploring wildlife detection with real-time capabilities!