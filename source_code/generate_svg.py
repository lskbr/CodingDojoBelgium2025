#!/usr/bin/env python3
"""
Generate SVG version of the coordinate grid
"""


def generate_svg():
    # SVG dimensions
    width = 800
    height = 480
    cell_size = 20

    # Start SVG
    svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <style>
            .grid-line {{ stroke: #ccc; stroke-width: 1; }}
            .axis-line {{ stroke: #000; stroke-width: 2; }}
            .coordinate-label {{ font-family: Arial, sans-serif; font-size: 12px; fill: #000; }}
            .special-label {{ font-family: Arial, sans-serif; font-size: 12px; fill: #f00; }}
        </style>
    </defs>

    <!-- Grid lines -->
"""

    # Draw vertical grid lines
    for x in range(41):
        x_pos = x * cell_size
        svg_content += f'    <line x1="{x_pos}" y1="0" x2="{x_pos}" y2="{height}" class="grid-line"/>\n'

    # Draw horizontal grid lines
    for y in range(25):
        y_pos = y * cell_size
        svg_content += f'    <line x1="0" y1="{y_pos}" x2="{width}" y2="{y_pos}" class="grid-line"/>\n'

    # Draw axes
    svg_content += f"""
    <!-- Axes -->
    <line x1="0" y1="0" x2="{width + 20}" y2="0" class="axis-line" marker-end="url(#arrowhead-right)"/>
    <line x1="0" y1="0" x2="0" y2="{height + 20}" class="axis-line" marker-end="url(#arrowhead-down)"/>

    <!-- Arrow markers -->
    <defs>
        <marker id="arrowhead-right" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="#000"/>
        </marker>
        <marker id="arrowhead-down" markerWidth="7" markerHeight="10" refX="3.5" refY="9" orient="auto">
            <polygon points="0 0, 7 0, 3.5 10" fill="#000"/>
        </marker>
    </defs>

    <!-- Coordinate labels -->
    <text x="5" y="-5" class="coordinate-label">(0,0)</text>
    <text x="{width - 60}" y="{height - 5}" class="coordinate-label">(39,23)</text>

    <!-- Special cell at (10,5) -->
    <rect x="{10 * cell_size}" y="{5 * cell_size}" width="{cell_size}" height="{cell_size}" fill="#000"/>

    <!-- Green cell at (39,23) -->
    <rect x="{39 * cell_size}" y="{23 * cell_size}" width="{cell_size}" height="{cell_size}" fill="#0f0"/>

    <!-- Line from special cell extending outside grid -->
    <line x1="{10 * cell_size + cell_size//2}" y1="{5 * cell_size + cell_size//2}"
          x2="-50" y2="{5 * cell_size + cell_size//2}"
          stroke="#f00" stroke-width="3"/>

    <!-- Special coordinate label at the left -->
    <text x="-45" y="{5 * cell_size + 5}" class="special-label">(10,5)</text>

    <!-- Green coordinate label for (39,23) -->
    <text x="{39 * cell_size + 5}" y="{23 * cell_size - 5}" class="special-label" style="fill: #0f0;">(39,23)</text>

    <!-- Axis labels -->
"""

    # Add x-axis labels at the top
    for x in [0, 10, 20, 30, 39]:
        x_pos = x * cell_size
        svg_content += (
            f'    <text x="{x_pos}" y="-5" class="coordinate-label">{x}</text>\n'
        )

    # Add y-axis labels
    for y in [0, 5, 10, 15, 20, 23]:
        y_pos = y * cell_size
        svg_content += (
            f'    <text x="5" y="{y_pos + 5}" class="coordinate-label">{y}</text>\n'
        )

    # Close SVG
    svg_content += "</svg>"

    return svg_content


if __name__ == "__main__":
    svg_content = generate_svg()

    with open("coordenadas.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)

    print("SVG file 'coordenadas.svg' generated successfully!")
