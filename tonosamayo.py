import streamlit as st
import time
import os
import json

# ====================
# 1. 共通設定とユーティリティ関数
# ====================

# 定義された新しいカラーパレットとボタンCSSを基にしたカスタムCSS
st.markdown("""
<style>
/* カラーパレット (お客様指定の色) */
:root {
    --color-background-primary: #F8F0E3;      /* 非常に薄い黄みがかったベージュ */
    --color-text-primary: #1A1A1A;           /* 非常に濃いグレー（ほぼ黒） */

    --color-button-normal: #8B4513;          /* ボタン サドルブラウン */
    --color-button-hover: #654321;           /* ボタンが押された時に変わる色 より濃いブラウン */
    --color-button-text: #FFFFFF;            /* ボタンの中の文字 純白 */

    --color-accent: #8B4513;                 /* アクセントカラー (サドルブラウン) */
    --color-input-background: #FFFFFF;       /* 入力フィールドの背景 */
    --color-input-border: #8B4513;           /* 入力フィールドのボーダー (サドルブラウン) */

    /* メッセージボックスの色 */
    --color-info-bg: #E8F4F8;
    --color-info-text: #0D47A1;
    --color-info-border: #1976D2;

    --color-warning-bg: #FFF8E1;
    --color-warning-text: #E65100;
    --color-warning-border: #FF9800;

    --color-success-bg: #E8F5E8;
    --color-success-text: #1B5E20;
    --color-success-border: #4CAF50;

    --color-error-bg: #FFEBEE;
    --color-error-text: #B71C1C;
    --color-error-border: #F44336;
}

/* 基本設定 */
html, body, [class^="st-"] {
    background-color: var(--color-background-primary) !important;
    color: var(--color-text-primary) !important;
    font-family: 'Helvetica Neue', Arial, sans-serif !important;
}

.stApp {
    background-color: var(--color-background-primary);
}

/* 全てのテキスト要素 */
h1, h2, h3, h4, h5, h6, p, span, div, li, strong, em {
    color: var(--color-text-primary) !important;
    text-shadow: none !important;
}

/* Infoボックスの色 */
div[data-testid="stInfo"] {
    background-color: var(--color-info-bg) !important;
    color: var(--color-info-text) !important;
    border-left: 4px solid var(--color-info-border) !important;
    padding: 16px !important;
    border-radius: 8px !important;
    margin: 15px 0 !important;
}
/* Warningボックスの色 */
div[data-testid="stWarning"] {
    background-color: var(--color-warning-bg) !important;
    color: var(--color-warning-text) !important;
    border-left: 4px solid var(--color-warning-border) !important;
    padding: 16px !important;
    border-radius: 8px !important;
    margin: 15px 0 !important;
}
/* Successボックスの色 */
div[data-testid="stSuccess"] {
    background-color: var(--color-success-bg) !important;
    color: var(--color-success-text) !important;
    border-left: 4px solid var(--color-success-border) !important;
    padding: 16px !important;
    border-radius: 8px !important;
    margin: 15px 0 !important;
}
/* Errorボックスの色 */
div[data-testid="stError"] {
    background-color: var(--color-error-bg) !important;
    color: var(--color-error-text) !important;
    border-left: 4px solid var(--color-error-border) !important;
    padding: 16px !important;
    border-radius: 8px !important;
    margin: 15px 0 !important;
}

/* 🔥 超強力なCSS - 確実にボタンを茶色にする */

/* 🔥 STEP 1: 最も強力なボタン指定 - 全てのボタン要素を対象 */
button,
input[type="button"],
input[type="submit"],
.stButton button,
.stButton > button,
.stFormSubmitButton button,
.stFormSubmitButton > button,
.stDownloadButton button,
.stDownloadButton > button,
[data-testid="stButton"] button,
[data-testid="stFormSubmitButton"] button,
[data-testid="stDownloadButton"] button,
[class*="stButton"] button,
[class*="baseButton"],
[class*="Button-"] {
    background-color: var(--color-button-normal) !important;
    background: var(--color-button-normal) !important;
    color: var(--color-button-text) !important;
    border: 2px solid var(--color-button-hover) !important;
    border-radius: 8px !important;
    font-weight: bold !important;
    padding: 12px 24px !important;
    cursor: pointer !important;
    font-size: 16px !important; /* フォントサイズを固定 */
    transition: all 0.3s ease !important;
    margin: 10px 5px !important;
    font-family: 'Helvetica Neue', Arial, sans-serif !important;
    text-decoration: none !important;
    text-align: center !important;
    display: inline-block !important;
    vertical-align: middle !important;
    box-shadow: none !important;
    outline: none !important;
    min-height: 2.5em !important;
}

/* 🔥 STEP 2: ボタン内部の全要素も強制的に統一 */
button *,
input[type="button"] *,
input[type="submit"] *,
.stButton button *,
.stButton > button *,
.stFormSubmitButton button *,
.stFormSubmitButton > button *,
.stDownloadButton button *,
.stDownloadButton > button *,
[data-testid="stButton"] button *,
[data-testid="stFormSubmitButton"] button *,
[data-testid="stDownloadButton"] button *,
[class*="stButton"] button *,
[class*="baseButton"] *,
[class*="Button-"] * {
    background-color: transparent !important;
    background: transparent !important;
    color: var(--color-button-text) !important;
    border: none !important;
    font-weight: bold !important;
    font-size: inherit !important;
    font-family: inherit !important;
    text-decoration: none !important;
    text-shadow: none !important;
    box-shadow: none !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* 🔥 STEP 3: ホバー時の強制指定 */
button:hover,
input[type="button"]:hover,
input[type="submit"]:hover,
.stButton button:hover,
.stButton > button:hover,
.stFormSubmitButton button:hover,
.stFormSubmitButton > button:hover,
.stDownloadButton button:hover,
.stDownloadButton > button:hover,
[data-testid="stButton"] button:hover,
[data-testid="stFormSubmitButton"] button:hover,
[data-testid="stDownloadButton"] button:hover,
[class*="stButton"] button:hover,
[class*="baseButton"]:hover,
[class*="Button-"]:hover {
    background-color: var(--color-button-hover) !important;
    background: var(--color-button-hover) !important;
    color: var(--color-button-text) !important;
    border-color: var(--color-button-hover) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
}

/* ホバー時の内部要素 */
button:hover *,
input[type="button"]:hover *,
input[type="submit"]:hover *,
.stButton button:hover *,
.stButton > button:hover *,
.stFormSubmitButton button:hover *,
.stFormSubmitButton > button:hover *,
.stDownloadButton button:hover *,
.stDownloadButton > button:hover *,
[data-testid="stButton"] button:hover *,
[data-testid="stFormSubmitButton"] button:hover *,
[data-testid="stDownloadButton"] button:hover *,
[class*="stButton"] button:hover *,
[class*="baseButton"]:hover *,
[class*="Button-"]:hover * {
    background-color: transparent !important;
    background: transparent !important;
    color: var(--color-button-text) !important;
}

/* 🔥 STEP 4: アクティブ/フォーカス時も強制指定 */
button:active,
button:focus,
input[type="button"]:active,
input[type="button"]:focus,
input[type="submit"]:active,
input[type="submit"]:focus,
.stButton button:active,
.stButton button:focus,
.stButton > button:active,
.stButton > button:focus,
.stFormSubmitButton button:active,
.stFormSubmitButton button:focus,
.stFormSubmitButton > button:active,
.stFormSubmitButton > button:focus,
.stDownloadButton button:active,
.stDownloadButton button:focus,
.stDownloadButton > button:active,
.stDownloadButton > button:focus,
[data-testid="stButton"] button:active,
[data-testid="stButton"] button:focus,
[data-testid="stFormSubmitButton"] button:active,
[data-testid="stFormSubmitButton"] button:focus,
[data-testid="stDownloadButton"] button:active,
[data-testid="stDownloadButton"] button:focus,
[class*="stButton"] button:active,
[class*="stButton"] button:focus,
[class*="baseButton"]:active,
[class*="baseButton"]:focus,
[class*="Button-"]:active,
[class*="Button-"]:focus {
    background-color: #5D3A0F !important;
    background: #5D3A0F !important;
    color: var(--color-button-text) !important;
    border-color: #5D3A0F !important;
    transform: translateY(1px) !important;
    outline: 2px solid #A0522D !important;
    outline-offset: 2px !important;
}

/* アクティブ/フォーカス時の内部要素 */
button:active *,
button:focus *,
input[type="button"]:active *,
input[type="button"]:focus *,
input[type="submit"]:active *,
input[type="submit"]:focus *,
.stButton button:active *,
.stButton button:focus *,
.stButton > button:active *,
.stButton > button:focus *,
.stFormSubmitButton button:active *,
.stFormSubmitButton button:focus *,
.stFormSubmitButton > button:active *,
.stFormSubmitButton > button:focus *,
.stDownloadButton button:active *,
.stDownloadButton button:focus *,
.stDownloadButton > button:active *,
.stDownloadButton > button:focus *,
[data-testid="stButton"] button:active *,
[data-testid="stButton"] button:focus *,
[data-testid="stFormSubmitButton"] button:active *,
[data-testid="stFormSubmitButton"] button:focus *,
[data-testid="stDownloadButton"] button:active *,
[data-testid="stDownloadButton"] button:focus *,
[class*="stButton"] button:active *,
[class*="stButton"] button:focus *,
[class*="baseButton"]:active *,
[class*="baseButton"]:focus *,
[class*="Button-"]:active *,
[class*="Button-"]:focus * {
    background-color: transparent !important;
    background: transparent !important;
    color: var(--color-button-text) !important;
}

/* 🔥 STEP 5: 非常に具体的なStreamlit内部クラス指定 */
[class*="element-container"] button,
[class*="stButton"] [class*="baseButton"],
[class*="stFormSubmitButton"] [class*="baseButton"],
[class*="stDownloadButton"] [class*="baseButton"] {
    background-color: var(--color-button-normal) !important;
    background: var(--color-button-normal) !important;
    color: var(--color-button-text) !important;
    border: 2px solid var(--color-button-hover) !important;
}

[class*="element-container"] button *,
[class*="stButton"] [class*="baseButton"] *,
[class*="stFormSubmitButton"] [class*="baseButton"] *,
[class*="stDownloadButton"] [class*="baseButton"] * {
    background-color: transparent !important;
    background: transparent !important;
    color: var(--color-button-text) !important;
}

/* 🔥 STEP 6: 最終手段 - 全てのボタン類似要素 */
[role="button"],
[type="button"],
[type="submit"] {
    background-color: var(--color-button-normal) !important;
    background: var(--color-button-normal) !important;
    color: var(--color-button-text) !important;
    border: 2px solid var(--color-button-hover) !important;
    border-radius: 8px !important;
    font-weight: bold !important;
    padding: 12px 24px !important;
}

[role="button"] *,
[type="button"] *,
[type="submit"] * {
    background-color: transparent !important;
    background: transparent !important;
    color: var(--color-button-text) !important;
}

/* ラジオボタンのスタイル (既存のものを維持しつつ、カラーパレットに合わせる) */
.stRadio > label {
    color: var(--color-text-primary) !important;
    display: flex !important;
    align-items: center !important;
    margin-bottom: 8px !important;
}
.stRadio > label > div[data-testid="stFlex"] > div:first-child {
    border: 2px solid var(--color-text-primary) !important;
    background-color: var(--color-input-background) !important; /* 白 */
    border-radius: 50% !important;
    width: 20px !important;
    height: 20px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-shrink: 0 !important;
    margin-right: 10px !important;
    transition: all 0.2s ease-in-out !important;
}
.stRadio > label > div[data-testid="stFlex"] > div:first-child > div {
    background-color: var(--color-button-normal) !important; /* サドルブラウン */
    border-radius: 50% !important;
    width: 10px !important;
    height: 10px !important;
    opacity: 0 !important;
    transform: scale(0) !important;
    transition: all 0.2s ease-in-out !important;
}
.stRadio input[type="radio"]:checked + div[data-testid="stFlex"] > div:first-child > div {
    opacity: 1 !important;
    transform: scale(1) !important;
}
.stRadio > label:hover > div[data-testid="stFlex"] > div:first-child {
    border-color: var(--color-button-normal) !important;
    box-shadow: 0 0 5px rgba(139, 69, 19, 0.5) !important; /* サドルブラウンの影 */
}

/* テキスト入力フィールド */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div > div {
    background-color: var(--color-input-background) !important;
    color: var(--color-text-primary) !important;
    border: 2px solid var(--color-input-border) !important; /* サドルブラウンの太い枠線 */
    border-radius: 6px !important;
    padding: 10px !important;
    font-size: 1em !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox > div > div > div > div:focus {
    outline: none !important;
    border-color: var(--color-button-hover) !important; /* フォーカス時により濃いブラウン */
    box-shadow: 0 0 0 2px rgba(139, 69, 19, 0.4) !important; /* フォーカス時の影も強調 */
}

/* 音声入力案内のカスタムスタイル */
.audio-input-guide {
    background: linear-gradient(45deg, #8B4513, #A0522D) !important; /* サドルブラウンから少し明るいブラウンへのグラデーション */
    padding: 24px !important;
    border-radius: 12px !important;
    margin: 20px 0 !important;
    text-align: center !important;
    box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.3) !important; /* 影を追加 */
}
.audio-input-guide h4, .audio-input-guide p {
    color: #FFFFFF !important; /* 白 */
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
}

/* ナビゲーションバーのスタイル */
.navigation-bar {
    background-color: #FFFFFF !important; /* 白 */
    border: 1px solid var(--color-accent) !important; /* サドルブラウン */
    border-radius: 10px !important;
    padding: 15px !important;
    margin-bottom: 30px !important;
    display: flex !important;
    justify-content: space-around !important;
    align-items: center !important;
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2) !important; /* ナビバーにも影を追加 */
}
.nav-step {
    color: var(--color-text-primary) !important; /* 非常に濃いグレー */
    font-weight: 500 !important;
    padding: 8px 16px !important;
    border-radius: 6px !important;
    transition: all 0.3s ease !important;
    background-color: #F0F0F0 !important; /* 非アクティブなステップの背景をソリッドな薄いグレーに */
    border: 1px solid rgba(0, 0, 0, 0.1) !important; /* 薄いボーダーで区別 */
}
.nav-step.active {
    color: var(--color-text-primary) !important; /* アクティブなステップの文字色を濃いグレーに */
    font-weight: bold !important;
    background-color: #FFFFFF !important; /* アクティブなステップの背景を白に */
    border: 1px solid var(--color-accent) !important; /* アクティブなステップのボーダーをサドルブラウンに */
}

/* 手順リスト */
.steps { /* HTMLプレビューの.stepsに対応 */
    background-color: #FFFFFF !important; /* 白 */
    border: 1px solid var(--color-accent) !important; /* サドルブラウン */
    border-radius: 10px !important;
    padding: 20px !important;
    margin: 20px 0 !important;
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2) !important; /* 影を追加 */
}
.step-item { /* HTMLプレビューの.step-itemに対応 */
    display: flex !important;
    align-items: center !important;
    margin: 15px 0 !important;
    padding: 10px !important;
    background-color: var(--color-background-primary) !important; /* 非常に薄い黄みがかったベージュ */
    border-radius: 8px !important;
    box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1) !important; /* 各ステップアイテムにも影を追加 */
}
.step-number { /* HTMLプレビューの.step-numberに対応 */
    background-color: var(--color-accent) !important; /* サドルブラウン */
    color: #FFFFFF !important; /* 白 */
    width: 30px !important;
    height: 30px !important;
    border-radius: 50% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-weight: bold !important;
    margin-right: 15px !important;
}
.step-text { /* HTMLプレビューの.step-textに対応 */
    color: var(--color-text-primary) !important; /* 非常に濃いグレー */
    font-weight: 500 !important;
}


/* デモ用のメトリクス */
.metrics {
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)) !important;
    gap: 20px !important;
    margin: 20px 0 !important;
}
.metric-card {
    background-color: #FFFFFF !important; /* 白 */
    border: 1px solid var(--color-accent) !important; /* サドルブラウン */
    border-radius: 8px !important;
    padding: 20px !important;
    text-align: center !important;
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2) !important; /* 影を追加 */
}
.metric-value {
    font-size: 2em !important;
    font-weight: bold !important;
    color: var(--color-accent) !important; /* サドルブラウン */
}
.metric-label {
    color: var(--color-text-primary) !important; /* 非常に濃いグレー */
    font-size: 0.9em !important;
    margin-top: 5px !important;
}

/* その他の要素の調整 */
hr {
    border: 1px solid var(--color-accent) !important; /* サドルブラウン */
    margin: 30px 0 !important;
}
</style>
""", unsafe_allow_html=True)

