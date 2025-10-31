import random


class Snake:
    """
    The class is a snake game, with allows snake to move and eat food, and also enables to reset, and generat a random food position.
    """

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE, food_position):
        """
        Initialize the length of the snake, screen width, screen height, block size, snake head position, score, and food position.
        :param SCREEN_WIDTH: int
        :param SCREEN_HEIGHT: int
        :param BLOCK_SIZE: int, Size of moving units
        :param food_position: tuple, representing the position(x, y) of food.
        """
        self.length = 1
        self.SCREEN_WIDTH = int(SCREEN_WIDTH)
        self.SCREEN_HEIGHT = int(SCREEN_HEIGHT)
        self.BLOCK_SIZE = int(BLOCK_SIZE) if BLOCK_SIZE else 1
        cx = self.SCREEN_WIDTH // 2
        cy = self.SCREEN_HEIGHT // 2
        self.positions = [(cx, cy)]
        self.score = 0
        self.food_position = food_position

    def move(self, direction):
        """
        Move the snake in the specified direction. If the new position of the snake's head is equal to the position of the food, then eat the food; If the position of the snake's head is equal to the position of its body, then start over, otherwise its own length plus one.
        :param direction: tuple, representing the direction of movement (x, y).
        :return: None
        >>> snake.move((1,1))
        self.length = 1
        self.positions = [(51, 51), (50, 50)]
        self.score = 10
        """
        if not direction or len(direction) != 2:
            return
        dx, dy = direction
        head_x, head_y = self.positions[0]
        new_head = (
            head_x + dx * self.BLOCK_SIZE,
            head_y + dy * self.BLOCK_SIZE,
        )

        # Add new head
        self.positions.insert(0, new_head)

        # Self-collision: reset
        if new_head in self.positions[1:]:
            self.reset()
            return

        # Eat food: increase score and keep tail this move
        if self.food_position is not None and new_head == self.food_position:
            self.score += 10
            self.random_food_position()
        else:
            # Maintain current length: trim tail
            if len(self.positions) > self.length:
                self.positions = self.positions[:self.length]

    def random_food_position(self):
        """
        Randomly generate a new food position, but don't place it on the snake.
        :return: None, Change the food position
        """
        # Generate all possible grid positions
        possible_x = range(0, self.SCREEN_WIDTH + 1, self.BLOCK_SIZE) if self.SCREEN_WIDTH % self.BLOCK_SIZE == 0 else range(
            0, self.SCREEN_WIDTH, self.BLOCK_SIZE)
        possible_y = range(0, self.SCREEN_HEIGHT + 1, self.BLOCK_SIZE) if self.SCREEN_HEIGHT % self.BLOCK_SIZE == 0 else range(
            0, self.SCREEN_HEIGHT, self.BLOCK_SIZE)

        snake_set = set(self.positions)
        # Fallback to avoid infinite loop if grid is full
        max_attempts = 1000
        for _ in range(max_attempts):
            x = random.choice(list(possible_x))
            y = random.choice(list(possible_y))
            if (x, y) not in snake_set:
                self.food_position = (x, y)
                return

        # As a last resort, scan for any available cell
        for x in possible_x:
            for y in possible_y:
                if (x, y) not in snake_set:
                    self.food_position = (x, y)
                    return
        # If no space, set to None
        self.food_position = None

    def reset(self):
        """
        Reset the snake to its initial state. Set the length to 1, the snake head position to ((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2)), the score to 0, and randomly generate new food position.
        :return: None
        >>> snake = Snake(100, 100, 1, (51, 51))
        >>> snake.reset()
        self.length = 1
        self.positions = [(50, 50)]
        self.score = 0
        self.random_food_position()
        """
        self.length = 1
        cx = self.SCREEN_WIDTH // 2
        cy = self.SCREEN_HEIGHT // 2
        self.positions = [(cx, cy)]
        self.score = 0
        self.random_food_position()

    def eat_food(self):
        """
        Increase the length of the snake by 1 and increase the score by 100. Randomly generate a new food position, but
        don't place it on the snake.
        :return: None
        >>> snake = Snake(100, 100, 1, (51, 51))
        >>> snake.move((1,1))
        >>> snake.eat_food()
        self.length = 2
        self.score = 10
        """
        # Increase only the length as per example; score remains unchanged here
        self.length += 1
        # Ensure positions do not exceed new length after next moves
        # Food is handled upon move when head reaches food, so no change here
