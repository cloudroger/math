from PIL import Image
import numpy as np
import math


def pixelize_image(image, percent):
    im = Image.open(image).convert('RGB')
    im2 = im.copy()
    pix = im.load()

    width, height = im.size

    def get_squares(width, height):
        mini = min(width, height)
        halves = -1
        num = 1
        while True:
            halves += 1
            num = num * 2
            if num > mini:
                break

        squares = {0:{'widths':[[0, width]], 'heights':[[0, height]]}}

        for i in range(halves):
            prevwidths = squares[i]['widths']
            prevheights = squares[i]['heights']

            index = i + 1
            squares[index] = {}
            squares[index]['widths'] = []
            squares[index]['heights'] = []

            for position in range(len(prevwidths)):
                widthrange = prevwidths[position]
                heightrange = prevheights[position]

                wmidpoint = int((((widthrange[1] - widthrange[0]) / 2) + widthrange[0]))
                squares[index]['widths'].append([widthrange[0], wmidpoint])
                squares[index]['widths'].append([wmidpoint, widthrange[1]])

                hmidpoint = int((((heightrange[1] - heightrange[0]) / 2) + heightrange[0]))
                squares[index]['heights'].append([heightrange[0], hmidpoint])
                squares[index]['heights'].append([hmidpoint, heightrange[1]])

        index = index + 1
        squares[index] = {}
        squares[index]['widths'] = []
        squares[index]['heights'] = []

        for width in range(width-1):
            squares[index]['widths'].append([width, width+1])

        for height in range(height-1):
            squares[index]['heights'].append([height, height+1])

        return squares


    def get_square_averages(squares, pixels):

        square_averages = {}

        for level in squares.keys():
            square_averages[level] = {}

            length = len(squares[level]['widths'])
            hlength = len(squares[level]['heights'])

            for pos in range(length):
                for pospos in range(hlength):
                    ws = squares[level]['widths'][pos]
                    hs = squares[level]['heights'][pospos]

                    wstart = ws[0]
                    wend = ws[1]

                    hstart = hs[0]
                    hend = hs[1]

                    square_key = (wstart, wend, hstart, hend)

                    rs = []
                    gs = []
                    bs = []

                    for xi in range(wstart, wend):
                        for yi in range(hstart, hend):
                            rs.append(pixels[xi, yi][0])
                            gs.append(pixels[xi, yi][1])
                            bs.append(pixels[xi, yi][2])

                    rmean = int(np.mean(rs))
                    gmean = int(np.mean(gs))
                    bmean = int(np.mean(bs))
                    rgbmeans = (rmean, gmean, bmean)
                    square_averages[level][square_key] = rgbmeans

        return square_averages

    squares = get_squares(width, height)
    square_averages = get_square_averages(squares, pix)

    def pixelize(image, squares, square_averages, percent):
        levels = math.floor(list(squares.keys())[-1] * percent)

        for level in range(levels):
            for square_key in square_averages[level].keys():
                wstart = square_key[0]
                wend = square_key[1]
                hstart = square_key[2]
                hend = square_key[3]

                rgb = square_averages[level][square_key]

                for xi in range(wstart, wend):
                    for yi in range(hstart, hend):
                        image.putpixel((xi, yi), rgb)

        #image.save(str(time.time())+'.jpeg')
        return image

    pixeled_image = pixelize(im2, squares, square_averages, percent)
    #pixeled_image.show()
    return pixeled_image