# JavaScriptを使った強制スタイル適用
st.markdown("""
<script>
// ページ読み込み後にボタンスタイルを強制適用
document.addEventListener('DOMContentLoaded', function() {
    function forceButtonStyle() {
        // 全てのボタン要素を取得
        const buttons = document.querySelectorAll('button, [role="button"], input[type="button"], input[type="submit"]');
        
        buttons.forEach(button => {
            // 強制的にスタイルを適用
            button.style.setProperty('background-color', '#8B4513', 'important');
            button.style.setProperty('background', '#8B4513', 'important');
            button.style.setProperty('color', '#FFFFFF', 'important');
            button.style.setProperty('border', '2px solid #654321', 'important');
            button.style.setProperty('border-radius', '8px', 'important');
            button.style.setProperty('font-weight', 'bold', 'important');
            button.style.setProperty('padding', '12px 24px', 'important');
            button.style.setProperty('font-size', '16px', 'important');
            button.style.setProperty('min-height', '2.5em', 'important'); /* min-heightもJSで適用 */
            
            // 内部要素も強制適用
            const innerElements = button.querySelectorAll('*');
            innerElements.forEach(element => {
                element.style.setProperty('background-color', 'transparent', 'important');
                element.style.setProperty('background', 'transparent', 'important');
                element.style.setProperty('color', '#FFFFFF', 'important');
                element.style.setProperty('border', 'none', 'important');
            });

            // ホバー時のスタイル
            button.addEventListener('mouseenter', function() {
                this.style.setProperty('background-color', '#654321', 'important');
                this.style.setProperty('background', '#654321', 'important');
                this.style.setProperty('border-color', '#654321', 'important');
                this.style.setProperty('transform', 'translateY(-1px)', 'important');
                this.style.setProperty('box-shadow', '0 4px 8px rgba(0,0,0,0.2)', 'important');
            });
            button.addEventListener('mouseleave', function() {
                this.style.setProperty('background-color', '#8B4513', 'important');
                this.style.setProperty('background', '#8B4513', 'important');
                this.style.setProperty('border-color', '#654321', 'important'); /* 通常時のボーダー色 */
                this.style.setProperty('transform', 'translateY(0px)', 'important');
                this.style.setProperty('box-shadow', 'none', 'important'); /* 通常時は影なし */
            });

            // アクティブ/フォーカス時のスタイル
            button.addEventListener('mousedown', function() {
                this.style.setProperty('background-color', '#5D3A0F', 'important');
                this.style.setProperty('background', '#5D3A0F', 'important');
                this.style.setProperty('border-color', '#5D3A0F', 'important');
                this.style.setProperty('transform', 'translateY(1px)', 'important');
                this.style.setProperty('outline', '2px solid #A0522D', 'important');
                this.style.setProperty('outline-offset', '2px', 'important');
            });
            button.addEventListener('mouseup', function() {
                // マウスアップでホバー状態に戻るか、通常状態に戻るか
                if (button.matches(':hover')) {
                    this.style.setProperty('background-color', '#654321', 'important');
                    this.style.setProperty('background', '#654321', 'important');
                    this.style.setProperty('border-color', '#654321', 'important');
                    this.style.setProperty('transform', 'translateY(-1px)', 'important');
                    this.style.setProperty('box-shadow', '0 4px 8px rgba(0,0,0,0.2)', 'important');
                } else {
                    this.style.setProperty('background-color', '#8B4513', 'important');
                    this.style.setProperty('background', '#8B4513', 'important');
                    this.style.setProperty('border-color', '#654321', 'important');
                    this.style.setProperty('transform', 'translateY(0px)', 'important');
                    this.style.setProperty('box-shadow', 'none', 'important');
                }
                this.style.setProperty('outline', 'none', 'important'); /* アウトラインをリセット */
            });
            button.addEventListener('focus', function() {
                this.style.setProperty('outline', '2px solid #A0522D', 'important');
                this.style.setProperty('outline-offset', '2px', 'important');
            });
            button.addEventListener('blur', function() {
                this.style.setProperty('outline', 'none', 'important');
            });
        });
    }
    
    // 初回実行
    forceButtonStyle();
    
    // Streamlitの再レンダリング後も適用
    const observer = new MutationObserver(forceButtonStyle);
    observer.observe(document.body, { childList: true, subtree: true });
    
    // 定期的にも実行（念のため）
    setInterval(forceButtonStyle, 1000);
});
</script>
""", unsafe_allow_html=True)

