import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import easyocr
import cv2
import numpy as np
from PIL import Image
import io

def extract_text_from_image(image):
    """
    画像から文字を抽出する関数
    """
    # EasyOCRリーダーを初期化（日本語と英語に対応）
    reader = easyocr.Reader(['ja', 'en'])
    
    # 画像をOpenCV形式に変換
    if isinstance(image, str):
        # ファイルパスの場合
        img = cv2.imread(image)
    else:
        # PIL Imageの場合
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # 文字認識を実行
    results = reader.readtext(img)
    
    # 結果を整理
    extracted_texts = []
    for (bbox, text, confidence) in results:
        extracted_texts.append({
            'text': text,
            'confidence': confidence,
            'bbox': bbox
        })
    
    return extracted_texts

def filter_text_by_pattern(texts, pattern):
    """
    抽出されたテキストから特定のパターンにマッチするものをフィルタリング
    """
    import re
    filtered_texts = []
    
    for item in texts:
        if re.search(pattern, item['text']):
            filtered_texts.append(item)
    
    return filtered_texts

def filter_numeric_with_billion(texts):
    """
    「実力:」から始まる数字を抽出して重複除去・降順ソート
    """
    import re
    filtered_texts = []
    unique_numbers = set()  # 重複除去用
    
    # 「実力:」から始まる数字のパターン
    pattern = r'実力:\s*(\d+(?:\.\d+)?)'
    
    for item in texts:
        match = re.search(pattern, item['text'])
        if match:
            try:
                # 数字のみを抽出
                numeric_value = float(match.group(1))
                unique_numbers.add(numeric_value)
            except ValueError:
                continue
    
    # 降順でソートしてリストに変換
    sorted_numbers = sorted(unique_numbers, reverse=True)
    
    # 結果を辞書のリストに変換
    for number in sorted_numbers:
        filtered_texts.append({
            'text': str(number)
        })
    
    return filtered_texts
