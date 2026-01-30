EMPTY = '.'
TOKEN_P1 = 'X'
TOKEN_P2 = 'O'

HUMAN = 1
COMPUTER_RANDOM = 2
COMPUTER_STRATEGIC = 3


def get_board_dimensions():
    while True:
        try:
            rows = int(input("Enter number of rows\n").strip())
            if rows < 2 or rows > 100:
                print("Invalid rows. Must be between 2 and 100.")
                continue

            cols = int(input("Enter number of columns\n").strip())
            if cols < 2 or cols > 100:
                print("Invalid columns. Must be between 2 and 100.")
                continue

            return rows, cols
        except ValueError:
            print("Invalid input. Enter numbers only.")


def get_connect_n(rows, cols):
    max_dim = max(rows, cols)
    min_dim = min(rows, cols)

    if min_dim == 2:
        return 2

    if min_dim == 3 or max_dim == 3:
        return 3

    if max_dim <= 5:
        return 3

    if max_dim <= 10:
        return 4

    return 5


def is_column_full(board, col, rows, cols):
    if rows <= 0 or cols <= 0:
        return True
    if col < 0 or col >= cols:
        return True
    return board[0][col] != EMPTY


def is_board_full(board, rows, cols):
    for c in range(cols):
        if not is_column_full(board, c, rows, cols):
            return False
    return True


def is_in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def get_free_row(board, col, rows, cols):
    if col < 0 or col >= cols:
        return -1
    for r in range(rows - 1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return -1


def make_move(board, col, rows, cols, token):
    if col < 0 or col >= cols or is_column_full(board, col, rows, cols):
        return -1
    row = get_free_row(board, col, rows, cols)
    board[row][col] = token
    return row


def make_move_tictactoe(board, cell, token):
    row = (cell - 1) // 3
    col = (cell - 1) % 3
    if board[row][col] != EMPTY:
        return -1, -1
    board[row][col] = token
    return row, col


def is_cell_taken(board, cell):
    row = (cell - 1) // 3
    col = (cell - 1) % 3
    return board[row][col] != EMPTY


def check_victory(board, rows, cols, last_row, last_col, token, connect_n):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for dr, dc in directions:
        count = 1

        for i in range(1, connect_n):
            r = last_row - dr * i
            c = last_col - dc * i
            if is_in_bounds(r, c, rows, cols) and board[r][c] == token:
                count += 1
            else:
                break

        for i in range(1, connect_n):
            r = last_row + dr * i
            c = last_col + dc * i
            if is_in_bounds(r, c, rows, cols) and board[r][c] == token:
                count += 1
            else:
                break

        if count >= connect_n:
            return True
    return False


def human_choose(board, cols, rows):
    while True:
        try:
            col = int(input(f"Enter column (1-{cols}): "))
            col -= 1

            if col < 0 or col >= cols:
                print(f"Invalid column. Choose between 1 and {cols}.")
                continue

            if is_column_full(board, col, rows, cols):
                print(f"Column {col + 1} is full. Choose another column.")
                continue

            return col
        except ValueError:
            print("Invalid input. Enter a number.")


def human_choose_tictactoe(board):
    while True:
        try:
            cell = int(input("Enter position (1-9):\n"))

            if cell < 1 or cell > 9:
                print("Invalid cell. Choose between 1 and 9.")
                continue

            if is_cell_taken(board, cell):
                print(f"Cell {cell} is taken. Choose another cell.")
                continue

            return cell
        except ValueError:
            print("Invalid input. Enter a number.")


def computer_random_choose(board, cols, rows):
    for col in range(cols):
        if not is_column_full(board, col, rows, cols):
            return col
    return 0


def computer_strategic_choose(board, cols, rows, my_token, opp_token, connect_n):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    order = list(range(cols))
    center2 = cols + 1

    for i in range(cols - 1):
        best = i
        for j in range(i + 1, cols):
            c1, c2 = order[best], order[j]
            d1 = abs(2 * (c1 + 1) - center2)
            d2 = abs(2 * (c2 + 1) - center2)
            if d2 < d1 or (d2 == d1 and c2 < c1):
                best = j
        if best != i:
            order[i], order[best] = order[best], order[i]

    for col in order:
        if is_column_full(board, col, rows, cols):
            continue
        temp_board = [row[:] for row in board]
        row = make_move(temp_board, col, rows, cols, my_token)
        if row != -1 and check_victory(temp_board, rows, cols, row, col, my_token, connect_n):
            return col

    for col in order:
        if is_column_full(board, col, rows, cols):
            continue
        temp_board = [row[:] for row in board]
        row = make_move(temp_board, col, rows, cols, opp_token)
        if row != -1 and check_victory(temp_board, rows, cols, row, col, opp_token, connect_n):
            return col

    target = connect_n - 1
    for col in order:
        if is_column_full(board, col, rows, cols):
            continue
        temp_board = [row[:] for row in board]
        row = make_move(temp_board, col, rows, cols, my_token)
        if row == -1:
            continue

        for dr, dc in directions:
            count = 1
            for i in range(1, connect_n):
                rr, cc = row - dr * i, col - dc * i
                if is_in_bounds(rr, cc, rows, cols) and temp_board[rr][cc] == my_token:
                    count += 1
                else:
                    break
            for i in range(1, connect_n):
                rr, cc = row + dr * i, col + dc * i
                if is_in_bounds(rr, cc, rows, cols) and temp_board[rr][cc] == my_token:
                    count += 1
                else:
                    break
            if count == target:
                return col

    for col in order:
        if is_column_full(board, col, rows, cols):
            continue
        temp_board = [row[:] for row in board]
        row = make_move(temp_board, col, rows, cols, opp_token)
        if row == -1:
            continue

        for dr, dc in directions:
            count = 1
            for i in range(1, connect_n):
                rr, cc = row - dr * i, col - dc * i
                if is_in_bounds(rr, cc, rows, cols) and temp_board[rr][cc] == opp_token:
                    count += 1
                else:
                    break
            for i in range(1, connect_n):
                rr, cc = row + dr * i, col + dc * i
                if is_in_bounds(rr, cc, rows, cols) and temp_board[rr][cc] == opp_token:
                    count += 1
                else:
                    break
            if count == target:
                return col

    for col in order:
        if not is_column_full(board, col, rows, cols):
            return col
    return 0


def init_board(rows, cols):
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]


