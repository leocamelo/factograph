import os
import requests

from requests.auth import HTTPBasicAuth
from PIL import Image


email_img_w = 640
email_img_h = 316
email_icon_size = 200

social_img_w = 940
social_img_h = 492
social_cell_w = social_img_w // 2
social_cell_h = social_img_h

img_cache = {}
icon_cache = {}


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


def get_icon(app):
    if app in icon_cache:
        return icon_cache[app]

    icon = Image.open('icons/{a}/{a}-icon.png'.format(a=app)).convert('RGBA')
    icon_cache[app] = icon
    return icon


def create_img(app, color, width, height, icon_resize=None):
    cache_key = '{}@{}x{}'.format(app, width, height)

    if cache_key in img_cache:
        return img_cache[cache_key]

    img = Image.new('RGBA', (width, height), color)
    icon = get_icon(app)

    if icon_resize:
        icon = icon.resize(icon_resize)

    icon_x = (width - icon.width) // 2
    icon_y = (height - icon.height) // 2

    img.paste(icon, (icon_x, icon_y), icon)
    img_cache[cache_key] = img
    return img


def save_img(img, scope, filename):
    img.save('dist/{}/{}.png'.format(scope, filename), 'PNG', optimize=True)


def generate_email_images(colors):
    icon_resize = (email_icon_size, email_icon_size)

    for app, color in colors.items():
        img = create_img(app, color, email_img_w, email_img_h, icon_resize)
        save_img(img, 'email', app)
        print(app)


def generate_social_images(colors, matches):
    for app1, app2 in matches:
        title = '{}-{}'.format(app1, app2)
        img = Image.new('RGBA', (social_img_w, social_img_h))

        cell1 = create_img(app1, colors[app1], social_cell_w, social_cell_h)
        cell2 = create_img(app2, colors[app2], social_cell_w, social_cell_h)

        img.paste(cell1)
        img.paste(cell2, (social_cell_w, 0))

        save_img(img, 'social', title)
        print(title)


def main():
    colors, matches = generate_data()

    generate_email_images(colors)
    generate_social_images(colors, matches)


if __name__ == '__main__':
    main()
