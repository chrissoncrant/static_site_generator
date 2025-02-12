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