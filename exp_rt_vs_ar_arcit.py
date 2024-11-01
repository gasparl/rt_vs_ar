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
from psychopy.sound import Sound
import psychtoolbox as ptb
from codecs import open
from random import shuffle
from copy import deepcopy
from datetime import datetime
from os.path import isfile
from psychopy.parallel import ParallelPort
from platform import python_version
from psychopy import __version__
port = ParallelPort()

# =============================================================================
# basics
# =============================================================================

display_dur = 5
isi_delay = 20
init_delay = 8
trig_dur = 0.1
instruction_color = '#9999FF'
instr_wait = 0.3
fullscreen = True

block_infos = ['ポリグラフ検査を行います。\n検査では，以下の5つの項目が1つずつ，20～30秒間隔で提示されます。\nいずれか一つが，今回盗まれた個人情報です。\nPLACEHOLDER\n\n項目が提示されたら，事件への関与を否定するために，「いいえ」と口頭で返答してください。\n5つの項目がすべて提示されたら，短い休憩をとります。\nこれを，項目の提示順を変えて5回くり返します。\nスペースキーを押して検査をはじめてください。',
            '次の検査では，以下の5つの項目が1つずつ，20～30秒間隔で提示されます。\nいずれか一つが，今回盗まれた個人情報です。\nPLACEHOLDER\n\n項目が提示されたら，事件への関与を否定するために，「いいえ」と口頭で返答してください。\n5つの項目がすべて提示されたら，短い休憩をとります。\nこれを，項目の提示順を変えて5回くり返します。\nスペースキーを押して検査をはじめてください。']
pause_text = '短い休憩をとります。\n準備ができたらスペースキーを押して開始してください。'


# =============================================================================
# testing
# =============================================================================

testing = False # True for testing, False for real recording

if testing:
    fullscreen = False
    instr_wait = 0.1
    test_trial_num = 10
    display_dur = 1
    isi_delay = 2
    init_delay = 0.5

# =============================================================================
# MAIN ITEMS
# =============================================================================

