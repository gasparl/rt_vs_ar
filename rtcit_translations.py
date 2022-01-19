# this files contains all instructions and filler words used in the CIT

lg = 'jp'

lgs = {
    'en': 'English',
    'de': 'Deutsch',
    'jp': '日本語'
}

# target-side default fillers
targetref_words_orig = {
    # these words are not to be translated literally one by one. The translations should always try to find the simplest, clearest words that relate to relevance, familiarity, recognition, importance. (The English 'MINE' is actually not the best, but it's good to also have a shorter word and this fits there.)
    'en': ['FAMILIAR', 'MINE', 'RECOGNIZED'],
    'de': ['VERTRAUT', 'MEIN', 'RELEVANT'],
    'jp': ['関連する', '重要な', '知ってる']
}

# nontarget-side default fillers
nontargref_words_orig = {
    # these should have the meaning opposite of    relevance, familiarity, importance
    'en': ['FOREIGN', 'IRRELEVANT', 'OTHER', 'RANDOM', 'THEIRS', 'UNFAMILIAR'],
    'de': ['IRRELEVANT', 'FREMD', 'UNBEKANNT', 'ANDERE', 'SONSTIGES', 'UNVERTRAUT'],
    'jp': ['9999', '88888', '777', '66666', '555', '4444']
}

move_on = {
    'en': '\n\nPress Space to move on.',
    'de': '\n\nStart',
    'jp': '\n\nスペースキーを押して次に進んでください。'
}

show_inst = {
    'en': ' If needed, press Enter to read the full instructions again.',
    'de': '...',
    'jp': '\n必要であれば、Enterキーを押すと全ての教示を読み直せます。'
}

tostart = {
    'en': 'Press space to start.',
    'de': '...',
    'jp': 'スペースキーを押して課題を始めてください。'
}

feedtooslo = {
    'en': 'Too slow!',
    'de': 'Zu langsam!',
    'jp': '反応が遅すぎます！'
}
feedwrong = {
    'en': 'Wrong!',
    'de': 'Falsch!',
    'jp': '間違い！'
}

acc_feed1 = {
    'en': 'You will have to repeat this practice round due to a wrong response (or too much waiting).',
    'de': 'Sie müssen die Übungsrunde wegen einer falschen (oder zu langsamen) Antwort wiederholen.',
    'jp': '間違った反応(あるいは回答までの時間が長すぎる)のため、この練習試行をやり直します。'
}

acc_feed2 = {
    'en': {
        'targs': 'You will have to repeat this practice round because of too few correct responses to the items to be categorized with the right ("I") key. Please pay more attention to these items!',
        'nontargs': 'You will have to repeat this practice round because of too few correct responses to the items to be categorized with the left ("E") key. Please pay more attention to these items!',
        'allits': 'You will have to repeat this practice round because of too few correct responses to all the item types. Please pay more attention!'
    },
    'de': '...',
    'jp': {
        'targs': '右のキー("I")に分類されるべき項目への正答数が少ないためこの練習試行をやり直します。\nこれらの項目に注意してください。',
        'nontargs': '左のキー("E")に分類されるべき項目への正答数が少ないためこの練習試行をやり直します。\nこれらの項目に注意してください。',
        'allits': '全ての項目に対する正答数が少ないためこの練習試行をやり直します。'
    }
}

completed = {
    'en': 'Test completed. Please inform the experiment leader.',
    'de': '...',
    'jp': 'これで実験を終了します。\n実験者に声をかけてください。'
}

targs = 'TARGETS_PLACEHOLDER1'
nontargs = 'NONTARGS_PLACEHOLDER2'
trefs = 'TARGREFS_PLACEHOLDER3'
nontrefs = 'NONTREFS_PLACEHOLDER4'
comma = {
    'en': ', ',
    'de': ', ',
    'jp': '、'
}
cmma = comma[lg]

