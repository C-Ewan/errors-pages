import json, argparse
from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader('templates'))

def generate_http_error_page(error_data, template_name, output_file):
    template = env.get_template(template_name)

    rendered_html = template.render(
        code=error_data.get('code'),
        code_phrase=error_data.get('code_phrase'),
        description=error_data.get('description'),
        details=error_data.get('details'),
        details_title=error_data.get('details_title'),
        language=error_data.get('language', 'en'),
        title=error_data.get('title', f'{error_data.get("code")} - {error_data.get("code_phrase")}'),
        icon=error_data.get('icon'),
        icon_type=error_data.get('icon_type', 'png'),
    )

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(rendered_html)

def validate_error_data(error_data):
    required_fields = ['code', 'code_phrase']
    missing = [field for field in required_fields if field not in error_data or not error_data[field]]
    if missing:
        raise ValueError(f"Required fields missing or empty: {', '.join(missing)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate HTML error page from JSON data and Jinja2 template")
    parser.add_argument('--json-file', required=True, help='Path to the JSON file with error data')
    parser.add_argument('--output-file', required=True, help='Path to the output HTML file')
    parser.add_argument('--template-name', default='http_error.html', help='Name of the template in templates/ (default: http_error.html)')

    args = parser.parse_args()

    try:
        with open(args.json_file, 'r', encoding='utf-8') as f:
            error_data = json.load(f)

        validate_error_data(error_data)
        generate_http_error_page(error_data, args.template_name, args.output_file)
        print(f"Page generated successfully: {args.output_file}")
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}")
    except ValueError as e:
        print(f"Validation error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
