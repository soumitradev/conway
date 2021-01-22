class GameConfig:
    def __init__(self):
        self.name = "(Untitled)"
        self.comments = []
        self.author = "Unknown"
        self.start_coords = [0, 0]
        self.rules = {
            "survive": [2, 3],
            "death": [3]
        }
        self.board = []
        self.padding = 10


def printboard(game):
    for i in range(game.height):
        for j in range(game.width):
            print(int(game.board[i*game.width + j]), end="")
        print()


def read_rle(path):
    import re
    game = GameConfig()

    def get_name(line):
        game.name = line[3:]

    def get_comments(line):
        game.comments.append(line[3:])

    def get_author(line):
        game.author = line[3:]

    def get_start_coords(line):
        game.start_coords = [int(x) for x in line[3:].split()]

    def get_rules(line):
        rule_txt = line[3:].split("/")
        game.rules["survive"] = [int(x) for x in rule_txt[0]]
        game.rules["death"] = [int(x) for x in rule_txt[1]]

    info_lines = {
        "#C": get_comments,
        "#c": get_comments,
        "#O": get_author,
        "#N": get_name,
        "#R": get_start_coords,
        "#r": get_rules,
    }

    with open(path, "r") as f:
        lines = f.readlines()
        cmds = "".join([x.strip() for x in lines if not (
            x.startswith('#') or x.startswith('x'))])
    for line in lines:
        if line.startswith("#"):
            info_lines[line[:2]](line)
        elif line.startswith("x"):
            myl = line.split(", ")
            horizontal_size = int(myl[0].split("=")[1].strip())
            vertical_size = int(myl[1].split("=")[1].strip())
            game.board = [False] * (horizontal_size +
                                    2*game.padding) * (vertical_size + 2*game.padding)
            game.width = (horizontal_size + 2*game.padding)
            game.height = (vertical_size + 2*game.padding)
            if len(myl) == 3:
                rule_txt = myl[2].split("=")[1].strip().split("/")
                game.rules["survive"] = [int(x) for x in rule_txt[1][1:]]
                game.rules["death"] = [int(x) for x in rule_txt[0][1:]]
    key = {
        'b': False,
        'o': True
    }
    row_counter = game.padding
    multiplier = ""
    cmd_char_counter = 0
    column_counter = 0
    while cmd_char_counter < len(cmds):
        if cmds[cmd_char_counter].isdigit():
            multiplier += cmds[cmd_char_counter]
        else:
            if cmds[cmd_char_counter] in key:
                if multiplier:
                    for i in range(int(multiplier)):
                        game.board[(row_counter*game.width) +
                                   column_counter + game.padding] = key[cmds[cmd_char_counter]]
                        column_counter += 1
                    multiplier = ""
                else:
                    game.board[(row_counter*game.width) +
                               column_counter + game.padding] = key[cmds[cmd_char_counter]]
                    column_counter += 1
            elif cmds[cmd_char_counter] == "!":
                break
            elif cmds[cmd_char_counter] == "$":
                row_counter += 1
                column_counter = 0
            else:
                raise Exception("Invalid file format!")
        cmd_char_counter += 1
    return game
