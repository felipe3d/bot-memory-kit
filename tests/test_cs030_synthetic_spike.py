"""Synthetic, local-only acceptance tests for CS-030 Phase 1."""

import unittest

from scripts.cs030_synthetic_spike import (
    SyntheticProjectionPublisher,
    SyntheticVPSReader,
)


class ProjectionScopeTests(unittest.TestCase):
    def test_reader_receives_only_current_canonical_allowed_scope(self):
        records = [
            {
                "id": "AK-SPIKE-ALLOW",
                "status": "canonical",
                "scope": "spike.vps.read",
                "audience": "spike-vps",
                "sensitivity": "internal",
                "expires_at": None,
                "revision": 1,
                "verified_at": "2026-09-18T00:00:00Z",
                "source_locator": "synthetic://allow",
                "body": "synthetic allowed fact",
            },
            {
                "id": "AK-SPIKE-OUT-OF-SCOPE",
                "status": "canonical",
                "scope": "spike.other",
                "audience": "spike-vps",
                "sensitivity": "internal",
                "expires_at": None,
                "revision": 1,
                "verified_at": "2026-09-18T00:00:00Z",
                "source_locator": "synthetic://other",
                "body": "must not publish",
            },
        ]
        publisher = SyntheticProjectionPublisher(
            allowed_scope="spike.vps.read", allowed_audience="spike-vps"
        )
        publication = publisher.publish(records)
        reader = SyntheticVPSReader(publication, identity="synthetic-vps")

        allowed = reader.retrieve("AK-SPIKE-ALLOW")
        self.assertIsNotNone(allowed)
        assert allowed is not None
        self.assertEqual(allowed["body"], "synthetic allowed fact")
        self.assertIsNone(reader.retrieve("AK-SPIKE-OUT-OF-SCOPE"))

    def test_noncanonical_restricted_prohibited_and_expired_records_are_excluded(self):
        base = {
            "scope": "spike.vps.read",
            "audience": "spike-vps",
            "revision": 1,
            "verified_at": "2026-09-18T00:00:00Z",
            "source_locator": "synthetic://fixture",
            "body": "synthetic fixture",
        }
        records = [
            dict(base, id="AK-SPIKE-ALLOW", status="canonical", sensitivity="public", expires_at=None),
            dict(base, id="AK-SPIKE-CANDIDATE", status="candidate", sensitivity="public", expires_at=None),
            dict(base, id="AK-SPIKE-RESTRICTED", status="canonical", sensitivity="restricted", expires_at=None),
            dict(base, id="AK-SPIKE-PROHIBITED", status="canonical", sensitivity="prohibited", expires_at=None),
            dict(base, id="AK-SPIKE-EXPIRED", status="canonical", sensitivity="public", expires_at="2026-01-01T00:00:00Z"),
        ]
        publication = SyntheticProjectionPublisher(
            allowed_scope="spike.vps.read", allowed_audience="spike-vps"
        ).publish(records)
        reader = SyntheticVPSReader(publication, identity="synthetic-vps")

        self.assertEqual(set(publication.records), {"AK-SPIKE-ALLOW"})
        for record_id in ("AK-SPIKE-CANDIDATE", "AK-SPIKE-RESTRICTED", "AK-SPIKE-PROHIBITED", "AK-SPIKE-EXPIRED"):
            self.assertIsNone(reader.retrieve(record_id))

    def test_revocation_fails_closed_without_mutating_published_records(self):
        record = {
            "id": "AK-SPIKE-ALLOW",
            "status": "canonical",
            "scope": "spike.vps.read",
            "audience": "spike-vps",
            "sensitivity": "public",
            "expires_at": None,
            "revision": 1,
            "verified_at": "2026-09-18T00:00:00Z",
            "source_locator": "synthetic://allow",
            "body": "synthetic allowed fact",
        }
        publisher = SyntheticProjectionPublisher(
            allowed_scope="spike.vps.read", allowed_audience="spike-vps"
        )
        publication = publisher.publish([record])
        reader = SyntheticVPSReader(publication, identity="synthetic-vps")

        publisher.revoke(publication)

        self.assertIsNone(reader.retrieve("AK-SPIKE-ALLOW"))
        self.assertIn("AK-SPIKE-ALLOW", publication.records)

    def test_unknown_synthetic_identity_receives_no_projection(self):
        record = {
            "id": "AK-SPIKE-ALLOW",
            "status": "canonical",
            "scope": "spike.vps.read",
            "audience": "spike-vps",
            "sensitivity": "public",
            "expires_at": None,
            "revision": 1,
            "verified_at": "2026-09-18T00:00:00Z",
            "source_locator": "synthetic://allow",
            "body": "synthetic allowed fact",
        }
        publication = SyntheticProjectionPublisher(
            allowed_scope="spike.vps.read", allowed_audience="spike-vps"
        ).publish([record])

        self.assertIsNone(
            SyntheticVPSReader(publication, identity="synthetic-other").retrieve(
                "AK-SPIKE-ALLOW"
            )
        )

    def test_reader_cannot_write_or_mutate_the_publication(self):
        publication = SyntheticProjectionPublisher(
            allowed_scope="spike.vps.read", allowed_audience="spike-vps"
        ).publish([])
        reader = SyntheticVPSReader(publication, identity="synthetic-vps")

        with self.assertRaises(PermissionError):
            reader.write("AK-SPIKE-NEW", {"body": "synthetic write"})

        self.assertEqual(publication.records, {})

    def test_tampered_publication_fails_closed(self):
        record = {
            "id": "AK-SPIKE-ALLOW",
            "status": "canonical",
            "scope": "spike.vps.read",
            "audience": "spike-vps",
            "sensitivity": "public",
            "expires_at": None,
            "revision": 1,
            "verified_at": "2026-09-18T00:00:00Z",
            "source_locator": "synthetic://allow",
            "body": "synthetic allowed fact",
        }
        publication = SyntheticProjectionPublisher(
            allowed_scope="spike.vps.read", allowed_audience="spike-vps"
        ).publish([record])
        publication.records["AK-SPIKE-ALLOW"]["body"] = "tampered"

        self.assertIsNone(
            SyntheticVPSReader(publication, identity="synthetic-vps").retrieve(
                "AK-SPIKE-ALLOW"
            )
        )


if __name__ == "__main__":
    unittest.main()
