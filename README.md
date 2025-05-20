Purpose:
This project implements a Sparse Matrix in Python — a data structure optimized to store and manipulate large matrices that mostly contain zero values.

Features and Methods

getElement(row, col):
Returns the value at the specified position. If no value is stored there, returns 0.

setElement(row, col, value):
Stores or updates the value if it is non-zero.

If the value is zero, it removes the entry (to keep the matrix sparse).

add(other_matrix):
Returns a new sparse matrix that is the result of adding the current matrix and another.

subtract(other_matrix):
Returns a new sparse matrix that is the result of subtracting another matrix from the current one.

multiply(other_matrix):
Performs matrix multiplication between two sparse matrices. Follows standard matrix multiplication rules and skips zero values to improve efficiency.

toFile(filepath):
Writes the matrix to a .txt file in the same format it was originally read from.

Main Function:
The main() function provides a basic command-line interface:

(1)Prompts the user to choose an operation (add, subtract, or multiply).

(2)Asks for file paths to two input matrices.

(3)Loads the matrices, performs the chosen operation, and saves the result to a file.