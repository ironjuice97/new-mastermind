import turtle as t
from Marble import Marble
from Point import Point
from random import shuffle
from os import system, path

# Check and create a leaderboard file if it doesn't exist.
leaderboard_file = "leaderboard.txt"
if not path.exists(leaderboard_file):
    open(leaderboard_file, "x").close()

# Function to prompt the player for their name using a text input dialog.
def get_player_name():
    return t.textinput("Player Name", "Enter your name:")

# Store the player's name returned by the get_player_name function.
player_name = get_player_name()

def draw_color_pickers():
    color_picker_turtle.clear()  # Clear existing pickers before redrawing
    xpos = -250  # Starting position for color pickers
    ypos = -300  # Vertical position for color pickers

    for color in display_colors:
        color_picker_turtle.goto(xpos, ypos)
        color_picker_turtle.pendown()

        # Draw the outline
        color_picker_turtle.pencolor("black")
        color_picker_turtle.circle(15)

        # Fill the color if it's still available
        if color in available_colors_per_row[current_row]:
            color_picker_turtle.fillcolor(color)
            color_picker_turtle.begin_fill()
            color_picker_turtle.circle(15)
            color_picker_turtle.end_fill()
        else:
            pass  # Do nothing or implement some logic for unavailable colors

        color_picker_turtle.penup()
        xpos += 50  # Increment xpos for next color picker

        wn.update()  # Manually update the screen


# Set up the main window for the game using turtle graphics.
wn = t.Screen()
wn.title("Mastermind")
wn.bgcolor("white")
wn.setup(height=700, width=700)

# Add this line to register the check button image
wn.addshape("checkbutton.gif")
wn.addshape("xbutton.gif")  # Register the xbutton shape
wn.addshape("quit.gif")
wn.addshape("quitmsg.gif")
wn.addshape("winner.gif")

# Create a Turtle for the check button
check_button = t.Turtle()
check_button.shape("checkbutton.gif")  # Ensure 'checkbutton.gif' is in the same directory
check_button.penup()
check_button.goto(0, -300)  # Adjust the position as needed

# Create a Turtle for the quit button
quit_button = t.Turtle()
quit_button.shape("quit.gif")
quit_button.penup()
quit_button.goto(250, -250)  # Adjust the position as needed

# Function to be called when quit button is clicked
def on_quit_click(x, y):
    # Show the quit message popup
    quitmsg_turtle = t.Turtle()
    quitmsg_turtle.shape("quitmsg.gif")  # Ensure 'quitmsg.gif' is in the same directory
    quitmsg_turtle.penup()
    quitmsg_turtle.goto(0, 0)  # Position the quit message popup
    # Here you can wait for a click to close the message and quit the game
    # or you can directly close the game window using wn.bye()

# Bind the click event to the quit button
quit_button.onclick(on_quit_click)

# Function to append a player's name and score to the leaderboard file.
def update_leaderboard(name, score):
    with open(leaderboard_file, "a") as file:
        file.write(f"{name},{score}\n")

# Function to read the leaderboard file and return a sorted list of scores.
def read_leaderboard():
    with open(leaderboard_file, "r") as file:
        lines = file.readlines()
    leaderboard = [line.strip().split(",") for line in lines]
    leaderboard.sort(key=lambda x: int(x[1]))
    return leaderboard

# Function to display the top scores from the leaderboard on the screen.
def display_leaderboard():
    leaderboard = read_leaderboard()
    leaderboard_display = t.Turtle()
    leaderboard_display.ht()
    leaderboard_display.penup()
    leaderboard_display.goto(wn.window_width() / 3, wn.window_height() / 2 - 100)
    leaderboard_display.write("Top Scores:", align="right", font=("Arial", 16, "bold"))
    y_pos = wn.window_height() / 2 - 130
    for i, (name, score) in enumerate(leaderboard[:5]):
        leaderboard_display.goto(wn.window_width() / 4, y_pos - (20 * i))
        leaderboard_display.write(f"{i + 1}. {name} - {score}", align="right", font=("Arial", 12, "normal"))

# Display the leaderboard.
display_leaderboard()

# Initialize global variables for tracking the current game state.
current_row = 0
current_col = 0
gameover = False
ans_count = 1  # Number of attempts
ans_limit = 10

# Initialize the list of colors for secret code
colors = ["blue", "red", "green", "yellow", "purple", "black"]
display_colors = colors.copy()  # Copy of colors for display

# Global declaration of available_colors_per_row
available_colors_per_row = [colors.copy() for _ in range(10)]  # Assuming 10 rows

# Shuffle the list of colors and select the first four as the secret code.
shuffled_colors = colors.copy()
shuffle(shuffled_colors)
code = shuffled_colors[:4]  # Secret code

# Initialize lists for storing the guess and indicator marbles.
guess_marbles = []
indicator_marbles = []

# Create and display the guess and indicator marbles for each row.
for row in range(10):  # Assuming 10 rows
    row_guess_marbles = []
    row_indicator_marbles = []
    for col in range(4):  # Assuming 4 guesses per row
        # Position and create guess marble
        guess_position = Point(-250 + col * 50, 210 - row * 50)
        guess_marble = Marble(guess_position, "grey", 15)
        row_guess_marbles.append(guess_marble)
        guess_marble.draw_empty()

    # Position and create indicator marbles in a 2x2 grid
    for i in range(2):  # Two columns of indicators
        for j in range(2):  # Two rows of indicators
            # Calculate the position for each indicator marble
            indicator_x = 2 + i * 15  # Horizontal spacing of 15 units
            indicator_y = 225 - row * 50 - j * 15  # Vertical spacing of 15 units
            indicator_position = Point(indicator_x, indicator_y)
            indicator_marble = Marble(indicator_position, "white", 5)
            row_indicator_marbles.append(indicator_marble)
            indicator_marble.draw_empty()

    guess_marbles.append(row_guess_marbles)
    indicator_marbles.append(row_indicator_marbles)

