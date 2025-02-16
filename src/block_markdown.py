def markdown_to_blocks(markdown):
    if type(markdown) != str:
        raise ValueError("argument must be a string")
    
    if markdown.strip() == "":
        raise ValueError("input string has no content")
    
    block_list = markdown.split("\n\n")
    
    block_list = map(lambda x: x.strip(), block_list)

    block_list = list(filter(lambda x: x != "", block_list))

    return block_list

def solution_markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    if type(block) != str:
        raise ValueError("argument must be a string")
    
    if block[0:3] == "```" and block[-3:] == "```":
        return "code"
    
    if block[0] == ">":
        split_by_newline = block.split("\n")
        for line in split_by_newline:
            if not line or line[0] != ">":
                return "paragraph"
            else:
                continue
        return "quote"

    split_by_space = block.split(" ", 1)

    if len(split_by_space) == 1:
        return "paragraph"
    
    ch_to_check = split_by_space[0]

    # Heading Check
    if ch_to_check[0] == "#":
        valid_headings = ["#", "##", "###", "####", "#####", "######"]
        if ch_to_check in valid_headings:
            return "heading"
        else:
            return "paragraph"
        
    # Ordered List Check
    if ch_to_check[0:2] == "1.":
        split_by_newline = block.split("\n")
        num_check = 0
        for line in split_by_newline:
            num_check += 1
            split_by_period = line.split(". ", 1)
            digit = split_by_period[0]
            if digit.isdigit():
                if num_check == int(digit):
                    continue
                else:
                    return "paragraph"
            else:
                return "paragraph"
        return "ordered_list"     

    # Unordered List Check
    if ch_to_check[0] == "-" or ch_to_check[0] == "*":
        valid_characters = ["- ", "* "]
        split_by_newline = block.split("\n")
        for line in split_by_newline:
            characters_to_check = line[0:2]
            if characters_to_check in valid_characters:
                continue
            else:
                return "paragraph"
        return "unordered_list" 

    return "paragraph"