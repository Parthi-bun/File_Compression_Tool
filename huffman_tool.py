from __future__ import annotations

import heapq
import json
import os
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Node:

    char: Optional[str]
    freq: int
    left: Optional["Node"] = None
    right: Optional["Node"] = None

    def __lt__(self, other: "Node") -> bool:
        return self.freq < other.freq


def build_frequency_table(text: str) -> Dict[str, int]:
    frequency: Dict[str, int] = {}
    for char in text:
        frequency[char] = frequency.get(char, 0) + 1
    return frequency


def build_huffman_tree(frequency: Dict[str, int]) -> Optional[Node]:
    if not frequency:
        return None

    heap = [Node(char=char, freq=freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    if len(heap) == 1:
        only_node = heapq.heappop(heap)
        return Node(char=None, freq=only_node.freq, left=only_node, right=None)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(char=None, freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)

    return heap[0]


def generate_huffman_codes(root: Optional[Node]) -> Dict[str, str]:
    codes: Dict[str, str] = {}

    if root is None:
        return codes

    def dfs(node: Optional[Node], current_code: str) -> None:
        if node is None:
            return

        if node.char is not None:
            codes[node.char] = current_code if current_code else "0"
            return

        dfs(node.left, current_code + "0")
        dfs(node.right, current_code + "1")

    dfs(root, "")
    return codes


def encode_text(text: str, codes: Dict[str, str]) -> str:
    return "".join(codes[char] for char in text)


def decode_text(encoded_bits: str, root: Optional[Node]) -> str:
    if root is None or not encoded_bits:
        return ""

    decoded_chars = []
    current = root

    for bit in encoded_bits:
        current = current.left if bit == "0" else current.right
        if current and current.char is not None:
            decoded_chars.append(current.char)
            current = root

    return "".join(decoded_chars)


def pad_encoded_bits(encoded_bits: str) -> str:
    extra_padding = (8 - len(encoded_bits) % 8) % 8
    padded_bits = encoded_bits + ("0" * extra_padding)
    padding_info = format(extra_padding, "08b")
    return padding_info + padded_bits


def remove_padding(padded_bits: str) -> str:
    if len(padded_bits) < 8:
        return ""

    extra_padding = int(padded_bits[:8], 2)
    encoded_bits = padded_bits[8:]

    if extra_padding > 0:
        encoded_bits = encoded_bits[:-extra_padding]

    return encoded_bits


def bits_to_bytes(bit_string: str) -> bytes:
    if not bit_string:
        return b""

    byte_array = bytearray()
    for i in range(0, len(bit_string), 8):
        byte_array.append(int(bit_string[i : i + 8], 2))
    return bytes(byte_array)


def bytes_to_bits(byte_data: bytes) -> str:
    return "".join(format(byte, "08b") for byte in byte_data)


def serialize_frequency_table(frequency: Dict[str, int]) -> bytes:
    serializable = {str(ord(char)): count for char, count in frequency.items()}
    return json.dumps(serializable, separators=(",", ":")).encode("utf-8")


def deserialize_frequency_table(data: bytes) -> Dict[str, int]:
    """Deserializes frequency table from bytes."""
    if not data:
        return {}

    loaded = json.loads(data.decode("utf-8"))
    return {chr(int(code_point)): count for code_point, count in loaded.items()}


def compress_file(input_path: str = "sample.txt", output_path: str = "compressed.bin") -> None:
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.")
        return

    with open(input_path, "r", encoding="utf-8") as file:
        text = file.read()

    if text == "":
        with open(output_path, "wb") as file:
            file.write((0).to_bytes(4, byteorder="big"))
        print("Input file is empty. Created an empty compressed file.")
        print_file_stats(input_path, output_path)
        return

    frequency = build_frequency_table(text)
    huffman_root = build_huffman_tree(frequency)
    codes = generate_huffman_codes(huffman_root)

    encoded_bits = encode_text(text, codes)
    padded_bits = pad_encoded_bits(encoded_bits)
    compressed_bytes = bits_to_bytes(padded_bits)

    freq_bytes = serialize_frequency_table(frequency)
    header_length = len(freq_bytes)

    with open(output_path, "wb") as file:
        file.write(header_length.to_bytes(4, byteorder="big"))
        file.write(freq_bytes)
        file.write(compressed_bytes)

    print(f"Compression successful: '{input_path}' -> '{output_path}'")
    print_file_stats(input_path, output_path)


def decompress_file(
    input_path: str = "compressed.bin", output_path: str = "decompressed.txt"
) -> None:
    if not os.path.exists(input_path):
        print(f"Error: Compressed file '{input_path}' not found.")
        return

    with open(input_path, "rb") as file:
        raw = file.read()

    if len(raw) < 4:
        print("Error: Invalid compressed file format.")
        return

    header_length = int.from_bytes(raw[:4], byteorder="big")
    if len(raw) < 4 + header_length:
        print("Error: Corrupted compressed file (invalid header length).")
        return

    freq_bytes = raw[4 : 4 + header_length]
    compressed_payload = raw[4 + header_length :]

    frequency = deserialize_frequency_table(freq_bytes)

    if header_length == 0 and not compressed_payload:
        with open(output_path, "w", encoding="utf-8") as file:
            file.write("")
        print(f"Decompression successful: '{input_path}' -> '{output_path}' (empty file)")
        return

    huffman_root = build_huffman_tree(frequency)

    bit_string = bytes_to_bits(compressed_payload)
    encoded_bits = remove_padding(bit_string)
    decoded_text = decode_text(encoded_bits, huffman_root)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(decoded_text)

    print(f"Decompression successful: '{input_path}' -> '{output_path}'")


def print_file_stats(original_path: str, compressed_path: str) -> None:
    if not os.path.exists(original_path) or not os.path.exists(compressed_path):
        return

    original_size = os.path.getsize(original_path)
    compressed_size = os.path.getsize(compressed_path)

    print(f"Original file size   : {original_size} bytes")
    print(f"Compressed file size : {compressed_size} bytes")

    if original_size == 0:
        print("Compression ratio    : N/A (original file is empty)")
    else:
        ratio = compressed_size / original_size
        print(f"Compression ratio    : {ratio:.4f} ({ratio * 100:.2f}%)")


def print_menu() -> None:
    print("\n===== File Compression Tool (Huffman Coding) =====")
    print("1. Compress file")
    print("2. Decompress file")
    print("3. Exit")


def main() -> None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, "sample.txt")
    compressed_file = os.path.join(base_dir, "compressed.bin")
    decompressed_file = os.path.join(base_dir, "decompressed.txt")

    while True:
        print_menu()
        try:
            choice = input("Enter your choice (1-3): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting program.")
            break

        if choice == "1":
            try:
                print(f"Compressing: {input_file}")
                compress_file(input_file, compressed_file)
            except Exception as error:
                print(f"Compression failed: {error}")
        elif choice == "2":
            try:
                print(f"Decompressing: {compressed_file}")
                decompress_file(compressed_file, decompressed_file)
            except Exception as error:
                print(f"Decompression failed: {error}")
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
