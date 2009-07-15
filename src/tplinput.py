"""
This module provides an simple interface for entering values from the command line.
It is coded in boundle with templater for using it within the templates.

Basic usage:

>>> lastname, firstname = read(TextInput('Lastname:','Firstname:')
Lastname: Bar
Firstname: Foo
>>> print(firstname, lastname)
Foo Bar

You can choose between ``read`` and ``cread`` for asking values.
``read`` uses a simple command line with ``print`` and ``input()``.
``cread`` will be show an curses interface
"""

__all__=['cread', 'Line', 'TextInput', 'LongTextInput',
         'IntInput', 'BoolInput', 'read', 'PyInput']
__version__='1.1'


import abc

def read(*args):
    """ Asking the user after the given values on the command line interface.
    
    ``*args`` is an list of Line, TextInput, LongTextInput, IntInput, BoolInput, PyInput

    @return an tuple with the values asking for 
    """
    output = []
    for input in args:
        # ignore only output lines
        if type(input) is Line: 
            input.read(); continue
        output.append(input.read())
    return output


def cread(*args):
    """Display a curses window. the user can enter values for each input arg.
    ``*args`` is an list of Line,TextInput,LongTextInput, IntInput, BoolInput,PyInput
    @return a tuple with value in the given order from the args
    """
    
    import urwid.curses_display
    import urwid

    ui = CursesUI(*args)
    ui.main()
    return [x.value for x in ui.inputs if type(x) is not Line]

#############################################################################
## Urwid Helper functions
def attr_input(widget):
    return urwid.AttrWrap(widget,"input")

def attr_prompt(text):
    return urwid.AttrWrap(urwid.Text(text),"prompt")

def line(text, in_widget):
    pmpt = attr_prompt(text)
    widget = attr_input(in_widget)
    return urwid.Columns((pmpt,widget))

###########################################################
##

class Input(object):
    __metaclass__=abc.ABCMeta
    def __init__(self,prompt, default=None):
        Line.__init__(self, prompt)
        self.value = default
        
    @abc.abstractmethod
    def read(self): pass 

###############################################################################
    
class Line(Input):
    """Represent an simple comment line in the interface. For printing additional
    informations or instructions."""
    def __init__(self, prompt):
        """
        ``prompt`` information to be printed
        """
        self.prompt = prompt

    def toUi(self):  return attr_prompt(self.prompt)
    def retrValue(self):pass
    def read(self):
        print self.prompt        

        
###############################################################################
class IntInput(Input):
    """ Asking for an Integer input)
    ``prompt`` - Label to be shown
    ``default`` - default value (defaults to 0)
    """
    def __init__(self,prompt, default = 0):
        Input.__init__(self,prompt,default)
        
    def toUi(self):
        self.widget =  urwid.IntEdit(
            default = int(self.value) )
        return line(self.prompt, self.widget)

    def retrValue(self):
        self.value = int(self.widget.get_text()[0])
    
    def read(self):
        print self.prompt, 
        return int(raw_input())

###############################################################################
class TextInput(Input):
    """ The standard one single line string input
    ``prompt`` - Label to be shown
    ``default`` - default value (defaults to "")
    """
    def __init__(self,prompt, default=""):
        Input.__init__(self,prompt,default)

    def toUi(self):
        self.widget = urwid.Edit( "" , self.value , multiline=False)
        return line(self.prompt, self.widget )

    def retrValue(self):
        self.value = self.widget.get_text()[0]

    def read(self):
        print self.prompt, 
        s =  raw_input() 
        return s
        
###############################################################################
class LongTextInput(Input):
    """Asking for an multiline input, this will have to close with CTRL-D
    ``prompt`` - Label to be shown
    ``default`` - default value (defaults to "")
    """
    def __init__(self,prompt, default=""):
        Input.__init__(self,prompt,default)

    def toUi(self):
        self.widget = urwid.Edit( "" , self.value , multiline=True)
        pmpt = attr_prompt(self.prompt)
        widget = attr_input( self.widget )
        return urwid.Pile((pmpt,widget))

    def retrValue(self):
        self.value = self.widget.get_text()[0]

    def read(self):
        print self.prompt
        s = ''
        try:
            while True:
                s+=raw_input()
        except EOFError,e:
            pass
        return s
            
###############################################################################
class BoolInput(Input):
    """Asking for a true/false input
    User can insert every value. It will try to convert.
    If the conversion fails, the default value will be return.
    
    ``prompt`` - Label to be shown
    ``default`` - default value (defaults to False)
    """
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

    def read(self):
        print self.prompt,
        try:
            i = input()
            return bool(i)
        except:
            print "could not transform '%s' to an bool value" % i
            return self.default

###############################################################################
        
class PyInput(TextInput):
    """Asking for an one line input.
    The input will be parsed by python and an appropriate python object will be returnd.
    
    ``prompt`` - Label to be shown
    ``default`` - default value (defaults to None)
    """
    def __init__(self,prompt, default=None):
        TextInput.__init__(self, prompt, default)
    
    def retrValue(self):
        TextInput.retrValue(self)
        self.value = eval(self.value)

    def read(self):
        print self.prompt, 
        return eval( raw_input() )                      

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
			('input', 'white', 'black'),
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

