"""Phone Usage Analytics Dashboard - Nhóm B (STEM Tin học 9)."""
import pandas as pd
import streamlit as st
from logic import (
    REQUIRED_COLUMNS, prepare_dataframe, validate_dataframe,
    summarize_dataframe, calculate_sleep_hours, create_message, get_sample_dataframe,
)

# [1] CẤU HÌNH TRANG
st.set_page_config(
    page_title="Phone Usage Analytics - Lớp 9B",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# [2] CUSTOM CSS CHO GIAO DIỆN DARK DASHBOARD CAO CẤP
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Be Vietnam Pro', sans-serif;
        background-color: #0b0f19;
        color: #f8fafc;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }

    /* Top Bar Header */
    .top-header {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 12px;
        padding: 16px 24px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .header-title-box {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .app-icon {
        background: #2563eb;
        color: white;
        width: 44px;
        height: 44px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
    }

    /* Tabs tùy chỉnh */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #111827;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #1f2937;
        margin-bottom: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 18px;
        font-weight: 600;
        color: #9ca3af;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #3b82f6 !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        display: none;
    }

    /* Thẻ Dashboard Card */
    .dash-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        position: relative;
    }
    .dash-card-red {
        background: #181118;
        border: 1px solid #7f1d1d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }
    .card-label {
        color: #9ca3af;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    .card-value {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 700;
        line-height: 1.1;
    }
    .card-sub {
        font-size: 0.82rem;
        color: #9ca3af;
        margin-top: 8px;
    }
    .card-sub-green { color: #34d399; font-weight: 600; }
    .card-sub-yellow { color: #fbbf24; font-weight: 600; }
    .card-sub-red { color: #f87171; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# Khởi tạo session state lưu dữ liệu khảo sát
if "df_data" not in st.session_state:
    st.session_state["df_data"] = get_sample_dataframe()

df = st.session_state["df_data"]
summary = summarize_dataframe(df)

# [3] TOP HEADER
c_head1, c_head2 = st.columns([3, 1])
with c_head1:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 16px;">
        <div style="background: #2563eb; color: white; width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 22px;">📱</div>
        <div>
            <div style="font-size: 1.25rem; font-weight: 700; color: #ffffff; letter-spacing: 0.5px;">PHONE USAGE ANALYTICS</div>
            <div style="font-size: 0.85rem; color: #9ca3af;">Khảo sát Thời gian Sử dụng Điện thoại & Giấc ngủ - Lớp 9B (30 Học sinh)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c_head2:
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("↺ Khôi phục gốc", use_container_width=True):
            st.session_state["df_data"] = get_sample_dataframe()
            st.rerun()
    with col_b2:
        csv_bytes = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "⭳ Xuất Excel",
            data=csv_bytes,
            file_name="phuong_an_khao_sat_nhom_b.csv",
            mime="text/csv",
            use_container_width=True
        )

# [4] 5 TABS CHÍNH
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard Tổng Quan",
    "📁 Bảng Dữ Liệu Khảo Sát",
    "⚙️ Tiêu Chí & Điều Kiện",
    "🧮 Khu Vực Công Thức Excel",
    "📋 Báo Cáo & In Ân"
])

# --- TAB 1: DASHBOARD TỔNG QUAN ---
with tab1:
    # Hàng 1: 5 Thẻ KPI
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.markdown(f"""
        <div class="dash-card">
            <div class="card-label">Tổng học sinh</div>
            <div class="card-value">{summary['total']}</div>
            <div class="card-sub">👥 Lớp 9B khảo sát</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="dash-card">
            <div class="card-label">Thời gian dùng ĐT TB</div>
            <div class="card-value">{summary['avg_screen']} h</div>
            <div class="card-sub">⏱️ Giờ / ngày / học sinh</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="dash-card">
            <div class="card-label">Thời lượng ngủ TB</div>
            <div class="card-value">{summary['avg_sleep']} h</div>
            <div class="card-sub card-sub-green">Khuyến nghị: ≥ 8h</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        pct_before = round((summary['before_bed_yes'] / summary['total']) * 100) if summary['total'] > 0 else 0
        st.markdown(f"""
        <div class="dash-card">
            <div class="card-label">Màn hình trước ngủ</div>
            <div class="card-value">{summary['before_bed_yes']} HS</div>
            <div class="card-sub">{pct_before}% tổng số học sinh</div>
        </div>
        """, unsafe_allow_html=True)
    with k5:
        st.markdown(f"""
        <div class="dash-card">
            <div class="card-label">Cần lưu ý cảnh báo</div>
            <div class="card-value" style="color: #f87171;">{summary['warning_count']} HS</div>
            <div class="card-sub card-sub-red">Cần can thiệp/nhắc nhở</div>
        </div>
        """, unsafe_allow_html=True)

    # Hàng 2: 3 Thẻ Nhóm
    g1, g2, g3 = st.columns(3)
    with g1:
        st.markdown(f"""
        <div class="dash-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div class="card-label">Nhóm 1 (< 2H)</div>
                <span style="color: #3b82f6; font-size: 1.2rem;">🛡️</span>
            </div>
            <div class="card-value">{summary['n1_count']} HS</div>
            <div class="card-sub">Tổng: {summary['n1_sum']}h</div>
            <hr style="border-color: #1f2937; margin: 12px 0;">
            <div style="font-size: 0.8rem; color: #34d399;">Mức độ an toàn - Duy trì thói quen tốt</div>
        </div>
        """, unsafe_allow_html=True)
    with g2:
        st.markdown(f"""
        <div class="dash-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div class="card-label">Nhóm 2 (2H - 4H)</div>
                <span style="color: #f59e0b; font-size: 1.2rem;">⚖️</span>
            </div>
            <div class="card-value">{summary['n2_count']} HS</div>
            <div class="card-sub">Tổng: {summary['n2_sum']}h</div>
            <hr style="border-color: #1f2937; margin: 12px 0;">
            <div style="font-size: 0.8rem; color: #fbbf24;">Mức độ trung bình - Cần quản lý thời gian</div>
        </div>
        """, unsafe_allow_html=True)
    with g3:
        st.markdown(f"""
        <div class="dash-card-red">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div class="card-label" style="color: #fca5a5;">Nhóm 3 (> 4H)</div>
                <span style="color: #f87171; font-size: 1.2rem;">⚠️</span>
            </div>
            <div class="card-value" style="color: #fca5a5;">{summary['n3_count']} HS</div>
            <div class="card-sub" style="color: #fca5a5;">Tổng: {summary['n3_sum']}h</div>
            <hr style="border-color: #7f1d1d; margin: 12px 0;">
            <div style="font-size: 0.8rem; color: #fca5a5;">Nguy cơ cao - Cần nhắc nhở và điều chỉnh</div>
        </div>
        """, unsafe_allow_html=True)

    # Hàng 3: Biểu đồ
    c_chart1, c_chart2 = st.columns([1.2, 1])
    with c_chart1:
        with st.container(border=True):
            st.markdown("#### 📊 Phân Phối Học Sinh Theo Nhóm Sử Dụng Điện Thoại")
            chart_data = pd.DataFrame({
                "Nhóm": ["Nhóm 1 (< 2H)", "Nhóm 2 (2H - 4H)", "Nhóm 3 (> 4H)"],
                "Số học sinh": [summary['n1_count'], summary['n2_count'], summary['n3_count']],
            }).set_index("Nhóm")
            st.bar_chart(chart_data, color="#3b82f6")

    with c_chart2:
        with st.container(border=True):
            st.markdown("#### 🍩 Thói Quen Dùng Điện Thoại 1 Giờ Trước Khi Ngủ")
            yes_bed = summary['before_bed_yes']
            no_bed = summary['total'] - yes_bed
            pie_data = pd.DataFrame({
                "Trạng thái": ["Có dùng trước khi ngủ", "Không dùng trước khi ngủ"],
                "Số lượng": [yes_bed, no_bed]
            }).set_index("Trạng thái")
            st.bar_chart(pie_data, color="#f59e0b")

# --- TAB 2: BẢNG DỮ LIỆU KHẢO SÁT ---
with tab2:
    st.markdown("### 📁 Quản lý và Tải lên Dữ liệu Khảo Sát")
    uploaded_file = st.file_uploader("Tải lên file Excel (.xlsx) hoặc CSV", type=["xlsx", "xls", "csv"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith((".xlsx", ".xls")):
                raw = pd.read_excel(uploaded_file, sheet_name="Du_lieu_khao_sat", skiprows=2)
            else:
                raw = pd.read_csv(uploaded_file)
            st.session_state["df_data"] = prepare_dataframe(raw)
            df = st.session_state["df_data"]
            st.success("Tải file và chuẩn hóa dữ liệu thành công!")
        except Exception as e:
            st.error(f"Lỗi đọc file: {e}")

    issues = validate_dataframe(df)
    if issues:
        st.warning(f"⚠️ Phát hiện {len(issues)} vấn đề về dữ liệu cần lưu ý.")
        for issue in issues:
            st.write(f"- {issue}")
    else:
        st.success("✅ Dữ liệu hợp lệ, không có lỗi định dạng.")

    st.markdown("#### Bảng Dữ Liệu Chi Tiết (Đã ẩn danh)")
    st.dataframe(df, use_container_width=True, hide_index=True)

# --- TAB 3: TIÊU CHÍ & ĐIỀU KIỆN ---
with tab3:
    st.markdown("### ⚙️ Tiêu Chí Phân Loại & Quy Ước Dự Án")
    st.info(
        "Các tiêu chí dưới đây được Nhóm B xây dựng nhằm mục đích học tập môn Tin học 9 "
        "(thực hành hàm IF, COUNTIF, SUMIF) và truyền thông nâng cao nhận thức sức khỏe học đường."
    )
    c_t1, c_t2 = st.columns(2)
    with c_t1:
        with st.container(border=True):
            st.markdown("#### 📱 Phân nhóm thời gian sử dụng")
            st.markdown(
                "- **Nhóm 1 (< 2 giờ/ngày):** Mức độ an toàn, duy trì thói quen lành mạnh.\n"
                "- **Nhóm 2 (2 – 4 giờ/ngày):** Mức độ trung bình, cần quản lý thời gian giải trí hợp lý.\n"
                "- **Nhóm 3 (> 4 giờ/ngày):** Nguy cơ cao, cần can thiệp và điều chỉnh thói quen."
            )
    with c_t2:
        with st.container(border=True):
            st.markdown("#### 🌙 Quy chuẩn giấc ngủ & thói quen")
            st.markdown(
                "- **Thời lượng ngủ khuyến nghị:** 8 – 10 giờ mỗi đêm đối với học sinh trung học cơ sở.\n"
                "- **Sử dụng màn hình trước khi ngủ:** Tránh dùng thiết bị trước 60 phút để không ảnh hưởng đến hormone giấc ngủ (Melatonin).\n"
                "- **Nguyên tắc bảo mật:** Dữ liệu hoàn toàn ẩn danh, không xếp loại công khai gây áp lực tâm lý."
            )

# --- TAB 4: KHU VỰC CÔNG THỨC EXCEL ---
with tab4:
    st.markdown("### 🧮 Khu Vực Công Thức Excel Tương Đương")
    st.write("Bảng dưới đây ánh xạ các hàm Python đang dùng trong ứng dụng sang các công thức Excel tương đương cho báo cáo STEM:")
    
    formula_df = pd.DataFrame([
        ["Tổng số học sinh tham gia", "=COUNTA(A4:A33)", "Đếm tổng số bản ghi hợp lệ"],
        ["Số HS thuộc Nhóm > 4h", '=COUNTIF(H4:H33, "Nhóm 3 (> 4H)")', "Đếm học sinh có thời gian màn hình cao"],
        ["Tổng giờ màn hình Nhóm > 4h", '=SUMIF(H4:H33, "Nhóm 3 (> 4H)", B4:B33)', "Tính tổng thời gian sử dụng của nhóm nguy cơ"],
        ["Số HS ngủ dưới 8 giờ", '=COUNTIF(I4:I33, "Dưới 8 giờ")', "Thống kê học sinh thiếu ngủ"],
        ["Thời lượng ngủ trung bình", "=AVERAGE(F4:F33)", "Tính số giờ ngủ trung bình toàn lớp"],
        ["Cảnh báo thói quen", '=IF(OR(B4>4, C4="Có", F4<8), "Cần xem lại", "Phù hợp")', "Hàm logic đánh giá tự động"],
    ], columns=["Chỉ tiêu thống kê", "Công thức Excel", "Ý nghĩa nghiệp vụ"])
    st.dataframe(formula_df, use_container_width=True, hide_index=True)

# --- TAB 5: BÁO CÁO & IN ÂN ---
with tab5:
    st.markdown("### 📋 Báo Cáo Tổng Hợp Kết Quả Khảo Sát Lớp 9B")
    with st.container(border=True):
        st.markdown(f"""
        ### 🏫 TRƯỜNG THCS ... | DỰ ÁN STEM TIN HỌC 9
        **Chủ đề:** Màn hình thông minh – Giấc ngủ an lành (Nhóm B)  
        **Đối tượng khảo sát:** 30 Học sinh lớp 9B  
        
        ---
        
        #### 📌 Tóm tắt kết quả chính:
        1. **Thời gian sử dụng thiết bị trung bình:** `{summary['avg_screen']} giờ/ngày/học sinh`. Trong đó có `{summary['n3_count']} học sinh` nằm trong nhóm nguy cơ cao (`> 4 giờ/ngày`).
        2. **Thói quen trước khi ngủ:** Có `{summary['before_bed_yes']} học sinh ({pct_before}%)` sử dụng màn hình điện thoại trong vòng 1 giờ trước khi lên giường.
        3. **Chất lượng giấc ngủ:** Thời lượng ngủ trung bình của lớp đạt `{summary['avg_sleep']} giờ/đêm`. Tuy nhiên, vẫn còn trường hợp ngủ chưa đủ mốc khuyến nghị (`≥ 8 giờ`).
        
        #### 💡 Đề xuất & Khuyến nghị:
        - Tuyên truyền giới hạn thời gian giải trí trên thiết bị điện tử dưới 3 giờ mỗi ngày.
        - Xây dựng thói quen tắt thiết bị di động trước khi ngủ ít nhất 60 phút để cải thiện chất lượng giấc ngủ và sự tập trung học tập trên lớp.
        """)
    if st.button("🖨️ In / Xuất báo cáo PDF"):
        st.info("Tính năng in báo cáo đã sẵn sàng. Bạn có thể nhấn Ctrl+P trên trình duyệt để lưu trang này thành PDF.")

# [5] CHÂN TRANG
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #6b7280; font-size: 0.85rem;'>"
    "Sản phẩm học tập STEM – Tin học 9 | Nhóm B | Dữ liệu vì sức khỏe học đường"
    "</div>",
    unsafe_allow_html=True,
)