# Ứng dụng Ôn tập NLCM

Đây là ứng dụng ôn tập dạng trắc nghiệm được xây dựng bằng [Streamlit](https://streamlit.io/). Ứng dụng cho phép bạn luyện tập với bộ câu hỏi có sẵn trong file Excel và lựa chọn số câu hỏi (10, 20 hoặc 50) để làm bài.

## Tính năng

- Lựa chọn nhanh số lượng câu hỏi (10, 20 hoặc 50 câu)
- Thời gian làm bài mặc định 60 phút cho mỗi lần ôn tập
- Hiển thị từng câu hỏi với các phương án A/B/C/D/E và cho phép điều hướng qua lại
- Chấm điểm tự động, hiển thị số câu đúng và điểm phần trăm sau khi nộp bài hoặc hết giờ
- Bảng chi tiết kết quả cho từng câu hỏi

## Cài đặt

1. **Clone** hoặc tải về thư mục dự án này

```
git clone <đường dẫn repo của bạn>
cd quiz_app
```

2. **Tạo môi trường ảo (khuyến nghị):**

```bash
python -m venv .venv
source .venv/bin/activate  # Windows dùng .venv\Scripts\activate
```

3. **Cài đặt các thư viện phụ thuộc:**

```bash
pip install -r requirements.txt
```

## Chạy ứng dụng

Sử dụng lệnh sau để khởi chạy ứng dụng Streamlit:

```bash
streamlit run app.py
```

Sau khi chạy, một đường dẫn cục bộ sẽ xuất hiện trên terminal. Mở đường dẫn đó trong trình duyệt để sử dụng ứng dụng.

## Cấu trúc thư mục

```
quiz_app/
├── app.py               # Mã nguồn chính của ứng dụng Streamlit
├── requirements.txt     # Danh sách thư viện phụ thuộc
├── README.md            # Hướng dẫn sử dụng
├── Cau hoi on tap 2025.xlsx  # Bộ câu hỏi và đáp án dùng cho ôn tập
└── assets/
    └── app_header.png   # Hình minh họa ở phần đầu trang
```

## Tuỳ chỉnh

Bạn có thể thay đổi dữ liệu câu hỏi bằng cách chỉnh sửa file Excel `Cau hoi on tap 2025.xlsx`. Hãy đảm bảo cấu trúc các cột không thay đổi (TT, Câu hỏi, Phương án A/B/C/D/E, Đ.án đúng, ...). Nếu muốn cập nhật hình minh họa, hãy thay thế file `assets/app_header.png` bằng hình của bạn với tỷ lệ ngang.