all_items = {
    1: {
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
    2: {
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

all_items_dict = {
    'みずほ銀行' : 'Mizuho_bank',
    'りそな銀行' : 'Risona_bank',
    'スルガ銀行' : 'Suruga_bank',
    'セブン銀行' : 'Seven_bank',
    'イオン銀行' : 'Aeon_bank',
    'ソニー銀行' : 'Sony_bank',
    '桜井 優希' : 'Sakurai_Yuki',
    '野口 夏樹' : 'Noguchi_Natsuki',
    '谷口 千里' : 'Taniguchi_Chisato',
    '岩崎 未来' : 'Iwasaki_Mirai',
    '内田 日向' : 'Uchida_Hinata',
    '木下 浩実' : 'Kinoshita_Hiromi',
    '横浜銀行' : 'Yokohama_bank',
    '足利銀行' : 'Ashikaga_bank',
    '千葉銀行' : 'Chiba_bank',
    '筑波銀行' : 'Tsukuba_bank',
    '群馬銀行' : 'Gunma_bank',
    '常陽銀行' : 'Joyo_bank',
    '新井 純' : 'Arai_Jun',
    '武田 司' : 'Takeda_Tsukasa',
    '小田 薫' : 'Oda_Kaoru',
    '佐野 忍' : 'Sano_Shinobu',
    '上野 律' : 'Ueno_Ritsu',
    '松井 望' : 'Matsui_Nozomi'
}

aud_paths = ['audio_m/', 'audio_f/']
for ky in all_items_dict:
    all_items_dict[ky] = all_items_dict[ky] + '.wav'
    for pth in aud_paths:
        if not isfile(pth + all_items_dict[ky]):
            raise Exception("File not found!: " + all_items_dict[ky])

block_num = 0

def escaper():
    win.flip()
    end_quest = TextStim(win, wrapWidth = 800, height = 40, pos = [0,300],
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
    do_checks()
    create_file() # create output file
    win.mouseVisible = False

    run_blocks() # begin task & run until finished

    print("************** END OF EXPERIMENT **************")

    data_out.write("session_info\t" +
                   "/".join( ['python_v', 'psypy_v', 'guilt', 'cit_order',
                              'set_order', 'block_order', 'probe_set']) + '\t' +
                   "/".join( [ str(nmbr) for nmbr in
                              [python_version(), __version__, guilt, cit_order,
                               set_order, block_order, probe_set]]) + "\n")
    data_out.close()
    show_inf( 'これで実験を終了します。\n実験者に声をかけてください。' )
    kb.waitKeys(keyList = ['b'])
    quit()

def set_screen(): # screen properties
    global win, center_disp, instruction_page, kb, cit_audio
    win = Window([1280, 1000], color='Black', fullscr = fullscreen,
                 screen = 1, units = 'pix', allowGUI = False) # 1280 1024
    center_disp = TextStim(win, color='white', font='Arial',
                           text = '', height = 45, wrapWidth = 800)
    instruction_page = TextStim(win, wrapWidth = 1000, height = 28, alignText = 'left',
                                font='Verdana', color = instruction_color)
    cit_audio = Sound('A', stereo = True)
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


def do_checks():
    cit_audio.setSound('audio_test/test.wav')
    show_inf('Check "SCR", "SCL", "Resp", "Pulse", "ECG".\n\nIf all good, start trigger checks (2x "S1" then 2x "S2") and sound test.')
    center_disp.text = '...'
    win.flip()
    nextFlip = win.getFutureFlipTime(clock='ptb')
    cit_audio.play(when=nextFlip)
    center_disp.draw()
    win.flip()
    port.setData(1)
    wait(trig_dur)
    port.setData(0)
    wait(0.5)
    port.setData(1)
    wait(trig_dur)
    port.setData(0)
    wait(0.5)
    port.setData(2)
    wait(trig_dur)
    port.setData(0)
    wait(0.5)
    port.setData(2)
    wait(trig_dur)
    port.setData(0)
    wait(0.5)
    instruction_page.setText('Tiggers & sound correct?\n\nIf yes, start recording!')
    instruction_page.draw()
    win.flip()
    wait(instr_wait)
    if kb.waitKeys()[0] != 'y':
        escaper()
        do_checks()

def set_conds(prep_tab = False):
    global item_cats, probe_set, cit_order, set_order, block_order, guilt, a_path
    subj_num = int(subj_id) - 1
    if not (subj_id != '' and subj_num > -1 and subj_num < 200):
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
        set_order = '1_2'
        item_sets = [1, 2]
    else:
        set_order = '2_1'
        item_sets = [2, 1]
    if ((subj_num // 8) % 2 == 0):
        a_path = aud_paths[0]
        block_order = 'banks_names'
        item_cats = ['banks', 'names']
    else:
        a_path = aud_paths[1]
        block_order = 'names_banks'
        item_cats = ['names', 'banks']
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
    # select the one set from the two
    create_item_base(all_items[item_sets[ans_item_set-1]])
    subj_info = '\n-- '.join(['ID: ' + subj_id, guilt[0], cit_order,
                              set_order, block_order, 'p' + str(probe_set)])
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
        for idx, itm in enumerate(words_base[categ]): ## create basic dictionaries for the 4 crucial items, with types and categories
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
    "stimulus_shown", "category", "stim_type",  "date_in_s" ] ) + "\n" )
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
        fix_disp()
        wait(init_delay)
        for trial_num in range(len(blck_itms)): # go through all stimuli of current block
            print("------- Trial number:", trial_num, "In block:", block_num)
            stim_current = blck_itms[trial_num]
            stim_type = stim_current["item_type"]
            stim_text = stim_current["word"]
            cit_audio.setSound(a_path + all_items_dict[stim_text])
            center_disp.text = stim_text
            win.flip()
            nextFlip = win.getFutureFlipTime(clock='ptb')
            cit_audio.play(when=nextFlip)
            center_disp.draw()
            win.callOnFlip(triggr)
            win.flip()
            wait(display_dur - trig_dur) # diplay word
            fix_disp()
            add_resp()
            wait(isi_delay) # wait ISI
            if (trial_num + 1) % 5 == 0 and (trial_num + 1) < len(blck_itms):
                data_out.write( 'PAUSE\n' )
                show_inf(pause_text)
                win.flip()
                fix_disp()
                wait(init_delay)

def fix_disp():
    center_disp.text = '+'
    center_disp.draw()
    win.flip()

def show_inf(instruction_text):
    instruction_page.setText(instruction_text)
    instruction_page.draw()
    win.flip()
    wait(instr_wait)
    kb.waitKeys(keyList = ['space'])

def triggr():
    if stim_type == 'probe':
        port.setData(1)
    else:
        port.setData(2)
    wait(trig_dur)
    port.setData(0)

# EXECUTE
execute()
