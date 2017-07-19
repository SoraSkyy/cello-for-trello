import urwid
import json

urwid.set_encoding("UTF-8")

f = open('data.json', 'rb')
data = json.loads(f.read().decode())
f.close()

def boardSelection():
    body = [urwid.Text('Boards'), urwid.Divider()]
    boardEntities = data.keys()
    for boardEntity in boardEntities:
        button = urwid.Button(data[boardEntity]['name'])
        urwid.connect_signal(button, 'click', toListView, boardEntity)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))
        
def toListSelection(button, boardEntity):
    setMainWidget(urwid.Overlay(urwid.Padding(listSelection(boardEntity), left=2, right=2), urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    align='center', width=('relative', 90),
    valign='middle', height=('relative', 90),
    min_width=20, min_height=9))

def listSelection(boardEntity):
    columns = []
    listEntities = data[boardEntity]['lists'].keys()
    for listEntity in listEntities:
        body = [urwid.Text(data[boardEntity]['lists'][listEntity]['name']),urwid.Divider()]
        cards = data[boardEntity]['lists'][listEntity]['cards']
        for index,card in enumerate(cards):
            button = urwid.Button(data[boardEntity]['lists'][listEntity]['cards'][index]['name'])
            urwid.connect_signal(button, 'click', toListView, boardEntity)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        columns.append((20,urwid.ListBox(urwid.SimpleFocusListWalker(body))))
    return columns
    

    
def toListView(button, boardEntity):
    setMainWidget(urwid.Overlay(urwid.Columns(listSelection(boardEntity),1,None), urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    align='center', width=('relative', 90),
    valign='middle', height=('relative', 90),
    min_width=20, min_height=9))
    
def exit_program(button):
    raise urwid.ExitMainLoop()

def setMainWidget(newWidget):
    loop.widget = newWidget

main = urwid.Padding(boardSelection(), left=2, right=2)
top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    align='center', width=('relative', 60),
    valign='middle', height=('relative', 60),
    min_width=20, min_height=9)
loop = urwid.MainLoop(top, palette=[('reversed', 'standout', '')])
loop.run()
