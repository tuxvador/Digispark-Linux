#!/usr/bin/env python3
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "exes"))
from duck2spark import generate_source


def test_generate_source_with_bytes():
    payload = b"\x00\x01\x02\x03"
    result = generate_source(payload, loop_count=1)
    assert "#include \"DigiKeyboard.h\"" in result
    assert "#define DUCK_LEN 4" in result
    assert "0x0" in result
    assert "0x1" in result
    assert "0x2" in result
    assert "0x3" in result
    assert "void setup()" in result
    assert "void loop()" in result
    assert "int i = 1;" in result
    print("PASS: test_generate_source_with_bytes")


def test_generate_source_loop_count():
    payload = b"\x9b\x29"
    result = generate_source(payload, loop_count=-1)
    assert "int i = -1;" in result
    print("PASS: test_generate_source_loop_count")


def test_generate_source_blink():
    payload = b"\x00\x00"
    result = generate_source(payload, blink=True)
    assert "bool blink=true;" in result
    result = generate_source(payload, blink=False)
    assert "bool blink=false;" in result
    print("PASS: test_generate_source_blink")


def test_generate_source_init_delay():
    payload = b"\x00\x00"
    result = generate_source(payload, init_delay=2000)
    assert "DigiKeyboard.delay(2000);" in result
    print("PASS: test_generate_source_init_delay")


def test_real_bin_file():
    bin_path = os.path.join(os.path.dirname(__file__), "..", "bin", "notepad.bin")
    with open(bin_path, "rb") as f:
        payload = f.read()
    assert len(payload) == 136
    result = generate_source(payload, loop_count=1)
    assert "#define DUCK_LEN 136" in result
    assert "void setup()" in result
    assert "void loop()" in result
    print("PASS: test_real_bin_file")


def test_cli_invocation():
    root = os.path.dirname(os.path.dirname(__file__))
    bin_path = os.path.join(root, "bin", "notepad.bin")
    out_path = os.path.join(root, "test_output.ino")
    try:
        ret = os.system(
            f"python3 {os.path.join(root, 'exes', 'duck2spark.py')} "
            f"-i {bin_path} -o {out_path} -l 1"
        )
        assert ret == 0
        with open(out_path) as f:
            content = f.read()
        assert "#include \"DigiKeyboard.h\"" in content
        assert "#define DUCK_LEN 136" in content
        print("PASS: test_cli_invocation")
    finally:
        if os.path.exists(out_path):
            os.unlink(out_path)


if __name__ == "__main__":
    test_generate_source_with_bytes()
    test_generate_source_loop_count()
    test_generate_source_blink()
    test_generate_source_init_delay()
    test_real_bin_file()
    test_cli_invocation()
    print("\nAll tests passed!")