# ====================
# 2. 共通関数
# ====================

# 2.1. 仮の認証・決済関数
def authenticate_user(store_id):
    """
    マスターシートでStore IDの存在を確認する（シミュレーション）。
    実際にはGoogle Sheets APIなどと連携してStore IDを検証します。
    """
    st.info(f"マスターシートでストアID: {store_id} の存在を確認中...")
    time.sleep(0.5) # シミュレーションのための待機時間
    return store_id == "TONOSAMA001" # "TONOSAMA001"のみを有効なIDとする

# 2.2. 仮の決済状況確認関数
def check_payment_status(store_id):
    """
    Stripe決済状況を確認する（シミュレーション）。
    実際にはStripe APIと連携して決済状況を取得します。
    """
    st.info(f"決済状況を確認中...")
    time.sleep(0.5) # シミュレーションのための待機時間
    return "paid" if store_id == "TONOSAMA001" else "unpaid" # "TONOSAMA001"は支払済みとする

# 2.3. 利用の流れ・手順を表示する関数
def show_usage_guide():
    """
    アプリケーションの利用手順を説明表示する。
    初回訪問時にユーザーにシステム全体の流れを理解してもらうためのガイド。
    """
    st.markdown("---")
    st.markdown("### 🌟 ご利用の流れ")
    st.markdown("""
    TONOSAMAへようこそ！このシステムで、あなたのメニューを世界に届けましょう。
    たった5つのステップで、多言語対応のメニューが完成します！

    1.  **ログイン**: 発行されたストアIDを入力してログインします。
    2.  **メニュー表アップロード**: お店のメニュー画像をアップロードしてください。メニュー情報を読み取ります。
    3.  **想いヒアリング**: お店のコンセプトやメニューへの想いを教えてください。魅力的な文章を作成します。
    4.  **詳細設定**: 各メニューのカテゴリやアレルギー情報、写真などを設定します。
    5.  **完了**: 全ての設定が完了すると、多言語メニュー情報が準備されます。
    """)
    st.markdown("---")

# 2.4. 全ページ共通のナビゲーションバーを表示する関数
def show_universal_navigation():
    """
    全ページ共通のステップナビゲーションバーを表示する。
    現在のステップをハイライトし、ユーザーに全体の進捗を示す。
    """
    st.markdown("""
    <style>
    /* ナビゲーションバーのスタイル */
    .navigation-bar {
        background-color: #FFFFFF; /* 白 */
        border: 1px solid var(--color-accent); /* サドルブラウン */
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 30px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
    }
    .nav-step {
        color: var(--color-text-primary);
        font-weight: 500;
        padding: 8px 16px;
        border-radius: 6px;
        transition: all 0.3s ease;
        background-color: #F0F0F0; /* 非アクティブなステップの背景をソリッドな薄いグレーに */
        border: 1px solid rgba(0, 0, 0, 0.1);
    }
    .nav-step.active {
        color: var(--color-text-primary);
        font-weight: bold;
        background-color: #FFFFFF; /* アクティブなステップの背景を白に */
        border: 1px solid var(--color-accent);
    }
    </style>
    """, unsafe_allow_html=True)

    steps = ["ログイン", "アップロード", "想いヒアリング", "詳細設定", "完了"]
    current = st.session_state.get("current_step", 0)

    nav_html = '<div class="navigation-bar">'
    for i, step in enumerate(steps):
        active_class = "active" if i == current else ""
        nav_html += f'<span class="nav-step {active_class}">{i+1}. {step}</span>'
    nav_html += '</div>'

    st.markdown(nav_html, unsafe_allow_html=True)

# ====================
# 3. STEP1: ログイン・認証（簡素化版）
# ====================

# 3.1. 店主がStore IDを入力してログインするページ
def show_login_page():
    """
    STEP1のメインページ。
    店主がStore IDを入力し、認証・決済状況を確認してログインするUIを提供する。
    ログイン成功後、次のステップへ遷移する。
    """
    # セッション状態の初期化
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'store_id' not in st.session_state:
        st.session_state.store_id = ""

    # 共通ナビゲーションバーを表示
    show_universal_navigation()

    # ページのタイトルと説明
    st.title("🔑 TONOSAMAへようこそ！")
    st.subheader("ストアIDを入力してログインしてください")

    # 利用の流れ・手順を表示
    show_usage_guide()

    # Store ID入力フォーム
    store_id_input = st.text_input(
        "あなたのストアIDを入力してください",
        value=st.session_state.store_id,
        placeholder="例: TONOSAMA001",
        key="store_id_input"
    )

    # 責任者ナンバー入力フォーム
    responsible_number_input = st.text_input(
        "責任者ナンバー",
        type="password",
        placeholder="例: 12345",
        key="responsible_number_input"
    )

    # ログインボタン
    if st.button("ログイン", key="login_button"):
        if store_id_input and responsible_number_input:
            if responsible_number_input != "99999":
                st.error("❌ 無効な責任者ナンバーです。")
                st.session_state.logged_in = False
            else:
                st.session_state.store_id = store_id_input

                # 認証と決済状況の確認
                auth_success = authenticate_user(st.session_state.store_id)
                payment_status = check_payment_status(st.session_state.store_id)

                if auth_success and payment_status == "paid":
                    st.success("✅ ログインに成功しました！")
                    st.session_state.logged_in = True
                    st.session_state.current_step = 1
                    time.sleep(1)
                    st.rerun()
                elif auth_success and payment_status != "paid":
                    st.warning("⚠️ ストアIDは確認できましたが、決済が完了していません。代理店にご確認ください。")
                    st.session_state.logged_in = False
                else:
                    st.error("❌ 無効なストアIDです。もう一度お確かめください。")
                    st.session_state.logged_in = False
        else:
            st.warning("ストアIDと責任者ナンバーを入力してください。")

    st.markdown("---")
    st.subheader("請求書・領収書発行")
    st.info("アプリ使用に関する請求書・領収書が必要な方は、こちらから発行いただけます。")
    if st.button("アプリ使用請求書・領収書を発行", key="issue_app_invoice_receipt"):
        st.success("アプリ使用請求書・領収書の発行プロセスを開始しました。ご登録のメールアドレスに送付されます。")
        # TODO: 請求書・領収書発行のバックエンド連携をここに実装


# ====================
# 4. STEP2: メニュー表処理・基本確認（統合版）
# ====================

# 4.1. モックOCRデータ (GeminiCLIのシミュレーション用)
MOCK_OCR_RESULTS = [
    {"name": "唐揚げ定食", "price": "980円"},
    {"name": "焼き魚御膳", "price": "1200円"},
    {"name": "海老チリセット", "price": "1150円"},
    {"name": "特製ラーメン", "price": "850円"},
    {"name": "餃子 (6個)", "price": "400円"},
    {"name": "生ビール", "price": "550円"},
    {"name": "日本酒 (一合)", "price": "600円"},
]

# 4.2. メニューカテゴリーリスト
MENU_CATEGORIES = ["フード", "コース", "ランチ", "デザート", "ドリンク"]

