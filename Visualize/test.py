# Cái cu ni nè, font chữ nó không hỗ trợ tiếng việt, nên nó không hiển thị được tiếng việt

# import pygame module
import pygame
from unidecode import unidecode
# import time module
import time

txt = "à"
BANG_DANH_DAU = {
    "vni": {
                   "Á": "A1" , "À": "A2" , "Ả": "A3" , "Ã": "A4" , "Ạ": "A5" ,
        "Ă": "A8", "Ắ": "A81", "Ằ": "A82", "Ẳ": "A83", "Ẵ": "A84", "Ặ": "A85",
        "Â": "A6", "Ấ": "A61", "Ầ": "A62", "Ẩ": "A63", "Ẫ": "A64", "Ậ": "A65",
        "Đ": "D9",
                   "É": "E1" , "È": "E2" , "Ẻ": "E3" , "Ẽ": "E4" , "Ẹ": "E5" ,
        "Ê": "E6", "Ế": "E61", "Ề": "E62", "Ể": "E63", "Ễ": "E64", "Ệ": "E65",
                   "Í": "I1" , "Ì": "I2" , "Ỉ": "I3" , "Ĩ": "I4" , "Ị": "I5" ,
                   "Ó": "O1" , "Ò": "O2" , "Ỏ": "O3" , "Õ": "O4" , "Ọ": "O5" ,
        "Ô": "O6", "Ố": "O61", "Ồ": "O62", "Ổ": "O63", "Ỗ": "O64", "Ộ": "O65",
        "Ơ": "O7", "Ớ": "O71", "Ờ": "O72", "Ở": "O73", "Ỡ": "O74", "Ợ": "O75",
                   "Ú": "U1" , "Ù": "U2" , "Ủ": "U3" , "Ũ": "U4" , "Ụ": "U5" ,
        "Ư": "U7", "Ứ": "U71", "Ừ": "U72", "Ử": "U73", "Ữ": "U74", "Ự": "U75",
                   "Ý": "Y1" , "Ỳ": "Y2" , "Ỷ": "Y3" , "Ỹ": "Y4" , "Ỵ": "Y5" ,
                   "á": "a1" , "à": "a2" , "ả": "a3" , "ã": "a4" , "ạ": "a5" ,
        "ă": "a8", "ắ": "a81", "ằ": "a82", "ẳ": "a83", "ẵ": "a84", "ặ": "a85",
        "â": "a6", "ấ": "a61", "ầ": "a62", "ẩ": "a63", "ẫ": "a64", "ậ": "a65",
        "đ": "d9",
                   "é": "e1" , "è": "e2" , "ẻ": "e3" , "ẽ": "e4" , "ẹ": "e5" ,
        "ê": "e6", "ế": "e61", "ề": "e62", "ể": "e63", "ễ": "e64", "ệ": "e65",
                   "í": "i1" , "ì": "i2" , "ỉ": "i3" , "ĩ": "i4" , "ị": "i5" ,
                   "ó": "o1" , "ò": "o2" , "ỏ": "o3" , "õ": "o4" , "ọ": "o5" ,
        "ô": "o6", "ố": "o61", "ồ": "o62", "ổ": "o63", "ỗ": "o64", "ộ": "o65",
        "ơ": "o7", "ớ": "o71", "ờ": "o72", "ở": "o73", "ỡ": "o74", "ợ": "o75",
                   "ú": "u1" , "ù": "u2" , "ủ": "u3" , "ũ": "u4" , "ụ": "u5" ,
        "ư": "u7", "ứ": "u71", "ừ": "u72", "ử": "u73", "ữ": "u74", "ự": "u75",
                   "ý": "y1" , "ỳ": "y2" , "ỷ": "y3" , "ỹ": "y4" , "ỵ": "y5" ,
    },
    "telex": {
                   "Á": "AS" , "À": "AF" , "Ả": "AR" , "Ã": "AX" , "Ạ": "AJ" ,
        "Ă": "AW", "Ắ": "AWS", "Ằ": "AWF", "Ẳ": "AWR", "Ẵ": "AWX", "Ặ": "AWJ",
        "Â": "AA", "Ấ": "AAS", "Ầ": "AAF", "Ẩ": "AAR", "Ẫ": "AAX", "Ậ": "AAJ",
        "Đ": "DD",
                   "É": "ES" , "È": "EF" , "Ẻ": "ER" , "Ẽ": "EX" , "Ẹ": "EJ" ,
        "Ê": "EE", "Ế": "EES", "Ề": "EEF", "Ể": "EER", "Ễ": "EEX", "Ệ": "EEJ",
                   "Í": "IS" , "Ì": "IF" , "Ỉ": "IR" , "Ĩ": "IX" , "Ị": "IJ" ,
                   "Ó": "OS" , "Ò": "OF" , "Ỏ": "OR" , "Õ": "OX" , "Ọ": "OJ" ,
        "Ô": "OO", "Ố": "OOS", "Ồ": "OOF", "Ổ": "OOR", "Ỗ": "OOX", "Ộ": "OOJ",
        "Ơ": "OW", "Ớ": "OWS", "Ờ": "OWF", "Ở": "OWR", "Ỡ": "OWX", "Ợ": "OWJ",
                   "Ú": "US" , "Ù": "UF" , "Ủ": "UR" , "Ũ": "UX" , "Ụ": "UJ" ,
        "Ư": "UW", "Ứ": "UWS", "Ừ": "UWF", "Ử": "UWR", "Ữ": "UWX", "Ự": "UWJ",
                   "Ý": "YS" , "Ỳ": "YF" , "Ỷ": "YR" , "Ỹ": "YX" , "Ỵ": "YJ" ,
                   "á": "as" , "à": "af" , "ả": "ar" , "ã": "ax" , "ạ": "aj" ,
        "ă": "aw", "ắ": "aws", "ằ": "awf", "ẳ": "awr", "ẵ": "awx", "ặ": "awj",
        "â": "aa", "ấ": "aas", "ầ": "aaf", "ẩ": "aar", "ẫ": "aax", "ậ": "aaj",
        "đ": "dd",
                   "é": "es" , "è": "ef" , "ẻ": "er" , "ẽ": "ex" , "ẹ": "ej" ,
        "ê": "ee", "ế": "ees", "ề": "eef", "ể": "eer", "ễ": "eex", "ệ": "eej",
                   "í": "is" , "ì": "if" , "ỉ": "ir" , "ĩ": "ix" , "ị": "ij" ,
                   "ó": "os" , "ò": "of" , "ỏ": "or" , "õ": "ox" , "ọ": "oj" ,
        "ô": "oo", "ố": "oos", "ồ": "oof", "ổ": "oor", "ỗ": "oox", "ộ": "ooj",
        "ơ": "ow", "ớ": "ows", "ờ": "owf", "ở": "owr", "ỡ": "owx", "ợ": "owj",
                   "ú": "us" , "ù": "uf" , "ủ": "ur" , "ũ": "ux" , "ụ": "uj" ,
        "ư": "uw", "ứ": "uws", "ừ": "uwf", "ử": "uwr", "ữ": "uwx", "ự": "uwj",
                   "ý": "ys" , "ỳ": "yf" , "ỷ": "yr" , "ỹ": "yx" , "ỵ": "yj" ,
    }
}

