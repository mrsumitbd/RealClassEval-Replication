class Cube:
    """
    A Rubik's cube implementation with accurate move handling.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset the cube to solved state"""
        self.cube = [[[UP_COLOR for _ in range(3)] for _ in range(3)], [[DOWN_COLOR for _ in range(3)] for _ in range(3)], [[LEFT_COLOR for _ in range(3)] for _ in range(3)], [[RIGHT_COLOR for _ in range(3)] for _ in range(3)], [[FRONT_COLOR for _ in range(3)] for _ in range(3)], [[BACK_COLOR for _ in range(3)] for _ in range(3)]]

    def is_solved(self) -> bool:
        """Check if the cube is solved"""
        for face in self.cube:
            center_color = face[1][1]
            for row in face:
                for color in row:
                    if color != center_color:
                        return False
        return True

    def count_solved_cubies(self) -> float:
        """
        Count the number of stickers in their correct position
        Returns a normalized score between 0 and 1
        """
        reference = Cube()
        total_stickers = 6 * 9
        match_count = 0
        for face_idx in range(6):
            for i in range(3):
                for j in range(3):
                    if self.cube[face_idx][i][j] == reference.cube[face_idx][i][j]:
                        match_count += 1
        return match_count / total_stickers

    def rotate(self, move: str):
        """
        Perform a move on the cube using standard notation
        U, D, L, R, F, B are clockwise rotations of respective faces
        U', D', L', R', F', B' are counterclockwise rotations
        U2, D2, L2, R2, F2, B2 are double (180°) rotations
        """
        face_map = {'U': 0, 'D': 1, 'L': 2, 'R': 3, 'F': 4, 'B': 5}
        if len(move) == 0:
            raise ValueError('Empty move')
        face = move[0]
        if face not in face_map:
            raise ValueError(f'Invalid face: {face}')
        face_idx = face_map[face]
        if len(move) == 1:
            count = 1
        elif len(move) == 2:
            if move[1] == "'":
                count = 3
            elif move[1] == '2':
                count = 2
            else:
                raise ValueError(f'Invalid move modifier: {move[1]}')
        else:
            raise ValueError(f'Invalid move format: {move}')
        for _ in range(count):
            self._rotate_face_clockwise(face_idx)
            self._rotate_adjacent_faces(face_idx)

    def _rotate_face_clockwise(self, face_idx: int):
        """Rotate a face clockwise"""
        face = self.cube[face_idx]
        new_face = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                new_face[j][2 - i] = face[i][j]
        self.cube[face_idx] = new_face

    def _rotate_adjacent_faces(self, face_idx: int):
        """Rotate the appropriate edges on adjacent faces"""
        if face_idx == 0:
            temp = self.cube[4][0][:]
            self.cube[4][0] = self.cube[2][0][:]
            self.cube[2][0] = self.cube[5][0][:]
            self.cube[5][0] = self.cube[3][0][:]
            self.cube[3][0] = temp
        elif face_idx == 1:
            temp = self.cube[4][2][:]
            self.cube[4][2] = self.cube[3][2][:]
            self.cube[3][2] = self.cube[5][2][:]
            self.cube[5][2] = self.cube[2][2][:]
            self.cube[2][2] = temp
        elif face_idx == 2:
            temp = [self.cube[0][i][0] for i in range(3)]
            for i in range(3):
                self.cube[0][i][0] = self.cube[5][2 - i][2]
            for i in range(3):
                self.cube[5][i][2] = self.cube[1][2 - i][0]
            for i in range(3):
                self.cube[1][i][0] = self.cube[4][i][0]
            for i in range(3):
                self.cube[4][i][0] = temp[i]
        elif face_idx == 3:
            temp = [self.cube[0][i][2] for i in range(3)]
            for i in range(3):
                self.cube[0][i][2] = self.cube[4][i][2]
            for i in range(3):
                self.cube[4][i][2] = self.cube[1][i][2]
            for i in range(3):
                self.cube[1][i][2] = self.cube[5][2 - i][0]
            for i in range(3):
                self.cube[5][i][0] = temp[2 - i]
        elif face_idx == 4:
            temp = self.cube[0][2][:]
            for i in range(3):
                self.cube[0][2][i] = self.cube[2][2 - i][2]
            for i in range(3):
                self.cube[2][i][2] = self.cube[1][0][i]
            for i in range(3):
                self.cube[1][0][i] = self.cube[3][2 - i][0]
            for i in range(3):
                self.cube[3][i][0] = temp[i]
        elif face_idx == 5:
            temp = self.cube[0][0][:]
            for i in range(3):
                self.cube[0][0][i] = self.cube[3][2 - i][2]
            for i in range(3):
                self.cube[3][i][2] = self.cube[1][2][i]
            for i in range(3):
                self.cube[1][2][i] = self.cube[2][2 - i][0]
            for i in range(3):
                self.cube[2][i][0] = temp[i]

    def __str__(self) -> str:
        """Convert cube to string representation"""
        face_names = ['U', 'D', 'L', 'R', 'F', 'B']
        result = []
        for i, face in enumerate(self.cube):
            result.append(f"{face_names[i]}: {' '.join(face[0])}")
            result.append(f"   {' '.join(face[1])}")
            result.append(f"   {' '.join(face[2])}")
        return '\n'.join(result)