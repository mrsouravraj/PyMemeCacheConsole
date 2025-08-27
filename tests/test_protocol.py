from pymemcacheconsole.models import StorageCommand, RetrievalCommand
from pymemcacheconsole.protocol import (
    serialize_storage,
    deserialize_storage,
    serialize_retrieval,
    deserialize_retrieval,
)


def test_serialize_deserialize_storage_roundtrip():
    cmd = StorageCommand(
        command="set",
        key="foo",
        flags=0,
        exptime=0,
        bytes=3,
        value="bar",
        noreply=True,
    )
    msg = serialize_storage(cmd)
    parsed = deserialize_storage(msg)
    assert parsed == cmd


def test_serialize_deserialize_retrieval_roundtrip():
    cmd = RetrievalCommand(keys=["foo", "bar"])
    msg = serialize_retrieval(cmd)
    parsed = deserialize_retrieval(msg)
    assert parsed == cmd


