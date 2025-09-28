# Kho tài liệu Khoa học Tự nhiên THCS

Repo này lưu trữ và chia sẻ tài liệu dạy học môn Khoa học Tự nhiên cấp THCS. Bao gồm giáo án, đề kiểm tra, thí nghiệm ảo và tài liệu tham khảo.

## Mục tiêu
- Quản lý tài liệu dạy học có hệ thống.
- Hỗ trợ giáo viên trong tổ cùng xây dựng kho chung.
- Giúp học sinh truy cập tài nguyên học tập trực tuyến.

## Cấu trúc thư mục
- **GiaoAn/**: Giáo án theo từng lớp (6, 7, 8, 9).
- **DeKiemTra/**: Ma trận, bản đặc tả, đề và đáp án (giữa kỳ, cuối kỳ).
- **ThiNghiemAo/**: Thí nghiệm mô phỏng (Hóa, Lý, Sinh).
- **TaiLieu/**: SGK, công văn và tài liệu tham khảo.
- **tools/lesson_planner/**: Ứng dụng tạo kế hoạch bài dạy KHTN và xuất Markdown.

## Hướng dẫn sử dụng
1. Clone repo về máy:
   ```
   git clone https://github.com/<tai-khoan>/KHTN-THCS.git
   cd KHTN-THCS
   ```
2. Thêm hoặc chỉnh sửa tài liệu vào thư mục phù hợp.
3. Commit thay đổi:
   ```
   git add .
   git commit -m "Cập nhật giáo án Lớp 7 - Nồng độ dung dịch"
   git push
   ```

## Ứng dụng tạo kế hoạch bài dạy KHTN

Thư mục `tools/lesson_planner/` chứa script Python hỗ trợ soạn giáo án/bài giảng điện tử
và xuất ra file Markdown có thể nhúng công thức LaTeX.

### Cách chạy

1. (Tuỳ chọn) Tạo kế hoạch từ file JSON mẫu:
   ```
   cd tools/lesson_planner
   python lesson_plan_generator.py --from-json sample_lesson_plan.json ke_hoach.md
   ```

2. Hoặc nhập liệu tương tác trực tiếp trên terminal:
   ```
   cd tools/lesson_planner
   python lesson_plan_generator.py --interactive ke_hoach.md
   ```

Script sẽ tạo file `.md` chứa đầy đủ cấu trúc mục tiêu, học liệu, hoạt động dạy học,
đánh giá... Các công thức viết dạng LaTeX (ví dụ `$F = ma$`) sẽ giữ nguyên trong
file Markdown để sử dụng với các hệ thống hỗ trợ MathJax.

## Đóng góp
- Giáo viên: fork repo, chỉnh sửa và gửi pull request.
- Học sinh: tải tài liệu hoặc gửi đề xuất qua Issues.

## Bản quyền
- Tài liệu tuân thủ Chương trình GDPT 2018 và công văn Bộ GD&ĐT.
- Dùng cho mục đích dạy học, không thương mại hóa.
