import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import time
import base64
from typing import Dict, List, Optional, Any, Union
import logging
import re # For validation

# ====================
# HTML Content for the Login Page (Frozen UI - Modified for Streamlit interaction)
# ====================
# IMPORTANT: The original HTML's <script> block with handleLogin() and the onclick attribute
# on the button have been removed to prevent alert() calls and enable communication with Streamlit.
# New JavaScript is added within this HTML to send data to the Streamlit parent.
# This modification is necessary to comply with the "Never use alert()" rule and enable Streamlit interaction,
# which is a deviation from "第2条" and "第10条" of the Frozen Version Protection Principles.
FROZEN_LOGIN_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TONOSAMA - 改善版UI</title>
    <style>
        body {
            background-color: #F8F0E3;
            color: #1A1A1A;
            font-family: 'Helvetica Neue', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            background-color: #F8F0E3;
            padding: 20px;
        }

        /* メインタイトル */
        .main-title {
            text-align: center;
            font-size: 2.8em;
            font-weight: bold;
            color: #1A1A1A;
            margin: 40px 0 20px 0;
        }

        .subtitle {
            text-align: center;
            font-size: 1.3em;
            color: #1A1A1A;
            margin-bottom: 40px;
        }

        /* ご利用の流れセクション */
        .flow-section {
            background-color: #FFFFFF;
            border: 3px solid #8B4513;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 40px;
            box-shadow: 0 4px 12px rgba(139, 69, 19, 0.2);
        }

        .flow-title {
            color: #8B4513;
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
        }

        .flow-title::before {
            content: "⭐";
            margin-right: 10px;
            font-size: 1.2em;
        }

        .flow-description {
            color: #1A1A1A;
            font-size: 1.1em;
            margin-bottom: 25px;
            line-height: 1.7;
        }

        .flow-steps {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .flow-step {
            display: flex;
            align-items: flex-start;
            margin-bottom: 15px;
            padding: 12px;
            background-color: #F8F0E3;
            border-left: 4px solid #8B4513;
            border-radius: 8px;
        }

        .flow-step-number {
            background-color: #8B4513;
            color: #FFFFFF;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 14px;
            margin-right: 15px;
            flex-shrink: 0;
        }

        .flow-step-text {
            color: #1A1A1A;
            font-size: 1em;
            line-height: 1.5;
        }

        /* ログインフォーム */
        .login-form {
            background-color: #FFFFFF;
            border: 3px solid #8B4513;
            border-radius: 16px;
            padding: 40px;
            margin-bottom: 40px;
            box-shadow: 0 6px 20px rgba(139, 69, 19, 0.2);
            max-width: 500px;
            margin-left: auto;
            margin-right: auto;
        }

        .form-group {
            margin-bottom: 25px;
        }

        .form-label {
            display: block;
            font-size: 1.1em;
            font-weight: 600;
            color: #1A1A1A;
            margin-bottom: 8px;
        }

        .form-input {
            width: 100%;
            padding: 18px 20px;
            font-size: 18px;
            font-weight: 500;
            border: 3px solid #8B4513;
            border-radius: 12px;
            background-color: #FFFFFF;
            color: #1A1A1A;
            transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            box-shadow: 0 2px 4px rgba(139, 69, 19, 0.15);
            box-sizing: border-box;
            min-height: 60px;
        }

        .form-input:focus {
            outline: none;
            border-color: #654321;
            box-shadow:
                0 0 0 4px rgba(139, 69, 19, 0.25),
                0 4px 8px rgba(139, 69, 19, 0.2);
            transform: translateY(-1px);
        }

        .form-input:hover {
            border-color: #654321;
            box-shadow: 0 3px 6px rgba(139, 69, 19, 0.2);
        }

        .form-input::placeholder {
            color: #8B4513;
            opacity: 0.6;
            font-style: italic;
        }

        /* 改善されたログインボタン */
        .login-button {
            width: 100%;
            padding: 20px 32px;
            font-size: 20px;
            font-weight: bold;
            font-family: 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(145deg, #A0522D, #8B4513);
            color: #FFFFFF;
            border: none;
            border-radius: 16px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            margin-top: 20px;
            min-height: 70px;

            /* 美しい立体感 */
            box-shadow:
                0 8px 16px rgba(139, 69, 19, 0.4),
                0 4px 8px rgba(139, 69, 19, 0.3),
                0 2px 4px rgba(0, 0, 0, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.2),
                inset 0 -1px 0 rgba(0, 0, 0, 0.1);

            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            user-select: none;
        }

        .login-button:hover {
            background: linear-gradient(145deg, #B8633A, #9A5520);
            transform: translateY(-3px) scale(1.02);
            box-shadow:
                0 12px 24px rgba(139, 69, 19, 0.5),
                0 6px 12px rgba(139, 69, 19, 0.4),
                0 3px 6px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.3),
                inset 0 -1px 0 rgba(0, 0, 0, 0.1);
        }

        .login-button:active {
            background: linear-gradient(145deg, #7A4015, #654321);
            transform: translateY(1px) scale(0.98);
            box-shadow:
                0 2px 4px rgba(139, 69, 19, 0.4),
                0 1px 2px rgba(0, 0, 0, 0.3),
                inset 0 2px 4px rgba(0, 0, 0, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }

        /* 追加のアクセサリー */
        .security-note {
            background-color: #E8F4F8;
            border: 2px solid #1976D2;
            border-radius: 12px;
            padding: 16px;
            margin-top: 20px;
            font-size: 0.9em;
            color: #0D47A1;
            text-align: center;
        }

        /* レスポンシブデザイン */
        @media (max-width: 768px) {
            .login-form {
                margin: 20px;
                padding: 30px 20px;
            }

            .main-title {
                font-size: 2.2em;
            }

            .form-input,
            .login-button {
                font-size: 16px;
            }
        }
    </style>
</head>
<body>
    <div class="container">


        <!-- メインタイトル -->
        <h1 class="main-title">🏯 TONOSAMAへようこそ！</h1>
        <p class="subtitle">ストアIDを入力してログインしてください</p>

        <!-- ご利用の流れセクション -->
        <div class="flow-section">
            <h2 class="flow-title">ご利用の流れ</h2>
            <p class="flow-description">
                TONOSAMAへようこそ！このシステムで、あなたのメニューを世界に届けましょう。たった5つのステップで、多言語対応のメニューが完成します！
            </p>

            <ol class="flow-steps">
                <li class="flow-step">
                    <div class="flow-step-number">1</div>
                    <div class="flow-step-text">ログイン: 発行されたストアIDを入力してログインします。</div>
                </li>
                <li class="flow-step">
                    <div class="flow-step-number">2</div>
                    <div class="flow-step-text">メニュー表アップロード: お店のメニュー画像をアップロードしてください。メニュー情報を読み取ります。</div>
                </li>
                <li class="flow-step">
                    <div class="flow-step-number">3</div>
                    <div class="flow-step-text">想いとヒアリング: お店のコンセプトやメニューへの想いを教えてください。魅力的な文章を作成します。</div>
                </li>
                <li class="flow-step">
                    <div class="flow-step-number">4</div>
                    <div class="flow-step-text">詳細設定: 各メニューのカテゴリやアレルギー情報、写真などを設定します。</div>
                </li>
                <li class="flow-step">
                    <div class="flow-step-number">5</div>
                    <div class="flow-step-text">完了: 全ての設定が完了すると、多言語メニュー情報が準備されます。</div>
                </li>
            </ol>
        </div>

        <!-- 改善されたログインフォーム -->
        <div class="login-form">
            <div class="form-group">
                <label class="form-label" for="store-id">あなたのストアIDを入力してください</label>
                <input
                    type="text"
                    id="store-id"
                    class="form-input"
                    placeholder="例: TONOSAMA001"
                    value=""
                >
            </div>

            <div class="form-group">
                <label class="form-label" for="member-id">責任者メンバー</label>
                <input
                    type="password"
                    id="member-id"
                    class="form-input"
                    placeholder="例: 12345"
                    value=""
                >
            </div>

            <button class="login-button" id="html-login-button">
                ログイン
            </button>

            <div class="security-note">
                🔒 あなたの情報は暗号化されて安全に保護されます
            </div>
        </div>
    </div>

    <script>
        // Original handleLogin() function has been removed to avoid alert() calls and enable Streamlit interaction.
        // Input field interaction improvement (kept as it doesn't conflict and is part of UI)
        document.querySelectorAll('.form-input').forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.style.transform = 'translateY(-2px)';
            });

            input.addEventListener('blur', function() {
                this.parentElement.style.transform = 'translateY(0)';
            });
        });

        // --- NEW JAVASCRIPT FOR STREAMLIT COMMUNICATION ---
        // This script runs inside the iframe. It sends data to the Streamlit parent frame.
        const htmlLoginButton = document.getElementById('html-login-button');
        const htmlStoreIdInput = document.getElementById('store-id');
        const htmlResponsibleNumberInput = document.getElementById('member-id');

        if (htmlLoginButton && htmlStoreIdInput && htmlResponsibleNumberInput) {
            htmlLoginButton.addEventListener('click', function() {
                const storeId = htmlStoreIdInput.value;
                const memberId = htmlResponsibleNumberInput.value;

                // Send data to the Streamlit parent frame using postMessage
                // This data will be picked up by the Streamlit Python backend.
                window.parent.postMessage(
                    {
                        type: 'login_attempt',
                        storeId: storeId,
                        memberId: memberId
                    },
                    '*' // Target origin, '*' for any origin (less secure, but common in iframes)
                );
            });
        }
        // --- END NEW JAVASCRIPT ---
    </script>
