# 🔬 3D/4D Cell Segmentation Pipeline

An automated computer vision pipeline for segmenting cell structures from 2D images and 3D/4D microscopy volume datasets (Zarr stores). Built with **Python**, **OpenCV**, **Zarr**, and **Docker**.

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)

---

## 🌟 Key Features

* **Multi-Format Support**: Processes standard 2D images (`.png`, `.jpg`, `.tif`) as well as multi-dimensional 3D/4D biological `.zarr` stores.
* **Flexible Volume Slicing**: Specify specific timepoints (`--t`) and Z-depth slices (`--z`), or batch process entire 3D volume stacks automatically.
* **OpenCV Watershed Pipeline**: Combines Gaussian blurring, Otsu's automatic thresholding, morphological noise filtering, and marker-controlled Watershed segmentation.
* **Fully Containerized**: Packaged as a lightweight Docker container for 1-command execution on any operating system without manual dependency setups.

---

## 📁 Project Structure

```text
cell-segmentation/
├── src/
│   ├── segment.py        # Core image processing & Watershed algorithm
│   └── main.py           # CLI entrypoint and Zarr/Image data loader
├── Dockerfile            # Production Docker image configuration
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## 🛠️ Image Processing Pipeline

The segmentation algorithm follows a 4-stage computer vision workflow:

1. **Preprocessing & Noise Reduction**: Gaussian blur (`5x5` kernel) to smooth high-frequency noise.
2. **Binarization**: Otsu's automatic thresholding to isolate cell candidate regions from background.
3. **Morphological Filtering**: Sequential closing and opening operations to remove noise artifacts and fill internal cell gaps.
4. **Watershed Segmentation**: Distance transform and connected components labelling to resolve overlapping touching cells with boundary demarcation.

---

## 🐳 Quickstart with Docker (Recommended)

No local Python environment or dependencies required!

### 1. Build the Docker Image
```bash
docker build -t cell-segmenter .
```

### 2. Run Segmentation

#### A. Process a Single 2D Image
```bash
docker run --rm \
  -v "$(pwd)/sample_data:/app/data" \
  cell-segmenter \
  --input /app/data/cell.png \
  --output /app/data/result.png
```

#### B. Process a Specific Slice from a 3D/4D Zarr Volume
```bash
docker run --rm \
  -v "$(pwd)/sample_data:/app/data" \
  cell-segmenter \
  --input /app/data/sample.zarr \
  --output /app/data/result.png \
  --t 0 --z 60
```

#### C. Batch Process All Slices in a Zarr Volume
```bash
docker run --rm \
  -v "$(pwd)/sample_data:/app/data" \
  cell-segmenter \
  --input /app/data/sample.zarr \
  --output /app/data/results_folder \
  --t 0
```

---

## 💻 Local Setup (Without Docker)

### 1. Installation
```bash
git clone https://github.com/your-username/cell-segmentation.git
cd cell-segmentation
pip install -r requirements.txt
```

### 2. Usage
```bash
# Process single image
python src/main.py --input sample_data/cell.png --output sample_data/result.png

# Process Zarr volume slice
python src/main.py --input sample_data/sample.zarr --output sample_data/result.png --t 0 --z 60
```

---

## 📋 Command Line Options

| Parameter | Required | Description |
| :--- | :--- | :--- |
| `--input` | **Yes** | Path to input image file (`.png`, `.jpg`, `.tif`) OR `.zarr` directory |
| `--output` | **Yes** | Destination path for output image file OR directory |
| `--t` | Optional | Target timepoint index (integer) for Zarr datasets |
| `--z` | Optional | Target Z-slice index (integer) for Zarr datasets |

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
