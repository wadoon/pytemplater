<%
from tplinput  import cread, TextInput, Line, LongTextInput      

author, version, email, desc = cread(
	Line('Enter values for the template script.sh'),
	TextInput('Author:','Alexander Weigl'),
	TextInput('Version:','1.0'),
	TextInput('E-Mail','alexweigl@gmail.com'),
	LongTextInput('Beschreibung')	
)

desc = "\n# ".join( desc.split("\n") )

%>
#!/bin/bash
#
# File: ${output_file} - ${version}
# 
# Author: ${author} <${email}>
# Date:   ${now}

#--[ Purpose ]------------------------------------------------------------------
# ${desc}
 
#--[ History ]------------------------------------------------------------------
# ${now.date()} ${version} ${author[0:15]}: initial comment 




