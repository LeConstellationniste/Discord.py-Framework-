# Other imports:
# 	Dont forget to import here files who contain
# 	variable used in the cmds
import command as create
import bot 


#from baseLauncher import client


#commands imports
import commands.testCmds as testcm

#checks imports
import checks.checksTest as testch

commandSet1=[]
# behind is your command set. All the cmds are created here.
commandSet1.append(create.Command("test", testcm.testFunc, testch.checkOne))

print("test")
