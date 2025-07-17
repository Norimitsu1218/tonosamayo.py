import streamlit as st
import pandas as pd
import time
from typing import Dict, List, Optional
import json

# 🎯 PS3風デザインCSS（凍結版保護）
def load_ps3_styles():
    st.markdown("""
    <style>
    /* PS3風ベースデザイン完全保護 */
    .main-container {
        background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 50%, #0f1419 100%);
        min-height: 100vh;
    }
    
    .ps3-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(16px);
    }
    
    .ps3-header {
        text-align: center;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #f59e0b);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .ps3-nav {
        background: linear-gradient(90deg, rgba(59, 130, 246, 0.5), rgba(139, 92, 246, 0.5));
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(16px);
    }
    
    .step-indicator {
        display: inline-block;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        text-align: center;
        line-height: 40px;
        margin: 0 10px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .step-active {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        color: white;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.6);
        transform: scale(1.1);
    }
    
    .step-completed {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
    }
    
    .step-pending {
        background: rgba(75, 85, 99, 0.5);
        color: #9ca3af;
        border: 1px solid #374151;
    }
    
    .ps3-button {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    .ps3-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
    }
    
    .featured-menu {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(217, 119, 6, 0.3));
        border: 2px solid rgba(245, 158, 11, 0.5);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        height: 8px;
        border-radius: 4px;
        transition: width 1s ease;
    }
    
    .success-message {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(5, 150, 105, 0.3));
        border: 1px solid rgba(16, 185, 129, 0.5);
        border-radius: 8px;
        padding: 1rem;
        color: #10b981;
    }
    
    .error-message {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(220, 38, 38, 0.3));
        border: 1px solid rgba(239, 68, 68, 0.5);
        border-radius: 8px;
        padding: 1rem;
        color: #ef4444;
    }
    </style>
    """, unsafe_allow_html=True)

# 🏗️ データ構造定義（凍結版保護）
class MenuData:
    def __init__(self, id: int, name: str, price: str, category: str):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.order = 0
        self.imageUrl = ""
        self.allergens = []
        self.multilingualDescriptions = {"日本語": ""}
        self.isFeatured = False
        self.shouldIntroduce = True

class TONOSAMAConfig:
    COMMON_ALLERGENS = [
        "小麦", "甲殻類", "卵", "魚", "大豆", "ピーナッツ", 
        "牛乳", "くるみ", "セロリ", "マスタード", "ゴマ", 
        "亜硫酸塩", "ルピナス", "貝"
    ]
    
    MENU_CATEGORIES = ["フード", "コース", "ランチ", "デザート", "ドリンク"]
    
    PLANS = [
        {
            "id": "basic",
            "name": "ベーシックプラン",
            "description": "基本的な多言語メニュー作成",
            "features": ["5言語対応", "基本メニュー翻訳", "CSVファイル出力"],
            "recommended": False
        },
        {
            "id": "premium", 
            "name": "プレミアムプラン",
            "description": "高品質な多言語メニュー作成", 
            "features": ["15言語対応", "高品質翻訳", "イチオシメニュー設定", "画像対応", "CSVファイル出力"],
            "recommended": True
        },
        {
            "id": "enterprise",
            "name": "エンタープライズプラン", 
            "description": "完全カスタマイズ可能",
            "features": ["全言語対応", "AI翻訳", "完全カスタマイズ", "24時間サポート", "API連携"],
            "recommended": False
        }
    ]

# 🔐 認証機能（凍結版保護）
def authenticate_credentials(store_id: str, member_number: str) -> bool:
    """模擬認証システム"""
    return store_id == "TONOSAMA001" and member_number == "99999"

def perform_ocr_simulation() -> List[MenuData]:
    """OCRシミュレーション"""
    mock_menus = [
        MenuData(1001, "唐揚げ定食", "980円", "フード"),
        MenuData(1002, "焼き魚御膳", "1200円", "フード"), 
        MenuData(1003, "特製ラーメン", "850円", "フード")
    ]
    mock_menus[0].allergens = ["小麦", "大豆"]
    mock_menus[1].allergens = ["魚"] 
    mock_menus[2].allergens = ["小麦", "卵"]
    return mock_menus

