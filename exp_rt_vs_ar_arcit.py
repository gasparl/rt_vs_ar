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
from random import shuffle
from copy import deepcopy
from datetime import datetime
from psychopy.parallel import ParallelPort
from platform import python_version
from psychopy import __version__
port = ParallelPort()

# =============================================================================
# basics
# =============================================================================

display_dur = 30
isi_delay = 0.5
trig_dur = 0.1
instruction_color = '#9999FF'
instr_wait = 0.3

block_infos = ['You will be repeatedly shown the following items one by one: PLACEHOLDER. Say "no" whenever you see a new item. Press space to move on.',
            'You will now be shown the following items: PLACEHOLDER. Again, say "no" whenever you see a new item. Press space to move on.',
            'You will now be shown the following items: PLACEHOLDER. Again, say "no" whenever you see a new item. Press space to move on.' ]
pause_text = 'You can rest a little. Press space when you are ready to move on.'


# =============================================================================
# testing
# =============================================================================

testing = True # True for testing, False for real recording

if testing:
    fullscreen = False
    instr_wait = 0.1
    test_trial_num = 10
    display_dur = 1
else:
    fullscreen = True

# =============================================================================
# MAIN ITEMS
# =============================================================================

all_items = {
    1: {
        "banks": ["Phoenix Community Trust", "Citizen Union Finances", "Vertex Corporation Banks", 
        "Goldward Credit Union", "Springwell Bank Group", "Elysium Holding Company"],
        "forenames": ["Jenks", "Howe", "Snell", "Rand", "Falk", "Croft"],
        "surnames": ["Phil", "Tim", "Ray", "Neil", "Gene", "Ralph"]
    },
    2: {
        "banks": ["Elysium Holding Company", "Citadel Syndicate Group", "Zenith National Holdings", "Vanguard Savings Bank", "Bulwarks Credit Union", "Phoenix Community Trust"],
        "forenames": ["Spence", "Bryant", "Platt", "Rusk", "Ames", "Dade"],
        "surnames": ["Dale", "Wayne", "Glenn", "Walt", "Tod", "Earl"]
    }}


block_num = 0

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
    show_inf('START')
    create_file() # create output file
    win.mouseVisible = False

    run_blocks() # begin task & run until finished

    print("************** END OF EXPERIMENT **************")

    data_out.write("session_info\t" +
                   "/".join( ['python_v', 'psypy_v', 'guilt', 'cit_order', 
                              'items_order', 'block_order', 'probe_set']) + '\t' + 
                   "/".join( [ str(nmbr) for nmbr in 
                              [python_version(), __version__, guilt, cit_order,
                               items_order, block_order, probe_set]]) + "\n")
    data_out.close()    
    show_inf( 'Test completed' )
    kb.waitKeys(keyList = ['b'])
    quit()

