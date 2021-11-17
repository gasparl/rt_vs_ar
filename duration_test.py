from psychopy.visual import Window, Rect 
from psychopy.core import wait, quit
from psychopy.hardware import keyboard
win = Window([500, 500], color='gray', fullscr = False,
                 screen = 1, units = 'pix', allowGUI = False)
rec = Rect(win = win, width=400, height=400, units='pix', fillColor='white', autoDraw=True)
kb = keyboard.Keyboard()
   
    
for i in range(3):
    print('#########----------', str(i+1))
    wait(0.5)
    rec.fillColor = 'green'
    win.callOnFlip(kb.clock.reset)
    win.flip()
    kb.clearEvents()
    starting  = (kb.clock.getTime())
    response = kb.waitKeys(maxWait = 5, waitRelease = False, clear=False,
                           keyList=['e', 'i'])
    rec.fillColor = 'purple'
    win.flip()  
    if not response:
        rt_start = kb.clock.getTime()
        resp_key = 'NA'
        press_dur = 'NA'
    else:
        resp_key = response[0].name
        rt_start = response[0].rt
        press_dur = response[0].duration
    print(resp_key)
    print(rt_start)
    print('press_dur1')
    print(press_dur)
    
    wait(2, hogCPUperiod = 0)
    rec.fillColor = 'blue'
    win.flip()  
    
    response2 = kb.getKeys(keyList=['e', 'i'])
    print('response2')
    if response2:
        print(response2[0].name)
        print(response2[0].rt)
        print('press_dur2')
        print(response2[0].duration)
    else:
        print('nonnne')
    
print('THE END')
    