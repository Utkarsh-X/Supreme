import unittest
import datetime
import uuid
from session_serializer import SessionSerializer

class TestSessionSerializer(unittest.TestCase):
    def setUp(self):
        self.serializer = SessionSerializer()

    def test_basic_types(self):
        data = {"user_id": 42, "username": "alice", "is_active": True}
        serialized = self.serializer.serialize(data)
        deserialized = self.serializer.deserialize(serialized)
        self.assertEqual(data, deserialized)

    def test_datetime_serialization(self):
        now = datetime.datetime(2026, 8, 13, 12, 0, 0)
        data = {"last_login": now}
        serialized = self.serializer.serialize(data)
        self.assertIn("2026-08-13T12:00:00", serialized)

    def test_uuid_serialization(self):
        session_id = uuid.uuid4()
        data = {"session_id": session_id}
        serialized = self.serializer.serialize(data)
        self.assertIn(str(session_id), serialized)

if __name__ == "__main__":
    unittest.main()
