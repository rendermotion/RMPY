import maya.cmds as cmds


def disconnect():
	if cmds.commandPort(':7001', q=True):
		cmds.commandPort(name=":7001", cl=True)
		print('disconnecting ":7001"')
	else:
		print('port ":7001" allready disconnected')
	if cmds.commandPort(':7002', q=True):
		cmds.commandPort(name=":7002", cl=True)
		print('disconnecting ":7002"')
	else:
		print('port ":7002" allready disconnected')


def connect():
	if not cmds.commandPort( ":7001", q=True):
		cmds.commandPort(name=":7001", sourceType="mel")
		print('Command Port ":7001" activated')
	else:
		print('Command Port ":7001" allready active')

	if not cmds.commandPort(":7002", q=True):
		cmds.commandPort(name=":7002", sourceType="python")
		print('Command Port ":7002" activated')
	else:
		print('Command Port ":7002" allready active')

