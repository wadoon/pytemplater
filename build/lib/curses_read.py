import urwid.curses_display
import urwid

__all__=['cread', 'Line', 'TestInput', 'LongTextInput', 'IntInput', 'BoolInput']

def cread(*args):
    """
    display a curses window. the user can enter values for each Input arg.
    @return a tuple with value in the given order from the args
    """
    ui = CursesUI(*args)
    ui.main()
    return [x.value for x in ui.inputs if type(x) is  not Line]

def attr_input(widget):
    return urwid.AttrWrap(widget,"input")

def attr_prompt(text):
    return urwid.AttrWrap(urwid.Text(text),"prompt")

def line(text, in_widget):
    pmpt = attr_prompt(text)
    widget = attr_input(in_widget)
    return urwid.Columns((pmpt,widget))

class Line(object):
    def __init__(self, prompt):
        self.prompt = prompt

    def toUi(self):  return attr_prompt(self.prompt)
    def retrValue(self):pass
###############################################################################
class Input(Line):
    def __init__(self,prompt, default=None):
        Line.__init__(self, prompt)
        self.value = default
###############################################################################
class IntInput(Input):
    def __init__(self,prompt, default = 0):
        Input.__init__(self,prompt,default)

    def toUi(self):
        self.widget =  urwid.IntEdit(
            default = int(self.value) )
        return line(self.prompt, self.widget)

    def retrValue(self):
        self.value = int(self.widget.get_text()[0])
###############################################################################
class TextInput(Input):
    def __init__(self,prompt, default=""):
        Input.__init__(self,prompt,default)

    def toUi(self):
        self.widget = urwid.Edit( "" , self.value , multiline=False)
        return line(self.prompt, self.widget )

    def retrValue(self):
        self.value = self.widget.get_text()[0]
###############################################################################
class LongTextInput(Input):
    def __init__(self,prompt, default=""):
        Input.__init__(self,prompt,default)

    def toUi(self):
        self.widget = urwid.Edit( "" , self.value , multiline=True)
        pmpt = attr_prompt(self.prompt)
        widget = attr_input( self.widget )
        return urwid.Pile((pmpt,widget))

    def retrValue(self):
        self.value = self.widget.get_text()[0]
###############################################################################
class BoolInput(Input):
    def __init__(self,prompt, default=False):
        Input.__init__(self, prompt, default)
    
    def toUi(self):
        self.widget =  urwid.CheckBox("",
                               state = bool( self.value), 
                               on_state_change=self.on_state_change)

        return line(self.prompt,self.widget)

    def on_state_change(self,checkbox, newstate, user_data=None):
        self.value = newstate

    def retrValue(self): pass
                      
###############################################################################
###############################################################################
###############################################################################
class CursesUI(object):
	def __init__(self, *inputs):
            self.inputs = inputs
            self.uiInputs = [x.toUi() for x in self.inputs]
            self.uiInputs.append( 
                urwid.Button('Accept', on_press=self.checkInputs)
                )
            self.center = urwid.SimpleListWalker(self.uiInputs)
            self.listbox = urwid.ListBox(self.center)

            self.infoText = urwid.AttrWrap( 
                urwid.Text(''), 'info')

            header = urwid.AttrWrap( 
                urwid.Text("Press F8 to exit.") , 'header' )
        
            self.frame = urwid.Frame(self.listbox, header)
            self.exit=False

        def checkInputs(self, button=None, user_data=None):
            try:
                for input in self.inputs:
                    input.retrValue()
            except e:
                self.infoText.set_text(str(e))
                return false
            self.exit=True
            

	def main(self):
		self.ui = urwid.curses_display.Screen()
		self.ui.register_palette([
			('header', 'black', 'dark cyan', 'standout'),
			('input', 'default', 'black'),
			('prompt', 'yellow', 'black', 'bold'),
			('info', 'light red', 'dark cyan'),
			])
		self.ui.run_wrapper( self.run )
	
	def run(self):
		size = self.ui.get_cols_rows()

		while not self.exit:
			self.draw_screen( size )
			keys = self.ui.get_input()
			if "f8" in keys:
				break
			for k in keys:
                            if k == "window resize":
                                size = self.ui.get_cols_rows()
                                continue                            
                            self.frame.keypress( size, k )
                                
			
	def draw_screen(self, size):
		canvas = self.frame.render( size, focus=True )
		self.ui.draw_screen( size, canvas )

if __name__ == '__main__':
    print cread(
        TextInput('Name'),
        TextInput('Vorname'),
        LongTextInput(u"Hier koennen Sie einen langen Text eingeben"),
        IntInput('Alter'),
        BoolInput('Use Git?')
        )