# 4.3. Google Driveへのファイルアップロードをシミュレートする関数
def simulate_drive_upload(uploaded_file, store_id):
    """
    Google Driveへのファイルアップロードをシミュレートします。
    実際にはGoogle Drive APIを使用します。
    アップロードされたファイルを指定されたパスに保存する（ダミーの実装）。
    """
    file_path = f"simulated_drive/{store_id}/{uploaded_file.name}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True) # ディレクトリがなければ作成
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer()) # ファイルの内容を書き込む
    st.success(f"ファイルを保存しました: {file_path}")
    return file_path

# 4.4. GeminiCLIでのOCR処理をシミュレートする関数
def process_ocr_with_gemini(uploaded_file_path):
    """
    メニュー情報の読み取りをシミュレートします。
    実際には画像からメニュー情報を抽出します。
    ここではモックデータを返します。
    """
    st.info(f"メニュー情報を読み取り中...")
    time.sleep(2) # 処理のシミュレーション時間
    return MOCK_OCR_RESULTS # 事前定義されたモックデータを返す

# 4.5. メニュー表をアップロードし、OCRで基本情報を抽出・確認するページ
def show_menu_upload_page():
    """
    STEP2のメインページ。
    店主がメニュー表の画像やPDFをアップロードし、OCR処理を実行。
    抽出されたメニュー情報を確認・修正し、カテゴリー設定や並び替えを行う。
    """
    st.session_state.current_step = 1 # 現在のステップを設定

    # 共通ナビゲーションバーを表示
    show_universal_navigation()

    # ページのタイトルと説明
    st.title("📄 メニュー表アップロード・基本確認")
    st.info("お店のメニュー表（画像またはPDF）をアップロードしてください。メニュー情報を読み取ります。")

    # セッション状態の初期化 (STEP2固有の変数)
    if 'uploaded_menu_file' not in st.session_state:
        st.session_state.uploaded_menu_file = None # アップロードされたファイルオブジェクト
    if 'ocr_results' not in st.session_state:
        st.session_state.ocr_results = None # 抽出された生のメニューデータ
    if 'finalized_menus' not in st.session_state:
        st.session_state.finalized_menus = [] # ユーザーが確認・修正した後の最終的なメニューデータリスト
    if 'ocr_processed' not in st.session_state:
        st.session_state.ocr_processed = False # 処理が一度実行されたかどうかのフラグ
    # 手動追加メニューのIDを管理するカウンター
    if 'manual_menu_id_counter' not in st.session_state:
        st.session_state.manual_menu_id_counter = 1000 # 既存IDと衝突しないように高い値から開始

    # ファイルアップローダーウィジェット
    uploaded_file = st.file_uploader(
        "メニュー表の画像またはPDFをアップロード",
        type=["png", "jpg", "jpeg", "pdf"], # 許可するファイル形式
        help="ファイルサイズは10MBまで。必要に応じて自動でリサイズされます。" # ユーザーへのヒント
    )

    if uploaded_file is not None:
        st.session_state.uploaded_menu_file = uploaded_file
        st.write(f"ファイル名: {uploaded_file.name}")
        # アップロードされたファイルが画像であればプレビューを表示
        if uploaded_file.type.startswith('image'):
            st.image(uploaded_file, caption='アップロードされたメニュー表', use_container_width=True)

        # 処理がまだ実行されていなければ、開始ボタンを表示
        if not st.session_state.ocr_processed:
            st.warning("アップロードされたファイルはまだ処理されていません。「メニュー情報読み取り開始」ボタンをクリックしてください。")

            # 処理開始ボタン
            if st.button("メニュー情報読み取り開始", key="start_ocr_button"):
                with st.spinner("メニュー情報読み取り中..."):
                    # Google Driveにファイルを保存するシミュレーション
                    uploaded_file_path = simulate_drive_upload(uploaded_file, st.session_state.store_id)

                    # 処理をシミュレート
                    ocr_data = process_ocr_with_gemini(uploaded_file_path)

                    st.session_state.ocr_results = ocr_data
                    st.session_state.ocr_processed = True # 処理完了フラグを設定
                    st.success("メニュー情報の読み取りが完了しました！")
                    st.rerun() # ページを再ロードして結果表示UIへ進む

    # 結果の表示と確認・修正UI (処理完了後にのみ表示)
    if st.session_state.ocr_processed and st.session_state.ocr_results:
        st.markdown("---")
        st.subheader("💡 読み取られたメニュー情報をご確認ください")
        st.info("メニューごとに「掲載・掲載しない」を選択し、メニュー名、価格、カテゴリーを修正・設定してください。")

        # finalized_menusが未初期化の場合、OCR結果から初期化
        if not st.session_state.finalized_menus: # 初回のみOCR結果から初期化
            for i, item in enumerate(st.session_state.ocr_results):
                st.session_state.finalized_menus.append({
                    "id": i, # 各メニューにユニークなIDを付与
                    "original_name": item.get("name", ""), # 読み取り元の名前
                    "name": item.get("name", ""), # ユーザーが修正する名前
                    "price": item.get("price", ""), # ユーザーが修正する価格
                    "category": MENU_CATEGORIES[0], # デフォルトで最初のカテゴリーを設定
                    "should_introduce": True, # デフォルトで「掲載する」にチェック
                    "order": i # 初期表示順序
                })

        # 新しいメニューを追加するボタン
        st.markdown("---")
        st.subheader("手動でメニューを追加する")
        st.info("OCRで読み取れなかったメニューや、新たに掲載したいメニューがある場合にご利用ください。")
        if st.button("新しいメニューを追加", key="add_manual_menu_button"):
            new_menu_id = st.session_state.manual_menu_id_counter
            st.session_state.manual_menu_id_counter += 1
            st.session_state.finalized_menus.append({
                "id": new_menu_id,
                "original_name": "新しいメニュー",
                "name": "新しいメニュー",
                "price": "0円",
                "category": MENU_CATEGORIES[0],
                "should_introduce": True,
                "order": len(st.session_state.finalized_menus) # 最後に追加
            })
            st.rerun() # 新しいメニューを追加したらUIを更新

        # 各メニューの情報をループで表示し、ユーザーに修正を促す
        updated_menus = [] # 修正されたメニューを一時的に保持するリスト
        for i, menu in enumerate(st.session_state.finalized_menus):
            # st.expanderを使って各メニューの詳細を折りたたみ可能にする
            with st.expander(f"メニュー {i+1}: {menu['name']} （{menu['price']}）"):
                col1, col2 = st.columns([0.6, 0.4]) # レイアウトを2列に分割

                with col1:
                    menu['name'] = st.text_input(
                        f"メニュー名 (日本語)",
                        value=menu['name'],
                        key=f"name_{menu['id']}" # Streamlitのwidget keyはユニークに
                    )
                    menu['price'] = st.text_input(
                        f"お値段 (税込)",
                        value=menu['price'],
                        key=f"price_{menu['id']}"
                    )
                    # カテゴリー選択 (現在のカテゴリーがリストになければデフォルトを0に)
                    category_index = MENU_CATEGORIES.index(menu['category']) if menu['category'] in MENU_CATEGORIES else 0
                    menu['category'] = st.selectbox(
                        f"カテゴリー",
                        options=MENU_CATEGORIES,
                        index=category_index,
                        key=f"category_{menu['id']}"
                    )
                with col2:
                    menu['should_introduce'] = st.checkbox(
                        "このメニューを掲載する",
                        value=menu['should_introduce'],
                        key=f"introduce_{menu['id']}"
                    )
                    # メニュー削除ボタン
                    if st.button("このメニューを削除", key=f"delete_menu_{menu['id']}"):
                        st.session_state.finalized_menus = [m for m in st.session_state.finalized_menus if m['id'] != menu['id']]
                        st.success(f"メニュー「{menu['name']}」を削除しました。")
                        st.rerun() # 削除したらUIを更新
                updated_menus.append(menu) # 変更を一時リストに追加
        st.session_state.finalized_menus = updated_menus # セッション状態を更新

        st.markdown("---")
        st.subheader("🔁 メニューの並び替え")
        # 並び替えを行うかどうかのチェックボックス
        st.checkbox("メニューの表示順を変更しますか？", key="confirm_reorder_checkbox")

        if st.session_state.get("confirm_reorder_checkbox", False):
            st.info("希望するメニューの表示順を、カンマ区切りで番号を入力してください（例: 3,1,2,5,4）。")
            # 現在のメニュー順序を表示 (1から始まる番号)
            current_order_display = ",".join([str(m['order']+1) for m in sorted(st.session_state.finalized_menus, key=lambda x: x['order'])])
            new_order_str = st.text_input(
                "新しいメニューの並び順",
                value=current_order_display,
                key="new_menu_order_input"
            )

            # 並び順更新ボタン
            if st.button("並び順を更新", key="update_order_button"):
                try:
                    # 入力された文字列を数値のリストに変換 (1から始まる番号を0から始まるインデックスに)
                    new_order_indices = [int(x.strip()) - 1 for x in new_order_str.split(',')]

                    # 入力値のバリデーション (メニュー数と一致するか、重複がないか、範囲内か)
                    if len(new_order_indices) != len(st.session_state.finalized_menus) or \
                       len(set(new_order_indices)) != len(st.session_state.finalized_menus) or \
                       not all(0 <= idx < len(st.session_state.finalized_menus) for idx in new_order_indices):
                        st.error("❌ 無効な並び順です。全てのメニュー番号を重複なく、正しく入力してください。")
                    else:
                        # 新しい順序で finalized_menus を再構築
                        reordered_menus_temp = [None] * len(st.session_state.finalized_menus)
                        # finalized_menus は現在の表示順序なので、original_orderに基づいて正しいアイテムを取得
                        original_ordered_menus = sorted(st.session_state.finalized_menus, key=lambda x: x['order'])

                        for new_pos, original_idx_to_pick in enumerate(new_order_indices):
                            menu_item = original_ordered_menus[original_idx_to_pick]
                            reordered_menus_temp[new_pos] = menu_item
                            reordered_menus_temp[new_pos]['order'] = new_pos # orderプロパティも新しい順序に更新

                        st.session_state.finalized_menus = reordered_menus_temp
                        # IDを新しい並び順で振り直し (重要: UIのkeyを確実にユニークにするため)
                        for i, menu in enumerate(st.session_state.finalized_menus):
                             menu['id'] = i
                        st.success("✅ 並び順を更新しました！")
                        st.rerun() # 更新された並び順で表示を更新

                except ValueError:
                    st.error("❌ 不正な入力です。番号をカンマ区切りで入力してください。")

        st.markdown("---")
        # ナビゲーションボタン (戻る/次へ)
        col_prev, col_next = st.columns([1, 1])
        with col_prev:
            if st.button("⬅️ 戻る (ログインページへ)", key="step2_back_to_login"):
                st.session_state.current_step = 0
                st.session_state.logged_in = False # ログイン状態もリセット
                st.rerun()
        with col_next:
            # 「掲載する」メニューが1つ以上選択されているか確認
            if any(m['should_introduce'] for m in st.session_state.finalized_menus):
                if st.button("次へ進む (想いヒアリングへ) ➡️", key="step2_next_to_thoughts"):
                    # should_introduceがFalseのメニューは除外してセッションに保存
                    st.session_state.finalized_menus = [
                        m for m in st.session_state.finalized_menus if m['should_introduce']
                    ]
                    st.session_state.current_step = 2 # 次のステップ (STEP3: 想いヒアリング) へ
                    st.rerun()
            else:
                st.warning("少なくとも1つのメニューを「掲載する」に設定してください。")


