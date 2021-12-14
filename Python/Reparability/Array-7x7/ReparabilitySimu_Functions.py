import copy


def get_next_location(n_f, current_list):
    inc_idx = n_f - 1
    while current_list[inc_idx] == 49 - n_f + inc_idx:
        inc_idx = inc_idx - 1
        if inc_idx == -1:
            return -1
    new_list = []
    for ii in range(0, inc_idx):
        new_list.append(current_list[ii])
    new_list.append(current_list[inc_idx] + 1)
    for ii in range(inc_idx + 1, n_f):
        new_list.append(new_list[-1] + 1)
    assert len(new_list) == n_f
    return copy.deepcopy(new_list)



def get_f_array(seeds):
    assert isinstance(seeds, tuple)
    f_array = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ]
    for seed_i in seeds:
        assert seed_i in range(0, 49)
        seed_i_x = seed_i // 7
        seed_i_y = seed_i % 7
        assert f_array[seed_i_x][seed_i_y] == 0
        f_array[seed_i_x][seed_i_y] = 1

    return copy.deepcopy(f_array)

def check_01(f_array):  # Local self-repair method with FNS-CAC codec. Number of redundant TSVs: 1,1,1,2,2,2,2
    nf_row = [0, 0, 0, 0, 0, 0, 0]
    for row_idx in range(0, 7):
        cnt_f = 0
        for col_idx in range(0, 7):
            assert f_array[row_idx][col_idx] in (0, 1)
            if f_array[row_idx][col_idx] == 1:
                cnt_f = cnt_f + 1
        if (row_idx in range(0, 3)) and (cnt_f > 1):
            return False
        elif (row_idx in range(3, 7)) and (cnt_f > 2):
            return False
        else:
            assert ((row_idx in range(0, 3)) and (cnt_f <= 1)) or ((row_idx in range(3, 7)) and (cnt_f <= 2))
        nf_row[row_idx] = cnt_f
    return True

def check_02(f_array):  # Router-based global self-repair
    for row_idx in range(0, 6):
        for col_idx in range(0, 6):
            cnt_f = 0
            if f_array[row_idx][col_idx] == 1:
                for row_idx_temp in range(row_idx, 7):
                    for col_idx_temp in range(col_idx, 7):
                        if not ( (row_idx_temp == 6) and (col_idx_temp == 6) ):
                            cnt_f = cnt_f + f_array[row_idx_temp][col_idx_temp]
                if cnt_f > ( 12 - row_idx - col_idx ):
                    return False
    return True

def check_03(f_array):
    data_code_f_map = (0, 1, 2, 2, 3, 4, 4, 5) # The number of I/O port that should be marked as unavailable is data_code_f_map[i] when there are i faulty TSVs
    # data_code_f_map_6 = (0, 1, 1, 2, 3, 3, 4)
    ioport_f_array = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    for row_idx in range(0, 7):
        f_cnt = 0
        for col_idx in range(0, 7):
            f_cnt = f_cnt + f_array[row_idx][col_idx]
        for ii in range(0, data_code_f_map[f_cnt]):
            assert ioport_f_array[row_idx][ii] == 0
            ioport_f_array[row_idx][ii] = 1

    for row_idx in range(0, 6):
        for col_idx in range(0, 4):
            cnt_f = 0
            if ioport_f_array[row_idx][col_idx] == 1:
                for row_idx_temp in range(row_idx, 7):
                    for col_idx_temp in range(col_idx, 5):
                        if not ( (row_idx_temp == 6) and (col_idx_temp == 4) ):
                            cnt_f = cnt_f + ioport_f_array[row_idx_temp][col_idx_temp]
                if cnt_f > ( 10 - row_idx - col_idx ):
                    return False
    return True

def check_04(f_array):
    target_port_flag = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ]
    for (row_idx, col_idx) in (
            (0,0),
            (0,1), (1,0),
            (0,2), (1,1), (2,0),
            (0,3), (1,2), (2,1), (3,0),
            (0,4), (1,3), (2,2), (3,1), (4,0),
            (0,5), (1,4), (2,3), (3,2), (4,1), (5,0),
            (1,5), (2,4), (3,3), (4,2), (5,1),
            (2,5), (3,4), (4,3), (5,2),
            (3,5), (4,4), (5,3),
            (4,5), (5,4),
            (5,5),

    ):
        #print("check_04 - {}".format( (row_idx, col_idx) ))
        target_candidate = (
            (row_idx, col_idx),
            (row_idx, col_idx + 1), (row_idx + 1, col_idx),
            (row_idx, col_idx + 2), (row_idx + 1, col_idx + 1), (row_idx + 2, col_idx)
        )
        candidate_idx = 0
        candidate_idx_max = 5

        if_done = False
        while not if_done:
            if candidate_idx == candidate_idx_max + 1:
                return False
            target_row_idx = target_candidate[candidate_idx][0]
            target_col_idx = target_candidate[candidate_idx][1]
            if (0 <= target_row_idx <= 6) and (0 <= target_col_idx <= 6) and ( not ( (target_row_idx == 6) and (target_col_idx == 6) ) ):
                if (target_port_flag[target_row_idx][target_col_idx] == 0) and (f_array[target_row_idx][target_col_idx] == 0):
                    if_done = True
                    target_port_flag[target_row_idx][target_col_idx] = 1
            candidate_idx = candidate_idx + 1
            #print("candidate{}".format(candidate_idx))
    return True

def check_05(f_array):
    data_code_f_map = (0, 1, 2, 2, 3, 4, 4, 5) # The number of I/O port that should be marked as unavailable is data_code_f_map[i] when there are i faulty TSVs
    # data_code_f_map_6 = (0, 1, 1, 2, 3, 3, 4)
    ioport_f_array = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    for row_idx in range(0, 7):
        f_cnt = 0
        for col_idx in range(0, 7):
            f_cnt = f_cnt + f_array[row_idx][col_idx]
        for ii in range(0, data_code_f_map[f_cnt]):
            assert ioport_f_array[row_idx][ii] == 0
            ioport_f_array[row_idx][ii] = 1

    target_port_flag = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    for (row_idx, col_idx) in (
            (0, 0),
            (0, 1), (1, 0),
            (0, 2), (1, 1), (2, 0),
            (0, 3), (1, 2), (2, 1), (3, 0),
            (1, 3), (2, 2), (3, 1), (4, 0),
            (2, 3), (3, 2), (4, 1), (5, 0),
            (3, 3), (4, 2), (5, 1),
            (4, 3), (5, 2),
            (5, 3)

    ):
        # print("check_04 - {}".format( (row_idx, col_idx) ))
        target_candidate = (
            (row_idx, col_idx),
            (row_idx, col_idx + 1), (row_idx + 1, col_idx),
            (row_idx, col_idx + 2), (row_idx + 1, col_idx + 1), (row_idx + 2, col_idx)
        )
        candidate_idx = 0
        candidate_idx_max = 5

        if_done = False
        while not if_done:
            if candidate_idx == candidate_idx_max + 1:
                return False
            target_row_idx = target_candidate[candidate_idx][0]
            target_col_idx = target_candidate[candidate_idx][1]
            if (0 <= target_row_idx <= 6) and (0 <= target_col_idx <= 4) and (
            not ((target_row_idx == 6) and (target_col_idx == 4))):
                if (target_port_flag[target_row_idx][target_col_idx] == 0) and (
                        ioport_f_array[target_row_idx][target_col_idx] == 0):
                    if_done = True
                    target_port_flag[target_row_idx][target_col_idx] = 1
            candidate_idx = candidate_idx + 1
            # print("candidate{}".format(candidate_idx))


    return True










