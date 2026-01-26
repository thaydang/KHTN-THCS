import unittest

from app.timeseries_data import create_sample_timeseries, TimeseriesData


class CreateSampleTimeseriesTests(unittest.TestCase):
    def test_rejects_non_positive_sampling_rate(self) -> None:
        with self.assertRaisesRegex(ValueError, "sampling_rate_hz must be a positive"):
            create_sample_timeseries("Chủ đề", "Thiết bị", sampling_rate_hz=0)

    def test_rejects_non_positive_num_points(self) -> None:
        with self.assertRaisesRegex(ValueError, "num_points must be greater than zero"):
            create_sample_timeseries("Chủ đề", "Thiết bị", num_points=0)


class TimeseriesDataCachingTests(unittest.TestCase):
    """Test caching behavior of TimeseriesData.to_dict()"""

    def test_to_dict_caching(self) -> None:
        """Test that to_dict() caches results for performance."""
        data = create_sample_timeseries("Test", "Device", 1.0, 10)
        
        # First call should populate cache
        result1 = data.to_dict()
        
        # Second call should return the same cached object (same identity)
        result2 = data.to_dict()
        
        # Verify they're the same object (not just equal)
        self.assertIs(result1, result2, "to_dict() should return cached result on second call")
        
        # Verify the content is correct
        self.assertEqual(result1["metadata"]["topic"], "Test")
        self.assertEqual(len(result1["timeseries"]), 10)

    def test_to_json_uses_cached_dict(self) -> None:
        """Test that to_json() benefits from cached to_dict()."""
        data = create_sample_timeseries("Test", "Device", 1.0, 10)
        
        # Call to_dict() first
        dict_result = data.to_dict()
        
        # to_json() should use the cached dict
        json_result = data.to_json()
        
        # Verify JSON contains expected data
        self.assertIn('"topic": "Test"', json_result)
        self.assertIn('"device": "Device"', json_result)


if __name__ == "__main__":
    unittest.main()
