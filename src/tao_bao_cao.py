# -*- coding: utf-8 -*-
"""
Sinh bao cao khoa hoc PDF tu dong tu du lieu MovieLens.
Cach chay (tu thu muc goc cua du an):
    py src/tao_bao_cao.py
"""
import io, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import phan_tich as pt
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

THANH_VIEN = "Võ Duy Nhứt, Huỳnh Nhật Trường, Võ Thị Cẩm Ngân, Lê Trung Tín"


def _font():
    for thuong, dam in [("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
                        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                         "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")]:
        if os.path.exists(thuong) and os.path.exists(dam):
            pdfmetrics.registerFont(TTFont("VN", thuong))
            pdfmetrics.registerFont(TTFont("VN-Bold", dam))
            return
    raise RuntimeError("Khong tim thay font Arial/DejaVu de hien thi tieng Viet.")


def _n(x):
    return f"{x:,}".replace(",", ".")


def tao_bao_cao(df, nhat_ky, mo_ta_loc="Toàn bộ dữ liệu"):
    """Tao bao cao PDF, tra ve noi dung dang bytes (dung cho ca dashboard)."""
    _font()
    ss = getSampleStyleSheet()
    H1 = ParagraphStyle("H1", parent=ss["Title"], fontName="VN-Bold", fontSize=16, leading=21)
    H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontName="VN-Bold", fontSize=12.5,
                        spaceBefore=10, spaceAfter=4, keepWithNext=1)
    P = ParagraphStyle("P", parent=ss["BodyText"], fontName="VN", fontSize=10.5,
                       leading=15, alignment=4)
    C = ParagraphStyle("C", parent=P, alignment=1, fontSize=9.5, textColor=colors.grey)

    def bang(du_lieu, rong):
        t = Table(du_lieu, colWidths=rong, repeatRows=1)
        t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "VN", 9.5),
                               ("FONT", (0, 0), (-1, 0), "VN-Bold", 9.5),
                               ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbe5f1")),
                               ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                               ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
        return t

    tmp = tempfile.mkdtemp()

    def hinh(fig, ten):
        duong_dan = os.path.join(tmp, ten)
        fig.savefig(duong_dan, dpi=150)
        pt.plt.close(fig)
        return Image(duong_dan, width=15 * cm, height=7.7 * cm)

    tk = pt.thong_ke(df)
    tl = pt.thong_ke_the_loai(df)
    tp = pt.top_phim(df)
    mh = pt.mo_hinh_hoi_quy(df)

    s = [Paragraph("PHÂN TÍCH DỮ LIỆU ĐÁNH GIÁ PHIM MOVIELENS VÀ MÔ HÌNH DỰ ĐOÁN ĐIỂM", H1),
         Paragraph(f"Nhóm thực hiện: {THANH_VIEN}<br/>Học phần Công nghệ số nâng cao (CT999) – "
                   "Đại học Cần Thơ", C), Spacer(1, 0.3 * cm)]

    s += [Paragraph("1. Giới thiệu đề tài", H2),
          Paragraph("Hệ thống gợi ý cần dự đoán mức độ yêu thích của người dùng đối với sản phẩm "
                    "chưa xem. Đề tài phân tích dữ liệu đánh giá phim MovieLens để tìm hiểu đặc điểm "
                    "của dữ liệu đánh giá, đồng thời xây dựng mô hình hồi quy tuyến tính đơn giản "
                    "dự đoán điểm đánh giá. Toàn bộ báo cáo được sinh tự động bằng Python.", P)]

    s += [Paragraph("2. Mô tả dữ liệu và làm sạch", H2),
          Paragraph(f"Dữ liệu: MovieLens ml-latest-small (GroupLens). Phạm vi phân tích: {mo_ta_loc}. "
                    f"Ban đầu có {_n(nhat_ky['so_dong_ban_dau'])} dòng đánh giá. Các bước làm sạch: "
                    f"loại {_n(nhat_ky['bo_dong_thieu'])} dòng thiếu giá trị, "
                    f"{_n(nhat_ky['bo_dong_trung'])} dòng trùng cặp người dùng – phim, "
                    f"{_n(nhat_ky['bo_diem_khong_hop_le'])} dòng có điểm ngoài khoảng 0,5–5; "
                    "chuyển dấu thời gian sang ngày, tách năm phát hành từ tên phim và tách thể loại.", P),
          Spacer(1, 0.2 * cm),
          bang([["Chỉ số", "Giá trị"],
                ["Số lượt đánh giá", _n(tk["so_danh_gia"])],
                ["Số người dùng / số phim", f"{_n(tk['so_nguoi_dung'])} / {_n(tk['so_phim'])}"],
                ["Thời gian đánh giá", f"{tk['tu_nam']}–{tk['den_nam']}"],
                ["Điểm trung bình (độ lệch chuẩn)", f"{tk['diem_tb']:.2f} ({tk['do_lech_chuan']:.2f})"],
                ["Trung vị / điểm phổ biến nhất", f"{tk['diem_trung_vi']:g} / {tk['diem_pho_bien']:g}"],
                ["Độ thưa ma trận người dùng – phim", f"{tk['do_thua']*100:.2f}%"]],
               [9 * cm, 6 * cm]),
          Paragraph("Bảng 1. Thống kê mô tả dữ liệu sau khi làm sạch", C)]

    s += [Paragraph("3. Kết quả phân tích", H2),
          Paragraph("Bảng 2 trình bày 10 phim có điểm trung bình cao nhất (tối thiểu 50 lượt đánh giá).", P),
          Spacer(1, 0.2 * cm)]
    du_lieu = [["STT", "Tên phim", "Số lượt", "Điểm TB"]]
    for i, r in enumerate(tp.itertuples(), 1):
        du_lieu.append([i, Paragraph(str(r.title), P), _n(int(r.so_luot)), f"{r.diem_tb:.2f}"])
    s += [bang(du_lieu, [1.2 * cm, 10 * cm, 2.2 * cm, 2.2 * cm]),
          Paragraph("Bảng 2. Mười phim có điểm trung bình cao nhất", C)]

    b0, b1, b2 = mh["he_so"]
    s += [Paragraph("4. Mô hình hồi quy dự đoán điểm đánh giá", H2),
          Paragraph(f"Mô hình: điểm = b0 + b1 × (điểm TB của người dùng) + b2 × (điểm TB của phim). "
                    f"Dữ liệu chia ngẫu nhiên 80% huấn luyện ({_n(mh['so_mau_train'])} dòng) và 20% kiểm tra "
                    f"({_n(mh['so_mau_test'])} dòng); điểm trung bình chỉ tính trên tập huấn luyện. "
                    f"Hệ số ước lượng: b0 = {b0:.3f}, b1 = {b1:.3f}, b2 = {b2:.3f}.", P),
          Spacer(1, 0.2 * cm),
          bang([["Mô hình", "RMSE trên tập kiểm tra"],
                ["Cơ sở (dự đoán bằng điểm TB toàn bộ)", f"{mh['rmse_co_so']:.4f}"],
                ["Hồi quy tuyến tính", f"{mh['rmse_mo_hinh']:.4f}"],
                ["Mức cải thiện / R²", f"{mh['cai_thien']:.1f}% / {mh['r2']:.3f}"]],
               [9 * cm, 6 * cm]),
          Paragraph("Bảng 3. Kết quả mô hình hồi quy trên tập kiểm tra", C)]

    s += [Paragraph("5. Biểu đồ minh họa", H2),
          hinh(pt.bd_phan_bo_diem(df), "h1.png"), Paragraph("Hình 1. Phân bố điểm đánh giá", C),
          hinh(pt.bd_the_loai(df), "h2.png"), Paragraph("Hình 2. Số lượt đánh giá theo thể loại", C),
          hinh(pt.bd_so_luot_vs_diem(df), "h3.png"),
          Paragraph("Hình 3. Mức độ phổ biến và điểm trung bình của phim", C),
          hinh(pt.bd_du_doan(mh), "h4.png"), Paragraph("Hình 4. Điểm dự đoán theo điểm thực tế", C)]

    if mh["cai_thien"] > 0:
        nhan_xet_mh = (f"Mô hình hồi quy dựa trên điểm trung bình của người dùng và của phim giảm RMSE "
                       f"{mh['cai_thien']:.1f}% so với mô hình cơ sở, cho thấy thói quen chấm điểm của "
                       "người dùng và chất lượng chung của phim là hai yếu tố quan trọng.")
    else:
        nhan_xet_mh = ("Mô hình hồi quy chưa cải thiện được so với mô hình cơ sở trên phạm vi dữ liệu này, "
                       "có thể do số lượt đánh giá của mỗi người dùng và mỗi phim còn ít.")
    s += [Paragraph("6. Kết luận và đề xuất", H2),
          Paragraph(f"Người dùng có xu hướng đánh giá tích cực (điểm trung bình {tk['diem_tb']:.2f}, "
                    f"phổ biến nhất là {tk['diem_pho_bien']:g} điểm). Thể loại {tl.index[0]} nhận nhiều "
                    f"lượt đánh giá nhất. Ma trận người dùng – phim thưa tới {tk['do_thua']*100:.2f}%, "
                    "là thách thức chính của hệ thống gợi ý. " + nhan_xet_mh + " Đề xuất: bổ sung đặc trưng thể loại, thời gian và thử nghiệm "
                    "các mô hình phân rã ma trận hoặc học sâu (NCF) để cải thiện độ chính xác.", P)]

    bo_nho = io.BytesIO()
    SimpleDocTemplate(bo_nho, pagesize=A4, leftMargin=2.2 * cm, rightMargin=2 * cm,
                      topMargin=1.8 * cm, bottomMargin=1.8 * cm,
                      title="Bao cao MovieLens").build(s)
    return bo_nho.getvalue()


if __name__ == "__main__":
    thu_muc = sys.argv[1] if len(sys.argv) > 1 else os.path.join("data", "ml-latest-small")
    print("[1/3] Doc va lam sach du lieu:", thu_muc)
    ratings, movies = pt.doc_du_lieu(thu_muc)
    df, nhat_ky = pt.lam_sach(ratings, movies)
    print("[2/3] Phan tich, chay mo hinh va ve bieu do")
    pdf = tao_bao_cao(df, nhat_ky)
    os.makedirs("reports", exist_ok=True)
    ra = os.path.join("reports", "bao_cao_movielens.pdf")
    with open(ra, "wb") as f:
        f.write(pdf)
    print("[3/3] Hoan thanh! Da tao:", ra)
