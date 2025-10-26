#!/usr/bin/env python3
"""Command-line tool for working with timeseries experiment data.

This tool allows you to create, validate, and visualize timeseries data
from science experiments.
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.timeseries_data import TimeseriesData, create_sample_timeseries


def validate_command(args: argparse.Namespace) -> int:
    """Validate a timeseries data file.
    
    Args:
        args: Command-line arguments
        
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"❌ Lỗi: Không tìm thấy tệp {input_path}")
        return 1
    
    try:
        data = TimeseriesData.from_json_file(input_path)
        is_valid, error_msg = data.validate()
        
        if is_valid:
            print(f"✅ Dữ liệu hợp lệ!")
            print(f"   📊 Số điểm dữ liệu: {len(data.timeseries)}")
            print(f"   🔬 Chủ đề: {data.metadata.topic}")
            print(f"   📱 Thiết bị: {data.metadata.device}")
            print(f"   ⏱️  Tần số lấy mẫu: {data.metadata.sampling_rate_hz} Hz")
            return 0
        else:
            print(f"❌ Dữ liệu không hợp lệ: {error_msg}")
            return 1
    except Exception as e:
        print(f"❌ Lỗi khi đọc tệp: {e}")
        return 1


def create_sample_command(args: argparse.Namespace) -> int:
    """Create a sample timeseries data file.
    
    Args:
        args: Command-line arguments
        
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    output_path = Path(args.output)
    
    try:
        data = create_sample_timeseries(
            topic=args.topic,
            device=args.device,
            sampling_rate_hz=args.sampling_rate,
            num_points=args.num_points
        )
        
        data.save(output_path)
        print(f"✅ Đã tạo tệp dữ liệu mẫu tại: {output_path}")
        print(f"   📊 Số điểm dữ liệu: {len(data.timeseries)}")
        return 0
    except Exception as e:
        print(f"❌ Lỗi khi tạo tệp: {e}")
        return 1


def info_command(args: argparse.Namespace) -> int:
    """Display information about a timeseries data file.
    
    Args:
        args: Command-line arguments
        
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"❌ Lỗi: Không tìm thấy tệp {input_path}")
        return 1
    
    try:
        data = TimeseriesData.from_json_file(input_path)
        
        print("=" * 60)
        print("📊 THÔNG TIN DỮ LIỆU THÍ NGHIỆM")
        print("=" * 60)
        print(f"\n🔬 Chủ đề: {data.metadata.topic}")
        print(f"📱 Thiết bị: {data.metadata.device}")
        print(f"⏱️  Tần số lấy mẫu: {data.metadata.sampling_rate_hz} Hz")
        print(f"📅 Thời gian tạo: {data.metadata.created_at}")
        print(f"📌 Phiên bản: {data.metadata.version}")
        
        print(f"\n📈 Biến số đo lường:")
        for i, var in enumerate(data.variables, 1):
            print(f"   {i}. {var.name} ({var.unit}) - Loại: {var.type}")
        
        print(f"\n📊 Dữ liệu chuỗi thời gian:")
        print(f"   Số điểm: {len(data.timeseries)}")
        if data.timeseries:
            first_point = data.timeseries[0]
            last_point = data.timeseries[-1]
            print(f"   Thời gian bắt đầu: {first_point.time_s}s")
            print(f"   Thời gian kết thúc: {last_point.time_s}s")
            print(f"   Nhiệt độ ban đầu: {first_point.temp_C}°C")
            print(f"   Nhiệt độ cuối: {last_point.temp_C}°C")
        
        is_valid, error_msg = data.validate()
        print(f"\n{'✅' if is_valid else '❌'} Tình trạng: {'Hợp lệ' if is_valid else f'Không hợp lệ - {error_msg}'}")
        print("=" * 60)
        
        return 0
    except Exception as e:
        print(f"❌ Lỗi khi đọc tệp: {e}")
        return 1


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Công cụ xử lý dữ liệu chuỗi thời gian cho thí nghiệm khoa học."
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Lệnh thực hiện")
    
    # Validate command
    validate_parser = subparsers.add_parser(
        "validate",
        help="Kiểm tra tính hợp lệ của tệp dữ liệu"
    )
    validate_parser.add_argument(
        "input",
        help="Đường dẫn tệp JSON cần kiểm tra"
    )
    
    # Create sample command
    create_parser = subparsers.add_parser(
        "create-sample",
        help="Tạo tệp dữ liệu mẫu"
    )
    create_parser.add_argument(
        "output",
        help="Đường dẫn tệp JSON đầu ra"
    )
    create_parser.add_argument(
        "--topic",
        default="Thí nghiệm mẫu",
        help="Chủ đề thí nghiệm (mặc định: 'Thí nghiệm mẫu')"
    )
    create_parser.add_argument(
        "--device",
        default="Thiết bị đo mẫu",
        help="Tên thiết bị đo (mặc định: 'Thiết bị đo mẫu')"
    )
    create_parser.add_argument(
        "--sampling-rate",
        type=float,
        default=1.0,
        help="Tần số lấy mẫu (Hz) (mặc định: 1.0)"
    )
    create_parser.add_argument(
        "--num-points",
        type=int,
        default=10,
        help="Số điểm dữ liệu (mặc định: 10)"
    )
    
    # Info command
    info_parser = subparsers.add_parser(
        "info",
        help="Hiển thị thông tin chi tiết về tệp dữ liệu"
    )
    info_parser.add_argument(
        "input",
        help="Đường dẫn tệp JSON cần xem thông tin"
    )
    
    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()
    
    if args.command == "validate":
        return validate_command(args)
    elif args.command == "create-sample":
        return create_sample_command(args)
    elif args.command == "info":
        return info_command(args)
    else:
        print("❌ Lỗi: Vui lòng chọn một lệnh (validate, create-sample, info)")
        print("   Sử dụng --help để xem hướng dẫn")
        return 1


if __name__ == "__main__":
    sys.exit(main())
