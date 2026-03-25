File Compression Tool (Huffman Coding)

This project implements a file compression and decompression utility using the Huffman Coding algorithm, a widely used lossless data compression technique. It demonstrates fundamental concepts from data structures and algorithms, including trees, priority queues, recursion, and binary encoding.

⸻

Overview

The tool reads a text file, compresses its contents into a binary format, and stores the necessary metadata to allow full reconstruction of the original file. The decompression process restores the exact original content without any loss.

⸻

Features
	•	Lossless file compression using Huffman Coding
	•	Accurate decompression with full data recovery
	•	Efficient encoding using binary representations
	•	Frequency table serialization for reconstruction
	•	Handles edge cases such as empty files and single-character inputs
	•	Displays compression statistics (size and ratio)

⸻

How It Works
	1.	Frequency Table Construction
Each character in the input file is counted to determine its frequency.
	2.	Huffman Tree Construction
A binary tree is built using a priority queue (min-heap), where nodes with lower frequencies are merged first.
	3.	Code Generation
Each character is assigned a unique binary code based on its position in the tree. Left edges represent 0, and right edges represent 1.
	4.	Encoding Process
The input text is converted into a binary string using the generated codes.
	5.	Padding and Byte Conversion
The binary string is padded to align with byte boundaries and then converted into bytes for storage.
	6.	File Storage Format
The compressed file contains:
	•	A header specifying the size of the frequency table
	•	The serialized frequency table (JSON format)
	•	The compressed binary data
	7.	Decoding Process
The frequency table is reconstructed, the Huffman tree is rebuilt, and the binary data is decoded back into the original text.

⸻

Project Structure
'''
File_Compression_Tool/
│
├── sample.txt       
├── compressed.bin      
├── decompressed.txt      
└── main.py     
'''

Usage

Run the Program

'''
python main.py
'''

Menu Options
	•	1 → Compress the input file (sample.txt)
	•	2 → Decompress the file (compressed.bin)
	•	3 → Exit the program

Requirements
	•	Python 3.8 or higher
	•	No external libraries required (uses standard library only)

⸻

Key Concepts Demonstrated
	•	Huffman Coding Algorithm
	•	Binary Trees
	•	Priority Queues (Heap)
	•	Recursion (DFS traversal)
	•	File Handling (binary and text)
	•	Data Serialization (JSON)

⸻

Limitations
	•	Designed for text files (UTF-8 encoding)
	•	Not optimized for very large files
	•	Compression effectiveness depends on character distribution

⸻

Future Improvements
	•	Support for arbitrary binary files
	•	GUI-based interface
	•	Improved compression efficiency
	•	Streaming support for large files

⸻
