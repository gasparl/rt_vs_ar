/*jshint esversion: 6 */

let subj_id, guilt, cit_order, block_order, probe_set, item_sets, item_cats, filename_to_dl;


all_items = {
    1: {
        "banks": [
            'みずほ銀行', // (Mizuho Bank)
            'りそな銀行', // (Risona Bank)
            'スルガ銀行', // (Suruga Bank)
            'セブン銀行', // (Seven Bank)
            'イオン銀行', // (Aeon Bank)
            'ソニー銀行' // (Sony Bank)
        ],
        "names": [
            '桜井 優希', // (Sakurai Yuki)
            '野口 夏樹', // (Noguchi Natsuki)
            '谷口 千里', // (Taniguchi Chisato)
            '岩崎 未来', // (Iwasaki Mirai)
            '内田 日向', // (Uchida Hinata)
            '木下 浩実' // (Kinoshita Hiromi)
        ]
    },
    2: {
        "banks": [
            '横浜銀行', // (Bank of Yokohama)
            '足利銀行', // (Ashikaga Bank)
            '千葉銀行', // (Chiba Bank)
            '筑波銀行', // (Tsukuba Bank)
            '群馬銀行', // (Gunma Bank)
            '常陽銀行' // (Joyo Bank)
        ],
        "names": [
            '新井 純', // (Arai Jun)
            '武田 司', // (Takeda Tsukasa)
            '小田 薫', // (Oda Kaoru)
            '佐野 忍', // (Sano Shinobu)
            '上野 律', // (Ueno Ritsu)
            '松井 望' // (Matsui Nozomi)
        ]
    }
};

function subj_info() {
    subj_id = document.getElementById('subj_num').value;
    let subj_num = parseInt(subj_id) - 1;
    let type_ans = 'ポリグラフ検査';
    let type_rt = '反応時間測定をベースとした';
    if (subj_id != '' && subj_num > -1 && subj_num <= 200) {
        if (Math.floor(subj_num) % 2 == 0) {
            guilt = 'guilty';
        } else {
            guilt = 'innocent';
        }
        if (Math.floor(subj_num / 2) % 2 == 0) {
            cit_order = 'RT_ANS';
            document.getElementById('cit1').textContent = type_rt;
            document.getElementById('cit11').textContent = type_rt;
            document.getElementById('cit2').textContent = type_ans;
            document.getElementById('cit22').textContent = type_ans;
        } else {
            cit_order = 'ANS_RT';
            document.getElementById('cit1').textContent = type_ans;
            document.getElementById('cit11').textContent = type_ans;
            document.getElementById('cit2').textContent = type_rt;
            document.getElementById('cit22').textContent = type_rt;
        }
        if (Math.floor(subj_num / 4) % 2 == 0) {
            set_order = '1_2';
            item_sets = [1, 2];
        } else {
            set_order = '2_1';
            item_sets = [2, 1];
        }
        if (Math.floor(subj_num / 8) % 2 == 0) {
            block_order = 'banks_names';
            item_cats = ['banks', 'names'];
        } else {
            block_order = 'names_banks';
            item_cats = ['names', 'banks'];
        }
        if (subj_num < 40) {
            probe_set = 1;
        } else if (subj_num < 80) {
            probe_set = 2;
        } else if (subj_num < 120) {
            probe_set = 3;
        } else if (subj_num < 160) {
            probe_set = 4;
        } else if (subj_num < 200) {
            probe_set = 5;
        } else {
            alert('subject number must be between 1 and 200');
            console.log('subject number must be between 1 and 200');
        }
        document.getElementById('subj_num_re').textContent = subj_id;
        document.getElementById('guilt').textContent = guilt[0];
        document.getElementById('cit_order').textContent = cit_order;
        document.getElementById('set_order').textContent = set_order;
        document.getElementById('block_order').textContent = block_order;
        document.getElementById('probe_set').textContent = probe_set;
        document.getElementById('start_btn').style.display = 'block';
    } else {
        alert('subject number must be between 1 and 200');
        console.log('subject number must be between 1 and 200');
    }
}

