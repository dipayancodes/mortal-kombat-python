import curses
import random
import time

class Fighter:
    def __init__(self, name, health, damage):
        self.name = name
        self.health = health
        self.damage = damage
        self.blocked_damage = 0

    def attack(self, other):
        attack_damage = random.randint(self.damage // 2, self.damage)
        other.health -= attack_damage - other.blocked_damage
        other.blocked_damage = 0
        return attack_damage

    def special_move(self, other):
        # Simple special move logic: deals double damage
        attack_damage = self.damage * 2
        other.health -= attack_damage - other.blocked_damage
        other.blocked_damage = 0
        return attack_damage

    def block(self):
        self.blocked_damage = random.randint(1, self.damage // 3)

def clear_screen(stdscr):
    stdscr.clear()

def draw_health_bar(stdscr, y, x, health, max_health):
    bar_length = 20
    bar_fill = int((health / max_health) * bar_length)
    health_bar = "=" * bar_fill + " " * (bar_length - bar_fill)
    stdscr.addstr(y, x, f"[{health_bar}] {health}/{max_health}")

def show_message(stdscr, message):
    height, width = stdscr.getmaxyx()
    msg_height, msg_width = 3, 40

    if height < msg_height or width < msg_width:
        # Terminal window is too small to display the message properly
        stdscr.addstr(height // 2, width // 2 - 15, "Terminal window is too small to display the message.")
        stdscr.refresh()
        return

    win = curses.newwin(msg_height, msg_width, height // 2 - msg_height // 2, width // 2 - msg_width // 2)
    win.border()
    win.addstr(1, 1, message.center(msg_width - 2))
    win.refresh()

def opponent_turn(opponent, player):
    # The opponent randomly selects an action
    action = random.choice(["attack", "special_move", "block"])

    if action == "attack":
        attack_damage = opponent.attack(player)
        return f"{opponent.name} attacks {player.name} for {attack_damage} damage!"
    elif action == "special_move":
        attack_damage = opponent.special_move(player)
        return f"{opponent.name} performs a special move and deals {attack_damage} damage!"
    elif action == "block":
        opponent.block()
        return f"{opponent.name} is blocking!"

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    fighter1 = Fighter("Scorpion", 100, 20)
    fighter2 = Fighter("Sub-Zero", 100, 18)

    stdscr.addstr(0, 0, "Mortal Kombat - CLI Edition")
    stdscr.addstr(2, 0, f"{fighter1.name} vs. {fighter2.name}")

    stdscr.refresh()
    time.sleep(2)  # Give players time to read the intro

    while fighter1.health > 0 and fighter2.health > 0:
        clear_screen(stdscr)

        draw_health_bar(stdscr, 4, 5, fighter1.health, 100)
        draw_health_bar(stdscr, 4, 40, fighter2.health, 100)

        stdscr.addstr(6, 5, f"{fighter1.name}'s Turn:")
        stdscr.addstr(8, 5, "Press 'a' to attack, 's' for special move, or 'b' to block...")

        stdscr.refresh()

        # Handle player 1 input
        while True:
            key = stdscr.getch()
            if key == ord('a'):
                attack_damage = fighter1.attack(fighter2)
                stdscr.addstr(10, 5, f"{fighter1.name} attacks {fighter2.name} for {attack_damage} damage!")
                break
            elif key == ord('s'):
                attack_damage = fighter1.special_move(fighter2)
                stdscr.addstr(10, 5, f"{fighter1.name} performs a special move and deals {attack_damage} damage!")
                break
            elif key == ord('b'):
                fighter1.block()
                stdscr.addstr(10, 5, f"{fighter1.name} is blocking!")
                break

        if fighter2.health <= 0:
            break

        stdscr.addstr(12, 5, f"{fighter2.name}'s Turn:")
        stdscr.addstr(14, 5, "Press 'a' to attack, 's' for special move, or 'b' to block...")

        stdscr.refresh()

        # Opponent's turn
        stdscr.addstr(16, 5, opponent_turn(fighter2, fighter1))
        stdscr.refresh()
        time.sleep(1)

        if fighter1.health <= 0:
            break

        stdscr.refresh()
        time.sleep(1)

    stdscr.addstr(18, 5, "--- Battle Finished ---")
    stdscr.refresh()

    # Delay before showing the final result
    time.sleep(2)

    # Show the winner or tie message in the middle of the screen
    clear_screen(stdscr)
    if fighter1.health > 0:
        show_message(stdscr, f"{fighter1.name} wins!")
    elif fighter2.health > 0:
        show_message(stdscr, f"{fighter2.name} wins!")
    else:
        show_message(stdscr, "It's a tie!")

    stdscr.getch()  # Wait for user input before exiting

if __name__ == "__main__":
    curses.wrapper(main)
