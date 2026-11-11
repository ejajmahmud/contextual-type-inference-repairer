"""CLI for contextual-type-inference-repairer."""
import sys
import argparse
from .repairer import TypeRepairer

def main():
    parser = argparse.ArgumentParser(description="Contextual Type Inference Repairer CLI")
    parser.add_argument("--demo", action="store_true", help="Infer types on untyped function")
    args = parser.parse_args()

    if args.demo:
        repairer = TypeRepairer()
        fn = """
def format_header(title, count):
    msg = title.lower().strip()
    tot = count + 10
    return msg
        """
        res = repairer.infer_and_repair(fn)
        print(f"Function: {res.func_name}")
        print(f"Inferred Args: {res.repaired_args}")
        print(f"Inferred Return: {res.repaired_return}")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
