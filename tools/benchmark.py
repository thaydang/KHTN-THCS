#!/usr/bin/env python3
"""Benchmark script for KHTN-THCS performance testing.

This script provides simple benchmarks for key operations to help
identify performance regressions and measure optimization improvements.
"""

import time
import sys
from pathlib import Path
from typing import Callable, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.lesson_plan_generator import build_markdown
from app.timeseries_data import create_sample_timeseries


def benchmark(name: str, func: Callable[[], Any], iterations: int = 100) -> None:
    """Run a benchmark and print results.
    
    Args:
        name: Name of the benchmark
        func: Function to benchmark
        iterations: Number of iterations to run
    """
    print(f"\n{'=' * 60}")
    print(f"Benchmark: {name}")
    print(f"Iterations: {iterations}")
    print(f"{'=' * 60}")
    
    start = time.time()
    for _ in range(iterations):
        func()
    end = time.time()
    
    total_time = end - start
    avg_time = total_time / iterations
    
    print(f"Total time: {total_time:.4f} seconds")
    print(f"Average time: {avg_time * 1000:.2f} ms")
    print(f"Operations/sec: {iterations / total_time:.0f}")


def benchmark_timeseries_generation() -> None:
    """Benchmark timeseries data generation."""
    data = create_sample_timeseries("Thí nghiệm", "Thiết bị", 1.0, 100)


def benchmark_timeseries_serialization() -> None:
    """Benchmark timeseries data serialization."""
    data = create_sample_timeseries("Thí nghiệm", "Thiết bị", 1.0, 100)
    _ = data.to_dict()


def benchmark_timeseries_validation() -> None:
    """Benchmark timeseries data validation."""
    data = create_sample_timeseries("Thí nghiệm", "Thiết bị", 1.0, 100)
    _ = data.validate()


def benchmark_lesson_plan_simple() -> None:
    """Benchmark simple lesson plan generation."""
    config = {
        "metadata": {
            "title": "Bài học thử nghiệm",
            "grade": "Lớp 7",
        },
        "objectives": ["Mục tiêu 1", "Mục tiêu 2", "Mục tiêu 3"],
        "materials": ["Vật liệu 1", "Vật liệu 2"],
    }
    _ = build_markdown(config)


def benchmark_lesson_plan_complex() -> None:
    """Benchmark complex lesson plan with activities."""
    config = {
        "metadata": {
            "title": "Bài học phức tạp",
            "date": "2024-01-15",
            "grade": "Lớp 7",
            "unit": "Chủ đề 3",
            "topic": "Bài 5",
        },
        "objectives": [f"Mục tiêu {i}" for i in range(10)],
        "materials": [f"Vật liệu {i}" for i in range(5)],
        "activities": [
            {
                "title": f"Hoạt động {i}",
                "duration": "10 phút",
                "goals": [f"Mục tiêu {j}" for j in range(3)],
                "steps": [
                    {"actor": "Giáo viên", "content": f"Bước {j}"}
                    for j in range(5)
                ],
                "digital_assets": [f"Học liệu {j}" for j in range(3)],
            }
            for i in range(5)
        ],
        "assessment": [f"Đánh giá {i}" for i in range(3)],
    }
    _ = build_markdown(config)


def main() -> int:
    """Run all benchmarks."""
    print("KHTN-THCS Performance Benchmarks")
    print("=" * 60)
    
    # Timeseries benchmarks
    benchmark("Timeseries: Generation (100 points)", benchmark_timeseries_generation)
    benchmark("Timeseries: Serialization (100 points)", benchmark_timeseries_serialization)
    benchmark("Timeseries: Validation (100 points)", benchmark_timeseries_validation)
    
    # Lesson plan benchmarks
    benchmark("Lesson Plan: Simple", benchmark_lesson_plan_simple)
    benchmark("Lesson Plan: Complex (5 activities)", benchmark_lesson_plan_complex)
    
    print("\n" + "=" * 60)
    print("Benchmarks completed successfully!")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
