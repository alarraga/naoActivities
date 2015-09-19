import walk
import walkBackward
import standUp
import turnLeft
import turnRight
import dance
import colorName
import sit
import lyingBack
import lyingBelly 
import sitRelax

def leertxt(nombre, IP):
    ofile = open(nombre,'r')
    linea = ofile.readline()
    while linea!="":
        print linea
        if (linea.strip() == 'Turn Left'):
            turnLeft.main(IP, 6)
        if (linea.strip() == 'Turn Right'):
            turnRight.main(IP, 6)
        if (linea.strip() == 'Dance'):
            dance.main(IP)
        if (linea.strip() == 'Sit Down'):
            sit.main(IP)
        if (linea.strip() == 'Stand Up'):
            standUp.main(IP)
        if (linea.strip() == 'Crouch'):
            crouch.main(IP)
        if (linea.strip() == 'Lay Down'):
            lyingBack.main(IP)
        if (linea.strip() == 'Lay on Belly'):
            lyingBELLY.main(IP)
        if (linea.strip() == 'Sit Relax'):
            sitRelax.main(IP)
        if (linea[0:6] == 'Detect'):
            colorName.main(IP)            


        linea=ofile.readline()
        
    ofile.close()


if __name__ == '__main__':
    # execute as script
    IP = "192.168.0.1"
    leertxt('example.txt', IP) #send the file exported
	
    
