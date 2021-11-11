# this files contains all instructions and filler words used in the CIT

lang = 'en'

lgs = {
    'en': 'English',
    'de': 'Deutsch',
    'jp': '日本語'
}

# target-side default fillers
targetref_words_orig = {
    'en': ["FAMILIAR", "MINE", "RECOGNIZED"], # these words are not to be translated literally one by one. The translations should always try to find the simplest, clearest words that relate to relevance, familiarity, recognition, importance. (The English "MINE" is actually not the best, but it's good to also have a shorter word and this fits there.)
    'de': ["VERTRAUT", "MEIN", "RELEVANT"],
    'jp': '日本語'
}

# nontarget-side default fillers
nontargref_words_orig = {
    'en': ["FOREIGN", "IRRELEVANT", "OTHER", "RANDOM", "THEIRS", "UNFAMILIAR"], # these should have the meaning opposite of    relevance, familiarity, importance
    'de': ["IRRELEVANT", "FREMD", "UNBEKANNT", "ANDERE", "SONSTIGES", "UNVERTRAUT"],
    'jp': '日本語'
}


start = {
    'en': 'Start',
    'de': 'Start',
    'jp': '日本語'
}

show_inst = {
    'en': 'show instructions again',
    'de': 'Instruktionen erneut anzeigen',
    'jp': '日本語'
}


taptostart = {
    'en': 'Press space to start',
    'de': '...',
    'jp': '日本語'
}

feedtooslo = {
    'en': "Too slow!",
    'de': 'Zu langsam!',
    'jp': '日本語'
}
feedwrong = {
    'en': "Wrong!",
    'de': "Falsch!",
    'jp': '日本語'
}

it_type_feed_dict = {
    'en': {
        'targ_items': "items to be categorized to the right side",
        'nontarg_items': "items to be categorized to the left side"
    },

    'de': {
        'targetflr': "...",
        'nontargflr': "..."
    },
    'jp': '日本語'
}

correct = {
    'en': "% correct",
    'de': '% korrekt',
    'jp': '日本語'
}
accrep_feed = {
    'en': 'You will have to repeat this practice round due to a wrong response (or too much waiting).',
    'de': 'Sie müssen die Übungsrunde wegen einer falschen (oder zu langsamen) Antwort wiederholen.',
    'jp': '日本語'
}
acc_feed = {
    'en': ['You will have to repeat this practice round, because of too few correct responses.</b>\n\nYou need at least ', "% accuracy on each item category, but you did not have enough correct responses for the following one(s):"],
    'de': ['Sie müssen die Übungsrunde wegen zu weniger korrekter Antworten wiederholen.</b>\n\nSie benötigen mindestens ', "% richtige Anworten pro Elementkategorie, aber für diese Kategorie(n) hatten Sie zu viele Fehler:"],
    'jp': '日本語'
}

cit_completed = {
    'en': 'Test completed.',
    'de': 'Test abgeschlossen.',
    'jp': '日本語'
}

targs = 'TARGETS_PLACEHOLDER'
nontargs =  'NONTARGS_PLACEHOLDER'
trefs = 'TREFS'
nontrefs = 'NONTREFS'

# instructions preceding given blocks, set based on the selected CIT version
# In English it seems unnecessary, but in other languages, it is often better to clarify that the items appear "one by one". It may also be worthwhile to somehow make it clearer that the "buttons" are just touchscreen surfaces.

        # 0: fillers & target, 1: standard CIT, 2: fillers (no target)
blck_texts = {
    'en': [ 'During the test, various items will appear in the middle of the screen. There will be two buttons displayed on the screen: one on the left side and one on the right side. You have to categorize each item by touching the left button or the right button. There will be three short practice rounds. \n\nIn the first practice round, you have to categorize two kinds of items. ' + '\n\nTouch the <i>right</i> (→■) button when you see any of the following items:\n<div class = "rightitems_list">' + trefs + '</div>Touch the <i>left</i> (■←) button when you see any other item. These other items are:\n' + nontrefs +                'There is a certain time limit for making each response. Please try to be both fast and accurate. In each category, you need at least 80% correct responses in time, otherwise you have to repeat the practice round.</span>',
         
               "<span id='feedback_id2'>In the second practice round, you have to categorize the main test items. The aim of the entire test will be to show whether or not one of these main items is recognized by you. " + 'Touch the <i>right</i> (→■) button when you see the following target item:\n<div class = "rightitems_list">' +
            targs +
            '</div>Touch the <i>left</i> (■←) button when you see any other item. These other items are:\n' +
            nontargs + 'In this practice round, you will have a lot of time to choose each response, but <b>you must respond to each item correctly</b>. If you choose an incorrect response (or not give response for over 10 seconds), you will have to repeat the practice round.' + '</span>',
                
                    "<span id='feedback_id3'>In the third and last practice round all items are present.\n\nYou again have to respond fast, but a certain number of errors is allowed. The task is the same. Touch the <i>right</i> (→■) button when you see the following items:\n<div class = 'rightitems_list'>" + targs + trefs + "</div>Touch the <i>left</i> (■←) button for everything else.</span>"
             ,
                "Now the actual test begins. The task is the same. Touch the <i>right</i> (→■) button when you see the following items:\n<div class = 'rightitems_list'>" + targs + trefs + "</div>Touch the <i>left</i> (■←) button for everything else.\n\nTry to be both accurate and fast."
        ],

    'de': '...',
    'jp': '日本語'
}

