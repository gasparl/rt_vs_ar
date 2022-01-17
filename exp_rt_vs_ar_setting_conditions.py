
# Below are all possible items.
# For each participant, one set (either "1" or "2") is used for ANS CIT,
# and the other set is used for RT-CIT ("2" or "1", respectively).
# The probe item within each category depends on the subject number; see below.

all_items = {
    1: { # set 1
        "banks": [
        'みずほ銀行', # (Mizuho Bank)
        'りそな銀行', # (Risona Bank)
        'スルガ銀行', # (Suruga Bank)
        'セブン銀行', # (Seven Bank)
        'イオン銀行', # (Aeon Bank)
        'ソニー銀行' # (Sony Bank)
        ],
        "names": [
        '桜井 優希', # (Sakurai Yuki)
        '野口 夏樹', # (Noguchi Natsuki)
        '谷口 千里', # (Taniguchi Chisato)
        '岩崎 未来', # (Iwasaki Mirai)
        '内田 日向', # (Uchida Hinata)
        '木下 浩実' # (Kinoshita Hiromi)
        ]
    },
    2: { # set 2
        "banks": [
        '横浜銀行', # (Bank of Yokohama)
        '足利銀行', # (Ashikaga Bank)
        '千葉銀行', # (Chiba Bank)
        '筑波銀行', # (Tsukuba Bank)
        '群馬銀行', # (Gunma Bank)
        '常陽銀行' # (Joyo Bank)
        ],
        "names": [
        '新井 純', # (Arai Jun)
        '武田 司', # (Takeda Tsukasa)
        '小田 薫', # (Oda Kaoru)
        '佐野 忍', # (Sano Shinobu)
        '上野 律', # (Ueno Ritsu)
        '松井 望' # (Matsui Nozomi)
        ]
    }}


def set_conds(prep_tab = False):
    global item_cats, probe_set, cit_order, set_order, block_order, guilt
    subj_num = int(subj_id) - 1 # subject number for the calculations below
    # (Minus one is needed for easier handling of divisibility.)
    if not (subj_id != '' and subj_num > -1 and subj_num <= 200):
        print('subject number must be between 1 and 200')
        quit()

    # Guilt:
    # If subject number is divisible by 2, the participant is guilty.
    # This is just for information, and not needed for the task.
    if ((subj_num) % 2 == 0):
        guilt = 'guilty'
    else:
        guilt = 'innocent'
        
    # CIT order:
    # If the subject number is in each first set of 2, RT-CIT comes first, ANS-CIT second.
    # Otherwise the reverse.
    if ((subj_num // 2) % 2 == 0):
        cit_order = 'RT_ANS'
        rt_item_set = 1
        ans_item_set = 2
    else:
        cit_order = 'ANS_RT'
        rt_item_set = 2
        ans_item_set = 1        

    # Set order: 
    # If in each first set of 4, set 1 comes first, set 2 comes second.
    # Otherwise the reverse.
    # (So if e.g. RT-CIT and set 1 both come first, RT-CIT will have set 1 items.)
    if ((subj_num // 4) % 2 == 0):
        set_order = '1_2'
        item_sets = [1, 2]
    else:
        set_order = '2_1'
        item_sets = [2, 1]
    
    # Block order:
    # If in each first set of 8, bank names comes first, names second.
    # Otherwise the reverse.
    # (Name order is always: first forenames, then surnames.)
    if ((subj_num // 8) % 2 == 0):
        block_order = 'banks_names'
        item_cats = ['banks', 'names']
    else:
        block_order = 'names_banks'
        item_cats = ['names', 'banks']
        
    # Probe choice:    
    # Depending on subject number as specified below, participants may get 
    # a certain one of the 5 probes within each category.
    # For example, those with subject number below or equal to 40, 
    # they get the first item in each category (e.g. Mizuho Bank and Sakurai Yuki).
    # If they are between 41 and 80, they get the second item in each category. And so forth.
    # (The "target" in the RT-CIT is always the item that comes after the probe.
    # This item is simply skipped in case of ANS-CIT.)
    if (subj_num < 40):
        probe_set = 1
    elif (subj_num < 80):
        probe_set = 2
    elif (subj_num < 120):
        probe_set = 3
    elif (subj_num < 160):
        probe_set = 4
    else:
        probe_set = 5
    # select the applicable one set from the two
    ans_probes = create_item_base( all_items[item_sets[rt_item_set-1]],
                                  all_items[item_sets[ans_item_set-1]])
    # (Note: in Python, indexing starts at zero, hence the minus one.)
    subj_info = '\n-- '.join(['ID: ' + subj_id, guilt[0], cit_order,
                              set_order, block_order, 'p' + str(probe_set)])
    print(subj_info)


    return('\n' + '\t'.join([subj_id, guilt, cit_order, set_order,
                             block_order, 'p' + str(probe_set),
                             '; '.join(task_probes), '; '.join(ans_probes)]))

def create_item_base(words_base, words_other):
    global task_probes
    stims_base = {}
    the_targets = []
    task_probes = []
    ans_probes = []
    the_main_items = []
    for categ in item_cats: # iterate through each category
        stims_base[categ] = []
        for idx, itm in enumerate(words_base[categ]): # get the item index within category
            if idx == (probe_set - 1): # if probe, add to probes
                itmtype = "probe"
                the_main_items.append(itm)
                task_probes.append(itm)
                ans_probes.append(words_other[categ][idx])
            elif idx == probe_set:  # if target, add to targets
                itmtype = "target"
                the_targets.append(itm)
            else: # unless target, add to controls
                itmtype = "control"
                the_main_items.append(itm)
            stims_base[categ].append({'word': itm,
                                      'item_type': itmtype,
                                      'categ': categ })
    the_main_items.sort()  
    return(ans_probes)

def prep_table(): # to create participants' spreadsheet
    global subj_id
    table_out = '\t'.join(['subject_id', 'guilt', 'cit_order',
                           'set_order', 'block_order', 'probe_set',
                           'probes_rt', 'probes_ans'])
    for sid in range(200):
        subj_id = str(sid+1)
        table_out += set_conds(prep_tab = True)
    table_file = open('expX_rt_vs_ar_table.txt', 'a', encoding='utf-8')
    table_file.write(table_out)
    table_file.close()
    
prep_table()