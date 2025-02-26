# Static Site Generator Project

## Resources
-   Hugo, static site framework: https://gohugo.io/
-   https://www.markdownguide.org/cheat-sheet/
-   Unittest: https://docs.python.org/3/library/unittest.html
-   Regex: https://docs.python.org/3/library/re.html

## How This Works
-   Converting Markdown to HTML
-   Our static site generator will take a directory of Markdown files (one for
    each web page), and build a directory of HTML files.

### Flow
-   Markdown files are in the /content directory. A template.html file is in the
    root of the project
-   The static site generator (the Python code in src/) reads the Markdown files 
    and the template file
-   The generator converts the Markdown files to a final HTML file for each page
    and writes them to the /public directory
-   We start the built-in Python HTTP server (a separate program, unrelated to
    the generator) to serve the contents of the /public directory on
    http://localhost:8888 (local machine)
-   We open a browser and navigate to http://localhost:8888 to view the rendered
    site
-   It will assume valid Markdown Parsing:
    -   Blocks are separated by two lines; lines separated by one line will be
        considered part of the same block. This will lead to problems if, for example, a paragraph is separated by a heading only by a single line.
    -   excessive spaces in the middle of single lines will not be altered.
-   Supported Inline Markdown Parsing:
    -   italics
    -   bold
    -   code
    -   images
    -   links
-   Supported Block Markdown Parsing:
    -   paragraph
    -   heading
    -   code
    -   quote
    -   list (ordered and unordered)


### How the Generator Works
-   Delete everything in /public directory
-   Copy static site assets (HTML template, images, CSS, etc.) to the /public
    directory.
-   For Markdown File:
    -   Open the file and read its contents
    -   Split the MD into "blocks" (paragraphs, headings, lists, etc.)
    -   Convert each block into a tree of HTMLNode objects. So for inline
        elements (bold, links/anchors, etc) we will convert in this manner: Raw MD -> TextNode -> HTMLNode
    -   Join all the HTMLNode blocks under one large parent HTMLNode for the
        pages
    -   Use recursive `to_html()` method to convert HTMLNode and its nested
        nodes to a giant HTML string and inject it in the HTML template
    -   Write the full HTML string to a file for that page in the /public
        directory

## Project Details
-   shell script created (main.sh) in order to run the code more easily from
    command line.
-   shell script created (test.sh) to run tests more easily from command line

## Future Improvements:
-   ability to parse multiple levels of inline nesting; currently only one level is allowed for. Example: "This is an *italic sentence with a **bold** word in it*." will only parse at the italic level.
- Add functionality for other inline textnodes, such as inline quotes.
-   Ability to handle cases where different block items (a heading and paragraph, for example) are only separated by a single newline character
-   Ability to set Code Block type (py, etc), currently if those characters are included, they will be included in the text in the rendered html.

## Observations:
-   simple tests are best. I am noticing that once I test the format of an attribute, and how its string renders, then there is no point in adding attributes in further test cases


###################################################
###################################################

## Markdown to HTMLNode:
Based on the block type we can determine what kind of parent block is needed.

### HTML Node review:
- Parents: requires a tag, requires children as a list (these can be parents and leafs); these do not have values
- Leafs: require a value unless image; has tags, but not required. Example of Leaf without a tag would be a paragraph.

### TextNodes
text, bold, italics, code, links, images

### My Questions
Need some function to extract the actual text from the block level markdown (extracting the heading text from the md string which starts with "#')

Need to create the children list to pass into the overall ParentNode, which would then run the .to_html() on that to generate the html.

### I notice:
block_markdown imports from nowhere (yet)
inline_markdown imports from textnode
textnode only uses leafnodes
htmlnode doesn't import from anywhere

### Block Level Elements
Entire Document gets nested in <html> Parent HTMLNode

Paragraphs: <p> Parent HTMLNode --> LeafNodes --> TextNodes
- Paragraphs are separated by double \n
- If a plain string is only separated by a single \n, it still goes into a single paragraph element
    - Need a function to replace \n with &NewLine; and then add `style="white-space: pre-line"` property.

Headings: <h{1-6}> Parent HTMLNode --> LeafNodes --> TextNodes

Block Code: <code> Parent HTMLNode --> <pre> Parent HTMLNode --> LeafNodes --> TextNodes

Quotes: <blockquote> Parent HTMLNode --> <p> Parent HTMLNode --> LeafNode --> TextNodes 

Ordered Lists: <ol> Parent HTMLNode --> <li> Parent HTMLNode --> LeafNodes --> TextNodes

Unordered Lists: <ul> Parent HTMLNode --> <li> Parent HTMLNode --> LeafNodes --> TextNodes

______________
block_markdown.md
markdown_to_blocks()
block_to_block_type() 
extract text from the block symbol (if needed; headings, lists, code, quotes)

inlinemarkdown.md
text_to_textnodes() which will convert input string to a TextNode List, run TextNode list through the split_nodes_delimiter for bold, italic, code, run the new list through imaging and link parsing and return a new list of TextNodes.

textnode.md
text_node_to_html_node() must run each of the nodes in the returned list through this function and return a new list of LeafNodes. This list will be the child list for the relevant ParentNode.

htmlnode.md
ParentNode(tag, children, props)
    - tag and children are required.
Create ParentNode based on the block type, which determines the tag, and using the returned list as the children argument

Append ParentNode to the child_list

return ParentNode("html", child_list)

### Page Generation
Print message: f"Generating page from {from_path} to {dest_path} using {template_path}"

Open and read markdown file from from_path and store the contents in a variable

Open and read html file in temp_path and store the contents

Convert the markdown to html (md_to_html) and store the html string.

Extract the title and store it

Replace {{title}} in the template with the title

replace the {{content}} with the converted string

Write the new file html page to a file at dest_path and create any new necessary directories if they don't exist in the dest_path

Converting the contents of the markdown file in Content directory into html and using the template.html to create a new file that will be in the Public directory.

#########
Content may have several files within it and a nested directory.

If the directory doesn't exist in the destination folder (Public), they need to be created first.

But, we don't want to create the 'content' folder.

### Main Function
delete files from public dir
copy all files from static to public
generate the page from content/index.md using template.html and write it to public/index.html

If all files are deleted from Public, then copied from Static to Public first, then all the images must be added to Static first, and all nested html files need to have the appropriate link to the styles.

This would need to be changed in the Template.

Another thing... creating the 

Next phase would be to create a recursive call on generate_page.







