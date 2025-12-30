def senjata(gun="sniper"):
    def tembak():
        print(f"menembakan peluru {gun}")
        # return f"menembakan peluru {gun}"
    
    return tembak

senjata(gun="pistol")