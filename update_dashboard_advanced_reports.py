"""
Update the Advanced Reports section in sharing_status_model_dashboard_v2.html
with actual interactive Chart.js visualizations.
"""

# Read the original HTML file
with open(r'D:\claude\sharing_status_model_dashboard_v2.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Read the replacement section
with open(r'D:\claude\advanced_reports_section_replacement.html', 'r', encoding='utf-8') as f:
    new_section = f.read()

# Read the chart initialization script
with open(r'D:\claude\advanced_charts_init.js', 'r', encoding='utf-8') as f:
    chart_script = f.read()

# Find the Advanced Reports section start and end
section_start = None
section_end = None
div_count = 0
in_section = False

for i, line in enumerate(lines):
    if 'id="advanced-reports"' in line and 'class="section"' in line:
        section_start = i
        in_section = True
        div_count = 0

    if in_section:
        if '<div' in line:
            div_count += 1
        if '</div>' in line:
            div_count -= 1
            if div_count == 0:
                section_end = i + 1  # Include the closing </div>
                break

print(f"Found Advanced Reports section: lines {section_start + 1} to {section_end}")

# Build new content
new_lines = []

# Add everything before the section
new_lines.extend(lines[:section_start])

# Add the new section
new_lines.append(new_section + '\n')

# Add everything after the old section until the closing </script> tag before footer
# Find where the last </script> is before footer
footer_line = None
for i in range(len(lines) - 1, section_end, -1):
    if '<footer' in lines[i]:
        footer_line = i
        break

# Find last </script> before footer
last_script_end = None
for i in range(footer_line - 1, section_end, -1):
    if '</script>' in lines[i]:
        last_script_end = i + 1
        break

print(f"Last script ends at line {last_script_end}")
print(f"Footer starts at line {footer_line + 1}")

# Add everything from after section to after last script
new_lines.extend(lines[section_end:last_script_end])

# Add the new chart initialization script
new_lines.append('\n    <script>\n')
new_lines.append(chart_script)
new_lines.append('\n    </script>\n\n')

# Add footer and closing tags
new_lines.extend(lines[footer_line:])

# Write the updated file
with open(r'D:\claude\sharing_status_model_dashboard_v2_updated.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("\n=== UPDATE COMPLETE ===")
print(f"Original file lines: {len(lines)}")
print(f"New file lines: {len(new_lines)}")
print(f"Output: D:\\claude\\sharing_status_model_dashboard_v2_updated.html")
