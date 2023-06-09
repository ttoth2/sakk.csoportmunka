import pygame

class Bábu:
    def __init__(self, pos, color, tábla):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.has_moved = False

    def get_moves(self, tábla):
        output = []
        for direction in self.get_possible_moves(tábla):
            for square in direction:
                if square.occupying_piece is not None:
                    if square.occupying_piece.color == self.color:
                        break
                    else:
                        output.append(square)
                        break
                else:
                    output.append(square)
        return output
    def lehet(self, tábla):
        output = []
        for square in self.get_moves(tábla):
            if not tábla.sak(self.color, board_change=[self.pos, square.pos]):
                output.append(square)
        return output
    def move(self, tábla, square, force=False):
        for i in tábla.squares:
            i.highlight = False
        if square in self.lehet(tábla) or force:
            prev_square = tábla.get_square_from_pos(self.pos)
            self.pos, self.x, self.y = square.pos, square.x, square.y
            prev_square.occupying_piece = None
            square.occupying_piece = self
            tábla.selected_piece = None
            self.has_moved = True

            if self.jel == ' ':
                if self.y == 0 or self.y == 7:
                    square.occupying_piece = Vezér(
                        (self.x, self.y),
                        self.color,
                        tábla
                    )

            if self.jel == 'K':
                if prev_square.x - self.x == 2:
                    rook = tábla.get_piece_from_pos((0, self.y))
                    rook.move(tábla, tábla.get_square_from_pos((3, self.y)), force=True)
                elif prev_square.x - self.x == -2:
                    rook = tábla.get_piece_from_pos((7, self.y))
                    rook.move(tábla, tábla.get_square_from_pos((5, self.y)), force=True)
            return True
        else:
            tábla.selected_piece = None
            return False

    def attacking_squares(self, board):
        return self.get_moves(board)



###################################################################################################
class Paraszt(Bábu):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        img_path = 'sakk/' + color[0] + '_pawn.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (board.tile_width - 35, board.tile_height - 35))
        self.jel = ' '

    def lehetöség(self, tábla):
        output = []
        moves = []
        # move forward
        if self.color == 'white':
            moves.append((0, -1))
            if not self.has_moved:
                moves.append((0, -2))


        elif self.color == 'black':
            moves.append((0, 1))
            if not self.has_moved:
                moves.append((0, 2))
        for move in moves:
            new_pos = (self.x, self.y + move[1])
            if new_pos[1] < 8 and new_pos[1] >= 0:
                output.append(
                    tábla.get_square_from_pos(new_pos)
                )
        return output

    def get_moves(self, tábla):
        output = []
        for square in self.lehetöség(tábla):
            if square.occupying_piece != None:
                break
            else:
                output.append(square)
        if self.color == 'white':
            if self.x + 1 < 8 and self.y - 1 >= 0:
                square = tábla.get_square_from_pos(
                    (self.x + 1, self.y - 1)
                )
                if square.occupying_piece != None:
                    if square.occupying_piece.color != self.color:
                        output.append(square)
            if self.x - 1 >= 0 and self.y - 1 >= 0:
                square = tábla.get_square_from_pos(
                    (self.x - 1, self.y - 1)
                )
                if square.occupying_piece != None:
                    if square.occupying_piece.color != self.color:
                        output.append(square)
        elif self.color == 'black':
            if self.x + 1 < 8 and self.y + 1 < 8:
                square = tábla.get_square_from_pos(
                    (self.x + 1, self.y + 1)
                )
                if square.occupying_piece != None:
                    if square.occupying_piece.color != self.color:
                        output.append(square)
            if self.x - 1 >= 0 and self.y + 1 < 8:
                square = tábla.get_square_from_pos(
                    (self.x - 1, self.y + 1)
                )
                if square.occupying_piece != None:
                    if square.occupying_piece.color != self.color:
                        output.append(square)
        return output

    def attacking_squares(self, tábla):
        moves = self.get_moves(tábla)
        # return the diagonal moves
        return [i for i in moves if i.x != self.x]



