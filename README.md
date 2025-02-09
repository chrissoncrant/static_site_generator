# Static Site Generator Project

## Resources

-   Hugo, static site framework: https://gohugo.io/
-   https://www.markdownguide.org/cheat-sheet/
-   https://docs.python.org/3/library/unittest.html

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
    is allowed for. Example: "This is an _italic and **bold** word_." is not
    will only parse at the italic level.

## Observations:

-   simple tests are best. I am noticing that once I test the format of an
    attribute, and how its string renders, then there is no point in adding
    attributes in further test cases

### Brainstorming split_nodes_delimiter function.

#### Special Cases

-   when a delimiter is used by itself, without a closing delimiter. Example:
    "This \*line only has one asterisk"
    -   Do I need to worry about this? When someone is converting Markdown, it
        is implied that these symbols have special use cases. Also, these can be
        escaped using \
-   A TextNode is a single string. This can be multiple sentences long. These
    are broken up by new lines, \n.
-   Is this function to be applied to all TextNodes? If so, then there should be
    a check to determine if the delimiter is present.

I need a recursive function that will deal with splits...

-   The Stopping Case: a string with no more opening delimiters.
    -   once found it will:

### Tests To Create:

-   veriy text nodes without delimiters get added right away
-   verify splitting occurs correctly for:
    -   bold
    -   italicized
    -   code
    -   multiple instances of a delimiter in one fragment
-   verify that what is returned is a list
-   verify that what is each item in returned list is a TextNode
