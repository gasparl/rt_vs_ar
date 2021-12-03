#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 11:22:48 2021

@author: Gaspar Lukacs
"""

from psychopy.visual import Window, TextStim
from psychopy.core import wait, quit
from psychopy.event import globalKeys
from psychopy.hardware import keyboard
from psychopy.gui import Dlg
from codecs import open
from random import shuffle, choice, randint
from copy import deepcopy
from numpy import mean
from datetime import datetime
from itertools import permutations
from platform import python_version
from psychopy import __version__
import rtcit_translations as tr
print(tr.lgs[tr.lg])

# =============================================================================
# testing
# =============================================================================

testing = False # True for testing, False for real recording

if testing:
    fullscreen = False
    instr_wait = 0.1
    test_trial_num = 10
    first_ignore = True
    feed_time = 0.1
else:
    instr_wait = 0.3
    fullscreen = True
    first_ignore = False


# =============================================================================
# basics
# =============================================================================

main_ddline = 1 # sec
isi_min_max = (500, 800)
feed_time = 0.5
instruction_color = '#9999FF'
targetkey = 'i'
nontargetkey = 'e'

# =============================================================================
# MAIN ITEMS
# =============================================================================

all_items = {
    1: {
        "banks": ["Phoenix Community Trust", "Citizen Union Finances", "Vertex Corporation Banks", 
        "Goldward Credit Union", "Springwell Bank Group", "Elysium Holding Company"],
        "names": ["Jenks", "Howe", "Snell", "Rand", "Falk", "Croft"]
    },
    2: {
        "banks": ["Elysium Holding Company", "Citadel Syndicate Group", "Zenith National Holdings", "Vanguard Savings Bank", "Bulwarks Credit Union", "Phoenix Community Trust"],
        "names": ["Spence", "Bryant", "Platt", "Rusk", "Ames", "Dade"]
    }}

targetref_words = sorted(tr.targetref_words_orig[tr.lg])
nontargref_words = sorted(tr.nontargref_words_orig[tr.lg])
blck_texts = tr.blck_texts[tr.lg]

block_num = 0
all_main_rts = { 'probe' : [], 'control': [] }

def escaper():    
    win.flip()
    end_quest = TextStim(win, wrapWidth = 1200, height = 40, pos = [0,300],
                                font='Verdana', color = 'red')
    end_quest.text = ('Sure you want to quit?\nPress Y to quit, or press the spacebar to continue.')
    end_quest.draw()
    win.flip()
    wait(instr_wait)
    if kb.waitKeys(keyList = ['y', 'space'])[0] == 'y':
        print('okay, closing down...')
        try:
            data_out.close()
        except Exception:
            pass
        quit()
globalKeys.add(key="q", modifiers = ['ctrl'], func=escaper)


# EXECUTE all main functions here
def execute():
    start_input() # prompt to input stuff
    # now initiate stuff
    set_screen() # creates psychopy screen and stim objects
    # window opens
    show_instruction('START')
    create_file() # create output file
    win.mouseVisible = False

    next_block() # begin task & run until finished

    print("************** END OF EXPERIMENT **************")

    ending() # saves demographic & final infos, gives feedback, closes program

def ending():
    full_duration = round( ( datetime.now() - start_date ).total_seconds()/60, 2)
    probs_corr = len(all_main_rts['probe'])
    conts_corr = len(all_main_rts['control'])
    if probs_corr > 5 and conts_corr > 5:
        mean_diff = (mean(all_main_rts['probe']) - mean(all_main_rts['control']))
    else:
        mean_diff = 'NA'
    data_out.write("session_info\t" +
                   "/".join( ['duration','mean_diff', 'python_v', 'psypy_v',
                              'guilt', 'cit_order', 'items_order', 'block_order',
                              'probe_set']) + '\t' + 
                   "/".join( [ str(nmbr) for nmbr in 
                              [full_duration, mean_diff, python_version(),
                               __version__, guilt, cit_order, items_order, 
                               block_order, probe_set]]) + "\n")
    data_out.close()
    rtcit_eval = ('Correct probes: ' + str(probs_corr) + ' (' +
                  str(round(probs_corr/36*100, 1)) + '%)' +
                  '\nCorrect controls: ' + str(conts_corr) + ' (' +
                  str(round(conts_corr/144*100, 1)) + '%)' +
                  '\nMean diff (smaller than 20?): ' + str(round(mean_diff, 1)))
    show_instruction( tr.completed[tr.lg] )
    
    kb.waitKeys(keyList = ['b']) # press B to end the exp (prevents subject from closing window)
    print(rtcit_eval)
    show_instruction( rtcit_eval )
    quit()


def set_screen(): # screen properties
    global win, start_text, left_label, right_label, center_disp, instruction_page, kb    
    win = Window([1280, 1000], color='Black', fullscr = fullscreen,
                 screen = 1, units = 'pix', allowGUI = False) # 1280 1024    
    start_text = TextStim(win, color=instruction_color, font='Verdana', 
                          text = 'Press Space to start.', pos = [0,-300], 
                          height=35, bold = True, wrapWidth= 1100)
    left_label = TextStim(win, color='white', font='Verdana', 
                          text = '', pos = [-350,-160], height=35, alignText='center')
    right_label = TextStim(win, color='white', font='Verdana', 
                           text = '', pos = [350,-160], height=35, alignText='center')
    center_disp = TextStim(win, color='white', font='Arial', 
                           text = '', height = 45, wrapWidth = 1200)
    instruction_page = TextStim(win, wrapWidth = 1200, height = 28, alignText = 'left',
                                font='Verdana', color = instruction_color)
    kb = keyboard.Keyboard()


def start_input():
    global subj_id, categories
    input_box = Dlg(title='Session information', 
                    labelButtonOK='OK', labelButtonCancel='Cancel')
    input_box.addField(label='Subject number', tip = 'number between 1 and 200')
    input_box.show()
    if input_box.OK:
        subj_id = input_box.data[0]
        print("subj_id:", subj_id)
        set_conds()
    else:
        quit()

def set_conds(prep_tab = False):    
    global item_cats, probe_set, cit_order, items_order, block_order, guilt
    subj_num = int(subj_id) - 1
    if not (subj_id != '' and subj_num > -1 and subj_num <= 200):
        print('subject number must be between 1 and 200')
        quit()
    if ((subj_num) % 2 == 0):
        guilt = 'guilty'
    else:
        guilt = 'innocent'    
    if ((subj_num // 2) % 2 == 0):
        cit_order = 'RT_ANS'
        rt_item_set = 1
        ans_item_set = 2
    else:
        cit_order = 'ANS_RT' 
        rt_item_set = 2
        ans_item_set = 1
    if ((subj_num // 4) % 2 == 0):
        items_order = '1_2'
        item_sets = [1, 2]
    else:
        items_order = '2_1'
        item_sets = [2, 1]   
    if ((subj_num // 8) % 2 == 0):
        block_order = 'banks_names'
        item_cats = ['banks', 'names']
    else:
        block_order = 'names_banks'
        item_cats = ['names', 'banks']    
    if (subj_num <= 40):
        probe_set = 1
    elif (subj_num <= 80):
        probe_set = 2
    elif (subj_num <= 120):
        probe_set = 3
    elif (subj_num <= 160):
        probe_set = 4
    else:
        probe_set = 5
    # select the one set from the two
    ans_probes = create_item_base( all_items[item_sets[rt_item_set-1]],
                                  all_items[item_sets[ans_item_set-1]])
    subj_info = '\n-- '.join(['ID: ' + subj_id, guilt[0], cit_order, 
                              items_order, block_order, 'p' + str(probe_set)])
    print(subj_info)
    
    if prep_tab == False:
        confirm_box = Dlg(title='Confirmation', labelButtonOK='ALL CORRECT', 
                          labelButtonCancel='No, cancel')
        confirm_box.addText('Is the following information correct?\n' + subj_info)
        confirm_box.show()
        if not confirm_box.OK:
            print('cancelled...')
            quit()
    else:
        return('\n' + '\t'.join([subj_id, guilt, cit_order, items_order, 
                                 block_order, 'p' + str(probe_set), 
                                 '; '.join(task_probes), '; '.join(ans_probes)]))

def prep_table(): # to create participants' spreadsheet
    global subj_id
    table_out = '\t'.join(['subj_id', 'guilt', 'cit_order',
                           'items_order', 'block_order', 'probe_set', 
                           'probes_rt', 'probes_ans'])
    for sid in range(200):
        subj_id = str(sid+1)
        table_out += set_conds(prep_tab = True)
    table_file = open('expX_rt_vs_ar_table.txt', 'a', encoding='utf-8')
    table_file.write(table_out)
    table_file.close()

def create_item_base(words_base, words_other):
    global blcks_base, stims_base, targetrefs, nontargrefs, the_targets, the_main_items, task_probes
    stims_base = {}
    the_targets = []
    task_probes = []
    ans_probes = []
    the_main_items = []
    for categ in item_cats:
        stims_base[categ] = []
        for idx, itm in enumerate(words_base[categ]): ## create basic dictionaries for the 6 crucial items, with types and categories
            if idx == (probe_set - 1):
                itmtype = "probe"
                the_main_items.append(itm)
                task_probes.append(itm)
                ans_probes.append(words_other[categ][idx])
            elif idx == probe_set:
                itmtype = "target"
                the_targets.append(itm)
            else:
                itmtype = "control"
                the_main_items.append(itm)
            stims_base[categ].append({'word': itm,
                                      'item_type': itmtype,
                                      'categ': categ })
    the_main_items.sort()
    blcks_base = []
    for cat in item_cats: # this blcks_base now equals stim_base but could be different
        blcks_base.append( deepcopy( stims_base[cat] ) )
    targetrefs = []
    nontargrefs = []
    for ref_word in targetref_words:
        targetrefs.append({'word': ref_word, 'item_type': 'targetref', 'categ': 'inducer' })
    for ref_word in nontargref_words:
        nontargrefs.append({'word': ref_word, 'item_type': 'nontargref', 'categ': 'inducer' })
    return(ans_probes)

def main_items():
    global blcks_base, crrnt_phase
    print('main_items()')
    block_stim_base = blcks_base.pop(0)
    main_stims = add_inducers(block_stim_base)
    stim_dicts_f = [dct for sublist in main_stims for dct in sublist] # flatten
    if testing == True:
        stim_dicts_f = stim_dicts_f[0:test_trial_num]
    return stim_dicts_f

def strict_practice_items():
    print('strict_practice_items()')
    item_order_temp = deepcopy(blcks_base[0])
    shuffle(item_order_temp)
    return item_order_temp

def rndmz_details(block_stim_base):
    item_order=[]
    prev_last = '' # prev order is the item order of the previous trial sequence
    for i in range(0,18):# each i represents a sequence of 6 trials
        item_order_temp = deepcopy(block_stim_base) # create a temporary item order, this represents the item order WITHIN one trial sequence
        shuffle(item_order_temp) # shuffle this
        while prev_last == item_order_temp[0]: # if the last one of the previous block is the first of this one
            shuffle(item_order_temp) # reshuffle
        item_order.append(deepcopy(item_order_temp)) # make this the item order for this trial sequence
        prev_last = item_order_temp[-1]
    return item_order

def add_inducers(block_stim_base):
    word_assignment = {}
    # First we want to assign which words get an inducer. We want each word to get an inducer in half (9) of the trials. In addition, we want half of the words in one trial sequence (3) to have an inducer. Thus we make 9 permumtations of yes/no.
    yesno_perm = list(set(permutations('yyynnn')))
    shuffle(yesno_perm)
    options = yesno_perm[:9]
    blck_rev = []     # create an empty list for the reversed block
    for opt in options: # then we loop through to create the reverse
        optz_new = list(range(6))
        for index, item in enumerate(opt):
            if (item == "n"):
                optz_new[index] = "y"
            else:
                optz_new[index] = "n"
        blck_rev.append(deepcopy(optz_new)) # everytime add the current reversed line to the reversed block
    blck1 = options[0:3] + blck_rev[0:3] # because we wanna split them up in 3 we create blcks of 6 which are each  time 3 lines and then the reverse of those 3 lines
    blck2 = options[3:6] + blck_rev[3:6]
    blck3 = options[6:9] + blck_rev[6:9]
    shuffle(blck1)
    shuffle(blck2)
    shuffle(blck3)
    #create final block
    blck_fin = blck1 + blck2 + blck3
    for indx, dct in enumerate(block_stim_base): #assign the yes/nos to the words
        word_assignment[ dct['word'] ] = [opt[indx] for opt in blck_fin] # combine them to create an inducer assignment for all 18 trial sequences and assign them to the dict
    #  We then need to decide which inducer is shown thus we make a list
    inducer_lists = inducer_randomized() # randomize 6 lists of inducer words
    inducer_per_main = {}
    for dct in block_stim_base:
            inducer_per_main[ dct['word'] ] = inducer_lists.pop()
    # now insert the inducers
    final_item_order = []
    for t_indx, trial_seq in enumerate(rndmz_details(block_stim_base)): # trial sequence represents the order in which the x amount of words are presented within one sequence (n=6) of trials
        final_temp = []
        for i_indx, item in enumerate(trial_seq): # item represents each individual word (or trial)
            if word_assignment[item["word"]][t_indx] == "y": # check if the word should get an inducer
                inducer_pick= inducer_per_main[item["word"]].pop(0) # pick the right inducer
            # then we should delete this element so inducer so we use pop
                final_temp.append(inducer_pick) # append the inducer to our item order
            final_temp.append(item) # append the item to our item order
        final_item_order.append(deepcopy(final_temp)) # create final item order list
    return final_item_order

def inducer_randomized(): # 6 possible inducer orders
    targetrefs_perm = list(permutations(targetrefs)) # 3 x 2 = 6 arrangements
    shuffle(targetrefs_perm)
    nontarg_temp = deepcopy(nontargrefs)
    shuffle(nontarg_temp)
    nontargrefs_perm1 = list(permutations(nontarg_temp[:3])) # 3 x 2 = 6
    nontargrefs_perm2 = list(permutations(nontarg_temp[3:])) # 3 x 2 = 6
    nontargrefs_perm = []
    for i in range(3): # 6/2 = 3
        nontargrefs_perm.append(nontargrefs_perm1.pop(0)+nontargrefs_perm2.pop(0))
        nontargrefs_perm.append(nontargrefs_perm2.pop(0)+nontargrefs_perm1.pop(0))
    shuffle(nontargrefs_perm)
    inducer_lists = []
    for trefs, ntrefs in zip(targetrefs_perm, nontargrefs_perm):
        trefs = list(trefs)
        ntrefs = list(ntrefs)
        lst_temp = ntrefs
        nums = list(range(len(trefs+ntrefs)))
        insert_locs = []
        for i in range(len(trefs)): # tref never repeats successively
            new_rand = choice(nums)
            insert_locs.append(new_rand)
            nums = [n for n in nums if abs(n-new_rand) > 1]
        for loc in sorted(insert_locs): # trefs to the 3 locs
            lst_temp.insert( loc, trefs.pop() )
        inducer_lists.append(deepcopy(lst_temp))
    return inducer_lists

def inducer_items():
    print('inducer_items()')
    blck_itms_temp = deepcopy(targetrefs + nontargrefs + targetrefs + nontargrefs) # inducers x2
    shuffle(blck_itms_temp) # shuffle it, why not
    safecount = 0 # just to not freeze the app if sth goes wrong
    stim_dicts_f = [] # in here the final list of dictionary items is collected, one by one
    while len(blck_itms_temp) > 0: # stop if all items from blck_itms_temp were use up
        dict_item = blck_itms_temp[0]
        safecount += 1
        if safecount > 911:
            print('break due to unfeasable safecount')
            break
        good_indexes = [] # will collect the indexes where the dict item may be inserted
        dummy_dict = [{ 'word': '-', 'item_type': '-' }] # dummy dict to the end
        for f_index, f_item in enumerate(stim_dicts_f + dummy_dict):
            if dict_item['word'] in diginto_dict(stim_dicts_f, f_index, 'word', 4):
                continue # if there is, continue without adding the index as good index
            good_indexes.append(f_index) # if did not continue above, do add as good index
        if len(good_indexes) == 0:
            print('no good_indexes - count', safecount)
            shuffle(blck_itms_temp) # reshuffle
        else: # if there are good places, choose one randomly, insert the new item, and remove it from blck_itms_temp
            stim_dicts_f.insert( choice(good_indexes) , blck_itms_temp.pop(0))
    if testing == True:
        stim_dicts_f = stim_dicts_f[0:test_trial_num]
    return stim_dicts_f # return final list (for blck_items var assignment)


def full_practice_items():
    print('practice_items()')
    blck_itms_temp = deepcopy(blcks_base[0] + targetrefs + nontargrefs)
    shuffle(blck_itms_temp) # shuffle it, why not
    # below the pseudorandomization to avoid close repetition of similar items (same item type)
    safecount = 0 # just to not freeze the app if sth goes wrong
    stim_dicts_f = [] # in here the final list of dictionary items is collected, one by one
    while len(blck_itms_temp) > 0: # stop if all items from blck_itms_temp were use up (added to stim_dicts_f and removed with pop() )
        dict_item = blck_itms_temp[0] # assign first dictionary item as separate variable; for easier access below
        safecount += 1
        if safecount > 911:
            print('break due to unfeasable safecount')
            break
        good_indexes = [] # will collect the indexes where the dict item may be inserted
        dummy_dict = [{ 'word': '-', 'item_type': '-' }] # dummy dict to the end; if the item is to be inserted to the end, there is no following dict that could cause an unwanted repetition
        for f_index, f_item in enumerate(stim_dicts_f + dummy_dict): # check all potential indexes for insertion in the stim_dicts_f as it is so far (plus 1 place at the end)
            if (dict_item['item_type'] not in ('probe', 'control') and 
                    dict_item['item_type'] in diginto_dict(stim_dicts_f, f_index, 'item_type', 1)): # checks whether there is preceding or following identical item_type around the potential index (see diginto_dict function)
                continue # if there is, continue without adding the index as good index
            good_indexes.append(f_index) # if did not continue above, do add as good index
        if len(good_indexes) == 0: # if by chance no good indexes found, print notification and reshuffle the items
            print('no good_indexes - count', safecount) # this should normally happen max couple of times
            blck_itms_temp.insert( len(blck_itms_temp), blck_itms_temp.pop(0) ) # move first element to last, and let's hope next first item is luckier and has place
        else: # if there are good places, choose one randomly, insert the new item, and remove it from blck_itms_temp
            stim_dicts_f.insert( choice(good_indexes) , blck_itms_temp.pop(0))
    if testing == True:
        stim_dicts_f = stim_dicts_f[0:test_trial_num]
    return stim_dicts_f # return final list (for blck_items var assignment)

def diginto_dict(dct, indx, key_name, min_dstnc):
    if indx - min_dstnc < 0: # if starting index is negative, it counts from the end of the list; thats no good
        strt = 0 # so if negative, we just set it to 0
    else:
        strt = indx - min_dstnc # if not negative, it can remain the same
    return [ d[key_name] for d in dct[ strt : indx+min_dstnc ] ] # return all values for the specified dict key within the specified distance (from the specified dictionary)


# create output file, begin writing, reset parameters
def create_file():
    global data_out, start_date 
    start_date = datetime.now()
    f_name = 'exp_rt_vs_ar_rtcit_' + subj_id + start_date.strftime("_%Y%m%d_%H%M") + '.txt'
    data_out = open(f_name, 'a', encoding='utf-8')
    data_out.write( '\t'.join( [ "subject_id", "phase", "block_number", "trial_number", 
    "stimulus_shown", "category", "stim_type", "response_key", "rt_start", "incorrect", 
    "too_slow", "press_duration", "isi", "date_in_ms" ] ) + "\n" )
    print("File created:", f_name)

def str_if_num( num_val ):
    if isinstance(num_val, str):
        return num_val
    else:
        return str( num_val*1000 )

def replcs(text):
    comma = tr.comma[tr.lg]
    targw = []
    nontargw = []
    for item in blcks_base[0]:
        if item['item_type'] == 'target':
            targw.append(item["word"])
        else:
            nontargw.append(item["word"])
    return(text.replace(tr.trefs, comma.join(targetref_words)).replace(
           tr.nontrefs, comma.join(nontargref_words)).replace(
           tr.targs, comma.join(sorted(targw))).replace(
           tr.nontargs, comma.join(sorted(nontargw))))

def add_resp():
    data_out.write( '\t'.join( [ subj_id, crrnt_phase, str(block_num), str(trial_num+1), 
    stim_text, stim_current["categ"], stim_type, resp_key, str_if_num(rt_start), str(incorrect), 
    str(tooslow), str_if_num(press_dur), str_if_num( isi_min_max[0]/1000 + isi_delay ), datetime.now().strftime("%y%m%d_%H%M%S") ] ) + '\n' )
    print("resp key:", resp_key, "for stim:", stim_text, "incorrect:", incorrect, "rt_start:", rt_start)

def start_with_space():
    start_text.draw() # start with space
    center_disp.setText("+")
    center_disp.draw()
    draw_labels()
    win.flip()
    kb.waitKeys(keyList = ['space'])
    draw_labels()
    win.flip()
    wait(isi_min_max[0]/1000)

def draw_labels():
    if block_num <= 2:
        left_label.draw()
        right_label.draw()

def next_block():
    global ddline, block_num, rt_data_dict, blck_itms, crrnt_phase, block_info
    if len(blcks_base) > 0:
        ddline = main_ddline
        if (block_num not in (1,2,3,5)) or practice_eval():
                block_num+=1
                block_info = replcs(blck_texts[block_num-1]) + tr.move_on[tr.lg]
        crrnt_phase = 'practice'
        rt_data_dict = {}
        if block_num == 1:
            blck_itms = inducer_items()
        elif block_num in (2, 5):
            crrnt_phase = 'practice_strict'
            blck_itms = strict_practice_items()
            ddline = 10
        elif block_num == 3:
            blck_itms = full_practice_items()
        else:
            crrnt_phase = 'main'
            block_info = replcs(blck_texts[block_num-1]) + tr.move_on[tr.lg]
            blck_itms = main_items()
        print('BLOCK', block_num)
        run_block()

first_try = False
def practice_eval():
    global block_info, first_try
    is_valid = True
    feedb = ''
    if block_num == 0:
        return True
    if block_num == 3:
        if first_try == True:
            return True
        else:
            first_try = True
    if first_wrong == True:
        is_valid = False
        block_info = tr.acc_feed1[tr.lg] + tr.move_on[tr.lg] + tr.show_inst[tr.lg]
    elif crrnt_phase != 'practice_strict':
        if block_num == 1:
            min_ratio = 0.8
        else:
            min_ratio = 0.5
        if testing == True:
            min_ratio = 0.1
        for it_type in rt_data_dict:
            rts_correct = [ rt_item for rt_item in rt_data_dict[it_type] if rt_item > 0.15 ]
            corr_ratio = len( rts_correct )/ len( rt_data_dict[it_type] )
            if corr_ratio < min_ratio:
                is_valid = False
                if feedb == '':
                    feedb = it_type
                else:
                    feedb = 'allits'
        if is_valid == False:
            block_info = tr.acc_feed2[tr.lg][feedb] + tr.move_on[tr.lg] + tr.show_inst[tr.lg]
    return is_valid

def show_instruction(instruction_text):
    instruction_page.setText(instruction_text)
    instruction_page.draw()
    win.flip()
    wait(instr_wait)
    kb.waitKeys(keyList = ['space'])

def show_block_instr():
    instruction_page.setText( block_info )
    instruction_page.draw()
    win.flip()
    wait(instr_wait)
    show_again = 'return'
    inst_resp = kb.waitKeys( keyList = [ 'space', show_again ] )
    if inst_resp[0] == show_again:
        show_instruction(  replcs(blck_texts[block_num-1]) + tr.move_on[tr.lg] )

def run_block():
    global block_num, trial_num, stim_current, stim_text, stim_type, incorrect, tooslow, first_wrong, show_feed, isi_delay, resp_key, rt_start, press_dur
    show_block_instr()
    first_wrong = False
    print("len(blck_itms):", len(blck_itms))
    start_with_space()
    for trial_num in range(len(blck_itms)): # go through all stimuli of current block
        print("------- Trial number:", trial_num, "In block:", block_num)
        stim_current = blck_itms[trial_num]
        incorrect = 0
        tooslow = 0
        stim_type = stim_current["item_type"]
        stim_text = stim_current["word"]
        isi_delay = randint(1, isi_min_max[1]-isi_min_max[0]) / 1000
        wait(isi_delay) # wait ISI
        center_disp.text = stim_text
        draw_labels()
        center_disp.draw()
        win.callOnFlip(kb.clock.reset)
        win.flip()
        kb.clearEvents()
        response = kb.waitKeys(maxWait = ddline, waitRelease = False,
                               keyList=[targetkey, nontargetkey])
        if not response:
            rt_start = kb.clock.getTime()
            resp_key = 'NA'
            tooslow += 1
            show_tooslow()
        else:
            resp_key = response[0].name
            rt_start = response[0].rt
            if resp_key == targetkey:
                if stim_type in ("target", "targetref"):
                    incorrect = 0
                    tooslow = 0
                else:
                    incorrect += 1
                    show_false()
            elif resp_key == nontargetkey:
                if stim_type[:10] in ("probe","control", "nontargref"):
                    incorrect = 0
                    tooslow = 0
                else:
                    incorrect += 1
                    show_false()
        draw_labels()
        win.flip()
        isi2 = isi_min_max[0]/1000
        wait(isi2, hogCPUperiod = isi2)
        get_dur = kb.getKeys(keyList=[resp_key])
        if get_dur:
            press_dur = get_dur[0].duration
        else:
            press_dur = 'NA'
        add_resp() # store trial data
        # check if comprehension check has to be repeated
        if crrnt_phase == 'practice_strict' and (incorrect+tooslow) > 0 and first_ignore == False:
            first_wrong = True
            break
        collect_rts()
    next_block()

def collect_rts(): # for practice evaluation & dcit calculation
    global rt_data_dict, all_main_rts
    rt = rt_start
    if (incorrect+tooslow) > 0:
        rt = -9
    if stim_type in ("target", "targetref"):
        group_type = 'targs'
    else:
        group_type = 'nontargs'
    if group_type not in rt_data_dict:
        rt_data_dict[group_type] = []
    rt_data_dict[group_type].append(rt)
    if (crrnt_phase == 'main' and stim_type in ("probe","control") and 
        incorrect != 1 and tooslow != 1 and rt > 0.15 and rt < main_ddline):
        all_main_rts[ stim_type ].append(rt)

def show_false():
    center_disp.text = 'Wrong!'
    center_disp.color = '#ff1111'
    center_disp.draw()
    draw_labels()
    win.flip()
    wait(feed_time)
    center_disp.color = 'white'
def show_tooslow():
    center_disp.text = 'Too slow!'
    center_disp.color = '#ff1111'
    center_disp.draw()
    draw_labels()
    win.flip()
    wait(feed_time)
    center_disp.color = 'white'

# EXECUTE
execute()
