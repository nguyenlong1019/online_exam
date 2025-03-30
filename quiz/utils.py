from django.utils.timezone import localtime 
from django.utils.html import format_html 


def to_localtime(time):
    try:
        return localtime(time).strftime("%d-%m-%Y %H:%M:%S")
    except Exception as e:
        return ''
    

def to_blank_window(url, desc):
    return format_html('<a href="{}" target="_blank">{}</a>', url, desc)


def to_download_window(url, desc):
    return format_html('<a href="{}" download>{}</a>', url, desc)


def to_display_image(url, desc):
    if url:
        return format_html('<img src="{}" alt="{}" style="width: 40px;height: 40px;border-radius: 50%;border: 2px solid #fff;"/>', url, desc)
    return format_html('<img src="/static/assets/images/image-gallery.png" alt="No image" style="width: 40px;height: 40px;border-radius: 50%;border: 2px solid #000;"/>', url, desc)