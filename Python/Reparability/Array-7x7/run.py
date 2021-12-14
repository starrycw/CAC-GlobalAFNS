import ReparabilitySimu_Functions as rsfunction

#############################################
# Configuration

n_f = 5  # 故障数目
#############################################

f_list = []
for n_f_i in range(0, n_f):
    f_list.append(n_f_i)

result_01 = [0, 0, 0]
result_02 = [0, 0, 0]
result_03 = [0, 0, 0]
result_04 = [0, 0, 0]
result_05 = [0, 0, 0]

while f_list != -1:
    result_01[0] = result_01[0] + 1
    result_02[0] = result_02[0] + 1
    result_03[0] = result_03[0] + 1
    result_04[0] = result_04[0] + 1
    result_05[0] = result_05[0] + 1
    f_array = rsfunction.get_f_array(seeds=tuple(f_list))

    if rsfunction.check_01(f_array=f_array):
        result_01[1] = result_01[1] + 1
        flag_01 = True
    else:
        result_01[2] = result_01[2] + 1
        flag_01 = False

    if rsfunction.check_02(f_array=f_array):
        result_02[1] = result_02[1] + 1
        flag_02 = True
    else:
        result_02[2] = result_02[2] + 1
        flag_02 = False

    if rsfunction.check_03(f_array=f_array):
        result_03[1] = result_03[1] + 1
        flag_03 = True
    else:
        result_03[2] = result_03[2] + 1
        flag_03 = False

    if rsfunction.check_04(f_array=f_array):
        result_04[1] = result_04[1] + 1
        flag_04 = True
    else:
        result_04[2] = result_04[2] + 1
        flag_04 = False

    if rsfunction.check_05(f_array=f_array):
        result_05[1] = result_05[1] + 1
        flag_05 = True
    else:
        result_05[2] = result_05[2] + 1
        flag_05 = False

    print("faults:{}, 01-{}, 02-{}, 03-{}, 04-{}, 05-{}".format(f_list, flag_01, flag_02, flag_03, flag_04, flag_05))

    f_list = rsfunction.get_next_location(n_f = n_f, current_list=f_list)



print(result_01, result_02, result_03, result_04, result_05)