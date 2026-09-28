import unittest
from io import BytesIO
from unittest.mock import patch

from tool import profile_records, estimate_dataset_cost


class DatasetSamplerTests(unittest.TestCase):
    def test_profiles_field_coverage_and_nulls(self):
        result = profile_records([{"name": "A", "country": "US"}, {"name": "B", "country": None}])
        self.assertEqual(result["record_count"], 2)
        self.assertEqual(result["field_coverage"]["name"]["present"], 2)
        self.assertEqual(result["field_coverage"]["country"]["present"], 1)

    def test_empty_records_have_no_fields(self):
        self.assertEqual(profile_records([])["field_coverage"], {})

    def test_cost_estimate_uses_returned_records_and_validates_inputs(self):
        self.assertEqual(estimate_dataset_cost(1200), 3.0)
        with self.assertRaises(ValueError):
            estimate_dataset_cost(-1)

    def test_live_sample_size_is_bounded(self):
        with patch("tool.urlopen") as request:
            with self.assertRaises(ValueError):
                from tool import sample_linkedin_people
                sample_linkedin_people("token", "x", size=1001)
            request.assert_not_called()

    def test_live_sample_uses_documented_marketplace_search_route(self):
        from tool import sample_linkedin_people
        response = BytesIO(b'{"hits": [], "total_hits": 0}')
        with patch("tool.urlopen", return_value=response) as mocked:
            sample_linkedin_people("test-key", "engineer", size=7)
        request = mocked.call_args.args[0]
        self.assertEqual(request.full_url, "https://api.brightdata.com/datasets/search/gd_l1viktl72bvl7bjuj0")
        self.assertIn(b'"sort": "random"', request.data)
        self.assertIn(b'"size": 7', request.data)

    def test_profile_marks_sample_exploratory_and_non_representative(self):
        result = profile_records([{"name": "A"}])
        self.assertIn("exploratory", result["decision_note"].lower())
        self.assertIn("not representative", result["decision_note"].lower())

    def test_live_api_errors_have_actionable_message(self):
        from urllib.error import HTTPError
        from tool import sample_linkedin_people
        with patch("tool.urlopen", side_effect=HTTPError("https://api.brightdata.com", 429, "Too Many Requests", {}, BytesIO(b"sensitive response"))):
            with self.assertRaises(HTTPError) as error:
                sample_linkedin_people("test-key", "engineer")
            self.assertNotIn("sensitive response", str(error.exception))

    def test_live_cli_errors_are_structured_and_do_not_retry_or_leak_secrets(self):
        import os
        import json
        from contextlib import redirect_stderr
        from io import StringIO
        from urllib.error import URLError
        from tool import main
        with patch("tool.sample_linkedin_people", side_effect=URLError("secret-token")), patch.dict(os.environ, {"BRIGHT_DATA_API_KEY": "secret-token"}), patch("sys.argv", ["tool.py", "--live", "x"]), redirect_stderr(StringIO()) as error:
            with self.assertRaises(SystemExit) as exit_error:
                main()
        payload = json.loads(error.getvalue())
        self.assertEqual(exit_error.exception.code, 1)
        self.assertFalse(payload["error"]["retryable"])
        self.assertNotIn("secret-token", error.getvalue())


if __name__ == "__main__":
    unittest.main()
