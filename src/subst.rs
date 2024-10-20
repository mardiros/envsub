use std::env;

#[derive(Debug)]
enum Token {
    Str(String),                // Represents plain strings
    Var(String),                // Represents variables in the form ${NAME}
    VarDefault(String, String), // Represents variables in the form ${NAME}
}

impl Token {
    fn to_string(&self) -> String {
        match self {
            Token::Str(s) => s.clone(), // Return the string as is
            Token::Var(var) => {
                // Remove the ${} from the variable name
                env::var(var).unwrap_or_else(|_| format!("${{{}}}", var.clone()))
            }
            Token::VarDefault(var, default) => {
                // Remove the ${} from the variable name
                env::var(var).unwrap_or(default.clone())
            }
        }
    }
}

fn tokenize(input: &str) -> Vec<Token> {
    let mut tokens = Vec::new();
    let mut last_pos = 0;

    while let Some(start) = input[last_pos..].find("${") {
        let start = last_pos + start;

        if last_pos < start {
            tokens.push(Token::Str(input[last_pos..start].to_string()));
        }

        if let Some(end) = input[start..].find('}') {
            let end = start + end + 1;
            let token = input[start + 2..end - 1].to_string();
            if let Some(default_start) = token.find('-') {
                tokens.push(Token::VarDefault(
                    token[0..default_start].to_string(),
                    token[default_start + 1..].to_string(),
                ));
            } else {
                tokens.push(Token::Var(token.to_string()));
            }
            last_pos = end; // Move past the placeholder
        } else {
            break; // No closing brace found, exit the loop
        }
    }

    if last_pos < input.len() {
        tokens.push(Token::Str(input[last_pos..].to_string()));
    }

    tokens
}

pub fn substr(input: &str) -> String {
    let tokens = tokenize(input);
    let result: String = tokens.iter().map(|token| token.to_string()).collect();
    return result;
}
