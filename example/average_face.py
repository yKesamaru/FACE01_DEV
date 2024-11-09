"""平均顔を作成するコード例.

Summary:
    このエグザンプルコードでは、average_face.txtにリストされたファイル名を持つ顔画像を読み込み、
    それらの画像から平均顔を作成する手順を学びます。

.. image:: ../docs/img/average_face.png
    :alt: 平均顔の画像

Example:
    .. code-block:: bash

        python3 example/average_face.py

Source code:
    `average_face.py <https://github.com/yKesamaru/FACE01_DEV/blob/master/example/average_face.py>`_
"""
import glob

# Operate directory: Common to all examples
import cv2
import mediapipe as mp
import numpy as np

# Initializing the Mediapipe face landmark detector
mp_face_mesh = mp.solutions.face_mesh  # type: ignore
face_mesh = mp_face_mesh.FaceMesh()

# images_dir = 'assets/mix'
images_dir = 'assets/data/c'


def align_face(image):
    # Detecting face landmarks
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # type: ignore

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Calculating the center of the face
            center = np.mean([[data.x, data.y] for data in face_landmarks.landmark], axis=0).astype("int")

            # Calculating the angle of the face
            dX = face_landmarks.landmark[33].x - face_landmarks.landmark[263].x
            dY = face_landmarks.landmark[33].y - face_landmarks.landmark[263].y
            angle = np.degrees(np.arctan2(dY, dX)) - 180

            # Calculating the center of the image
            (h, w) = image.shape[:2]
            (cX, cY) = (w // 2, h // 2)

            # Rotating the image to align the face frontally
            M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)  # type: ignore
            aligned = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)  # type: ignore

            return aligned


if __name__ == '__main__':
    png_list = glob.glob(f'{images_dir}/*.png')

    images = []
    for png_file in png_list:
        image = cv2.imread(png_file)  # type: ignore
        try:
            aligned = align_face(image)
            resized = cv2.resize(aligned, (224, 224))  # type: ignore
            images.append(resized)
        except:
            continue

    # Converting images to a numpy array
    images = np.array(images)

    # Calculating the average face
    average_face = np.mean(images, axis=0).astype("uint8")

    # Displaying the average face
    cv2.imshow("Average Face", average_face)  # type: ignore
    cv2.waitKey(0)  # type: ignore
