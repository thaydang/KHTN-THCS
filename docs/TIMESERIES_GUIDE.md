# Công cụ Dữ liệu Chuỗi Thời gian (Timeseries Data Tool)

## Giới thiệu

Công cụ này hỗ trợ giáo viên và học sinh lưu trữ, xác thực và quản lý dữ liệu thí nghiệm khoa học theo chuỗi thời gian. Dữ liệu được lưu trữ theo định dạng JSON chuẩn hóa, phù hợp cho các thí nghiệm đo lường nhiệt độ, áp suất, hoặc các đại lượng vật lý khác theo thời gian.

## Cấu trúc Dữ liệu

Mỗi tệp dữ liệu chuỗi thời gian bao gồm ba phần chính:

### 1. Metadata (Siêu dữ liệu)
Thông tin về thí nghiệm và thiết bị đo:
- **topic** (bắt buộc): Chủ đề/tên thí nghiệm
- **device** (bắt buộc): Tên thiết bị đo
- **sampling_rate_hz** (bắt buộc): Tần số lấy mẫu (Hz)
- **created_at** (tùy chọn): Thời gian tạo dữ liệu (ISO 8601)
- **version** (tùy chọn): Phiên bản schema

### 2. Variables (Biến số)
Danh sách các biến số được đo:
- **name** (bắt buộc): Tên biến
- **unit** (bắt buộc): Đơn vị đo
- **type** (bắt buộc): Loại dữ liệu (ví dụ: "continuous", "discrete")

### 3. Timeseries (Dữ liệu chuỗi thời gian)
Dữ liệu đo thực tế (tối thiểu 5 điểm):
- **time_s** (bắt buộc): Thời gian (giây, ≥ 0)
- **temp_C** (bắt buộc): Nhiệt độ (°C)

## Ví dụ Tệp Dữ liệu

```json
{
  "metadata": {
    "topic": "Nung nóng nước - Quan sát sự thay đổi nhiệt độ",
    "device": "Nhiệt kế điện tử DS18B20",
    "sampling_rate_hz": 0.5,
    "created_at": "2024-10-26T10:30:00+07:00",
    "version": "1.0"
  },
  "variables": [
    {
      "name": "time",
      "unit": "seconds",
      "type": "continuous"
    },
    {
      "name": "temperature",
      "unit": "Celsius",
      "type": "continuous"
    }
  ],
  "timeseries": [
    {"time_s": 0, "temp_C": 25.0},
    {"time_s": 2, "temp_C": 28.5},
    {"time_s": 4, "temp_C": 32.1},
    {"time_s": 6, "temp_C": 35.8},
    {"time_s": 8, "temp_C": 39.2}
  ]
}
```

## Sử dụng Công cụ CLI

### 1. Kiểm tra tính hợp lệ (Validate)

Kiểm tra xem tệp dữ liệu có tuân thủ schema không:

```bash
python app/timeseries_tool.py validate <đường-dẫn-tệp.json>
```

Ví dụ:
```bash
python app/timeseries_tool.py validate samples/heating_water_experiment.json
```

Kết quả:
```
✅ Dữ liệu hợp lệ!
   📊 Số điểm dữ liệu: 10
   🔬 Chủ đề: Nung nóng nước - Quan sát sự thay đổi nhiệt độ
   📱 Thiết bị: Nhiệt kế điện tử DS18B20
   ⏱️  Tần số lấy mẫu: 0.5 Hz
```

### 2. Xem thông tin chi tiết (Info)

Hiển thị thông tin đầy đủ về tệp dữ liệu:

```bash
python app/timeseries_tool.py info <đường-dẫn-tệp.json>
```

Ví dụ:
```bash
python app/timeseries_tool.py info samples/heating_water_experiment.json
```

### 3. Tạo tệp dữ liệu mẫu (Create Sample)

Tạo tệp dữ liệu mẫu cho mục đích thử nghiệm:

```bash
python app/timeseries_tool.py create-sample <tệp-đầu-ra.json> \
  --topic "Chủ đề thí nghiệm" \
  --device "Tên thiết bị" \
  --sampling-rate 1.0 \
  --num-points 10
```

