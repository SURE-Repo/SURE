# collect the MIs of defects4j
def collect_defects4j(db, class_path, failed_testcases, break_points):
    mem_data = []

    for i in range(len(failed_testcases)):
        finalPointPos = testCase.rfind(".")

        testCase = failed_testcases[i]

        shell_command = 'jdb ' + class_path + ' SingleJUnitTestRunner ' + \
            testCase[:finalPointPos] + '#' + testCase[finalPointPos + 1:]

        p = pexpect.spawn(shell_command)

        p.expect('>')
        output = p.before.decode()

        p.sendline("run")
        index = p.expect("main\[1\]")

        output = p.before.decode()

        for bp in break_points.keys():
            p.sendline("stop at " + bp)
            p.expect("main\[1\]")
            output = p.before.decode()

        p.sendline("cont")
        index = p.expect("main\[1\]")
        output = p.before.decode()
        while True:
            className = output[output.find(",") + 2:output.rfind(".")]
            line_pos = output.rfind("line=")
            lineNum = output[line_pos+5:output.rfind("bci")]

            bp_pos = className + ":" + str(locale.atoi(lineNum))

            p.sendline("step")
            index = p.expect("main\[1\]")
            output = p.before.decode()

            val = getVars(p)

            mem_data.append((i+1, bp_pos, break_points[bp_pos], str(val)))

            if output.find("Breakpoint hit") != -1:
                continue
            else:
                p.sendline("cont")
                index = p.expect("main\[1\]")
                output = p.before.decode()

            p.sendline("cont")
            index = p.expect("main\[1\]")
            if index != 0:
                break
            output = p.before.decode()

    sqlcmd = "insert into bp_tc(tc_id, lineNumber, bp_id, val) values (?, ?, ?, ?);"
    db.executeMany(sqlcmd, mem_data)
    db.closeDB()

# collect the MIs of SIR
def collect_SIR(db, gdb, Testcase, selected_exLines, selected_suspiciousValues):
    for line_num in selected_exLines:
        output = gdb.question("b " + '%d' % (int(line_num)))

    output = gdb.question("info b")

    db.insertBreakpoint(output, selected_exLines, selected_suspiciousValues)

    memory_data_list = []

    for tc_num in sorted(Testcase.testcases):
        testcase = Testcase.testcases.get(tc_num)
        count += 1

        gdb.question(testcase.invocation)
        gdb.child.fromchild.readline()

        output = gdb.question(testcase.invocation)

        gdb.child.fromchild.readline()
        while output.find("\nBreakpoint ") != -1:
            s2 = output[output.find("\nBreakpoint "):output.find(
                ",", output.find("\nBreakpoint"))]
            s2 = int(s2.split(" ")[1])
            next_bp = gdb.question("next")
            state = gdb.state()
            memory_data_list.append(
                (s2, selected_exLines[s2 - 1], tc_num, str(state)))
            if next_bp.find("Breakpoint") != -1:
                output = next_bp
            else:
                output = gdb.question("c")

    sqlcmd = "insert into bp_tc(bp_id, lineNumber, tc_id, val) values (?, ?, ?, ?);"
    db.executemany_sql(sqlcmd, memory_data_list)
