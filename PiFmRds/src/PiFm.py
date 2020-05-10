import os 
from subprocess import call

#def play_freq():
 #   currPath = os.path.dirname(os.path.abspath(__file__))
  #  call(["sudo", currPath + "/pi_fm_rds"])
    #call(["sudo", currPath + "/pi_fm_rds", "-freq", "88.1"])
   # return
def play_freq(freq, song):
    currPath = os.path.dirname(os.path.abspath(__file__))
    call(["sudo", currPath + "/pi_fm_rds", "-freq", freq, "-audio", song])
    return