Ví dụ:
```bash
python app/timeseries_tool.py create-sample outputs/my_experiment.json \
  --topic "Thí nghiệm làm lạnh nước" \
  --device "Nhiệt kế thủy ngân" \
  --sampling-rate 2.0 \
  --num-points 15
```

## Sử dụng Thư viện Python

Bạn có thể import và sử dụng các class trong code Python:

```python
from pathlib import Path
from app.timeseries_data import (
    TimeseriesData,
    Metadata,
    Variable,
    TimeseriesDataPoint,
    create_sample_timeseries
)

# Tạo dữ liệu mới
metadata = Metadata(
    topic="Thí nghiệm của tôi",
    device="Nhiệt kế điện tử",
    sampling_rate_hz=1.0
)

variables = [
    Variable(name="time", unit="seconds", type="continuous"),
    Variable(name="temperature", unit="Celsius", type="continuous")
]

timeseries = [
    TimeseriesDataPoint(time_s=0, temp_C=25.0),
    TimeseriesDataPoint(time_s=1, temp_C=26.5),
    TimeseriesDataPoint(time_s=2, temp_C=28.0),
    TimeseriesDataPoint(time_s=3, temp_C=29.5),
    TimeseriesDataPoint(time_s=4, temp_C=31.0),
]

data = TimeseriesData(
    metadata=metadata,
    variables=variables,
    timeseries=timeseries
)

# Xác thực dữ liệu
is_valid, error_msg = data.validate()
if is_valid:
    print("Dữ liệu hợp lệ!")
    # Lưu vào tệp
    data.save(Path("output.json"))
else:
    print(f"Lỗi: {error_msg}")

# Đọc từ tệp
data = TimeseriesData.from_json_file(Path("input.json"))
```

## Quy tắc Xác thực

Công cụ sẽ kiểm tra các điều kiện sau:

1. ✅ Dữ liệu chuỗi thời gian phải có **ít nhất 5 điểm**
2. ✅ Giá trị `time_s` phải **không âm** (≥ 0)
3. ✅ Trường `topic` và `device` trong metadata **không được rỗng**
4. ✅ `sampling_rate_hz` phải là **số dương** (> 0)
5. ✅ Phải có **ít nhất một biến số** được định nghĩa
6. ✅ Mỗi biến số phải có đầy đủ `name`, `unit`, và `type`

## Ứng dụng Thực tế

Công cụ này có thể được sử dụng cho:

- 🌡️ Thí nghiệm đo nhiệt độ (nung nóng, làm lạnh)
- 📈 Theo dõi biến đổi áp suất
- 🔬 Ghi nhận tốc độ phản ứng hóa học
- 🌍 Đo độ ẩm, ánh sáng trong môi trường
- ⚡ Thí nghiệm về điện (dòng điện, điện áp theo thời gian)

## Tích hợp với Bảng Tuần hoàn

Hình ảnh bảng tuần hoàn các nguyên tố hóa học trong issue gợi ý rằng công cụ này có thể được mở rộng để:
- Lưu trữ dữ liệu về tính chất của các nguyên tố
- Theo dõi phản ứng hóa học giữa các nguyên tố
- Ghi nhận kết quả thí nghiệm hóa học theo thời gian

## Ghi chú

- Dữ liệu được lưu trữ với encoding UTF-8 để hỗ trợ tiếng Việt
- Định dạng JSON dễ đọc và có thể chỉnh sửa bằng trình soạn thảo văn bản
- Tệp dữ liệu có thể được chia sẻ giữa giáo viên và học sinh
- Tương thích với các công cụ phân tích dữ liệu (Python, R, Excel)

## Tài liệu Tham khảo

- [JSON Schema](http://json-schema.org/draft-07/schema)
- [ISO 8601 Date Format](https://en.wikipedia.org/wiki/ISO_8601)
- Chương trình GDPT 2018 - Khoa học Tự nhiên THCS
