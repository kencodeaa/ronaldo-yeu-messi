"""Các hàm xử lý dữ liệu độc lập với giao diện Streamlit (Phiên bản Dashboard Nhóm B)."""
from __future__ import annotations
import math
import pandas as pd
import numpy as np

REQUIRED_COLUMNS = [
    "Mã HS",
    "Thời gian sử dụng màn hình (giờ/ngày)",
    "Có sử dụng màn hình trong 1 giờ trước khi ngủ? (Có/Không)",
    "Giờ đi ngủ",
    "Giờ thức dậy",
    "Thời lượng ngủ (giờ)",
    "Tự đánh giá ngủ đủ? (Có/Không)",
]

SCREEN_LIMIT_HOURS = 4.0
SLEEP_MIN_HOURS = 8.0
SLEEP_MAX_HOURS = 10.0

def _to_hour(value):
    if pd.isna(value):
        return None
    if hasattr(value, "hour") and hasattr(value, "minute"):
        return value.hour * 60 + value.minute
    text = str(value).strip()
    if not text:
        return None
    try:
        parts = text.split(":")
        hour, minute = int(parts[0]), int(parts[1])
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            return None
        return hour * 60 + minute
    except (ValueError, IndexError):
        return None

def calculate_sleep_hours(bedtime, wake_time):
    start, end = _to_hour(bedtime), _to_hour(wake_time)
    if start is None or end is None or start == end:
        return None
    minutes = (end - start) % (24 * 60)
    if minutes <= 0:
        return None
    return round(minutes / 60, 2)

def classify_screen_time(hours):
    """Phân loại thành 3 nhóm theo giao diện mẫu."""
    if pd.isna(hours):
        return "Chưa đủ dữ liệu"
    h = float(hours)
    if h < 2.0:
        return "Nhóm 1 (< 2H)"
    elif h <= 4.0:
        return "Nhóm 2 (2H - 4H)"
    else:
        return "Nhóm 3 (> 4H)"

def classify_sleep(hours):
    if pd.isna(hours):
        return "Chưa đủ dữ liệu"
    value = float(hours)
    if value < SLEEP_MIN_HOURS:
        return "Dưới 8 giờ"
    if value <= SLEEP_MAX_HOURS:
        return "8–10 giờ"
    return "Trên 10 giờ"

def create_message(screen_hours, before_sleep, sleep_hours):
    if pd.isna(screen_hours) or before_sleep not in ("Có", "Không") or pd.isna(sleep_hours):
        return "Chưa đủ dữ liệu để tạo thông điệp"
    if float(screen_hours) > 4.0 or before_sleep == "Có" or float(sleep_hours) < SLEEP_MIN_HOURS:
        return "Cần xem lại thói quen màn hình và giấc ngủ"
    return "Thói quen tương đối phù hợp theo quy ước dự án"

def get_sample_dataframe():
    """Tạo dữ liệu mẫu 30 học sinh lớp 9B khớp với các chỉ số trên dashboard mẫu."""
    screen_vals = (
        [1.2, 1.5, 1.8, 1.0, 1.4, 1.6, 1.1, 1.3, 1.7, 1.9, 1.5] + # 11 HS (<2h)
        [2.5, 2.8, 3.0, 2.2, 3.5, 2.4, 3.1, 2.7, 3.3, 2.9] +      # 10 HS (2h-4h)
        [4.5, 5.0, 4.2, 5.5, 4.8, 6.0, 4.3, 5.2, 4.7]              # 9 HS (>4h)
    )
    bedtimes = ["22:00", "22:30", "23:00", "23:30", "21:30"]
    wake_times = ["06:00", "06:15", "06:30", "07:00"]

    data = []
    for i in range(1, 31):
        hs_id = f"HS{i:02d}"
        sh = screen_vals[i-1]
        bs = "Có" if (sh > 3.0 or i % 2 == 0) else "Không"
        bed = bedtimes[i % len(bedtimes)]
        wake = wake_times[i % len(wake_times)]
        sleep_h = calculate_sleep_hours(bed, wake)
        if sleep_h is None:
            sleep_h = 7.0
        eval_sleep = "Có" if sleep_h >= 8 else "Không"
        data.append({
            "Mã HS": hs_id,
            "Thời gian sử dụng màn hình (giờ/ngày)": sh,
            "Có sử dụng màn hình trong 1 giờ trước khi ngủ? (Có/Không)": bs,
            "Giờ đi ngủ": bed,
            "Giờ thức dậy": wake,
            "Thời lượng ngủ (giờ)": sleep_h,
            "Tự đánh giá ngủ đủ? (Có/Không)": eval_sleep
        })
    df = pd.DataFrame(data)
    return prepare_dataframe(df)

