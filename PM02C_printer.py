
from PIL import Image, ImageDraw, ImageFont
import serial
#================================= Serial setup ==================================#

try:
    ser = serial.Serial("/dev/ttyUSB0", 4800, timeout=1)
    ser.close()
except:
    print("Brak portu /dev/ttyUSB0")
    x = serial.Serial()

#================================== Variables ====================================#
         #     0     1     2     3     4     5     6     7     8     9     A     B     C     D     E     F
latin2PC = [   '' ,  '' , ''  , ''  , ''  , ''  , ''  , ''  , 'BS', ''  ,r'\n', 'VT', ''  ,r'\r', ''  , ''  # 0
            ,  '' ,  '' , ''  , ''  , ''  , ''  , ''  , ''  , ''  , ''  , ''  ,'ESC', ''  ,  '' , ''  , ''  # 1
            , ' ' , '!' , '"' , '#' , '$' , '%' , '&' ,'\'' , '(' , ')' , '*' , '+' , ',' , '-' , '.' , '/' # 2
            , '0' , '1' , '2' , '3' , '4' , '5' , '6' , '7' , '8' , '9' , ':' , ';' , '<' , '=' , '>' , '?' # 3
            , '@' , 'A' , 'B' , 'C' , 'D' , 'E' , 'F' , 'G' , 'H' , 'I' , 'J' , 'K' , 'L' , 'M' , 'N' , 'O' # 4
            , 'P' , 'Q' , 'R' , 'S' , 'T' , 'U' , 'V' , 'W' , 'X' , 'Y' , 'Z' , '[' , '\\', ']' , '^' , '_' # 5
            , '`' , 'a' , 'b' , 'c' , 'd' , 'e' , 'f' , 'g' , 'h' , 'i' , 'j' , 'k' , 'l' , 'm' , 'n' , 'o' # 6
            , 'p' , 'q' , 'r' , 's' , 't' , 'u' , 'v' , 'w' , 'x' , 'y' , 'z' , '{' , '|' , '}' , '~' , '▲' # 7
            , 'Ç' , 'ü' , 'é' , 'â' , 'ä' , 'á' , 'ć' , 'ç' , 'ł' , 'ë' , 'é' ,  '' , 'î' , 'Ź' , 'Ä' , 'Ć' # 8
            , 'É' , 'æ' , 'Æ' , 'ô' , 'ó' , 'ú' , 'Ś' , 'ś' , 'ö' , 'ü' , 'Ü' , '¢' , '£' , 'Ł' , '₧' , 'ƒ' # 9
            , 'á' , 'í' , 'ó' , 'ú' , 'Ą' , 'ą' , 'ª' , 'º' , 'Ę' , 'ę' , '¬' , 'Ź' , '¼' , '¡' , '«' , '»' # A
            , '░' , '▒' , '▓' , '│' , '┤' , '╡' , '╢' , '╖' , '╕' , '╣' , '║' , '╗' , '╝' , 'Ż' , 'ż' , '┐' # B
            , '└' , '┴' , '┬' , '├' , '─' , '┼' , '╞' , '╟' , '╚' , '╔' , '╩' , '╦' , '╠' , '═' , '╬' , 'Zł'# C
            , '╨' , '╤' , '╥' , '╙' , '╘' , '╒' , '╓' , '╫' , '╪' , '┘' , '┌' , '█' , '▄' , '▌' , '▐' , '▀' # D
            , 'α' , 'ß' , 'Γ' , 'Ń' , 'ń' , 'σ' , 'µ' , 'τ' , 'Φ' , 'Θ' , 'Ω' , 'δ' , '∞' , 'φ' , 'ε' , '∩' # E
            , '≡' , '±' , '≥' , '≤' , '⌠' , '§' , '÷' , '≈' , '°' , '∙' , '·' , '√' , 'ⁿ' , '²' , '■' , '',]# F