# 🎨 ナビゲーション表示（凍結版保護）
def render_navigation(current_step: int):
    steps = ["プラン", "ログイン", "メニュー", "詳細設定", "店主の想い", "イチオシ", "完成！"]
    
    st.markdown('<div class="ps3-nav">', unsafe_allow_html=True)
    
    # ステップインジケーター
    cols = st.columns(7)
    for i, (col, step) in enumerate(zip(cols, steps)):
        with col:
            if i == current_step:
                st.markdown(f'<div class="step-indicator step-active">{i+1}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="text-align: center; color: white; font-weight: bold;">{step}</div>', unsafe_allow_html=True)
            elif i < current_step:
                st.markdown(f'<div class="step-indicator step-completed">✓</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="text-align: center; color: #10b981;">{step}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="step-indicator step-pending">{i+1}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="text-align: center; color: #9ca3af;">{step}</div>', unsafe_allow_html=True)
    
    # プログレスバー
    progress = (current_step / (len(steps) - 1)) * 100
    st.markdown(f"""
    <div style="margin-top: 2rem;">
        <div style="background: #374151; height: 8px; border-radius: 4px; overflow: hidden;">
            <div class="progress-bar" style="width: {progress}%;"></div>
        </div>
        <div style="text-align: center; margin-top: 1rem; color: #3b82f6; font-weight: bold;">
            進捗状況: {int(progress)}% 完了
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 📋 Step 0: プラン選択（凍結版保護）
def render_plan_selection():
    st.markdown('<div class="ps3-card">', unsafe_allow_html=True)
    st.markdown('<h1 class="ps3-header">👑 プラン選択</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #9ca3af; font-size: 1.2rem;">お店に最適なプランを選択して、世界中のお客様に素晴らしい体験を提供しましょう</p>', unsafe_allow_html=True)
    
    cols = st.columns(3)
    for i, plan in enumerate(TONOSAMAConfig.PLANS):
        with cols[i]:
            if plan["recommended"]:
                st.markdown('<div style="text-align: center;"><span style="background: linear-gradient(90deg, #f59e0b, #d97706); color: black; padding: 4px 12px; border-radius: 12px; font-weight: bold;">⭐ おすすめ</span></div>', unsafe_allow_html=True)
            
            st.markdown(f'<h3 style="text-align: center; color: white; font-weight: bold;">{plan["name"]}</h3>', unsafe_allow_html=True)
            st.markdown(f'<p style="text-align: center; color: #9ca3af;">{plan["description"]}</p>', unsafe_allow_html=True)
            
            for feature in plan["features"]:
                st.markdown(f'<div style="color: #10b981; margin: 0.5rem 0;">✅ {feature}</div>', unsafe_allow_html=True)
            
            if st.button(f'{plan["name"]}を選択', key=f'plan_{plan["id"]}', help="このプランを選択"):
                st.session_state.selected_plan = plan["id"]
                st.session_state.current_step = 1
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# 🔐 Step 1: ログイン（凍結版保護）
def render_login():
    st.markdown('<div class="ps3-card">', unsafe_allow_html=True)
    st.markdown('<h1 class="ps3-header">🖥️ TONOSAMA</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #3b82f6; font-size: 1.2rem;">東大レベル翻訳システム</p>', unsafe_allow_html=True)
    
    # セッション状態の初期化（エラー修正）
    if 'login_store_id' not in st.session_state:
        st.session_state.login_store_id = ""
    if 'login_member_number' not in st.session_state:
        st.session_state.login_member_number = ""
    
    st.markdown('<h3 style="color: #3b82f6;">🛡️ ストアID</h3>', unsafe_allow_html=True)
    store_id = st.text_input("", placeholder="例: TONOSAMA001", value=st.session_state.login_store_id, key="store_id_input")
    
    st.markdown('<h3 style="color: #3b82f6;">🛡️ 責任者ナンバー</h3>', unsafe_allow_html=True)
    member_number = st.text_input("", type="password", placeholder="例: 99999", value=st.session_state.login_member_number, key="member_number_input")
    
    # セッション状態更新（安全な方法）
    st.session_state.login_store_id = store_id
    st.session_state.login_member_number = member_number
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        login_clicked = st.button("⚡ システムログイン", use_container_width=True, type="primary")
    
    if login_clicked and store_id and member_number:
        with st.spinner("認証中..."):
            time.sleep(1)  # 認証処理シミュレーション
            if authenticate_credentials(store_id, member_number):
                st.session_state.logged_in = True
                st.session_state.store_id = store_id
                st.session_state.current_step = 2
                st.success("✅ ログイン成功！")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ ログイン情報が正しくありません")
    elif login_clicked:
        st.warning("⚠️ ストアIDと責任者ナンバーを入力してください")
    
    st.markdown('<div style="text-align: center; color: #3b82f6; background: rgba(59, 130, 246, 0.1); padding: 1rem; border-radius: 8px; margin-top: 1rem;"><div style="font-size: 1.2rem;">🛡️</div>あなたの情報は暗号化されて安全に保護されます</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 📤 Step 2: メニューアップロード（凍結版保護）
def render_menu_upload():
    st.markdown('<div class="ps3-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #3b82f6;">📤 メニューアップロード</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #9ca3af;">お店のメニュー表（画像またはPDF）をアップロードしてください</p>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "ファイルを選択してください", 
        type=['png', 'jpg', 'jpeg', 'pdf'],
        help="PNG, JPG, PDF (最大10MB)"
    )
    
    if uploaded_file:
        st.markdown('<div class="success-message">✅ ファイルアップロード完了</div>', unsafe_allow_html=True)
        
        if st.button("🤖 AI解析開始", use_container_width=True):
            with st.spinner("AI解析中..."):
                time.sleep(2)
                menus = perform_ocr_simulation()
                st.session_state.menus = menus
                st.session_state.current_step = 3
                st.rerun()
    
    # メニュー編集セクション
    if 'menus' in st.session_state and st.session_state.menus:
        st.markdown('<h3 style="color: #f59e0b;">✏️ メニュー情報の編集</h3>', unsafe_allow_html=True)
        
        for i, menu in enumerate(st.session_state.menus):
            with st.expander(f"📋 メニュー {i+1}: {menu.name}"):
                col1, col2 = st.columns(2)
                with col1:
                    menu.name = st.text_input("メニュー名", value=menu.name, key=f"name_{menu.id}")
                    menu.category = st.selectbox("カテゴリー", TONOSAMAConfig.MENU_CATEGORIES, 
                                               index=TONOSAMAConfig.MENU_CATEGORIES.index(menu.category), key=f"cat_{menu.id}")
                with col2:
                    menu.price = st.text_input("価格", value=menu.price, key=f"price_{menu.id}")
                    menu.shouldIntroduce = st.checkbox("このメニューを掲載する", value=menu.shouldIntroduce, key=f"intro_{menu.id}")
                
                st.markdown("**アレルギー情報**")
                selected_allergens = st.multiselect(
                    "該当するアレルギー成分を選択", 
                    TONOSAMAConfig.COMMON_ALLERGENS,
                    default=menu.allergens,
                    key=f"allergens_{menu.id}"
                )
                menu.allergens = selected_allergens
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("➡️ 次へ進む", use_container_width=True):
                st.session_state.current_step = 3
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ⚙️ Step 3: 詳細設定（凍結版保護）
def render_detail_settings():
    st.markdown('<div class="ps3-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #3b82f6;">⚙️ 詳細設定</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #9ca3af;">アレルギー情報に関する表示ポリシーを設定してください</p>', unsafe_allow_html=True)
    
    allergy_policy = st.radio(
        "**アレルギー情報表示ポリシー**",
        ["全メニューにアレルギー情報を表示する", "アレルギー情報は表示しない", "店内の注意書きのみとする"],
        key="allergy_policy"
    )
    
    if allergy_policy == "店内の注意書きのみとする":
        st.markdown('<h4 style="color: #3b82f6;">店内でのアレルギー対応について</h4>', unsafe_allow_html=True)
        allergy_disclaimer = st.text_area(
            "注意書き内容", 
            placeholder="例: アレルギーをお持ちのお客様は、ご来店時にスタッフまでお申し出ください。可能な限り対応させていただきます。",
            height=100
        )
        st.session_state.allergy_disclaimer = allergy_disclaimer
    
    st.session_state.allergy_policy = allergy_policy
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ 戻る"):
            st.session_state.current_step = 2
            st.rerun()
    with col3:
        if st.button("➡️ 次へ進む"):
            st.session_state.current_step = 4
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# 💭 Step 4: 店主の想い（凍結版保護）
def render_owner_thoughts():
    st.markdown('<div class="ps3-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #3b82f6;">💭 店主の想いを世界に伝えましょう</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #f59e0b; font-size: 1.1rem; font-weight: bold;">15問の質問にお答えいただき、お店の想いを教えてください</p>', unsafe_allow_html=True)
    
    if 'owner_answers' not in st.session_state:
        st.session_state.owner_answers = {}
    
    # 質問セクション
    questions = [
        ("🏪 お店の基本情報", [
            ("restaurant_name", "お店の名前を教えてください", "例: 和食処 さくら"),
            ("years_in_business", "お店を開いてから何年になりますか?", "例: 10年になります"),
            ("location_features", "お店の場所・立地の特徴を教えてください", "例: 駅から徒歩3分、商店街の中にあります")
        ]),
        ("💭 お店の想い・こだわり", [
            ("concept", "お店のコンセプトや想いを教えてください", "例: 家庭的な温かい雰囲気で、心のこもった料理を提供したい"),
            ("ingredient_commitment", "特にこだわっている食材や調理法はありますか?", "例: 地元の野菜を使用し、手作りにこだわっています"),
            ("service_approach", "お客様に対してどのようなサービスを心がけていますか?", "例: 一人一人のお客様との会話を大切にしています")
        ]),
        ("🍽️ 料理・メニューについて", [
            ("signature_dish", "お店の看板メニューとその特徴を教えてください", "例: 手作りハンバーグは祖母から受け継いだレシピです"),
            ("seasonal_menus", "季節ごとのメニューやイベントはありますか?", "例: 春は山菜料理、夏は冷やし中華に力を入れています"),
            ("menu_development", "新しいメニューを考える時に大切にしていることは?", "例: お客様の声を聞いて、健康的で美味しい料理を考えています")
        ]),
        ("🌏 国際的なお客様について", [
            ("international_experience", "海外のお客様にどのような体験をしてほしいですか?", "例: 日本の家庭料理の温かさを感じてほしいです"),
            ("cultural_sharing", "お店の文化や料理の背景で伝えたいことはありますか?", "例: 手作りの大切さと、食材への感謝の気持ちを伝えたいです"),
            ("international_message", "海外からのお客様へのメッセージをお聞かせください", "例: 日本の味を楽しんでいただき、素敵な思い出を作ってください")
        ]),
        ("🚀 今後の展望", [
            ("future_goals", "今後のお店の目標や夢を教えてください", "例: 地域の人々と海外の方々の交流の場になりたいです"),
            ("multilingual_expectations", "多言語メニューでどのような効果を期待されますか?", "例: 言葉の壁を越えて、より多くの方に料理を楽しんでもらいたいです"),
            ("customer_message", "最後に、お客様への一言メッセージをお願いします", "例: 心を込めて作った料理で、皆様に笑顔をお届けします")
        ])
    ]
    
    total_questions = sum(len(section[1]) for section in questions)
    answered_count = len([k for k in st.session_state.owner_answers.keys() if st.session_state.owner_answers.get(k, '').strip()])
    
    # プログレス表示
    progress = (answered_count / total_questions) * 100
    st.markdown(f"""
    <div style="background: rgba(59, 130, 246, 0.1); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
        <div style="display: flex; justify-content: space-between; color: #3b82f6; font-weight: bold;">
            <span>回答進捗</span>
            <span>{answered_count}/{total_questions} 完了</span>
        </div>
        <div style="background: #374151; height: 6px; border-radius: 3px; margin-top: 0.5rem; overflow: hidden;">
            <div style="background: linear-gradient(90deg, #3b82f6, #8b5cf6); height: 100%; width: {progress}%; transition: width 0.5s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 質問表示
    for section_title, section_questions in questions:
        st.markdown(f'<h3 style="color: #f59e0b;">{section_title}</h3>', unsafe_allow_html=True)
        for key, question, placeholder in section_questions:
            st.markdown(f'<h4 style="color: #3b82f6;">{question}</h4>', unsafe_allow_html=True)
            st.markdown(f'<p style="color: #9ca3af; font-size: 0.9rem;"><strong>回答例:</strong> {placeholder}</p>', unsafe_allow_html=True)
            answer = st.text_area("", placeholder=placeholder, key=key, height=80)
            st.session_state.owner_answers[key] = answer
            st.markdown('<br>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ 戻る"):
            st.session_state.current_step = 3
            st.rerun()
    with col3:
        can_proceed = answered_count == total_questions
        if st.button("➡️ 次へ進む", disabled=not can_proceed):
            if can_proceed:
                st.session_state.current_step = 5
                st.rerun()
            else:
                st.error("すべての質問にお答えください")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ⭐ Step 5: イチオシメニュー（凍結版保護）
def render_featured_menus():
    st.markdown('<div class="ps3-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #f59e0b;">⭐ イチオシメニュー設定</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #9ca3af;">お店のイチオシメニューを選択し、詳細情報を設定してください</p>', unsafe_allow_html=True)
    
    if 'featured_menus' not in st.session_state:
        st.session_state.featured_menus = []
    
    # イチオシメニュー選択
    st.markdown('<h3 style="color: #f59e0b;">イチオシメニューを選択してください</h3>', unsafe_allow_html=True)
    
    available_menus = [menu for menu in st.session_state.get('menus', []) if menu.shouldIntroduce]
    
    for menu in available_menus:
        is_featured = menu.id in [fm.id for fm in st.session_state.featured_menus]
        
        if st.checkbox(f"{menu.name} ({menu.price})", value=is_featured, key=f"featured_{menu.id}"):
            if not is_featured:
                st.session_state.featured_menus.append(menu)
        else:
            if is_featured:
                st.session_state.featured_menus = [fm for fm in st.session_state.featured_menus if fm.id != menu.id]
    
    # イチオシメニュー詳細設定
    if st.session_state.featured_menus:
        st.markdown('<h3 style="color: #f59e0b;">イチオシメニュー詳細設定</h3>', unsafe_allow_html=True)
        
        for menu in st.session_state.featured_menus:
            st.markdown(f'<div class="featured-menu">', unsafe_allow_html=True)
            st.markdown(f'<h4 style="color: #f59e0b;">⭐ {menu.name}</h4>', unsafe_allow_html=True)
            
            menu.imageUrl = st.text_input("イチオシメニュー用画像URL", value=menu.imageUrl, key=f"img_{menu.id}")
            
            description = st.text_area(
                "日本語説明文", 
                value=menu.multilingualDescriptions.get("日本語", ""),
                placeholder=f"{menu.name}の魅力的な説明をどうぞ",
                height=100,
                key=f"desc_{menu.id}"
            )
            menu.multilingualDescriptions["日本語"] = description
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ 戻る"):
            st.session_state.current_step = 4
            st.rerun()
    with col3:
        if st.button("➡️ 次へ進む"):
            st.session_state.current_step = 6
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# 🎉 Step 6: 完成（凍結版保護）
def render_completion():
    st.markdown('<div class="ps3-card">', unsafe_allow_html=True)
    
    if 'is_completed' not in st.session_state:
        st.session_state.is_completed = False
    
    if not st.session_state.is_completed:
        st.markdown('<h1 class="ps3-header">🎁 完成！</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #9ca3af; font-size: 1.2rem;">いよいよ最終ステップです！</p>', unsafe_allow_html=True)
        
        # サマリー表示
        st.markdown('<h3 style="color: #3b82f6;">📋 入力内容サマリー</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div style="background: rgba(59, 130, 246, 0.1); padding: 1rem; border-radius: 8px;">', unsafe_allow_html=True)
            st.markdown('<h4 style="color: #3b82f6;">店舗情報</h4>', unsafe_allow_html=True)
            selected_plan_name = next((p["name"] for p in TONOSAMAConfig.PLANS if p["id"] == st.session_state.get("selected_plan", "")), "未選択")
            st.markdown(f'<p><span style="color: #3b82f6;">プラン:</span> {selected_plan_name}</p>', unsafe_allow_html=True)
            st.markdown(f'<p><span style="color: #3b82f6;">店舗ID:</span> {st.session_state.get("store_id", "")}</p>', unsafe_allow_html=True)
            st.markdown(f'<p><span style="color: #3b82f6;">店名:</span> {st.session_state.get("owner_answers", {}).get("restaurant_name", "")}</p>', unsafe_allow_html=True)
            menu_count = len([m for m in st.session_state.get("menus", []) if m.shouldIntroduce])
            st.markdown(f'<p><span style="color: #3b82f6;">メニュー数:</span> {menu_count}品</p>', unsafe_allow_html=True)
            featured_count = len(st.session_state.get("featured_menus", []))
            st.markdown(f'<p><span style="color: #3b82f6;">イチオシ:</span> {featured_count}品</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div style="background: rgba(59, 130, 246, 0.1); padding: 1rem; border-radius: 8px;">', unsafe_allow_html=True)
            st.markdown('<h4 style="color: #3b82f6;">設定情報</h4>', unsafe_allow_html=True)
            allergy_policy_text = {
                "全メニューにアレルギー情報を表示する": "表示する",
                "アレルギー情報は表示しない": "表示しない", 
                "店内の注意書きのみとする": "注意書きのみ"
            }.get(st.session_state.get("allergy_policy", ""), "未設定")
            st.markdown(f'<p><span style="color: #3b82f6;">アレルギー表示:</span> {allergy_policy_text}</p>', unsafe_allow_html=True)
            st.markdown('<p><span style="color: #3b82f6;">想いの回答:</span> 15/15 完了</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<hr style="border: 1px solid #374151; margin: 2rem 0;">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✨ 完成！", use_container_width=True, help="多言語メニューの作成を完了します"):
                with st.spinner("処理中..."):
                    time.sleep(2)
                    st.session_state.is_completed = True
                    st.rerun()
        
        st.markdown('<p style="text-align: center; color: #9ca3af; margin-top: 1rem;">ボタンを押すと多言語メニューの作成が完了します</p>', unsafe_allow_html=True)
    
    else:
        # 完成画面
        st.markdown('<h1 class="ps3-header">🎉 完成！</h1>', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center; color: #10b981; font-size: 2rem;">おめでとうございます！🎉</h2>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #9ca3af; font-size: 1.2rem;">多言語メニューの準備が完了しました！<br>世界中のお客様に素晴らしい体験をお届けください！</p>', unsafe_allow_html=True)
        
        # 完了内容表示
        st.markdown('<div class="success-message">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #10b981;">📋 完了内容</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            selected_plan_name = next((p["name"] for p in TONOSAMAConfig.PLANS if p["id"] == st.session_state.get("selected_plan", "")), "未選択")
            st.markdown(f'<p><span style="color: #10b981;">プラン:</span> {selected_plan_name}</p>', unsafe_allow_html=True)
            st.markdown(f'<p><span style="color: #10b981;">店名:</span> {st.session_state.get("owner_answers", {}).get("restaurant_name", "")}</p>', unsafe_allow_html=True)
            menu_count = len([m for m in st.session_state.get("menus", []) if m.shouldIntroduce])
            st.markdown(f'<p><span style="color: #10b981;">メニュー数:</span> {menu_count}品</p>', unsafe_allow_html=True)
        
        with col2:
            featured_count = len(st.session_state.get("featured_menus", []))
            st.markdown(f'<p><span style="color: #10b981;">イチオシ:</span> {featured_count}品</p>', unsafe_allow_html=True)
            st.markdown('<p><span style="color: #10b981;">想いの回答:</span> 15/15 完了</p>', unsafe_allow_html=True)
            st.markdown('<p><span style="color: #10b981;">アレルギー設定:</span> 完了</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div style="text-align: center; color: #10b981; font-size: 1.5rem; font-weight: bold; margin: 2rem 0;">システム処理が完了しました！</div>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #9ca3af;">多言語対応メニューの作成が正常に完了いたしました。<br>素晴らしいお店作りを心より応援しております！</p>', unsafe_allow_html=True)
        
        # CSVダウンロード機能
        if st.session_state.get("menus"):
            csv_data = generate_csv_output()
            st.download_button(
                label="📥 多言語メニューCSVをダウンロード",
                data=csv_data,
                file_name=f"tonosama_menu_{st.session_state.get('store_id', 'export')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    st.markdown('</div>', unsafe_allow_html=True)

# 📊 CSV出力機能（凍結版保護）
def generate_csv_output() -> str:
    """メニュー情報をCSV形式で出力"""
    if not st.session_state.get("menus"):
        return ""
    
    csv_data = []
    headers = ["ID", "メニュー名", "価格", "カテゴリー", "アレルギー情報", "イチオシ", "説明文"]
    csv_data.append(",".join(headers))
    
    for menu in st.session_state.menus:
        if menu.shouldIntroduce:
            row = [
                str(menu.id),
                f'"{menu.name}"',
                f'"{menu.price}"',
                f'"{menu.category}"',
                f'"{", ".join(menu.allergens)}"',
                "○" if menu.id in [fm.id for fm in st.session_state.get("featured_menus", [])] else "",
                f'"{menu.multilingualDescriptions.get("日本語", "")}"'
            ]
            csv_data.append(",".join(row))
    
    return "\n".join(csv_data)

# 🎮 メイン関数（凍結版保護）
def main():
    # ページ設定
    st.set_page_config(
        page_title="TONOSAMA - 多言語メニュー作成システム",
        page_icon="🏮",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # PS3風スタイル読み込み
    load_ps3_styles()
    
    # セッション状態初期化
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    # メインコンテナ
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # ナビゲーション表示
    render_navigation(st.session_state.current_step)
    
    # ステップごとの画面表示
    if st.session_state.current_step == 0:
        render_plan_selection()
    elif st.session_state.current_step == 1:
        render_login()
    elif st.session_state.current_step == 2:
        render_menu_upload()
    elif st.session_state.current_step == 3:
        render_detail_settings()
    elif st.session_state.current_step == 4:
        render_owner_thoughts()
    elif st.session_state.current_step == 5:
        render_featured_menus()
    elif st.session_state.current_step == 6:
        render_completion()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # フッター
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; color: #6b7280; border-top: 1px solid #374151;">
        <p>🏮 TONOSAMA 東大レベル翻訳システム | 約束を守ることの大事さを知っている人へ</p>
        <p style="font-size: 0.9rem;">美しいお店作りを心より応援しております</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