def prepare_dataframe(raw_df):
    df = raw_df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError("Thiếu cột bắt buộc: " + ", ".join(missing))

    df = df[REQUIRED_COLUMNS].copy()
    df["Mã HS"] = df["Mã HS"].astype("string").str.strip()
    df["Thời gian sử dụng màn hình (giờ/ngày)"] = pd.to_numeric(
        df["Thời gian sử dụng màn hình (giờ/ngày)"], errors="coerce"
    )
    yes_no_cols = [
        "Có sử dụng màn hình trong 1 giờ trước khi ngủ? (Có/Không)",
        "Tự đánh giá ngủ đủ? (Có/Không)",
    ]
    for col in yes_no_cols:
        df[col] = df[col].astype("string").str.strip().str.capitalize()

    sleep_values = [
        calculate_sleep_hours(bed, wake)
        for bed, wake in zip(df["Giờ đi ngủ"], df["Giờ thức dậy"])
    ]
    df["Thời lượng ngủ (giờ)"] = sleep_values
    screen_col = "Thời gian sử dụng màn hình (giờ/ngày)"
    before_col = yes_no_cols[0]
    df["Nhóm thời gian màn hình"] = df[screen_col].apply(classify_screen_time)
    df["Nhóm thời lượng ngủ"] = df["Thời lượng ngủ (giờ)"].apply(classify_sleep)
    df["Thông điệp gợi ý"] = [
        create_message(s, b, h)
        for s, b, h in zip(df[screen_col], df[before_col], df["Thời lượng ngủ (giờ)"])
    ]
    return df

def validate_dataframe(df):
    issues = []
    id_col = "Mã HS"
    if df[id_col].isna().any() or (df[id_col].astype("string").str.len() == 0).any():
        issues.append("Có dòng chưa có mã học sinh.")
    duplicates = df.loc[df[id_col].notna(), id_col].duplicated()
    if duplicates.any():
        issues.append("Có mã học sinh bị trùng.")
    screen_col = "Thời gian sử dụng màn hình (giờ/ngày)"
    invalid_screen = df[screen_col].notna() & ~df[screen_col].between(0, 24)
    if invalid_screen.any():
        issues.append(f"Có {int(invalid_screen.sum())} giá trị thời gian màn hình ngoài khoảng 0–24 giờ.")
    return issues

def summarize_dataframe(df):
    screen_col = "Thời gian sử dụng màn hình (giờ/ngày)"
    sleep_col = "Thời lượng ngủ (giờ)"
    screen_group = "Nhóm thời gian màn hình"
    
    total = int(df["Mã HS"].notna().sum())
    avg_screen = float(df[screen_col].mean()) if total > 0 else 0.0
    avg_sleep = float(df[sleep_col].mean()) if total > 0 else 0.0
    
    n1_df = df[df[screen_group] == "Nhóm 1 (< 2H)"]
    n2_df = df[df[screen_group] == "Nhóm 2 (2H - 4H)"]
    n3_df = df[df[screen_group] == "Nhóm 3 (> 4H)"]
    
    before_bed_yes = int((df["Có sử dụng màn hình trong 1 giờ trước khi ngủ? (Có/Không)"] == "Có").sum())
    warning_mask = (df[screen_group] == "Nhóm 3 (> 4H)") | (df["Có sử dụng màn hình trong 1 giờ trước khi ngủ? (Có/Không)"] == "Có") | (df["Thời lượng ngủ (giờ)"] < 8.0)
    warning_count = int(warning_mask.sum())

    return {
        "total": total,
        "avg_screen": round(avg_screen, 1),
        "avg_sleep": round(avg_sleep, 1),
        "before_bed_yes": before_bed_yes,
        "warning_count": warning_count,
        
        "n1_count": len(n1_df),
        "n1_sum": round(float(n1_df[screen_col].sum()), 1),
        
        "n2_count": len(n2_df),
        "n2_sum": round(float(n2_df[screen_col].sum()), 1),
        
        "n3_count": len(n3_df),
        "n3_sum": round(float(n3_df[screen_col].sum()), 1),
    }
