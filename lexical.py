import re
import pandas as pd

def tokenize_text(input_text, token, token_type):
    matches = re.finditer(token, input_text)
    tokens = []
    for match in matches:
        token_value = match.group()
        token_start = match.start()
        token_end = match.end()
        tokens.append((token_type, token_value, (token_start, token_end)))
    return tokens

def tokenize_and_save_csv(input_file, output_file, patterns):
    with open(input_file, 'r', encoding='utf-8') as file:
        input_text = file.read()

    all_tokens = []
    errors = []
    r = 1
    # c = 1
    for pattern, token_type in patterns:
        matches = re.finditer(pattern, input_text)
        r=1
        for match in matches:
            token_value = match.group()
            lo = r
            if token_value.strip():  # Check if the token is not just whitespace
                all_tokens.append((token_type, token_value, lo))
            else:
                errors.append((f"Invalid token: '{token_value}'",lo))
        #     c += 1
            r += 1
        # c = 1

    tokens_df = pd.DataFrame(all_tokens, columns=['Token Type', 'Token Value', 'location from first'])
    errors_df = pd.DataFrame(errors, columns=['Error', 'Row', 'Column'])

    tokens_df.to_csv(output_file, index=False)
    if not errors_df.empty:
        errors_df.to_csv(output_file, mode='a', header=False, index=False, encoding='utf-8', line_terminator='\n\n')

# Example usage
input_file = 'input.txt'
output_file = 'tokens.csv'
tokens = [
    (r"[a-zA-Z_]\w*", "<identifier>"),
    (r"\d+", "<number>"),
    (r"int|void|if|while|return|read|write|print|continue|break|binary|decimal", "<reserved word>"),
    (r"\(|\)|\{|\}|\[|\]|,|;|\+|-|\*|/|==|!=|>=|<=|=|&&|\|\|", "<symbol>"),
    (r"\".*?\"", "<string>"),
    (r"(#|\/\/).*?(\n|$)", "<meta statement>")
]

tokenize_and_save_csv(input_file, output_file, tokens)
