# -*- coding: utf-8 -*-
"""
Dashboard tuong tac phan tich du lieu MovieLens.
Cach chay:  py -m streamlit run app.py
"""
import os, sys
import streamlit as st
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
import phan_tich as pt
from tao_bao_cao import tao_bao_cao

st.set_page_config(page_title="Phân tích dữ liệu MovieLens", page_icon="🎬", layout="wide")
THU_MUC = os.path.join("data", "ml-latest-small")


@st.cache_data
def nap_du_lieu():
    ratings, movies = pt.doc_du_lieu(THU_MUC)
    return pt.lam_sach(ratings, movies)


st.title("🎬 Phân tích dữ liệu đánh giá phim MovieLens")
st.caption("Mini-project – Học phần Công nghệ số nâng cao (CT999) – Đại học Cần Thơ")

if not os.path.exists(os.path.join(THU_MUC, "ratings.csv")):
    st.error("Chưa có dữ liệu. Hãy chạy lệnh:  py src/tai_du_lieu.py")
    st.stop()

df, nhat_ky = nap_du_lieu()

# ---------- Thanh ben: chon bien loc ----------
st.sidebar.header("Bộ lọc dữ liệu")
tat_ca_tl = sorted({t for ds in df["the_loai"] for t in ds if t})
chon_tl = st.sidebar.multiselect("Thể loại phim", tat_ca_tl)
nam_min, nam_max = int(df["nam_phat_hanh"].min()), int(df["nam_phat_hanh"].max())
chon_nam = st.sidebar.slider("Năm phát hành", nam_min, nam_max, (nam_min, nam_max))
chon_bd = st.sidebar.selectbox("Biểu đồ muốn xem", list(pt.BIEU_DO.keys()))

loc = pt.loc_du_lieu(df, chon_tl, chon_nam)
if loc.empty:
    st.warning("Không có dữ liệu phù hợp với bộ lọc.")
    st.stop()

# ---------- Chi so tong quan ----------
tk = pt.thong_ke(loc)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Số lượt đánh giá", f"{tk['so_danh_gia']:,}".replace(",", "."))
c2.metric("Số người dùng", tk["so_nguoi_dung"])
c3.metric("Số phim", tk["so_phim"])
c4.metric("Điểm trung bình", f"{tk['diem_tb']:.2f}")

# ---------- Bieu do theo lua chon ----------
st.subheader(chon_bd)
st.pyplot(pt.BIEU_DO[chon_bd](loc))

col_a, col_b = st.columns(2)
with col_a:
    st.subheader("Top 10 phim điểm cao (≥ 50 lượt)")
    st.dataframe(pt.top_phim(loc).rename(columns={"title": "Tên phim", "so_luot": "Số lượt",
                                                  "diem_tb": "Điểm TB"}).drop(columns="movieId").round(2),
                 hide_index=True)
with col_b:
    st.subheader("Thống kê theo thể loại")
    st.dataframe(pt.thong_ke_the_loai(loc).rename(columns={"so_luot": "Số lượt",
                                                           "diem_tb": "Điểm TB"}).rename_axis("Thể loại").round(2))

# ---------- Mo hinh hoi quy ----------
st.subheader("Mô hình hồi quy dự đoán điểm đánh giá")
if st.button("Chạy mô hình"):
    kq = pt.mo_hinh_hoi_quy(loc)
    m1, m2, m3 = st.columns(3)
    m1.metric("RMSE mô hình cơ sở", f"{kq['rmse_co_so']:.4f}")
    m2.metric("RMSE hồi quy tuyến tính", f"{kq['rmse_mo_hinh']:.4f}",
              f"-{kq['cai_thien']:.1f}%", delta_color="inverse")
    m3.metric("R²", f"{kq['r2']:.3f}")
    st.pyplot(pt.bd_du_doan(kq))

# ---------- Tai bao cao PDF ----------
st.subheader("Tải báo cáo")
mo_ta = (f"thể loại {', '.join(chon_tl) if chon_tl else 'tất cả'}, "
         f"năm phát hành {chon_nam[0]}–{chon_nam[1]}")
if st.button("Tạo báo cáo PDF theo bộ lọc hiện tại"):
    with st.spinner("Đang tạo báo cáo..."):
        st.session_state["pdf"] = tao_bao_cao(loc, nhat_ky, mo_ta)
if "pdf" in st.session_state:
    st.download_button("⬇ Tải báo cáo PDF", st.session_state["pdf"],
                       file_name="bao_cao_movielens.pdf", mime="application/pdf")