function start() {
    filename_to_dl = 'exp_rt_vs_ar_qa_' + subj_id + '_' + neat_date() + '.txt';
    if (guilt == 'innocent') {
        let els = document.getElementsByClassName('g_only');
        for (var i = 0; i < els.length; i++) {
            els[i].style.display = 'none';
        }
    }
    document.getElementById('outro_start').style.display = 'none';
    document.getElementById('outro_main').style.display = 'block';
    create_stim_base();
}

let all_probes = [];
let words_lists = [];

function create_stim_base() {

    item_sets.forEach((it_set, num1) => {
        words_lists.push([]);
        item_cats.forEach((itemskey, num2) => {
            itemlist = all_items[it_set][itemskey];
            words_lists[num1].push([]);
            itemlist.forEach((item, indx) => {
                if ((probe_set - 1) === indx) {
                    words_lists[num1][num2].push(item);
                    all_probes.push(item);
                } else if (probe_set !== indx) {
                    words_lists[num1][num2].push(item);
                }
            });
            words_lists[num1][num2] = words_lists[num1][num2].sort(function(a, b) {
                return a.localeCompare(b);
            });
            words_lists[num1][num2].push("わからない");
        });
    });
    words_lists.forEach((wbase, ind1) => {
        wbase.forEach((wlist, ind2) => {
            let radopts = "";
            wlist.forEach(function(word) {
                radopts += word + ' <input type="radio" name="pch' + (ind1 + 1) + ind2 + '" value="' + word + '"><br>';
            });
            let el = document.getElementById('div_pcheck' + (ind1 + 1) + ind2);
            el.innerHTML += radopts;
        });
    });
}

let pchosen;
let pcount1 = 0;
let pcount2 = 0;

function submit() {
    document.getElementById('outro_main').style.display = 'none';
    let len = 9;
    let pfeed = '';
    pchosen = [];
    if (guilt == 'guilty') {
        ['pch10', 'pch11', 'pch20', 'pch21'].forEach((prob) => {
            let p_chk = document.querySelector('input[name="' + prob + '"]:checked');
            pchosen.push(p_chk ? p_chk.value : undefined);
        });
        len = pchosen.filter((v) => {
            return v !== undefined;
        }).length;
        pchosen.forEach((seldprobe, idx) => {
            theprob = all_probes[idx];
            if (seldprobe == theprob) {
                pfeed += seldprobe + ' -> <b>correct (' + theprob + ')</b><br>';
                if (idx < 2) {
                    pcount1 += 1;
                } else {
                    pcount2 += 1;
                }
            } else {
                pfeed += '<span style="color:red">' + seldprobe + ' -> <b>INCORRECT (' + theprob + ')</b></span><br>';
            }
        });
        pfeed += '<br>Correct count: ' + pcount1 + ' (first test) and ' + pcount2 + ' (second test) out of all 4.';
    } else {
        pfeed = "(Not guilty.)";
        all_probes = [];
        pcount1 = '';
        pcount2 = '';
    }
    document.getElementById('probsfeed').innerHTML = pfeed;
    if (len < 4) {
        document.getElementById('outro_main').style.display = 'block';
        alert('4つの項目リストから好きな項目を1つ選択してください。');
    } else {
        window.scrollTo(0, 0);
        document.getElementById('outro_end').style.display = 'block';
    }
}

function moveon() {
    document.getElementById('outro_end').style.display = 'none';
    if (guilt == 'guilty') {
        document.getElementById('outro_check_g').style.display = 'block';
    } else {
        document.getElementById('outro_check_i').style.display = 'block';
    }
}

let outro_data = '';

