#!/usr/bin/env python3


from json import load
from itertools import product

from PIL import Image


image_w = 940
image_h = 492

cells_cache = {}


def create_cell(app, color, w, h):
    if app in cells_cache:
        return cells_cache[app]

    cell = Image.new('RGBA', (w, h), color)
    icon = Image.open('icons/{}-icon.png'.format(app)).convert('RGBA')

    icon_x = int(w / 2 - icon.width / 2)
    icon_y = int(h / 2 - icon.height / 2)

    cell.paste(icon, (icon_x, icon_y), icon)
    cells_cache[app] = cell

    return cell


def main():
    with open('data.json') as f:
        data = load(f).items()

        cell_w = image_w // 2
        cell_h = image_h

        for (app1, color1), (app2, color2) in product(data, data):
            if app1 != app2:
                title = '{}-{}'.format(app1, app2)
                image = Image.new('RGBA', (image_w, image_h))

                cell1 = create_cell(app1, color1, cell_w, cell_h)
                cell2 = create_cell(app2, color2, cell_w, cell_h)

                image.paste(cell1)
                image.paste(cell2, (cell_w, 0))

                image.save('dist/{}.png'.format(title), 'PNG')
                print(title)


if __name__ == '__main__':
    main()