# Draw color pickers for player selection at the bottom of the screen.
color_picker_turtle = t.Turtle()
color_picker_turtle.hideturtle()
color_picker_turtle.speed(0)  # Set turtle speed to the fastest
color_picker_turtle.penup()
xpos = -250  # Starting position for color pickers
ypos = -300  # Vertical position for color pickers

# Call draw_color_pickers initially to draw the color pickers for the first time
draw_color_pickers()

# Function to be called when check button is clicked
def on_check_click(x, y):
    global current_col, current_row, gameover
    if current_col == 4:  # Ensure 4 colors have been picked
        check_guess()
        if not gameover:  # Prepare for the next guess if the game is not over
            current_row += 1
            current_col = 0
            if current_row < 10:  # Check if the new row is within bounds
                available_colors_per_row[current_row] = colors.copy()
                draw_color_pickers()  # Redraw color pickers for the next row
        # Handle game over logic here if needed

# Bind the click event to the check button
check_button.onclick(on_check_click)

# Create a Turtle for the X button
x_button = t.Turtle()
x_button.shape("xbutton.gif")  # Ensure 'xbutton.gif' is in the same directory
x_button.penup()
x_button.goto(50, -300)  # Adjust the position as needed

# Function to be called when X button is clicked
def on_x_click(x, y):
    global current_col
    if current_col > 0:  # Check if there are any guesses to remove
        current_col -= 1  # Move back one column
        last_color = guess_marbles[current_row][current_col].get_color()
        guess_marbles[current_row][current_col].set_color("grey")  # Reset the color of the marble
        guess_marbles[current_row][current_col].draw_empty()  # Redraw the marble as empty

        # Add the removed color back to available colors
        if last_color not in available_colors_per_row[current_row]:
            available_colors_per_row[current_row].append(last_color)

        # Redraw the color pickers for the current row
        draw_color_pickers()

# Bind the click event to the X button
x_button.onclick(on_x_click)

# Function to show winner message when the player wins
def show_winner_message():
    winner_turtle = t.Turtle()
    winner_turtle.shape("winner.gif")  # Ensure 'winner.gif' is in the same directory
    winner_turtle.penup()
    winner_turtle.goto(0, 0)  # Position the winner message popup
    # You may want to pause the game here and wait for a click or set a timer to close the winner message

# Define the check_guess function
def check_guess():
    global current_row, gameover, ans_count
    guess = [marble.get_color() for marble in guess_marbles[current_row]]
    print(f"Current guess: {guess}")  # Debugging print statement
    print(f"Secret code: {code}")  # Debugging print statement
    black, red = 0, 0
    code_copy = code[:]

    # First pass for black indicators (correct color and position).
    for i in range(4):
        if guess[i] == code[i]:
            black += 1
            code_copy[i] = None

    # Second pass for white indicators (correct color, wrong position).
    for i in range(4):
        if guess[i] in code_copy and guess[i] != code[i]:
            red += 1
            code_copy[code_copy.index(guess[i])] = None

    # Debugging: Print the results of this guess
    print(f"Black indicators: {black}, Red indicators: {red}")

    # Update indicator marbles based on black and red counts.
    for i in range(4):
        if i < black:
            indicator_marbles[current_row][i].set_color("black")
        elif i < black + red:
            indicator_marbles[current_row][i].set_color("red")
        else:
            indicator_marbles[current_row][i].draw_empty()
        indicator_marbles[current_row][i].draw()

    # Update game state after each guess.
    ans_count += 1

    # Check win or lose conditions.
    if black == 4:  # All four pegs are black, the guess is correct
        gameover = True
        update_leaderboard(player_name, ans_count)  # Update leaderboard on win
        show_winner_message()  # Show the winner message
        # You can add a delay or wait for a click to continue after showing the winner message
    elif ans_count > ans_limit:
        gameover = True
        # Display lose message (implementation not shown)

    wn.update()

def clk(x, y):
    global current_col, current_row, gameover, ans_count, available_colors_per_row

    if gameover:
        return

    xpos = -250  # Starting position for color pickers
    color_picker_width = 50  # Width between color pickers

    for index, color in enumerate(display_colors):
        if xpos <= x <= xpos + color_picker_width and -315 <= y <= -285:
            if current_col < 4 and color in available_colors_per_row[current_row]:
                print(f"Color clicked: {color}")

                # Set the color of the current guess marble and draw it
                guess_marbles[current_row][current_col].set_color(color)
                guess_marbles[current_row][current_col].draw()

                # Remove the selected color from available choices for this row
                available_colors_per_row[current_row].remove(color)

                # Redraw the color pickers for the current row
                draw_color_pickers()

                current_col += 1
            break
        xpos += color_picker_width

    # Enter button logic - submit guess and check it.
    if 105 < x < 175 and 245 < y < 275 and not gameover:
        if current_col == 4:  # Ensure all 4 marbles are colored
            check_guess()  # Check the player's guess

            # Move to the next row and reset available colors for the new row
            current_row += 1
            current_col = 0
            if current_row < 10:  # Check if the new row is within bounds
                available_colors_per_row[current_row] = colors.copy()

    # Reset button logic - restart or exit the game.
    if 110 < x < 175 and -207 < y < -188:
        wn.bye()
        system("Mastermind.py")  # Restart the game script

    wn.update()  # Manually update the screen

# Set up turtle to listen for mouse clicks.
t.onscreenclick(clk)
t.listen()
t.done()  # Keep the window open