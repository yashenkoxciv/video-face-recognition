import os
import cv2
import argparse
import numpy as np
import face_recognition
from PIL import Image, ImageDraw

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('face_root')
parser.add_argument('video')
args = parser.parse_args()

faces = {}
for face_dir in os.listdir(args.face_root):
    current_path = os.path.join(args.face_root, face_dir)
    faces[face_dir] = []
    for face_image_file in os.listdir(current_path):
        face_image_path = os.path.join(current_path, face_image_file)
        face_image = face_recognition.load_image_file(face_image_path)
        face_encodings = face_recognition.face_encodings(face_image)
        if len(face_encodings) != 0:
            face_encoding = face_encodings[0]
            faces[face_dir].append(face_encoding)
        print(face_image_path, 'found', len(face_encodings), 'faces')

out = cv2.VideoWriter(
    '/output.avi',
    cv2.VideoWriter_fourcc(*'XVID'),
    30.0, (1280, 720)
)
video = cv2.VideoCapture(args.video)

frame_id = 0
while video.isOpened():
    print('\r', frame_id, end='', flush=True)
    dohavenext, frame = video.read()
    if not dohavenext:
        break
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    if len(face_encodings) == 0:  # didn't find faces
        cv2.imwrite('frames/{0:025d}.png'.format(frame_id), frame)
        out.write(frame)
        continue
    # lets match faces and draw bounding boxes around
    pil_image = Image.fromarray(frame)
    draw = ImageDraw.Draw(pil_image)
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        results = {}
        for face_name, known_face_encodings in faces.items():
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            results[face_name] = np.array(matches).astype(np.int).mean()
        max_accuracy = -1.0
        match_face_name = None
        for face_name, accuracy in results.items():
            if accuracy > max_accuracy:
                max_accuracy = accuracy
                match_face_name = face_name
        # now we've got matches face name (match_face_name)
        # Draw a box around the face using the Pillow module
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
        # Draw a label with a name below the face
        text_width, text_height = draw.textsize(match_face_name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), match_face_name, fill=(255, 255, 255, 255))
    #cv2.imwrite('frames/{0:025d}.png'.format(frame_id), np.array(pil_image))
    out.write(np.array(pil_image))
    #import ipdb; ipdb.set_trace()
    frame_id += 1
    del draw
    # if frame_id == 100:
    #    break
print()
video.release()
out.release()
