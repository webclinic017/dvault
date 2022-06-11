from string import Template
import shutil

def from_template(
        template_path, template_vars):

    with open(template_path, "r") as f:
        contents = f.read()
        template = Template(contents)
    contents = template.substitute(template_vars)

    return contents

def write_from_template(
        template_path, working_path, target_path, template_vars, dry_run):

    contents = from_template(template_path, template_vars)

    with open(working_path, 'w') as outfile:
        outfile.write(contents)

    if not dry_run:
        shutil.move(working_path, target_path)

