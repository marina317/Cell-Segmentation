import argparse
import sys
from pathlib import Path
import cv2 as cv
import zarr
from segment import run_pipeline


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", required=True, help="path of input image or zarr folder"
    )
    parser.add_argument("--output", required=True, help="output path")
    parser.add_argument(
        "--t", required=False, type=int, help="specify timepoint"
    )
    parser.add_argument("--z", required=False, type=int, help="specify slice")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse()
    input_path = Path(args.input)
    output_path = Path(args.output)

    # 1. Single image file (.png, .jpg, .tif)
    if input_path.is_file() and input_path.suffix in [".png", ".jpg", ".tif"]:
        img = cv.imread(str(input_path))
        result = run_pipeline(img)
        
        # Ensure parent directory exists and write file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        cv.imwrite(str(output_path), result)
        print(f"Saved: {output_path}")

    # 2. Zarr dataset folder
    elif input_path.is_dir() and input_path.suffix == ".zarr":
        data = zarr.open(str(input_path), mode="r")
        volume = data["0"]

        # Determine timepoints to process
        if args.t is None:
            timepoints = range(volume.shape[0])
        else:
            timepoints = [args.t]

        # Determine slices to process
        if args.z is None:
            slices = range(volume.shape[1])
        else:
            slices = [args.z]

        # If saving multiple output images, ensure output is a directory
        is_multiple = len(timepoints) > 1 or len(slices) > 1
        if is_multiple:
            output_path.mkdir(parents=True, exist_ok=True)

        for t_idx in timepoints:
            for z_idx in slices:
                img = volume[t_idx, z_idx]
                result = run_pipeline(img)

                if is_multiple:
                    out_file = output_path / f"segment_t{t_idx}_z{z_idx}.png"
                else:
                    out_file = output_path
                    out_file.parent.mkdir(parents=True, exist_ok=True)

                cv.imwrite(str(out_file), result)
                print(f"Saved: {out_file}")
  