def xoa_dau_sang_vni_telex(txt: str, kieu_go: str) -> str:
    kieu_go = kieu_go.lower()
    if kieu_go not in BANG_DANH_DAU:
        raise Exception("kiểu gõ ko hợp lệ")
    for k, v in BANG_DANH_DAU[kieu_go].items():
        txt = txt.replace(k, v)
    return txt


print(xoa_dau_sang_vni_telex(txt, "telex"))
xoa_dau_sang_vni_telex(txt, "vni")   # "“D9a5o d9u71c kinh”"
xoa_dau_sang_vni_telex(txt, "telex") # "“DDajo dduwsc kinh”"





pygame.init()
# set the window screen size
display_screen = pygame.display.set_mode((500, 500))

# add some text
text = 'Hello Guys!!'

# add default font style with font
# size
font = pygame.font.Font("Resources/Fonts/arial.ttf", 40)

# render the text
img = font.render(text, True, (255, 0, 0))

rect = img.get_rect()
rect.topleft = (20, 20)
cursor = pygame.Rect(rect.topright, (3, rect.height))

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # detect if key is physically
        # pressed down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and event.unicode == "\x08":
                if len(text) > 0:
                    # stores the text except last
                    # character
                    text = text[:-1]
            else:
                text += xoa_dau_sang_vni_telex(event.unicode, "telex")[-1]
                print(event.key, event.unicode, event.scancode, event.mod, sep=" | ")
            img = font.render(text, True, (255, 0, 0))
            rect.size = img.get_size()
            cursor.topleft = rect.topright

    # Add background color to the window screen
    display_screen.fill((200, 255, 200))
    display_screen.blit(img, rect)

    # cursor is made to blink after every 0.5 sec
    if time.time() % 1 > 0.5:
        pygame.draw.rect(display_screen, (255, 0, 0), cursor)

    # update display
    pygame.display.update()

pygame.quit()