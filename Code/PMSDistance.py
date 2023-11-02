# "failed" is the list of failed test cases.
def calDis(failed):
    m = len(failed)

    distance_dict = {}
    for i in range(0, m):
        for j in range(i + 1, m):
            img1 = 'memoryImage/10%/img/t' + str(failed[i]) + '.jpg'
            img2 = 'memoryImage/10%/img/t' + str(failed[j]) + '.jpg'

            image_1 = Image.open(img1)
            image_2 = Image.open(img2)

            probability = detect_image(image_1, image_2)
            dis = 1 - probability

            i1_size = image_1.size[0]
            i2_size = image_2.size[0]

            if i1_size == i2_size:
                sizediff = 1
            elif i1_size > i2_size:
                sizediff = i1_size / i2_size
            elif i2_size > i1_size:
                sizediff = i2_size / i1_size

            distance_dict['t' + str(failed[i]) + '_' + 't' + str(failed[j])] = dis * sizediff

    new_distance_dict = copy.deepcopy(distance_dict)
    for i in range(0, m):
        new_distance_dict['t' + str(failed[i]) + '_' + 't' + str(failed[i])] = 0
        for j in range(i + 1, m):
            new_distance_dict['t' + str(failed[j]) + '_' + 't' + str(failed[i])] = \
                distance_dict['t' + str(failed[i]) + '_' + 't' + str(failed[j])]

    f = xlsxwriter.Workbook('SURE_Dis/PMS.csv')
    sheet1 = f.add_worksheet(u'sheet1')
    dict_row = 0
    for k, v in new_distance_dict.items():
        sheet1.write(dict_row, 0, k)
        sheet1.write(dict_row, 1, v)
        dict_row += 1
    f.close()
