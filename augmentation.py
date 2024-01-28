import cv2
import os
import numpy as np
from config import INPUT_DIR, OUTPUT_DIR, OUTPUT_LABEL


def apply_augmentations(image):
    images = []

    # 원본 이미지
    images.append(image)

    # 이미지 회전
    angles = [90, 180, 270, 360]
    for angle in angles:
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h))
        images.append(rotated)

    # 크기 조정
    scales = [0.5, 0.75, 1.25, 1.5]
    for scale in scales:
        resized = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        images.append(resized)

    # 밝기 조정
    alphas = [0.5, 1, 1.5]
    for alpha in alphas:
        adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=0)
        images.append(adjusted)

    # 이미지 반전
    flip_modes = [0, 1]  # 0은 수직, 1은 수평
    for mode in flip_modes:
        flipped = cv2.flip(image, mode)
        images.append(flipped)

    # 색상 조정
    for beta in [30, 60, 90]:
        adjusted = cv2.convertScaleAbs(image, alpha=1.0, beta=beta)
        images.append(adjusted)

    # 노이즈 추가
    noise = np.random.randint(0, 50, (image.shape[0], image.shape[1], 3), dtype='uint8')
    image_with_noise = cv2.add(image, noise)
    images.append(image_with_noise)

    # 이미지 이동
    translations = [20, -20]
    for tx in translations:
        M = np.float32([[1, 0, tx], [0, 1, 0]])
        shifted = cv2.warpAffine(image, M, (w, h))
        images.append(shifted)

    # 이미지 왜곡
    pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
    pts2 = np.float32([[10, 100], [200, 50], [100, 250]])
    M = cv2.getAffineTransform(pts1, pts2)
    distorted = cv2.warpAffine(image, M, (w, h))
    images.append(distorted)

    return images


def save_images(images, base_filename, output_dir):
    for i, img in enumerate(images):
        filename = f"{base_filename}_{i}.png"
        filepath = os.path.join(output_dir, filename)
        cv2.imwrite(filepath, img)

        labelname = f"{base_filename}.txt"
        labelpath = os.path.join(OUTPUT_LABEL, labelname)
        newlabelname = OUTPUT_LABEL + f"{base_filename}_{i}.txt"

        try:
            f = open(labelpath, 'r')
            h = open(newlabelname, 'w')

            data = f.read()
            h.write(data)

            f.close()
            h.close()
            print(base_filename + "'s image & label save")
        except:
            continue


# 이미지를 읽고, 증강하고, 저장하는 메인 함수
def process_and_save_images(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(input_dir, filename)
            image = cv2.imread(img_path)
            augmented_images = apply_augmentations(image)
            print(filename + ": augmentation finished")
            base_filename = os.path.splitext(filename)[0]
            save_images(augmented_images, base_filename, output_dir)


# 출력 폴더가 없으면 생성
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# 이미지 처리 함수 호출
process_and_save_images(INPUT_DIR, OUTPUT_DIR)
