class Gamestats:
    """Track stats for Alien Invasion."""

    def __init__(self):
        """Initialize statistics"""
        self.score = 0
        # High score never resets.
        self.get_high_score()

    def get_high_score(self):
        """Read the high score from the file in a correct manner"""
        f = open("high_score.txt", "r")
        high_score = str(f.read())
        self.high_score = high_score.split()
        for x in range(len(self.high_score)):
            self.high_score[x] = int(self.high_score[x])

    def write_high_score(self):
        """Convert the high score list back into file format, to be saved between games"""
        high_score = open("high_score.txt", "w")
        write_out = ""
        for x in range(len(self.high_score)):
            write_out += (str(self.high_score[x]) + ' ')
        high_score.write(write_out)

    def increment_score(self):
        self.score += 1
        for x in range(len(self.high_score)):
            if self.score>self.high_score[x]:
                self.high_score[x] = self.score
                break

