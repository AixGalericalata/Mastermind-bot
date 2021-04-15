from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype("seguiemj.ttf", 30)
bull = '\U0001F402'
cow = '\U0001F404'


def create_image(moves):
    WIDTH = 400
    HEIGHT = 600
    image = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    x = 20
    y = HEIGHT - 55
    for move in moves:
        user_move = ''.join(map(lambda x: str(x), move[0]))
        draw.text((x, y), f'{user_move} {" " * 7} {bull * move[1][0]} {cow * move[1][1]}',
                  embedded_color=True, font=font)
        y -= 40

    return image
