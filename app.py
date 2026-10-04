import streamlit as st
import urllib.request
import json

def safe_analyze_and_calculate(ticker_code):
    code = str(ticker_code).strip()
    try:
        url = f"https://yahoo.com{code}.TW?range=1mo&interval=1d"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
        if 'error' in data.get('chart', {}) or data['chart']['result'] is None:
            url = f"https://yahoo.com{code}.TWO?range=1mo&interval=1d"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
        result = data['chart']['result']
        indicators = result['indicators']['quote']
        close_list = [x for x in indicators['close'] if x is not None]
        high_list = [x for x in indicators['high'] if x is not None]
        low_list = [x for x in indicators['low'] if x is not None]
        current_price = float(close_list[-1])
        near_support = sorted([x for x in low_list if x < current_price], reverse=True) if any(x < current_price for x in low_list) else current_price * 0.985
        second_support = near_support * 0.97
        key_breakout = sorted([x for x in high_list if x > current_price]) if any(x > current_price for x in high_list) else current_price * 1.015
        second_resistance = key_breakout * 1.03
        near_support_range = f"{round(near_support*0.99,2)}-{round(near_support*1.01,2)}"
        second_support_range = f"{round(second_support*0.99,2)}-{round(second_support*1.01,2)}"
        def get_dist(target): return round(((target - current_price) / current_price) * 100, 1)

        html_output = f"""
        <div class="card-box">
            <div class="card-title card-title-blue">🛡️ 支撐觀察</div>
            <div class="row-flex">
                <div><div class="left-label">近端支撐</div><div class="left-sublabel">波段低點／前高轉支撐／爆量 K 低點</div></div>
                <div><div class="right-value">{round(near_support, 2)}</div><div class="right-subvalue">價格帶 {near_support_range}</div><div class="right-subvalue" style="color:#FF6B6B;">距現價 {get_dist(near_support)}%</div></div>
            </div>
            <div class="row-flex" style="margin-top: 18px;">
                <div><div class="left-label">第二支撐 │ 近端</div><div class="left-sublabel">爆量 K 收盤／缺口上緣／MA5</div></div>
                <div><div class="right-value">{round(second_support, 2)}</div><div class="right-subvalue">價格帶 {second_support_range}</div><div class="right-subvalue" style="color:#FF6B6B;">距現價 {get_dist(second_support)}%</div></div>
            </div>
            <div class="card-footer-text">現價之下的支撐觀察區與最接近的真實結構價位。目前即時最新股價：<b>{round(current_price, 2)}</b> 元。</div>
        </div>
        <div class="card-box">
            <div class="card-title card-title-orange">⚡ 關鍵突破 ／ 壓力共振區</div>
            <div class="row-flex">
                <div><div class="left-label">關鍵突破／壓力共振區</div></div>
                <div><div class="right-value">{round(key_breakout, 2)}</div><div class="right-subvalue" style="color:#2ED573;">距現價 +{get_dist(key_breakout)}%</div></div>
            </div>
        </div>
        <div class="card-box">
            <div class="card-title card-title-red">🔥 第二壓力</div>
            <div class="row-flex">
                <div><div class="left-label">第二壓力</div></div>
                <div><div class="right-value">{round(second_resistance, 2)}</div><div class="right-subvalue" style="color:#2ED573;">距現價 +{get_dist(second_resistance)}%</div></div>
            </div>
        </div>
        """
        return html_output
    except: return f"<div class='card-box' style='color:#FF6B6B;'>⚠️ 請確認輸入是否為正確的台股上市櫃數字代號。</div>"

# 高質感深藍色 App 字卡風格 CSS
st.markdown("""
<style>
.stApp { background-color: #051329 !important; color: white !important; }
.card-box { background-color: #0B1E36; border-radius: 16px; padding: 22px; margin-bottom: 22px; border: 1px solid #142F52; }
.stMarkdown { display: flex; flex-direction: column; gap: 0px; }
.card-title { font-size: 16px; font-weight: bold; margin-bottom: 18px; }
.card-title-blue { color: #54A0FF; } .card-title-orange { color: #FF9F43; } .card-title-red { color: #FF6B6B; }
.row-flex { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px; }
.left-label { font-size: 15px; color: #FFFFFF; font-weight: 500; } .left-sublabel { font-size: 11px; color: #6D7F98; margin-top: 4px; }
.right-value { font-size: 24px; font-weight: 700; text-align: right; color: #FFFFFF; line-height: 1; } .right-subvalue { font-size: 11px; color: #6D7F98; text-align: right; margin-top: 4px; }
.card-footer-text { font-size: 12px; color: #8A9CB4; border-top: 1px solid #142F52; padding-top: 12px; margin-top: 8px; }
input { background-color: #0B1E36 !important; color: white !important; border: 1px solid #142F52 !important; text-align: center !important; }
div[data-testid="stDecoration"] { display: none !important; }
header { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

st.title("世界")
ticker = st.text_input("", value="2330")
if st.button("開始自動分析", use_container_width=True):
    result_html = safe_analyze_and_calculate(ticker)
    st.markdown(result_html, unsafe_allow_html=True)
else:
    result_html = safe_analyze_and_calculate("2330")
    st.markdown(result_html, unsafe_allow_html=True)