###################################################################################################


class Ló(Bábu):
    def __init__(self, pos, color, tábla):
        super().__init__(pos, color, tábla)
        img_path = 'sakk/' + color[0] + '_knight.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (tábla.tile_width - 20, tábla.tile_height - 20))
        self.jel = 'L'

    def get_possible_moves(self, tábla):
        l = []
        moves = [(1, -2),(2, -1),(2, 1),(1, 2),(-1, 2),(-2, 1),(-2, -1),(-1, -2)]

        for move in moves:
            new_pos = (self.x + move[0], self.y + move[1])
            if (
                new_pos[0] < 8 and
                new_pos[0] >= 0 and
                new_pos[1] < 8 and
                new_pos[1] >= 0
            ):
                l.append([
                    tábla.get_square_from_pos(
                        new_pos
                    )
                ])
        return l



####################################################################################################################
class Bástya(Bábu):
    def __init__(self, pos, color, tábla):
        super().__init__(pos, color, tábla)
        img_path = 'sakk/' + color[0] + '_rook.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (tábla.tile_width - 20, tábla.tile_height - 20))
        self.jel = 'B'

    def get_possible_moves(self, tábla):
        l = []
        moves_north = []
        for y in range(self.y)[::-1]:
            moves_north.append(tábla.get_square_from_pos(
                (self.x, y)
            ))
        l.append(moves_north)
        moves_east = []
        for x in range(self.x + 1, 8):
            moves_east.append(tábla.get_square_from_pos(
                (x, self.y)
            ))
        l.append(moves_east)
        moves_south = []
        for y in range(self.y + 1, 8):
            moves_south.append(tábla.get_square_from_pos(
                (self.x, y)
            ))
        l.append(moves_south)
        moves_west = []
        for x in range(self.x)[::-1]:moves_west.append(tábla.get_square_from_pos((x, self.y)))
        l.append(moves_west)
        return l





####################################################################################################


class Futó(Bábu):
    def __init__(self, pos, color, tábla):
        super().__init__(pos, color, tábla)
        img_path = 'sakk/' + color[0] + '_bishop.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (tábla.tile_width - 20, tábla.tile_height - 20))
        self.jel = 'F'

    def get_possible_moves(self, tábla):
        l = []
        moves_ne = []
        for i in range(1, 8):
            if self.x + i > 7 or self.y - i < 0:
                break
            moves_ne.append(tábla.get_square_from_pos(
                (self.x + i, self.y - i)
            ))
        l.append(moves_ne)
        moves_se = []
        for i in range(1, 8):
            if self.x + i > 7 or self.y + i > 7:
                break
            moves_se.append(tábla.get_square_from_pos(
                (self.x + i, self.y + i)
            ))
        l.append(moves_se)
        moves_sw = []
        for i in range(1, 8):
            if self.x - i < 0 or self.y + i > 7:
                break
            moves_sw.append(tábla.get_square_from_pos(
                (self.x - i, self.y + i)
            ))
        l.append(moves_sw)
        moves_nw = []
        for i in range(1, 8):
            if self.x - i < 0 or self.y - i < 0:
                break
            moves_nw.append(tábla.get_square_from_pos(
                (self.x - i, self.y - i)
            ))
        l.append(moves_nw)
        return l

############################################


