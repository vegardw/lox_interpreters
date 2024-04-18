import re
import os
from typing import List

imports = [
    "from abc import ABC, abstractmethod",
    "from typing import Any",
    "from .token import Token"
]

expr_definitions = [
    "Binary   : Expr left, Token operator, Expr right",
    "Grouping : Expr expression",
    "Literal  : Any value",
    "Unary    : Token operator, Expr right"
]

def generate_file(class_definitions: List[str], base_name: str, save_path: str="lox"):
    forward_declarations = ["# Forward declarations, needed for declaring visitor interface before the actual classes"]
    class_definitions = []
    visitor_methods = []

    for definition in expr_definitions:
        class_name, fields = definition.split(":")
        class_name = class_name.strip()
        fields = [f.strip() for f in fields.split(",")]

        forward_declarations.append(f"class {class_name}{base_name}:\n  pass")

        class_definition = [f"class {class_name}{base_name}({base_name}):"]
        constructor_params = []
        constructor_assignments = []

        for field in fields:
            field_type, field_name = re.split(r"\s+", field, maxsplit=1)
            constructor_params.append(f"{field_name}: {field_type}")
            constructor_assignments.append(f"    self.{field_name} = {field_name}\n")

        constructor_definition = [
            "  def __init__(self, " + ", ".join(constructor_params) + ") -> None:",
            "".join(constructor_assignments)
        ]

        accept_method = [
            f"  def accept(self, visitor: {base_name}Visitor):",
            f"    return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)"
        ]

        visitor_method = [
            f"  @abstractmethod",
            f"  def visit_{class_name.lower()}_{base_name.lower()}(self, {base_name.lower()}: {class_name}{base_name}):",
            "    pass"
        ]

        class_definitions.append("\n".join(class_definition + constructor_definition + accept_method))
        visitor_methods.append("\n".join(visitor_method))

    visitor_class = [
        f"# {base_name}Visitor interface", 
        f"class {base_name}Visitor(ABC):",
        "\n".join(visitor_methods)
    ]

    base_class = [
        f"# {base_name} base class and sub classes",
        f"class {base_name}(ABC):",
        "  @abstractmethod",
        f"  def accept(self, visitor: {base_name}Visitor):",
        "    pass"
    ]

    file_contents = [
        "\n".join(imports),
        "\n\n\n",
        "\n".join(forward_declarations),
        "\n\n\n",
        "\n".join(visitor_class),
        "\n\n\n",
        "\n".join(base_class),
        "\n\n",
        "\n\n".join(class_definitions),
        "\n"
    ]

    file_name = os.path.join(save_path, f"{base_name.lower()}.py")
    with open(file_name, "w") as file:
        file.write("".join(file_contents))

    return file_name

expr_file = generate_file(expr_definitions, "Expr")
print(f"File '{expr_file}' has been generated.")