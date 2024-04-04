# Meal Picker Application

## Introduction

The Meal Picker application is designed to help users discover meals that match their dietary preferences and nutritional goals. Utilizing a simple yet powerful graphical user interface (GUI) built with Tkinter, the application allows users to search for meals based on specific nutritional criteria, explore similar meal options, and receive recommendations tailored to their needs. Whether you're looking for low-carb options, high-protein meals, or anything in between, Meal Picker makes finding the right meal easy and fun.

## Getting Started

### Prerequisites

Before running the Meal Picker application, ensure you have Python installed on your system. The application has been tested with Python 3.8 and newer versions. Additionally, you will need to install the following Python packages:

- `tkinter` for the GUI
- `pandas` for data handling
- `python-ta` for code checking and debugging purposes (optional)

You can install the required packages using pip:

```bash
pip install pandas python-ta
```

Note: Tkinter is included with most Python installations. If you encounter any issues with Tkinter, please refer to the [official Tkinter documentation](https://docs.python.org/3/library/tkinter.html) for installation instructions.

### Installation

1. Clone the repository or download the source code to your local machine.
2. Ensure all prerequisites are installed.
3. Locate the CSV file (`data.csv`) containing meal data. This file should be placed in the same directory as the application code or in a location accessible by the application.

## Running the Application

To run the Meal Picker application, navigate to the directory containing the source code and execute the following command:

```bash
python main.py
```

This command will launch the application's main window, where you can start exploring meal options.

## Features and Usage

The Meal Picker application is comprised of several key components, each contributing to the overall functionality of finding and recommending meals:

1. **Welcome Page:** Introduces the application and provides instructions on getting started.
2. **Meal Picker:** Allows users to search for meals by name or nutritional criteria. Users can adjust sliders to specify the range of nutrients they're interested in (e.g., calories, protein, carbs).
3. **Side Panel:** Contains sliders for adjusting nutritional preferences, enabling users to refine their meal search based on specific nutritional goals.
4. **Recommendations:** Based on the selected meal and nutritional preferences, the application suggests similar meals that meet the user's criteria.

## Searching for Meals
1. Use the sliders on the left panel to set nutritional preferences.
2. Click the "Search" button to display meals that match your criteria.
3. Select a meal from the list to view more details or to explore similar meal options.

## Getting Recommendations
1. After selecting a meal, adjust the sliders on the right panel to set the importance of each nutritional category for recommendations.
2. Click the "Find closest meal" button to receive a list of recommended meals based on your preferences.
3. Explore the recommended meals and discover new options that fit your dietary needs.

## Resetting Sliders

To reset all sliders to their default values, click the "Reset Sliders" button located at the bottom of the side panel. This allows you to start a new search with fresh criteria.

## Have a happy time using AltMeal!
Thank you for taking the time to read the README.md, and our team truly hopes that you find this app useful. Contributions to the Meal Picker application are also very welcome! Whether you're interested in adding new features, improving the UI, or refining the meal recommendation algorithm, we value your input. Please feel free to submit issues and pull requests. Happy finding AltMeals :)