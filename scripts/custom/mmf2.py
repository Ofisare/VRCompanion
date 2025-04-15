if starting:
    boolAddress = mmf.RegisterBool()
    intAddress = mmf.RegisterInt()
    floatAddress = mmf.RegisterFloat()
    doubleAddress = mmf.RegisterDouble()
    mmf.Open("mmf-test")
    boolValue = True
    floatValue = 0
    
boolValue = not boolValue
floatValue = floatValue + 0.0001

mmf.WriteBool(boolAddress, boolValue)
mmf.WriteFloat(floatAddress, floatValue)

diagnostics.watch(boolValue)
diagnostics.watch(mmf.ReadInt(intAddress))
diagnostics.watch(floatValue)
diagnostics.watch(mmf.ReadDouble(doubleAddress))