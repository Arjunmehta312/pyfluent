"""
Script to copy generated ablation images to documentation static folder.

This script will:
1. Run the modeling_ablation.py example to generate all plot images
2. Copy the generated images to the documentation static directory
"""

import os
import shutil
import subprocess
from pathlib import Path

# Directory paths
base_dir = Path(os.getcwd())
doc_static_dir = base_dir / "doc" / "source" / "_static"
examples_dir = base_dir / "examples" / "00-fluent"

# List of image files to be copied
image_files = [
    "ablation-residual.png",
    "ablation-drag_force_x.png",
    "ablation-avg_pressure.png",
    "ablation-recede_point.png",
    "ablation-pressure.png",
    "ablation-mach-number.png",
    "ablation-mach-number-thumbnail.png"
]

def ensure_dir_exists(dir_path):
    """Ensure the directory exists, create if it doesn't."""
    if not dir_path.exists():
        print(f"Creating directory: {dir_path}")
        dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path.exists()

def run_ablation_example():
    """Run the ablation example to generate the images."""
    print("Running the ablation example to generate images...")
    ablation_script = examples_dir / "modeling_ablation.py"
    
    try:
        # Run the example script to generate the images
        subprocess.run(["python", str(ablation_script)], check=True)
        print("Successfully ran ablation example.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running ablation example: {e}")
        return False

def copy_images():
    """Copy the generated images to the documentation static folder."""
    # Ensure the target directory exists
    if not ensure_dir_exists(doc_static_dir):
        print(f"Failed to create/access directory: {doc_static_dir}")
        return False
    
    success = True
    copied_files = []
    missing_files = []
    
    # Copy each image file
    for image in image_files:
        source_path = Path(image)
        target_path = doc_static_dir / image
        
        if source_path.exists():
            try:
                shutil.copy2(source_path, target_path)
                copied_files.append(image)
                print(f"Copied: {image} to {target_path}")
            except Exception as e:
                print(f"Error copying {image}: {e}")
                success = False
        else:
            print(f"Warning: Source file not found: {source_path}")
            missing_files.append(image)
            success = False
    
    # Print summary
    if copied_files:
        print(f"\nSuccessfully copied {len(copied_files)} images:")
        for file in copied_files:
            print(f"  - {file}")
    
    if missing_files:
        print(f"\nMissing files ({len(missing_files)}):")
        for file in missing_files:
            print(f"  - {file}")
    
    return success

def main():
    """Main function to run the example and copy images."""
    print("=" * 60)
    print("Ablation Example Image Copier")
    print("=" * 60)
    
    # Run the ablation example
    if run_ablation_example():
        # Copy the generated images
        if copy_images():
            print("\nSuccess: All images have been generated and copied to the documentation static folder.")
        else:
            print("\nWarning: Some images may be missing or could not be copied.")
    else:
        print("\nError: Failed to run the ablation example. Cannot proceed with copying images.")
    
    print("\nProcess completed.")

if __name__ == "__main__":
    main()