def set_screen(): # screen properties
    global win, start_text, center_disp, instruction_page, kb    
    win = Window([1280, 1000], color='Black', fullscr = fullscreen,
                 screen = 1, units = 'pix', allowGUI = False) # 1280 1024    
    start_text = TextStim(win, color=instruction_color, font='Verdana', 
                          text = 'Press Space to start.', pos = [0,-300], 
                          height=35, bold = True, wrapWidth= 1100)
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
        ans_item_set = 2
    else:
        cit_order = 'ANS_RT'
        ans_item_set = 1
    if ((subj_num // 4) % 2 == 0):
        items_order = '1_2'
        item_sets = [1, 2]
    else:
        items_order = '2_1'
        item_sets = [2, 1]   
    if ((subj_num // 8) % 2 == 0):
        block_order = 'banks_names'
        item_cats = ['banks', 'forenames', 'surnames']
    else:
        block_order = 'names_banks'
        item_cats = ['forenames', 'surnames', 'banks']    
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
    create_item_base(all_items[item_sets[ans_item_set-1]])
    subj_info = '\n-- '.join(['ID: ' + subj_id, guilt[0], cit_order, 
                              items_order, block_order, 'p' + str(probe_set)])
    print(subj_info)
    confirm_box = Dlg(title='Confirmation', labelButtonOK='ALL CORRECT', 
                      labelButtonCancel='No, cancel')
    confirm_box.addText('Is the following information correct?\n' + subj_info)
    confirm_box.show()
    if not confirm_box.OK:
        print('cancelled...')
        quit()

def create_item_base(words_base):
    global blcks_base, block_words
    stims_base = {}
    block_words = []
    for categ in item_cats:
        stims_base[categ] = []
        for idx, itm in enumerate(words_base[categ]): ## create basic dictionaries for the 6 crucial items, with types and categories
            if not idx == probe_set:
                if idx == (probe_set - 1):
                    itmtype = "probe"
                else:
                    itmtype = "control"
                stims_base[categ].append({'word': itm,
                                          'item_type': itmtype,
                                          'categ': categ })
        newblockwords = '、'.join(sorted(words_base[categ]))
        block_words.append(newblockwords)
    blcks_base = []
    for cat in item_cats: # this blcks_base now equals stim_base but could be different
        blcks_base.append( deepcopy( stims_base[cat] ) )

def block_items():
    global blcks_base, crrnt_phase
    print('main_items()')
    block_stim_base = blcks_base.pop(0)
    shuffle(block_stim_base)
    itorders = ((2, 3, 1, 4, 5), (5, 1, 4, 2, 3), (4, 5, 3, 1, 2),
               (1, 2, 5, 3, 4), (3, 4, 2, 5, 1))
    stim_dicts_f = []
    for itordr in itorders:
        stim_dicts_f += [block_stim_base[i-1] for i in itordr]
    if testing == True:
        stim_dicts_f = stim_dicts_f[0:test_trial_num]
    return stim_dicts_f

# create output file, begin writing, reset parameters
def create_file():
    global data_out, start_date 
    start_date = datetime.now()
    f_name = 'exp_rt_vs_ar_arcit_' + subj_id + start_date.strftime("_%Y%m%d_%H%M") + '.txt'
    data_out = open(f_name, 'a', encoding='utf-8')
    data_out.write( '\t'.join( [ "subject_id", "block_number", "trial_number", 
    "stimulus_shown", "category", "stim_type",  "date_in_ms" ] ) + "\n" )
    print("File created:", f_name)


def add_resp():
    data_out.write( '\t'.join( [ subj_id, str(block_num), str(trial_num+1), stim_text,
                                stim_current["categ"], stim_type, 
                                datetime.now().strftime("%y%m%d_%H%M%S") ] ) + '\n' )
    print("Block:", block_num, "Trial:", trial_num, "Stim:", stim_text)


def run_blocks():
    global block_num, trial_num, stim_current, stim_text, stim_type
    while len(blcks_base) > 0:
        show_inf(block_infos.pop(0).replace('PLACEHOLDER', block_words.pop(0)))
        block_num += 1
        blck_itms = block_items()
        print('BLOCK', block_num)
        print("len(blck_itms):", len(blck_itms))
        for trial_num in range(len(blck_itms)): # go through all stimuli of current block
            print("------- Trial number:", trial_num, "In block:", block_num)
            stim_current = blck_itms[trial_num]
            stim_type = stim_current["item_type"]
            stim_text = stim_current["word"]
            center_disp.text = stim_text
            center_disp.draw()
            win.callOnFlip(triggr)  
            win.flip()
            wait(display_dur - isi_delay - trig_dur) # diplay word
            win.flip()
            add_resp()
            wait(isi_delay) # wait ISI
            if (trial_num+1) % 5 == 0:
                data_out.write( 'PAUSE\n' )
                show_inf(pause_text)
                win.flip()
                wait(isi_delay)

def show_inf(instruction_text):
    instruction_page.setText(instruction_text)
    instruction_page.draw()
    win.flip()
    wait(instr_wait)
    kb.waitKeys(keyList = ['space'])

def triggr():
    if stim_type == 'probe':
        port.setData(2)
    else:
        port.setData(1)
    wait(trig_dur)
    port.setData(0)

# EXECUTE
execute()
