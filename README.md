# MovieLens Dashboard – Phân tích dữ liệu và sinh báo cáo khoa học tự động

Mini-project học phần **Công nghệ số nâng cao (CT999)** – Trường Công nghệ Thông tin và Truyền thông, Đại học Cần Thơ.

## Giới thiệu đề tài
Hệ thống gợi ý cần dự đoán mức độ yêu thích của người dùng đối với sản phẩm chưa xem. Dự án phân tích dữ liệu đánh giá phim **MovieLens**, xây dựng mô hình hồi quy tuyến tính dự đoán điểm đánh giá, **tự động sinh báo cáo PDF** và cung cấp **dashboard tương tác** bằng Streamlit.

## Mục tiêu
- Làm sạch và phân tích dữ liệu đánh giá phim bằng `pandas`, `numpy`.
- Trực quan hóa dữ liệu bằng `matplotlib`.
- Xây dựng mô hình hồi quy tuyến tính dự đoán điểm, đánh giá bằng RMSE.
- Tự động sinh báo cáo khoa học PDF bằng `reportlab`.
- Xây dựng dashboard cho phép chọn biến, xem biểu đồ và tải báo cáo.

## Phương pháp
1. **Làm sạch:** loại dòng thiếu, dòng trùng, điểm không hợp lệ; tách năm phát hành và thể loại.
2. **Phân tích mô tả:** thống kê điểm, độ thưa ma trận, top phim, thể loại.
3. **Mô hình:** `điểm = b0 + b1 × điểm TB người dùng + b2 × điểm TB phim`, chia 80/20, so sánh RMSE với mô hình cơ sở.
4. **Báo cáo và dashboard:** sinh PDF tự động, giao diện Streamlit.

## Cấu trúc thư mục
```
movielens-dashboard/
├── app.py                  # Dashboard Streamlit
├── src/
│   ├── phan_tich.py        # Làm sạch, thống kê, mô hình, biểu đồ
│   ├── tao_bao_cao.py      # Sinh báo cáo PDF
│   └── tai_du_lieu.py      # Tải dữ liệu MovieLens
├── data/                   # Dữ liệu (tải về bằng tai_du_lieu.py)
├── reports/                # Báo cáo PDF đã sinh
├── docs/                   # Ảnh minh họa
├── requirements.txt
├── LICENSE
└── README.md
```

## Cách chạy
```bash
py -m pip install -r requirements.txt   # 1. Cài thư viện
py src/tai_du_lieu.py                   # 2. Tải dữ liệu
py src/tao_bao_cao.py                   # 3. Sinh báo cáo PDF -> reports/
py -m streamlit run app.py              # 4. Mở dashboard
```

## Kết quả
- Báo cáo PDF: [`reports/bao_cao_movielens.pdf`](reports/bao_cao_movielens.pdf)
- Dashboard: lọc theo thể loại, năm phát hành; chọn biểu đồ; chạy mô hình; tải báo cáo PDF.

## Dữ liệu
Bộ dữ liệu **MovieLens ml-latest-small** do GroupLens Research (University of Minnesota) cung cấp.
Theo điều khoản sử dụng của GroupLens, dữ liệu **không được phân phối lại**, vì vậy repo không chứa dữ liệu gốc;
hãy tải về bằng `src/tai_du_lieu.py` hoặc tại <https://grouplens.org/datasets/movielens/>.

> F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets: History and Context.
> ACM Transactions on Interactive Intelligent Systems 5(4), Article 19. https://doi.org/10.1145/2827872

## Nhóm thực hiện
| Thành viên | Vai trò |
|---|---|
| Võ Duy Nhứt (M2526012) | Trưởng nhóm, điều phối, kiểm tra tổng thể |
| Huỳnh Nhật Trường (M2526015) | Nghiên cứu tài liệu, phân tích dữ liệu |
| Võ Thị Cẩm Ngân | Tổng hợp, biên tập báo cáo |
| Lê Trung Tín | Thiết kế giao diện dashboard, rà soát tài liệu |

## Giấy phép
Mã nguồn được phát hành theo giấy phép **MIT** – xem tệp [LICENSE](LICENSE).
Dữ liệu MovieLens tuân theo điều khoản sử dụng riêng của GroupLens.
