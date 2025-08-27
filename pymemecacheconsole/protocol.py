from .models import StorageCommand, RetrievalCommand, ValueResponse


def serialize_storage(cmd: StorageCommand) -> str:
    base = f"{cmd.command} {cmd.key} {cmd.flags} {cmd.exptime} {cmd.bytes}"
    if cmd.noreply:
        base += " noreply"
    return f"{base}\r\n{cmd.value}\r\n"


def deserialize_storage(msg: str) -> StorageCommand:
    header, value = msg.split("\r\n", 1)
    value = value.strip()
    parts = header.split()
    command, key, flags, exptime, byte_count, *rest = parts
    noreply = "noreply" in rest
    return StorageCommand(
        command=command,
        key=key,
        flags=int(flags),
        exptime=int(exptime),
        bytes=int(byte_count),
        value=value,
        noreply=noreply,
    )


def serialize_retrieval(cmd: RetrievalCommand) -> str:
    return f"get {' '.join(cmd.keys)}\r\n"


def deserialize_retrieval(msg: str) -> RetrievalCommand:
    parts = msg.strip().split()
    assert parts[0] == "get"
    return RetrievalCommand(keys=parts[1:])


def deserialize_value_response(msg: str):
    lines = msg.split("\r\n")
    i = 0
    while i < len(lines):
        if lines[i].startswith("VALUE"):
            _, key, flags, bytes_ = lines[i].split()
            value = lines[i + 1]
            yield ValueResponse(
                key=key,
                flags=int(flags),
                bytes=int(bytes_),
                value=value,
            )
            i += 2
        elif lines[i] == "END":
            break
        else:
            i += 1


