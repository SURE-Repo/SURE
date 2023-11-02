def getVars(p):
    vars = {}
    p.sendline("where")
    p.expect("main\[1\]")
    raw_data = p.before.decode()
    temp = re.findall("\[(\d+)\]", raw_data)
    if len(temp) != 0:
        stack_height = temp[-1]
    else:
        stack_height = 0
    p.sendline("locals")
    p.expect("main\[1\]")
    raw_data = p.before.decode()
    for line in raw_data.split(os.linesep):
        equal_index = line.find("= ")
        if equal_index != -1:
            val_name = line[:equal_index - 1].strip()
            val_value = line[equal_index + 2:].strip()
            vars[val_name] = val_value
            if val_value.find("instance") != -1:
                p.sendline("dump " + val_name)
                p.expect("main\[1\]")
                temp = p.before.decode()
                if temp.find("= ") == -1:
                    vars[(val_name, stack_height)] = val_value
                else:
                    vars[(val_name, stack_height)] = temp[temp.find("= ")+2:]
    return vars