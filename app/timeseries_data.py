"""Timeseries data handler for science experiments.

This module provides utilities for creating, validating, and working with
timeseries experimental data following a structured JSON schema. It's designed
to support laboratory experiments where measurements are taken over time.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class Variable:
    """Represents a variable being measured in the experiment."""

    name: str
    unit: str
    type: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return asdict(self)


@dataclass
class Metadata:
    """Metadata about the experiment and data collection."""

    topic: str
    device: str
    sampling_rate_hz: float
    created_at: Optional[str] = None
    version: Optional[str] = None

    def __post_init__(self):
        """Set default values after initialization."""
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.version is None:
            self.version = "1.0"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return asdict(self)


@dataclass
class TimeseriesDataPoint:
    """A single measurement point in the timeseries.

    Note: Currently supports temperature measurements as specified in the schema.
    The schema requires time_s and temp_C fields. For other measurement types,
    the schema would need to be extended.
    """

    time_s: float
    temp_C: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return asdict(self)


@dataclass
class TimeseriesData:
    """Complete timeseries experiment data with metadata and measurements."""

    metadata: Metadata
    variables: List[Variable]
    timeseries: List[TimeseriesDataPoint] = field(default_factory=list)

    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate the timeseries data against schema requirements.

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check minimum timeseries items
        if len(self.timeseries) < 5:
            return (
                False,
                f"Timeseries must have at least 5 data points, got {len(self.timeseries)}",
            )

        # Check all time values are non-negative
        for i, point in enumerate(self.timeseries):
            if point.time_s < 0:
                return (
                    False,
                    f"Time value at index {i} must be non-negative, got {point.time_s}",
                )

        # Check required metadata fields
        if not self.metadata.topic:
            return False, "Metadata.topic is required"
        if not self.metadata.device:
            return False, "Metadata.device is required"
        if self.metadata.sampling_rate_hz <= 0:
            return (
                False,
                f"Metadata.sampling_rate_hz must be positive, got {self.metadata.sampling_rate_hz}",
            )

        # Check variables
        if len(self.variables) == 0:
            return False, "At least one variable must be defined"

        for i, var in enumerate(self.variables):
            if not var.name:
                return False, f"Variable at index {i} must have a name"
            if not var.unit:
                return False, f"Variable at index {i} must have a unit"
            if not var.type:
                return False, f"Variable at index {i} must have a type"

        return True, None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation for JSON serialization."""
        return {
            "metadata": asdict(self.metadata),
            "variables": [asdict(var) for var in self.variables],
            "timeseries": [asdict(point) for point in self.timeseries],
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def save(self, path: Path) -> None:
        """Save timeseries data to a JSON file."""
        path.write_text(self.to_json(), encoding="utf-8")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TimeseriesData:
        """Create TimeseriesData from a dictionary.

        Note: This implementation follows the schema specification which requires
        time_s and temp_C fields in timeseries data points. The variables array
        is for documentation purposes to describe what measurements are being taken.

        Args:
            data: Dictionary containing metadata, variables, and timeseries

        Returns:
            TimeseriesData instance
        """
        metadata_dict = data.get("metadata", {})
        metadata = Metadata(
            topic=metadata_dict.get("topic", ""),
            device=metadata_dict.get("device", ""),
            sampling_rate_hz=metadata_dict.get("sampling_rate_hz", 1.0),
            created_at=metadata_dict.get("created_at"),
            version=metadata_dict.get("version"),
        )

        variables = [
            Variable(
                name=var.get("name", ""),
                unit=var.get("unit", ""),
                type=var.get("type", ""),
            )
            for var in data.get("variables", [])
        ]

        timeseries = [
            TimeseriesDataPoint(
                time_s=point.get("time_s", 0.0), temp_C=point.get("temp_C", 0.0)
            )
            for point in data.get("timeseries", [])
        ]

        return cls(metadata=metadata, variables=variables, timeseries=timeseries)

    @classmethod
    def from_json_file(cls, path: Path) -> TimeseriesData:
        """Load timeseries data from a JSON file.

        Args:
            path: Path to JSON file

        Returns:
            TimeseriesData instance
        """
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)


def create_sample_timeseries(
    topic: str, device: str, sampling_rate_hz: float = 1.0, num_points: int = 10
) -> TimeseriesData:
    """Create sample timeseries data for demonstration purposes.

    Args:
        topic: The experiment topic
        device: The measuring device used
        sampling_rate_hz: Sampling rate in Hz
        num_points: Number of data points to generate

    Returns:
        TimeseriesData with sample measurements
    """
    if sampling_rate_hz <= 0:
        raise ValueError(
            "sampling_rate_hz must be a positive value to generate sample data"
        )
    if num_points <= 0:
        raise ValueError("num_points must be greater than zero")

    metadata = Metadata(topic=topic, device=device, sampling_rate_hz=sampling_rate_hz)

    variables = [
        Variable(name="time", unit="seconds", type="continuous"),
        Variable(name="temperature", unit="Celsius", type="continuous"),
    ]

    # Generate sample temperature data (simulating heating)
    timeseries = []
    base_temp = 25.0  # Room temperature in Celsius
    for i in range(num_points):
        time_s = i * (1.0 / sampling_rate_hz)
        # Simulate gradual heating
        temp_C = base_temp + (i * 2.5)
        timeseries.append(TimeseriesDataPoint(time_s=time_s, temp_C=temp_C))

    return TimeseriesData(metadata=metadata, variables=variables, timeseries=timeseries)
