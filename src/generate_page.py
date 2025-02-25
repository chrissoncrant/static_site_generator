def generate_page(from_path, template_path, des_path):
    print(f"Generating page from '{from_path}' to '{des_path}' using '{template_path}'")

generate_page("../content/index.md", "../template.html", "../static")