def print_board(board, rows, cols):
    print()
    for r in range(rows):
        print("|", end="")
        for c in range(cols):
            print(board[r][c], end="|")
        print()
    for c in range(1, cols + 1):
        print(f" {c % 10}", end="")
    print("\n")


def print_board_tictactoe(board):
    for r in range(3):
        print("|", end="")
        for c in range(3):
            print(board[r][c], end="|")
        print()


def is_board_full_tictactoe(board):
    for r in range(3):
        for c in range(3):
            if board[r][c] == EMPTY:
                return False
    return True


def get_player_type(player_number):
    while True:
        ch = input(f"Choose type for player {player_number}: h - human, r - random/simple computer, s - strategic computer: ").strip()
        if not ch:
            print("Input error. Try again.")
            continue
        ch = ch[0].lower()
        if ch == 'h':
            return HUMAN
        if ch == 'r':
            return COMPUTER_RANDOM
        if ch == 's':
            return COMPUTER_STRATEGIC
        print("Invalid selection. Enter h, r, or s.")


def run_connect_four(board, rows, cols, p1_type, p2_type, connect_n):
    tokens = [TOKEN_P1, TOKEN_P2]
    types = [p1_type, p2_type]
    current_player = 0

    while True:
        player_num = current_player + 1
        token = tokens[current_player]

        print(f"Player {player_num} ({token}) turn.")

        if types[current_player] == HUMAN:
            col = human_choose(board, cols, rows)
        elif types[current_player] == COMPUTER_RANDOM:
            col = computer_random_choose(board, cols, rows)
            print(f"Computer chose column {col + 1}")
        else:
            col = computer_strategic_choose(board, cols, rows, tokens[current_player],
                                            tokens[1 - current_player], connect_n)
            print(f"Computer chose column {col + 1}")

        row = make_move(board, col, rows, cols, token)
        print_board(board, rows, cols)

        if check_victory(board, rows, cols, row, col, token, connect_n):
            print(f"Player {player_num} ({token}) wins!")
            break

        if is_board_full(board, rows, cols):
            print("Board full and no winner. It's a tie!")
            break

        current_player = 1 - current_player


def run_tictactoe(board):
    tokens = [TOKEN_P1, TOKEN_P2]
    current_player = 0

    while True:
        player_num = current_player + 1
        token = tokens[current_player]

        cell = human_choose_tictactoe(board)
        row, col = make_move_tictactoe(board, cell, token)

        print_board_tictactoe(board)

        if check_victory(board, 3, 3, row, col, token, 3):
            print(f"Player {player_num} ({token}) wins!")
            break

        if is_board_full_tictactoe(board):
            print("Board full and no winner. It's a tie!")
            break

        current_player = 1 - current_player


def main():
    rows, cols = get_board_dimensions()
    connect_n = get_connect_n(rows, cols)

    if rows == 3 or cols == 3:
        rows = 3
        cols = 3
        connect_n = 3
        print("Tic Tac Toe (Human vs Human)")
        board = init_board(rows, cols)
        print_board_tictactoe(board)
        run_tictactoe(board)
    else:
        print(f"Connect Four - Or More [Or Less] ({rows} rows x {cols} cols, connect {connect_n})")
        p1_type = get_player_type(1)
        p2_type = get_player_type(2)
        board = init_board(rows, cols)
        print_board(board, rows, cols)
        run_connect_four(board, rows, cols, p1_type, p2_type, connect_n)


if __name__ == "__main__":
    main()