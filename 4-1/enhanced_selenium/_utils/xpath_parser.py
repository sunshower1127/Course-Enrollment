from __future__ import annotations

from pyparsing import (
    Combine,
    OneOrMore,
    QuotedString,
    Suppress,
    White,
    Word,
    ZeroOrMore,
    infix_notation,
    one_of,
    opAssoc,
    pyparsing_unicode,
)

# Define the grammar
word = Word(pyparsing_unicode.alphanums + "_-")
identifier = (
    Combine(OneOrMore(word + ZeroOrMore(White() + word)))
    | QuotedString('"')
    | QuotedString("'")
)
operator = one_of("! & |")
lparen = Suppress("(")
rparen = Suppress(")")

# Define the expression using infix_notation
expr = infix_notation(
    identifier,
    [("!", 1, opAssoc.RIGHT), (one_of("& |"), 2, opAssoc.LEFT)],
    lpar=lparen,
    rpar=rparen,
)


def get_prop_format(prop_name: str):
    prop_name = prop_name.replace("class_name", "class")
    if "text" in prop_name:
        prop_name = prop_name.replace("text", "text()")
    else:
        prop_name = "@" + prop_name

    idx = prop_name.find("_contains")
    if idx != -1:
        prop_name = prop_name[:idx]
        return "contains(" + prop_name + ", '{}')"

    return prop_name + "='{}'"


def preprocess_for_not(node: list):
    for i in range(len(node)):
        if isinstance(node[i], list):
            preprocess_for_not(node[i])
        elif i > 0 and node[i - 1] == "!":
            node[i] = [node[i]]


# Parse the expression
def parse_expression(expression: str, prop_name: str):
    parsed_expression = expr.parse_string(expression, parse_all=True).as_list()[0]

    # A -> (A) 로 바꾸기 -> 마지막에 괄호 없애는 과정 통일
    if isinstance(parsed_expression, str):
        parsed_expression = [parsed_expression]

    preprocess_for_not(parsed_expression)

    prop_format = get_prop_format(prop_name)
    logical_expression = convert_to_logical_expression(parsed_expression, prop_format)
    if logical_expression[0] == "(":
        logical_expression = logical_expression[1:-1]
    return logical_expression


def convert_to_logical_expression(element: str | list, prop_format: str) -> str:
    if isinstance(element, list):
        result = ""
        if element[0] != "!":
            result += "("

        result += "".join(
            convert_to_logical_expression(sub_element, prop_format)
            for sub_element in element
        )

        if element[0] != "!":
            result += ")"

        return result

    if element == "|":
        return " or "
    if element == "&":
        return " and "
    if element == "!":
        return "not"

    return prop_format.format(element)


def get_xpath(data: dict):
    data = data.copy()
    data.pop("self", None)
    data.pop("xpath", None)

    if "kwargs" in data:
        for key, value in data["kwargs"].items():
            data[key] = value
        del data["kwargs"]

    header = data.pop("axis", "descendant") + "::" + data.pop("tag", "*")
    body = []
    for key, value in data.items():
        if value is None:
            continue

        body.append(parse_expression(value, key))

    if body:
        return f"{header}[{ ' and '.join(body) }]"
    else:
        return header


"""

오케이.

A B C -> 는 "A B C" 로 입력되게 했구요.
양쪽 띄어쓰기들은 제거 되게 해놨으니깐 
굳이 인식되게 하려면 따움표 쓰면 됩니다.
이상.

"""
# Test code
if __name__ == "__main__":
    expression = "A & B  C "
    prop_format = "text"
    result = parse_expression(expression, prop_format)
    print(result)