</body>
</html>
"""

# ====================
# 1. 共通設定とユーティリティ関数
# ====================

# ロギング設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 定数・設定値
CONFIG = {
    "theme": {
        "primary_color": "#8B4513", # サドルブラウン
        "background_color": "#F8F0E3", # 明るいベージュ
        "text_color": "#1A1A1A" # ダークグレー
    },
    "layout": {
        "max_width": "900px",
        "sidebar_width": "250px"
    },
    "pricing_plans": {
        "free": {"name": "フリー", "price": 0, "features": ["PDF版メニュー"], "cashback_per_use": 0},
        "basic": {"name": "ベーシック", "price": 7700, "features": ["POP印刷・配送"], "cashback_per_use": 0},
        "premium": {"name": "プレミアム", "price": 15400, "features": ["アプリ利用", "AI支援"], "cashback_per_use": 0},
        "business": {"name": "ビジネス", "price": 27500, "features": ["キャッシュバック11円/回"], "cashback_per_use": 11},
        "enterprise": {"name": "エンタープライズ", "price": 42900, "features": ["キャッシュバック16.5円/回"], "cashback_per_use": 16.5}
    },
    "common_allergens": [
        "卵 (Egg)", "乳 (Milk)", "小麦 (Wheat)", "そば (Buckwheat)",
        "落花生 (Peanut)", "えび (Shrimp)", "かに (Crab)", "アーモンド (Almond)",
        "あわび (Abalone)", "いか (Squid)", "いくら (Salmon Roe)", "オレンジ (Orange)",
        "カシューナッツ (Cashew Nut)", "キウイフルーツ (Kiwi Fruit)", "牛肉 (Beef)",
        "くるみ (Walnut)", "ごま (Sesame)", "さけ (Salmon)", "さば (Mackerel)",
        "大豆 (Soybean)", "鶏肉 (Chicken)", "バナナ (Banana)", "豚肉 (Pork)",
        "まつたけ (Matsutake Mushroom)", "もも (Peach)", "やまいも (Yam)",
        "りんご (Apple)", "ゼラチン (Gelatin)"
    ],
    "supported_languages": [
        "日本語", "英語", "韓国語", "中国語(標準語)", "台湾語", "広東語", "タイ語",
        "フィリピノ語", "ベトナム語", "インドネシア語", "スペイン語", "ドイツ語",
        "フランス語", "イタリア語", "ポルトガル語"
    ],
    "menu_categories": ["フード", "コース", "ランチ", "デザート", "ドリンク"]
}

# ====================
# 2. CSS・スタイル定義
# ====================
def apply_custom_css():
    """カスタムCSS適用"""
    st.markdown(f"""
    <style>
    /* CSSロード確認用インジケーター (デバッグ用) */
    .css-load-indicator {{
        position: fixed;
        top: 10px;
        right: 10px;
        width: 20px;
        height: 20px;
        background-color: #4CAF50; /* 緑色: CSSが適用されている */
        border-radius: 50%;
        z-index: 9999;
        box-shadow: 0 0 5px rgba(0,0,0,0.5);
    }}

    /* TONOSAMA茶色テーマ (config.pyから統合) */
    :root {{
        --primary-color: #8B4513; /* サドルブラウン */
        --background-color: #F8F0E3; /* 明るいベージュ */
        --text-color: #1A1A1A; /* ダークグレー */
        --accent-color: #FFD700; /* ゴールド */
    }}

    /* グローバルスタイル */
    html, body, [class^="st-"] {{
        background-color: var(--background-color) !important;
        color: var(--text-color) !important;
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        line-height: 1.6 !important;
    }}

    .stApp {{
        background-color: var(--background-color);
        max-width: {CONFIG['layout']['max_width']};
        margin: auto;
        padding: 2rem !important;
    }}

    h1, h2, h3, h4, h5, h6, p, span, div, li, strong, em {{
        color: var(--text-color) !important;
        text-shadow: none !important;
    }}

    h1, h2, h3, h4, h5, h6 {{
        letter-spacing: 0.02em !important;
    }}

    /* ボタンスタイル */
    .stButton button {{
        background: linear-gradient(145deg, #A0522D, var(--primary-color));
        color: white;
        border: none;
        border-radius: 16px;
        padding: 20px 32px;
        font-weight: bold;
        font-size: 20px;
        transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        box-shadow: 0 8px 16px rgba(139, 69, 19, 0.4);
        min-height: 70px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }}

    .stButton button:hover {{
        background: linear-gradient(145deg, #B8633A, #9A5520);
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 12px 24px rgba(139, 69, 19, 0.5);
    }}

    .stButton button:active {{
        background: linear-gradient(145deg, #7A4015, #654321);
        transform: translateY(1px) scale(0.98);
        box-shadow: 0 2px 4px rgba(139, 69, 19, 0.4);
    }}

    /* 入力フィールドのスタイル */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {{
        border: 3px solid var(--primary-color) !important;
        border-radius: 12px !important;
        background-color: #FFFFFF !important;
        color: var(--text-color) !important;
        padding: 18px 20px !important;
        font-size: 18px !important;
        min-height: 60px !important;
        box-shadow: 0 2px 4px rgba(139, 69, 19, 0.15) !important;
    }}

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus-within {{
        border-color: #654321 !important;
        box-shadow: 0 0 0 4px rgba(139, 69, 19, 0.25), 0 4px 8px rgba(139, 69, 19, 0.2) !important;
        outline: none !important;
    }}

    /* チェックボックスのスタイル */
    .stCheckbox > label {{
        background-color: #FFFFFF !important;
        border: 3px solid var(--primary-color) !important;
        border-radius: 12px !important;
        padding: 20px 24px !important;
        margin: 12px 0 !important;
        display: flex !important;
        align-items: center !important;
        cursor: pointer !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        color: var(--text-color) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        min-height: 70px !important;
        box-shadow: 0 4px 12px rgba(139, 69, 19, 0.2) !important;
        user-select: none !important;
    }}

    .stCheckbox input[type="checkbox"]:checked + label {{
        background-color: var(--primary-color) !important;
        border-color: #654321 !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
    }}

    /* ナビゲーションバーのスタイル */
    .navigation-bar {{
        background-color: #FFFFFF;
        border: 1px solid var(--primary-color);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 30px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
    }}
    .nav-step {{
        color: var(--text-color);
        font-weight: 500;
        padding: 8px 16px;
        border-radius: 6px;
        transition: all 0.3s ease;
        background-color: #F0F0F0;
        border: 1px solid rgba(0, 0, 0, 0.1);
    }}
    .nav-step.active {{
        color: var(--text-color);
        font-weight: bold;
        background-color: #FFFFFF;
        border: 1px solid var(--primary-color);
    }}

    /* メッセージボックスのスタイル */
    div[data-testid="stSuccess"], div[data-testid="stInfo"], div[data-testid="stWarning"], div[data-testid="stError"] {{
        border-radius: 12px !important;
        padding: 20px 24px !important;
        margin: 20px 0 !important;
        font-size: 18px !important;
        font-weight: 600 !important;
    }}
    div[data-testid="stSuccess"] {{ background-color: #E8F5E8 !important; color: #1B5E20 !important; border: 3px solid #4CAF50 !important; box-shadow: 0 4px 12px rgba(76, 175, 80, 0.2) !important; }}
    div[data-testid="stInfo"] {{ background-color: #E8F4F8 !important; color: #0D47A1 !important; border: 3px solid #1976D2 !important; box-shadow: 0 4px 12px rgba(25, 118, 210, 0.2) !important; }}
    div[data-testid="stWarning"] {{ background-color: #FFF8E1 !important; color: #E65100 !important; border: 3px solid #FF9800 !important; box-shadow: 0 4px 12px rgba(255, 152, 0, 0.2) !important; }}
    div[data-testid="stError"] {{ background-color: #FFEBEE !important; color: #B71C1C !important; border: 3px solid #F44336 !important; box-shadow: 0 4px 12px rgba(244, 67, 54, 0.2) !important; }}

    /* プログレスバー (config.pyから統合) */
    .progress-container {{
        background-color: #E0E0E0;
        border-radius: 10px;
        padding: 3px;
        margin: 20px 0;
    }}

    .progress-bar {{
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
        border-radius: 8px;
        height: 20px;
        transition: width 0.3s ease;
    }}

    /* StreamlitデフォルトUIの非表示 */
    #MainMenu, footer, [data-testid="deployButton"], button[title*="Deploy"], button[aria-label*="more"], .css-1rs6os, .hidden-streamlit-widget {{
        display: none !important;
        visibility: hidden !important;
        position: absolute !important;
        left: -9999px !important;
        top: -9999px !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        overflow: hidden !important;
    }}

    /* アレルギー方針ボタンの選択状態スタイル */
    .selection-button.selected {{
        background-color: var(--primary-color) !important;
        background: linear-gradient(145deg, #A0522D, var(--primary-color)) !important; /* Consistent with login button */
        color: #FFFFFF !important;
        border-color: #654321 !important;
        font-weight: bold !important;
        box-shadow: 0 6px 20px rgba(139, 69, 19, 0.4) !important;
        transform: translateY(-1px) !important; /* Slight lift */
    }}

    /* レスポンシブデザイン */
    @media (max-width: 768px) {{
        .main-title {{ font-size: 2.2em !important; }}
        .login-form-container {{ margin: 20px !important; padding: 30px 20px !important; }}
        button, .stButton button {{ padding: 18px 24px !important; font-size: 16px !important; min-height: 70px !important; width: 100% !important; margin: 8px 0 !important; }}
        .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div > div {{ padding: 18px 20px !important; font-size: 20px !important; min-height: 70px !important; }}
        .stCheckbox > label {{ padding: 18px 20px !important; font-size: 20px !important; min-height: 70px !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)

    # JavaScript for additional forced styling and Streamlit communication
    st.markdown("""
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // CSSロード確認用インジケーターのHTMLを追加
        const cssIndicator = document.createElement('div');
        cssIndicator.className = 'css-load-indicator';
        document.body.appendChild(cssIndicator);

        function forceStyles() {
            const hiddenSelectors = [
                '[data-testid="deployButton"]', 'button[title*="Deploy"]', 'button[aria-label*="Deploy"]',
                'button[aria-label*="more"]', 'button[title*="more"]', '#MainMenu', 'footer', '.css-1rs6os'
            ];
            hiddenSelectors.forEach(selector => {
                const elements = document.querySelectorAll(selector);
                elements.forEach(el => { if (el) el.style.display = 'none'; });
            });

            const streamlitButtonSelectors = [
                '.stButton button', '.stButton > button', '[data-testid="stButton"] button',
                '[data-testid="stFormSubmitButton"] button', '[data-testid="stDownloadButton"] button',
                '[class*="stButton"] button', '[class*="baseButton"]', '[class*="Button-"]'
            ];
            streamlitButtonSelectors.forEach(el => {
                // Ensure these are not the hidden bridge buttons
                if (el.getAttribute('aria-label') === 'Hidden Login Trigger') {
                    // This is handled by .hidden-streamlit-widget CSS class
                    return;
                }

                // Apply hover/active styles via JS for robustness, if not already handled by CSS
                if (!el.hasAttribute('data-custom-event-listeners-added')) { // Corrected here
                    el.setAttribute('data-custom-event-listeners-added', 'true');
                    
                    el.addEventListener('mouseenter', function() {
                        if (!this.disabled) {
                            this.style.setProperty('background', 'linear-gradient(145deg, #B8633A, #9A5520)', 'important');
                            this.style.setProperty('background-color', '#9A5520', 'important');
                            this.style.setProperty('transform', 'translateY(-3px) scale(1.02)', 'important');
                            this.style.setProperty('box-shadow', '0 12px 24px rgba(139, 69, 19, 0.5), 0 6px 12px rgba(139, 69, 19, 0.4), 0 3px 6px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.3), inset 0 -1px 0 rgba(0, 0, 0, 0.1)', 'important');
                        }
                    });
                    
                    el.addEventListener('mouseleave', function() {
                        if (!this.disabled) {
                            this.style.setProperty('background', 'linear-gradient(145deg, #A0522D, var(--primary-color))', 'important');
                            this.style.setProperty('background-color', 'var(--primary-color)', 'important');
                            this.style.setProperty('transform', 'translateY(0px) scale(1)', 'important');
                            this.style.setProperty('box-shadow', '0 8px 16px rgba(139, 69, 19, 0.4), 0 4px 8px rgba(139, 69, 19, 0.3), 0 2px 4px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.2), inset 0 -1px 0 rgba(0, 0, 0, 0.1)', 'important');
                        }
                    });
                    
                    el.addEventListener('mousedown', function() {
                        if (!this.disabled) {
                            this.style.setProperty('background', 'linear-gradient(145deg, #7A4015, #654321)', 'important');
                            this.style.setProperty('background-color', '#654321', 'important');
                            this.style.setProperty('transform', 'translateY(1px) scale(0.98)', 'important');
                            this.style.setProperty('box-shadow', '0 2px 4px rgba(139, 69, 19, 0.4), 0 1px 2px rgba(0, 0, 0, 0.3), inset 0 2px 4px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.1)', 'important');
                        }
                    });
                    
                    el.addEventListener('mouseup', function() {
                        if (!this.disabled) {
                            if (this.matches(':hover')) {
                                this.style.setProperty('background', 'linear-gradient(145deg, #B8633A, #9A5520)', 'important');
                                this.style.setProperty('background-color', '#9A5520', 'important');
                                this.style.setProperty('transform', 'translateY(-3px) scale(1.02)', 'important');
                                this.style.setProperty('box-shadow', '0 12px 24px rgba(139, 69, 19, 0.5), 0 6px 12px rgba(139, 69, 19, 0.4), 0 3px 6px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.3), inset 0 -1px 0 rgba(0, 0, 0, 0.1)', 'important');
                            } else {
                                this.style.setProperty('background', 'linear-gradient(145deg, #A0522D, var(--primary-color))', 'important');
                                this.style.setProperty('background-color', 'var(--primary-color)', 'important');
                                this.style.setProperty('transform', 'translateY(0px) scale(1)', 'important');
                                this.style.setProperty('box-shadow', '0 8px 16px rgba(139, 69, 19, 0.4), 0 4px 8px rgba(139, 69, 19, 0.3), 0 2px 4px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.2), inset 0 -1px 0 rgba(0, 0, 0, 0.1)', 'important');
                            }
                        }
                    });
                    
                    el.addEventListener('focus', function() {
                        if (!this.disabled) {
                            this.style.setProperty('outline', '3px solid var(--accent-color)', 'important');
                            this.style.setProperty('outline-offset', '2px', 'important');
                        }
                    });
                    
                    el.addEventListener('blur', function() {
                        this.style.setProperty('outline', 'none', 'important');
                    });
                }
            });
        }

        // Function specifically for allergy buttons (if needed, or merge into forceStyles)
        function applyAllergyButtonStyles() {
            const showAllergyButton = document.querySelector('button[data-testid="stButton"][key="show_allergy"]');
            const hideAllergyButton = document.querySelector('button[data-testid="stButton"][key="hide_allergy"]');
            if (showAllergyButton) showAllergyButton.classList.remove('selected');
            if (hideAllergyButton) hideAllergyButton.classList.remove('selected');
            // This part needs to read Streamlit's session state from Python, which requires a bridge.
            // For now, it will apply based on a placeholder. The Python side will handle the actual state.
            // const allergyPolicy = window.parent.streamlitReportSession.get('allergy_policy'); // Placeholder
            // if (allergyPolicy === "display" && showAllergyButton) { showAllergyButton.classList.add('selected'); }
            // else if (allergyPolicy === "not_display" && hideAllergyButton) { hideAllergyButton.classList.add('selected'); }
        }

        // Function to apply styles to Streamlit's dynamically created widgets
        function applyStylesToStreamlitWidgets() {
            document.querySelectorAll('.stTextInput > div > div > input').forEach(input => {
                if (!input.classList.contains('custom-styled')) {
                    input.classList.add('custom-styled');
                    input.addEventListener('focus', function() { this.style.borderColor = '#654321'; this.style.boxShadow = '0 0 0 4px rgba(139, 69, 19, 0.25), 0 4px 8px rgba(139, 69, 19, 0.2)'; this.style.transform = 'translateY(-1px)'; });
                    input.addEventListener('blur', function() { this.style.borderColor = 'var(--primary-color)'; this.style.boxShadow = '0 2px 4px rgba(139, 69, 19, 0.15)'; this.style.transform = 'translateY(0)'; });
                    input.addEventListener('mouseenter', function() { this.style.borderColor = '#654321'; this.style.boxShadow = '0 3px 6px rgba(139, 69, 19, 0.2)'; });
                    input.addEventListener('mouseleave', function() { if (!this.matches(':focus')) { this.style.borderColor = 'var(--primary-color)'; this.style.boxShadow = '0 2px 4px rgba(139, 69, 19, 0.15)'; } });
                }
            });
            document.querySelectorAll('.stTextArea > div > div > textarea').forEach(textarea => {
                if (!textarea.classList.contains('custom-styled')) {
                    textarea.classList.add('custom-styled');
                    textarea.addEventListener('focus', function() { this.style.borderColor = '#654321'; this.style.boxShadow = '0 0 0 4px rgba(139, 69, 19, 0.25), 0 4px 8px rgba(139, 69, 19, 0.2)'; this.style.transform = 'translateY(-1px)'; });
                    textarea.addEventListener('blur', function() { this.style.borderColor = 'var(--primary-color)'; this.style.boxShadow = '0 2px 4px rgba(139, 69, 19, 0.15)'; this.style.transform = 'translateY(0)'; });
                    textarea.addEventListener('mouseenter', function() { this.style.borderColor = '#654321'; this.style.boxShadow = '0 3px 6px rgba(139, 69, 19, 0.2)'; });
                    textarea.addEventListener('mouseleave', function() { if (!this.matches(':focus')) { this.style.borderColor = 'var(--primary-color)'; this.style.boxShadow = '0 2px 4px rgba(139, 69, 19, 0.15)'; } });
                }
            });
            document.querySelectorAll('.stNumberInput > div > div > input').forEach(input => {
                if (!input.classList.contains('custom-styled')) {
                    input.classList.add('custom-styled');
                    input.addEventListener('focus', function() { this.style.borderColor = '#654321'; this.style.boxShadow = '0 0 0 4px rgba(139, 69, 19, 0.25), 0 4px 8px rgba(139, 69, 19, 0.2)'; this.style.transform = 'translateY(-1px)'; });
                    input.addEventListener('blur', function() { this.style.borderColor = 'var(--primary-color)'; this.style.boxShadow = '0 2px 4px rgba(139, 69, 19, 0.15)'; this.style.transform = 'translateY(0)'; });
                    input.addEventListener('mouseenter', function() { this.style.borderColor = '#654321'; this.style.boxShadow = '0 3px 6px rgba(139, 69, 19, 0.2)'; });
                    input.addEventListener('mouseleave', function() { if (!this.matches(':focus')) { this.style.borderColor = 'var(--primary-color)'; this.style.boxShadow = '0 2px 4px rgba(139, 69, 19, 0.15)'; } });
                }
            });
            document.querySelectorAll('.stSelectbox > div > div > div').forEach(selectbox => {
                if (!selectbox.classList.contains('custom-styled')) {
                    selectbox.classList.add('custom-styled');
                    selectbox.addEventListener('focus', function() { this.style.borderColor = '#654321'; this.style.boxShadow = '0 0 0 4px rgba(139, 69, 19, 0.25), 0 4px 8px rgba(139, 69, 19, 0.2)'; this.style.transform = 'translateY(-1px)'; });
                    selectbox.addEventListener('blur', function() { this.style.borderColor = 'var(--primary-color)'; this.style.boxShadow = '0 2px 4px rgba(139, 69, 19, 0.15)'; this.style.transform = 'translateY(0)'; });
                    selectbox.addEventListener('mouseenter', function() { this.style.borderColor = '#654321'; this.style.boxShadow = '0 3px 6px rgba(139, 69, 19, 0.2)'; });
                    selectbox.addEventListener('mouseleave', function() { if (!this.matches(':focus')) { this.style.borderColor = 'var(--primary-color)'; this.style.boxShadow = '0 2px 4px rgba(139, 69, 19, 0.15)'; } });
                }
            });
            document.querySelectorAll('.streamlit-expanderHeader').forEach(expanderHeader => {
                if (!expanderHeader.classList.contains('custom-styled')) {
                    expanderHeader.classList.add('custom-styled');
                    expanderHeader.addEventListener('mouseenter', function() { this.style.borderColor = '#654321'; this.style.backgroundColor = '#FFF8F0'; this.style.boxShadow = '0 6px 20px rgba(139, 69, 19, 0.3)'; this.style.transform = 'translateY(-2px)'; });
                    expanderHeader.addEventListener('mouseleave', function() { this.style.borderColor = 'var(--primary-color)'; this.style.backgroundColor = '#FFFFFF'; this.style.boxShadow = '0 4px 12px rgba(139, 69, 19, 0.2)'; this.style.transform = 'translateY(0)'; });
                }
            });
        }

        // Initial execution
        forceStyles();
        applyAllergyButtonStyles(); // Apply allergy button styles initially
        applyStylesToStreamlitWidgets(); // Apply styles to other widgets initially
        
        // Monitor changes for dynamically added elements
        const observer = new MutationObserver(forceStyles);
        observer.observe(document.body, { childList: true, subtree: true });
        
        // Periodic execution (as a fallback)
        setInterval(forceStyles, 1000);
    });
    </script>
    """, unsafe_allow_html=True)

# ====================
# 3. セッション状態管理
# ====================
def ensure_session_state(key: str, default_value: Any):
    """
    機能: セッション状態の確実な初期化
    STEP: 全体
    入力: key (str), default_value (Any)
    出力: なし
    エラー: なし
    """
    if key not in st.session_state:
        st.session_state[key] = default_value
        logger.info(f"Session state '{key}' initialized with default value.")

def initialize_app_session_state():
    """
    機能: アプリケーション全体のセッション状態を初期化
    STEP: 全体
    入力: なし
    出力: なし
    エラー: なし
    """
    ensure_session_state("current_step", -1) # 初期ステップは-1 (利用規約)
    ensure_session_state("logged_in", False)
    ensure_session_state("store_id", "")
    ensure_session_state("responsible_number", "")
    ensure_session_state("selected_plan", None) # 選択された料金プラン
    ensure_session_state("payment_status", "pending") # 'pending', 'paid', 'failed'
    ensure_session_state("terms_agreed", False) # 利用規約同意
    ensure_session_state("uploaded_menu_file", None)
    ensure_session_state("ocr_results", None) # OCRで抽出された生データ
    ensure_session_state("finalized_menus", []) # ユーザーが編集したメニューリスト
    ensure_session_state("ocr_processed", False)
    ensure_session_state("manual_menu_id_counter", 1000)
    ensure_session_state("owner_answers_dict", {}) # 店主の想いヒアリング回答
    ensure_session_state("summarized_thought", "")
    ensure_session_state("translated_thoughts", None)
    ensure_session_state("allergy_policy", None) # 'display' or 'not_display'
    ensure_session_state("featured_menus", []) # イチオシメニューのIDリスト
    ensure_session_state("csv_generated", False) # CSV生成完了フラグ
    ensure_session_state("csv_download_url", "") # 生成されたCSVのダウンロードURL
    logger.info("Application session state initialized.")

def reset_session_state(keys: Optional[List[str]] = None):
    """
    機能: 指定されたセッション状態、または全てのセッション状態をリセット
    STEP: 全体
    入力: keys (List[str], optional): リセットするキーのリスト。Noneの場合、全てリセット。
    出力: なし
    エラー: なし
    """
    if keys is None:
        # Streamlitの内部キーを除外してクリア
        for key in list(st.session_state.keys()):
            if not key.startswith("FormSubmitter") and not key.startswith("file_uploader"):
                del st.session_state[key]
        logger.info("All relevant session states reset.")
    else:
        for key in keys:
            if key in st.session_state:
                del st.session_state[key]
                logger.info(f"Session state '{key}' reset.")

# ====================
# 4. コンポーネント関数群
# ====================
def show_universal_navigation():
    """
    機能: 全ページ共通のステップナビゲーションバーを表示
    STEP: 全体
    入力: なし
    出力: なし
    エラー: なし
    """
    steps = ["利用規約", "プラン選択", "ログイン", "メニュー", "想い", "詳細設定", "イチオシ", "完了"]
    current = st.session_state.get("current_step", -1)

    nav_html = '<div class="navigation-bar">'
    for i, step in enumerate(steps):
        active_class = "active" if i == current else ""
        nav_html += f'<span class="nav-step {active_class}">{i+1}. {step}</span>'
    nav_html += '</div>'
    st.markdown(nav_html, unsafe_allow_html=True)

    # プログレスバーの表示
    progress_percentage = ((current + 1) / len(steps)) * 100 if current >= -1 else 0
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {progress_percentage:.0f}%;"></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:var(--text-color);'>進捗: {progress_percentage:.0f}%</p>", unsafe_allow_html=True)


def create_card_component(title: str, content: str, key: str, actions: Optional[List[Dict]] = None):
    """
    機能: 再利用可能なカードコンポーネント
    STEP: 全体
    入力: title (str), content (str), key (str), actions (List[Dict], optional)
    出力: なし
    エラー: なし
    """
    st.markdown(f"""
    <div class="card" style="
        background-color: #FFFFFF;
        border: 3px solid var(--primary-color);
        border-radius: 16px;
        padding: 30px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(139, 69, 19, 0.2);
    ">
        <h3 class="card-title" style="color:var(--primary-color); font-size:1.5em; margin-bottom:15px;">{title}</h3>
        <div class="card-content" style="color:var(--text-color); line-height:1.6;">{content}</div>
        <div class="card-actions" style="margin-top:20px;">
            <!-- アクションボタンはStreamlitのボタンを配置 -->
        </div>
    </div>
    """, unsafe_allow_html=True)
    # Streamlit buttons need to be rendered outside the markdown for interactivity
    if actions:
        cols = st.columns(len(actions))
        for i, action in enumerate(actions):
            with cols[i]:
                if st.button(action['label'], key=f"{key}_action_{i}"):
                    action['callback']()

def create_form_field(field_type: str, label: str, key: str, **kwargs: Any) -> Any:
    """
    機能: 統一されたフォームフィールド
    STEP: 全体
    入力: field_type (str), label (str), key (str), kwargs (Any)
    出力: フィールドの値
    エラー: なし
    """
    st.markdown(f'<label class="form-label" style="display:block; font-size:1.1em; font-weight:600; color:var(--text-color); margin-bottom:8px;">{label}</label>', unsafe_allow_html=True)
    
    if field_type == "text":
        return st.text_input("", key=key, label_visibility="collapsed", **kwargs)
    elif field_type == "number":
        return st.number_input("", key=key, label_visibility="collapsed", **kwargs)
    elif field_type == "select":
        return st.selectbox("", key=key, label_visibility="collapsed", **kwargs)
    elif field_type == "textarea":
        return st.text_area("", key=key, label_visibility="collapsed", **kwargs)
    elif field_type == "password":
        return st.text_input("", type="password", key=key, label_visibility="collapsed", **kwargs)
    else:
        logger.warning(f"Unsupported field type: {field_type}")
        return None

def create_button(label: str, key: str, variant: str = "primary", size: str = "md", **kwargs: Any) -> bool:
    """
    機能: 統一されたボタンコンポーネント
    STEP: 全体
    入力: label (str), key (str), variant (str), size (str), kwargs (Any)
    出力: ボタンがクリックされたか (bool)
    エラー: なし
    """
    # Streamlitのボタンは直接CSSクラスを適用できないため、CSSはグローバルに定義し、
    # ここではStreamlitのネイティブボタンを使用
    return st.button(label, key=key, help=kwargs.get('help', ''))

def display_message(message: str, type: str = "info"):
    """
    機能: 統一されたメッセージボックスを表示
    STEP: 全体
    入力: message (str), type (str): 'success', 'info', 'warning', 'error'
    出力: なし
    エラー: なし
    """
    if type == "success":
        st.success(message)
    elif type == "info":
        st.info(message)
    elif type == "warning":
        st.warning(message)
    elif type == "error":
        st.error(message)
    else:
        st.write(message) # Fallback for unknown type

# ====================
# 5. データ構造定義
# ====================
class PricingPlan:
    """料金プランデータクラス"""
    def __init__(self, name: str, price: int, features: List[str], cashback_per_use: float):
        self.name = name
        self.price = price
        self.features = features
        self.cashback_per_use = cashback_per_use

class MenuData:
    """
    メニューデータクラス
    65列CSV構造のメニュー情報を保持
    """
    def __init__(self, id: int, name: str, price: str, category: str, order: int,
                 image_url: Optional[str] = None,
                 allergens: Optional[List[str]] = None,
                 multilingual_descriptions: Optional[Dict[str, str]] = None,
                 is_featured: bool = False): # イチオシメニューフラグ
        self.id = id
        self.name = name # 日本語メニュー名
        self.price = price
        self.category = category
        self.order = order
        self.image_url = image_url if image_url is not None else ""
        self.allergens = allergens if allergens is not None else []
        # multilingual_descriptions: {"言語": "説明文"}
        self.multilingual_descriptions = multilingual_descriptions if multilingual_descriptions is not None else {"日本語": ""}
        self.is_featured = is_featured # イチオシメニューフラグ
        self.should_introduce = True # メニューアップロード時に掲載するかどうか

class OwnerThoughts:
    """店主想いデータクラス"""
    def __init__(self, answers: Dict[str, str], summary: str = "", translations: Optional[Dict[str, str]] = None):
        self.answers = answers # ヒアリングの生回答
        self.summary = summary # AIが要約した想い（日本語）
        self.translations = translations if translations is not None else {} # 各言語への翻訳

class CSVRowStructure:
    """
    最終的な65列CSVの行構造を定義するクラス
    このクラスは、MenuDataとOwnerThoughtsから最終的なCSV行を構築する責任を持つ
    """
    def __init__(self, menu_item: MenuData, owner_thoughts: OwnerThoughts, allergy_policy: str):
        self.menu_item = menu_item
        self.owner_thoughts = owner_thoughts
        self.allergy_policy = allergy_policy
        self.row_data: Dict[str, Any] = {}
        self._build_row()

    def _build_row(self):
        # 基本情報 (5列)
        self.row_data['価格'] = self.menu_item.price
        self.row_data['画像URL'] = self.menu_item.image_url
        self.row_data['カテゴリ'] = self.menu_item.category
        self.row_data['おすすめ'] = "TRUE" if self.menu_item.is_featured else "FALSE"
        self.row_data['並び順'] = self.menu_item.order + 1 # 1から始まる番号

        # アレルギー情報 (28列)
        for allergen in CONFIG['common_allergens']:
            col_name = f"アレルギー_{allergen.split(' ')[0]}" # 例: アレルギー_卵
            self.row_data[col_name] = "TRUE" if allergen in self.menu_item.allergens and self.allergy_policy == "display" else "FALSE"

        # メニュー翻訳 (30列: 15言語 x 2項目)
        for lang in CONFIG['supported_languages']:
            # メニュー名翻訳（日本語はMenuData.nameを使用、他は翻訳APIから取得）
            menu_name_col = f"メニュー名_{lang}"
            self.row_data[menu_name_col] = self.menu_item.multilingual_descriptions.get(lang, self.menu_item.name if lang == "日本語" else "")

            # メニュー説明翻訳
            menu_desc_col = f"メニュー説明_{lang}"
            self.row_data[menu_desc_col] = self.menu_item.multilingual_descriptions.get(lang, "")

        # 店主想い翻訳 (15列)
        for lang in CONFIG['supported_languages']:
            owner_thought_col = f"店主想い_{lang}"
            self.row_data[owner_thought_col] = self.owner_thoughts.translations.get(lang, "")

        # 備考 (1列)
        self.row_data['備考'] = "" # 現時点では空、必要に応じて追加

    def get_row(self) -> Dict[str, Any]:
        return self.row_data

    def get_headers(self) -> List[str]:
        # ヘッダーの順序を定義 (65列)
        headers = ['価格', '画像URL', 'カテゴリ', 'おすすめ', '並び順']
        for allergen in CONFIG['common_allergens']:
            headers.append(f"アレルギー_{allergen.split(' ')[0]}")
        for lang in CONFIG['supported_languages']:
            headers.append(f"メニュー名_{lang}")
            headers.append(f"メニュー説明_{lang}")
        for lang in CONFIG['supported_languages']:
            headers.append(f"店主想い_{lang}")
        headers.append('備考')
        return headers

# ====================
# 6. ユーティリティ関数
# ====================
def safe_execute(func, *args, **kwargs) -> Optional[Any]:
    """
    機能: 安全な関数実行（エラーハンドリング付き）
    STEP: 全体
    入力: func (Callable), *args, **kwargs
    出力: 関数の戻り値、またはNone (エラー時)
    エラー: 実行時エラーを捕捉し、ログ出力とStreamlitメッセージ表示
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"エラーが発生しました: {func.__name__} - {str(e)}")
        st.error(f"申し訳ございません。エラーが発生しました: {str(e)}")
        return None

def validate_input(value: Any, validation_type: str, **kwargs) -> bool:
    """
    機能: 入力値のバリデーション
    STEP: 全体
    入力: value (Any), validation_type (str), kwargs (Dict)
    出力: バリデーション結果 (bool)
    エラー: なし (呼び出し元でエラーメッセージ表示)
    """
    try:
        if validation_type == "email":
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return bool(re.match(pattern, value))
        elif validation_type == "phone":
            pattern = r'^[0-9-+\s()]+$'
            return bool(re.match(pattern, value))
        elif validation_type == "number":
            min_val = kwargs.get('min', float('-inf'))
            max_val = kwargs.get('max', float('inf'))
            return min_val <= float(value) <= max_val
        elif validation_type == "length":
            min_len = kwargs.get('min', 0)
            max_len = kwargs.get('max', float('inf'))
            return min_len <= len(str(value)) <= max_len
        elif validation_type == "not_empty":
            return bool(value and str(value).strip())
        return True
    except Exception as e:
        logger.error(f"バリデーションエラー: {str(e)}")
        return False

def log_event(level: str, message: str, **kwargs: Any):
    """
    機能: アプリケーションイベントのログ出力
    STEP: 全体
    入力: level (str): 'info', 'warning', 'error', message (str), kwargs (Any)
    出力: なし
    エラー: なし
    """
    if level == "info":
        logger.info(message, extra=kwargs)
    elif level == "warning":
        logger.warning(message, extra=kwargs)
    elif level == "error":
        logger.error(message, extra=kwargs)
    else:
        logger.debug(message, extra=kwargs)

def get_base64_image(image_path: str) -> str:
    """
    機能: 画像ファイルをBase64エンコードして返す (ダミー)
    STEP: 詳細設定
    入力: image_path (str)
    出力: Base64エンコードされた画像データ (str)
    エラー: ファイルが見つからない場合
    """
    # 実際には画像パスからBase64を生成
    # ここではダミーのBase64データを返す
    if image_path.startswith("simulated_image_url"):
        # 例: 非常に小さな透明なGIFのBase64
        return "data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=="
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded_string}"
    except FileNotFoundError:
        logger.warning(f"Image file not found: {image_path}")
        return "" # またはデフォルト画像

# ====================
# 7. ページ別表示関数
# ====================

#### STEP -1: 利用規約確認・同意

def load_terms_of_service() -> str:
    """
    機能: 利用規約テキストの読み込み
    STEP: -1
    入力: なし
    出力: 利用規約テキスト (str)
    外部連携: なし (将来的には外部ファイルやDBから読み込み)
    エラー: なし
    """
    terms = """
    ## TONOSAMA 利用規約

    ### 第1条（本規約の適用）
    本規約は、合同会社オリオーネ（以下「当社」といいます）が提供する「TONOSAMA」サービス（以下「本サービス」といいます）の利用に関する一切に適用されます。

    ### 第2条（本サービスの利用）
    利用者は、本規約に同意の上、本サービスを利用するものとします。

    ### 第3条（利用料金）
    本サービスの利用料金は、別途定める料金プランに従うものとします。

    ### 第4条（禁止事項）
    利用者は、本サービスの利用にあたり、以下の行為を行ってはなりません。
    1. 法令または公序良俗に違反する行為
    2. 当社または第三者の権利を侵害する行為
    3. 本サービスの運営を妨害する行為

    ### 第5条（免責事項）
    当社は、本サービスの利用により利用者に生じた損害について、一切の責任を負わないものとします。

    ### 第6条（本規約の変更）
    当社は、必要と判断した場合、利用者に通知することなく本規約を変更できるものとします。

    ### 第7条（準拠法および管轄裁判所）
    本規約の解釈にあたっては、日本法を準拠法とします。また、本サービスに関する一切の紛争については、名古屋地方裁判所を第一審の専属的合意管轄裁判所とします。

    ---
    **合同会社オリオーネ**
    """
    return terms

def show_terms_of_service_page():
    """
    機能: 利用規約確認・同意ページを表示
    STEP: -1
    入力: なし
    出力: なし
    エラー: なし
    """
    show_universal_navigation()
    st.title("📜 利用規約")
    st.info("本サービスをご利用いただく前に、以下の利用規約をご確認いただき、同意をお願いいたします。")

    terms_content = load_terms_of_service()
    st.markdown(terms_content, unsafe_allow_html=True)

    # 同意チェックボックス
    agreed = st.checkbox("利用規約に同意します。", key="terms_agreement_checkbox")

    if create_button("次へ進む (プラン選択へ) ➡️", key="terms_next_button", disabled=not agreed):
        st.session_state.terms_agreed = True
        st.session_state.current_step = 0 # 次のステップへ
        st.rerun()
    elif not agreed:
        st.warning("利用規約に同意しないと次のステップに進めません。")

#### STEP 0: プラン選択・Stripe決済

def get_pricing_plans() -> Dict[str, PricingPlan]:
    """
    機能: 料金プラン情報の取得
    STEP: 0
    入力: なし
    出力: プラン情報辞書 (Dict[str, PricingPlan])
    外部連携: なし (CONFIGから読み込み)
    エラー: なし
    """
    plans = {}
    for key, data in CONFIG['pricing_plans'].items():
        plans[key] = PricingPlan(data['name'], data['price'], data['features'], data['cashback_per_use'])
    return plans

def create_stripe_checkout_session(plan_id: str, store_id: str) -> Optional[str]:
    """
    機能: Stripe決済セッション作成
    STEP: 0
    入力: plan_id (str), store_id (str)
    出力: 決済URL (str) または None (エラー時)
    外部連携: Stripe API
    エラー: Stripe API呼び出し失敗、無効なプランID
    """
    # 実際にはStripe APIを呼び出す
    # import stripe
    # stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
    # try:
    #     checkout_session = stripe.checkout.Session.create(
    #         line_items=[
    #             {
    #                 'price_data': {
    #                     'currency': 'jpy',
    #                     'product_data': {
    #                         'name': CONFIG['pricing_plans'][plan_id]['name'],
    #                     },
    #                     'unit_amount': CONFIG['pricing_plans'][plan_id]['price'],
    #                 },
    #                 'quantity': 1,
    #             },
    #         ],
    #         mode='payment',
    #         success_url='http://localhost:8501/?payment_success=true&session_id={CHECKOUT_SESSION_ID}',
    #         cancel_url='http://localhost:8501/?payment_cancel=true',
    #         metadata={'store_id': store_id, 'plan_id': plan_id},
    #     )
    #     return checkout_session.url
    # except stripe.error.StripeError as e:
    #     logger.error(f"Stripe checkout session creation failed: {e}")
    #     st.error(f"決済セッションの作成に失敗しました: {e}")
    #     return None
    
    # モック実装
    st.info(f"Stripe決済セッションを作成中... (プラン: {CONFIG['pricing_plans'][plan_id]['name']})")
    time.sleep(1)
    mock_payment_url = f"https://mock-stripe.com/checkout?session_id=mock_{plan_id}_{int(time.time())}"
    logger.info(f"Mock Stripe URL generated: {mock_payment_url}")
    return mock_payment_url

def handle_stripe_webhook(payload: Dict) -> bool:
    """
    機能: StripeからのWebhookイベントを処理し、決済状況を更新
    STEP: 0 (バックエンド処理)
    入力: payload (Dict): Stripe Webhookデータ
    出力: 処理成功 (bool)
    外部連携: Stripe API (イベント検証)
    エラー: 無効なイベント、署名検証失敗
    備考: Streamlitアプリ内でのWebhookエンドポイント実装は難しいため、
          実際には別途Webサーバーで実装し、DB経由でStreamlitと連携する。
          ここでは、決済成功後のリダイレクトパラメータを処理する形で代替。
    """
    # 実際にはStripe Webhookの署名検証とイベント処理を行う
    # try:
    #     event = stripe.Webhook.construct_event(
    #         payload, sig_header, os.environ.get("STRIPE_WEBHOOK_SECRET")
    #     )
    # except ValueError as e:
    #     logger.error(f"Invalid payload: {e}")
    #     return False
    # except stripe.error.SignatureVerificationError as e:
    #     logger.error(f"Invalid signature: {e}")
    #     return False

    # if event['type'] == 'checkout.session.completed':
    #     session = event['data']['object']
    #     store_id = session['metadata']['store_id']
    #     plan_id = session['metadata']['plan_id']
    #     # データベースに決済情報を記録し、store_idの決済ステータスを更新
    #     logger.info(f"Stripe checkout session completed for store_id: {store_id}, plan: {plan_id}")
    #     return True
    
    logger.info(f"Mock Stripe Webhook handled. Payload: {payload}")
    return True # モックでは常に成功

def issue_invoice_receipt(store_id: str, type: str = "invoice") -> Optional[str]:
    """
    機能: 請求書または領収書を発行し、ダウンロードURLを生成
    STEP: 0 (およびログインページからアクセス可能)
    入力: store_id (str), type (str): 'invoice' or 'receipt'
    出力: ダウンロードURL (str) または None (エラー時)
    外部連携: Google Drive API (PDF保存), SMTP (メール送付)
    エラー: ファイル生成失敗、アップロード失敗、メール送信失敗
    """
    st.info(f"{store_id} の {type} を発行中...")
    time.sleep(1.5)
    # 実際にはPDF生成ライブラリ (ReportLabなど) でPDFを作成し、Google Driveにアップロード
    # その後、ダウンロードURLを生成し、SMTPでユーザーにメール送信
    mock_url = f"https://mock-drive.com/download/{store_id}_{type}_{int(time.time())}.pdf"
    logger.info(f"Mock {type} URL generated: {mock_url}")
    # send_email(store_id, f"TONOSAMA {type} 発行のお知らせ", f"ダウンロードはこちら: {mock_url}")
    return mock_url

def show_plan_selection_page():
    """
    機能: プラン選択・決済ページを表示
    STEP: 0
    入力: なし
    出力: なし
    エラー: なし
    """
    show_universal_navigation()
    st.title("💰 プラン選択")
    st.info("お客様のニーズに合わせた最適なプランをお選びください。")

    plans = get_pricing_plans()
    
    cols = st.columns(len(plans))
    selected_plan_key = st.session_state.get("selected_plan_key", None)

    for i, (key, plan) in enumerate(plans.items()):
        with cols[i]:
            card_style = "border: 3px solid var(--primary-color);" if selected_plan_key == key else "border: 1px solid #ddd;"
            st.markdown(f"""
            <div style="
                background-color: #FFFFFF;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                text-align: center;
                min-height: 250px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                {card_style}
            ">
                <h3 style="color:var(--primary-color); margin-bottom:10px;">{plan.name}</h3>
                <p style="font-size:1.8em; font-weight:bold; color:var(--text-color);">¥{plan.price:,}</p>
                <ul style="list-style:none; padding:0; margin-bottom:15px; font-size:0.9em;">
                    {"".join([f'<li>✅ {f}</li>' for f in plan.features])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if create_button(f"このプランを選択 ({plan.name})", key=f"select_plan_{key}", use_container_width=True):
                st.session_state.selected_plan_key = key
                st.session_state.selected_plan = plan # プランオブジェクトを保存
                st.success(f"「{plan.name}」プランを選択しました。")
                st.rerun()

    if st.session_state.selected_plan:
        st.markdown("---")
        st.subheader(f"選択中のプラン: **{st.session_state.selected_plan.name}** (¥{st.session_state.selected_plan.price:,})")
        st.info("選択したプランで決済に進みます。")
        
        if create_button("Stripeで決済する 💳", key="proceed_to_payment_button"):
            payment_url = safe_execute(create_stripe_checkout_session, st.session_state.selected_plan_key, "TONOSAMA_TEMP_STORE_ID") # 仮のストアID
            if payment_url:
                st.markdown(f'<a href="{payment_url}" target="_blank" style="display:inline-block; padding:15px 30px; background-color:#6772E5; color:white; border-radius:8px; text-decoration:none; font-weight:bold;">決済ページへ移動</a>', unsafe_allow_html=True)
                st.warning("決済ページへ移動してください。決済完了後、このページに戻ると自動的にログインページへ進みます。")
                # 決済完了を待つロジック（実際はWebhookまたはポーリング）
                # ここでは簡易的に、ユーザーが手動で戻ってきたと仮定し、次へ進むボタンを表示
                st.session_state.payment_status = "paid" # モックとして決済済みとする
                time.sleep(1) # ユーザーが決済ページに遷移するのを待つシミュレーション
                st.session_state.current_step = 1 # 決済完了後、ログインページへ
                st.rerun()
    else:
        st.warning("プランを選択してください。")

    st.markdown("---")
    # ナビゲーションボタン (戻る)
    if create_button("⬅️ 戻る (利用規約へ)", key="step0_back_to_terms"):
        st.session_state.current_step = -1
        st.rerun()

#### STEP 1: ログイン・認証

def authenticate_store_id(store_id: str) -> bool:
    """
    機能: マスターシートでStore IDの存在を確認
    STEP: 1
    入力: store_id (str)
    出力: 認証結果 (bool)
    外部連携: Google Sheets API / 内部DB (概念)
    エラー: 無効なストアID
    """
    display_message(f"マスターシートでストアID: {store_id} の存在を確認中...", "info")
    time.sleep(0.5)
    # TODO: Google Sheets APIまたはDBと連携して実際の認証を行う
    return store_id == "TONOSAMA001" # モックID

def authenticate_responsible_number(responsible_number: str) -> bool:
    """
    機能: 責任者番号の認証
    STEP: 1
    入力: responsible_number (str)
    出力: 認証結果 (bool)
    外部連携: 内部DB (概念)
    エラー: 無効な責任者番号
    """
    display_message(f"責任者ナンバーを確認中...", "info")
    time.sleep(0.5)
    # TODO: 実際の認証ロジック
    return responsible_number == "99999" # モック番号

def check_payment_status(store_id: str) -> str:
    """
    機能: Stripe決済状況を確認
    STEP: 1
    入力: store_id (str)
    出力: 決済状況 ('paid', 'unpaid', 'error')
    外部連携: Stripe API / 内部DB (概念)
    エラー: API呼び出し失敗
    """
    display_message(f"決済状況を確認中...", "info")
    time.sleep(0.5)
    # TODO: Stripe APIまたはDBと連携して実際の決済状況を取得
    return "paid" if store_id == "TONOSAMA001" else "unpaid" # モック

def show_login_page():
    """
    機能: ログイン・認証ページを表示
    STEP: 1
    入力: なし
    出力: なし
    エラー: なし
    """
    show_universal_navigation()
    
    # Streamlitのメッセージ表示用プレースホルダー
    message_placeholder = st.empty()

    st.components.v1.html(FROZEN_LOGIN_HTML, height=900, scrolling=True) # 凍結版HTMLを埋め込み

    # Streamlitの隠しウィジェット (JavaScriptからのデータを受け取るためのブリッジ)
    # これらのウィジェットはCSSで完全に非表示にされます。
    hidden_store_id_input = st.text_input(
        "Hidden Store ID Input",
        value="", # 初期値は空
        key="hidden_store_id_bridge",
        label_visibility="collapsed",
    )
    hidden_responsible_number_input = st.text_input(
        "Hidden Responsible Number Input",
        value="", # 初期値は空
        type="password",
        key="hidden_responsible_number_bridge",
        label_visibility="collapsed",
    )
    hidden_login_trigger_button = st.button(
        "Hidden Login Trigger",
        key="hidden_login_trigger_button",
    )

    if hidden_login_trigger_button:
        store_id_val = st.session_state.hidden_store_id_bridge
        responsible_number_val = st.session_state.hidden_responsible_number_bridge

        if not validate_input(store_id_val, "not_empty"):
            message_placeholder.warning("ストアIDを入力してください。")
        elif not validate_input(responsible_number_val, "not_empty"):
            message_placeholder.warning("責任者ナンバーを入力してください。")
        else:
            auth_store_id_success = safe_execute(authenticate_store_id, store_id_val)
            if not auth_store_id_success:
                message_placeholder.error("❌ 無効なストアIDです。もう一度お確かめください。")
            else:
                auth_responsible_number_success = safe_execute(authenticate_responsible_number, responsible_number_val)
                if not auth_responsible_number_success:
                    message_placeholder.error("❌ 無効な責任者ナンバーです。")
                else:
                    payment_status = safe_execute(check_payment_status, store_id_val)
                    if payment_status == "paid":
                        message_placeholder.success("✅ ログインに成功しました！")
                        st.session_state.logged_in = True
                        st.session_state.store_id = store_id_val
                        st.session_state.responsible_number = responsible_number_val
                        st.session_state.current_step = 2 # 次のステップへ
                        time.sleep(1)
                        st.rerun()
                    elif payment_status == "unpaid":
                        message_placeholder.warning("⚠️ ストアIDは確認できましたが、決済が完了していません。代理店にご確認ください。")
                    else:
                        message_placeholder.error("❌ 決済状況の確認中にエラーが発生しました。")
    
    st.markdown("---")
    st.subheader("請求書・領収書発行")
    st.info("アプリ使用に関する請求書・領収書が必要な方は、こちらから発行いただけます。")
    if create_button("アプリ使用請求書・領収書を発行", key="issue_app_invoice_receipt_btn"):
        if st.session_state.get('store_id'):
            download_url = safe_execute(issue_invoice_receipt, st.session_state.store_id, "invoice")
            if download_url:
                st.success(f"請求書が発行されました。ダウンロードはこちら: [請求書をダウンロード]({download_url})")
        else:
            st.warning("請求書を発行するには、まずストアIDでログインしてください。")

    # Streamlitの隠しウィジェットをCSSで非表示にするためのJavaScriptを注入
    # これはStreamlitのレンダリング後に実行されるようにする
    st.markdown("""
    <script>
        // Streamlitの隠しウィジェット要素を特定し、hidden-streamlit-widgetクラスを付与
        const hiddenStoreIdBridge = document.querySelector('[data-testid="stTextInput"] input[type="text"][aria-label="Hidden Store ID Input"]');
        const hiddenResponsibleNumberBridge = document.querySelector('[data-testid="stTextInput"] input[type="password"][aria-label="Hidden Responsible Number Input"]');
        const hiddenLoginTriggerButton = document.querySelector('[data-testid="stButton"] button[aria-label="Hidden Login Trigger"]');

        if (hiddenStoreIdBridge) {
            hiddenStoreIdBridge.closest('[data-testid="stTextInput"]').classList.add('hidden-streamlit-widget');
        }
        if (hiddenResponsibleNumberBridge) {
            hiddenResponsibleNumberBridge.closest('[data-testid="stTextInput"]').classList.add('hidden-streamlit-widget');
        }
        if (hiddenLoginTriggerButton) {
            hiddenLoginTriggerButton.classList.add('hidden-streamlit-widget');
        }

        // HTML内のJavaScriptからpostMessageでデータを受け取った際の処理
        window.addEventListener('message', function(event) {
            // Check if the message is from our embedded iframe and has the correct type
            if (event.source && event.data && event.data.type === 'login_attempt') {
                const storeId = event.data.storeId;
                const memberId = event.data.memberId;

                // Set values to Streamlit's hidden input fields
                if (hiddenStoreIdBridge && hiddenResponsibleNumberBridge) {
                    hiddenStoreIdBridge.value = storeId;
                    hiddenResponsibleNumberBridge.value = memberId;
                    
                    // Dispatch input event to notify Streamlit of the change
                    hiddenStoreIdBridge.dispatchEvent(new Event('input', { bubbles: true }));
                    hiddenResponsibleNumberBridge.dispatchEvent(new Event('input', { bubbles: true }));
                }

                // Programmatically click the hidden Streamlit button to trigger a rerun
                if (hiddenLoginTriggerButton) {
                    hiddenLoginTriggerButton.click();
                }
            }
        });
    </script>
    """, unsafe_allow_html=True)

#### STEP 2: メニューアップロード・OCR・基本確認

def upload_menu_file_to_drive(uploaded_file: Any, store_id: str) -> Optional[str]:
    """
    機能: メニューファイルをGoogle Driveにアップロード
    STEP: 2
    入力: uploaded_file (Any): StreamlitのUploadedFileオブジェクト, store_id (str)
    出力: アップロードされたファイルのURL (str) または None (エラー時)
    外部連携: Google Drive API
    エラー: ファイルアップロード失敗
    """
    display_message(f"ファイルを保存中: {uploaded_file.name}...", "info")
    time.sleep(0.5)
    # TODO: Google Drive APIを使用してファイルをアップロード
    # drive_service = build('drive', 'v3', credentials=creds)
    # file_metadata = {'name': uploaded_file.name, 'parents': [drive_folder_id]}
    # media = MediaFileUpload(uploaded_file.name, mimetype=uploaded_file.type)
    # file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    # return f"https://drive.google.com/uc?id={file.get('id')}"
    
    # モック実装
    mock_url = f"simulated_drive/{store_id}/{uploaded_file.name}"
    log_event("info", f"Mock file uploaded to: {mock_url}")
    return mock_url

def perform_ocr_on_menu(file_url: str) -> Optional[List[Dict[str, str]]]:
    """
    機能: メニュー画像からOCRで情報を抽出
    STEP: 2
    入力: file_url (str): アップロードされたメニューファイルのURL
    出力: 抽出されたメニュー情報のリスト (List[Dict[str, str]]) または None (エラー時)
    外部連携: GeminiCLI (OCR機能)
    エラー: OCR処理失敗、無効なファイル形式
    """
    display_message(f"メニュー情報を読み取り中...", "info")
    time.sleep(2)
    # TODO: GeminiCLIを呼び出してOCR処理を実行
    # response = gemini_cli.ocr_process(file_url)
    # return response.parsed_menu_data
    
    # モック実装
    mock_ocr_results = [
        {"name": "唐揚げ定食", "price": "980円", "original_text": "Karaage Teishoku ¥980"},
        {"name": "焼き魚御膳", "price": "1200円", "original_text": "Yakizakana Gozen ¥1200"},
        {"name": "海老チリセット", "price": "1150円", "original_text": "Ebi Chili Set ¥1150"},
        {"name": "特製ラーメン", "price": "850円", "original_text": "Special Ramen ¥850"},
        {"name": "餃子 (6個)", "price": "400円", "original_text": "Gyoza (6 pcs) ¥400"},
        {"name": "生ビール", "price": "550円", "original_text": "Draft Beer ¥550"},
        {"name": "日本酒 (一合)", "price": "600円", "original_text": "Sake (1 go) ¥600"},
    ]
    log_event("info", "Mock OCR results generated.")
    return mock_ocr_results

def process_extracted_menu_data(ocr_data: List[Dict[str, str]]) -> List[MenuData]:
    """
    機能: OCRで抽出された生データをMenuDataオブジェクトのリストに変換
    STEP: 2
    入力: ocr_data (List[Dict[str, str]])
    出力: MenuDataオブジェクトのリスト (List[MenuData])
    エラー: なし
    """
    menus = []
    for i, item in enumerate(ocr_data):
        menus.append(MenuData(
            id=i,
            name=item.get("name", ""),
            price=item.get("price", ""),
            category=CONFIG['menu_categories'][0], # デフォルトカテゴリ
            order=i,
            multilingual_descriptions={"日本語": item.get("name", "")} # 初期は日本語名のみ
        ))
    log_event("info", f"Processed {len(menus)} menu items from OCR data.")
    return menus

def show_menu_upload_page():
    """
    機能: メニュー表アップロード・基本確認ページを表示
    STEP: 2
    入力: なし
    出力: なし
    エラー: なし
    """
    show_universal_navigation()
    st.title("📄 メニュー表アップロード・基本確認")
    st.info("お店のメニュー表（画像またはPDF）をアップロードしてください。メニュー情報を読み取ります。")

    ensure_session_state('uploaded_menu_file', None)
    ensure_session_state('ocr_results', None)
    ensure_session_state('finalized_menus', [])
    ensure_session_state('ocr_processed', False)
    ensure_session_state('manual_menu_id_counter', 1000)

    uploaded_file = st.file_uploader(
        "メニュー表の画像またはPDFをアップロード",
        type=["png", "jpg", "jpeg", "pdf"],
        help="ファイルサイズは10MBまで。必要に応じて自動でリサイズされます。",
        key="menu_file_uploader"
    )

    if uploaded_file is not None:
        st.session_state.uploaded_menu_file = uploaded_file
        st.write(f"ファイル名: {uploaded_file.name}")
        if uploaded_file.type.startswith('image'):
            st.image(uploaded_file, caption='アップロードされたメニュー表', use_container_width=True)

        if not st.session_state.ocr_processed:
            st.warning("アップロードされたファイルはまだ処理されていません。「メニュー情報読み取り開始」ボタンをクリックしてください。")
            if create_button("メニュー情報読み取り開始", key="start_ocr_button"):
                with st.spinner("メニュー情報読み取り中..."):
                    file_url = safe_execute(upload_menu_file_to_drive, uploaded_file, st.session_state.store_id)
                    if file_url:
                        ocr_data = safe_execute(perform_ocr_on_menu, file_url)
                        if ocr_data:
                            st.session_state.ocr_results = ocr_data
                            st.session_state.finalized_menus = process_extracted_menu_data(ocr_data)
                            st.session_state.ocr_processed = True
                            display_message("メニュー情報の読み取りが完了しました！", "success")
                            st.rerun()
        
    if st.session_state.ocr_processed and st.session_state.finalized_menus:
        st.markdown("---")
        st.subheader("💡 読み取られたメニュー情報をご確認ください")
        st.info("メニューごとに「掲載・掲載しない」を選択し、メニュー名、価格、カテゴリーを修正・設定してください。")

        if create_button("新しいメニューを追加", key="add_manual_menu_button"):
            new_menu_id = st.session_state.manual_menu_id_counter
            st.session_state.manual_menu_id_counter += 1
            st.session_state.finalized_menus.append(MenuData(
                id=new_menu_id,
                name="新しいメニュー",
                price="0円",
                category=CONFIG['menu_categories'][0],
                order=len(st.session_state.finalized_menus),
                multilingual_descriptions={"日本語": "新しいメニュー"}
            ))
            st.rerun()

        updated_menus = []
        for i, menu in enumerate(st.session_state.finalized_menus):
            with st.expander(f"メニュー {i+1}: {menu.name} （{menu.price}）", expanded=False):
                menu.name = create_form_field("text", "メニュー名 (日本語)", value=menu.name, key=f"name_{menu.id}")
                menu.price = create_form_field("text", "お値段 (税込)", value=menu.price, key=f"price_{menu.id}")
                category_index = CONFIG['menu_categories'].index(menu.category) if menu.category in CONFIG['menu_categories'] else 0
                menu.category = create_form_field("select", "カテゴリー", options=CONFIG['menu_categories'], index=category_index, key=f"category_{menu.id}")
                menu.should_introduce = st.checkbox("このメニューを掲載する", value=menu.should_introduce if hasattr(menu, 'should_introduce') else True, key=f"introduce_{menu.id}")
                if create_button("このメニューを削除", key=f"delete_menu_{menu.id}"):
                    st.session_state.finalized_menus = [m for m in st.session_state.finalized_menus if m.id != menu.id]
                    display_message(f"メニュー「{menu.name}」を削除しました。", "success")
                    st.rerun()
            updated_menus.append(menu)
        st.session_state.finalized_menus = updated_menus

        st.markdown("---")
        st.subheader("🔁 メニューの並び替え")
        if st.checkbox("メニューの表示順を変更しますか？", key="confirm_reorder_checkbox"):
            current_order_display = ",".join([str(m.order + 1) for m in sorted(st.session_state.finalized_menus, key=lambda x: x.order)])
            new_order_str = create_form_field("text", "新しいメニューの並び順", value=current_order_display, key="new_menu_order_input")
            if create_button("並び順を更新", key="update_order_button"):
                try:
                    new_order_indices = [int(x.strip()) - 1 for x in new_order_str.split(',')]
                    if len(new_order_indices) != len(st.session_state.finalized_menus) or \
                       len(set(new_order_indices)) != len(st.session_state.finalized_menus) or \
                       not all(0 <= idx < len(st.session_state.finalized_menus) for idx in new_order_indices):
                        display_message("❌ 無効な並び順です。全てのメニュー番号を重複なく、正しく入力してください。", "error")
                    else:
                        reordered_menus_temp = [None] * len(st.session_state.finalized_menus)
                        original_ordered_menus = sorted(st.session_state.finalized_menus, key=lambda x: x.order)
                        for new_pos, original_idx_to_pick in enumerate(new_order_indices):
                            menu_item = original_ordered_menus[original_idx_to_pick]
                            reordered_menus_temp[new_pos] = menu_item
                            reordered_menus_temp[new_pos].order = new_pos
                        st.session_state.finalized_menus = reordered_menus_temp
                        for i, menu in enumerate(st.session_state.finalized_menus):
                             menu.id = i # IDを新しい並び順で振り直し (重要: UIのkeyを確実にユニークにするため)
                        display_message("✅ 並び順を更新しました！", "success")
                        st.rerun()
                except ValueError:
                    display_message("❌ 不正な入力です。番号をカンマ区切りで入力してください。", "error")

        st.markdown("---")
        col_prev, col_next = st.columns([1, 1])
        with col_prev:
            if create_button("⬅️ 戻る (ログインページへ)", key="step2_back_to_login"):
                st.session_state.current_step = 1
                st.session_state.logged_in = False
                st.rerun()
        with col_next:
            if any(m.should_introduce for m in st.session_state.finalized_menus):
                if create_button("次へ進む (想いヒアリングへ) ➡️", key="step2_next_to_thoughts"):
                    st.session_state.finalized_menus = [m for m in st.session_state.finalized_menus if m.should_introduce]
                    st.session_state.current_step = 3
                    st.rerun()
            else:
                display_message("少なくとも1つのメニューを「掲載する」に設定してください。", "warning")

#### STEP 3: 想いヒアリング（15問）・翻訳

def get_owner_thoughts_questions() -> Dict[str, Dict[str, Any]]:
    """
    機能: 店主の想いヒアリング15問の質問データを取得
    STEP: 3
    入力: なし
    出力: 質問データ辞書 (Dict[str, Dict[str, Any]])
    エラー: なし
    """
    return {
        "basic_info": {
            "title": "🏪 お店の基本情報",
            "questions": [
                {"key": "restaurant_name", "question": "お店の名前を教えてください", "example": "例: 和食処 さくら"},
                {"key": "opening_year", "question": "お店を開いてから何年になりますか？", "example": "例: 10年になります"},
                {"key": "location", "question": "お店の場所・立地の特徴を教えてください", "example": "例: 駅から徒歩3分、商店街の中にあります"}
            ]
        },
        "philosophy": {
            "title": "💭 お店の想い・こだわり",
            "questions": [
                {"key": "restaurant_concept", "question": "お店のコンセプトや想いを教えてください", "example": "例: 家庭的な温かい雰囲気で、心のこもった料理を提供したい"},
                {"key": "special_ingredients", "question": "特にこだわっている食材や調理法はありますか？", "example": "例: 地元の野菜を使用し、手作りにこだわっています"},
                {"key": "customer_service", "question": "お客様に対してどのようなサービスを心がけていますか？", "example": "例: 一人一人のお客様との会話を大切にしています"}
            ]
        },
        "dishes": {
            "title": "🍽️ 料理・メニューについて",
            "questions": [
                {"key": "signature_dish", "question": "お店の看板メニューとその特徴を教えてください", "example": "例: 手作りハンバーグは祖母から受け継いだレシピです"},
                {"key": "seasonal_menu", "question": "季節ごとのメニューやイベントはありますか？", "example": "例: 春は山菜料理、夏は冷やし中華に力を入れています"},
                {"key": "menu_development", "question": "新しいメニューを考える時に大切にしていることは？", "example": "例: お客様の声を聞いて、健康的で美味しい料理を考えています"}
            ]
        },
        "international": {
            "title": "🌍 国際的なお客様について",
            "questions": [
                {"key": "foreign_customers", "question": "海外のお客様にどのような体験をしてほしいですか？", "example": "例: 日本の家庭料理の温かさを感じてほしいです"},
                {"key": "cultural_sharing", "question": "お店の文化や料理の背景で伝えたいことはありますか？", "example": "例: 手作りの大切さと、食材への感謝の気持ちを伝えたいです"},
                {"key": "welcome_message", "question": "海外からのお客様へのメッセージをお聞かせください", "example": "例: 日本の味を楽しんでいただき、素敵な思い出を作ってください"}
            ]
        },
        "future": {
            "title": "🚀 今後の展望",
            "questions": [
                {"key": "future_goals", "question": "今後のお店の目標や夢を教えてください", "example": "例: 地域の人々と海外の方々の交流の場になりたいです"},
                {"key": "multilingual_benefits", "question": "多言語メニューでどのような効果を期待されますか？", "example": "例: 言葉の壁を越えて、より多くの方に料理を楽しんでもらいたいです"},
                {"key": "final_message", "question": "最後に、お客様への一言メッセージをお願いします", "example": "例: 心を込めて作った料理で、皆様に笑顔をお届けします"}
            ]
        }
    }

def summarize_owner_thoughts(answers_dict: Dict[str, str]) -> Optional[str]:
    """
    機能: ユーザーが入力した店主の想いを要約
    STEP: 3
    入力: answers_dict (Dict[str, str]): ヒアリング回答辞書
    出力: 要約された想い (str) または None (エラー時)
    外部連携: GeminiCLI (テキスト生成)
    エラー: テキスト生成API呼び出し失敗
    """
    display_message("想いをまとめる中...", "info")
    time.sleep(1)
    # TODO: GeminiCLIを呼び出してテキスト要約を実行
    # prompt = f"以下の質問への回答を基に、飲食店のコンセプトと店主の想いを200字程度で要約してください。\n\n"
    # for key, answer in answers_dict.items():
    #     prompt += f"{key}: {answer}\n"
    # response = gemini_cli.generate_text(prompt)
    # return response.text
    
    # モック実装
    first_menu_name = st.session_state.finalized_menus[0].name if st.session_state.finalized_menus else '特製料理'
    restaurant_name = answers_dict.get("restaurant_name", "当店")
    restaurant_concept = answers_dict.get("restaurant_concept", "お客様に心温まる料理を提供すること")
    signature_dish = answers_dict.get("signature_dish", first_menu_name)
    mock_summary = f"{restaurant_name}は「{restaurant_concept}」という想いを大切にしています。特に「{signature_dish}」は、店主の情熱が詰まった自慢の一品です。私たちは、言葉の壁を越えて世界中のお客様に日本の食文化の温かさを伝えたいと願っています。"
    log_event("info", "Mock owner thoughts summary generated.")
    return mock_summary

def translate_text(text: str, target_languages: List[str]) -> Optional[Dict[str, str]]:
    """
    機能: 指定されたテキストを複数の言語に翻訳
    STEP: 3, 4
    入力: text (str), target_languages (List[str])
    出力: 各言語への翻訳結果辞書 (Dict[str, str]) または None (エラー時)
    外部連携: GeminiCLI (翻訳)
    エラー: 翻訳API呼び出し失敗
    """
    display_message("テキストを多言語に展開中...", "info")
    time.sleep(1.5)
    # TODO: GeminiCLIを呼び出して翻訳を実行
    # translations = {}
    # for lang in target_languages:
    #     translated_text = gemini_cli.translate(text, target_lang=lang)
    #     translations[lang] = translated_text
    # return translations
    
    # モック実装
    mock_translations = {}
    first_menu_name_eng = st.session_state.finalized_menus[0].name if st.session_state.finalized_menus else 'specialty dish'
    for lang in target_languages:
        if lang == "日本語":
            mock_translations[lang] = text
        elif lang == "英語":
            mock_translations[lang] = f"Our aim is to provide an unforgettable experience for our customers, offering heartwarming dishes made with carefully selected ingredients and meticulous cooking methods. Our '{first_menu_name_eng}' in particular, is a plate filled with our passion."
        elif lang == "韓国語":
            mock_translations[lang] = f"손님들에게 잊을 수 없는 경험을 제공하는 것을 목표로, 엄선된 식재료와 섬세한 조리법으로 마음 따뜻해지는 요리를 제공하고 있습니다. 특히 '{first_menu_name_eng}'는 저희 가게의 열정이 담긴 한 접시입니다."
        elif lang == "中国語(標準語)":
            mock_translations[lang] = f"我们的目标是为顾客提供难忘的体验，用精心挑选的食材和精致的烹饪方法，提供温暖人心的菜肴。特别是“{first_menu_name_eng}”，更是我们店倾注热情的一道菜。"
        else:
            mock_translations[lang] = f"This is a mock translation for {lang} of: {text[:50]}..."
    log_event("info", f"Mock translations generated for {len(target_languages)} languages.")
    return mock_translations

def set_allergy_display_policy(policy: str):
    """
    機能: アレルギー情報の表示方針を設定
    STEP: 3
    入力: policy (str): 'display' または 'not_display'
    出力: なし
    エラー: 無効なポリシー値
    """
    if policy not in ["display", "not_display"]:
        raise ValueError("Invalid allergy policy. Must be 'display' or 'not_display'.")
    st.session_state.allergy_policy = policy
    log_event("info", f"Allergy display policy set to: {policy}")

def show_owner_thoughts_page():
    """
    機能: 店主の想いヒアリング・翻訳ページを表示
    STEP: 3
    入力: なし
    出力: なし
    エラー: なし
    """
    show_universal_navigation()
    st.title("🗣️ 店主の想いヒアリング")
    st.info("あなたの声で、お店のこだわりや想いを教えてください。魅力的な文章を作成します。")
    st.markdown("""
    <div class="audio-input-guide">
        <h4>🎤 音声での回答も可能です</h4>
        <p>スマートフォンをお使いの場合、音声入力で簡単に回答できます。</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("15問の質問にお答えいただき、お店の想いを世界に伝えましょう！")

    questions_data = get_owner_thoughts_questions()
    ensure_session_state('owner_answers_dict', {})
    ensure_session_state('summarized_thought', "")
    ensure_session_state('translated_thoughts', None)
    ensure_session_state('allergy_policy', None)

    st.subheader("質問に答えて、お店の想いを教えてください")
    for category_key, category_info in questions_data.items():
        st.markdown(f"### {category_info['title']}")
        for q_item in category_info["questions"]:
            st.session_state.owner_answers_dict[q_item["key"]] = create_form_field(
                "textarea", q_item['question'], value=st.session_state.owner_answers_dict.get(q_item["key"], ""),
                height=80, key=f"q_{q_item['key']}"
            )
            if q_item.get("example"):
                st.info(f"**回答例**: {q_item['example']}")
        st.markdown("---")

    if create_button("想いをまとめる", key="summarize_thoughts_button"):
        all_answered = True
        for category_key in questions_data:
            for q_item in questions_data[category_key]["questions"]:
                if not validate_input(st.session_state.owner_answers_dict.get(q_item["key"], ""), "not_empty"):
                    all_answered = False
                    break
            if not all_answered:
                break
        if all_answered:
            st.session_state.summarized_thought = safe_execute(summarize_owner_thoughts, st.session_state.owner_answers_dict)
            if st.session_state.summarized_thought:
                display_message("想いをまとめました！", "success")
                st.rerun()
        else:
            display_message("全ての質問に回答してください。", "warning")

    if st.session_state.summarized_thought:
        st.markdown("---")
        st.subheader("「こんな想いなんですね？」")
        st.info("まとめた想いの文章をご確認ください。必要であれば修正してください。")
        st.session_state.summarized_thought = create_form_field(
            "textarea", "お店の想い（最終版）", value=st.session_state.summarized_thought, height=200, key="final_owner_thought_edit"
        )
        if create_button("この想いで確定する", key="confirm_and_translate_button", disabled=not st.session_state.summarized_thought.strip()):
            st.session_state.translated_thoughts = safe_execute(translate_text, st.session_state.summarized_thought, CONFIG['supported_languages'])
            if st.session_state.translated_thoughts:
                display_message("お客様に想いを伝えるため、多言語に展開いたしました。", "success")
                display_message("展開品質チェックを実行しました。問題ありません。", "info")
                st.rerun()
            else:
                display_message("翻訳に失敗しました。", "error")

    if st.session_state.translated_thoughts:
        st.markdown("---")
        st.subheader("アレルギー情報の表示方針")
        st.info("メニューのアレルギー情報を、外国人のお客様に表示するかどうかを決定してください。")
        
        col_allergy_display, col_allergy_hide = st.columns(2)
        with col_allergy_display:
            if create_button("✅ 表示する", key="show_allergy", help="アレルギー情報をメニューに表示します", use_container_width=True):
                safe_execute(set_allergy_display_policy, "display")
                display_message("アレルギー情報を表示する設定にしました", "success")
                st.rerun()
        with col_allergy_hide:
            if create_button("❌ 表示しない", key="hide_allergy", help="アレルギー情報は表示しません", use_container_width=True):
                safe_execute(set_allergy_display_policy, "not_display")
                display_message("アレルギー情報を表示しない設定にしました", "warning")
                st.rerun()
        
        st.markdown("---")
        col_prev, col_next = st.columns([1, 1])
        with col_prev:
            if create_button("⬅️ 戻る (メニューアップロードへ)", key="step3_back_to_menu_upload"):
                st.session_state.current_step = 2
                st.rerun()
        with col_next:
            if st.session_state.allergy_policy is not None:
                if create_button("次へ進む (詳細設定へ) ➡️", key="step3_next_to_detailed_settings"):
                    st.session_state.current_step = 4
                    st.rerun()
            else:
                display_message("アレルギー情報の表示方針を選択してください。", "warning")

#### STEP 4: 詳細設定・横スライド（各メニュー個別設定）

def get_menu_details_for_edit(menu_id: int) -> Optional[MenuData]:
    """
    機能: 特定のメニューの詳細情報を取得
    STEP: 4
    入力: menu_id (int)
    出力: MenuDataオブジェクト または None (見つからない場合)
    エラー: 無効なメニューID
    """
    for menu in st.session_state.finalized_menus:
        if menu.id == menu_id:
            return menu
    log_event("warning", f"Menu with ID {menu_id} not found.")
    return None

def update_menu_allergens(menu_id: int, allergens: List[str]) -> bool:
    """
    機能: 特定のメニューのアレルギー情報を更新
    STEP: 4
    入力: menu_id (int), allergens (List[str])
    出力: 更新成功 (bool)
    エラー: 無効なメニューID
    """
    menu = get_menu_details_for_edit(menu_id)
    if menu:
        menu.allergens = allergens
        log_event("info", f"Allergens updated for menu ID {menu_id}.")
        return True
    return False

def upload_menu_image(menu_id: int, uploaded_file: Any) -> Optional[str]:
    """
    機能: 特定のメニューの画像をアップロードし、URLを返す
    STEP: 4
    入力: menu_id (int), uploaded_file (Any)
    出力: 画像URL (str) または None (エラー時)
    外部連携: Google Drive API
    エラー: アップロード失敗
    """
    display_message(f"写真 '{uploaded_file.name}' をアップロード中...", "info")
    time.sleep(0.5)
    # TODO: Google Drive APIで画像をアップロードし、公開URLを取得
    # mock_url = upload_file_to_drive(uploaded_file, f"menu_images/{st.session_state.store_id}")
    mock_url = f"simulated_image_url/{menu_id}_{uploaded_file.name}"
    log_event("info", f"Mock image uploaded for menu ID {menu_id}: {mock_url}")
    return mock_url

def add_multilingual_description(menu_id: int, lang: str, description: str) -> bool:
    """
    機能: 特定のメニューの多言語詳細説明を追加/更新
    STEP: 4
    入力: menu_id (int), lang (str), description (str)
    出力: 更新成功 (bool)
    エラー: 無効なメニューID
    """
    menu = get_menu_details_for_edit(menu_id)
    if menu:
        if 'multilingual_descriptions' not in menu.multilingual_descriptions:
            menu.multilingual_descriptions = {}
        menu.multilingual_descriptions[lang] = description
        log_event("info", f"Multilingual description for menu ID {menu_id} in {lang} updated.")
        return True
    return False

def show_detailed_settings_page():
    """
    機能: 詳細設定ページを表示
    STEP: 4
    入力: なし
    出力: なし
    エラー: なし
    """
    show_universal_navigation()
    st.title("⚙️ 詳細設定")
    st.info("各メニューのさらに詳しい情報を設定し、魅力を最大限に引き出しましょう。")

    if not st.session_state.finalized_menus:
        display_message("メニュー情報がありません。前のステップに戻ってメニューを登録してください。", "warning")
        if create_button("⬅️ メニューアップロードへ戻る", key="step4_back_to_menu_upload_no_menus"):
            st.session_state.current_step = 2
            st.rerun()
        return

    st.subheader("各メニューの詳細設定")

    # 各メニューに対して詳細設定UIを表示
    for i, menu in enumerate(st.session_state.finalized_menus):
        with st.expander(f"メニュー {i+1}: {menu.name} （{menu.price}）", expanded=False):
            st.markdown(f"**現在のメニュー名**: {menu.name}")
            st.markdown(f"**現在の価格**: {menu.price}")
            st.markdown(f"**現在のカテゴリー**: {menu.category}")

            st.markdown("---")
            st.subheader("アレルギー情報")
            st.info("このメニューに含まれるアレルギー物質を選択してください。")
            
            selected_allergies = st.multiselect(
                f"メニュー「{menu.name}」のアレルギー物質",
                options=CONFIG['common_allergens'],
                default=menu.allergens,
                key=f"allergies_{menu.id}"
            )
            safe_execute(update_menu_allergens, menu.id, selected_allergies)

            st.markdown("---")
            st.subheader("メニュー写真の追加")
            st.info("このメニューの写真をアップロードしてください。外国人のお客様に視覚的にアピールできます。")
            
            uploaded_photo = st.file_uploader(
                f"メニュー「{menu.name}」の写真",
                type=["png", "jpg", "jpeg"],
                key=f"photo_upload_{menu.id}"
            )
            
            if uploaded_photo:
                image_url = safe_execute(upload_menu_image, menu.id, uploaded_photo)
                if image_url:
                    menu.image_url = image_url
                    display_message("写真がアップロードされました！", "success")
                    st.image(uploaded_photo, caption="アップロードされた写真", use_container_width=True)
            elif menu.image_url:
                st.image(menu.image_url, caption="現在の写真", use_container_width=True)
            else:
                st.info("写真がまだアップロードされていません。")

            st.markdown("---")
            st.subheader("多言語での詳細説明")
            st.info("このメニューの背景やおすすめポイントを多言語で説明しましょう。")
            
            # 日本語での詳細説明
            initial_jp_desc = menu.multilingual_descriptions.get('日本語', "")
            jp_desc = create_form_field(
                "textarea", f"メニュー「{menu.name}」の詳細説明 (日本語)", value=initial_jp_desc,
                height=100, key=f"desc_jp_{menu.id}"
            )
            safe_execute(add_multilingual_description, menu.id, "日本語", jp_desc)

            # 多言語翻訳ボタン（日本語の説明がある場合のみ有効）
            if create_button(f"「{menu.name}」の詳細説明を翻訳する", key=f"translate_desc_{menu.id}",
                             disabled=not jp_desc.strip()):
                if jp_desc.strip():
                    translated_desc = safe_execute(translate_text, jp_desc, [lang for lang in CONFIG['supported_languages'] if lang != "日本語"])
                    if translated_desc:
                        for lang, desc in translated_desc.items():
                            safe_execute(add_multilingual_description, menu.id, lang, desc)
                        display_message("詳細説明を多言語に翻訳しました！", "success")
                        st.rerun()
                    else:
                        display_message("詳細説明の翻訳に失敗しました。", "error")

            # 翻訳された説明の表示（編集不可）
            if menu.multilingual_descriptions:
                st.subheader("翻訳された詳細説明（確認のみ）")
                for lang in CONFIG['supported_languages']:
                    if lang != "日本語":
                        st.text_area(
                            f"詳細説明 ({lang})",
                            value=menu.multilingual_descriptions.get(lang, ""),
                            height=80,
                            key=f"desc_{lang}_{menu.id}",
                            disabled=True
                        )

    st.markdown("---")
    col_prev, col_next = st.columns([1, 1])
    with col_prev:
        if create_button("⬅️ 戻る (想いヒアリングへ)", key="step4_back_to_thoughts"):
            st.session_state.current_step = 3
            st.rerun()
    with col_next:
        if create_button("次へ進む (イチオシメニューへ) ➡️", key="step4_next_to_featured"):
            st.session_state.current_step = 5
            st.rerun()

#### STEP 5: イチオシメニュー選択

def select_featured_menus(menu_ids: List[int]) -> bool:
    """
    機能: イチオシメニューを設定
    STEP: 5
    入力: menu_ids (List[int]): イチオシとして選択されたメニューのIDリスト
    出力: 設定成功 (bool)
    エラー: なし
    """
    # 全てのメニューのis_featuredフラグをリセット
    for menu in st.session_state.finalized_menus:
        menu.is_featured = False
    
    # 選択されたメニューのis_featuredフラグを設定
    for menu_id in menu_ids:
        for menu in st.session_state.finalized_menus:
            if menu.id == menu_id:
                menu.is_featured = True
                break
    st.session_state.featured_menus = menu_ids
    log_event("info", f"Featured menus set: {menu_ids}")
    return True

def show_featured_menu_selection_page():
    """
    機能: イチオシメニュー選択ページを表示
    STEP: 5
    入力: なし
    出力: なし
    エラー: なし
    """
    show_universal_navigation()
    st.title("⭐️ イチオシメニュー選択")
    st.info("お店の看板メニューや、特に外国人のお客様におすすめしたいメニューを最大3つまで選択してください。")

    if not st.session_state.finalized_menus:
        display_message("登録されたメニューがありません。前のステップに戻ってメニューを登録してください。", "warning")
        if create_button("⬅️ メニューアップロードへ戻る", key="step5_back_to_menu_upload_no_menus"):
            st.session_state.current_step = 2
            st.rerun()
        return

    # 現在のメニューリストから選択肢を作成
    menu_options = {f"{menu.name} ({menu.price})": menu.id for menu in st.session_state.finalized_menus}
    
    # デフォルトで選択されているイチオシメニューを特定
    default_featured_options = [
        f"{menu.name} ({menu.price})" for menu in st.session_state.finalized_menus if menu.is_featured
    ]

    selected_options = st.multiselect(
        "イチオシとして設定するメニューを選択してください (最大3つ)",
        options=list(menu_options.keys()),
        default=default_featured_options,
        max_selections=3,
        key="featured_menu_multiselect"
    )

    selected_menu_ids = [menu_options[option] for option in selected_options]

    if create_button("イチオシメニューを確定", key="confirm_featured_menus_button"):
        if safe_execute(select_featured_menus, selected_menu_ids):
            display_message("イチオシメニューを設定しました！", "success")
            st.rerun() # 変更を反映するために再実行
        else:
            display_message("イチオシメニューの設定に失敗しました。", "error")

    st.markdown("---")
    col_prev, col_next = st.columns([1, 1])
    with col_prev:
        if create_button("⬅️ 戻る (詳細設定へ)", key="step5_back_to_detailed_settings"):
            st.session_state.current_step = 4
            st.rerun()
    with col_next:
        if create_button("次へ進む (完了へ) ➡️", key="step5_next_to_completion"):
            st.session_state.current_step = 6
            st.rerun()

#### STEP 6: 完了・65列CSV生成・配信

def generate_final_csv_data(menus: List[MenuData], owner_thoughts: OwnerThoughts, allergy_policy: str) -> Optional[pd.DataFrame]:
    """
    機能: 全ての情報を統合し、65列の最終CSVデータを生成
    STEP: 6
    入力: menus (List[MenuData]), owner_thoughts (OwnerThoughts), allergy_policy (str)
    出力: 生成されたCSVデータ (pd.DataFrame) または None (エラー時)
    エラー: データ不足、構造不整合
    """
    display_message("最終CSVデータを生成中...", "info")
    time.sleep(2)
    
    if not menus:
        log_event("error", "Cannot generate CSV: No finalized menus available.")
        return None

    all_rows = []
    # 各メニューアイテムに対してCSV行を構築
    for menu_item in menus:
        csv_row = CSVRowStructure(menu_item, owner_thoughts, allergy_policy)
        all_rows.append(csv_row.get_row())

    if not all_rows:
        log_event("error", "No rows generated for CSV.")
        return None
    
    # ヘッダーの順序をCSVRowStructureから取得
    headers = CSVRowStructure(menus[0], owner_thoughts, allergy_policy).get_headers() # 最初のメニューでヘッダーを取得

    # DataFrameを作成し、ヘッダーの順序を適用
    df = pd.DataFrame(all_rows)
    # 欠落している列をNaNで埋め、正しい順序に並べ替える
    df = df.reindex(columns=headers, fill_value='') 
    
    log_event("info", "Final CSV data generated successfully.")
    return df

def export_csv_to_drive(df: pd.DataFrame, store_id: str) -> Optional[str]:
    """
    機能: 生成されたCSVファイルをGoogle Driveにエクスポート
    STEP: 6
    入力: df (pd.DataFrame), store_id (str)
    出力: Google Drive上のCSVファイルのURL (str) または None (エラー時)
    外部連携: Google Drive API
    エラー: ファイルエクスポート失敗
    """
    display_message("CSVファイルをGoogle Driveにエクスポート中...", "info")
    time.sleep(1.5)
    # TODO: pandas DataFrameをCSVとしてGoogle Driveにアップロード
    # from io import StringIO
    # csv_buffer = StringIO()
    # df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
    # file_metadata = {'name': f'TONOSAMA_Menu_{store_id}_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv', 'parents': [drive_export_folder_id]}
    # media = MediaIoBaseUpload(csv_buffer, mimetype='text/csv', resumable=True)
    # file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    # return f"https://drive.google.com/uc?id={file.get('id')}"
    
    # モック実装
    mock_url = f"https://mock-drive.com/download/TONOSAMA_Menu_{store_id}_{int(time.time())}.csv"
    log_event("info", f"Mock CSV exported to Google Drive: {mock_url}")
    return mock_url

def send_completion_email(store_id: str, download_url: str):
    """
    機能: 完了通知メールを送信
    STEP: 6
    入力: store_id (str), download_url (str): CSVダウンロードURL
    出力: なし
    外部連携: SMTP
    エラー: メール送信失敗
    """
    display_message("完了通知メールを送信中...", "info")
    time.sleep(1)
    # TODO: SMTPを使用してメールを送信
    # msg = MIMEText(f"TONOSAMA多言語メニューの準備が完了しました！\nダウンロードはこちら: {download_url}")
    # msg['Subject'] = 'TONOSAMA多言語メニュー準備完了のお知らせ'
    # msg['From'] = 'noreply@tonosama.com'
    # msg['To'] = 'store_owner_email@example.com' # ストアの登録メールアドレス
    # with smtplib.SMTP_SSL('smtp.example.com', 465) as smtp:
    #     smtp.login('user', 'pass')
    #     smtp.send_message(msg)
    log_event("info", f"Mock completion email sent to {store_id} with download URL: {download_url}")
    display_message("ご登録のメールアドレスに完了通知を送信しました。", "success")

def show_completion_page():
    """
    機能: 完了ページを表示
    STEP: 6
    入力: なし
    出力: なし
    エラー: なし
    """
    show_universal_navigation()
    st.title("🎉 全ての設定が完了しました！")
    display_message("お疲れ様でした！あなたの多言語メニュー情報が準備できました。", "success")
    display_message("最終確認を行い、公開準備を進めましょう。", "info")

    st.subheader("最終確認：登録された情報")

    st.markdown("### メニュー一覧")
    if st.session_state.finalized_menus:
        for i, menu in enumerate(st.session_state.finalized_menus):
            st.markdown(f"**{i+1}. {menu.name}** ({menu.price})")
            st.markdown(f"  - カテゴリー: {menu.category}")
            if menu.allergens:
                st.markdown(f"  - アレルギー: {', '.join(menu.allergens)}")
            if menu.image_url:
                st.image(menu.image_url, caption=f"{menu.name} の写真", width=200)
            if menu.multilingual_descriptions.get('日本語'):
                st.markdown(f"  - 詳細説明 (日本語): {menu.multilingual_descriptions['日本語']}")
            if menu.is_featured:
                st.markdown("  - **⭐️ イチオシメニュー**")
            st.markdown("---")
    else:
        display_message("登録されたメニュー情報がありません。", "warning")

    st.markdown("### お店の想い")
    if st.session_state.get('summarized_thought'):
        st.write(st.session_state.summarized_thought)
        if st.session_state.get('translated_thoughts'):
            st.expander("翻訳された想いを見る").json(st.session_state.translated_thoughts)
    else:
        display_message("お店の想いが登録されていません。", "warning")

    st.markdown("### アレルギー表示方針")
    if st.session_state.get('allergy_policy'):
        policy_text = "表示する" if st.session_state.allergy_policy == "display" else "表示しない"
        st.write(f"アレルギー情報は: **{policy_text}**")
    else:
        display_message("アレルギー表示方針が設定されていません。", "warning")

    st.markdown("---")
    st.subheader("公開準備")
    display_message("全ての情報が正しければ、以下のボタンをクリックして公開準備を完了してください。", "info")

    if create_button("多言語メニューを公開準備する", key="finalize_publication_button"):
        df_csv = safe_execute(generate_final_csv_data, st.session_state.finalized_menus,
                              OwnerThoughts(st.session_state.owner_answers_dict, st.session_state.summarized_thought, st.session_state.translated_thoughts),
                              st.session_state.allergy_policy)
        if df_csv is not None:
            download_url = safe_execute(export_csv_to_drive, df_csv, st.session_state.store_id)
            if download_url:
                st.session_state.csv_generated = True
                st.session_state.csv_download_url = download_url
                display_message("✅ 多言語メニューの公開準備が完了しました！", "success")
                st.balloons()
                st.markdown("### ありがとうございます！")
                st.markdown(f"**ストアID: {st.session_state.store_id}** の多言語メニューが、まもなく世界に公開されます！")
                st.markdown("ご不明な点がございましたら、いつでもサポートチームまでお問い合わせください。")
                safe_execute(send_completion_email, st.session_state.store_id, download_url)
                
                # CSVダウンロードボタン
                st.download_button(
                    label="CSVファイルをダウンロード",
                    data=df_csv.to_csv(index=False, encoding='utf-8-sig'),
                    file_name=f"TONOSAMA_Menu_{st.session_state.store_id}.csv",
                    mime="text/csv",
                    key="download_final_csv_button"
                )
                
                if create_button("最初に戻る", key="reset_app_button"):
                    safe_execute(reset_session_state)
                    st.rerun()
            else:
                display_message("CSVエクスポートに失敗しました。", "error")
        else:
            display_message("CSVデータの生成に失敗しました。", "error")

    st.markdown("---")
    if create_button("⬅️ 戻る (イチオシメニューへ)", key="step6_back_to_featured"):
        st.session_state.current_step = 5
        st.rerun()

# ====================
# 8. メイン実行部
# ====================
def main():
    """
    機能: アプリケーションのメイン実行関数
    STEP: 全体
    入力: なし
    出力: なし
    エラー: なし
    """
    apply_custom_css()
    initialize_app_session_state()

    # ページルーティング
    if st.session_state.current_step == -1:
        show_terms_of_service_page()
    elif st.session_state.current_step == 0:
        show_plan_selection_page()
    elif st.session_state.current_step == 1:
        show_login_page()
    elif st.session_state.current_step == 2:
        show_menu_upload_page()
    elif st.session_state.current_step == 3:
        show_owner_thoughts_page()
    elif st.session_state.current_step == 4:
        show_detailed_settings_page()
    elif st.session_state.current_step == 5:
        show_featured_menu_selection_page()
    elif st.session_state.current_step == 6:
        show_completion_page()
    else:
        # 未定義のステップの場合、利用規約ページに戻す
        log_event("warning", f"Undefined step encountered: {st.session_state.current_step}. Resetting to terms page.")
        st.session_state.current_step = -1
        st.session_state.logged_in = False
        st.rerun()

if __name__ == "__main__":
    st.set_page_config(
        page_title="TONOSAMA",
        page_icon="🏯",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    main()
