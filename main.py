import numpy as np

def separate_matrix(matrix: np.ndarray, split_column: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Separates a matrix into two submatrices based on the specified column index.
    :param matrix: The input matrix.
    :param split_column: The column index where the separation occurs.
    :return: A tuple containing two submatrices.
    """
    if split_column < 0 or split_column >= matrix.shape[1]:
        raise ValueError("Invalid split column index")

    left_matrix = matrix[:, :split_column + 1]
    right_matrix = matrix[:, split_column + 1:]

    return left_matrix, right_matrix

# Example usage:
original_matrix = np.array([[1, 2, 3],
                            [4, 5, 6],
                            [7, 8, 9]])

split_column_index = 0
left_submatrix, right_submatrix = separate_matrix(original_matrix, split_column_index)

print("Original Matrix:")
print(original_matrix)

print("\nLeft Submatrix:")
print(left_submatrix)

print("\nRight Submatrix:")
print(right_submatrix)