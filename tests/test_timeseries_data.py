import unittest

from app.timeseries_data import create_sample_timeseries


class CreateSampleTimeseriesTests(unittest.TestCase):
    def test_rejects_non_positive_sampling_rate(self) -> None:
        with self.assertRaisesRegex(ValueError, "sampling_rate_hz must be a positive"):
            create_sample_timeseries("Chủ đề", "Thiết bị", sampling_rate_hz=0)

    def test_rejects_non_positive_num_points(self) -> None:
        with self.assertRaisesRegex(ValueError, "num_points must be greater than zero"):
            create_sample_timeseries("Chủ đề", "Thiết bị", num_points=0)


if __name__ == "__main__":
    unittest.main()
