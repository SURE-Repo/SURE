def toAscii(inputStr):
    outputAscii = 0
    for i in range(len(inputStr)):
        outputAscii += (i + 1) * ord(inputStr[i])
    return outputAscii

def singleVersion(dbfile):

    # =================
    bp_threshold = '10%'
    bp_threshold_num = 0.1

    if not os.path.exists("memoryImage"):
        os.mkdir("memoryImage")
    if not os.path.exists("memoryImage/" + bp_threshold):
        os.mkdir("memoryImage/" + bp_threshold)
    if not os.path.exists("memoryImage/" + bp_threshold + "/img"):
        os.makedirs("memoryImage/" + bp_threshold + "/img")

    failed_list = []
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    sql = "select id from testcase where all_result = '1'"
    cursor.execute(sql)
    for c in cursor:
        failed_list.append(c[0])


    breakpoint_id = []
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    sql = "select id from breakpoint"
    cursor.execute(sql)
    for c in cursor:
        breakpoint_id.append(c[0])


    thre = int(len(breakpoint_id) * bp_threshold_num)


    metaData = np.zeros((len(failed_list), 3))
    metaData_index = 0


    memory_pkl = {}


    sql = "select bp_id, val from bp_tc where tc_id = ?"
    for failed in failed_list:
        failed_memory = []
        cursor = conn.cursor()
        cursor.execute(sql, [failed])

        bp_exec = 0
        for c in cursor:

            if c[0] <= thre:
                bp_exec += 1
                dict = eval(c[1])
                for key, value in list(dict.items()):
                    failed_memory.append(key[0])
                    failed_memory.append(value)
                    failed_memory.append(key[1])

        failed_len = int(len(failed_memory) / 3)


        if failed_len == 0:

            rgb_Matrix = np.zeros((1, 1, 3), dtype=np.uint8)
            memory_pkl['t' + str(failed)] = rgb_Matrix
            imageio.imsave('memoryImage/' + bp_threshold + '/img/t' + str(failed) + '.jpg', rgb_Matrix)

            metaData[metaData_index, :] = bp_exec, failed_len, 0
            metaData_index += 1
            continue

        varsName_ori = [failed_memory[i] for i in range(0, len(failed_memory), 3)]
        varsValue_ori = [failed_memory[i] for i in range(1, len(failed_memory), 3)]
        varsFrame_ori = [failed_memory[i] for i in range(2, len(failed_memory), 3)]

        varsName_asc = []
        varsValue_asc = []

        for i in range(failed_len):
            varsName_asc.append(toAscii(varsName_ori[i]))
            varsValue_asc.append(toAscii(varsValue_ori[i]))

        varsName_norm = []
        Max_varsName = max(varsName_asc)
        Min_varsName = min(varsName_asc)
        Div_varsName = Max_varsName - Min_varsName

        varsValue_norm = []
        Max_varsValue = max(varsValue_asc)
        Min_varsValue = min(varsValue_asc)
        Div_varsValue = Max_varsValue - Min_varsValue

        varsFrame_norm = []
        Max_varsFrame = max(varsFrame_ori)
        Min_varsFrame = min(varsFrame_ori)
        Div_varsFrame = Max_varsFrame - Min_varsFrame

        for i in range(failed_len):

            if Div_varsName != 0:
                k_name = (255 - 1) / Div_varsName
                normResult_Name = 1 + k_name * (varsName_asc[i] - Min_varsName)
                varsName_norm.append(normResult_Name)
            else:
                varsName_norm.append(1)


            if Div_varsValue != 0:
                k_value = (255 - 1) / Div_varsValue
                normResult_Value = 1 + k_value * (varsValue_asc[i] - Min_varsValue)
                varsValue_norm.append(normResult_Value)
            else:
                varsValue_norm.append(1)


            if Div_varsFrame != 0:
                k_frame = (255 - 1) / Div_varsFrame
                normResult_Frame = 1 + k_frame * (varsFrame_ori[i] - Min_varsFrame)
                varsFrame_norm.append(normResult_Frame)
            else:
                varsFrame_norm.append(1)


        length = math.ceil(math.sqrt(failed_len))
        depth = 3

        rgb_Matrix = np.zeros((length, length, depth), dtype = np.uint8)
        index = 0
        for i in range(length):
            for j in range(length):
                if index < failed_len:
                    rgb_Matrix[j, i, :] = [varsName_norm[index], varsValue_norm[index], varsFrame_norm[index]]
                    index += 1

        memory_pkl['t' + str(failed)] = rgb_Matrix
        imageio.imsave('memoryImage/' + bp_threshold + '/img/t' + str(failed) + '.jpg', rgb_Matrix)

        metaData[metaData_index, :] = bp_exec, failed_len, length
        metaData_index += 1