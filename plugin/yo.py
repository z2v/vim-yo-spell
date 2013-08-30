## -*- coding: utf-8 -*-
import vim

## Import part {{{1
try: import text
except ImportError:
    raise ImportError(
            "This module available only from Vim editor, only with text module"
            )
reload(text)
try:
    if text.HEXVERSION < 0x10003: raise "Too old text module"
except AttributeError:
    raise "Too old text module"

import shelve, os, os.path

def fix_case(first, second):
    """\
    fix_case(first, second) -> string or None

    look to case of FIRST argument and return SECOND argument in sane
    case. But if the case can't recognized, return None
    """
    if   first.islower(): return second.lower()
    elif first.istitle(): return second.title()
    elif first.isupper(): return second.upper()

def read_dat(yo_path, encoding):
    print unicode("Подождите пока я зачитаю базу %(yo)s.dat, это недолго...\n"
            % {"yo":yo_path}, "utf-8").encode(encoding)
    sh = shelve.open(yo_path+".dat")
    MAY_BE_YO = sh["may_be_yo"]
    ONLY_YO   = sh["only_yo"]
    sh.close()
    return MAY_BE_YO, ONLY_YO

def yo_cmp(one, two):
    if one.startswith(u"*"): one = one[2:]
    if two.startswith(u"*"): two = two[2:]
    for i,j in zip(one, two):
        if i==j: continue
        elif ord(i) not in [1025, 1105] and ord(j) not in [1025, 1105]:
            return cmp(i, j)
        elif ord(i)==1105:        # ё
            if ord(j) <= 1077: return  1
            else             : return -1
        elif ord(i)==1025:        # Ё
            if ord(j) <= 1045: return  1
            else             : return -1
        elif ord(j)==1105:
            if ord(i) <= 1077: return -1
            else             : return  1
        elif ord(j)==1025:
            if ord(i) <= 1045: return -1
            else             : return  1
    else:
        if len(one) < len(two): return -1
        else                  : return  1

def repare_txt(MAY_BE_YO, ONLY_YO, yo_path):
    text._print_warning(unicode("Warning! Нет файла %(yo)s.txt,\n"
            "подождите пока я восстановлю его. Это долго...\n" %\
                    {"yo":yo_path.replace("\\","\\\\")},
            "utf-8").encode(buffer.encoding))

    yo_txt = file(yo_path+".txt", "wt")
    yo_list = map(lambda x: u"* "+x, MAY_BE_YO.values()) + ONLY_YO.values()
    yo_list.sort(yo_cmp)
    yo_txt.write("\n".join(yo_list).encode("utf-8"))
    yo_txt.close()

## }}}

def repare_dat(yo_path, encoding):
    print unicode("База %(yo)s.dat неготова к работе, возможно это первый\n"
            "запуск программы, или файл %(yo)s.txt новее %(yo)s.dat.\nНадо "
            "подождать, это может занять пару десятков секунд...\n" %
                    {"yo":yo_path},
            "utf-8").encode(encoding)
    YO = unicode("ё", "utf-8")
    E  = unicode("е", "utf-8")
    LIST = file(yo_path+".txt", "rt").readlines()
    MAY_BE_YO, ONLY_YO = {}, {}
    for i in LIST:
        i=unicode(i.strip(), "utf-8")
        if i.startswith(u"*"):
            MAY_BE_YO[i[2:].replace(YO, E)] = i[2:]
        else:
            ONLY_YO[i.replace(YO, E)] = i
    if os.path.isfile(yo_path+".dat"):
        os.remove(yo_path+".dat")
    sh = shelve.open(yo_path+".dat")
    sh["may_be_yo"] = MAY_BE_YO
    sh["only_yo"] = ONLY_YO
    sh.close()
    return MAY_BE_YO, ONLY_YO


def main():
    yo_path = os.path.splitext(vim.eval('g:vim_yo_spell_dict'))[0]

    buffer = text.Text()
    E_WORD = buffer.re.compile(ur"\b\w*[\u0435\u0415]\w*\b")

    _exit = False

    if (os.path.isfile(yo_path+".dat") and os.path.isfile(yo_path+".txt") and\
            os.stat(yo_path+".dat").st_mtime >= os.stat(yo_path+".txt").st_mtime) or\
            os.path.isfile(yo_path+".dat") and not os.path.isfile(yo_path+".txt"):
        # Если есть yo.dat и yo.txt, причём yo.dat моложе
        # или
        # есть yo.dat, но нет yo.txt

        if not "MAY_BE_YO" in dir() or not "ONLY_YO" in dir():
            MAY_BE_YO, ONLY_YO = read_dat(yo_path, buffer.encoding)

        if not os.path.isfile(yo_path+".txt"):
            repare_txt(MAY_BE_YO, ONLY_YO, yo_path)

    elif os.path.isfile(yo_path+".txt") and\
        (not os.path.isfile(yo_path+".dat") or\
        (   os.path.isfile(yo_path+".dat") and\
            os.stat(yo_path+".dat").st_mtime < os.stat(yo_path+".txt").st_mtime)):
        # Если есть yo.txt
        # и
        # нет yo.dat или он есть, но старый

        MAY_BE_YO, ONLY_YO = repare_dat(yo_path, buffer.encoding)

    else:
        import sys
        sys.stderr.write(unicode("Не обнаружено ни %(yo)s, ни %(yo)s"%{"yo":yo_path},
            "utf-8").encode(buffer.encoding))
        _exit = True
    yo, i, s, e = None, None, None, None

    ## }}}
    ## Prepearing part {{{1

    if not _exit:
        for i in buffer.re.finditer(E_WORD):
            try:
                yo = fix_case(i.mo.group(), ONLY_YO[i.mo.group().lower()])
                if yo:
                    s,e = i.span()
                    buffer[s:e] = yo
            except KeyError:
                try:
                    yo = fix_case(i.mo.group(), MAY_BE_YO[i.mo.group().lower()])
                    if yo:
                        s,e = i.span()
                        buffer.replace_i(s,e,[yo])
                except KeyError:
                    pass
                except buffer.exceptions.CancelDialog:
                    break
    ## }}}
    ## del instraction. This is important for vim {{{1

    #del yo, s, e, buffer, i, yo_path, repare_txt, repare_dat, fix_case, yo_cmp
    #del read_dat, base_encoding, E_WORD, _exit
    # we don't delete MAY_BE_YO, ONLY_YO: for futere sessions

    ## }}}

## vim: fdm=marker