# instructions preceding given blocks, set based on the selected CIT version
# In English it seems unnecessary, but in other languages, it is often better to clarify that the items appear 'one by one'.
blck_texts = {
    'en': [
        # block 1
        'During the following test, various items will appear in the middle of the screen. You have to categorize each item by pressing the key "E" on the left or the key "I" on the right. There will be three short practice rounds.\n\nIn the first practice round, you have to categorize two kinds of items. \n\nPress the right ("I") key when you see any of the following items (referring to familiarity with the crime details): ' + trefs +
        '.\nPress the left ("E") key when you see any other item. These other items are: ' + nontrefs + \
        '.\n\nThere is a certain time limit for making each response. Please try to be both fast and accurate. In each of the two item categories, you need at least 80% correct responses in time, otherwise you have to repeat the practice round.',
        # block 2
        'In the second practice round, you have to categorize the main test items. The aim of the entire test will be to show whether or not one of these main items (a crime detail) is recognized by you.\n\nPress the right ("I") key when you see the following target item: ' + targs +
        '.\nPress the left ("E") key when you see any other item. These other items are: ' + nontargs + \
        '.\nIn this practice round, you will have a lot of time to choose each response, but you must respond to each item correctly. If you choose an incorrect response (or not give response for over 10 seconds), you will have to repeat the practice round.',
        # block 3
        'In the third and last practice round all items are present.\n\nYou again have to respond fast, but a certain number of errors is allowed. The task is the same. Press the right ("I") key when you see the following items: ' + targs + cmma + trefs +
        '. Press the left ("E") key for everything else.',
        # block 4
        'Now the actual test begins. The task is the same. Press the right ("I") key when you see the following items: ' + targs + cmma + trefs +
        '. Press the left ("E") key for everything else.',
        # block 5
        'Now the main words will be different. Press the right ("I") key when you see the following "target" item: ' + targs +
        '. Press the left ("E") key when you see any of the following items: ' + nontargs + \
        '.\n\nTo make sure you understood this, in the following short practice round, you must respond to each item correctly, otherwise you have to repeat this round.',
        # block 6
        'Alright. The next block starts. The task is the same. Press the right ("I") key, when you see any of the following items: ' + targs + cmma + trefs +
        '. Press the left ("E") key when you see any other item.'],
    'de': '...',
    'jp': [
        # block 1
        'これから始まる課題では、さまざまな項目が画面中央に提示されます。\n各項目は一度に1つずつ画面に提示されます。\nこの課題では、それぞれの項目を正しく分類することが求められます。\n項目の分類は、左のキー("E")あるいは右のキー("I")を押して行ってください。\n実験の本試行を開始する前に、3回の短い練習試行が設けられています。\n\n1回目の練習試行では、2種類の項目を分類することが求められます。\n\n以下の項目が提示された場合には右のキー("I")を押してください：\n' + \
        trefs + ' \n\nまた、以下の項目が提示された場合には左のキー("E")を押してください：\n' + nontrefs + \
        '\n\n各項目に対する反応には制限時間があります。\n従って、各項目にはできるだけ速く、そして正確に反応してください。\nこの練習試行では、2種類の両項目に対して、\n制限時間内に最低でも正答率80%を達成しなければなりません。\n正答率がこの基準を下回った場合、練習試行をやり直す必要があります。',
        # block 2
        '2回目の練習試行では、主要テスト項目を分類することが求められます。\nこの練習試行の主な目的は、あなたが主要なテスト項目の一つ(架空犯罪の詳細)\nを理解できているかどうかを確かめることです。\n\n以下にある"ターゲット"項目(特に注意を払うべき項目)を見た場合には右のキー("I")を押してください:\n' + targs + \
        '。\nそれ以外の項目が提示された場合には左のキー("E")を押してください。\nそれ以外の項目は:\n' + nontargs + \
        '。\n\nこの練習試行では、各項目について選択をする機会がたくさんありますが、\n各項目に対して正確に反応する必要があります。\n誤反応(あるいは10秒以上反応をしなかった場合)、この練習試行をやり直す必要があります。',
        # block 3
        '3回目の練習試行では(これが最後の練習ラウンドになります)、全ての項目が提示されます。\n\nこの練習試行でも、できるだけ速く反応することが求められますが、\n数回程度であれば間違えても問題はありません。\n課題自体は全く同じです。\n以下の項目を見た場合には右のキー("I")を押してください:\n' + \
        targs + cmma + trefs + '。\n他の項目を見た場合には左のキー("E")を押してください。',
        # block 4
        'ここから、本試行が始まります。\n課題自体は全く同じです。\n以下の項目を見た場合には右のキー("I")を押してください:\n' + \
        targs + cmma + trefs + '。\n他の項目を見た場合には左のキー("E")を押してください。',
        # block 5
        'この課題では、主要な単語が異なります。\n以下にある"ターゲット"項目(特に注意を払うべき項目)を見た場合には右のキー("I")を押してください:\n' + targs + '。\n以下にある項目が提示された場合には左のキー("E")を押してください\n' + \
        nontargs + '。\n\nあなたがこの課題を正確に理解しているかどうかを確かめるために、短い練習試行を設けてあります。\nこの練習試行では、各項目に正確に反応することが求められます。\n誤答があった場合、この練習試行をやり直す必要があります。',
        # block 6
        '次のブロックが始まります。\n課題自体は全く同じです。\n以下の項目を見た場合には右のキー("I")を押してください:\n' + targs + cmma + trefs + '。\n他の項目を見た場合には左のキー("E")を押してください。']
}
