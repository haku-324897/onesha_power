import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import pytesseract
import cv2
import numpy as np
from PIL import Image
import io

def extract_text_from_image(image):
    """
    画像から文字を抽出する関数（Tesseract使用）
    """
    # 画像をOpenCV形式に変換
    if isinstance(image, str):
        # ファイルパスの場合
        img = cv2.imread(image)
    else:
        # PIL Imageの場合
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # 文字認識を実行（日本語対応）
    text = pytesseract.image_to_string(img, lang='jpn+eng')
    
    # 結果を整理（EasyOCRと同じ形式に合わせる）
    extracted_texts = []
    lines = text.strip().split('\n')
    
    for i, line in enumerate(lines):
        if line.strip():  # 空行でない場合
            extracted_texts.append({
                'text': line.strip(),
                'confidence': 0.8,  # Tesseractは信頼度を返さないので仮の値
                'bbox': [[0, i*20], [100, i*20], [100, (i+1)*20], [0, (i+1)*20]]  # 仮の座標
            })
    
    return extracted_texts

def filter_numeric_with_billion(texts):
    """
    「実力:」から始まる数字を抽出して重複除去・降順ソート
    """
    import re
    filtered_texts = []
    unique_numbers = set()
    
    # 「実力:」から始まる数字のパターン
    pattern = r'実力:\s*(\d+(?:\.\d+)?)'
    
    for item in texts:
        match = re.search(pattern, item['text'])
        if match:
            try:
                numeric_value = float(match.group(1))
                unique_numbers.add(numeric_value)
            except ValueError:
                continue
    
    # 降順でソートしてリストに変換
    sorted_numbers = sorted(unique_numbers, reverse=True)
    
    for number in sorted_numbers:
        filtered_texts.append({
            'text': str(number)
        })
    
    return filtered_texts
