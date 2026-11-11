"""Core Contextual Type Inference Repairer implementation."""
import ast
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class RepairedSignature:
    func_name: str
    repaired_args: Dict[str, str]
    repaired_return: str

class TypeRepairer:
    """Infers and injects accurate Python type annotations based on internal function body AST usage."""
    
    def infer_and_repair(self, func_code: str) -> RepairedSignature:
        tree = ast.parse(func_code)
        func_node = None
        for n in ast.walk(tree):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_node = n
                break
        
        if not func_node:
            raise ValueError("No function found in provided code")

        arg_types = {arg.arg: "Any" for arg in func_node.args.args}
        return_type = "None"

        # Walk body to infer types
        for node in ast.walk(func_node):
            # Check string methods
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                caller = node.func.value
                if isinstance(caller, ast.Name) and caller.id in arg_types:
                    if node.func.attr in {"split", "lower", "strip", "replace", "startswith"}:
                        arg_types[caller.id] = "str"
                    elif node.func.attr in {"append", "extend", "pop"}:
                        arg_types[caller.id] = "List[Any]"

            # Check math operators
            if isinstance(node, ast.BinOp):
                if isinstance(node.left, ast.Name) and node.left.id in arg_types:
                    arg_types[node.left.id] = "int"
                if isinstance(node.right, ast.Name) and node.right.id in arg_types:
                    arg_types[node.right.id] = "int"

            # Check return statement
            if isinstance(node, ast.Return) and node.value:
                if isinstance(node.value, ast.Constant):
                    return_type = type(node.value.value).__name__
                elif isinstance(node.value, ast.List):
                    return_type = "List[Any]"
                elif isinstance(node.value, ast.Dict):
                    return_type = "Dict[str, Any]"
                else:
                    return_type = "Any"

        return RepairedSignature(
            func_name=func_node.name,
            repaired_args=arg_types,
            repaired_return=return_type
        )
