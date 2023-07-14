import avinit

def create_avatar(name: str) -> any:
    avinit.get_svg_avatar(name)
    return avinit.get_avatar_data_url(name)