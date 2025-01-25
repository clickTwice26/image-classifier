from flask import Flask, url_for, jsonify, request, render_template, send_file
import os
import cv2
import face_recognition
from werkzeug.utils import secure_filename
from zipfile import ZipFile
from ic.programs import *

UPLOAD_FOLDER = os.path.join('storage', "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def toolsViewer(db, request, session):
    tools = [
        {
            'name': 'Video To Individual Face',
            'image_url': '/static/assets/tools_face_extractor.png',
            'description': 'You can extract the faces from a video.',
            'link': url_for("toolFaceExtractorView")
        },
        {
            'name': 'Data Visualizer',
            'image_url': 'https://via.placeholder.com/300x200',
            'description': 'Create stunning visualizations from your data.',
            'link': '/data-visualizer'
        },
        {
            'name': 'Model Trainer',
            'image_url': 'https://via.placeholder.com/300x200',
            'description': 'Train custom AI models with ease.',
            'link': '/model-trainer'
        }
    ]
    return render_template("toolsView.html", tools=tools)

def extract_faces_from_video(video_path, interval, fileCode, OUTPUT_FOLDER):
    try:
        interval = int(interval)
        video_capture = cv2.VideoCapture(video_path)
        if not video_capture.isOpened():
            raise ValueError("Error opening video stream or file")

        total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = video_capture.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * interval)
        face_images = []
        frame_num = 0

        while frame_num < total_frames:
            ret, frame = video_capture.read()
            if not ret:
                break

            if frame_num % frame_interval == 0:
                face_locations = face_recognition.face_locations(frame)
                for i, (top, right, bottom, left) in enumerate(face_locations):
                    face_image = frame[top:bottom, left:right]
                    face_filename = f"face_{frame_num}_{i}.jpg"
                    face_filepath = os.path.join(OUTPUT_FOLDER, face_filename)
                    cv2.imwrite(face_filepath, face_image)
                    face_images.append(face_filepath)

            frame_num += 1

        video_capture.release()
        return face_images
    except Exception as e:
        return str(e)

def create_zip_from_faces(faces, fileCode):

    zip_filename = f"faces_{fileCode}.zip"
    zip_filename = os.path.join("face_extractor", zip_filename)
    with ZipFile(zip_filename, 'w') as zipf:
        for face in faces:
            if os.path.exists(face):
                zipf.write(face, os.path.basename(face))
    return zip_filename

def faceExtractorUploader(db, request, session):
    fileCode = getUniqueToken()
    OUTPUT_FOLDER = os.path.join('storage', fileCode)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    if 'video' not in request.files:
        return "No file part", 400

    video_file = request.files['video']
    if video_file.filename == '':
        return "No selected file", 400

    filename = secure_filename(video_file.filename)
    interval = request.form.get("interval", 30)
    interval = int(interval)
    if not filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        return "Unsupported file format", 400

    video_path = os.path.join(UPLOAD_FOLDER, filename)
    video_file.save(video_path)
    faces = extract_faces_from_video(video_path, interval, fileCode, OUTPUT_FOLDER)

    if not faces:
        return "No faces detected in the video", 400

    zip_file_path = create_zip_from_faces(faces, fileCode)
    shutil.rmtree(OUTPUT_FOLDER) 

    if os.path.exists(zip_file_path):
        return jsonify({'download_url': url_for('download_zip', filename=os.path.basename(zip_file_path))})
    else:
        return "Error: File not found", 404

def download_zip(filename):
    zip_file_path = os.path.join("face_extractor", filename)
    if os.path.exists(zip_file_path):
        return send_file(zip_file_path, as_attachment=True, download_name=filename)
    else:
        return "File not found", 404

def faceExtractorViewer(db, request, session):
    return render_template("tools/face_extractor.html")
