# Wildlife Detection System

A system for detecting and classifying wildlife in images using AI and computer vision.

## Features

- Detects wildlife in images and video streams
- Classifies detected animals by species
- Provides annotated output with bounding boxes and labels
- Modular and extensible codebase

## Requirements

- Python 3.8+
- OpenCV
- PyTorch
- NumPy
- Other dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/ejona/wildlife-detection-system.git
   cd wildlife-detection-system
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run detection on an image:
```
python detect.py --image path/to/image.jpg
```

To run detection on a video:
```
python detect.py --video path/to/video.mp4
```

For additional options, use:
```
python detect.py --help
```

## Model Training

To train a new model, use:
```
python train.py --data path/to/dataset
```
Refer to the documentation for dataset format and training options.

## Output

- Annotated images and videos are saved in the `output/` directory.
- Logs and model checkpoints are stored in the `logs/` and `checkpoints/` directories.

## Contributing

Contributions are welcome. Please submit pull requests or open issues for suggestions and bug reports.

## License

This project is licensed under the MIT License.
