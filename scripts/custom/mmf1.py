if starting:
    boolAddress = mmf.RegisterBool()
    intAddress = mmf.RegisterInt()
    floatAddress = mmf.RegisterFloat()
    doubleAddress = mmf.RegisterDouble()
    mmf.Open("mmf-test")
    intValue = 0
    doubleValue = 0
    
intValue = intValue + 1
doubleValue = doubleValue + 0.0001

mmf.WriteInt(intAddress, intValue)
mmf.WriteDouble(doubleAddress, doubleValue)

diagnostics.watch(mmf.ReadBool(boolAddress))
diagnostics.watch(intValue)
diagnostics.watch(mmf.ReadFloat(floatAddress))
diagnostics.watch(doubleValue)