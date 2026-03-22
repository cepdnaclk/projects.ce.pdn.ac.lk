import unittest

from python_scripts.util.algolia_projects import (
    build_project_record,
    diff_records,
    sanitize_url,
    transform_projects_payload,
)


class TestAlgoliaProjects(unittest.TestCase):
    def test_sanitize_url_rejects_placeholders_and_invalid_urls(self) -> None:
        self.assertIsNone(sanitize_url("#"))
        self.assertIsNone(sanitize_url("notaurl"))
        self.assertEqual(sanitize_url("https://projects.ce.pdn.ac.lk/demo/"), "https://projects.ce.pdn.ac.lk/demo/")

    def test_build_project_record_normalizes_sparse_fields(self) -> None:
        record = build_project_record(
            "e21-demo",
            {
                "title": " Demo Project ",
                "description": "  A useful project description.  ",
                "category": {"title": "Final Year Projects", "code": "4yp"},
                "project_url": "https://projects.ce.pdn.ac.lk/4yp/e21/demo/",
                "repo_url": "https://github.com/cepdnaclk/e21-demo",
                "page_url": "#",
                "api_url": "https://api.ce.pdn.ac.lk/projects/v1/4yp/E21/demo/",
                "thumbnail_url": "https://projects.ce.pdn.ac.lk/thumb.jpg",
                "tags": ["AI", "", "ai", "#", "Vision"],
                "team": {
                    "E/21/001": {
                        "name": "Alice Example",
                        "email": "e21001@eng.pdn.ac.lk",
                        "profile_url": "https://people.ce.pdn.ac.lk/students/e21/001/",
                        "profile_image": "https://people.ce.pdn.ac.lk/images/students/e21/e21001.jpg",
                    }
                },
                "supervisors": {
                    "mentor@eng.pdn.ac.lk": {
                        "name": "Dr. Mentor",
                        "email": "mentor@eng.pdn.ac.lk",
                        "profile_url": "https://people.ce.pdn.ac.lk/staff/academic/mentor/",
                        "profile_image": "https://people.ce.pdn.ac.lk/images/staff/mentor.jpg",
                    }
                },
            },
        )

        self.assertEqual(record["title"], "Demo Project")
        self.assertEqual(record["page_url"], None)
        self.assertEqual(record["tags"], ["AI", "Vision"])
        self.assertEqual(record["team_names"], ["Alice Example"])
        self.assertEqual(record["supervisor_names"], ["Dr. Mentor"])
        self.assertEqual(record["result_url"], "https://projects.ce.pdn.ac.lk/4yp/e21/demo/")

    def test_transform_projects_payload_reports_invalid_records(self) -> None:
        records, errors = transform_projects_payload(
            {
                "valid-project": {
                    "title": "Valid Project",
                    "category": {"title": "Course", "code": "co227"},
                },
                "broken-project": {"title": "   "},
                "not-an-object": [],
            }
        )

        self.assertEqual(len(records), 1)
        self.assertEqual(len(errors), 2)

    def test_diff_records_returns_upserts_and_deletes(self) -> None:
        existing = [
            {"objectID": "same", "title": "Same"},
            {"objectID": "old", "title": "Old"},
        ]
        target = [
            {"objectID": "same", "title": "Same"},
            {"objectID": "new", "title": "New"},
        ]

        to_upsert, to_delete = diff_records(existing, target)
        self.assertEqual([record["objectID"] for record in to_upsert], ["new"])
        self.assertEqual(to_delete, ["old"])


if __name__ == "__main__":
    unittest.main()
