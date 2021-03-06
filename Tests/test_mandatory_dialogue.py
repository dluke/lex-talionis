# Tests mandatory Dialogue
import os
import pstats
import cProfile

import pygame
import pyautogui

import Code.GlobalConstants as GC
import Code.SaveLoad as SaveLoad
import Code.GameStateObj as GameStateObj
import Code.Dialogue as Dialogue
import Code.Engine as Engine

import logging

pyautogui.PAUSE = 0
GC.DISPLAYSURF = pygame.display.set_mode((GC.WINWIDTH, GC.WINHEIGHT))

my_level = logging.DEBUG
logging.basicConfig(filename='Tests/debug.log.test', filemode='w', level=my_level,
                    disable_existing_loggers=False, format='%(levelname)8s:%(module)20s: %(message)s')

def main():
    gameStateObj = GameStateObj.GameStateObj()
    metaDataObj = {}
    gameStateObj.build_new()
    scripts = ['preBase', 'in_base_', 'narration', 'intro', 'prep', 'turnChange', 'move',
               'menu', 'attack', 'interact']
    for num in range(0, GC.cf.CONSTANTS['num_levels']):
        print('Level: %s'%num)
        levelfolder = 'Data/Level' + str(num)
        SaveLoad.load_level(levelfolder, gameStateObj, metaDataObj)
        print('Num Units: %s  Map Size: %s'%(len(gameStateObj.allunits), gameStateObj.map.width*gameStateObj.map.height))
        if num == 3:
            for script in scripts:
                fp = levelfolder + '/' + script + 'Script.txt'
                run(gameStateObj, metaDataObj, fp)
            for _ in range(20):
                gameStateObj.turncount += 1
                fp = levelfolder + '/turnChangeScript.txt'
                run(gameStateObj, metaDataObj, fp)
            fp = levelfolder + '/outroScript.txt'
            run(gameStateObj, metaDataObj, fp)
        gameStateObj.clean_up()
        print('Num Units Remaining: %s'%(len(gameStateObj.allunits)))

def run(gameStateObj, metaDataObj, fp):
    if os.path.exists(fp):
        print(fp)
        gameStateObj.message.append(Dialogue.Dialogue_Scene(fp, optionalunit=gameStateObj.allunits[0]))
        gameStateObj.stateMachine.changeState('dialogue')
        counter = 0
        while gameStateObj.message:
            Engine.update_time()
            counter += 1
            if not counter%50:
                pyautogui.press('x')
            eventList = Engine.build_event_list()
            mapSurf, repeat = gameStateObj.stateMachine.update(eventList, gameStateObj, metaDataObj)
            while repeat:
                mapSurf, repeat = gameStateObj.stateMachine.update(eventList, gameStateObj, metaDataObj)
            GC.DISPLAYSURF.blit(mapSurf, (0, 0))
            pygame.display.update()

if __name__ == '__main__':
    cProfile.run("main()", "Profile.prof")
    s = pstats.Stats("Profile.prof")
    s.strip_dirs().sort_stats("time").print_stats(20)
    os.remove("Profile.prof")
