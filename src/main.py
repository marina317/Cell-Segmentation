import argparse
import sys
from pathlib import Path
import cv2 as cv
import zarr
from segment import run_pipeline

def parse():
  parser = argparse.ArgumentParser()
  parser.add_argument("--input", required = True, help = "path of input image or zarr folder")
  parser.add_argument("--output", required = True, help = "output path")
  parser.add_argument("--t", required = False, type = int, help = "specify timepoint")
  parser.add_argument("--z", required = False, type = int, help = "specify slice")
  args = parser.parse_args()
  return args

  

if __name__ == "__main__":
  args = parse()
  input_path = Path(args.input)
  if input_path.is_file() and input_path.suffix in [".png", ".jpg", ".tif"]:
    
    output = run_pipeline(input_path)

  elif input_path.is_dir() and input_path.suffix == ".zarr":
    if args.t is None:
      # loop over all timepoint
    else:
      data = zarr.open(input_path, mode = "r")
      volume = data["0"]
      if args.z is None:
        # loop over all slices
      else:
        img = volume[args.t, args.z]
        result = run_pipeline(img)
        
  