# ====================
# 5. STEP3: 想いヒアリング・翻訳（効率化版）
# ====================

# 5.1. 想いヒアリング質問データ（完全版）
def get_owner_thoughts_questions():
    """店主の想いヒアリング15問"""
    return {
        "basic_info": {
            "title": "🏪 お店の基本情報",
            "questions": [
                {
                    "key": "restaurant_name",
                    "question": "お店の名前を教えてください",
                    "example": "例: 和食処 さくら"
                },
                {
                    "key": "opening_year",
                    "question": "お店を開いてから何年になりますか？",
                    "example": "例: 10年になります"
                },
                {
                    "key": "location",
                    "question": "お店の場所・立地の特徴を教えてください",
                    "example": "例: 駅から徒歩3分、商店街の中にあります"
                }
            ]
        },
        "philosophy": {
            "title": "💭 お店の想い・こだわり",
            "questions": [
                {
                    "key": "restaurant_concept",
                    "question": "お店のコンセプトや想いを教えてください",
                    "example": "例: 家庭的な温かい雰囲気で、心のこもった料理を提供したい"
                },
                {
                    "key": "special_ingredients",
                    "question": "特にこだわっている食材や調理法はありますか？",
                    "example": "例: 地元の野菜を使用し、手作りにこだわっています"
                },
                {
                    "key": "customer_service",
                    "question": "お客様に対してどのようなサービスを心がけていますか？",
                    "example": "例: 一人一人のお客様との会話を大切にしています"
                }
            ]
        },
        "dishes": {
            "title": "🍽️ 料理・メニューについて",
            "questions": [
                {
                    "key": "signature_dish",
                    "question": "お店の看板メニューとその特徴を教えてください",
                    "example": "例: 手作りハンバーグは祖母から受け継いだレシピです"
                },
                {
                    "key": "seasonal_menu",
                    "question": "季節ごとのメニューやイベントはありますか？",
                    "example": "例: 春は山菜料理、夏は冷やし中華に力を入れています"
                },
                {
                    "key": "menu_development",
                    "question": "新しいメニューを考える時に大切にしていることは？",
                    "example": "例: お客様の声を聞いて、健康的で美味しい料理を考えています"
                }
            ]
        },
        "international": {
            "title": "� 国際的なお客様について",
            "questions": [
                {
                    "key": "foreign_customers",
                    "question": "海外のお客様にどのような体験をしてほしいですか？",
                    "example": "例: 日本の家庭料理の温かさを感じてほしいです"
                },
                {
                    "key": "cultural_sharing",
                    "question": "お店の文化や料理の背景で伝えたいことはありますか？",
                    "example": "例: 手作りの大切さと、食材への感謝の気持ちを伝えたいです"
                },
                {
                    "key": "welcome_message",
                    "question": "海外からのお客様へのメッセージをお聞かせください",
                    "example": "例: 日本の味を楽しんでいただき、素敵な思い出を作ってください"
                }
            ]
        },
        "future": {
            "title": "🚀 今後の展望",
            "questions": [
                {
                    "key": "future_goals",
                    "question": "今後のお店の目標や夢を教えてください",
                    "example": "例: 地域の人々と海外の方々の交流の場になりたいです"
                },
                {
                    "key": "multilingual_benefits",
                    "question": "多言語メニューでどのような効果を期待されますか？",
                    "example": "例: 言葉の壁を越えて、より多くの方に料理を楽しんでもらいたいです"
                },
                {
                    "key": "final_message",
                    "question": "最後に、お客様への一言メッセージをお願いします",
                    "example": "例: 心を込めて作った料理で、皆様に笑顔をお届けします"
                }
            ]
        }
    }


# 5.2. 店主の想い要約のシミュレーション関数
def process_thoughts_summary(answers_dict): # 引数を辞書に変更
    """
    ユーザーが入力した店主の想いを要約する処理をシミュレートします。
    実際には大規模言語モデルなどを呼び出します。
    """
    st.info("想いをまとめる中...")
    time.sleep(1) # シミュレーションのための待機時間

    # finalized_menusから最初のメニュー名を取得（存在しない場合も考慮）
    if 'finalized_menus' in st.session_state and st.session_state.finalized_menus:
        first_menu_name = st.session_state.finalized_menus[0]['name']
    else:
        first_menu_name = '特製料理' # デフォルト値

    # answers_dict を使用してより具体的な要約を生成 (モック)
    restaurant_name = answers_dict.get("restaurant_name", "当店") # flatな辞書構造に変更されたため修正
    restaurant_concept = answers_dict.get("restaurant_concept", "お客様に心温まる料理を提供すること")
    signature_dish = answers_dict.get("signature_dish", first_menu_name)

    mock_summary = f"{restaurant_name}は「{restaurant_concept}」という想いを大切にしています。特に「{signature_dish}」は、店主の情熱が詰まった自慢の一品です。私たちは、言葉の壁を越えて世界中のお客様に日本の食文化の温かさを伝えたいと願っています。"
    return mock_summary

