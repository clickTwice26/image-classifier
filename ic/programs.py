import os
def getEmptyDirectorys(path: str) -> list:
    rootDirs = os.listdir(path)
    emptyDirs = []
    for i in rootDirs:
        childDir = len(os.listdir(os.path.join(path, i)))  # Corrected path concatenation
        if childDir == 0:
            emptyDirs.append(i)
    emptyDirs.remove("classified_images")
    return emptyDirs
