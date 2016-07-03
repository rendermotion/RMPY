def RMPyArrayToMelArray(Array):
	print type(Array)
	Txt="{"
	for g in range(0,Array):
		Txt+="\""
		Txt+=g
		Txt+="\""
		Txt+=","
	Txt=Txt[:-1]
	Txt+="}"
	return Txt

