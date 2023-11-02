def Formula_DStar(table_sum, exline):
    ranking = zeros((exline, 3))
    i = 0
    for line in table_sum:
        line = mat(line).flatten().A[0]
        ranking[i, 1] = line[0]
        fz = pow(line[2], 2)
        fm = line[4] + line[1]
        ranking[i, 2] = fz / fm

        i += 1
    ranking = ranking[ranking[:, 2].argsort()[::-1]]
    for i in range(0, exline):
        ranking[i, 0] = i + 1
    return ranking

