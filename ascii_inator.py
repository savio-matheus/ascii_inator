from math import floor
from os import system

from wand.image import Image

class Ascii:
    __CHARACTERS = '`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
    __NUMBER_CHRS = 65
    __STEP = 3.923076924 # ~= 255 / 65

    def __init__(self, filename, multiplier=1, mapping_alg='average'):
        self.pixelMatrix = list()
        self.charMatrix = list()
        self.colorMatrix = list()
        self.filename = filename
        self.width = 0
        self.height = 0

        self.__load_image()
        self.__map_chars(multiplier, mapping_alg)

    def print_ascii(self, to_file=False):
        title = f'{self.filename}\n{self.width} x {self.height} pixels'
        if to_file:
            with open(self.filename + '.txt', 'w') as f:
                print(title, file=f)
                for i in self.charMatrix:
                    print(i, file=f)
        else:
            print(title)
            for i in range(len(self.charMatrix)):
                print(self.colored(self.colorMatrix[i][0], self.colorMatrix[i][1], self.colorMatrix[i][2], self.charMatrix[i]))

    def __load_image(self):
        with Image(filename=self.filename) as img:
            p = img.export_pixels(channel_map='RGB')
            
            # Agrupa os valores em tuplas (r, g, b)
            p = [i for i in zip(*[iter(p)] * 3)]
            self.colorMatrix = p
            # Transforma a lista uma matriz
            self.pixelMatrix = [p[i:i+img.width] for i in range(0, len(p), img.width)]

            self.width = img.width
            self.height = img.height

    # não é muito rápido...
    def __map_chars(self, multiplier, mapping_alg):
        if mapping_alg == 'lightness':
            alg = self.__lightness
        elif mapping_alg == 'luminosity':
            alg = self.__luminosity
        else:
            alg = self.__average

        for i in range(len(self.pixelMatrix)):
            self.charMatrix.append("")
            for j in range(len(self.pixelMatrix[i])):
                c = floor(alg(self.pixelMatrix[i][j]) / self.__STEP)
                c = self.__CHARACTERS[c]
                self.charMatrix[i] += c*multiplier

    def __average(self, rgb):
        r, g, b = rgb
        return (r + g + b) / 3

    def __lightness(self, rgb):
        r, g, b = rgb
        return (max(r, g, b) + min(r, g, b)) / 2

    def __luminosity(self, rgb):
        r, g, b = rgb
        return 0.21*r + 0.72*g + 0.07*b

    def colored(self, r, g, b, text):
        return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


def main():
    print('Boas-vindas ao Ascii Inator!')
    print('Use Ctrl+C para sair\n')
    while True:
        filename = input('Nome da imagem (incluindo extensão): ')
        if not filename:
            continue
        try:
            with open(filename, 'rb') as tmp:
                pass
        except FileNotFoundError:
            print('O arquivo não existe')
        else:
            break

    while True:
        mult = input('\nMultiplicar largura por [padrão = 1]: ')
        if not mult:
            mult = 1
            break
        try:
            mult = int(mult)
            if mult <= 0:
                raise ValueError
        except ValueError:
            print('Insira um número natural não nulo')
        else:
            break

    while True:
        print('\nAlgoritmo de mapeamento')
        print('0: Média')
        print('1: Claridade')
        print('2: Luminosidade')
        alg = input('ESCOLHA [padrão = 0]: ')
        if not alg:
            alg = 0
            break
        try:
            alg = int(alg)
            if alg < 0 or alg > 2:
                raise ValueError
        except ValueError:
            print('Opção inválida')
        else:
            break

    while True:
        print('\nSaída')
        print('0: terminal')
        print('1: arquivo')
        out = input('ESCOLHA [padrão = 0]: ')
        if not out:
            out = 0
            break
        try:
            out = int(out)
            if out < 0 or out > 1:
                raise ValueError
        except ValueError:
            print('Opção inválida')
        else:
            break

    algorithms = {
        0:'average',
        1:'lightness',
        2:'luminosity',
    }
    to_file = {
        0:False,
        1:True,
    }

    system('clear')
    image = Ascii(filename, mult, algorithms[alg])
    image.print_ascii(to_file[out])

if __name__ == '__main__':
    main()
