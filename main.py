from pygame import *


class Base(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.imagen = image.load('imagenes/segm7.png')
        self.imagen = transform.scale2x(self.imagen)
        self.imagen.set_colorkey((255, 0, 255), RLEACCEL)
        self.rect = self.imagen.get_rect(topleft=(x, y))

    def update(self, superficie):
        superficie.blit(self.imagen, self.rect)


class Fondo(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.imagen = Surface((340, 520))
        self.imagen.fill((60, 60, 60))
        self.rect = self.imagen.get_rect(topleft=(x, y))

    def update(self, superficie):
        superficie.blit(self.imagen, self.rect)


class Boton(sprite.Sprite):
    def __init__(self, pos, index, name="", name_pos=(0, 0)):
        sprite.Sprite.__init__(self)
        self.imagen = Surface((100, 60))
        self.rect = self.imagen.get_rect(center=pos)
        self.index = index
        self.nombre = name
        self.encendido = False
        self.etiqueta= Texto(name_pos[0], name_pos[1], 30)

    def update(self, superficie):
        if self.encendido:
            self.imagen.fill((200, 20, 20))
        else:
            self.imagen.fill((128, 128, 128))
        superficie.blit(self.imagen, self.rect)
        self.etiqueta.update(superficie, self.nombre)


class Pin(sprite.Sprite):
    def __init__(self, pos, index, name="", name_pos=(0, 0)):
        sprite.Sprite.__init__(self)
        self.imagen = Surface((20, 60))
        self.rect = self.imagen.get_rect(topleft=pos)
        self.index = index
        self.nombre = name
        self.encendido = True if name not in ("-", "+")else False
        self.etiqueta= Texto(name_pos[0], name_pos[1], 30)

    def update(self, superficie):
        if self.encendido:
            self.imagen.fill((200, 20, 20))
        else:
            self.imagen.fill((128, 128, 128))
        superficie.blit(self.imagen, self.rect)
        self.etiqueta.update(superficie, self.nombre)


class Segmento(sprite.Sprite):
    def __init__(self, pos, index, name, name_pos=(10, 10)):
        sprite.Sprite.__init__(self)
        self.imagen = image.load('imagenes/seg'+str(index)+'.png')
        self.imagen.set_colorkey((255, 0, 255), RLEACCEL)
        self.imagen = transform.scale2x(self.imagen)
        self.rect = self.imagen.get_rect(topleft=(pos[0], pos[1]))
        self.index = index
        self.nombre = name
        self.encendido = True
        self.etiqueta= Texto(name_pos[0], name_pos[1], 30, (220, 220, 220))

    def update(self, superficie):
        if self.encendido:
            superficie.blit(self.imagen, self.rect)
        self.etiqueta.update(superficie, self.nombre)


class Texto(object):
    def __init__(self, xpos, ypos, size=40, color=(0, 0, 0)):
        self.letra = font.SysFont('Segoe UI', size)
        self.color = color
        self.x = xpos
        self.y = ypos

    def update(self, superficie, mensage):
        self.imagen = self.letra.render(str(mensage), True, self.color)
        self.rect = self.imagen.get_rect(center=(self.x, self.y))
        superficie.blit(self.imagen, self.rect)


class Cursor(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.imagen = Surface((20, 20))
        self.rect = self.imagen.get_rect(topleft=(0, 0))
        self.select = False

    def update(self, superficie, pos):
        self.rect.center = (pos)
        if self.select:
            self.select = False


pin_pos = ([(291, 80), "a", (301, 60)], [(368, 80), "b", (378, 60)], [(291, 660), "c", (301, 735)], [(137, 660), "d", (147, 735)], [(60, 660), "e", (70, 735)], [
           (137, 80), "f", (147, 60)], [(60, 80), "g", (70, 60)], [(368, 660), "DP", (378, 735)], [(214, 660), "-", (224, 735)], [(214, 80), "-", (224, 60)])


seg_pos = ([(142, 184), "a", (245, 200)], [(302, 192), "b", (330, 290)], [(278, 402), "c", (305, 500)], [(98, 578), "d", (205, 595)], [
           (88, 410), "e", (115, 500)], [(114, 194), "f", (145, 290)], [(136, 380), "g", (220, 395)], [(326, 574), "DP", (350, 597)])


class Display_7(object):
    def __init__(self):
        init()
        self.correr = True
        self.pantalla = display.set_mode((800, 800))
        self.lista_bin = [1, 1, 1, 1, 1, 1, 1, 1]
        self.valor_bin = str("".join(map(str, self.lista_bin)))
        self.modulo_display = Base(50, 140)
        self.fondo = Fondo(50, 140)
        self.pins = sprite.Group()
        for i in range(10):
            i = Pin(pin_pos[i][0], i, pin_pos[i][1], pin_pos[i][2])
            self.pins.add(i)

        self.texto_bin = Texto(600, 160)
        self.texto_bin_inv = Texto(600, 100)

        self.texto_hex = Texto(600, 280)
        self.texto_hex_inv = Texto(600, 220)

        self.cursor = Cursor()
        self.grupo_cursor = sprite.Group(self.cursor)
        self.grupo_segmento = sprite.Group()
        for i in range(8):
            i = Segmento(seg_pos[i][0], i, seg_pos[i][1], seg_pos[i][2])
            self.grupo_segmento.add(i)

        self.boton=Boton((720,720),0, "Cátodo", (720,720))
        self.grupo_boton= sprite.Group(self.boton)
        self.anodo_catodo = 'Cátodo'

    def input(self):
        self.keys = key.get_pressed()
        for event_type in event.get():
            if event_type.type == QUIT:
                self.correr = False
                quit()
            if event_type.type == MOUSEBUTTONDOWN:
                for boton in sprite.groupcollide(self.grupo_boton,
                                                self.grupo_cursor, False, False):
                    
                    self.anodo_catodo = 'Ánodo' if self.anodo_catodo == 'Cátodo' else 'Cátodo'
                    boton.nombre = self.anodo_catodo

                    for pin in self.pins:
                        
                        pin.encendido = not pin.encendido
                        pin.nombre = '-' if pin.nombre == '+' else '+' if pin.nombre == '-' else pin.nombre


                    for tile in self.grupo_segmento:
                        pin.nombre = '-' if pin.nombre == '+' else '+' if pin.nombre == '-' else pin.nombre
                    
                        self.lista_bin[-tile.index-1] = int(tile.encendido if self.anodo_catodo == 'Cátodo' else not tile.encendido)
                        self.valor_bin = str("".join(map(str, self.lista_bin)))
                    

                for tile in sprite.groupcollide(self.grupo_segmento,
                                                self.grupo_cursor, False, False):
                    tile.encendido = not tile.encendido
                    for pin in self.pins:
                        if pin.index == tile.index:
                            pin.encendido = tile.encendido if self.anodo_catodo == 'Cátodo' else not tile.encendido
                            break
                    self.lista_bin[-tile.index-1] = int(tile.encendido if self.anodo_catodo == 'Cátodo' else not tile.encendido)
                    self.valor_bin = str("".join(map(str, self.lista_bin)))

    def Act(self):
        while self.correr:
            d = mouse.get_pos()
            self.grupo_cursor.update(self.pantalla, d)
            self.pantalla.fill((200, 200, 200))
            self.pins.update(self.pantalla)
            self.fondo.update(self.pantalla)
            self.grupo_segmento.update(self.pantalla)
            self.texto_bin.update(self.pantalla, "Bin  (Inv): " + str(self.valor_bin))
            self.texto_bin_inv.update(self.pantalla, "Bin: " + str(self.valor_bin[::-1]))
            self.texto_hex.update(self.pantalla, "Hex (Inv): " +
                                 hex(int(str(self.valor_bin)[::-1], 2)))
            self.texto_hex_inv.update(
                self.pantalla, "Hex: " + hex(int(str(self.valor_bin), 2)))
            self.modulo_display.update(self.pantalla)
            self.grupo_boton.update(self.pantalla)
            display.update()
            self.input()


display_7 = Display_7()
display_7.Act()
