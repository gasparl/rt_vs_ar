# this files contains all instructions and filler words used in the CIT

lg = 'en'

lgs = {
    'en': 'English',
    'de': 'Deutsch',
    'jp': '日本語'
}

# target-side default fillers
targetref_words_orig = {
    'en': ['FAMILIAR', 'MINE', 'RECOGNIZED'], # these words are not to be translated literally one by one. The translations should always try to find the simplest, clearest words that relate to relevance, familiarity, recognition, importance. (The English 'MINE' is actually not the best, but it's good to also have a shorter word and this fits there.)
    'de': ['VERTRAUT', 'MEIN', 'RELEVANT'],
    'jp': '日本語'
}

# nontarget-side default fillers
nontargref_words_orig = {
    'en': ['FOREIGN', 'IRRELEVANT', 'OTHER', 'RANDOM', 'THEIRS', 'UNFAMILIAR'], # these should have the meaning opposite of    relevance, familiarity, importance
    'de': ['IRRELEVANT', 'FREMD', 'UNBEKANNT', 'ANDERE', 'SONSTIGES', 'UNVERTRAUT'],
    'jp': '日本語'
}

move_on = {
    'en': '\n\nPress Space to move on.',
    'de': 'Start',
    'jp': '日本語'
}

show_inst = {
    'en': 'If needed, press Enter to read the full instructions again.',
    'de': '...',
    'jp': '日本語'
}


taptostart = {
    'en': 'Press space to start.',
    'de': '...',
    'jp': '日本語'
}

feedtooslo = {
    'en': 'Too slow!',
    'de': 'Zu langsam!',
    'jp': '日本語'
}
feedwrong = {
    'en': 'Wrong!',
    'de': 'Falsch!',
    'jp': '日本語'
}

it_type_feed_dict = {
    'en': {
        'targ_items': 'items to be categorized to the right side',
        'nontarg_items': 'items to be categorized to the left side'
    },

    'de': {
        'targetflr': '...',
        'nontargflr': '...'
    },
    'jp': '日本語'
}

accrep_feed = {
    'en': 'You will have to repeat this practice round due to a wrong response (or too much waiting).',
    'de': 'Sie müssen die Übungsrunde wegen einer falschen (oder zu langsamen) Antwort wiederholen.',
    'jp': '日本語'
}

acc_feed = {
    'en': {
        'start': 'You will have to repeat this practice round because of too few correct responses ',
        'targs': 'to the items to be categorized with the right ("I") key. Please pay more attention to these items!',
        'nontargs': 'to the items to be categorized with the left ("E") key. Please pay more attention to these items!',
        'allits': 'to all the item types. Please pay more attention!'
        },
    'de': '...',
    'jp': {
        'start': '日本語',
        'targs': '日本語',
        'nontargs': '日本語',
        'allits': '日本語'
        }
}

cit_completed = {
    'en': 'Test completed. Please inform the experiment leader.',
    'de': '...',
    'jp': '日本語'
}

targs = 'TARGETS_PLACEHOLDER'
nontargs =  'NONTARGS_PLACEHOLDER'
trefs = 'TREFS_PLACEHOLDER'
nontrefs = 'NONTREFS_PLACEHOLDER'

# instructions preceding given blocks, set based on the selected CIT version
# In English it seems unnecessary, but in other languages, it is often better to clarify that the items appear 'one by one'. It may also be worthwhile to somehow make it clearer that the 'buttons' are just pressscreen surfaces.
blck_texts = {
    'en': [
        # block 1
        'During the following test, various items will appear in the middle of the screen. You have to categorize each item by pressing the key "E" on the left or the key "I" on the right. There will be three short practice rounds. \n\nIn the first practice round, you have to categorize two kinds of items. \n\nPress the right ("I") key when you see any of the following items (referring to familiarity with the crime details):\n' + trefs + 'Press the left ("E") key when you see any other item. These other items are:\n' + nontrefs + 'There is a certain time limit for making each response. Please try to be both fast and accurate. In each of the two item categories, you need at least 80% correct responses in time, otherwise you have to repeat the practice round.',
        # block 2
        'In the second practice round, you have to categorize the main test items. The aim of the entire test will be to show whether or not one of these main items (a crime detail) is recognized by you. ' + 'Press the right ("I") key when you see the following target item:\n' + targs +   'Press the left ("E") key when you see any other item. These other items are:\n' + nontargs + 'In this practice round, you will have a lot of time to choose each response, but you must respond to each item correctly. If you choose an incorrect response (or not give response for over 10 seconds), you will have to repeat the practice round.',
        # block 3
        'In the third and last practice round all items are present.\n\nYou again have to respond fast, but a certain number of errors is allowed. The task is the same. Press the right ("I") key when you see the following items:\n' + targs + trefs + 'Press the left ("E") key for everything else.',
        # block 4
        'Now the actual test begins. The task is the same. Press the right ("I") key when you see the following items:\n' + targs + trefs + 'Press the left ("E") key for everything else.',
        # block 5
        'Now the main words will be different. Press the right ("I") key when you see the following "target" item: ' + targs + '.\n\nPress the left ("E") key when you see any of the following items: ' + nontargs + '.\n\nTo make sure you understood this, in the following short practice round, you must respond to each item correctly, otherwise you have to repeat this round.',
        # block 6
        'Alright. The next block starts. The task is the same. Press the right ("I") key, when you see any of the following items: ' + targs + ', ' + trefs + '. Press the left ("E") key when you see any other item.'],
    'de': '...',
    'jp': [
        # block 1
        '',
        # block 2
        '',
        # block 3
        '',
        # block 4
        '',
        # block 5
        '',
        # block 6
        '']
}