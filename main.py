import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import streamlit as st
import pandas as pd
from OCR import extract_text_from_image, filter_numeric_with_billion
from PIL import Image
import re
import time

st.set_page_config(page_title="画像文字抽出ツール", layout="wide")

# 簡単なモード切り替え
mode = st.radio("モード選択", ["数字+億抽出", "全テキスト抽出"])

# ファイルアップローダー（複数ファイル対応）
uploaded_files = st.file_uploader(
    "画像ファイルを選択してください（複数選択可能）",
    type=['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp', 'gif', 'ico'],
    accept_multiple_files=True
)

if uploaded_files:
    # 抽出ボタン
    if st.button("文字抽出開始！", type="primary"):
        with st.spinner("文字認識中..."):
            all_extracted_texts = []
            
            # 各画像から文字抽出
            for i, uploaded_file in enumerate(uploaded_files):
                image = Image.open(uploaded_file)
                extracted_texts = extract_text_from_image(image)
                
                if extracted_texts:
                    # ファイル名を追加
                    for item in extracted_texts:
                        item['file_name'] = uploaded_file.name
                        item['file_index'] = i + 1
                    all_extracted_texts.extend(extracted_texts)
            
            if all_extracted_texts:
                st.success(f"{len(uploaded_files)}個の画像から{len(all_extracted_texts)}個のテキストを検出しました！")
                
                if mode == "数字+億抽出":
                    # 数字+億のフィルタリング
                    filtered_texts = filter_numeric_with_billion(all_extracted_texts)
                    
                    if filtered_texts:
                        st.success(f"数字+億のテキスト: {len(filtered_texts)}個")
                        
                        # pandas DataFrameで表示（ファイル名なし）
                        df = pd.DataFrame([
                            {
                                'テキスト': item['text']
                            }
                            for item in filtered_texts
                        ])
                        
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.warning("数字+億のテキストが見つかりませんでした。")
                
                else:  # 全テキスト抽出
                    # 全テキスト表示（ファイル名なし）
                    for i, item in enumerate(all_extracted_texts):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**テキスト {i+1}:** {item['text']}")
                        with col2:
                            st.write(f"信頼度: {item['confidence']:.2f}")
            else:
                st.error("テキストを検出できませんでした。")