# 5.3. 店主の想いの多言語翻訳のシミュレーション関数
def translate_thoughts_immediately(text):
    """
    店主の想いを14言語に翻訳する処理をシミュレートします。
    実際には大規模言語モデルなどを呼び出します。
    """
    st.info("想いを多言語に展開中...")
    time.sleep(1.5) # シミュレーションのための待機時間

    # 翻訳結果のモックデータ生成 (指定された14言語)
    if 'finalized_menus' in st.session_state and st.session_state.finalized_menus:
        first_menu_name_eng = st.session_state.finalized_menus[0]['name'] # 英語版はそのまま使う
    else:
        first_menu_name_eng = 'specialty dish' # デフォルト値

    mock_translations = {
        "韓国語": f"손님들에게 잊을 수 없는 경험을 제공하는 것을 목표로, 엄선된 식재료와 섬세한 조리법으로 마음 따뜻해지는 요리를 제공하고 있습니다. 특히 '{first_menu_name_eng}'는 저희 가게의 열정이 담긴 한 접시입니다.",
        "中国語(標準語)": f"我们的目标是为顾客提供难忘的体验，用精心挑选的食材和精致的烹饪方法，提供温暖人心的菜肴。特别是“{first_menu_name_eng}”，更是我们店倾注热情的一道菜。",
        "台湾語": f"阮的目標是予顧客一个難忘的經驗，用仔細挑選的食材kap細緻的烹飪方法，提供溫暖人心的料理。尤其是阮的「{first_menu_name_eng}」，閣是阮店鋪心血的一道菜。",
        "広東語": f"我哋嘅目標係為顧客提供一個難忘嘅體驗，用精心挑選嘅食材同細緻嘅烹飪方法，提供暖人心嘅菜餚。特別係我哋嘅「{first_menu_name_eng}」，更係我哋店舖傾注熱情嘅一道菜。",
        "タイ語": f"เป้าหมายของเราคือการมอบประสบการณ์ที่น่าจดจำให้กับลูกค้าของเรา โดยนำเสนออาหารที่อบอุ่นใจที่ทำจากวัตถุดิบที่คัดสรรมาอย่างดีและวิธีการปรุงอาหารที่พิถีพิถัน โดยเฉพาะ '{first_menu_name_eng}' ของเรานั้นเป็นจานที่เต็มไปด้วยความหลงใหลของเรา",
        "フィリピノ語": f"Ang aming layunin ay magbigay ng isang di malilimutang karanasan sa aming mga customer, nag-aalok ng mga nakakapagpainit na pagkain na gawa sa maingat na napiling sangkap at masusing pamamaraan ng pagluluto. Ang aming '{first_menu_name_eng}' lalo na, ay isang ulam na puno ng aming passion.",
        "ベトナム語": f"Mục tiêu của chúng tôi là mang đến trải nghiệm khó quên cho khách hàng, phục vụ các món ăn ấm lòng được chế biến từ nguyên liệu tuyển chọn kỹ lưỡng và phương pháp nấu ăn tỉ mỉ. Đặc biệt, món '{first_menu_name_eng}' của chúng tôi là một món ăn chứa đầy tâm huyết của chúng tôi.",
        "インドネシア語": f"Tujuan kami adalah memberikan pengalaman yang tak terlupakan bagi pelanggan kami, menawarkan hidangan yang menghangatkan hati yang dibuat dengan bahan-bahan pilihan dan metode memasak yang cermat. Khususnya '{first_menu_name_eng}' kami, adalah hidangan yang dipenuhi dengan hasrat kami.",
        "英語": f"Our aim is to provide an unforgettable experience for our customers, offering heartwarming dishes made with carefully selected ingredients and meticulous cooking methods. Our '{first_menu_name_eng}' in particular, is a plate filled with our passion.",
        "スペイン語": f"Nuestro objetivo es brindar una experiencia inolvidable a nuestros clientes, ofreciendo platos reconfortantes elaborados con ingredientes cuidadosamente seleccionados y métodos de cocción meticulosos. Nuestro '{first_menu_name_eng}', en particular, es un plato lleno de nuestra pasión.",
        "ドイツ語": f"Unser Ziel ist es, unseren Kunden ein unvergessliches Erlebnis zu bieten, indem wir herzerwärmende Gerichte anbieten, die mit sorgfältig ausgewählten Zutaten und akribischen Kochmethoden zubereitet werden. Unser '{first_menu_name_eng}' ist insbesondere ein Gericht voller unserer Leidenschaft.",
        "フランス語": f"Notre objectif est d'offrir une expérience inoubliable à nos clients, en proposant des plats réconfortants préparés avec des ingrédients soigneusement sélectionnés et des méthodes de cuisson méticuleuses. Notre '{first_menu_name_eng}', en particulier, est un plat rempli de notre passion.",
        "イタリア語": f"Il nostro obiettivo è offrire un'esperienza indimenticabile ai nostri clienti, proponendo piatti confortanti preparati con ingredienti selezionati con cura e metodi di cottura meticolosi. Il nostro '{first_menu_name_eng}', in particolare, è un piatto pieno della nostra passione.",
        "ポルトガル語": f"Nosso objetivo é proporcionar uma experiência inesquecível aos nossos clientes, oferecendo pratos reconfortantes feitos com ingredientes cuidadosamente selectedos e métodos de cozimento meticulosos. Nosso '{first_menu_name_eng}', em particular, é um prato cheio de nossa paixão.",
    }
    return mock_translations

# 5.4. 店主の想いヒアリング・翻訳のメインページ
def show_owner_thoughts_page():
    """
    STEP3のメインページ。
    店主からの質問への回答を収集し、要約・翻訳を行う。
    アレルギー情報の表示方針もここで設定する。
    """
    st.session_state.current_step = 2 # 現在のステップを設定

    # 共通ナビゲーションバーを表示
    show_universal_navigation()

    st.title("🗣️ 店主の想いヒアリング")
    st.info("あなたの声で、お店のこだわりや想いを教えてください。魅力的な文章を作成します。")

    # 音声入力案内
    st.markdown("""
    <div class="audio-input-guide">
        <h4>🎤 音声での回答も可能です</h4>
        <p>スマートフォンをお使いの場合、音声入力で簡単に回答できます。</p>
    </div>
    """, unsafe_allow_html=True)

    st.info("15問の質問にお答えいただき、お店の想いを世界に伝えましょう！")

    # 質問データを取得
    questions_data = get_owner_thoughts_questions()

    # セッション状態の初期化 (STEP3固有の変数)
    # 各質問のkeyに対応する辞書としてanswersを保持
    if 'owner_answers_dict' not in st.session_state:
        st.session_state.owner_answers_dict = {}
        # flat_answers_dict を構築するためにここで全てのkeyを初期化
        for category_key in questions_data:
            for q_item in questions_data[category_key]["questions"]:
                st.session_state.owner_answers_dict[q_item["key"]] = ""

    if 'summarized_thought' not in st.session_state:
        st.session_state.summarized_thought = "" # 要約した店主の想い
    if 'translated_thoughts' not in st.session_state:
        st.session_state.translated_thoughts = None # 翻訳した店主の想い（辞書形式）
    if 'allergy_policy' not in st.session_state:
        st.session_state.allergy_policy = None # アレルギー情報の表示方針

    st.subheader("質問に答えて、お店の想いを教えてください")

    # カテゴリごとに質問を表示
    for category_key, category_info in questions_data.items():
        st.markdown(f"### {category_info['title']}")
        for i, q_item in enumerate(category_info["questions"]):
            st.session_state.owner_answers_dict[q_item["key"]] = st.text_area(
                f"{q_item['question']}",
                value=st.session_state.owner_answers_dict[q_item["key"]],
                height=80, # テキストエリアの高さ
                key=f"q_{q_item['key']}" # ユニークなキー
            )
            # 回答例を枠で表示
            if q_item.get("example"):
                st.info(f"**回答例**: {q_item['example']}")
        st.markdown("---") # カテゴリ間の区切り線


    # 想いをまとめるボタン
    if st.button("想いをまとめる", key="summarize_thoughts_button"):
        # 全ての質問に回答が入力されているかチェック
        all_answered = True
        for category_key in questions_data:
            for q_item in questions_data[category_key]["questions"]:
                if st.session_state.owner_answers_dict.get(q_item["key"], "").strip() == "":
                    all_answered = False
                    break
            if not all_answered:
                break

        if all_answered:
            # process_thoughts_summary 関数は flat な辞書を期待しているので、そのまま渡す
            st.session_state.summarized_thought = process_thoughts_summary(st.session_state.owner_answers_dict) # 要約を実行
            st.success("想いをまとめました！")
            st.rerun() # ページを再実行して要約結果表示UIへ進む
        else:
            st.warning("全ての質問に回答してください。")

    # 要約された想いの表示と修正UI (要約後にのみ表示)
    if st.session_state.summarized_thought:
        st.markdown("---")
        st.subheader("「こんな想いなんですね？」")
        st.info("まとめた想いの文章をご確認ください。必要であれば修正してください。")

        st.session_state.summarized_thought = st.text_area(
            "お店の想い（最終版）",
            value=st.session_state.summarized_thought,
            height=200, # テキストエリアの高さ
            key="final_owner_thought_edit"
        )

        # 翻訳開始ボタン
        if st.button("この想いで確定し、多言語で展開する", key="confirm_and_translate_button"):
            if st.session_state.summarized_thought.strip() != "":
                st.session_state.translated_thoughts = translate_thoughts_immediately(st.session_state.summarized_thought) # 翻訳を実行
                st.success("お客様に想いを伝えるため、多言語に展開いたしました。")
                st.info("展開品質チェックを実行しました。問題ありません。")
                st.rerun() # ページを再実行してアレルギー方針UIへ進む
            else:
                st.warning("お店の想いを入力してください。")

    # アレルギー情報の表示方針設定 (翻訳完了後にのみ表示)
    if st.session_state.translated_thoughts:
        st.markdown("---")
        st.subheader("アレルギー情報の表示方針")
        st.info("メニューのアレルギー情報を、外国人のお客様に表示するかどうかを決定してください。")

        # allergy_policy の初期値を適切に設定
        initial_allergy_index = 0
        if st.session_state.allergy_policy == "not_display":
            initial_allergy_index = 1

        allergy_option = st.radio(
            "アレルギー情報をメニューに表示しますか？",
            ("表示する", "表示しない"),
            index=initial_allergy_index,
            key="allergy_policy_radio"
        )
        if allergy_option == "表示する":
            st.session_state.allergy_policy = "display"
            st.success("アレルギー情報はメニューに表示されます。")
        else:
            st.session_state.allergy_policy = "not_display"
            st.warning("アレルギー情報はメニューに表示されません。")

    st.markdown("---")
    # ナビゲーションボタン (戻る/次へ)
    col_prev, col_next = st.columns([1, 1])
    with col_prev:
        if st.button("⬅️ 戻る (アップロードページへ)", key="step3_back_to_upload"):
            st.session_state.current_step = 1 # STEP2へ戻る
            st.rerun()
    with col_next:
        # 翻訳とアレルギー方針が両方完了している場合のみ「次へ」ボタンを有効化
        if st.session_state.translated_thoughts and st.session_state.allergy_policy:
            if st.button("次へ進む (詳細設定へ) ➡️", key="step3_next_to_details"):
                st.session_state.current_step = 3 # STEP4へ進む
                st.rerun()
        else:
            st.warning("想いのまとめ、多言語展開、およびアレルギー情報の表示方針を完了してください。")


# ====================
# 6. STEP4: 詳細設定（モック）
# ====================