function end_save() {
    show_check = document.getElementById('show_check').value;
    if (guilt == 'innocent' || ['y', 'n'].includes(show_check)) {
        document.getElementById('outro_check_g').style.display = 'none';
        document.getElementById('outro_check_i').style.display = 'none';
        let gend_chk = document.querySelector('input[name="gender"]:checked');
        let gender = gend_chk ? gend_chk.value : 'NA';
        let age = document.getElementById('age').value;
        let ncomment = document.getElementById('ncomment').value;

        let scales = ['realism', 'anxiety', 'excitement',
            'detected1', 'detected2', 'accuracy1', 'accuracy2'
        ];
        let rats = [];
        scales.forEach((scl) => {
            if (document.getElementById(scl).classList.contains("slider_hide_thumb")) {
                rats.push('NA');
            } else {
                rats.push(document.getElementById(scl).value);
            }
        });

        outro_data += ['subject_id', 'guilt', 'cit_order', 'set_order', 'block_order', 'probe_set', 'age', 'gender', 'selected_probes', 'actual_probes', 'correct_selected1', 'correct_selected2', 'attention', 'corrects_noted', 'comment'].join('\t') + '\t' + scales.join('\t') + '\n' + [subj_id, guilt, cit_order, set_order, block_order, probe_set, age, gender, pchosen.join('|'), all_probes.join('|'), pcount1, pcount2, attcount, show_check, ncomment].join('\t') + '\t' + rats.join('\t') + '\n';

        console.log(outro_data);
        document.getElementById('data_display').innerHTML = filename_to_dl + "\n" + outro_data + '\n\n\n<button onclick="dl_as_file();"> try saving again </button>\n\n\n<button onclick="copy_to_clip();"> copy to clipboard </button>';
        dl_as_file();
    }
}

function dl_as_file() {
    data_to_dl = outro_data;
    let blobx = new Blob([data_to_dl], {
        type: 'text/plain'
    });
    let elemx = window.document.createElement('a');
    elemx.href = window.URL.createObjectURL(blobx);
    elemx.download = filename_to_dl;
    document.body.appendChild(elemx);
    elemx.click();
    document.body.removeChild(elemx);
}

function copy_to_clip() {
    let textarea = document.createElement("textarea");
    textarea.textContent = filename_to_dl + "\n" + outro_data;
    textarea.style.position = "fixed";
    document.body.appendChild(textarea);
    textarea.select();
    try {
        return document.execCommand("copy");
    } catch (ex) {
        console.warn("Copy to clipboard failed.", ex);
        return false;
    } finally {
        document.body.removeChild(textarea);
    }
}

function neat_date() {
    let m = new Date();
    return m.getFullYear() + "" +
        ("0" + (m.getMonth() + 1)).slice(-2) + "" +
        ("0" + m.getDate()).slice(-2) + "_" +
        ("0" + m.getHours()).slice(-2) + "" +
        ("0" + m.getMinutes()).slice(-2);
}


//only allow number in input field
function validate(evt) {
    let theEvent = evt || window.event;
    let key = theEvent.keyCode || theEvent.which;
    key = String.fromCharCode(key);
    let regex = /[0-9]/;
    if (!regex.test(key)) {
        theEvent.returnValue = false;
        if (theEvent.preventDefault) theEvent.preventDefault();
    }
}

function yesno(evt) {
    let theEvent = evt || window.event;
    let key = theEvent.keyCode || theEvent.which;
    key = String.fromCharCode(key);
    if (key == 'n') {
        document.getElementById('savebutt').style.display = 'none';
        document.getElementById('explain').style.display = 'block';
    } else if (key == 'y') {
        document.getElementById('explain').style.display = 'none';
        document.getElementById('savebutt').style.display = 'block';
    } else {
        theEvent.returnValue = false;
        if (theEvent.preventDefault) theEvent.preventDefault();
    }
}


let attcount = 0;

function attchecks() {
    document.getElementById("attcheck_id").classList.remove("slider_hide_thumb");
    attcount++;
    if (attcount > 2) {
        document.getElementById('attdiv').innerHTML = "<br><b>ありがとうございます。回答を続けてください。</b><br><br>";
    }
}