class Vezér(Bábu):
    def __init__(self, pos, color, tábla):
        super().__init__(pos, color, tábla)
        img_path = 'sakk/' + color[0] + '_queen.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (tábla.tile_width - 20, tábla.tile_height - 20))
        self.jel = 'V'

    def get_possible_moves(self, tábla):
        h = []
        moves_észak = []
        for y in range(self.y)[::-1]:moves_észak.append(tábla.get_square_from_pos((self.x, y)))
        h.append(moves_észak)
        moves_ne = []
        for i in range(1, 8):
            if self.x + i > 7 or self.y - i < 0:
                break
            moves_ne.append(tábla.get_square_from_pos(
                (self.x + i, self.y - i)
            ))
        h.append(moves_ne)
        moves_k = []
        for x in range(self.x + 1, 8):
            moves_k.append(tábla.get_square_from_pos((x, self.y)))
        h.append(moves_k)
        moves_se = []
        for i in range(1, 8):
            if self.x + i > 7 or self.y + i > 7:
                break
            moves_se.append(tábla.get_square_from_pos(
                (self.x + i, self.y + i)
            ))
        h.append(moves_se)
        moves_d = []
        for y in range(self.y + 1, 8):
            moves_d.append(tábla.get_square_from_pos(
                (self.x, y)
            ))
        h.append(moves_d)
        moves_sw = []
        for i in range(1, 8):
            if self.x - i < 0 or self.y + i > 7:
                break
            moves_sw.append(tábla.get_square_from_pos(
                (self.x - i, self.y + i)
            ))
        h.append(moves_sw)
        moves_west = []
        for x in range(self.x)[::-1]:
            moves_west.append(tábla.get_square_from_pos(
                (x, self.y)
            ))
        h.append(moves_west)
        moves_nw = []
        for i in range(1, 8):
            if self.x - i < 0 or self.y - i < 0:
                break
            moves_nw.append(tábla.get_square_from_pos(
                (self.x - i, self.y - i)
            ))
        h.append(moves_nw)
        return h

######################################################################################################################


class Kir(Bábu ):
    def __init__(self, pos, color, tábla):
        super().__init__(pos, color, tábla)
        img_path = 'sakk/' + color[0] + '_king.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (tábla.tile_width - 20, tábla.tile_height - 20))
        self.jel = 'K'

    def get_possible_moves(self, tábla):
        output = []
        moves = [(0,-1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), ]
        for i in moves:
            new_pos = (self.x + i[0], self.y + i[1])
            if (
                new_pos[0] < 8 and new_pos[0] >= 0 and new_pos[1] < 8 and new_pos[1] >= 0
            ):
                output.append([
                    tábla.get_square_from_pos(new_pos)
                ])
        return output

    def sánc(self, tábla):
        if not self.has_moved:
            if self.color == 'white':
                queenside_rook = tábla.get_piece_from_pos((0, 7))
                kingside_rook = tábla.get_piece_from_pos((7, 7))
                if queenside_rook != None:
                    if not queenside_rook.has_moved:
                        if [tábla.get_piece_from_pos((i, 7)) for i in range(1, 4)] == [None, None, None]:
                            return 'vezérold'
                if kingside_rook != None:
                    if not kingside_rook.has_moved:
                        if [
                            tábla.get_piece_from_pos((i, 7)) for i in range(5, 7)
                        ] == [None, None]:
                            return 'kirold'
            elif self.color == 'black':
                queenside_rook = tábla.get_piece_from_pos((0, 0))
                kingside_rook = tábla.get_piece_from_pos((7, 0))
                if queenside_rook != None:
                    if not queenside_rook.has_moved:
                        if [
                            tábla.get_piece_from_pos((i, 0)) for i in range(1, 4)
                        ] == [None, None, None]:
                            return 'vezérold'
                if kingside_rook != None:
                    if not kingside_rook.has_moved:
                        if [
                            tábla.get_piece_from_pos((i, 0)) for i in range(5, 7)
                        ] == [None, None]:
                            return 'kirold'

    def lehet(self, tábla):
        output = []
        for square in self.get_moves(tábla):
            if not tábla.sak(self.color, board_change=[self.pos, square.pos]):
                output.append(square)
        if self.sánc(tábla) == 'kirold':
            output.append(
                tábla.get_square_from_pos((self.x + 2, self.y)))
        if self.sánc(tábla) == 'vezérold':
            output.append(
                tábla.get_square_from_pos((self.x - 2, self.y)))
        return output