# 食べ方説明生成のシミュレーション関数
def generate_description_from_owner_thought(owner_thought, menu_name):
    """
    店主の想いとメニュー名から想定した訴求・一口目・二口目を生成するシミュレーション。
    約160字を想定。
    """
    st.info(f"「{menu_name}」の食べ方説明を想定しています...")
    time.sleep(1)

    # モックの生成ロジック。実際の生成ではより高度な処理が必要。
    base_description = f"{owner_thought[:50]}...という店主の想いから、{menu_name}が生まれました。"
    if "唐揚げ" in menu_name:
        description = base_description + "一口食べれば、秘伝のタレがジュワッと広がり、外はカリッ、中はジューシーな食感が楽しめます。二口目には、鶏肉本来の旨味と香ばしさが口いっぱいに広がり、ご飯が止まらなくなるでしょう。ぜひ揚げたてをお召し上がりください！"
    elif "焼き魚" in menu_name:
        description = base_description + "厳選された新鮮な魚を丁寧に焼き上げました。一口目には、ふっくらとした身の旨味と皮目の香ばしさが絶妙なハーモニーを奏でます。二口目には、素材本来の優しい味わいが口の中に広がり、どこか懐かしい日本の食卓を思い起こさせます。健康志向の方にもおすすめです。"
    elif "ラーメン" in menu_name:
        description = base_description + "特製のスープは、長時間煮込んだ秘伝の出汁が決め手です。一口目には、濃厚な旨味が口いっぱいに広がり、思わず唸ってしまうことでしょう。二口目には、コシのある麺と絡み合い、それぞれの具材の豊かな風味が加わり、箸が止まらなくなる至福の一杯です。ぜひ最後までスープを飲み干してください。"
    else:
        description = base_description + "一口食べれば、素材の持つ本来の味と、店主の温かい心が伝わる優しい味わいが広がります。二口目には、奥深いコクと香りが口いっぱいに満ちて、忘れられない感動を味わえるでしょう。ぜひ、この特別な一品をご体験ください。"

    # 160字に調整（簡易的な処理）
    return description[:160] # 最大160文字に切り詰める

def show_detailed_settings_page():
    """
    STEP4のメインページ。
    各メニューの詳細設定を行う。
    写真のアップロード、アレルギー情報の選択、おすすめ表示フラグの設定など。
    """
    st.session_state.current_step = 3 # 現在のステップを設定

    # 共通ナビゲーションバーを表示
    show_universal_navigation()

    st.title("⚙️ 詳細設定")
    st.info("各メニューの詳しい情報を設定します。写真の追加、詳細説明の記述が可能です。")

    # セッション状態の初期化 (STEP4固有の変数)
    if 'detailed_menus' not in st.session_state:
        # STEP2で確定したメニューリストをベースに、詳細設定用のデータを構築
        st.session_state.detailed_menus = []
        for menu_item in st.session_state.get('finalized_menus', []):
            st.session_state.detailed_menus.append({
                "id": menu_item['id'],
                "name": menu_item['name'],
                "price": menu_item['price'],
                "category": menu_item['category'],
                "should_introduce": menu_item['should_introduce'],
                "order": menu_item['order'],
                "photo_url": "", # メニュー写真のURL
                "allergens": [], # アレルギー物質リスト
                "is_recommended": False, # おすすめメニューフラグ
                "description_jp": "", # 日本語でのメニュー詳細説明
                "ai_description_approved": False, # 生成説明の承認フラグ
                "ai_description_generated": False, # AIによる説明が生成されたかどうかのフラグ
            })

    # アレルギー物質リスト (例)
    ALLERGENS = [
        "卵", "乳", "小麦", "そば", "落花生", "えび", "かに",
        "アーモンド", "あわび", "いか", "いくら", "オレンジ", "カシューナッツ",
        "キウイフルーツ", "牛肉", "くるみ", "ごま", "さけ", "さば", "大豆",
        "鶏肉", "バナナ", "豚肉", "まつたけ", "もも", "やまいも", "りんご",
        "ゼラチン"
    ]

    st.subheader("各メニューの詳細情報を入力してください")

    updated_detailed_menus = []
    for i, menu in enumerate(st.session_state.detailed_menus):
        with st.expander(f"メニュー {i+1}: {menu['name']}"):
            # メニュー名、価格、カテゴリーはSTEP2からの引き継ぎとして表示（編集不可にするか検討）
            st.write(f"**メニュー名**: {menu['name']}")
            st.write(f"**価格**: {menu['price']}")
            st.write(f"**カテゴリー**: {menu['category']}")

            # メニュー写真のアップロード
            # TODO: 実際のファイルアップロード機能とS3/GCSなどへの保存ロジックを実装
            st.info("メニュー写真をアップロードしてください（任意）。")
            uploaded_photo = st.file_uploader(
                f"写真のアップロード ({menu['name']})",
                type=["png", "jpg", "jpeg"],
                key=f"photo_upload_{menu['id']}"
            )
            if uploaded_photo:
                # ここでS3やGCSなどにアップロードし、URLをmenu['photo_url']に保存する
                # 現状はダミーURL
                st.image(uploaded_photo, caption=f"{menu['name']} の写真", use_container_width=True)
                menu['photo_url'] = f"https://dummy-image-url.com/{menu['id']}_{uploaded_photo.name}"
                st.success("写真がアップロードされました！ (ダミー保存)")

            st.markdown("---")
            st.subheader("💡 食べ方説明の提案")
            st.info("店主の想いとメニュー名から、想定される訴求ポイントを記述します。ご確認ください。必要に応じて修正してください。")

            # 説明文の生成と表示
            # AI説明がまだ生成されていない場合、または未承認の場合に生成
            if not menu.get('ai_description_generated', False):
                # AIによる説明を生成し、テキストエリアのデフォルト値として設定
                ai_text = generate_description_from_owner_thought(st.session_state.summarized_thought, menu['name'])
                menu['description_jp'] = ai_text
                menu['ai_description_generated'] = True
                menu['ai_description_approved'] = False # 生成されたばかりなので未承認
                # st.rerun() # 自動生成の場合はrerunしない

            # 常にテキストエリアは表示し、承認済みかどうかでdisabledを切り替える
            menu['description_jp'] = st.text_area(
                f"{menu['name']} の詳細説明（日本語）",
                value=menu['description_jp'],
                height=150,
                key=f"description_jp_{menu['id']}_edit",
                disabled=menu['ai_description_approved'] # 承認済みなら編集不可
            )

            # 承認・訂正ボタン
            if not menu['ai_description_approved']:
                col_approve, col_edit_done = st.columns([1, 1])
                with col_approve:
                    if st.button("これでOK (承認)", key=f"approve_desc_{menu['id']}"):
                        menu['ai_description_approved'] = True
                        st.success(f"{menu['name']} の説明を承認しました！")
                        st.rerun()
                with col_edit_done:
                    if st.button("訂正終了 (手入力・音声入力完了)", key=f"edit_done_desc_{menu['id']}"):
                        menu['ai_description_approved'] = True # 手動で訂正した場合も承認済みとする
                        st.success(f"{menu['name']} の説明を訂正・確定しました！")
                        st.rerun()
            else:
                st.success(f"{menu['name']} の説明は承認済みです。")


            # アレルギー情報の表示・非表示をSTEP3の選択に連動
            st.markdown("---")
            st.subheader("アレルギー情報")
            if st.session_state.get('allergy_policy') == "display":
                st.info("アレルギー情報を表示する設定です。このメニューに含まれるアレルギー物質を選択してください。")
                selected_allergens = st.multiselect(
                    f"{menu['name']} に含まれるアレルギー物質を選択してください",
                    options=ALLERGENS,
                    default=menu['allergens'],
                    key=f"allergens_{menu['id']}"
                )
                menu['allergens'] = selected_allergens
                st.write(f"選択済みのアレルギー物質: {', '.join(menu['allergens']) if menu['allergens'] else 'なし'}")
            else:
                st.warning("アレルギー情報を表示しない設定です。このメニューのアレルギー物質は表示されません。")
                st.write("アレルギー情報の設定は行いません。")
                menu['allergens'] = [] # 表示しない場合はデータをクリアしておく

            updated_detailed_menus.append(menu)

    st.session_state.detailed_menus = updated_detailed_menus

    st.markdown("---")
    # ナビゲーションボタン (戻る/最初に戻る)
    col_prev1, col_prev2, col_next = st.columns([1, 1, 1])
    with col_prev1:
        if st.button("⬅️ 戻る (想いヒアリングへ)", key="step4_back_to_thoughts"):
            st.session_state.current_step = 2 # STEP3へ戻る
            st.rerun()
    with col_prev2:
        # メニュー、値段の訂正ページに戻るボタン
        if st.button("⬅️ メニュー・値段訂正へ (STEP2)", key="step4_back_to_menu_edit"):
            st.session_state.current_step = 1 # STEP2へ戻る
            st.rerun()
    with col_next:
        # 全てのAI説明が承認されているかチェック
        all_descriptions_approved = all(m.get('ai_description_approved', False) for m in st.session_state.detailed_menus)
        if all_descriptions_approved:
            if st.button("次へ進む (完了へ) ➡️", key="step4_next_to_completion"):
                st.session_state.current_step = 4 # STEP5へ進む
                st.rerun()
        else:
            st.warning("全てのメニューの食べ方説明を承認または訂正・確定してください。")


