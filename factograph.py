import os
import requests

from requests.auth import HTTPBasicAuth
from PIL import Image


image_w = 940
image_h = 492

cells_cache = {}


def get_templates():
    url = 'https://api.pluga.co/support/v1/task_templates'

    username = os.getenv('PLG_SUPPORT_USERNAME')
    password = os.getenv('PLG_SUPPORT_PASSWORD')

    return requests.get(url, auth=HTTPBasicAuth(username, password)).json()


def generate_data():
    colors = {}
    matches = set()

    for template in get_templates():
        app_source = template['app_source']
        app_target = template['app_target']

        colors[app_source['app_id']] = app_source['color']
        colors[app_target['app_id']] = app_target['color']

        matches.add((app_source['app_id'], app_target['app_id']))

    return colors, matches


def create_cell(app, color, width, height):
    if app in cells_cache:
        return cells_cache[app]

    cell = Image.new('RGBA', (width, height), color)
    icon = Image.open('icons/{a}/{a}-icon.png'.format(a=app)).convert('RGBA')

    icon_x = (width - icon.width) // 2
    icon_y = (height - icon.height) // 2

    cell.paste(icon, (icon_x, icon_y), icon)
    cells_cache[app] = cell

    return cell


def main():
    colors, matches = generate_data()

    cell_w = image_w // 2
    cell_h = image_h

    for app1, app2 in matches:
        title = '{}-{}'.format(app1, app2)
        image = Image.new('RGBA', (image_w, image_h))

        cell1 = create_cell(app1, colors[app1], cell_w, cell_h)
        cell2 = create_cell(app2, colors[app2], cell_w, cell_h)

        image.paste(cell1)
        image.paste(cell2, (cell_w, 0))

        image.save('dist/{}.png'.format(title), 'PNG', optimize=True)
        image.save('dist/{}.png'.format(title), 'PNG', optimize=True)

        print(title)


if __name__ == '__main__':
    main()
