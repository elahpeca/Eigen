class MatrixData:
    """
    Represents matrix data.

    Stores the matrix in a 2D list and provides methods
    for updating cell values.
    """
    def __init__(self, rows, cols):
        """
        Initializes a MatrixData object.

        Args:
            rows (int): Number of rows in the matrix.
            cols (int): Number of columns in the matrix.
        """
        self.rows = rows
        self.cols = cols
        self.data = [[None] * cols for _ in range(rows)]

    def update_value(self, row, col, value):
        """
        Updates the value at a specific cell in the matrix.

        Args:
            row (int): Row index.
            col (int): Column index.
            value (str): New value for the cell.
        """
        try:
            self.data[row][col] = float(value) if value else None
        except ValueError:
            pass

    def resize(self, new_rows, new_cols):
        """
        Resizes the matrix data, preserving existing values.

        Args:
            new_rows (int): New number of rows.
            new_cols (int): New number of columns.
        """
        if new_rows > self.rows:
            self.data.extend([[None] * self.cols for _ in range(new_rows - self.rows)])
        elif new_rows < self.rows:
            self.data = self.data[:new_rows]

        for row in self.data:
            if new_cols > self.cols:
                row.extend([None] * (new_cols - self.cols))
            elif new_cols < self.cols:
                row[:] = row[:new_cols]

        self.rows = new_rows
        self.cols = new_cols
