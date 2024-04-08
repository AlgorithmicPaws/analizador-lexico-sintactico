import os
import re
import automata

def read_file(file_name):
    """
    Read the contents of a Python file and return a list of lines.

    Args:
        filename (str): The name of the Python file to read.

    Returns:
        list: A list containing the lines of the file.

    Raises:
        ValueError: If the provided filename does not end with '.py'.
        FileNotFoundError: If the file with the provided filename does not exist.
    """
    try:
        if not file_name.endswith('.py'):
            raise ValueError("Error: Only .py files are supported.")
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_dir, 'examples', file_name), 'r') as file:
            return file.readlines()   
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return []
    
def format_token(token):
    """
    Format a token into a string representation.

    Args:
        token (tuple): A tuple representing the token. It should have the format (token_type, lexeme, row, column)
                       or (token_type, row, column) depending on the presence of lexeme.

    Returns:
        str: A string representation of the token in the format "<token_type,lexeme,row,column>" or "<token_type,row,column>".

    Raises:
        ValueError: If the token format is invalid.
    """
    if len(token) == 4:
        token_type = token[0]
        lexeme, row, column = token[1:]
        return f"<{token_type},{lexeme},{row},{column}>\n"
    elif len(token) == 3:
        token_type = token[0]
        row, column = token[1:]
        return f"<{token_type},{row},{column}>\n"
    elif len(token) == 2:
        row = token[0]
        column = token[1]
        return f">>> lexical error,{row},{column}>\n"
    else:
        raise ValueError("Invalid token format")

def save_tokens_to_file(tokens, file_name):
    """
    Save a list of tokens to a file.

    Args:
        tokens (list): A list of tokens to be saved.
        file_name (str): The name of the file to save the tokens to.

    Raises:
        FileNotFoundError: If the specified file cannot be found.
        PermissionError: If permission is denied to write to the specified file.
        ValueError: If there is an issue with the format of any token.
    """
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_name = os.path.splitext(file_name)[0]
        output_file_name = base_name + ".txt"
        with open(os.path.join(current_dir, 'results', output_file_name), 'w') as file:
            for token in tokens:
                formatted_token = format_token(token)
                file.write(formatted_token)
        print("File created successfully.")
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
    except PermissionError:
        print(f"Error: Permission denied to write to '{file_name}'.")
    except ValueError as e:
        print(f"Error: {e}")

def create_regex_from_list(characters):
    regex = '|'.join(re.escape(character) for character in characters)
    return regex

