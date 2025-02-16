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
        considered part of the same block.
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
        elements (bold, links/anchors, etc) we will convert in this manner: Raw
        MD -> TextNode -> HTMLNode
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
-   ability to parse multiple levels of inline nesting; currently only one level
    is allowed for. Example: "This is an *italic sentence with a **bold** word in it*."
    will only parse at the italic level.

## Observations:
-   simple tests are best. I am noticing that once I test the format of an
    attribute, and how its string renders, then there is no point in adding
    attributes in further test cases


## Thoughts
paragraph seems to be the last item, as in if the pattern does not match anything, then return "paragraph"

for headings:
the first string sequence must be # and no longer than 6 characters long.
- can split by space
The Rules for valid Headings:
A valid heading can have # characters in its text content, as long as they're not at the beginning of a new line. Whitespace doesn't count as valid characters between newlines and the #. So "# Heading 1\n  #Not a heading" is invalid and should return paragraph
Valid headings can span multiple lines.
If I split by the first space, then all characters in the first sequence must be "#" because invalid input types:
Edge Cases:"#"
"# "
"# "
"####### Heading"
"# Heading\nMore text"
"# Heading\n# Another heading"
"# Heading\nThis # is just text"
"# Heading\n # This starts with a space"
"# Heading\n\n# Another"
"# Heading\n\n# Another"
"#Heading\n#########some text"

Unordered Lists:
first character is either "*" or "-"
All lines following this must start with "-" or "*".
- can split be space

Ordered Lists:
first ch is a "1."
All lines following this must start with a number incremented by 1 followed by a .
- can split by space
How to check for increments?
First split by space and check first character is "1."
Split by new line. Loop through and verify that first character of each item in list is larger that previous ch by one. Need to convert to number to verify.

Code blocks:
start and end with 3 backticks. So can slice the string by first 3 and last 3 characters to determine if its valid code
string[0:3] == "```"
string[-3:] == "```"

Quote blocks:
first character must be ">". 
All lines following this must start with ">".