param = {
    'Graphics_Mode': False,
    'char_count': 44, # kafka SQ:normal: 44,52,75,88 dense: 88,104,150,176
    'chr_spc': 24,
    'line_spc': 25,
    'VT_spaceing': 32,
    'x_margin': 10,
    'y_margin': 10,
    'x': 0,
    'y': 0,
    'chr_set': 'latin-2_PC',
    'skip_chr': 0,
    'graph_column_cnt': 0,
}
lines = {
#'line_0': [],

}
fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 35)
file = 'wydruk'
#================================== Functions ====================================#
def Serial_recive(port):
    number = 0
    if port.isOpen() == True:              # Odbiór danych z portu szeregowego                    
        activity = False                # Reset stanu aktywności
        while port.isOpen() == True :      # odczyt danych z portu szeregowego
            data = port.readline()
            if data != b'' :
                key_line = f'line_{number}'     #
                lines[key_line] = data          # Zapis danych 
                activity = True                 # Ustalenie stanu aktywnośći 
                print(key_line,' = ',data)
                number = number + 1             # Określenie numeri lini
            if activity == True and data == b'' :
                port.close()
                print("Port zamkniety")
def Find_Code(data,index):
    if param['Graphics_Mode'] == True:
        if param['graph_column_cnt'] <= 1:
            match data[index]:
                case 10:
                    param['y'] = param['y'] + 8
                    param ['Graphics_Mode'] = False
                    return('\n')
    else:
        match data[index]:
            case 27: #ESC
                print('esc found')
                try:
                    match data[index+1]:
                        case 51: #33 '3'
                            param['Graphics_Mode'] = False
                            n = data[index+2]
                            print('ESC 3',n,f'At {index}:{index+2}')
                            param['skip_chr']= 2
                            return[True]
                        case 90: #5A 'Z' graphical quad dinsity 8-dot columns at 240-DPI horisontal ,60-DPI vertical
                            param['Graphics_Mode'] = True
                            nL = data[index+2] #0 ≤ nL ≤ 255
                            nH = data[index+3] #0 ≤ nH ≤ 31
                            k = nH*256
                            k = k+nL   #number of columns
                            param['graph_column_cnt'] = k+1
                            param['skip_chr'] = 3
                            print('ESC Z',f' number of columns ={k}  At {index}:{index+3}')
                            return[True]
                except:
                    print('Cannot match ESC code')           
            case  8:
                param['x'] = param['x'] - param['chr_spc']
                return(True)
            case 10: # \n
                param['y'] = param['y'] + param['line_spc']
                return('\n')
            case 11:
                param['y'] = param['y'] + param['VT_spaceing']
                param['x'] = 0 + param['x_margin']
                return(True)
            case 13: #\r
                param['x'] = 0 +param['x_margin']
                return(True)
    
    return(False)
def Normal_Mode(data,index):
        if data[index] == 27:
            return(True)
        code = latin2PC[data[index]]
        draw.text((param['x'],param['y']),code,font =fnt, fill=(0,0,0,255))
        param['x'] = param['x'] + param['chr_spc']
        return(True)    
def Grapics_mode(data,index):
    scale = 10 ## equals to input data format
    num_of_bits = 8
    out = bin(int(str(data[index]), scale))[2:].zfill(num_of_bits)
    y = param['y']
    for i in out:
        if i == '1':
            draw.point((param['x'],y),fill=(0,0,0,255))
        y = y + 1   
    param['x']=param['x']+1       

#===================================== Main ======================================#
ser.open()
print('Port Open')
Serial_recive(ser)
ser.close()
print('number of lines = ',len(lines))
width = param['char_count'] * param['chr_spc'] + 2 * param['x_margin']
#width = 1100
lenght = len(lines) * param['line_spc'] + 2 * param['y_margin']
im = Image.new("RGB", (width, lenght), (255, 255, 255)) # create an image
draw = ImageDraw.Draw(im)
while True :
    for i in range(len(lines)):
        print(f'line{i}')
        key_line = f'line_{i}'
        raw = lines[key_line]
        
        for chr in range(len(raw)):
            if param['skip_chr'] > 0 :
                param['skip_chr'] = param['skip_chr'] - 1
                continue 
            match Find_Code(raw,chr): #search for codes
                case True:
                    continue
                case '\n':
                    break
            
            if param['Graphics_Mode'] == True:
                Grapics_mode(raw,chr)                           
            else:
                Normal_Mode(raw,chr)
            if param['graph_column_cnt'] == 0:
                param['Graphics_Mode'] = False
            if param['graph_column_cnt'] > 0:
                param['graph_column_cnt'] = param['graph_column_cnt'] - 1 
            
    im.save(file + ".PNG", "PNG")
    print('finished printing')
    break
