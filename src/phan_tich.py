# -*- coding: utf-8 -*-
"""Module phan tich du lieu MovieLens: doc, lam sach, thong ke, mo hinh hoi quy, ve bieu do."""
import os, re
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "DejaVu Sans"


def doc_du_lieu(thu_muc):
    """Doc 2 tep ratings.csv va movies.csv."""
    ratings = pd.read_csv(os.path.join(thu_muc, "ratings.csv"))
    movies = pd.read_csv(os.path.join(thu_muc, "movies.csv"))
    return ratings, movies


def lam_sach(ratings, movies):
    """Lam sach du lieu, tra ve (bang da gop, nhat ky cac buoc lam sach)."""
    nhat_ky = {"so_dong_ban_dau": len(ratings)}
    r = ratings.dropna()
    nhat_ky["bo_dong_thieu"] = len(ratings) - len(r)
    truoc = len(r)
    r = r.drop_duplicates(subset=["userId", "movieId"], keep="last")
    nhat_ky["bo_dong_trung"] = truoc - len(r)
    truoc = len(r)
    r = r[r["rating"].between(0.5, 5.0)]
    nhat_ky["bo_diem_khong_hop_le"] = truoc - len(r)
    r = r.assign(ngay_danh_gia=pd.to_datetime(r["timestamp"], unit="s"))
    r = r.assign(nam_danh_gia=r["ngay_danh_gia"].dt.year)

    m = movies.copy()
    m["nam_phat_hanh"] = m["title"].str.extract(r"\((\d{4})\)\s*$").astype(float)
    m["the_loai"] = m["genres"].replace("(no genres listed)", "").str.split("|")
    df = r.merge(m[["movieId", "title", "genres", "the_loai", "nam_phat_hanh"]],
                 on="movieId", how="inner")
    nhat_ky["so_dong_sau_lam_sach"] = len(df)
    return df, nhat_ky


def loc_du_lieu(df, the_loai=None, nam=None):
    """Loc theo the loai va khoang nam phat hanh (dung cho dashboard)."""
    kq = df
    if the_loai:
        kq = kq[kq["the_loai"].apply(lambda ds: any(t in ds for t in the_loai))]
    if nam:
        kq = kq[kq["nam_phat_hanh"].between(nam[0], nam[1])]
    return kq


def thong_ke(df):
    """Cac chi so thong ke mo ta."""
    so_nd, so_phim = df["userId"].nunique(), df["movieId"].nunique()
    return {
        "so_danh_gia": len(df), "so_nguoi_dung": so_nd, "so_phim": so_phim,
        "diem_tb": df["rating"].mean(), "do_lech_chuan": df["rating"].std(),
        "diem_trung_vi": df["rating"].median(), "diem_pho_bien": df["rating"].mode()[0],
        "do_thua": 1 - len(df) / (so_nd * so_phim),
        "tu_nam": int(df["nam_danh_gia"].min()), "den_nam": int(df["nam_danh_gia"].max()),
    }


def thong_ke_the_loai(df, top=10):
    """So luot va diem trung binh theo the loai."""
    tl = df[["rating", "the_loai"]].explode("the_loai")
    tl = tl[tl["the_loai"].astype(bool)]
    return (tl.groupby("the_loai")["rating"].agg(so_luot="count", diem_tb="mean")
            .sort_values("so_luot", ascending=False).head(top))


def top_phim(df, so_luot_toi_thieu=50, top=10):
    """Cac phim co diem trung binh cao nhat."""
    p = df.groupby(["movieId", "title"])["rating"].agg(so_luot="count", diem_tb="mean")
    p = p[p["so_luot"] >= so_luot_toi_thieu].sort_values("diem_tb", ascending=False)
    return p.head(top).reset_index()


