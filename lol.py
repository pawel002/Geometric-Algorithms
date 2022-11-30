import numpy as np
# write rows in row echelon form
def upper_triangular(M):
    # move all zeros to buttom of matrix
    M = np.concatenate((M[np.any(M != 0, axis=1)], M[np.all(M == 0, axis=1)]), axis=0)

    # iterate over matrix rows
    for i in range(0, M.shape[0]):
        print(np.array2string(M, separator=" & ", ))
        print()
        # initialize row-swap iterator
        j = 1

        # select pivot value
        pivot = M[i][i]

        # find next non-zero leading coefficient
        while pivot == 0 and i + j < M.shape[0]:
            # perform row swap operation
            M[[i, i + j]] = M[[i + j, i]]

            # incrememnt row-swap iterator
            j += 1

            # get new pivot
            pivot = M[i][i]

        # if pivot is zero, remaining rows are all zeros
        if pivot == 0:
            # return upper triangular matrix
            return M

        # extract row
        row = M[i]

        # get 1 along the diagonal
        M[i] = row / (1.0 * pivot)

        # iterate over remaining rows
        for j in range(i + 1, M.shape[0]):
            # subtract current row from remaining rows
            M[j] = M[j] - M[i] * M[j][i]

    # return upper triangular matrix
    return M


X = np.array([[1.,2.,3.,4.], [-4., 2., 15., 2.], [3., 1., 6., 5.], [2., 10., -5., 1.]])
print(upper_triangular(X))