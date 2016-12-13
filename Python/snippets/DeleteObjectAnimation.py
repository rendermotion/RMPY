import maya.cmds as cmds
import RMUncategorized

def deleteobjectListAnimation(ResetControls):
	for eachControl in ResetControls:
		Animation = cmds.listConnections(eachControl,type="animCurve",destination = False)
		if Animation:
			for eachAnim in Animation:
				cmds.delete (eachAnim)
	RMUncategorized.ResetPostoZero (ResetControls)
ResetControls = [u'PedroNew:gunholder_back_R2_ctrl',
	 u'PedroNew:bagLow_L1_ctrl', 
	 u'PedroNew:bagLow_R1_ctrl', 
	 u'PedroNew:gunholder_back_L2_ctrl', 
	 u'PedroNew:ChestBelt_R1_ctrl', 
	 u'PedroNew:Pedro_LF_Tirante_ctrl_BeltChest', 
	 u'PedroNew:gunholder_back_L1_ctrl', 
	 u'PedroNew:gunholder_back_R1_ctrl', 
	 u'PedroNew:armhole_frontLo_L_ctrl', 
	 u'PedroNew:armhole_frontLo_R_ctrl', 
	 u'PedroNew:armhole_frontLo_ctrl', 
	 u'PedroNew:armhole_frontUp_L_ctrl', 
	 u'PedroNew:armhole_frontUp_ctrl', 
	 u'PedroNew:armhole_frontUp_R_ctrl', 
	 u'PedroNew:bagLow_L3_ctrl', 
	 u'PedroNew:bagLow_R3_ctrl', 
	 u'PedroNew:gunholder_back_R2B_ctrl', 
	 u'PedroNew:gunholder_back_R1A_ctrl', 
	 u'PedroNew:gunholder_back_L1A_ctrl', 
	 u'PedroNew:gunholder_back_L2B_ctrl', 
	 u'PedroNew:armhole_chestFront_R_ctrl', 
	 u'PedroNew:RH_armholeshoulderBack_ctrl', 
	 u'PedroNew:armhole_shoulderFront_R_ctrl', 
	 u'PedroNew:armhole_chestBack_L_ctrl', 
	 u'PedroNew:armhole_bagFront_up_L_ctrl', 
	 u'PedroNew:bagLow_L2_ctrl', 
	 u'PedroNew:armhole_bagBack_up_R_ctrl', 
	 u'PedroNew:armhole_chestFront_L_ctrl', 
	 u'PedroNew:armhole_shoulderFront_L_ctrl', 
	 u'PedroNew:armhole_chestBack_R_ctrl', 
	 u'PedroNew:Pedro_LF_armholebagFrontup_ctrl_belts', 
	 u'PedroNew:bagLow_R2_ctrl', 
	 u'PedroNew:armhole_bagBack_up_L_ctrl', 
	 u'PedroNew:armhole_back_L_ctrl', 
	 u'PedroNew:RH_armholeback_ctrl']
