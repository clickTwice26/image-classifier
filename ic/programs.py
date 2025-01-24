import os
import shutil
import zipfile
from flask import send_from_directory

def getEmptyDirectorys(path: str) -> list:
    rootDirs = os.listdir(path)
    emptyDirs = []
    for i in rootDirs:
        childDir = len(os.listdir(os.path.join(path, i)))
        if childDir == 0:
            emptyDirs.append(i)
    try:
        emptyDirs.remove("classified_images")
    except Exception:
        pass
    return emptyDirs

def sortClassification(projectCode: str):
    try:
        classified_images_dir = os.path.join("static", "classified_images")
        storage_dir = os.path.join("storage", projectCode.replace(' ', '_'))
        
        os.makedirs(storage_dir, exist_ok=True)

        for image in os.listdir(classified_images_dir):
            if image.startswith(f"classified_{projectCode}"):
                source_path = os.path.join(classified_images_dir, image)
                category = image.split("_")[2]
                dest_dir = os.path.join(storage_dir, category)
                
                os.makedirs(dest_dir, exist_ok=True)

                dest_path = os.path.join(dest_dir, image)
                shutil.move(source_path, dest_path)
        
        zip_filename = f"{projectCode.replace(' ', '_')}_classified_images.zip"
        zip_filepath = os.path.join('storage', zip_filename)
        
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(storage_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, storage_dir))

        return send_from_directory(directory='storage', path=zip_filename, as_attachment=True)

    except Exception as e:
        return {"message": f"An error occurred: {str(e)}"}, 500
