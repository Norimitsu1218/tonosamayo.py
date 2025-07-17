import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import time
import base64
from typing import Dict, List, Optional, Any, Union
import logging
import re

# ====================
# 1. 設定・データ構造（骨子保護）
# ====================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__) # __name__ を使用する
CONFIG = {
    "theme": {
        "primary_color": "#0070f3",
        "secondary_color": "#1a1a1a",
        "accent_color": "#00d4ff",
        "background_color": "#f8fafc",
        "border_radius": "12px"
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
        "日本語", "英語", "韓国語", "中国語", "台湾語", "広東語", "タイ語",
        "フィリピン語", "ベトナム語", "インドネシア語", "スペイン語", "ドイツ語",
        "フランス語", "イタリア語", "ポルトガル語"
    ],
    "menu_categories": ["フード", "コース", "ランチ", "デザート", "ドリンク"]
}

# ====================
# 2. 美しいUI・CSS（tonosama_working.py風）
# ====================
def apply_beautiful_theme():
    """美しいPS5風テーマ適用"""
    st.markdown("""
    <style>
    :root {
        --primary-color: #0070f3;
        --secondary-color: #1a1a1a;
        --accent-color: #00d4ff;
        --background-color: #f8fafc;
        --text-color: #1a1a1a;
        --border-radius: 12px;
    }

    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: var(--text-color);
    }
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: var(--border-radius);
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    .tonosama-header {
        text-align: center;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .category-header {
        background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
        color: white;
        padding: 1rem 2rem;
        border-radius: var(--border-radius);
        margin: 1.5rem 0 1rem 0;
        font-size: 1.2rem;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0, 112, 243, 0.3);
    }
    .question-container {
        background: white;
        border: 2px solid #e1e5e9;
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    .question-container:hover {
        border-color: var(--primary-color);
        box-shadow: 0 5px 20px rgba(0, 112, 243, 0.1);
        transform: translateY(-2px);
    }
    .required-mark {
        color: #e74c3c;
        font-weight: bold;
        margin-left: 0.5rem;
    }
    .example-text {
        background: #f8f9fa;
        border-left: 4px solid var(--accent-color);
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        border-radius: 0 var(--border-radius) var(--border-radius) 0;
        font-style: italic;
        color: #6c757d;
    }
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--accent-color)) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--border-radius) !important;
        padding: 0.75rem 2rem !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 112, 243, 0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0, 112, 243, 0.4) !important;
    }
    .progress-container {
        background: #e9ecef;
        border-radius: 10px;
        padding: 3px;
        margin: 1rem 0;
    }
    .progress-bar {
        background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
        border-radius: 8px;
        height: 20px;
        transition: width 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 0.8rem;
    }
    .stTextArea > div > div > textarea {
        border: 2px solid #e1e5e9 !important;
        border-radius: var(--border-radius) !important;
        transition: all 0.3s ease !important;
    }
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(0, 112, 243, 0.1) !important;
    }
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .fade-in {
        animation: fadeInUp 0.6s ease-out;
    }
    .navigation-bar {
        background-color: #FFFFFF;
        border: 1px solid var(--primary-color);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 30px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
    }
    .nav-step {
        color: var(--text-color);
        font-weight: 500;
        padding: 8px 16px;
        border-radius: 6px;
        transition: all 0.3s ease;
        background-color: #F0F0F0;
        border: 1px solid rgba(0, 0, 0, 0.1);
    }
    .nav-step.active {
        color: var(--text-color);
        font-weight: bold;
        background-color: #FFFFFF;
        border: 1px solid var(--primary-color);
    }
    @media (max-width: 768px) {
        .tonosama-header {
            font-size: 2rem;
        }
        .main-container {
            margin: 0.5rem;
            padding: 1rem;
        }
        .category-header {
            padding: 0.8rem 1rem;
            font-size: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_progress_display(current: int, total: int, label: str = ""):
    """プログレス表示"""
    progress = (current / total) * 100

    st.markdown(f"""<div class="progress-container">    <div class="progress-bar" style="width: {progress}%;">        {label} {current}/{total} ({progress:.0f}%)    </div></div>""", unsafe_allow_html=True)

def show_universal_navigation():
    """ナビゲーションバー表示"""
    steps = ["ログイン", "メニュー", "想い", "詳細設定", "イチオシ", "完了"]
    current = st.session_state.get("current_step", 1)

    nav_html = '<div class="navigation-bar">'
    for i, step in enumerate(steps):
        active_class = "active" if i + 1 == current else ""
        nav_html += f'<span class="nav-step {active_class}">{i+1}. {step}</span>'
    nav_html += '</div>'
    st.markdown(nav_html, unsafe_allow_html=True)

    progress_percentage = (current / len(steps)) * 100 if current >= 1 else 0
    st.markdown(f"""<div class="progress-container">    <div class="progress-bar" style="width: {progress_percentage:.0f}%;"></div></div>""", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:var(--text-color);'>進捗: {progress_percentage:.0f}%</p>", unsafe_allow_html=True)

# ====================
# 3. セッション状態管理（骨子保護）
# ====================
def ensure_session_state(key: str, default_value: Any):
    if key not in st.session_state:
        st.session_state[key] = default_value
        logger.info(f"Session state '{key}' initialized with default value.")

def initialize_app_session_state():
    ensure_session_state("current_step", 1) # ログインから開始
    ensure_session_state("logged_in", False)
    ensure_session_state("store_id", "")
    ensure_session_state("responsible_number", "")
    ensure_session_state("uploaded_menu_file", None)
    ensure_session_state("ocr_results", None)
    ensure_session_state("finalized_menus", [])
    ensure_session_state("ocr_processed", False)
    ensure_session_state("manual_menu_id_counter", 1000)
    ensure_session_state("owner_answers_dict", {})
    ensure_session_state("summarized_thought", "")
    ensure_session_state("translated_thoughts", None)
    ensure_session_state("allergy_policy", None)
    ensure_session_state("featured_menus", [])
    ensure_session_state("csv_generated", False)
    ensure_session_state("csv_download_url", "")
    logger.info("Application session state initialized.")

# ====================
# 4. データ構造（骨子保護）
# ====================
class MenuData:
    def __init__(self, id: int, name: str, price: str, category: str, order: int,
                 image_url: Optional[str] = None,
                 allergens: Optional[List[str]] = None,
                 multilingual_descriptions: Optional[Dict[str, str]] = None,
                 is_featured: bool = False):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.order = order
        self.image_url = image_url if image_url is not None else ""
        self.allergens = allergens if allergens is not None else []
        self.multilingual_descriptions = multilingual_descriptions if multilingual_descriptions is not None else {"日本語": ""}
        self.is_featured = is_featured
        self.should_introduce = True

class OwnerThoughts:
    def __init__(self, answers: Dict[str, str], summary: str = "", translations: Optional[Dict[str, str]] = None):
        self.answers = answers
        self.summary = summary
        self.translations = translations if translations is not None else {}

class CSVRowStructure:
    def __init__(self, menu_item: MenuData, owner_thoughts: OwnerThoughts, allergy_policy: str):
        self.menu_item = menu_item
        self.owner_thoughts = owner_thoughts
        self.allergy_policy = allergy_policy
        self.row_data: Dict[str, Any] = {}
        self._build_row()

    def _build_row(self):
        self.row_data['価格'] = self.menu_item.price
        self.row_data['画像URL'] = self.menu_item.image_url
        self.row_data['カテゴリ'] = self.menu_item.category
        self.row_data['おすすめ'] = "TRUE" if self.menu_item.is_featured else "FALSE"
        self.row_data['並び順'] = self.menu_item.order + 1
        for allergen in CONFIG['common_allergens']:
            col_name = f"アレルギー_{allergen.split(' ')[0]}"
            # アレルギーポリシーが「表示」の場合のみTRUEにする
            self.row_data[col_name] = "TRUE" if allergen in self.menu_item.allergens and self.allergy_policy == "display" else "FALSE"

        # メニュー名と言語別メニュー名/説明
        for lang in CONFIG['supported_languages']:
            menu_name_col = f"メニュー名_{lang}"
            # 日本語はメニュー名、その他は多言語説明の該当言語か日本語メニュー名
            self.row_data[menu_name_col] = self.menu_item.multilingual_descriptions.get(lang, self.menu_item.name if lang == "日本語" else "")
            menu_desc_col = f"メニュー説明_{lang}"
            # 多言語説明がある場合はそちらを優先、なければ日本語メニュー名を代用
            self.row_data[menu_desc_col] = self.menu_item.multilingual_descriptions.get(lang, self.menu_item.name if lang == "日本語" else "")

        # 店主の想い
        for lang in CONFIG['supported_languages']:
            owner_thought_col = f"店主想い_{lang}"
            self.row_data[owner_thought_col] = self.owner_thoughts.translations.get(lang, "")
        self.row_data['備考'] = ""

    def get_row(self) -> Dict[str, Any]:
        return self.row_data

    def get_headers(self) -> List[str]:
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
# 5. 東大レベル翻訳エンジン（新技術）
# ====================
def premium_translate_text(text: str, target_languages: List[str]) -> Optional[Dict[str, str]]:
    """東大レベル翻訳（高品質・店主想いミックス）"""
    st.info("🎓 東大レベル翻訳エンジン実行中...")
    # NOTE: 本番環境ではここにGemini Pro + Claude Sonnetを呼び出すロジックを実装
    time.sleep(2)

    premium_translations = {}
    for lang in target_languages:
        if lang == "日本語":
            premium_translations[lang] = text
        elif lang == "英語":
            premium_translations[lang] = f"[PREMIUM EN] {text[:30]}... - A heartwarming authentic Japanese dining experience crafted with passion and traditional techniques."
        elif lang == "韓国語":
            premium_translations[lang] = f"[PREMIUM KO] {text[:30]}... - 정성과 전통 기법으로 만든 따뜻한 일본 정통 식사 경험을 제공합니다."
        elif lang == "中国語":
            premium_translations[lang] = f"[PREMIUM ZH] {text[:30]}... - 用心意和传统技法制作的温馨正宗日式用餐体验。"
        elif lang == "台湾語":
            premium_translations[lang] = f"[PREMIUM TW] {text[:30]}... - 用心意和傳統技法製作的溫馨正宗日式用餐體驗。"
        elif lang == "広東語":
            premium_translations[lang] = f"[PREMIUM HK] {text[:30]}... - 用心意同傳統技法製作嘅溫馨正宗日式用餐體驗。"
        elif lang == "タイ語":
            premium_translations[lang] = f"[PREMIUM TH] {text[:30]}... - ประสบการณ์การรับประทานอาหารญี่ปุ่นแท้ที่อบอุ่นและสร้างด้วยความใส่ใจ"
        elif lang == "フィリピン語":
            premium_translations[lang] = f"[PREMIUM TL] {text[:30]}... - Isang mainit-puso at tunay na Japanese dining experience na ginawa nang may puso at tradisyonal na pamamaraan."
        elif lang == "ベトナム語":
            premium_translations[lang] = f"[PREMIUM VI] {text[:30]}... - Trải nghiệm ẩm thực Nhật Bản chính thống ấm áp được chế tạo với đam mê và kỹ thuật truyền thống."
        elif lang == "インドネシア語":
            premium_translations[lang] = f"[PREMIUM ID] {text[:30]}... - Pengalaman bersantap Jepang autentik yang hangat yang dibuat dengan passion dan teknik tradisional."
        elif lang == "スペイン語":
            premium_translations[lang] = f"[PREMIUM ES] {text[:30]}... - Una experiencia gastronómica japonesa auténtica y cálida creada con pasión y técnicas tradicionales."
        elif lang == "ドイツ語":
            premium_translations[lang] = f"[PREMIUM DE] {text[:30]}... - Ein herzliches, authentisches japanisches Speiseerlebnis, das mit Leidenschaft und traditionellen Techniken geschaffen wurde."
        elif lang == "フランス語":
            premium_translations[lang] = f"[PREMIUM FR] {text[:30]}... - Une expérience culinaire japonaise authentique et chaleureuse créée avec passion et techniques traditionnelles."
        elif lang == "イタリア語":
            premium_translations[lang] = f"[PREMIUM IT] {text[:30]}... - Un'esperienza culinaria giapponese autentica e calorosa creata con passione e tecniche tradizionali."
        elif lang == "ポルトガル語":
            premium_translations[lang] = f"[PREMIUM PT] {text[:30]}... - Uma experiência gastronômica japonesa autêntica e acolhedora criada com paixão e técnicas tradicionais."
        else:
            premium_translations[lang] = f"[PREMIUM {lang}] {text}"
    logger.info(f"Premium translations generated for {len(target_languages)} languages.")
    return premium_translations

# ====================
# 6. ページ表示関数（骨子保護・UI美化）
# ====================
# STEP 1: シンプルログイン
def authenticate_store_id(store_id: str) -> bool:
    st.info(f"ストアID: {store_id} を確認中...")
    time.sleep(1)
    return store_id == "TONOSAMA001"

def authenticate_responsible_number(responsible_number: str) -> bool:
    st.info(f"責任者ナンバーを確認中...")
    time.sleep(1)
    return responsible_number == "99999"

def show_simple_login_page():
    """シンプル・美しいログインページ"""
    show_universal_navigation()

    st.markdown('<div class="main-container fade-in">', unsafe_allow_html=True)
    st.markdown('<h1 class="tonosama-header">🏯 TONOSAMA</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #6c757d; margin-bottom: 2rem;">東大レベル翻訳システム</h2>', unsafe_allow_html=True)
    st.info("ストアIDと責任者ナンバーを入力してログインしてください")

    col1, col2 = st.columns(2)
    with col1:
        store_id = st.text_input(
            "ストアID",
            placeholder="例: TONOSAMA001",
            key="login_store_id"
        )
    with col2:
        responsible_number = st.text_input(
            "責任者ナンバー",
            type="password",
            placeholder="例: 99999",
            key="login_responsible_number"
        )

    if st.button("🚀 ログイン", type="primary", use_container_width=True):
        if not store_id.strip():
            st.warning("ストアIDを入力してください")
        elif not responsible_number.strip():
            st.warning("責任者ナンバーを入力してください")
        else:
            if authenticate_store_id(store_id) and authenticate_responsible_number(responsible_number):
                st.success("✅ ログイン成功！")
                st.session_state.logged_in = True
                st.session_state.store_id = store_id
                st.session_state.responsible_number = responsible_number
                st.session_state.current_step = 2
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ ログイン情報が正しくありません")
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 2: メニューアップロード（骨子保護）
def upload_menu_file_to_drive(uploaded_file: Any, store_id: str) -> Optional[str]:
    st.info(f"ファイルを保存中: {uploaded_file.name}...")
    time.sleep(1)
    # NOTE: 本番環境ではGoogle Driveなどのストレージにアップロードするロジックを実装
    mock_url = f"simulated_drive/{store_id}/{uploaded_file.name}"
    logger.info(f"Mock file uploaded to: {mock_url}")
    return mock_url

def perform_ocr_on_menu(file_url: str) -> Optional[List[Dict[str, str]]]:
    st.info(f"メニュー情報を読み取り中...")
    # NOTE: 本番環境ではOCRサービス（Google Cloud Visionなど）を呼び出すロジックを実装
    time.sleep(2)

    # モックデータ
    mock_ocr_results = [
        {"name": "唐揚げ定食", "price": "980円", "original_text": "Karaage Teishoku ¥980"},
        {"name": "焼き魚御膳", "price": "1200円", "original_text": "Yakizakana Gozen ¥1200"},
        {"name": "海老チリセット", "price": "1150円", "original_text": "Ebi Chili Set ¥1150"},
        {"name": "特製ラーメン", "price": "850円", "original_text": "Special Ramen ¥850"},
        {"name": "餃子 (6個)", "price": "400円", "original_text": "Gyoza (6 pcs) ¥400"},
        {"name": "生ビール", "price": "550円", "original_text": "Draft Beer ¥550"},
        {"name": "日本酒 (一合)", "price": "600円", "original_text": "Sake (1 go) ¥600"},
    ]
    logger.info("Mock OCR results generated.")
    return mock_ocr_results

def process_extracted_menu_data(ocr_data: List[Dict[str, str]]) -> List[MenuData]:
    menus = []
    for i, item in enumerate(ocr_data):
        # 既存メニューIDとの衝突を避けるため、カウンターを使用
        new_id = st.session_state.manual_menu_id_counter + i
        menus.append(MenuData(
            id=new_id,
            name=item.get("name", ""),
            price=item.get("price", ""),
            category=CONFIG['menu_categories'][0], # デフォルトで最初のカテゴリを設定
            order=i,
            multilingual_descriptions={"日本語": item.get("name", "")}
        ))
    st.session_state.manual_menu_id_counter += len(ocr_data) # カウンターを更新
    logger.info(f"Processed {len(menus)} menu items from OCR data.")
    return menus

def show_menu_upload_page():
    """メニューアップロードページ（骨子保護・UI美化）"""
    show_universal_navigation()

    st.markdown('<div class="main-container fade-in">', unsafe_allow_html=True)
    st.markdown('<h1 class="tonosama-header">📄 メニューアップロード</h1>', unsafe_allow_html=True)
    st.info("お店のメニュー表（画像またはPDF）をアップロードしてください")

    uploaded_file = st.file_uploader(
        "メニュー表の画像またはPDFをアップロード",
        type=["png", "jpg", "jpeg", "pdf"],
        help="ファイルサイズは10MBまで"
    )

    if uploaded_file is not None:
        st.session_state.uploaded_menu_file = uploaded_file
        st.write(f"ファイル名: {uploaded_file.name}")
        if uploaded_file.type.startswith('image'):
            st.image(uploaded_file, caption='アップロードされたメニュー表', use_container_width=True)

        if not st.session_state.ocr_processed:
            if st.button("🔍 メニュー情報読み取り開始", type="primary"):
                with st.spinner("メニュー情報読み取り中..."):
                    file_url = upload_menu_file_to_drive(uploaded_file, st.session_state.store_id)
                    if file_url:
                        ocr_data = perform_ocr_on_menu(file_url)
                        if ocr_data:
                            st.session_state.ocr_results = ocr_data
                            st.session_state.finalized_menus = process_extracted_menu_data(ocr_data)
                            st.session_state.ocr_processed = True
                            st.success("✅ メニュー情報の読み取りが完了しました！")
                            st.rerun()
        else: # OCR処理済みの場合
            st.success("✅ メニュー情報の読み取りが完了しています！以下の情報を確認・編集してください。")


    if st.session_state.ocr_processed and st.session_state.finalized_menus:
        st.markdown("---")
        st.subheader("📝 読み取られたメニュー情報と調整")

        # 新規メニュー追加ボタン
        if st.button("➕ 新規メニューを追加", key="add_new_menu_btn"):
            new_id = st.session_state.manual_menu_id_counter
            st.session_state.manual_menu_id_counter += 1
            st.session_state.finalized_menus.append(MenuData(
                id=new_id,
                name=f"新しいメニュー {new_id - 1000 + 1}", # 1000からのオフセットで表示名を調整
                price="0円",
                category=CONFIG['menu_categories'][0],
                order=len(st.session_state.finalized_menus)
            ))
            st.experimental_rerun() # 新規追加後、画面を更新して表示

        updated_menus = []
        for i, menu in enumerate(st.session_state.finalized_menus):
            with st.expander(f"メニュー {i+1}: {menu.name} （{menu.price}）", expanded=False):
                # 削除ボタン
                if st.button(f"🗑️ メニュー {i+1} を削除", key=f"delete_menu_{menu.id}"):
                    st.session_state.finalized_menus = [m for m in st.session_state.finalized_menus if m.id != menu.id]
                    st.success(f"メニュー '{menu.name}' を削除しました。")
                    st.experimental_rerun() # 削除後、画面を更新

                menu.name = st.text_input("メニュー名", value=menu.name, key=f"name_{menu.id}")
                menu.price = st.text_input("価格", value=menu.price, key=f"price_{menu.id}")
                category_index = CONFIG['menu_categories'].index(menu.category) if menu.category in CONFIG['menu_categories'] else 0
                menu.category = st.selectbox("カテゴリー", CONFIG['menu_categories'], index=category_index, key=f"category_{menu.id}")

                # アレルギー選択（複数選択）
                selected_allergens = st.multiselect(
                    "アレルギー情報（該当するものを選択）",
                    options=CONFIG['common_allergens'],
                    default=menu.allergens,
                    key=f"allergens_{menu.id}"
                )
                menu.allergens = selected_allergens

                # 多言語説明文
                st.subheader(f"多言語説明文（メニュー名_{menu.name}）")
                current_lang_desc = menu.multilingual_descriptions.get("日本語", "")
                menu.multilingual_descriptions["日本語"] = st.text_area("日本語説明文", value=current_lang_desc, key=f"desc_ja_{menu.id}")

                for lang in CONFIG['supported_languages']:
                    if lang == "日本語": continue # 日本語は上で入力済み
                    current_lang_desc = menu.multilingual_descriptions.get(lang, "")
                    menu.multilingual_descriptions[lang] = st.text_area(f"{lang} 説明文", value=current_lang_desc, key=f"desc_{lang}_{menu.id}")

                menu.should_introduce = st.checkbox("このメニューを掲載する", value=menu.should_introduce, key=f"introduce_{menu.id}")
            updated_menus.append(menu)

        st.session_state.finalized_menus = updated_menus # 更新されたメニューリストを保存

        st.markdown("---")
        col_prev, col_next = st.columns([1, 1])
        with col_prev:
            if st.button("⬅️ 戻る", key="step2_back"):
                st.session_state.current_step = 1
                st.rerun()
        with col_next:
            if any(m.should_introduce for m in st.session_state.finalized_menus):
                if st.button("次へ進む ➡️", key="step2_next"):
                    # 掲載するメニューのみをフィルタリング
                    st.session_state.finalized_menus = [m for m in st.session_state.finalized_menus if m.should_introduce]
                    st.session_state.current_step = 3
                    st.rerun()
            else:
                st.warning("少なくとも1つのメニューを「掲載する」に設定してください")
    st.markdown('</div>', unsafe_allow_html=True)


# STEP 3: 15問ヒアリング（骨子保護）
def get_owner_thoughts_questions() -> Dict[str, Dict[str, Any]]:
    """店主の想いを引き出すための15問ヒアリング質問リスト"""
    return {
        "basic_info": {
            "title": "🏪 お店の基本情報",
            "questions": [
                {"key": "restaurant_name", "question": "お店の名前を教えてください", "type": "text_input", "required": True, "placeholder": "例: 和食処 味の匠"},
                {"key": "concept", "question": "お店のコンセプトやこだわりを教えてください", "type": "text_area", "required": True, "placeholder": "例: 旬の食材を活かした、心温まる家庭料理を提供しています。"},
                {"key": "founding_story", "question": "お店を始めたきっかけや創業時の想いがあれば教えてください", "type": "text_area", "required": False, "placeholder": "例: 祖母から受け継いだ味を多くの人に届けたいという思いで開店しました。"},
            ]
        },
        "food_philosophy": {
            "title": "🍳 料理への想い",
            "questions": [
                {"key": "ingredient_commitment", "question": "食材へのこだわりを教えてください", "type": "text_area", "required": True, "placeholder": "例: 地元の契約農家から仕入れる新鮮な野菜と、日本海で獲れたばかりの魚を使用しています。"},
                {"key": "cooking_method", "question": "調理法や隠し味、独自の工夫があれば教えてください", "type": "text_area", "required": False, "placeholder": "例: 出汁は毎朝丁寧にひき、素材の味を最大限に引き出すために薄味を心がけています。"},
                {"key": "signature_dish_story", "question": "看板メニューやおすすめメニューにまつわるエピソードがあれば教えてください", "type": "text_area", "required": False, "placeholder": "例: 定食の味噌汁は、創業以来変わらない秘伝の合わせ味噌で作られています。"},
            ]
        },
        "customer_experience": {
            "title": "🗣️ お客様への想い",
            "questions": [
                {"key": "atmosphere", "question": "お店の雰囲気やお客様にどのように過ごしてほしいかを教えてください", "type": "text_area", "required": True, "placeholder": "例: 木の温もりを感じる落ち着いた空間で、ゆったりと食事を楽しんでいただきたいです。"},
                {"key": "hospitality", "question": "お客様に提供したいおもてなしや体験について教えてください", "type": "text_area", "required": False, "placeholder": "例: お客様一人ひとりの好みに合わせた日本酒のペアリングをご提案しています。"},
                {"key": "target_customer_image", "question": "どんなお客様に来てほしいですか？", "type": "text_input", "required": False, "placeholder": "例: 美味しい和食と日本酒をゆっくりと楽しみたい方。"},
            ]
        },
        "future_vision": {
            "title": "✨ お店の未来",
            "questions": [
                {"key": "future_goals", "question": "お店の今後の目標や夢を教えてください", "type": "text_area", "required": False, "placeholder": "例: 地元の方々に愛されるだけでなく、国内外の観光客にも日本の食文化を発信していきたいです。"},
                {"key": "community_contribution", "question": "地域社会への貢献や取り組みがあれば教えてください", "type": "text_area", "required": False, "placeholder": "例: 地元の食材を使ったメニュー開発を通じて、地域の活性化に貢献しています。"},
            ]
        },
        "other_thoughts": {
            "title": "💡 その他",
            "questions": [
                {"key": "unique_selling_point", "question": "他のお店にはない、独自の魅力や強みは何ですか？", "type": "text_area", "required": False, "placeholder": "例: 旬の食材を使った日替わりメニューは、毎日来ても飽きない工夫をしています。"},
                {"key": "message_to_customers", "question": "お客様へのメッセージがあれば自由に記載してください", "type": "text_area", "required": False, "placeholder": "例: 皆様のご来店を心よりお待ちしております。"},
            ]
        }
    }


def show_owner_thoughts_page():
    """店主の想いヒアリングページ（骨子保護・UI美化）"""
    show_universal_navigation()

    st.markdown('<div class="main-container fade-in">', unsafe_allow_html=True)
    st.markdown('<h1 class="tonosama-header">💬 店主の想いヒアリング</h1>', unsafe_allow_html=True)
    st.info("お店の魅力やこだわりを伝えるために、以下の質問にお答えください。")

    questions_data = get_owner_thoughts_questions()
    all_questions_keys = []
    for category_data in questions_data.values():
        for q in category_data["questions"]:
            all_questions_keys.append(q["key"])

    # 回答を保存するためのディクショナリを初期化
    if "owner_answers_dict" not in st.session_state:
        st.session_state.owner_answers_dict = {key: "" for key in all_questions_keys}

    # 各質問カテゴリを表示
    for category_key, category_data in questions_data.items():
        st.markdown(f'<h3 class="category-header">{category_data["title"]}</h3>', unsafe_allow_html=True)
        for q in category_data["questions"]:
            question_key = q["key"]
            required_mark = '<span class="required-mark">*必須</span>' if q["required"] else ''
            st.markdown(f'<div class="question-container fade-in"><h4>{q["question"]} {required_mark}</h4>', unsafe_allow_html=True)

            current_answer = st.session_state.owner_answers_dict.get(question_key, "")

            if q["type"] == "text_input":
                st.session_state.owner_answers_dict[question_key] = st.text_input(
                    "回答を入力してください",
                    value=current_answer,
                    key=f"q_{question_key}",
                    placeholder=q.get("placeholder", "")
                )
            elif q["type"] == "text_area":
                st.session_state.owner_answers_dict[question_key] = st.text_area(
                    "回答を入力してください",
                    value=current_answer,
                    key=f"q_{question_key}",
                    placeholder=q.get("placeholder", "")
                )
            # 他のタイプ（radio, checkboxなど）が必要な場合はここに追加
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    col_prev, col_next = st.columns([1, 1])
    with col_prev:
        if st.button("⬅️ 戻る", key="step3_back"):
            st.session_state.current_step = 2
            st.rerun()
    with col_next:
        if st.button("次へ進む ➡️", key="step3_next"):
            # 必須項目のチェック
            all_required_filled = True
            for category_data in questions_data.values():
                for q in category_data["questions"]:
                    if q["required"] and not st.session_state.owner_answers_dict.get(q["key"], "").strip():
                        all_required_filled = False
                        break
                if not all_required_filled:
                    break

            if all_required_filled:
                st.success("✅ 店主の想いの入力が完了しました！")
                st.session_state.current_step = 4
                st.rerun()
            else:
                st.error("❌ 必須項目が入力されていません。全て記入してください。")

    st.markdown('</div>', unsafe_allow_html=True)


# STEP 4: 詳細設定（骨子保護）
def show_detail_settings_page():
    """詳細設定ページ（アレルギーポリシーなど）"""
    show_universal_navigation()

    st.markdown('<div class="main-container fade-in">', unsafe_allow_html=True)
    st.markdown('<h1 class="tonosama-header">⚙️ 詳細設定</h1>', unsafe_allow_html=True)
    st.info("アレルギー情報に関する表示ポリシーを設定してください。")

    allergy_policy_options = {
        "display": "メニューごとにアレルギー情報を表示する",
        "hide": "アレルギー情報は表示しない",
        "disclaimer_only": "アレルギー情報は表示せず、店内の注意書きのみとする"
    }

    current_allergy_policy = st.session_state.get("allergy_policy", "display")
    selected_policy_label = st.radio(
        "アレルギー情報表示ポリシー",
        options=list(allergy_policy_options.values()),
        index=list(allergy_policy_options.keys()).index(current_allergy_policy),
        key="allergy_policy_radio"
    )

    # 選択された表示ラベルからキーを取得し、セッションに保存
    st.session_state.allergy_policy = [k for k, v in allergy_policy_options.items() if v == selected_policy_label][0]

    if st.session_state.allergy_policy == "disclaimer_only":
        st.warning("⚠️ アレルギー情報を表示しない場合、お客様への適切な情報提供にご注意ください。")
        st.info("店内でのアレルギー対応について、具体的にどのように案内されますか？（例: アレルギーをお持ちのお客様はスタッフまでお声がけください、など）")
        st.session_state.owner_answers_dict["allergy_disclaimer_text"] = st.text_area(
            "店内でのアレルギー対応について",
            value=st.session_state.owner_answers_dict.get("allergy_disclaimer_text", ""),
            key="allergy_disclaimer_text_area",
            placeholder="例: アレルギーをお持ちのお客様は、ご来店時にスタッフまでお申し出ください。可能な限り対応させていただきます。"
        )

    st.markdown("---")
    col_prev, col_next = st.columns([1, 1])
    with col_prev:
        if st.button("⬅️ 戻る", key="step4_back"):
            st.session_state.current_step = 3
            st.rerun()
    with col_next:
        if st.button("次へ進む ➡️", key="step4_next"):
            st.session_state.current_step = 5
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# STEP 5: イチオシメニュー（骨子保護）
def show_featured_menus_page():
    """イチオシメニュー設定ページ"""
    show_universal_navigation()

    st.markdown('<div class="main-container fade-in">', unsafe_allow_html=True)
    st.markdown('<h1 class="tonosama-header">🌟 イチオシメニュー設定</h1>', unsafe_allow_html=True)
    st.info("お店のイチオシメニューを選択し、簡単な説明や画像URLを設定してください。")

    if not st.session_state.finalized_menus:
        st.warning("先にメニューアップロードページでメニューを登録してください。")
        if st.button("メニューアップロードへ戻る"):
            st.session_state.current_step = 2
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # 選択可能なメニューリスト
    menu_options = {menu.name: menu.id for menu in st.session_state.finalized_menus}
    
    # 既存のイチオシメニューのIDをセットとして保持
    current_featured_ids = {m.id for m in st.session_state.featured_menus}

    # Streamlitのmultiselectでイチオシメニューを選択
    selected_menu_names = st.multiselect(
        "イチオシメニューを選択してください（複数選択可）",
        options=list(menu_options.keys()),
        default=[name for name, mid in menu_options.items() if mid in current_featured_ids],
        key="featured_menu_selector"
    )

    # 選択されたメニューに基づいてst.session_state.featured_menusを更新
    new_featured_menus = []
    for name in selected_menu_names:
        menu_id = menu_options[name]
        # 既存のメニューからIDで取得
        selected_menu = next((m for m in st.session_state.finalized_menus if m.id == menu_id), None)
        if selected_menu:
            # 既存のfeatured_menusから取得して情報を引き継ぐ
            existing_featured = next((fm for fm in st.session_state.featured_menus if fm.id == menu_id), None)
            if existing_featured:
                new_featured_menus.append(existing_featured)
            else:
                new_featured_menus.append(selected_menu)
                selected_menu.is_featured = True # 新たにイチオシになったメニューはフラグを立てる

    # 古いイチオシメニューで選択解除されたものがあればis_featuredをFalseに
    for menu in st.session_state.finalized_menus:
        if menu.id in current_featured_ids and menu.id not in {m.id for m in new_featured_menus}:
            menu.is_featured = False

    st.session_state.featured_menus = new_featured_menus # 更新されたイチオシメニューリスト

    if st.session_state.featured_menus:
        st.markdown("---")
        st.subheader("📝 イチオシメニュー詳細設定")
        for i, menu in enumerate(st.session_state.featured_menus):
            with st.expander(f"イチオシメニュー: {menu.name}", expanded=True):
                st.markdown(f"**メニュー名:** {menu.name}")
                st.markdown(f"**価格:** {menu.price}")

                # イチオシ用の画像URL
                menu.image_url = st.text_input(
                    f"イチオシメニュー用画像URL（メニューID: {menu.id}）",
                    value=menu.image_url,
                    key=f"featured_image_url_{menu.id}",
                    placeholder="例: https://example.com/menu_karaage.jpg"
                )
                if menu.image_url:
                    try:
                        st.image(menu.image_url, caption="現在の画像", width=200)
                    except Exception:
                        st.warning("画像URLが無効です。")

                # イチオシメニューに対する多言語説明
                st.subheader("イチオシメニューの説明文")
                for lang in CONFIG['supported_languages']:
                    current_desc = menu.multilingual_descriptions.get(lang, "")
                    menu.multilingual_descriptions[lang] = st.text_area(
                        f"{lang} 説明文",
                        value=current_desc,
                        key=f"featured_desc_{lang}_{menu.id}",
                        placeholder=f"{menu.name}の{lang}での魅力的な説明をどうぞ"
                    )

    st.markdown("---")
    col_prev, col_next = st.columns([1, 1])
    with col_prev:
        if st.button("⬅️ 戻る", key="step5_back"):
            st.session_state.current_step = 4
            st.rerun()
    with col_next:
        if st.button("次へ進む ➡️", key="step5_next"):
            st.session_state.current_step = 6
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 6: 最終確認・CSV生成・ダウンロード
def show_completion_page():
    """最終確認・CSV生成・ダウンロードページ"""
    show_universal_navigation()

    st.markdown('<div class="main-container fade-in">', unsafe_allow_html=True)
    st.markdown('<h1 class="tonosama-header">✅ 最終確認 & CSV生成</h1>', unsafe_allow_html=True)
    st.info("これまでの入力内容を確認し、CSVファイルを生成・ダウンロードしてください。")

    st.subheader("📝 入力内容のサマリー")

    with st.expander("お店の基本情報と店主の想い", expanded=True):
        st.json(st.session_state.owner_answers_dict)

    with st.expander("メニュー情報", expanded=False):
        for i, menu in enumerate(st.session_state.finalized_menus):
            st.write(f"**メニュー {i+1}: {menu.name}**")
            st.write(f"価格: {menu.price}")
            st.write(f"カテゴリ: {menu.category}")
            st.write(f"アレルギー: {', '.join(menu.allergens) if menu.allergens else 'なし'}")
            st.write(f"掲載: {'はい' if menu.should_introduce else 'いいえ'}")
            if menu.is_featured:
                st.write(f"**イチオシメニュー！**")
                st.write(f"画像URL: {menu.image_url}")
            st.json(menu.multilingual_descriptions)
            st.markdown("---")

    with st.expander("アレルギー表示ポリシー", expanded=True):
        policy_map = {
            "display": "メニューごとにアレルギー情報を表示する",
            "hide": "アレルギー情報は表示しない",
            "disclaimer_only": "アレルギー情報は表示せず、店内の注意書きのみとする"
        }
        st.write(f"ポリシー: {policy_map.get(st.session_state.allergy_policy, '未設定')}")
        if st.session_state.allergy_policy == "disclaimer_only" and "allergy_disclaimer_text" in st.session_state.owner_answers_dict:
            st.write(f"店内アナウンス内容: {st.session_state.owner_answers_dict['allergy_disclaimer_text']}")

    st.markdown("---")

    if st.button("🚀 CSVファイルを生成", type="primary", use_container_width=True):
        if not st.session_state.finalized_menus:
            st.error("メニュー情報がありません。STEP2でメニューをアップロードしてください。")
        else:
            with st.spinner("CSVファイルを生成中..."):
                # 店主の想いを要約・翻訳（モック）
                combined_owner_thoughts = " ".join(st.session_state.owner_answers_dict.values())
                st.session_state.summarized_thought = f"【店主の想いサマリー】{combined_owner_thoughts[:100]}..." # 実際のサマリー処理を実装
                
                # 東大レベル翻訳エンジンで店主の想いを翻訳
                translated_thoughts = premium_translate_text(
                    st.session_state.summarized_thought,
                    CONFIG['supported_languages']
                )
                st.session_state.translated_thoughts = OwnerThoughts(
                    answers=st.session_state.owner_answers_dict,
                    summary=st.session_state.summarized_thought,
                    translations=translated_thoughts
                )

                # CSVデータ構築
                csv_rows = []
                headers_set = set()

                for menu_item in st.session_state.finalized_menus:
                    # イチオシメニューの翻訳情報を多言語説明に統合
                    if menu_item.is_featured and menu_item.multilingual_descriptions:
                         for lang, desc_text in menu_item.multilingual_descriptions.items():
                             menu_item.multilingual_descriptions[lang] = desc_text # 上書きはせずそのまま使用

                    row_obj = CSVRowStructure(
                        menu_item=menu_item,
                        owner_thoughts=st.session_state.translated_thoughts,
                        allergy_policy=st.session_state.allergy_policy
                    )
                    csv_rows.append(row_obj.get_row())
                    headers_set.update(row_obj.get_headers())
                
                # ヘッダーの順序を固定する
                ordered_headers = CSVRowStructure(
                    menu_item=st.session_state.finalized_menus[0] if st.session_state.finalized_menus else MenuData(0,"","",CONFIG['menu_categories'][0],0), # ダミーオブジェクト
                    owner_thoughts=st.session_state.translated_thoughts,
                    allergy_policy=st.session_state.allergy_policy
                ).get_headers()

                # DataFrame作成
                if csv_rows:
                    df = pd.DataFrame(csv_rows)
                    # ヘッダーの順番をCSVRowStructure.get_headers()で定義された順に並び替え
                    df = df[ordered_headers]
                    csv_data = df.to_csv(index=False, encoding='utf-8-sig') # Excelで開けるように'utf-8-sig'
                    b64 = base64.b64encode(csv_data.encode('utf-8-sig')).decode()
                    filename = f"tonosama_menu_data_{st.session_state.store_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                    st.session_state.csv_download_url = f"data:application/octet-stream;base64,{b64}"
                    st.session_state.csv_generated = True
                    st.success("✅ CSVファイルが正常に生成されました！")
                    logger.info("CSV file generated successfully.")
                else:
                    st.error("CSV生成対象のメニューがありません。")

    if st.session_state.csv_generated:
        st.markdown(f"""
            <a href="{st.session_state.csv_download_url}" download="tonosama_menu_data.csv">
                <button style="
                    background: linear-gradient(135deg, #28a745, #218838) !important;
                    color: white !important;
                    border: none !important;
                    border-radius: var(--border-radius) !important;
                    padding: 0.75rem 2rem !important;
                    font-weight: bold !important;
                    transition: all 0.3s ease !important;
                    box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3) !important;
                    cursor: pointer;
                    width: 100%;
                    margin-top: 1rem;
                ">
                    📥 CSVファイルをダウンロード
                </button>
            </a>
            """, unsafe_allow_html=True)
        st.success("ダウンロードボタンをクリックしてCSVファイルを保存してください。")

    st.markdown("---")
    col_prev, col_next = st.columns([1, 1])
    with col_prev:
        if st.button("⬅️ 戻る", key="step6_back"):
            st.session_state.current_step = 5
            st.rerun()
    with col_next:
        # このステップが最後なので「次へ」は不要だが、デザインの一貫性のために置くことも
        # if st.button("完了", key="step6_complete"):
        #     st.success("全ステップが完了しました！")
        #     # 必要であれば初期状態に戻すなどの処理
        #     pass
        pass # 現状は「完了」ボタンは設けない

    st.markdown('</div>', unsafe_allow_html=True)


# ====================
# アプリケーションのメイン実行部分
# ====================
def main():
    apply_beautiful_theme()
    initialize_app_session_state()

    # ログイン済みでなければログインページを表示
    if not st.session_state.logged_in:
        show_simple_login_page()
    else:
        # 現在のステップに応じてページを表示
        if st.session_state.current_step == 2:
            show_menu_upload_page()
        elif st.session_state.current_step == 3:
            show_owner_thoughts_page()
        elif st.session_state.current_step == 4:
            show_detail_settings_page()
        elif st.session_state.current_step == 5:
            show_featured_menus_page()
        elif st.session_state.current_step == 6:
            show_completion_page()
        else:
            # 想定外のステップ番号の場合、ログインページに戻すか、適切なエラー処理
            st.error("不明なステップです。ログインページに戻ります。")
            st.session_state.logged_in = False
            st.session_state.current_step = 1
            st.rerun()

if __name__ == "__main__":
    main()

