# argparse is a built-in Python library
# it lets us accept arguments from the terminal
import argparse
from log_parser import parse_log, chunk_logs
from llm_client import analyze_chunk
from report_generator import generate_report

def main():
    # Step 1: Define what arguments our tool accepts
    parser = argparse.ArgumentParser(
        description="AI Log Analyzer — automatically triages failures using Gemini"
    )

    # --log argument: which log file to analyze
    parser.add_argument(
        "--log",
        type=str,
        default="sample.log",
        help="Path to the log file you want to analyze"
    )

    # --output argument: where to save the report
    parser.add_argument(
        "--output",
        type=str,
        default="report",
        help="Name of the output report (without extension)"
    )

    # --chunk-size argument: how many lines per chunk
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=5,
        help="Number of log lines to send to Gemini at once"
    )

    # Step 2: Read what the user actually typed
    args = parser.parse_args()

    # Step 3: Run the pipeline using those arguments
    print("=" * 40)
    print("AI LOG ANALYZER")
    print("=" * 40)
    print(f"Log file   : {args.log}")
    print(f"Output     : {args.output}")
    print(f"Chunk size : {args.chunk_size}")
    print("=" * 40)

    print("\nStep 1: Reading log file...")
    lines = parse_log(args.log)
    chunks = chunk_logs(lines, chunk_size=args.chunk_size)
    print(f"         Found {len(lines)} lines → {len(chunks)} chunks")

    print("\nStep 2: Analyzing with Gemini...")
    results = []
    for i, chunk in enumerate(chunks):
        print(f"         Chunk {i+1} of {len(chunks)}...")
        result = analyze_chunk(chunk)
        results.append(result)

    print("\nStep 3: Generating reports...")
    generate_report(results, args.output)

if __name__ == "__main__":
    main()