def mo_hinh_hoi_quy(df, ti_le_test=0.2, seed=42):
    """
    Hoi quy tuyen tinh du doan diem danh gia:
        diem = b0 + b1 * (diem TB cua nguoi dung) + b2 * (diem TB cua phim)
    Cac gia tri TB chi tinh tren tap huan luyen (tranh ro ri du lieu).
    So sanh voi mo hinh co so: du doan bang diem TB toan bo.
    """
    rng = np.random.default_rng(seed)
    mask = rng.random(len(df)) < ti_le_test
    train, test = df[~mask], df[mask]
    mu = train["rating"].mean()
    tb_nd = train.groupby("userId")["rating"].mean()
    tb_phim = train.groupby("movieId")["rating"].mean()

    def dac_trung(d):
        x1 = d["userId"].map(tb_nd).fillna(mu).to_numpy()
        x2 = d["movieId"].map(tb_phim).fillna(mu).to_numpy()
        return np.column_stack([np.ones(len(d)), x1, x2])

    X_tr, y_tr = dac_trung(train), train["rating"].to_numpy()
    X_te, y_te = dac_trung(test), test["rating"].to_numpy()
    he_so, *_ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    du_doan = np.clip(X_te @ he_so, 0.5, 5.0)

    rmse = lambda a, b: float(np.sqrt(np.mean((a - b) ** 2)))
    rmse_mh = rmse(y_te, du_doan)
    rmse_cs = rmse(y_te, np.full(len(y_te), mu))
    r2 = 1 - np.sum((y_te - du_doan) ** 2) / np.sum((y_te - y_te.mean()) ** 2)
    return {"so_mau_train": len(train), "so_mau_test": len(test),
            "he_so": he_so.tolist(), "rmse_mo_hinh": rmse_mh, "rmse_co_so": rmse_cs,
            "cai_thien": (rmse_cs - rmse_mh) / rmse_cs * 100, "r2": float(r2),
            "y_test": y_te, "du_doan": du_doan}


# ---------------- Bieu do (tra ve doi tuong Figure) ----------------
def bd_phan_bo_diem(df):
    fig, ax = plt.subplots(figsize=(7, 3.6))
    df["rating"].value_counts().sort_index().plot(kind="bar", color="#4a86c8", ax=ax, rot=0)
    ax.set_xlabel("Điểm đánh giá"); ax.set_ylabel("Số lượt đánh giá")
    ax.set_title("Phân bố điểm đánh giá"); fig.tight_layout(); return fig


def bd_theo_nam(df):
    fig, ax = plt.subplots(figsize=(7, 3.6))
    df.groupby("nam_danh_gia").size().plot(ax=ax, marker="o", color="#6aa84f")
    ax.set_xlabel("Năm đánh giá"); ax.set_ylabel("Số lượt đánh giá")
    ax.set_title("Số lượt đánh giá theo năm"); fig.tight_layout(); return fig


def bd_the_loai(df):
    tl = thong_ke_the_loai(df)
    fig, ax = plt.subplots(figsize=(7, 3.6))
    tl["so_luot"].sort_values().plot(kind="barh", color="#e69138", ax=ax)
    ax.set_xlabel("Số lượt đánh giá"); ax.set_ylabel("")
    ax.set_title("10 thể loại được đánh giá nhiều nhất"); fig.tight_layout(); return fig


def bd_so_luot_vs_diem(df):
    p = df.groupby("movieId")["rating"].agg(["count", "mean"])
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.scatter(p["count"], p["mean"], s=6, alpha=0.35, color="#674ea7")
    ax.set_xscale("log"); ax.set_xlabel("Số lượt đánh giá của phim (thang log)")
    ax.set_ylabel("Điểm trung bình"); ax.set_title("Mức độ phổ biến và điểm trung bình của phim")
    fig.tight_layout(); return fig


def bd_du_doan(kq):
    fig, ax = plt.subplots(figsize=(7, 3.6))
    y, d = kq["y_test"], kq["du_doan"]
    muc = sorted(np.unique(y))
    ax.boxplot([d[y == m] for m in muc], tick_labels=[f"{m:g}" for m in muc])
    ax.set_xlabel("Điểm thực tế"); ax.set_ylabel("Điểm dự đoán")
    ax.set_title("Điểm dự đoán của mô hình hồi quy theo điểm thực tế")
    fig.tight_layout(); return fig


BIEU_DO = {
    "Phân bố điểm đánh giá": bd_phan_bo_diem,
    "Số lượt đánh giá theo năm": bd_theo_nam,
    "Số lượt đánh giá theo thể loại": bd_the_loai,
    "Số lượt và điểm trung bình của phim": bd_so_luot_vs_diem,
}