def main():
    """
    Main function to execute the program.
    """
    try:
        esp_characters_list = ['\\','?','$','`',"'",'"','#','/','%','@','<','>','&','|','^','~',':','=','!','(',')','[',']','{','}',';',':','.','-','+','*',',']
        unique_characters_list = ['\\','(',')','[',']','{','}',';','~',',']
        expetion_characters_list = ['?','$','`']
        initial_compouse_character_list = ['%','@','&','|','^',':','=','!','+']
        regex_esp_characters =  create_regex_from_list(esp_characters_list)
        alphabet = re.compile(r'[\w\s]|[' + regex_esp_characters + ']')
        unique_character = re.compile(r'[' + create_regex_from_list(unique_characters_list) + ']')
        initial_compouse_character = re.compile(r'[' + create_regex_from_list(initial_compouse_character_list) + ']')
        
        transitions = [
            #Numeros 
            ('q0', r'[1-9]', 'q1'),
            ('q1', r'\d', 'q1'),
            ('q1', r'[eE]', 'q10'),
            ('q1', r'_', 'q3'),
            ('q1', r'\.', 'q2'),
            ('q1', r'[jJ]', 'q16'),
            ('q1', r'[^0-9eEjJ._]', 'q5'),# Integer final state
            ('q2', r'\d', 'q14'),
            ('q2', r'[eE]', 'q50'),
            ('q2', r'[jJ]', 'q16'),
            ('q2', r'[^0-9eEjJ_]', 'q6'), # Float int. final state
            ('q3', r'\d', 'q4'),
            ('q4', r'\d', 'q4'),
            ('q4', r'_', 'q3'),
            ('q4', r'[eE]', 'q10'),
            ('q4', r'\.', 'q7'),
            ('q4', r'[jJ]', 'q16'),
            ('q4', r'[^0-9eEjJ._]', 'q5'), # Integer_ final state
            ('q7', r'\d', 'q8'),
            ('q7', r'[eE]', 'q10'),
            ('q7', r'[jJ]', 'q16'),
            ('q7', r'[^0-9eEjJ_]', 'q6'), # Float _int. final state
            ('q8', r'\d', 'q8'),
            ('q8', r'_', 'q9'),
            ('q8', r'[eE]', 'q50'),
            ('q8', r'[jJ]', 'q16'),
            ('q8', r'[^0-9eEjJ_]', 'q6'), # Float (._dec) o (_._dec) final state
            ('q9', r'\d', 'q8'),
            ('q10', r'[\d]', 'q11'),
            ('q10', r'-', 'q13'),
            ('q11', r'\d', 'q11'),
            ('q11', r'_', 'q15'),
            ('q11', r'[jJ]', 'q16'),
            ('q11', r'[^0-9jJ_]', 'q12'), # Int cientific final state 
            ('q13', r'\d', 'q11'),
            ('q14', r'_', 'q9'),
            ('q14', r'\d', 'q14'),
            ('q14', r'[eE]', 'q50'),
            ('q14', r'[jJ]', 'q16'),
            ('q14', r'[^0-9eEjJ_]', 'q6'), # Float final state
            ('q15', r'\d', 'q11'),
            ('q16', r'[^0-9_]', 'q17'), # Imaginary final state
            ('q50', r'[\d]', 'q51'),
            ('q50', r'-', 'q53'),
            ('q51', r'\d', 'q51'),
            ('q51', r'_', 'q55'),
            ('q51', r'[jJ]', 'q16'),
            ('q51', r'[^0-9jJ_]', 'q52'), # Float cientific final state 
            ('q53', r'\d', 'q51'),
            ('q55', r'\d', 'q51'),
            # hexa, oct, bin
            ('q0',r'0', 'q56'),
            ('q56',r'[0-9]', 'q1'),
            ('q56',r'[oO]', 'q57'),
            ('q56',r'[xX]', 'q58'),
            ('q56',r'[bB]', 'q59'),
            ('q56',r'[^0-9bBxXoO]', 'q12'),
            ('q57',r'[0-7]', 'q57'),
            ('q57',r'[^0-7]', 'q5'),# Integer oct final state
            ('q58',r'[0-9a-fA-F]', 'q58'),
            ('q58',r'[^0-9a-fA-F]', 'q5'),# Integer hexa final state
            ('q59',r'[0-1]', 'q59'),
            ('q59',r'[^0-1]', 'q5'),# Integer bin final state
            #keywords/id
            ('q0', r'[_a-zA-Z]', 'q18'),
            ('q18', r'[\w]', 'q18'),
            ('q18', r'[^\w]', 'q19'), #Id/keyword final state
            #strings
            ('q0', r'\'', 'q20'),
            ('q0', r'\"', 'q23'),
            ('q20', r"[^'\n]", 'q20'),
            ('q20', r"\'", 'q21'),
            ('q21', alphabet, 'q22'),# strings '' final state
            ('q23', r'[^"\n]', 'q23'),
            ('q23', r'\"', 'q24'),
            ('q24', alphabet, 'q22'),# strings "" final state
            #Comments
            ('q0', r'\#', 'q25'),
            ('q25',r'[^\n]', 'q25'),
            ('q25',r'\n', 'q26'), # Ignore comments final state
            #Compouse characters
            ('q0',initial_compouse_character, 'q27'),
            ('q27',r'\=', 'q28'),
            ('q27',r'[^=]','q29'), # Initial caracter final state
            ('q28',alphabet,'q29'), # Initial caracter = final state
            #Duplicate chatacters
            ('q0',r'\*', 'q30'),
            ('q30',r'\*', 'q31'),
            ('q30',r'\=', 'q33'),
            ('q30',alphabet,'q32'), # * character final state 
            ('q31',r'\=', 'q33'),
            ('q31',alphabet, 'q32'), # ** character final state 
            ('q33',alphabet, 'q32'), # *= or ** = character final state 
            ('q0',r'\>', 'q34'),
            ('q34',r'\>', 'q35'),
            ('q34',r'\=', 'q36'),
            ('q34',r'[^=]','q32'), # > character final state 
            ('q35',r'\=', 'q36'),
            ('q35',alphabet, 'q32'), # >> character final state 
            ('q36',alphabet, 'q32'), # >= or >>= character final state 
            ('q0',r'\<', 'q37'),
            ('q37',r'\<', 'q38'),
            ('q37',r'\=', 'q39'),
            ('q37',r'[^=]','q32'), # < character final state 
            ('q38',r'\=', 'q39'),
            ('q38',alphabet, 'q32'), # << character final state 
            ('q39',alphabet, 'q32'), # <= or <<= character final state 
            ('q0',r'\/', 'q40'),
            ('q40',r'\/', 'q41'),
            ('q40',r'\=', 'q42'),
            ('q40',r'[^=]','q32'), # / character final state 
            ('q41',r'\=', 'q42'),
            ('q41',alphabet, 'q32'), # // character final state 
            ('q42',alphabet, 'q32'), # /= or //= character final state 
            #unique caracter operator
            ('q0',unique_character, 'q43'),
            ('q43',alphabet,'q32'), # unique character final state 
            # - exception 
            ('q0',r'\-', 'q44'),
            ('q44',r'\>', 'q46'),
            ('q44',r'\=', 'q46'),
            ('q44',r'[^=]','q32'), # - character final state
            ('q46',alphabet, 'q32'), # -> or -= character final state 
            # .
            ('q0',r'\.', 'q47'),
            ('q47',r'\d', 'q2'),
            ('q47',r'[^0-9]', 'q32'), # . character final state
            # spaces and new line
            ('q0',r' ', 'q48'),
            ('q0',r'\t', 'q48'),
            ('q0',r'\n', 'q48'),
            ('q48',alphabet, 'q49'),
            
        ]   
        states = {'q0','q1','q2','q3','q4','q5','q6', 'q7','q8','q9','q10',
                'q11','q12','q13', 'q14','q15', 'q16','q17','q18','q19','q20',
                'q21','q22','q23','q24','q25','q26','q27','q28','q29','q30',
                'q31','q32','q33','q34','q35','q36','q37','q38','q39','q40',
                'q41','q42','q43','q44','q45','q46','q47','q48','q49','q50',
                'q51','q52','q53','q54','q55','q56','q57','q58','q59','q60'}
        initial_state = 'q0'
        accepting_states = {'q5','q6','q12','q17','q19','q22','q26', 'q29', 'q32', 'q49', 'q52'}
        afd = automata.Automaton(states, alphabet, initial_state, accepting_states, transitions)

        filename = input("Enter the filename: ")
        file_lines = read_file(filename)
        file_lines[-1] = ''.join([file_lines[-1], ' '])
        if file_lines is not None:  
            for line in file_lines:
                try:
                    result = afd.rerun(list(line))
                    if result == False:
                        break
                except Exception as e:  
                    #print(f"Lexical error encountered while processing line: {line[:-1]}")
                    print(f"Error: {e}")
                    break  
        else:
            print("Unable to read the file.")

        if afd.token_list:  
            save_tokens_to_file(afd.token_list, filename)
    
    except FileNotFoundError as e:
        print(e)

if __name__ == "__main__":
    main()