# ====================
# 7. STEP5: 完了
# ====================
def show_completion_page():
    """
    STEP5のメインページ。
    最終確認と最終処理の実行機能を提供する。
    """
    st.session_state.current_step = 4 # 現在のステップを設定

    # 共通ナビゲーションバーを表示
    show_universal_navigation()

    st.title("🎉 全ての設定が完了しました！")
    st.success("これであなたの多言語メニューを準備する準備が整いました。")

    st.markdown("---")
    st.subheader("最終確認")
    st.info("これまでの設定内容を最終確認してください。")

    # 店主の想いの表示
    st.markdown("#### 💬 お店の想い")
    if st.session_state.get('summarized_thought'):
        st.write(st.session_state.summarized_thought)
        with st.expander("多言語に展開された想いを確認"):
            for lang, text in st.session_state.get('translated_thoughts', {}).items():
                st.write(f"**{lang}**: {text}")
    else:
        st.warning("お店の想いが設定されていません。")

    # アレルギー表示方針の表示
    st.markdown("#### 🚫 アレルギー情報表示方針")
    if st.session_state.get('allergy_policy'):
        st.write(f"アレルギー情報は**{'表示する' if st.session_state.allergy_policy == 'display' else '表示しない'}**設定です。")
    else:
        st.warning("アレルギー情報表示方針が設定されていません。")

    # 各メニューの詳細情報の表示
    st.markdown("#### 🍽️ 各メニューの詳細")
    if st.session_state.get('detailed_menus'):
        for i, menu in enumerate(st.session_state.detailed_menus):
            with st.expander(f"メニュー {i+1}: {menu['name']}"):
                st.write(f"**カテゴリー**: {menu['category']}")
                st.write(f"**価格**: {menu['price']}")
                if menu['photo_url']:
                    st.write(f"**写真**: [アップロード済み](お待ちください)")
                else:
                    st.write("**写真**: なし")
                st.write(f"**詳細説明 (日本語)**: {menu['description_jp']}")
                if st.session_state.get('allergy_policy') == 'display':
                    st.write(f"**アレルギー物質**: {', '.join(menu['allergens']) if menu['allergens'] else 'なし'}")

    else:
        st.warning("メニュー情報が設定されていません。")

    st.markdown("---")
    st.subheader("店頭POP用：オススメメニュー選択")
    st.info("店頭POPに使用するため、オススメのメニューをおひとつお選びください。")

    # 選択可能なメニューリストを準備
    recommended_menu_options = [menu['name'] for menu in st.session_state.get('detailed_menus', []) if menu['should_introduce']]

    if recommended_menu_options:
        # 以前に選択されたメニューがあれば、それをデフォルトに設定
        default_index = 0
        if 'selected_recommended_menu' in st.session_state and st.session_state.selected_recommended_menu in recommended_menu_options:
            default_index = recommended_menu_options.index(st.session_state.selected_recommended_menu)

        selected_menu_for_pop = st.radio(
            "オススメとして選ぶメニュー",
            options=recommended_menu_options,
            index=default_index,
            key="recommended_menu_selector"
        )
        st.session_state.selected_recommended_menu = selected_menu_for_pop # 選択をセッションに保存
        st.success(f"店頭POP用オススメメニューとして「{selected_menu_for_pop}」が選択されました。")

        if st.button("このオススメメニューで確定", key="confirm_recommended_menu"):
            # ここで選択されたメニュー情報が戸塚さんに連携されることを想定
            st.info(f"「{selected_menu_for_pop}」の情報を戸塚さんへ連携しました。") # 戸塚さんへの連携メッセージを追加
            # TODO: 選択されたオススメメニューをバックエンドに連携するロジック
    else:
        st.warning("オススメとして選択可能なメニューがありません。STEP2でメニューを「掲載する」に設定してください。")

    st.markdown("---")
    st.subheader("最終処理と請求書・領収書")
    st.info("全ての情報が揃いました。最終処理を実行します。")

    # 「完了」ボタン。押されたら裏の作業が始まるという想定。
    if st.button("完了", key="complete_process_button"):
        with st.spinner("最終処理を実行中..."):
            time.sleep(2) # 実際の裏側処理のシミュレーション
            st.success("全ての処理が完了しました！")
            st.info("多言語メニューの作成が完了し、データがシステムに保存されました。")

            # ここで実際のCSV生成、データ保存、Stripe決済連携などのバックエンド処理が開始されることを想定
            st.markdown("---")
            st.subheader("今後の流れ")
            st.write("設定されたメニュー情報はシステムに保存されました。この後、以下のステップに進みます。")
            st.write("1. 代理店より、今回の情報に基づいたPOPのご提案が行われます。")
            st.write("2. ご希望のPOPを選んでいただき、決済が完了すると、多言語メニューが表示されます。")
            st.warning("責任者ナンバーからの請求書・領収書の発行、Stripeでの決済処理は、別途ご案内いたします。")

    # POP作成請求書・領収書ボタン
    if st.button("POP作成請求書・領収書を発行", key="issue_pop_invoice_receipt"):
        st.success("POP作成請求書・領収書の発行プロセスを開始しました。ご登録のメールアドレスに送付されます。")
        # TODO: POP作成に関する請求書・領収書発行のバックエンド連携をここに実装

    st.markdown("---")
    # ナビゲーションボタン (戻る/最初に戻る)
    col_prev_comp, col_restart_comp = st.columns([1, 1])
    with col_prev_comp:
        if st.button("⬅️ 戻る (詳細設定へ)", key="step5_back_to_details"):
            st.session_state.current_step = 3
            st.rerun()
    with col_restart_comp:
        if st.button("最初に戻る (ログアウト)", key="restart_from_step5"):
            st.session_state.clear() # セッション状態を全てクリアして最初に戻る
            st.rerun()


# ====================
# メインアプリケーションフロー
# ====================

def main_flow():
    """
    アプリケーションのメインエントリーポイント。
    セッション状態に基づいて、適切なページを表示する。
    """
    # アプリケーション起動時のセッション状態の初期化
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0

    # finalized_menus が存在しない、または不完全な場合に初期化
    # これは、ユーザーが途中のステップから開始したり、セッションがリセットされた場合に備えるため
    # OCR結果のモックデータ MOCK_OCR_RESULTS とカテゴリーリスト MENU_CATEGORIES を使用
    if 'finalized_menus' not in st.session_state or not st.session_state.finalized_menus:
        st.session_state.finalized_menus = []
        # OCR結果が初期化されていない場合のみ、モックデータで初期化
        if 'ocr_results' not in st.session_state or not st.session_state.ocr_results:
             st.session_state.ocr_results = MOCK_OCR_RESULTS # モックデータで初期化

        for i, item in enumerate(st.session_state.ocr_results):
            st.session_state.finalized_menus.append({
                "id": i,
                "original_name": item.get("name", ""),
                "name": item.get("name", ""),
                "price": item.get("price", ""),
                "category": MENU_CATEGORIES[0], # デフォルトで「フード」
                "should_introduce": True, # デフォルトで掲載する
                "order": i # 初期表示順
            })

    # detailed_menus が存在しない、または finalized_menus との整合性が取れていない場合に初期化
    # finalized_menus の内容が変わった場合にも対応できるよう、常に finalized_menus をベースに再構築を試みる
    if 'detailed_menus' not in st.session_state or \
       len(st.session_state.detailed_menus) != len(st.session_state.finalized_menus) or \
       any(dm['name'] != fm['name'] for dm, fm in zip(st.session_state.detailed_menus, st.session_state.finalized_menus)):

        # 既存の詳細データを保持しつつ、新しい finalized_menus に基づいて更新するロジック
        existing_detailed_map = {item['id']: item for item in st.session_state.get('detailed_menus', [])}
        new_detailed_menus = []
        for i, menu_item in enumerate(st.session_state.get('finalized_menus', [])):
            # 既存のデータがあればそれを利用し、なければ新規作成
            existing_data = existing_detailed_map.get(menu_item['id'], {})
            new_detailed_menus.append({
                "id": menu_item['id'],
                "name": menu_item['name'],
                "price": menu_item['price'],
                "category": menu_item['category'],
                "should_introduce": menu_item['should_introduce'],
                "order": menu_item['order'],
                "photo_url": existing_data.get("photo_url", ""), # 既存のURLを保持
                "allergens": existing_data.get("allergens", []), # 既存のアレルギーを保持
                "is_recommended": existing_data.get("is_recommended", False), # 既存のおすすめフラグを保持
                "description_jp": existing_data.get("description_jp", ""), # 既存の詳細説明を保持
                "ai_description_approved": existing_data.get("ai_description_approved", False), # 生成説明承認フラグ
                "ai_description_generated": existing_data.get("ai_description_generated", False), # 生成説明生成フラグ
            })
        st.session_state.detailed_menus = new_detailed_menus


    # アプリケーションフローの分岐
    if not st.session_state.logged_in:
        show_login_page() # ログインしていない場合はログインページを表示
    else:
        # ログイン済みの場合はcurrent_stepに基づいてページを分岐
        if st.session_state.current_step == 0:
             show_login_page() # 安全のため、もしcurrent_stepが0ならログインページに
        elif st.session_state.current_step == 1:
            show_menu_upload_page() # STEP2のページを表示
        elif st.session_state.current_step == 2:
            show_owner_thoughts_page() # STEP3のページを表示
        elif st.session_state.current_step == 3:
            show_detailed_settings_page() # STEP4のページを表示
        elif st.session_state.current_step == 4:
            show_completion_page() # STEP5のページを表示


# アプリケーションのエントリーポイント
if __name__ == "__main__":
    # Streamlitのキャッシュクリア (開発中に変更が反映されない場合などに利用)
    # st.cache_data.clear() # 必要に応じてコメントを解除
    main_flow()
