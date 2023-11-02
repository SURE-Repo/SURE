# "failed" is the list of failed test cases.
# "tech" is the name of a failure indexing technique.
# "r" is the actual number of faults.

def kmedoidsCluster(failed, tech, r):
    m = len(failed)

    read_distanceDict = {}
    distance_list = []
    #The distance information produced by the distance metric component of SURE
    table = xlrd.open_workbook('SURE_Dis/' + tech + '.csv').sheets()[0]
    row = table.nrows
    for key in range(row):
        read_distanceDict[table.row_values(key)[0]] = table.row_values(key)[1]

    distances = {}
    for i in range(row):
        distances[table.row_values(i)[0]] = table.row_values(i)[1]
    for i in range(m):
        for j in range(i+1,m):
            distance_list.append(distances['t' + str(int(failed[i])) + '_t' + str(int(failed[j]))])

    centroids = ['0', '1']  # determined by the mountain method in MSeer

    if len(centroids) != r:
        if len(centroids) > r:
            file = open('clusterAssment/' + tech + ' (medoids_over)' + '.txt', 'w')
            file.write(str(len(centroids)))
            file.close()
            return -1
        elif len(centroids) < r:
            file = open('clusterAssment/' + tech + ' (medoids_under)' + '.txt', 'w')
            file.write(str(len(centroids)))
            file.close()
            return -1

    print('centroids = ' + str(centroids))

    clusterAssment = mat(zeros((m, 2)))
    medoidsChanged_sign = True
    z = 1
    while medoidsChanged_sign:
        medoidsChanged_sign = False
        for i in range(m):
            minDist = inf
            minIndex = -1
            for j in range(r):
                distJI = read_distanceDict['t' + str(failed[i]) + '_t' + str(centroids[j])]

                if distJI < minDist:
                    minDist = distJI
                    minIndex = j

            clusterAssment[i, :] = failed[i], minIndex

        medoidsChanged_num = 0
        currentChanged = 0
        for cent in range(r):
            ptsInClust = np.array(failed)[nonzero(clusterAssment[:, 1].A == cent)[0]]

            sumMin = 0
            for otherPoint in ptsInClust:
                sumMin += read_distanceDict['t' + str(centroids[cent]) + '_t' + str(otherPoint)]

            for newMedoids_candidate in ptsInClust:
                sumReplace = 0
                for otherPoint in ptsInClust:
                    sumReplace += read_distanceDict['t' + str(newMedoids_candidate) + '_t' + str(otherPoint)]

                if sumReplace < sumMin:
                    sumMin = sumReplace
                    centroids[cent] = str(newMedoids_candidate)
                    medoidsChanged_sign = True
                    currentChanged = 1
            medoidsChanged_num += currentChanged
            currentChanged = 0
        print('Iteration: ' + str(z) + ', Changed Clusters: ' + str(medoidsChanged_num))
        z += 1


    f = xlsxwriter.Workbook('clusterAssment/' + tech + '.xls')
    sheet1 = f.add_worksheet(u'sheet1')
    [h, l] = clusterAssment.shape
    for i in range(h):
        for j in range(l):
            sheet1.write(i, j, clusterAssment[i, j])
    f.close()
    return clusterAssment


