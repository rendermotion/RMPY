import maya.cmds as cmds


def disconnect():
    if (cmds.commandPort(':4434', q=True)):
        cmds.commandPort(name=":4434", cl=True)
        print 'disconnecting ":4434"'
    else:
        print 'port ":4434" allready disconnected'


def connect():
    if not cmds.commandPort(":4434", q=True):
        cmds.commandPort(name=":4434")
        print 'Command Port ":4434" activated'
    else:
        print 'Command Port ":4434" allready active'
